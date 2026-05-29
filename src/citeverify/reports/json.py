from __future__ import annotations

from pathlib import Path

from citeverify import __version__
from citeverify.models import RunSummary, VerificationReport, VerificationResult


def build_json_report(
    results: list[VerificationResult], input_path: Path | str
) -> VerificationReport:
    exception_count = sum(1 for result in results if result.has_exception)
    return VerificationReport(
        version=__version__,
        input=str(input_path),
        summary=RunSummary(
            total_references=len(results),
            clean_references=len(results) - exception_count,
            exception_references=exception_count,
        ),
        results=results,
    )


def render_json_report(
    results: list[VerificationResult], input_path: Path | str
) -> str:
    report = build_json_report(results, input_path)
    return report.model_dump_json(indent=2)
