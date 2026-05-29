from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SourceFormat(StrEnum):
    BIBTEX = "bibtex"
    RAW_TEXT = "raw_text"
    LATEX = "latex"
    PDF = "pdf"


class IdentifierKind(StrEnum):
    DOI = "doi"
    TITLE = "title"
    JOURNAL_LOCATOR = "journal_locator"
    ARXIV_ID = "arxiv_id"
    PMID = "pmid"
    ISBN = "isbn"
    URL = "url"


class ComparisonResult(StrEnum):
    MATCH = "match"
    MISMATCH = "mismatch"
    NOT_CHECKED = "not_checked"
    ADDITIONAL_METADATA = "additional_metadata"


class VerificationStatus(StrEnum):
    FOUND_NO_SUPPLIED_FIELD_MISMATCH = "FOUND_NO_SUPPLIED_FIELD_MISMATCH"
    DOI_NOT_FOUND = "DOI_NOT_FOUND"
    TITLE_NOT_FOUND = "TITLE_NOT_FOUND"
    JOURNAL_LOCATOR_NOT_FOUND = "JOURNAL_LOCATOR_NOT_FOUND"
    AMBIGUOUS_MATCH = "AMBIGUOUS_MATCH"
    DOI_RESOLVES_TO_DIFFERENT_WORK = "DOI_RESOLVES_TO_DIFFERENT_WORK"
    TITLE_FOUND_WITH_FIELD_MISMATCHES = "TITLE_FOUND_WITH_FIELD_MISMATCHES"
    JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES = (
        "JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES"
    )
    IDENTIFIER_CONFLICT = "IDENTIFIER_CONFLICT"
    INSUFFICIENT_METADATA = "INSUFFICIENT_METADATA"
    UNSUPPORTED_REFERENCE_TYPE = "UNSUPPORTED_REFERENCE_TYPE"
    LOOKUP_ERROR = "LOOKUP_ERROR"


EXCEPTION_STATUSES = {
    VerificationStatus.DOI_NOT_FOUND,
    VerificationStatus.TITLE_NOT_FOUND,
    VerificationStatus.JOURNAL_LOCATOR_NOT_FOUND,
    VerificationStatus.AMBIGUOUS_MATCH,
    VerificationStatus.DOI_RESOLVES_TO_DIFFERENT_WORK,
    VerificationStatus.TITLE_FOUND_WITH_FIELD_MISMATCHES,
    VerificationStatus.JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES,
    VerificationStatus.IDENTIFIER_CONFLICT,
    VerificationStatus.INSUFFICIENT_METADATA,
    VerificationStatus.UNSUPPORTED_REFERENCE_TYPE,
    VerificationStatus.LOOKUP_ERROR,
}


class ParsedAuthor(BaseModel):
    raw_name: str
    family_name: str | None = None
    given_names: list[str] = Field(default_factory=list)
    given_initials: list[str] = Field(default_factory=list)
    suffix: str | None = None
    orcid: str | None = None
    position_in_list: int | None = None
    is_et_al_marker: bool = False


class JournalLocator(BaseModel):
    venue: str | None = None
    issn: list[str] = Field(default_factory=list)
    year: int | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    article_number: str | None = None

    def has_lookup_value(self) -> bool:
        has_venue = bool(self.venue or self.issn)
        has_location = bool(
            self.year or self.volume or self.issue or self.pages or self.article_number
        )
        return has_venue and has_location


class ParsedReference(BaseModel):
    reference_id: str
    raw_text: str
    title: str | None = None
    authors: list[ParsedAuthor] = Field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    issn: list[str] = Field(default_factory=list)
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    article_number: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    pmid: str | None = None
    isbn: str | None = None
    url: str | None = None
    source_format: SourceFormat = SourceFormat.RAW_TEXT

    def journal_locator(self) -> JournalLocator:
        return JournalLocator(
            venue=self.venue,
            issn=self.issn,
            year=self.year,
            volume=self.volume,
            issue=self.issue,
            pages=self.pages,
            article_number=self.article_number,
        )


class IdentifierCandidate(BaseModel):
    kind: IdentifierKind
    value: str
    normalized_value: str
    available_fields: list[str] = Field(default_factory=list)


class RegistryRecord(BaseModel):
    source: str
    source_record_url: str | None = None
    title: str | None = None
    authors: list[ParsedAuthor] = Field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    issn: list[str] = Field(default_factory=list)
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    article_number: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    pmid: str | None = None
    isbn: str | None = None
    url: str | None = None
    record_type: str | None = None
    raw_response: dict[str, Any] | None = None


class FieldComparison(BaseModel):
    field: str
    input_value: Any
    found_value: Any
    result: ComparisonResult
    note: str | None = None


class VerificationResult(BaseModel):
    reference_id: str
    raw_reference: str
    parsed_reference: ParsedReference
    identifier_candidates: list[IdentifierCandidate] = Field(default_factory=list)
    identifier_used: IdentifierCandidate | None = None
    lookup_sources: list[str] = Field(default_factory=list)
    lookup_records: list[RegistryRecord] = Field(default_factory=list)
    selected_record: RegistryRecord | None = None
    comparisons: list[FieldComparison] = Field(default_factory=list)
    status: VerificationStatus
    lookup_errors: list[str] = Field(default_factory=list)

    @property
    def has_exception(self) -> bool:
        return self.status in EXCEPTION_STATUSES


class RunSummary(BaseModel):
    total_references: int
    clean_references: int
    exception_references: int


class VerificationReport(BaseModel):
    tool: str = "citeverify"
    version: str
    input: str
    summary: RunSummary
    results: list[VerificationResult]
