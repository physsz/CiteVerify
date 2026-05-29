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


def pages_compatible(input_value: str | None, found_value: str | None) -> bool:
    input_pages = normalize_pages(input_value)
    found_pages = normalize_pages(found_value)
    if not input_pages or not found_pages:
        return False
    if input_pages == found_pages:
        return True

    input_start, input_end = _page_bounds(input_pages)
    found_start, found_end = _page_bounds(found_pages)
    if input_start != found_start:
        return False
    if input_end is None or found_end is None:
        return True
    return input_end == found_end


def normalize_article_number(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().strip(" .,")
    return value or None


def _page_bounds(value: str) -> tuple[str, str | None]:
    if "-" not in value:
        return value.lower(), None
    start, end = value.split("-", 1)
    start = start.strip().lower()
    end = end.strip().lower()
    return start, end if end and end != start else None
