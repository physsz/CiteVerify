from citeverify.models import (
    IdentifierCandidate,
    IdentifierKind,
    ParsedReference,
    RegistryRecord,
    VerificationResult,
    VerificationStatus,
)
from citeverify.reports.markdown import render_short_report


def test_short_report_renders_exception_table_and_omits_clean_references() -> None:
    clean = VerificationResult(
        reference_id="ref-1",
        raw_reference="raw clean",
        parsed_reference=ParsedReference(reference_id="ref-1", raw_text="raw clean"),
        status=VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH,
    )
    exception = VerificationResult(
        reference_id="ref-2",
        raw_reference="raw bad",
        parsed_reference=ParsedReference(reference_id="ref-2", raw_text="raw bad"),
        status=VerificationStatus.TITLE_NOT_FOUND,
    )
    report = render_short_report([clean, exception])
    assert (
        "| Reference | Status | Identifier Used | Article Link | Mismatch Details |"
        in report
    )
    assert "`ref-2`" in report
    assert "TITLE_NOT_FOUND" in report
    assert "identifier not found or insufficient metadata" in report
    assert "raw clean" not in report


def test_short_report_does_not_link_unselected_candidate_records() -> None:
    exception = VerificationResult(
        reference_id="ref-1",
        raw_reference="raw bad",
        parsed_reference=ParsedReference(reference_id="ref-1", raw_text="raw bad"),
        identifier_used=IdentifierCandidate(
            kind=IdentifierKind.JOURNAL_LOCATOR,
            value="journal locator",
            normalized_value="journal locator",
        ),
        lookup_records=[
            RegistryRecord(
                source="Fixture",
                doi="10.1000/unselected",
                title="Unselected Candidate",
            )
        ],
        selected_record=None,
        status=VerificationStatus.JOURNAL_LOCATOR_NOT_FOUND,
    )
    report = render_short_report([exception])
    assert "| `ref-1` |" in report
    assert "10.1000/unselected" not in report
    assert "ambiguous or unselected lookup records" in report
