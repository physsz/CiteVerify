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
from citeverify.normalize.arxiv import (
    extract_arxiv_id,
    is_arxiv_venue,
    normalize_arxiv_id,
)
from citeverify.normalize.doi import extract_doi, normalize_doi
from citeverify.normalize.journal import normalize_journal, venues_compatible
from citeverify.normalize.pages import (
    normalize_article_number,
    normalize_pages,
    pages_compatible,
)
from citeverify.normalize.title import normalize_title, titles_match

_JOURNAL_LOCATOR_COMPARISON_FIELDS = {
    "year",
    "venue",
    "volume",
    "issue",
    "pages",
    "article_number",
}
_FALLBACK_IDENTIFIER_FIELDS = _JOURNAL_LOCATOR_COMPARISON_FIELDS | {"doi", "title"}
_APS_DOI_JOURNAL_STEMS = {
    "physical review letters": "PhysRevLett",
    "physical review a": "PhysRevA",
    "physical review b": "PhysRevB",
    "physical review c": "PhysRevC",
    "physical review d": "PhysRevD",
    "physical review e": "PhysRevE",
    "physical review applied": "PhysRevApplied",
    "physical review research": "PhysRevResearch",
    "physical review x": "PhysRevX",
    "prx quantum": "PRXQuantum",
    "reviews of modern physics": "RevModPhys",
}


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

        arxiv_candidate = _first_candidate(candidates, IdentifierKind.ARXIV_ID)
        if arxiv_candidate:
            return await self._verify_by_arxiv_id(
                reference, candidates, arxiv_candidate
            )

        title_candidate = _first_candidate(candidates, IdentifierKind.TITLE)
        if title_candidate:
            result = await self._verify_by_title(reference, candidates, title_candidate)
            if result.selected_record is not None:
                return result
            fallback = await self._fallback_to_journal_locator(reference, candidates)
            if fallback is not None:
                return fallback
            return result

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
            fallback = await self._fallback_to_title_or_journal_locator(
                reference, candidates
            )
            if fallback is not None:
                return fallback
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
        if _should_try_fallback_after_doi_result(status, comparisons):
            fallback = await self._fallback_after_doi_conflict(
                reference, candidates, status, comparisons
            )
            if fallback is not None:
                return fallback
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

    async def _fallback_after_doi_conflict(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        status: VerificationStatus,
        comparisons: list[FieldComparison],
    ) -> VerificationResult | None:
        if _should_try_title_after_doi_result(status, comparisons):
            title_result = await self._fallback_to_title(reference, candidates)
            if title_result is not None:
                return title_result
        if not _should_try_journal_locator_after_doi_result(status, comparisons):
            return None
        return await self._fallback_to_journal_locator(reference, candidates)

    async def _fallback_to_title_or_journal_locator(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
    ) -> VerificationResult | None:
        title_result = await self._fallback_to_title(reference, candidates)
        if title_result is not None:
            return title_result
        return await self._fallback_to_journal_locator(reference, candidates)

    async def _fallback_to_title(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
    ) -> VerificationResult | None:
        title_candidate = _first_candidate(candidates, IdentifierKind.TITLE)
        if title_candidate is None:
            return None
        result = await self._verify_by_title(reference, candidates, title_candidate)
        if _is_actionable_fallback_result(result):
            return result
        return None

    async def _fallback_to_journal_locator(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
    ) -> VerificationResult | None:
        locator_candidate = _first_candidate(candidates, IdentifierKind.JOURNAL_LOCATOR)
        if locator_candidate is None:
            return None
        result = await self._verify_by_journal_locator(
            reference, candidates, locator_candidate
        )
        if _is_actionable_fallback_result(result):
            return result
        return None

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
            narrowed = _prefer_doi_bearing_records(narrowed)
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

    async def _verify_by_arxiv_id(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        identifier: IdentifierCandidate,
    ) -> VerificationResult:
        responses = await self._query_providers("arxiv_id", identifier.normalized_value)
        records, sources, errors = _collect_responses(responses)
        matches = _dedupe_records(
            [
                record
                for record in records
                if _record_arxiv_identity(record) == identifier.normalized_value
            ]
        )
        if not matches:
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
        if len(matches) != 1:
            matches = _prefer_doi_bearing_records(matches)
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
            VerificationStatus.IDENTIFIER_CONFLICT
            if any(
                comparison.field == "title"
                for comparison in mismatches(comparisons)
            )
            else (
                VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES
                if mismatches(comparisons)
                else VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH
            )
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
        inferred_doi = _infer_aps_doi(locator)
        if inferred_doi:
            inferred_result = await self._verify_journal_locator_by_inferred_doi(
                reference, candidates, identifier, inferred_doi
            )
            if inferred_result is not None:
                return inferred_result

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

    async def _verify_journal_locator_by_inferred_doi(
        self,
        reference: ParsedReference,
        candidates: list[IdentifierCandidate],
        identifier: IdentifierCandidate,
        inferred_doi: str,
    ) -> VerificationResult | None:
        responses = await self._query_providers("doi", inferred_doi)
        records, sources, errors = _collect_responses(responses)
        selected = records[0] if records else None
        if selected is None:
            return None
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
                if query_kind == "arxiv_id":
                    return await provider.get_by_arxiv_id(str(value))
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
        records.extend(
            record for record in response.records if _record_has_metadata(record)
        )
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


def _should_try_fallback_after_doi_result(
    status: VerificationStatus, comparisons: list[FieldComparison]
) -> bool:
    if status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH:
        return False
    mismatch_fields = {comparison.field for comparison in mismatches(comparisons)}
    return bool(mismatch_fields.intersection(_FALLBACK_IDENTIFIER_FIELDS))


def _should_try_title_after_doi_result(
    status: VerificationStatus, comparisons: list[FieldComparison]
) -> bool:
    if status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH:
        return False
    mismatch_fields = {comparison.field for comparison in mismatches(comparisons)}
    return "doi" in mismatch_fields or "title" in mismatch_fields


def _should_try_journal_locator_after_doi_result(
    status: VerificationStatus, comparisons: list[FieldComparison]
) -> bool:
    if status == VerificationStatus.FOUND_NO_SUPPLIED_FIELD_MISMATCH:
        return False
    mismatch_fields = {comparison.field for comparison in mismatches(comparisons)}
    if "doi" in mismatch_fields:
        return True
    return bool(mismatch_fields.intersection(_JOURNAL_LOCATOR_COMPARISON_FIELDS))


def _is_actionable_fallback_result(result: VerificationResult) -> bool:
    return (
        result.selected_record is not None
        or result.status == VerificationStatus.AMBIGUOUS_MATCH
    )


def _filter_title_matches(
    input_title: str | None, records: list[RegistryRecord]
) -> list[RegistryRecord]:
    normalized_input = normalize_title(input_title)
    exact_matches = [
        record
        for record in records
        if normalized_input and normalize_title(record.title) == normalized_input
    ]
    if exact_matches:
        return exact_matches
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
    doi = normalize_doi(reference.doi) or extract_doi(reference.url or "")
    if doi:
        doi_matches = [
            record for record in narrowed if normalize_doi(record.doi) == doi
        ]
        if doi_matches:
            narrowed = doi_matches
    if reference.venue and not is_arxiv_venue(reference.venue):
        venue_matches = [
            record
            for record in narrowed
            if venues_compatible(
                reference.venue,
                record.venue,
                reference.volume,
                record.volume,
            )
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
    arxiv_id = _record_arxiv_identity(record)
    if arxiv_id:
        return ("arxiv", arxiv_id)
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


def _record_has_metadata(record: RegistryRecord) -> bool:
    return any(
        value not in (None, "", [], {})
        for value in [
            record.source_record_url,
            record.title,
            record.authors,
            record.year,
            record.venue,
            record.issn,
            record.volume,
            record.issue,
            record.pages,
            record.article_number,
            record.doi,
            record.arxiv_id,
            record.pmid,
            record.isbn,
            record.url,
        ]
    )


def _record_arxiv_identity(record: RegistryRecord) -> str | None:
    return normalize_arxiv_id(record.arxiv_id) or extract_arxiv_id(
        record.doi,
        record.url,
        record.source_record_url,
        record.venue,
    )


def _prefer_doi_bearing_records(records: list[RegistryRecord]) -> list[RegistryRecord]:
    doi_records = [record for record in records if record.doi]
    return doi_records if doi_records else records


def _infer_aps_doi(locator: JournalLocator) -> str | None:
    journal = normalize_journal(locator.venue)
    stem = _APS_DOI_JOURNAL_STEMS.get(journal or "")
    volume = _doi_part(locator.volume)
    locator_number = _aps_locator_number(locator)
    if not stem or not volume or not locator_number:
        return None
    return normalize_doi(f"10.1103/{stem}.{volume}.{locator_number}")


def _aps_locator_number(locator: JournalLocator) -> str | None:
    article_number = normalize_article_number(locator.article_number)
    if article_number:
        return _doi_part(article_number)
    pages = normalize_pages(locator.pages)
    if not pages:
        return None
    first_page = pages.split("-", maxsplit=1)[0]
    return _doi_part(first_page)


def _doi_part(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().strip(" .,")
    return value or None


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
            and (
                not record.venue
                or not venues_compatible(
                    locator.venue,
                    record.venue,
                    locator.volume,
                    record.volume,
                )
            )
        ):
            continue
        if locator.year and (
            record.year is None or locator.year != record.year
        ):
            continue
        has_specific_locator_field = False
        confirmed_specific_locator_field = False
        if locator.volume:
            has_specific_locator_field = True
            if record.volume:
                if locator.volume != record.volume:
                    continue
                confirmed_specific_locator_field = True
        if locator.issue:
            has_specific_locator_field = True
            if record.issue:
                if locator.issue != record.issue:
                    continue
                confirmed_specific_locator_field = True
        if locator.pages:
            has_specific_locator_field = True
            if record.pages:
                if not pages_compatible(locator.pages, record.pages):
                    continue
                confirmed_specific_locator_field = True
            elif record.article_number:
                locator_pages = normalize_pages(locator.pages)
                record_article = normalize_article_number(record.article_number)
                if locator_pages != record_article:
                    continue
                confirmed_specific_locator_field = True
        if locator.article_number:
            has_specific_locator_field = True
            if record.article_number:
                locator_article = normalize_article_number(locator.article_number)
                record_article = normalize_article_number(record.article_number)
                if locator_article != record_article:
                    continue
                confirmed_specific_locator_field = True
            elif record.pages:
                locator_article = normalize_article_number(locator.article_number)
                record_pages = normalize_pages(record.pages)
                if locator_article != record_pages:
                    continue
                confirmed_specific_locator_field = True
        if (
            not has_specific_locator_field
            or not confirmed_specific_locator_field
        ):
            continue
        matches.append(record)
    return matches
