from __future__ import annotations

import re


def normalize_pages(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"\s*--?\s*", "-", value)
    value = value.strip(" .,")
    return value or None


def normalize_article_number(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().strip(" .,")
    return value or None
