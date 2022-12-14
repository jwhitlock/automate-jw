#!/usr/bin/env python3
from base64 import b64encode
from typing import Optional

from .rules import AnyURL, RuleBase, SubstackArticle

RuleSet = list[type[RuleBase]]

DEFAULT_RULES: RuleSet = [
    SubstackArticle,
    AnyURL,
]


class NoMatchingRule(Exception):
    """No rule matched the URL."""


def process_url(url: str, rules: Optional[RuleSet] = None) -> list[str]:
    if rules is None:
        rules = DEFAULT_RULES
    for ruleClass in rules:
        rule = ruleClass(url)
        if rule.is_match():
            data = b64encode(rule.as_task().as_json().encode()).decode()
            return [f"omnifocus {data}"]
    raise NoMatchingRule(f"No rule matched {url}")
