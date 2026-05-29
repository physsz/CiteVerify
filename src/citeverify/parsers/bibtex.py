from __future__ import annotations

from typing import Any

import bibtexparser  # type: ignore[import-untyped]

from citeverify.models import ParsedReference, SourceFormat
from citeverify.normalize.author import parse_author_list
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import normalize_issn
from citeverify.normalize.pages import normalize_article_number, normalize_pages


def _first_present(entry: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = entry.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def _parse_year(value: str | None) -> int | None:
    if not value:
        return None
    for token in value.replace("{", "").replace("}", "").split():
        if token.isdigit() and len(token) == 4:
            return int(token)
    return None


def parse_bibtex(text: str) -> list[ParsedReference]:
    parsed = bibtexparser.loads(text)
    references: list[ParsedReference] = []
    for index, entry in enumerate(parsed.entries, start=1):
        reference_id = str(entry.get("ID") or f"ref-{index}")
        venue = _first_present(entry, "journal", "journaltitle", "booktitle")
        issn_value = _first_present(entry, "issn")
        issn = [normalized for normalized in [normalize_issn(issn_value)] if normalized]
        references.append(
            ParsedReference(
                reference_id=reference_id,
                raw_text=str(entry),
                title=_first_present(entry, "title"),
                authors=parse_author_list(_first_present(entry, "author")),
                year=_parse_year(_first_present(entry, "year", "date")),
                venue=venue,
                issn=issn,
                volume=_first_present(entry, "volume"),
                issue=_first_present(entry, "number", "issue"),
                pages=normalize_pages(_first_present(entry, "pages")),
                article_number=normalize_article_number(
                    _first_present(entry, "eid", "article-number", "articleno")
                ),
                doi=normalize_doi(_first_present(entry, "doi")),
                arxiv_id=_first_present(entry, "eprint", "arxivid"),
                pmid=_first_present(entry, "pmid"),
                isbn=_first_present(entry, "isbn"),
                url=_first_present(entry, "url"),
                source_format=SourceFormat.BIBTEX,
            )
        )
    return references
