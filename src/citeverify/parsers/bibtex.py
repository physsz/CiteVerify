from __future__ import annotations

from typing import Any

import bibtexparser  # type: ignore[import-untyped]

from citeverify.models import ParsedReference, SourceFormat
from citeverify.normalize.arxiv import extract_arxiv_id, normalize_arxiv_id
from citeverify.normalize.author import parse_author_list
from citeverify.normalize.doi import extract_doi, normalize_doi
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


def _non_arxiv_volume(value: str | None) -> str | None:
    if not value:
        return None
    if value.strip().lower().startswith("abs/") and normalize_arxiv_id(value):
        return None
    return value


def parse_bibtex(text: str) -> list[ParsedReference]:
    parsed = bibtexparser.loads(text)
    references: list[ParsedReference] = []
    for index, entry in enumerate(parsed.entries, start=1):
        reference_id = str(entry.get("ID") or f"ref-{index}")
        venue = _first_present(entry, "journal", "journaltitle", "booktitle")
        url = _first_present(entry, "url")
        doi = normalize_doi(_first_present(entry, "doi")) or extract_doi(url or "")
        arxiv_id = (
            normalize_arxiv_id(_first_present(entry, "eprint", "arxivid"))
            or extract_arxiv_id(
                _first_present(entry, "doi"),
                url,
                venue,
                str(entry),
            )
        )
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
                volume=_non_arxiv_volume(_first_present(entry, "volume")),
                issue=_first_present(entry, "number", "issue"),
                pages=normalize_pages(_first_present(entry, "pages")),
                article_number=normalize_article_number(
                    _first_present(entry, "eid", "article-number", "articleno")
                ),
                doi=doi,
                arxiv_id=arxiv_id,
                pmid=_first_present(entry, "pmid"),
                isbn=_first_present(entry, "isbn"),
                url=url,
                source_format=SourceFormat.BIBTEX,
            )
        )
    return references
