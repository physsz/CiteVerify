from __future__ import annotations

import pytest

from citeverify.compare.references import Verifier
from citeverify.lookup.base import LookupResponse
from citeverify.models import (
    JournalLocator,
    ParsedReference,
    RegistryRecord,
    VerificationStatus,
)
from citeverify.normalize.author import parse_author_list


class FakeProvider:
    name = "Fixture"

    def __init__(self, records: list[RegistryRecord]) -> None:
        self.records = records

    async def get_by_doi(self, doi: str) -> LookupResponse:
        matches = [record for record in self.records if record.doi == doi]
        return LookupResponse(
            source=self.name,
            query_kind="doi",
            query_value=doi,
            records=matches,
            raw_status_code=200 if matches else 404,
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
async def test_doi_found_clean() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Fixture",
                        doi="10.1000/example",
                        title="A Real Paper",
                        authors=parse_author_list("Smith, John"),
                        year=2020,
                    )
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            doi="10.1000/example",
            title="A Real Paper",
            authors=parse_author_list("Smith, J."),
            year=2020,
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH


@pytest.mark.asyncio
async def test_doi_title_mismatch() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Fixture",
                        doi="10.1000/example",
                        title="Different Paper",
                    )
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            doi="10.1000/example",
            title="Input Paper",
        )
    )
    assert result.status == VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK


@pytest.mark.asyncio
async def test_title_found_with_year_mismatch() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Fixture",
                        title="A Real Paper",
                        year=2020,
                    )
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            title="A Real Paper",
            year=2021,
        )
    )
    assert result.status == VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES


@pytest.mark.asyncio
async def test_title_ambiguous_match() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(source="Fixture", title="A Real Paper", year=2020),
                    RegistryRecord(source="Fixture", title="A Real Paper", year=2021),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(reference_id="ref-1", raw_text="raw", title="A Real Paper")
    )
    assert result.status == VerificationStatus.AMBIGUOUS_MATCH


@pytest.mark.asyncio
async def test_title_duplicate_records_are_not_ambiguous() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Crossref",
                        doi="10.1000/example",
                        title="A Real Paper",
                        year=2020,
                    ),
                    RegistryRecord(
                        source="OpenAlex",
                        doi="10.1000/example",
                        title="A Real Paper",
                        year=2020,
                    ),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            title="A Real Paper",
            year=2020,
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH


@pytest.mark.asyncio
async def test_journal_locator_found() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Fixture",
                        venue="Physical Review Letters",
                        year=2018,
                        volume="121",
                        article_number="090502",
                    )
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="ref-1",
            raw_text="raw",
            venue="Phys. Rev. Lett.",
            year=2018,
            volume="121",
            article_number="090502",
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
