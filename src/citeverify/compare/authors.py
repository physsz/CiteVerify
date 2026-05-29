from __future__ import annotations

from citeverify.models import ComparisonResult, FieldComparison, ParsedAuthor
from citeverify.normalize.author import author_names_compatible


def compare_authors(
    input_authors: list[ParsedAuthor],
    found_authors: list[ParsedAuthor],
) -> FieldComparison:
    supplied = [author for author in input_authors if not author.is_et_al_marker]
    if not supplied:
        return FieldComparison(
            field="authors",
            input_value=[author.raw_name for author in input_authors],
            found_value=[author.raw_name for author in found_authors],
            result=ComparisonResult.NOT_CHECKED,
            note="no concrete supplied author names to check",
        )
    if not found_authors:
        return FieldComparison(
            field="authors",
            input_value=[author.raw_name for author in supplied],
            found_value=[],
            result=ComparisonResult.NOT_CHECKED,
            note="lookup source did not return authors",
        )

    mismatches: list[str] = []
    matched_found_indexes: set[int] = set()
    for supplied_author in supplied:
        found_index = _find_compatible_author(
            supplied_author, found_authors, matched_found_indexes
        )
        if found_index is None:
            mismatches.append(f"{supplied_author.raw_name}: no compatible author found")
            continue
        matched_found_indexes.add(found_index)

    return FieldComparison(
        field="authors",
        input_value=[author.raw_name for author in input_authors],
        found_value=[author.raw_name for author in found_authors],
        result=ComparisonResult.MISMATCH if mismatches else ComparisonResult.MATCH,
        note="; ".join(mismatches) if mismatches else None,
    )


def _find_compatible_author(
    supplied_author: ParsedAuthor,
    found_authors: list[ParsedAuthor],
    matched_found_indexes: set[int],
) -> int | None:
    position = supplied_author.position_in_list
    if (
        position is not None
        and position < len(found_authors)
        and position not in matched_found_indexes
        and author_names_compatible(supplied_author, found_authors[position])
    ):
        return position

    for index, found_author in enumerate(found_authors):
        if index in matched_found_indexes:
            continue
        if author_names_compatible(supplied_author, found_author):
            return index
    return None
