from __future__ import annotations

import asyncio
from enum import StrEnum
from pathlib import Path

import typer
from rich.console import Console

from citeverify.cache import ResponseCache
from citeverify.compare import verify_references
from citeverify.config import CiteVerifyConfig
from citeverify.errors import UnsupportedInputError
from citeverify.lookup import (
    ArxivProvider,
    CrossrefProvider,
    DataCiteProvider,
    OpenAlexProvider,
)
from citeverify.lookup.base import HttpLookupProvider, LookupProvider
from citeverify.models import ParsedReference, VerificationResult
from citeverify.parsers import parse_bibtex, parse_raw_text
from citeverify.reports import (
    render_full_report,
    render_json_report,
    render_short_report,
)

app = typer.Typer(help="Verify scholarly references against metadata sources.")
console = Console()


@app.callback()
def main() -> None:
    """Evidence-based scholarly reference verification."""


class InputFormat(StrEnum):
    AUTO = "auto"
    BIBTEX = "bibtex"
    RAW_TEXT = "raw-text"
    LATEX = "latex"
    PDF = "pdf"


@app.command()
def verify(
    input_path: Path = typer.Argument(..., exists=True, readable=True),
    full_report: Path = typer.Option(
        Path("citeverify_full_report.md"),
        "--full-report",
        help="Path for the full Markdown evidence report.",
    ),
    short_report: Path = typer.Option(
        Path("citeverify_short_report.md"),
        "--short-report",
        help="Path for the short Markdown exception report.",
    ),
    json_report: Path = typer.Option(
        Path("citeverify_report.json"),
        "--json-report",
        help="Path for the JSON report.",
    ),
    input_format: InputFormat = typer.Option(
        InputFormat.AUTO,
        "--format",
        help="Input format. Use auto for extension-based detection.",
    ),
    cache_path: Path = typer.Option(
        Path(".citeverify-cache.sqlite"),
        "--cache",
        help="SQLite cache path.",
    ),
    no_cache: bool = typer.Option(False, "--no-cache", help="Disable HTTP cache."),
    offline: bool = typer.Option(False, "--offline", help="Use cache only."),
    fail_on_exceptions: bool = typer.Option(
        False,
        "--fail-on-exceptions",
        help="Exit with code 1 when exception references are found.",
    ),
    timeout: float = typer.Option(20.0, "--timeout", help="HTTP timeout in seconds."),
    max_concurrency: int = typer.Option(
        5, "--max-concurrency", help="Lookup concurrency."
    ),
) -> None:
    """Verify references and write full, short, and JSON reports."""
    try:
        references = _parse_input(input_path, input_format)
    except UnsupportedInputError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(2) from exc

    config = CiteVerifyConfig.from_env()
    config = CiteVerifyConfig(
        cache_path=cache_path,
        use_cache=not no_cache,
        offline=offline,
        timeout=timeout,
        max_concurrency=max_concurrency,
        contact_email=config.contact_email,
        crossref_mailto=config.crossref_mailto,
        semantic_scholar_api_key=config.semantic_scholar_api_key,
        ncbi_api_key=config.ncbi_api_key,
    )
    cache = (
        ResponseCache(cache_path)
        if config.use_cache and config.cache_path
        else None
    )
    providers: list[LookupProvider] = [
        CrossrefProvider(config, cache=cache),
        DataCiteProvider(config, cache=cache),
        ArxivProvider(config, cache=cache),
        OpenAlexProvider(config, cache=cache),
    ]

    results = asyncio.run(
        _run_verification(
            references=references,
            providers=providers,
            max_concurrency=max_concurrency,
        )
    )

    full_report.write_text(render_full_report(results), encoding="utf-8")
    short_report.write_text(render_short_report(results), encoding="utf-8")
    json_report.write_text(render_json_report(results, input_path), encoding="utf-8")

    exception_count = sum(1 for result in results if result.has_exception)
    console.print(f"Verified {len(results)} reference(s).")
    console.print(f"Exception references: {exception_count}.")
    console.print(f"Full report: {full_report}")
    console.print(f"Short report: {short_report}")
    console.print(f"JSON report: {json_report}")
    if exception_count and fail_on_exceptions:
        raise typer.Exit(1)


def _parse_input(
    input_path: Path, input_format: InputFormat
) -> list[ParsedReference]:
    detected = _detect_format(input_path, input_format)
    if detected == InputFormat.BIBTEX:
        return parse_bibtex(input_path.read_text(encoding="utf-8"))
    if detected == InputFormat.RAW_TEXT:
        return parse_raw_text(input_path.read_text(encoding="utf-8"))
    if detected == InputFormat.LATEX:
        raise UnsupportedInputError("LaTeX input is planned but not implemented yet.")
    if detected == InputFormat.PDF:
        raise UnsupportedInputError("PDF input is planned but not implemented yet.")
    raise UnsupportedInputError(f"Unsupported input format: {detected}")


def _detect_format(input_path: Path, input_format: InputFormat) -> InputFormat:
    if input_format != InputFormat.AUTO:
        return input_format
    suffix = input_path.suffix.lower()
    if suffix == ".bib":
        return InputFormat.BIBTEX
    if suffix in {".txt", ".refs"}:
        return InputFormat.RAW_TEXT
    if suffix in {".tex", ".bbl"}:
        return InputFormat.LATEX
    if suffix == ".pdf":
        return InputFormat.PDF
    return InputFormat.RAW_TEXT


async def _close_providers(providers: list[LookupProvider]) -> None:
    for provider in providers:
        if isinstance(provider, HttpLookupProvider):
            await provider.aclose()


async def _run_verification(
    *,
    references: list[ParsedReference],
    providers: list[LookupProvider],
    max_concurrency: int,
) -> list[VerificationResult]:
    try:
        return await verify_references(
            references,
            providers,
            max_concurrency=max_concurrency,
        )
    finally:
        await _close_providers(providers)


if __name__ == "__main__":
    app()
