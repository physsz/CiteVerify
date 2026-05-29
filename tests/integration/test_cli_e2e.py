from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from typer.testing import CliRunner

import citeverify.cli as cli_module
from citeverify.cli import app
from citeverify.lookup.base import LookupResponse
from citeverify.models import JournalLocator, RegistryRecord
from citeverify.normalize.author import parse_author_list


class FakeProvider:
    name = "Fixture"

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        self.records = [
            RegistryRecord(
                source=self.name,
                doi="10.1000/clean",
                title="A Real Paper",
                authors=parse_author_list("Smith, John"),
                year=2020,
                venue="Journal of Test Cases",
                volume="1",
                pages="1-10",
            ),
            RegistryRecord(
                source=self.name,
                doi="10.1000/mismatch",
                title="A Different Paper",
                authors=parse_author_list("Doe, Jane"),
                year=2021,
                venue="Journal of Test Cases",
                volume="2",
                pages="11-20",
            ),
        ]

    async def get_by_doi(self, doi: str) -> LookupResponse:
        matches = [record for record in self.records if record.doi == doi]
        return LookupResponse(
            source=self.name,
            query_kind="doi",
            query_value=doi,
            records=matches,
            raw_status_code=200 if matches else 404,
        )

    async def get_by_arxiv_id(self, arxiv_id: str) -> LookupResponse:
        return LookupResponse(
            source=self.name,
            query_kind="arxiv_id",
            query_value=arxiv_id,
            records=[],
            raw_status_code=404,
        )

    async def search_by_title(self, title: str) -> LookupResponse:
        return LookupResponse(
            source=self.name,
            query_kind="title",
            query_value=title,
            records=self.records,
            raw_status_code=200,
        )

    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse:
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=locator.model_dump_json(),
            records=self.records,
            raw_status_code=200,
        )


def _patch_lookup_providers(monkeypatch: Any) -> None:
    monkeypatch.setattr(cli_module, "CrossrefProvider", FakeProvider)
    monkeypatch.setattr(cli_module, "DataCiteProvider", FakeProvider)
    monkeypatch.setattr(cli_module, "ArxivProvider", FakeProvider)
    monkeypatch.setattr(cli_module, "OpenAlexProvider", FakeProvider)


def _write_example_bib(path: Path) -> None:
    path.write_text(
        """
@article{clean,
  author = {Smith, J.},
  title = {A Real Paper},
  journal = {Journal of Test Cases},
  year = {2020},
  volume = {1},
  pages = {1--10},
  doi = {10.1000/clean}
}

@article{mismatch,
  author = {Doe, J.},
  title = {Input Paper},
  journal = {Journal of Test Cases},
  year = {2021},
  volume = {2},
  pages = {11--20},
  doi = {10.1000/mismatch}
}
""".strip(),
        encoding="utf-8",
    )


def test_cli_verifies_bibtex_and_writes_reports(
    tmp_path: Path, monkeypatch: Any
) -> None:
    _patch_lookup_providers(monkeypatch)
    bib_path = tmp_path / "refs.bib"
    full_report = tmp_path / "missing" / "reports" / "full.md"
    short_report = tmp_path / "missing" / "reports" / "short.md"
    json_report = tmp_path / "missing" / "json" / "report.json"
    _write_example_bib(bib_path)

    result = CliRunner().invoke(
        app,
        [
            "verify",
            str(bib_path),
            "--no-cache",
            "--full-report",
            str(full_report),
            "--short-report",
            str(short_report),
            "--json-report",
            str(json_report),
        ],
    )

    assert result.exit_code == 0, result.output
    assert full_report.exists()
    assert short_report.exists()
    assert json_report.exists()
    assert "Verified 2 reference(s)." in result.output
    assert "Exception references: 1." in result.output

    full_text = full_report.read_text(encoding="utf-8")
    short_text = short_report.read_text(encoding="utf-8")
    report_data = json.loads(json_report.read_text(encoding="utf-8"))

    assert "FOUND_NO_SUPPLIED_FIELD_MISMATCH" in full_text
    assert "DOI_RESOLVES_TO_DIFFERENT_WORK" in full_text
    assert "DOI_RESOLVES_TO_DIFFERENT_WORK" in short_text
    assert "A Real Paper" not in short_text
    assert report_data["summary"] == {
        "total_references": 2,
        "clean_references": 1,
        "exception_references": 1,
    }


def test_cli_default_reports_go_to_reports_directory(
    tmp_path: Path, monkeypatch: Any
) -> None:
    _patch_lookup_providers(monkeypatch)
    monkeypatch.chdir(tmp_path)
    bib_path = tmp_path / "refs.bib"
    _write_example_bib(bib_path)

    result = CliRunner().invoke(
        app,
        [
            "verify",
            str(bib_path),
            "--no-cache",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "reports" / "full_report.md").exists()
    assert (tmp_path / "reports" / "short_report.md").exists()
    assert (tmp_path / "reports" / "report.json").exists()
    assert "Full report: reports/full_report.md" in result.output
    assert "Short report: reports/short_report.md" in result.output
    assert "JSON report: reports/report.json" in result.output
