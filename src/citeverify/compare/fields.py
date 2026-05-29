from __future__ import annotations

from collections.abc import Callable
from typing import Any

from citeverify.compare.authors import compare_authors
from citeverify.models import (
    ComparisonResult,
    FieldComparison,
    ParsedReference,
    RegistryRecord,
)
from citeverify.normalize.arxiv import extract_arxiv_id, is_arxiv_venue
from citeverify.normalize.doi import extract_doi, normalize_doi
from citeverify.normalize.journal import (
    normalize_journal,
    venues_compatible,
)
from citeverify.normalize.pages import (
    normalize_article_number,
    normalize_pages,
    pages_compatible,
)
from citeverify.normalize.title import titles_match


def compare_references(
    input_reference: ParsedReference,
    found_record: RegistryRecord,
) -> list[FieldComparison]:
    comparisons = [
        _compare_field(
            "doi",
            input_reference.doi,
            found_record.doi,
            lambda value: normalize_doi(str(value)),
        ),
        _compare_title(input_reference.title, found_record.title),
        compare_authors(input_reference.authors, found_record.authors),
        _compare_field("year", input_reference.year, found_record.year, str),
        _compare_venue(input_reference, found_record),
        _compare_field("volume", input_reference.volume, found_record.volume, _clean),
        _compare_field("issue", input_reference.issue, found_record.issue, _clean),
        _compare_pages(
            input_reference.pages,
            found_record.pages,
            found_record.article_number,
        ),
        _compare_field(
            "article_number",
            input_reference.article_number,
            found_record.article_number,
            lambda value: normalize_article_number(str(value)),
        ),
        _compare_field(
            "arxiv_id", input_reference.arxiv_id, found_record.arxiv_id, _clean
        ),
        _compare_field("pmid", input_reference.pmid, found_record.pmid, _clean),
        _compare_field("isbn", input_reference.isbn, found_record.isbn, _clean),
    ]
    return [
        comparison
        for comparison in comparisons
        if comparison.result != ComparisonResult.ADDITIONAL_METADATA
        or comparison.found_value not in (None, "", [], {})
    ]


def mismatches(comparisons: list[FieldComparison]) -> list[FieldComparison]:
    return [
        comparison
        for comparison in comparisons
        if comparison.result == ComparisonResult.MISMATCH
    ]


def _compare_title(input_value: str | None, found_value: str | None) -> FieldComparison:
    if input_value in (None, "") and found_value not in (None, ""):
        return FieldComparison(
            field="title",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.ADDITIONAL_METADATA,
        )
    if input_value not in (None, "") and found_value in (None, ""):
        return FieldComparison(
            field="title",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
            note="lookup source did not return this field",
        )
    if input_value in (None, ""):
        return FieldComparison(
            field="title",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
        )
    return FieldComparison(
        field="title",
        input_value=input_value,
        found_value=found_value,
        result=ComparisonResult.MATCH
        if titles_match(input_value, found_value)
        else ComparisonResult.MISMATCH,
    )


def _compare_venue(
    input_reference: ParsedReference, found_record: RegistryRecord
) -> FieldComparison:
    if is_arxiv_venue(input_reference.venue):
        found_arxiv_id = found_record.arxiv_id or extract_arxiv_id(
            found_record.doi,
            found_record.url,
            found_record.source_record_url,
            found_record.venue,
        )
        if is_arxiv_venue(found_record.venue) or found_arxiv_id:
            return FieldComparison(
                field="venue",
                input_value=input_reference.venue,
                found_value=found_record.venue,
                result=ComparisonResult.MATCH,
                note="both records identify an arXiv/preprint venue",
            )
        if found_record.venue in (None, ""):
            return FieldComparison(
                field="venue",
                input_value=input_reference.venue,
                found_value=found_record.venue,
                result=ComparisonResult.NOT_CHECKED,
                note="lookup source did not return this field",
            )
        return FieldComparison(
            field="venue",
            input_value=input_reference.venue,
            found_value=found_record.venue,
            result=ComparisonResult.MISMATCH,
            note="input venue is arXiv/preprint; found venue is a publication venue",
        )
    if venues_compatible(
        input_reference.venue,
        found_record.venue,
        input_reference.volume,
        found_record.volume,
    ):
        return FieldComparison(
            field="venue",
            input_value=input_reference.venue,
            found_value=found_record.venue,
            result=ComparisonResult.MATCH,
            note=(
                "venue matched after accounting for volume"
                if normalize_journal(input_reference.venue)
                != normalize_journal(found_record.venue)
                else None
            ),
        )
    return _compare_field(
        "venue",
        input_reference.venue,
        found_record.venue,
        lambda value: normalize_journal(str(value)),
    )


def _compare_pages(
    input_value: str | None,
    found_pages: str | None,
    found_article_number: str | None = None,
) -> FieldComparison:
    found_value = found_pages
    found_is_article_number = False
    if (
        input_value not in (None, "")
        and found_value in (None, "")
        and found_article_number not in (None, "")
    ):
        found_value = found_article_number
        found_is_article_number = True
    if input_value in (None, "") and found_value not in (None, ""):
        return FieldComparison(
            field="pages",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.ADDITIONAL_METADATA,
        )
    if input_value not in (None, "") and found_value in (None, ""):
        return FieldComparison(
            field="pages",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
            note="lookup source did not return this field",
        )
    if input_value in (None, ""):
        return FieldComparison(
            field="pages",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
        )
    compatible = pages_compatible(input_value, found_value)
    return FieldComparison(
        field="pages",
        input_value=input_value,
        found_value=found_value,
        result=ComparisonResult.MATCH if compatible else ComparisonResult.MISMATCH,
        note=(
            "input pages matched found article number"
            if compatible
            and found_is_article_number
            and normalize_pages(input_value) == normalize_article_number(found_value)
            else (
                "page range and first page are compatible"
                if compatible
                and normalize_pages(input_value) != normalize_pages(found_value)
                else None
            )
        ),
    )


def _compare_url(input_value: str | None, found_value: str | None) -> FieldComparison:
    if input_value in (None, "") and found_value not in (None, ""):
        return FieldComparison(
            field="url",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.ADDITIONAL_METADATA,
        )
    if input_value not in (None, "") and found_value in (None, ""):
        return FieldComparison(
            field="url",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
            note="lookup source did not return this field",
        )
    if input_value in (None, ""):
        return FieldComparison(
            field="url",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
        )
    input_doi = extract_doi(input_value or "")
    found_doi = extract_doi(found_value or "")
    if input_doi and found_doi and input_doi == found_doi:
        return FieldComparison(
            field="url",
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.MATCH,
            note="both URLs contain the same DOI",
        )
    return FieldComparison(
        field="url",
        input_value=input_value,
        found_value=found_value,
        result=ComparisonResult.MATCH
        if _clean(input_value) == _clean(found_value)
        else ComparisonResult.MISMATCH,
    )


def _compare_field(
    field: str,
    input_value: Any,
    found_value: Any,
    normalizer: Callable[[Any], Any],
) -> FieldComparison:
    if input_value in (None, "", [], {}) and found_value not in (None, "", [], {}):
        return FieldComparison(
            field=field,
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.ADDITIONAL_METADATA,
        )
    if input_value not in (None, "", [], {}) and found_value in (None, "", [], {}):
        return FieldComparison(
            field=field,
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
            note="lookup source did not return this field",
        )
    if input_value in (None, "", [], {}):
        return FieldComparison(
            field=field,
            input_value=input_value,
            found_value=found_value,
            result=ComparisonResult.NOT_CHECKED,
        )
    return FieldComparison(
        field=field,
        input_value=input_value,
        found_value=found_value,
        result=ComparisonResult.MATCH
        if normalizer(input_value) == normalizer(found_value)
        else ComparisonResult.MISMATCH,
    )


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower() or None
