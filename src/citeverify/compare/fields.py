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
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import normalize_issn, normalize_journal
from citeverify.normalize.pages import normalize_article_number, normalize_pages
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
        _compare_field(
            "pages",
            input_reference.pages,
            found_record.pages,
            lambda value: normalize_pages(str(value)),
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
        _compare_field("url", input_reference.url, found_record.url, _clean),
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
    if input_reference.issn and found_record.issn:
        input_issn = {normalize_issn(value) for value in input_reference.issn}
        found_issn = {normalize_issn(value) for value in found_record.issn}
        return FieldComparison(
            field="venue",
            input_value=input_reference.issn,
            found_value=found_record.issn,
            result=ComparisonResult.MATCH
            if input_issn & found_issn
            else ComparisonResult.MISMATCH,
            note="compared by ISSN",
        )
    return _compare_field(
        "venue",
        input_reference.venue,
        found_record.venue,
        lambda value: normalize_journal(str(value)),
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
