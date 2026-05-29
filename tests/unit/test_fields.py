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


def test_arxiv_preprint_venue_is_not_literal_mismatch() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            venue="arXiv preprint arXiv:2603.05475",
        ),
        RegistryRecord(source="fixture", venue="arXiv.org"),
    )
    venue = next(
        comparison for comparison in comparisons if comparison.field == "venue"
    )
    assert venue.result == ComparisonResult.MATCH


def test_arxiv_preprint_venue_mismatches_published_venue() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            venue="ArXiv",
        ),
        RegistryRecord(source="fixture", venue="Quantum Science and Technology"),
    )
    venue = next(
        comparison for comparison in comparisons if comparison.field == "venue"
    )
    assert venue.result == ComparisonResult.MISMATCH


def test_page_range_matches_first_page_only() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            pages="1870-1879",
        ),
        RegistryRecord(source="fixture", pages="1870"),
    )
    pages = next(
        comparison for comparison in comparisons if comparison.field == "pages"
    )
    assert pages.result == ComparisonResult.MATCH


def test_venue_matches_when_volume_is_embedded_in_found_venue() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            venue="Advances in Neural Information Processing Systems",
            volume="35",
        ),
        RegistryRecord(
            source="fixture",
            venue="Advances in Neural Information Processing Systems 35",
        ),
    )
    venue = next(
        comparison for comparison in comparisons if comparison.field == "venue"
    )
    assert venue.result == ComparisonResult.MATCH


def test_url_is_not_checked_by_default() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            url="https://link.springer.com/article/10.1007/s11128-014-0809-8",
        ),
        RegistryRecord(
            source="fixture",
            url="https://doi.org/10.1007/s11128-014-0809-8",
        ),
    )
    assert "url" not in {comparison.field for comparison in comparisons}


def test_issn_is_not_used_for_venue_comparison_by_default() -> None:
    comparisons = compare_references(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            venue="Physical Review A",
            issn=["1050294710941622"],
        ),
        RegistryRecord(
            source="fixture",
            venue="Physical Review A",
            issn=["1050-2947", "1094-1622"],
        ),
    )
    venue = next(
        comparison for comparison in comparisons if comparison.field == "venue"
    )
    assert venue.result == ComparisonResult.MATCH
    assert venue.input_value == "Physical Review A"
