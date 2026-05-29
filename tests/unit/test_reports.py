from citeverify.models import ParsedReference, VerificationResult, VerificationStatus
from citeverify.reports.markdown import render_short_report


def test_short_report_omits_clean_references() -> None:
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
    assert "raw bad" in report
    assert "raw clean" not in report
