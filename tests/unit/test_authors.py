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


def test_inserted_registry_author_does_not_shift_later_matches() -> None:
    comparison = compare_authors(
        parse_author_list(
            r'H{\"a}ffner, Hartmut; H{\"a}nsel, Wolfgang; Roos, CF; '
            r"Benhelm, Jan; Chwalla, Michael; K{\"o}rber, Timo; et al."
        ),
        parse_author_list(
            "Häffner, H.; Hänsel, W.; Roos, C. F.; Benhelm, J.; "
            "Chek-al-kar, D.; Chwalla, M.; Körber, T."
        ),
    )
    assert comparison.result == ComparisonResult.MATCH


def test_extra_middle_initial_does_not_force_mismatch() -> None:
    comparison = compare_authors(
        parse_author_list("John M. Jumper"),
        parse_author_list("Jumper, John"),
    )
    assert comparison.result == ComparisonResult.MATCH


def test_family_particles_attach_to_uncomma_author_family_name() -> None:
    supplied = parse_author_list("Diego de Las Casas")
    found = parse_author_list("de las Casas, Diego")

    assert supplied[0].family_name == "de Las Casas"
    assert supplied[0].given_names == ["Diego"]

    comparison = compare_authors(supplied, found)
    assert comparison.result == ComparisonResult.MATCH
