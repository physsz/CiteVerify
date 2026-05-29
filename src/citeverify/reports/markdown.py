from __future__ import annotations

from citeverify.models import (
    ComparisonResult,
    FieldComparison,
    RegistryRecord,
    VerificationResult,
)


def render_full_report(results: list[VerificationResult]) -> str:
    lines = ["# CiteVerify Full Evidence Report", ""]
    lines.extend(_summary_lines(results))
    for result in results:
        lines.extend(_render_result(result, include_clean=True))
    return "\n".join(lines).rstrip() + "\n"


def render_short_report(results: list[VerificationResult]) -> str:
    exceptions = [result for result in results if result.has_exception]
    lines = ["# CiteVerify Short Exception Report", ""]
    lines.extend(_summary_lines(results))
    if not exceptions:
        lines.append(
            "No references with lookup failures or supplied-field mismatches "
            "were found."
        )
        return "\n".join(lines).rstrip() + "\n"
    lines.extend(_render_short_exception_table(exceptions))
    return "\n".join(lines).rstrip() + "\n"


def _summary_lines(results: list[VerificationResult]) -> list[str]:
    exception_count = sum(1 for result in results if result.has_exception)
    return [
        "## Summary",
        "",
        f"- Total references: `{len(results)}`",
        f"- Clean references: `{len(results) - exception_count}`",
        f"- Exception references: `{exception_count}`",
        "",
    ]


def _render_result(result: VerificationResult, include_clean: bool) -> list[str]:
    lines = [
        f"## Reference {result.reference_id}",
        "",
        f"Status: `{result.status.value}`",
        "",
        "### Raw Input",
        "",
        "```text",
        result.raw_reference,
        "```",
        "",
    ]
    if result.identifier_used:
        lines.extend(
            [
                "### Identifier Used",
                "",
                f"- Kind: `{result.identifier_used.kind.value}`",
                f"- Value: `{result.identifier_used.value}`",
                f"- Normalized: `{result.identifier_used.normalized_value}`",
                "",
            ]
        )
    else:
        lines.extend(["### Identifier Used", "", "None.", ""])

    lines.extend(_render_lookup_section(result))
    if result.selected_record:
        lines.extend(_render_record(result.selected_record))

    mismatch_lines = _render_mismatches(result.comparisons)
    if mismatch_lines:
        lines.extend(mismatch_lines)
    elif include_clean:
        lines.extend(["### Mismatches", "", "None.", ""])

    if include_clean:
        lines.extend(_render_all_comparisons(result.comparisons))
    if result.lookup_errors:
        lines.extend(["### Lookup Errors", ""])
        lines.extend(f"- {error}" for error in result.lookup_errors)
        lines.append("")
    return lines


def _render_lookup_section(result: VerificationResult) -> list[str]:
    lines = ["### Lookup", ""]
    if result.lookup_sources:
        lines.append(
            "- Sources queried: "
            + ", ".join(f"`{source}`" for source in result.lookup_sources)
        )
    else:
        lines.append("- Sources queried: none")
    lines.append(f"- Records returned: `{len(result.lookup_records)}`")
    lines.append("")
    if result.lookup_records and result.selected_record is None:
        lines.extend(["### Candidate Records", ""])
        for index, record in enumerate(result.lookup_records, start=1):
            label = record.title or record.doi or record.source_record_url or "untitled"
            lines.append(f"{index}. `{record.source}`: {label}")
        lines.append("")
    return lines


def _render_short_exception_table(results: list[VerificationResult]) -> list[str]:
    lines = [
        "## Exception References",
        "",
        "| Reference | Status | Identifier Used | Article Link | Mismatch Details |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(f"`{result.reference_id}`"),
                    _table_cell(f"`{result.status.value}`"),
                    _table_cell(_short_identifier(result)),
                    _table_cell(_article_link(result)),
                    _table_cell(_short_mismatch_details(result)),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _short_identifier(result: VerificationResult) -> str:
    identifier = result.identifier_used
    if identifier is None:
        return "None"
    return f"`{identifier.kind.value}`: {_inline_code(identifier.value)}"


def _article_link(result: VerificationResult) -> str:
    url = _best_article_url(result)
    if not url:
        return "None"
    label = _best_article_label(result)
    return f"[{_link_label(label)}]({url})"


def _best_article_url(result: VerificationResult) -> str | None:
    record = result.selected_record
    if record:
        if record.doi:
            return f"https://doi.org/{record.doi}"
        if record.url:
            return record.url
        if record.source_record_url:
            return record.source_record_url
    if result.identifier_used and result.identifier_used.kind.value == "url":
        return result.identifier_used.value
    return None


def _best_article_label(result: VerificationResult) -> str:
    record = result.selected_record
    if record:
        return record.doi or record.source or record.title or "article"
    return "article"


def _short_mismatch_details(result: VerificationResult) -> str:
    mismatches = [
        comparison
        for comparison in result.comparisons
        if comparison.result == ComparisonResult.MISMATCH
    ]
    if not mismatches:
        if result.selected_record is None:
            if result.lookup_errors:
                return "; ".join(
                    f"lookup error: {error}" for error in result.lookup_errors
                )
            if result.lookup_records:
                return "ambiguous or unselected lookup records"
            return "identifier not found or insufficient metadata"
        return "exception status without supplied-field mismatch"
    details = []
    for comparison in mismatches:
        item = (
            f"`{comparison.field}`: input {_inline_code(comparison.input_value)}; "
            f"found {_inline_code(comparison.found_value)}"
        )
        if comparison.note:
            item += f"; note: {comparison.note}"
        details.append(item)
    return "<br>".join(details)


def _table_cell(value: str) -> str:
    return value.replace("\n", " ").replace("|", r"\|")


def _inline_code(value: object) -> str:
    text = str(value).replace("`", "'").replace("\n", " ")
    return f"`{text}`"


def _link_label(value: str) -> str:
    return value.replace("[", "(").replace("]", ")")


def _render_record(record: RegistryRecord) -> list[str]:
    author_names = "; ".join(author.raw_name for author in record.authors) or None
    fields = [
        ("Source", record.source),
        ("Source URL", record.source_record_url),
        ("Title", record.title),
        ("Authors", author_names),
        ("Venue", record.venue),
        ("Year", record.year),
        ("Volume", record.volume),
        ("Issue", record.issue),
        ("Pages", record.pages),
        ("Article number", record.article_number),
        ("DOI", record.doi),
        ("URL", record.url),
        ("Type", record.record_type),
    ]
    lines = ["### Selected Record", ""]
    for label, value in fields:
        if value not in (None, "", [], {}):
            lines.append(f"- {label}: `{value}`")
    lines.append("")
    return lines


def _render_mismatches(comparisons: list[FieldComparison]) -> list[str]:
    mismatches = [
        comparison
        for comparison in comparisons
        if comparison.result == ComparisonResult.MISMATCH
    ]
    if not mismatches:
        return []
    lines = ["### Mismatches", ""]
    for comparison in mismatches:
        lines.extend(
            [
                f"- {comparison.field}:",
                f"  - Input: `{comparison.input_value}`",
                f"  - Found: `{comparison.found_value}`",
            ]
        )
        if comparison.note:
            lines.append(f"  - Note: {comparison.note}")
    lines.append("")
    return lines


def _render_all_comparisons(comparisons: list[FieldComparison]) -> list[str]:
    if not comparisons:
        return []
    lines = ["### Field Comparisons", ""]
    for comparison in comparisons:
        lines.append(
            f"- `{comparison.field}`: `{comparison.result.value}` "
            f"(input: `{comparison.input_value}`, found: `{comparison.found_value}`)"
        )
        if comparison.note:
            lines.append(f"  - Note: {comparison.note}")
    lines.append("")
    return lines
