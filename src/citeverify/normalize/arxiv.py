from __future__ import annotations

import re

ARXIV_NEW_PATTERN = re.compile(r"\b\d{4}\.\d{4,5}(?:v\d+)?\b", re.IGNORECASE)
ARXIV_OLD_PATTERN = re.compile(
    r"\b[a-z-]+(?:\.[a-z-]+)?/\d{7}(?:v\d+)?\b", re.IGNORECASE
)
ARXIV_DOI_PATTERN = re.compile(
    r"\b10\.48550/arxiv\.([a-z-]+(?:\.[a-z-]+)?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?\b",
    re.IGNORECASE,
)


def normalize_arxiv_id(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\.pdf$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^arxiv:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^arxiv\s+preprint\s+arxiv:\s*", "", value, flags=re.IGNORECASE)
    doi_match = ARXIV_DOI_PATTERN.search(value)
    if doi_match:
        value = doi_match.group(1)
    else:
        new_match = ARXIV_NEW_PATTERN.search(value)
        old_match = ARXIV_OLD_PATTERN.search(value)
        if new_match:
            value = new_match.group(0)
        elif old_match:
            value = old_match.group(0)
    value = re.sub(r"v\d+$", "", value, flags=re.IGNORECASE)
    value = value.strip().strip(" .;,")
    if ARXIV_NEW_PATTERN.fullmatch(value) or ARXIV_OLD_PATTERN.fullmatch(value):
        return value.lower()
    return None


def extract_arxiv_id(*values: str | None) -> str | None:
    for value in values:
        if not value:
            continue
        doi_match = ARXIV_DOI_PATTERN.search(value)
        if doi_match:
            normalized = normalize_arxiv_id(doi_match.group(1))
            if normalized:
                return normalized
        new_match = ARXIV_NEW_PATTERN.search(value)
        if new_match and _near_arxiv_marker(value, new_match.start()):
            normalized = normalize_arxiv_id(new_match.group(0))
            if normalized:
                return normalized
        old_match = ARXIV_OLD_PATTERN.search(value)
        if old_match and _near_arxiv_marker(value, old_match.start()):
            normalized = normalize_arxiv_id(old_match.group(0))
            if normalized:
                return normalized
    return None


def arxiv_doi(arxiv_id: str | None) -> str | None:
    normalized = normalize_arxiv_id(arxiv_id)
    if not normalized:
        return None
    return f"10.48550/arxiv.{normalized}"


def is_arxiv_venue(value: str | None) -> bool:
    if not value:
        return False
    return "arxiv" in value.lower()


def _near_arxiv_marker(value: str, match_start: int) -> bool:
    prefix = value[max(0, match_start - 40) : match_start].lower()
    return "arxiv" in prefix or "oai:arxiv.org:" in prefix
