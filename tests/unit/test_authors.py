from citeverify.compare.authors import compare_authors
from citeverify.models import ComparisonResult
from citeverify.normalize.author import parse_author_list


def test_initials_match_full_names() -> None:
    comparison = compare_authors(
        parse_author_list("Smith, J.; Wang, L.; et al."),
        parse_author_list("Smith, John; Wang, Li; Brown, Amy"),
    )
    assert comparison.result == ComparisonResult.MATCH


def test_supplied_author_mismatch_is_reported() -> None:
    comparison = compare_authors(
        parse_author_list("Smith, J.; Wang, L."),
        parse_author_list("Smith, John; Brown, Amy"),
    )
    assert comparison.result == ComparisonResult.MISMATCH
    assert "Wang" in (comparison.note or "")
