from __future__ import annotations

import asyncio
from collections.abc import Iterable

from citeverify.compare.fields import compare_references, mismatches
from citeverify.compare.identifiers import build_identifier_candidates
from citeverify.lookup.base import LookupProvider, LookupResponse
from citeverify.models import (
    FieldComparison,
    IdentifierCandidate,
    IdentifierKind,
    JournalLocator,
    ParsedReference,
    RegistryRecord,
    VerificationResult,
    VerificationStatus,
)
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import normalize_journal
from citeverify.normalize.pages import normalize_article_number, normalize_pages
from citeverify.normalize.title import normalize_title, titles_match


class Verifier:
    def __init__(
        self,
        providers: Iterable[LookupProvider],
        max_concurrency: int = 5,
    ) -> None:
        self.providers = list(providers)
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def verify_many(
        self, references: list[ParsedReference]
    ) -> list[VerificationResult]:
        return await asyncio.gather(
            *(self.verify_one(reference) for reference in references)
        )

    async def verify_one(self, reference: ParsedReference) -> VerificationResult:
        candidates = build_identifier_candidates(reference)
        doi_candidate = _first_candidate(candidates, IdentifierKind.DOI)
        if doi_candidate:
            return await self._verify_by_doi(reference, candidates, doi_candidate)

        title_candidate = _first_candidate(candidates, IdentifierKind.TITLE)
        if title_candidate:
            return await self._verify_by_title(reference, candidates, title_candidate)

        locator_candidate = _first_candidate(candidates, IdentifierKind.JOURNAL_LOCATOR)
        if locator_candidate:
            return await self._verify_by_journal_locator(
                reference, candidates, locator_candidate
            )

        return VerificationResult(
            reference_id=reference.reference_id,
            raw_reference=reference.raw_text,
            parsed_reference=reference,
            identifier_candidates=candidates,
            identifier_used=None,
            status=VerificationStatus.INSUFFICIENT_METADATA,
        )

    async def _verify_by_doi(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        identifier: IdentifierCandidate,
    ) -> VerificationResult:
        responses = await self._query_providers("doi", identifier.normalized_value)
        records, sources, errors = _collect_responses(responses)
        selected = records[0] if records else None
        if selected is None:
            return _result(
                reference,
                candidates,
                identifier,
                sources,
                records,
                None,
                [],
                VerificationStatus.DOI_NOT_FOUND
                if not errors
                else VerificationStatus.LOOKUP_ERROR,
                errors,
            )

        comparisons = compare_references(reference, selected)
        status = _status_for_doi(comparisons)
        return _result(
            reference,
            candidates,
            identifier,
            sources,
            records,
            selected,
            comparisons,
            status,
            errors,
        )

    async def _verify_by_title(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        identifier: IdentifierCandidate,
    ) -> VerificationResult:
        responses = await self._query_providers("title", identifier.value)
        records, sources, errors = _collect_responses(responses)
        title_matches = _filter_title_matches(reference.title, records)
        if not title_matches:
            status = VerificationStatus.TITLE_NOT_FOUND
            if errors and not records:
                status = VerificationStatus.LOOKUP_ERROR
            return _result(
                reference,
                candidates,
                identifier,
                sources,
                records,
                None,
                [],
                status,
                errors,
            )
        narrowed = _dedupe_records(_narrow_by_supplied_fields(reference, title_matches))
        if len(narrowed) != 1:
            return _result(
                reference,
                candidates,
                identifier,
                sources,
                records,
                None,
                [],
                VerificationStatus.AMBIGUOUS_MATCH,
                errors,
            )
        selected = narrowed[0]
        comparisons = compare_references(reference, selected)
        status = (
            VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES
            if mismatches(comparisons)
            else VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
        )
        return _result(
            reference,
            candidates,
            identifier,
            sources,
            records,
            selected,
            comparisons,
            status,
            errors,
        )

    async def _verify_by_journal_locator(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        identifier: IdentifierCandidate,
    ) -> VerificationResult:
        locator = reference.journal_locator()
        responses = await self._query_providers("journal_locator", locator)
        records, sources, errors = _collect_responses(responses)
        matches = _dedupe_records(_filter_journal_locator_matches(locator, records))
        if not matches:
            status = VerificationStatus.JOURNAL_LOCATOR_NOT_FOUND
            if errors and not records:
                status = VerificationStatus.LOOKUP_ERROR
            return _result(
                reference,
                candidates,
                identifier,
                sources,
                records,
                None,
                [],
                status,
                errors,
            )
        if len(matches) != 1:
            return _result(
                reference,
                candidates,
                identifier,
                sources,
                records,
                None,
                [],
                VerificationStatus.AMBIGUOUS_MATCH,
                errors,
            )
        selected = matches[0]
        comparisons = compare_references(reference, selected)
        status = (
            VerificationStatus.JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES
            if mismatches(comparisons)
            else VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
        )
        return _result(
            reference,
            candidates,
            identifier,
            sources,
            records,
            selected,
            comparisons,
            status,
            errors,
        )

    async def _query_providers(
        self, query_kind: str, value: str | JournalLocator
    ) -> list[LookupResponse]:
        async def call(provider: LookupProvider) -> LookupResponse:
            async with self.semaphore:
                if query_kind == "doi":
                    return await provider.get_by_doi(str(value))
                if query_kind == "title":
                    return await provider.search_by_title(str(value))
                if isinstance(value, JournalLocator):
                    return await provider.search_by_journal_locator(value)
                raise ValueError(f"unsupported query kind: {query_kind}")

        return await asyncio.gather(*(call(provider) for provider in self.providers))


async def verify_references(
    references: list[ParsedReference],
    providers: Iterable[LookupProvider],
    max_concurrency: int = 5,
) -> list[VerificationResult]:
    verifier = Verifier(providers, max_concurrency=max_concurrency)
    return await verifier.verify_many(references)


def _first_candidate(
    candidates: list[IdentifierCandidate], kind: IdentifierKind
) -> IdentifierCandidate | None:
    return next((candidate for candidate in candidates if candidate.kind == kind), None)


def _collect_responses(
    responses: list[LookupResponse],
) -> tuple[list[RegistryRecord], list[str], list[str]]:
    records: list[RegistryRecord] = []
    sources: list[str] = []
    errors: list[str] = []
    for response in responses:
        sources.append(response.source)
        records.extend(response.records)
        if response.error:
            errors.append(f"{response.source}: {response.error}")
    return records, sources, errors


def _result(
    reference: ParsedReference,
    candidates: list[IdentifierCandidate],
    identifier: IdentifierCandidate | None,
    sources: list[str],
    records: list[RegistryRecord],
    selected: RegistryRecord | None,
    comparisons: list[FieldComparison],
    status: VerificationStatus,
    errors: list[str],
) -> VerificationResult:
    return VerificationResult(
        reference_id=reference.reference_id,
        raw_reference=reference.raw_text,
        parsed_reference=reference,
        identifier_candidates=candidates,
        identifier_used=identifier,
        lookup_sources=sources,
        lookup_records=records,
        selected_record=selected,
        comparisons=comparisons,
        status=status,
        lookup_errors=errors,
    )


def _status_for_doi(comparisons: list[FieldComparison]) -> VerificationStatus:
    mismatch_fields = {comparison.field for comparison in mismatches(comparisons)}
    if "title" in mismatch_fields:
        return VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK
    if mismatch_fields:
        return VerificationStatus.IDENTIFIER_CONFLICT
    return VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH


def _filter_title_matches(
    input_title: str | None, records: list[RegistryRecord]
) -> list[RegistryRecord]:
    return [record for record in records if titles_match(input_title, record.title)]


def _narrow_by_supplied_fields(
    reference: ParsedReference,
    records: list[RegistryRecord],
) -> list[RegistryRecord]:
    narrowed = records
    if reference.year:
        year_matches = [record for record in narrowed if record.year == reference.year]
        if year_matches:
            narrowed = year_matches
    if reference.doi:
        doi = normalize_doi(reference.doi)
        doi_matches = [
            record for record in narrowed if normalize_doi(record.doi) == doi
        ]
        if doi_matches:
            narrowed = doi_matches
    if reference.venue:
        venue = normalize_journal(reference.venue)
        venue_matches = [
            record for record in narrowed if normalize_journal(record.venue) == venue
        ]
        if venue_matches:
            narrowed = venue_matches
    return narrowed


def _dedupe_records(records: list[RegistryRecord]) -> list[RegistryRecord]:
    deduped: list[RegistryRecord] = []
    seen: set[tuple[str, ...]] = set()
    for record in records:
        key = _record_identity(record)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped


def _record_identity(record: RegistryRecord) -> tuple[str, ...]:
    doi = normalize_doi(record.doi)
    if doi:
        return ("doi", doi)
    return (
        "metadata",
        normalize_title(record.title) or "",
        str(record.year or ""),
        normalize_journal(record.venue) or "",
        record.volume or "",
        record.issue or "",
        normalize_pages(record.pages) or "",
        normalize_article_number(record.article_number) or "",
    )


def _filter_journal_locator_matches(
    locator: JournalLocator, records: list[RegistryRecord]
) -> list[RegistryRecord]:
    matches: list[RegistryRecord] = []
    for record in records:
        if (
            locator.issn
            and record.issn
            and not set(locator.issn).intersection(record.issn)
        ):
            continue
        if (
            locator.venue
            and not locator.issn
            and normalize_journal(locator.venue) != normalize_journal(record.venue)
        ):
            continue
        if locator.year and record.year and locator.year != record.year:
            continue
        if locator.volume and record.volume and locator.volume != record.volume:
            continue
        if locator.issue and record.issue and locator.issue != record.issue:
            continue
        if (
            locator.pages
            and record.pages
            and normalize_pages(locator.pages) != normalize_pages(record.pages)
        ):
            continue
        if locator.article_number and record.article_number:
            locator_article = normalize_article_number(locator.article_number)
            record_article = normalize_article_number(record.article_number)
            if locator_article != record_article:
                continue
        matches.append(record)
    return matches
