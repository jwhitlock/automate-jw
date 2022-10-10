#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from json import dumps
from typing import Optional, Union
from urllib.parse import urlparse

import requests


@dataclass
class OmnifocusTask:
    action: str
    flag: bool = False
    project: str = ""
    tags: list[str] = field(default_factory=list)
    note: str = ""
    start_date: Optional[Union[date, datetime]] = None
    due_date: Optional[Union[date, datetime]] = None
    estimate: str = ""

    def __str__(self) -> str:
        def escape_str(in_str: str) -> str:
            trouble_chars = "/#:!@$"
            out_str = in_str
            for c in trouble_chars:
                out_str = out_str.replace(c, f"\\{c}")
            return out_str

        sections: list[str] = []

        assert self.action
        safe_action = escape_str(self.action)
        task_bits: list[str] = [safe_action]
        if self.flag:
            task_bits.append("!")
        if self.project:
            task_bits.extend(("::", escape_str(self.project)))
        sections.append("".join(task_bits))

        start_date = self.start_date
        due_date = self.due_date
        if start_date and not due_date:
            due_date = start_date + timedelta(days=1)
        if start_date:
            sections.append(f"#{start_date.isoformat()}")
        if due_date:
            sections.append(f"#{due_date.isoformat()}")

        if self.estimate:
            sections.append(f"${escape_str(self.estimate)}")

        for tag in self.tags:
            sections.append(f"@{escape_str(tag)}")

        if self.note:
            safe_note = escape_str(self.note)
            sections.append(f"//{safe_note}")

        return " ".join(sections)

    def as_dict(self) -> dict[str, Union[bool, str, list[str]]]:
        ret: dict[str, Union[bool, str, list[str]]] = {"task": self.action}
        if self.flag:
            ret["flag"] = True
        if self.project:
            ret["project"] = self.project
        if self.tags:
            ret["tags"] = self.tags
        if self.start_date:
            ret["start_date"] = self.start_date.isoformat()
        if self.due_date:
            ret["due_date"] = self.due_date.isoformat()
        if self.estimate:
            ret["estimate"] = self.estimate
        if self.note:
            ret["note"] = self.note
        return ret

    def as_json(self) -> str:
        return dumps(self.as_dict())


Url = str


class RuleBase:
    def __init__(self, url: Url):
        self.url = url

    def is_match(self) -> bool:
        return False

    def as_task(self) -> OmnifocusTask:
        return OmnifocusTask(action="New Task")


class SubstackArticle(RuleBase):

    author_re = re.compile(
        r"""(?x)                        # Verbose mode
         <meta\s+                       # meta tag plus any whitespace
         name="author"\s+               # name=author tag
         content="(?P<author>[^"]*)"    # Author's name
         \s*/?>                         # end tag
        """
    )

    title_re = re.compile(
        r"""(?x)                        # Verbose mode
         <meta\s+                       # meta tag plus any whitespace
         (data-preact-helmet\s+)?       # data-preact-helmet attr
         property="og:title"\s+         # FB opengraph title
         content="(?P<title>[^"]*)"     # Post title
         \s*/?>                         # end tag
        """
    )

    abs_url_re = re.compile(
        r"""(?x)                        # Verbose mode
         <meta\s+                       # meta tag plus any whitespace
         property="og:url"\s+           # FB opengraph URL
         content="(?P<abs_url>[^"]*)"   # Absolute URL
         \s*/?>                         # end tag
        """
    )

    def is_match(self) -> bool:
        parts = urlparse(self.url)
        if parts.hostname:
            return parts.hostname.endswith("substack.com")
        return False

    def as_task(self) -> OmnifocusTask:
        page = requests.get(self.url).text
        author = "Unknown"
        title = "Unknown"
        abs_url = self.url
        issues = []

        author_match = self.author_re.search(page)
        if author_match:
            author = author_match["author"]
        else:
            issues.append('Could not find `<meta name="author">`')

        title_match = self.title_re.search(page)
        if title_match:
            title = title_match["title"]
        else:
            issues.append('Could not find `<meta property="og:title">`')

        abs_url_match = self.abs_url_re.search(page)
        if abs_url_match:
            abs_url = abs_url_match["abs_url"]
        else:
            issues.append('Could not find `<meta property="og:url">`')

        task = f'Read \\"{title}\\" by {author}'
        note = abs_url
        if issues:
            note += "\n\nPARSE ISSUES\n" + "\n".join(issues) + "\nEND OF PARSE ISSUES"

        return OmnifocusTask(
            action=task,
            note=note,
            tags=["Any Device", "Read"],
            project="Consume online content",
        )


class AnyURL(RuleBase):
    def is_match(self) -> bool:
        return True

    def as_task(self) -> OmnifocusTask:
        return OmnifocusTask(action=f"Read {self.url}", note=self.url, tags=["Laptop"])


RuleSet = list[type[RuleBase]]

DEFAULT_RULES: RuleSet = [
    SubstackArticle,
    AnyURL,
]


class NoMatchingRule(Exception):
    """No rule matched the URL."""


def process_url(url: Url, rules: Optional[RuleSet] = None) -> list(str):
    if rules is None:
        rules = DEFAULT_RULES
    for ruleClass in rules:
        rule = ruleClass(url)
        if rule.is_match:
            data = rule.as_task().as_json()
            return [f"omnifocus {data}"]
    raise NoMatchingRule(f"No rule matched {url}")
