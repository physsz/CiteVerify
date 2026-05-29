from __future__ import annotations

import re

DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)


def extract_doi(value: str) -> str | None:
    match = DOI_PATTERN.search(value)
    if match is None:
        return None
    return normalize_doi(match.group(0))


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    value = value.strip().strip("<>")
    value = value.rstrip(".,;)")
    return value.lower() or None
