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
    for supplied_author in supplied:
        position = supplied_author.position_in_list
        found_author = (
            found_authors[position]
            if position is not None and position < len(found_authors)
            else None
        )
        if found_author is None:
            mismatches.append(
                f"{supplied_author.raw_name}: no corresponding author found"
            )
            continue
        if not author_names_compatible(supplied_author, found_author):
            mismatches.append(
                f"{supplied_author.raw_name} != {found_author.raw_name}"
            )

    return FieldComparison(
        field="authors",
        input_value=[author.raw_name for author in input_authors],
        found_value=[author.raw_name for author in found_authors],
        result=ComparisonResult.MISMATCH if mismatches else ComparisonResult.MATCH,
        note="; ".join(mismatches) if mismatches else None,
    )
