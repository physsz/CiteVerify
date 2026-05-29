from __future__ import annotations

from citeverify.models import IdentifierCandidate, IdentifierKind, ParsedReference
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.title import normalize_title


def build_identifier_candidates(
    reference: ParsedReference,
) -> list[IdentifierCandidate]:
    candidates: list[IdentifierCandidate] = []
    if reference.doi:
        normalized = normalize_doi(reference.doi)
        if normalized:
            candidates.append(
                IdentifierCandidate(
                    kind=IdentifierKind.DOI,
                    value=reference.doi,
                    normalized_value=normalized,
                    available_fields=_available_fields(reference),
                )
            )
    if reference.arxiv_id:
        candidates.append(
            IdentifierCandidate(
                kind=IdentifierKind.ARXIV_ID,
                value=reference.arxiv_id,
                normalized_value=reference.arxiv_id.strip().lower(),
                available_fields=_available_fields(reference),
            )
        )
    if reference.pmid:
        candidates.append(
            IdentifierCandidate(
                kind=IdentifierKind.PMID,
                value=reference.pmid,
                normalized_value=reference.pmid.strip(),
                available_fields=_available_fields(reference),
            )
        )
    if reference.title:
        normalized_title = normalize_title(reference.title)
        if normalized_title:
            candidates.append(
                IdentifierCandidate(
                    kind=IdentifierKind.TITLE,
                    value=reference.title,
                    normalized_value=normalized_title,
                    available_fields=_available_fields(reference),
                )
            )
    locator = reference.journal_locator()
    if locator.has_lookup_value():
        candidates.append(
            IdentifierCandidate(
                kind=IdentifierKind.JOURNAL_LOCATOR,
                value=locator.model_dump_json(),
                normalized_value=locator.model_dump_json(),
                available_fields=_available_fields(reference),
            )
        )
    if reference.url:
        candidates.append(
            IdentifierCandidate(
                kind=IdentifierKind.URL,
                value=reference.url,
                normalized_value=reference.url.strip().lower(),
                available_fields=_available_fields(reference),
            )
        )
    return candidates


def _available_fields(reference: ParsedReference) -> list[str]:
    fields = []
    for field in [
        "doi",
        "title",
        "authors",
        "year",
        "venue",
        "issn",
        "volume",
        "issue",
        "pages",
        "article_number",
        "arxiv_id",
        "pmid",
        "isbn",
        "url",
    ]:
        value = getattr(reference, field)
        if value not in (None, "", [], {}):
            fields.append(field)
    return fields
