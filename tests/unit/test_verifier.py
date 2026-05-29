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

LOW_DEPTH_TITLE = "Low-depth amplitude estimation via statistical eigengap estimation"


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

    async def get_by_arxiv_id(self, arxiv_id: str) -> LookupResponse:
        matches = [record for record in self.records if record.arxiv_id == arxiv_id]
        return LookupResponse(
            source=self.name,
            query_kind="arxiv_id",
            query_value=arxiv_id,
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


@pytest.mark.asyncio
async def test_arxiv_id_collapses_duplicate_records() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="DataCite",
                        doi="10.48550/arxiv.2603.05475",
                        arxiv_id="2603.05475",
                        title=LOW_DEPTH_TITLE,
                        authors=parse_author_list("Huang, Po-Wei; Koczor, Bálint"),
                        year=2026,
                        venue="arXiv",
                    ),
                    RegistryRecord(
                        source="OpenAlex",
                        arxiv_id="2603.05475",
                        title=LOW_DEPTH_TITLE,
                        authors=parse_author_list("Po-Wei Huang; Bálint Koczor"),
                        year=2026,
                        venue="ArXiv.org",
                    ),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="huang2026low",
            raw_text="raw",
            title=LOW_DEPTH_TITLE,
            authors=parse_author_list("Huang, Po-Wei; Koczor, B{\\'a}lint"),
            year=2026,
            venue="arXiv preprint arXiv:2603.05475",
            arxiv_id="2603.05475",
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH


@pytest.mark.asyncio
async def test_title_prefers_exact_title_over_near_title() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Crossref",
                        doi="10.1145/3406325.3465355",
                        title=(
                            "Neural tangent kernel: convergence and "
                            "generalization in neural networks (invited paper)"
                        ),
                        year=2021,
                    ),
                    RegistryRecord(
                        source="OpenAlex",
                        doi="10.48550/arxiv.1806.07572",
                        arxiv_id="1806.07572",
                        title=(
                            "Neural Tangent Kernel: Convergence and "
                            "Generalization in Neural Networks"
                        ),
                        year=2018,
                    ),
                    RegistryRecord(
                        source="OpenAlex",
                        title=(
                            "Neural Tangent Kernel: Convergence and "
                            "Generalization in Neural Networks"
                        ),
                        year=2018,
                    ),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="jacot2018neural",
            raw_text="raw",
            title=(
                "Neural tangent kernel: Convergence and generalization "
                "in neural networks"
            ),
            year=2018,
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
    assert result.selected_record is not None
    assert result.selected_record.doi == "10.48550/arxiv.1806.07572"


@pytest.mark.asyncio
async def test_title_uses_doi_embedded_in_url_to_disambiguate() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="Crossref",
                        doi="10.1007/s11128-014-0809-8",
                        title="The quest for a Quantum Neural Network",
                        year=2014,
                        venue="Quantum Information Processing",
                        volume="13",
                        issue="11",
                        pages="2567-2586",
                        url="https://doi.org/10.1007/s11128-014-0809-8",
                    ),
                    RegistryRecord(
                        source="OpenAlex",
                        doi="10.5555/2684509.2684546",
                        title="The quest for a Quantum Neural Network",
                        year=2014,
                        venue="Quantum Information Processing",
                    ),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="schuld2014quest",
            raw_text="raw",
            title="The quest for a quantum neural network",
            year=2014,
            venue="Quantum Information Processing",
            url="https://link.springer.com/article/10.1007/s11128-014-0809-8",
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
    assert result.selected_record is not None
    assert result.selected_record.doi == "10.1007/s11128-014-0809-8"


@pytest.mark.asyncio
async def test_title_uses_venue_with_embedded_volume_to_disambiguate() -> None:
    verifier = Verifier(
        [
            FakeProvider(
                [
                    RegistryRecord(
                        source="OpenAlex",
                        doi="10.48550/arxiv.2210.15812",
                        arxiv_id="2210.15812",
                        title=(
                            "Differentiable Analog Quantum Computing for "
                            "Optimization and Control"
                        ),
                        year=2022,
                        venue="arXiv (Cornell University)",
                    ),
                    RegistryRecord(
                        source="Crossref",
                        doi="10.52202/068431-0340",
                        title=(
                            "Differentiable Analog Quantum Computing for "
                            "Optimization and Control"
                        ),
                        year=2022,
                        venue="Advances in Neural Information Processing Systems 35",
                        pages="4707-4721",
                    ),
                ]
            )
        ]
    )
    result = await verifier.verify_one(
        ParsedReference(
            reference_id="leng2022differentiable",
            raw_text="raw",
            title=(
                "Differentiable analog quantum computing for optimization "
                "and control"
            ),
            year=2022,
            venue="Advances in Neural Information Processing Systems",
            volume="35",
            pages="4707-4721",
        )
    )
    assert result.status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
    assert result.selected_record is not None
    assert result.selected_record.doi == "10.52202/068431-0340"
