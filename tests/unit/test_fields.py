from citeverify.compare.fields import compare_references
from citeverify.models import ComparisonResult, ParsedReference, RegistryRecord
from citeverify.normalize.author import parse_author_list


def test_compare_only_supplied_fields_and_additional_metadata() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            title="A Real Paper",
            authors=parse_author_list("Smith, J."),
        ),
        RegistryRecord(
            source="fixture",
            title="A Real Paper",
            authors=parse_author_list("Smith, John"),
            year=2020,
            doi="10.1000/example",
        ),
    )
    by_field = {comparison.field: comparison for comparison in comparisons}
    assert by_field["title"].result == ComparisonResult.MATCH
    assert by_field["authors"].result == ComparisonResult.MATCH
    assert by_field["year"].result == ComparisonResult.ADDITIONAL_METADATA
    assert by_field["doi"].result == ComparisonResult.ADDITIONAL_METADATA


def test_title_mismatch() -> None:
    comparisons = compare_references(
        ParsedReference(reference_id="ref-1", raw_text="raw", title="Input Title"),
        RegistryRecord(source="fixture", title="Different Title"),
    )
    title = next(
        comparison for comparison in comparisons if comparison.field == "title"
    )
    assert title.result == ComparisonResult.MISMATCH
