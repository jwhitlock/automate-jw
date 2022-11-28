import re
from html import unescape
from urllib.parse import urlparse

import requests

from ..tasks import OmnifocusTask
from .base import RuleBase


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
            author = unescape(author_match["author"])
        else:
            issues.append('Could not find `<meta name="author">`')

        title_match = self.title_re.search(page)
        if title_match:
            title = unescape(title_match["title"])
        else:
            issues.append('Could not find `<meta property="og:title">`')

        abs_url_match = self.abs_url_re.search(page)
        if abs_url_match:
            abs_url = abs_url_match["abs_url"]
        else:
            issues.append('Could not find `<meta property="og:url">`')

        task = f'Read "{title}" by {author}'
        note = abs_url
        if issues:
            note += "\n\nPARSE ISSUES\n" + "\n".join(issues) + "\nEND OF PARSE ISSUES"

        return OmnifocusTask(
            action=task,
            note=note,
            tags=["Any Device", "Read"],
            project="Consume online content",
        )
