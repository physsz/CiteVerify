from __future__ import annotations

import re

from citeverify.normalize.text import normalize_basic_text

JOURNAL_ALIASES = {
    "prl": "physical review letters",
    "phys rev lett": "physical review letters",
    "physical review letters": "physical review letters",
    "phys rev a": "physical review a",
    "physical review a": "physical review a",
    "phys rev b": "physical review b",
    "physical review b": "physical review b",
    "nature": "nature",
    "science": "science",
    "pnas": "proceedings of the national academy of sciences",
    "proc natl acad sci usa": "proceedings of the national academy of sciences",
}


def normalize_issn(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    value = re.sub(r"[^0-9X]", "", value)
    if len(value) == 8:
        return f"{value[:4]}-{value[4:]}"
    return value or None


def normalize_journal(value: str | None) -> str | None:
    if not value:
        return None
    normalized = normalize_basic_text(value)
    normalized = normalized.replace(".", "")
    normalized = re.sub(r"\bjournal\b", "journal", normalized)
    normalized = normalized.strip()
    return JOURNAL_ALIASES.get(normalized, normalized) or None
