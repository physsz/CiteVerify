from __future__ import annotations

from pathlib import Path

import pytest

from citeverify.compare.fields import mismatches
from citeverify.compare.references import Verifier
from citeverify.lookup.base import LookupResponse
from citeverify.models import JournalLocator, RegistryRecord, VerificationStatus
from citeverify.normalize.author import parse_author_list
from citeverify.parsers.bibtex import parse_bibtex

FIXTURE_PATH = (
    Path(__file__).parents[1] / "fixtures" / "partially_fake_references.bib"
)
REAL_DOI = "10.1088/2058-9565/ab4eb5"
FAKE_DOI = "10.9999/fake-parameterized-qc"


class FakeProvider:
    name = "Fixture"

    def __init__(self) -> None:
        self.records = [
            RegistryRecord(
                source=self.name,
                doi=REAL_DOI,
                title="Parameterized quantum circuits as machine learning models",
                authors=parse_author_list(
                    "Marcello Benedetti; Erika Lloyd; "
                    "Stefan H. Sack; Mattia Fiorentini"
                ),
                year=2019,
                venue="Quantum Science and Technology",
                volume="4",
                issue="4",
                pages="043001",
            ),
        ]
        self.doi_aliases = {REAL_DOI: REAL_DOI, FAKE_DOI: REAL_DOI}

    async def get_by_doi(self, doi: str) -> LookupResponse:
        canonical_doi = self.doi_aliases.get(doi)
        matches = [
            record for record in self.records if record.doi == canonical_doi
        ]
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


@pytest.mark.asyncio
async def test_partially_fake_bib_fixture_has_expected_outcomes() -> None:
    references = parse_bibtex(FIXTURE_PATH.read_text(encoding="utf-8"))
    verifier = Verifier([FakeProvider()])
    results = await verifier.verify_many(references)

    expected = {
        "correctBenedetti2019ParameterizedQC": (
            VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH,
            set(),
        ),
        "fakeWrongDoi": (
            VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES,
            {"doi"},
        ),
        "fakeWrongTitle": (
            VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK,
            {"title"},
        ),
        "fakeWrongJournalInfo": (
            VerificationStatus.IDENTIFIER_CONFLICT,
            {"venue", "volume", "issue", "pages"},
        ),
        "fakeWrongDoiWrongTitle": (
            VerificationStatus.JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES,
            {"doi", "title"},
        ),
        "fakeWrongDoiWrongJournal": (
            VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES,
            {"doi", "venue", "volume", "issue", "pages"},
        ),
        "fakeWrongTitleWrongJournal": (
            VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK,
            {"title", "venue", "volume", "issue", "pages"},
        ),
        "fakeAllWrongDoiTitleJournal": (
            VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK,
            {"doi", "title", "venue", "volume", "issue", "pages"},
        ),
        "fakePartiallyWrongAuthors": (
            VerificationStatus.IDENTIFIER_CONFLICT,
            {"authors"},
        ),
    }

    assert {result.reference_id for result in results} == set(expected)
    for result in results:
        expected_status, expected_mismatch_fields = expected[result.reference_id]
        assert result.status == expected_status
        assert {comparison.field for comparison in mismatches(result.comparisons)} == (
            expected_mismatch_fields
        )

    author_result = next(
        result
        for result in results
        if result.reference_id == "fakePartiallyWrongAuthors"
    )
    author_mismatch = mismatches(author_result.comparisons)[0]
    assert author_mismatch.note is not None
    assert "Mallory Fake" in author_mismatch.note
