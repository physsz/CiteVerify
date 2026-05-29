from __future__ import annotations

import re

from citeverify.models import ParsedReference, SourceFormat
from citeverify.normalize.arxiv import extract_arxiv_id
from citeverify.normalize.author import parse_author_list
from citeverify.normalize.doi import extract_doi

YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
NUMBERED_REFERENCE_PATTERN = re.compile(r"^\s*(?:\[\d+\]|\d+[.)])\s*")


def split_raw_references(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.splitlines()]
    references: list[str] = []
    current: list[str] = []
    saw_numbering = any(NUMBERED_REFERENCE_PATTERN.match(line) for line in lines)

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current and not saw_numbering:
                references.append(" ".join(current).strip())
                current = []
            continue
        if saw_numbering and NUMBERED_REFERENCE_PATTERN.match(line):
            if current:
                references.append(" ".join(current).strip())
            current = [NUMBERED_REFERENCE_PATTERN.sub("", stripped)]
        else:
            current.append(stripped)

    if current:
        references.append(" ".join(current).strip())
    return [reference for reference in references if reference]


def _extract_year(value: str) -> int | None:
    match = YEAR_PATTERN.search(value)
    return int(match.group(0)) if match else None


def _extract_quoted_title(value: str) -> str | None:
    match = re.search(r'"([^"]{8,})"', value)
    if match:
        return match.group(1).strip()
    match = re.search(r"“([^”]{8,})”", value)
    if match:
        return match.group(1).strip()
    return None


def _extract_author_prefix(value: str) -> str | None:
    year_match = YEAR_PATTERN.search(value)
    prefix = value[: year_match.start()] if year_match else value[:120]
    prefix = prefix.strip(" ,.;")
    if not prefix:
        return None
    return prefix


def parse_raw_text(text: str) -> list[ParsedReference]:
    references: list[ParsedReference] = []
    for index, raw_reference in enumerate(split_raw_references(text), start=1):
        author_prefix = _extract_author_prefix(raw_reference)
        references.append(
            ParsedReference(
                reference_id=f"ref-{index}",
                raw_text=raw_reference,
                title=_extract_quoted_title(raw_reference),
                authors=parse_author_list(author_prefix),
                year=_extract_year(raw_reference),
                doi=extract_doi(raw_reference),
                arxiv_id=extract_arxiv_id(raw_reference),
                source_format=SourceFormat.RAW_TEXT,
            )
        )
    return references
