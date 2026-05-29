# CiteVerify Technical Implementation Plan

## Purpose

This document describes how to implement
[`reference_verification_plan.md`](reference_verification_plan.md) as a Python
package and CLI.

CiteVerify should verify references by checking supplied identifier candidates
against external bibliographic records. It must not produce confidence scores.
It should report the evidence found, the authoritative metadata returned, and
the exact supplied fields that mismatch.

## Implementation Principles

- Prefer deterministic identifier checks over broad search.
- Compare only fields supplied by the input reference.
- Keep parsing, normalization, lookup, comparison, and reporting as separate
  layers.
- Make every lookup decision auditable in the output.
- Treat `not found` as an evidence result, not proof of fabrication.
- Use caching and retries so repeated runs are reproducible and respectful of
  external APIs.

## Package Layout

```text
src/citeverify/
  __init__.py
  cli.py
  models.py
  config.py
  cache.py
  errors.py

  parsers/
    __init__.py
    bibtex.py
    raw_text.py
    latex.py
    pdf.py

  normalize/
    __init__.py
    doi.py
    title.py
    author.py
    journal.py
    pages.py
    text.py

  lookup/
    __init__.py
    base.py
    crossref.py
    datacite.py
    openalex.py
    arxiv.py
    pubmed.py

  compare/
    __init__.py
    fields.py
    authors.py
    references.py
    identifiers.py

  reports/
    __init__.py
    markdown.py
    json.py

tests/
  unit/
  integration/
  fixtures/
```

## Core Data Models

Use `pydantic` models so parsed input, lookup results, and final reports have
explicit schemas.

### ParsedReference

```python
class ParsedReference(BaseModel):
    reference_id: str
    raw_text: str
    title: str | None = None
    authors: list[ParsedAuthor] = []
    year: int | None = None
    venue: str | None = None
    issn: list[str] = []
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    article_number: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    pmid: str | None = None
    isbn: str | None = None
    url: str | None = None
    source_format: Literal["bibtex", "raw_text", "latex", "pdf"]
```

### ParsedAuthor

```python
class ParsedAuthor(BaseModel):
    raw_name: str
    family_name: str | None = None
    given_names: list[str] = []
    given_initials: list[str] = []
    suffix: str | None = None
    orcid: str | None = None
    position_in_list: int | None = None
    is_et_al_marker: bool = False
```

### JournalLocator

```python
class JournalLocator(BaseModel):
    venue: str | None = None
    issn: list[str] = []
    year: int | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    article_number: str | None = None
```

### IdentifierCandidate

```python
class IdentifierCandidate(BaseModel):
    kind: Literal["doi", "title", "journal_locator", "arxiv_id", "pmid", "isbn", "url"]
    value: str
    normalized_value: str
    available_fields: list[str]
```

### RegistryRecord

This model represents metadata returned by Crossref, DataCite, OpenAlex, arXiv,
PubMed, or another lookup provider.

```python
class RegistryRecord(BaseModel):
    source: str
    source_record_url: str | None = None
    title: str | None = None
    authors: list[ParsedAuthor] = []
    year: int | None = None
    venue: str | None = None
    issn: list[str] = []
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
```

### FieldComparison

```python
class FieldComparison(BaseModel):
    field: str
    input_value: Any
    found_value: Any
    result: Literal["match", "mismatch", "not_checked", "additional_metadata"]
    note: str | None = None
```

### VerificationResult

```python
class VerificationResult(BaseModel):
    reference_id: str
    raw_reference: str
    parsed_reference: ParsedReference
    identifier_candidates: list[IdentifierCandidate]
    identifier_used: IdentifierCandidate | None
    lookup_sources: list[str]
    lookup_records: list[RegistryRecord]
    selected_record: RegistryRecord | None
    comparisons: list[FieldComparison]
    status: VerificationStatus
    lookup_errors: list[str] = []
```

## Status Labels

Use enum values rather than free-form strings.

```text
FOUND_NO_SUPPLIED_FIELD_MISMATCH
DOI_NOT_FOUND
TITLE_NOT_FOUND
JOURNAL_LOCATOR_NOT_FOUND
AMBIGUOUS_MATCH
DOI_RESOLVES_TO_DIFFERENT_WORK
TITLE_FOUND_WITH_FIELD_MISMATCHES
JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES
IDENTIFIER_CONFLICT
INSUFFICIENT_METADATA
UNSUPPORTED_REFERENCE_TYPE
LOOKUP_ERROR
```

## End-to-End Pipeline

```text
input file
  -> parser
  -> ParsedReference[]
  -> normalizers
  -> IdentifierCandidate[]
  -> lookup planner
  -> lookup providers
  -> RegistryRecord[]
  -> candidate selector
  -> field comparators
  -> VerificationResult[]
  -> full report + short exception report + JSON
```

## Lookup Planner

The lookup planner decides which identifiers to try and in what order.

### Priority Order

1. DOI
2. arXiv ID or PMID when explicitly present
3. Title
4. Journal locator
5. URL or ISBN as later-stage fallback

### DOI Present

```text
Normalize DOI.
Query DOI-native providers.
If found:
  select DOI record.
  compare supplied fields.
  if supplied title mismatches found title:
    status = DOI_RESOLVES_TO_DIFFERENT_WORK
  else if any supplied field mismatches:
    status = TITLE_FOUND_WITH_FIELD_MISMATCHES or IDENTIFIER_CONFLICT
  else:
    status = FOUND_NO_SUPPLIED_FIELD_MISMATCH
If not found:
  status = DOI_NOT_FOUND
  optionally search title or journal locator and report any conflicting record.
```

### DOI Missing, Title Present

```text
Normalize title.
Search providers by title.
Filter candidates by exact normalized title or high-quality normalized match.
If no candidate:
  status = TITLE_NOT_FOUND
If multiple candidates remain:
  status = AMBIGUOUS_MATCH
If one candidate remains:
  compare supplied fields.
  if mismatches exist:
    status = TITLE_FOUND_WITH_FIELD_MISMATCHES
  else:
    status = FOUND_NO_SUPPLIED_FIELD_MISMATCH
```

### DOI and Title Missing, Journal Locator Present

```text
Build normalized journal locator.
Search by venue/ISSN + year + volume + issue + page/article number.
If no candidate:
  status = JOURNAL_LOCATOR_NOT_FOUND
If multiple candidates remain:
  status = AMBIGUOUS_MATCH
If one candidate remains:
  compare supplied fields.
  if mismatches exist:
    status = JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES
  else:
    status = FOUND_NO_SUPPLIED_FIELD_MISMATCH
```

## Lookup Providers

All providers should implement one interface.

```python
class LookupProvider(Protocol):
    name: str

    async def get_by_doi(self, doi: str) -> LookupResponse: ...
    async def search_by_title(self, title: str) -> LookupResponse: ...
    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse: ...
```

### LookupResponse

```python
class LookupResponse(BaseModel):
    source: str
    query_kind: str
    query_value: str
    records: list[RegistryRecord]
    error: str | None = None
    raw_status_code: int | None = None
```

### Provider Responsibilities

Each provider should:

- build provider-specific HTTP requests;
- handle provider-specific response formats;
- map returned metadata into `RegistryRecord`;
- avoid comparison logic;
- expose raw response metadata for auditability;
- use retry, timeout, and rate-limit settings from shared config.

## Normalization

Normalization should preserve original values while producing comparison keys.

### DOI Normalization

Rules:

- Strip URL prefixes such as `https://doi.org/`.
- Strip leading `doi:`.
- Lowercase ASCII DOI text.
- Remove trailing punctuation.
- Preserve slash and internal punctuation.

Examples:

```text
https://doi.org/10.1103/PhysRevLett.121.090502
-> 10.1103/physrevlett.121.090502

doi: 10.1000/XYZ.
-> 10.1000/xyz
```

### Title Normalization

Rules:

- Unicode normalize.
- Remove LaTeX braces and simple markup.
- Lowercase.
- Collapse whitespace.
- Normalize quotes, dashes, and subtitle punctuation.
- Remove terminal punctuation.
- Preserve meaningful math tokens when possible.

Title comparison should produce:

```text
exact_normalized_match
near_normalized_match
mismatch
```

The report should not expose a numeric similarity score.

### Journal Normalization

Rules:

- Normalize punctuation, ampersands, casing, and whitespace.
- Treat common abbreviations as aliases where a known mapping exists.
- Prefer ISSN when supplied.
- Keep both original venue string and normalized venue key.

Examples:

```text
Phys. Rev. Lett.
Physical Review Letters
PRL
```

These may map to the same journal alias when the alias table knows them.

### Page and Article Number Normalization

Rules:

- Normalize page ranges such as `100--112`, `100-112`, and `100–112`.
- Preserve article numbers separately from page ranges.
- Treat `090502` in APS-style references as an article number, not a page
  range, when provider metadata indicates article-number format.

## Author Parsing and Comparison

Author comparison should check only supplied names.

### Parsing Rules

The parser should detect:

- `et al.`, `etal`, and similar markers;
- semicolon-separated author lists;
- BibTeX `and`-separated author lists;
- `Family, Given` format;
- `Given Family` format;
- initials-only given names.

### Comparison Rules

For each supplied non-`et al.` author:

1. Compare against the corresponding found author when order is clear.
2. If order is not clear, compare against all found authors and accept the best
   compatible name.
3. Family names should match exactly after normalization, with limited fuzzy
   tolerance for accents and punctuation.
4. Given names are compatible when supplied initials match found given-name
   initials.
5. Do not report missing later authors when the input contains `et al.`.
6. Do not report registry-only authors as mismatches.

### Author Mismatch Examples

```text
Input: Smith, J.; Wang, L.; et al.
Found: Smith, John; Wang, Li; Brown, Amy
Result: match

Input: Smith, J.
Found: Smith, John
Result: match

Input: Smith, J.
Found: Wang, John
Result: mismatch

Input: Smith, J.; Wang, L.
Found: Smith, John; Brown, Amy
Result: Wang mismatches
```

## Field Comparison

Each comparator should return a `FieldComparison`.

### Comparison Matrix

```text
doi:
  exact normalized DOI match

title:
  exact or near normalized title match

authors:
  supplied author names only

year:
  exact year match

venue:
  ISSN match if available, otherwise normalized venue alias match

volume:
  normalized string match

issue:
  normalized string match

pages:
  normalized page range match

article_number:
  normalized article number match

url:
  normalized URL match when URL is used as an identifier or supplied field
```

### Missing Field Policy

```text
Input missing, registry has value:
  result = additional_metadata

Input has value, registry missing value:
  result = not_checked
  note = source did not return this field

Input has value, registry has different value:
  result = mismatch

Input has value, registry has compatible value:
  result = match
```

## Candidate Selection

Candidate selection should be deterministic and explainable.

### DOI Lookup

If a DOI lookup returns one record, select that record. Do not override it with
title search results. If the title conflicts, report
`DOI_RESOLVES_TO_DIFFERENT_WORK`.

### Title Lookup

For title lookup:

1. Normalize all candidate titles.
2. Keep exact normalized matches.
3. If no exact match exists, keep near normalized matches.
4. Use supplied year, author, venue, volume, issue, and page fields only to
   reduce ambiguity, not to create a hidden score.
5. If more than one candidate remains after deterministic filtering, report
   `AMBIGUOUS_MATCH`.

### Journal Locator Lookup

For journal locator lookup:

1. Match ISSN if available.
2. Otherwise match normalized venue alias.
3. Filter by year.
4. Filter by volume.
5. Filter by issue if supplied.
6. Filter by page or article number.
7. If more than one candidate remains, report `AMBIGUOUS_MATCH`.

## Reports

Generate three output formats:

```text
full_report.md
short_report.md
report.json
```

### Full Markdown Report

Includes every reference.

Required sections per reference:

```text
raw input reference
parsed fields
identifier candidates
identifier used
lookup sources queried
selected record
field comparisons
mismatches
additional metadata
status
lookup errors, if any
```

### Short Exception Report

Includes only references with:

```text
DOI_NOT_FOUND
TITLE_NOT_FOUND
JOURNAL_LOCATOR_NOT_FOUND
AMBIGUOUS_MATCH
DOI_RESOLVES_TO_DIFFERENT_WORK
TITLE_FOUND_WITH_FIELD_MISMATCHES
JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES
IDENTIFIER_CONFLICT
INSUFFICIENT_METADATA
UNSUPPORTED_REFERENCE_TYPE
LOOKUP_ERROR
```

If every reference is clean, the short report should explicitly say:

```text
No references with lookup failures or supplied-field mismatches were found.
```

### JSON Report

The JSON report should serialize the full `VerificationResult[]` list and a
small run summary:

```json
{
  "tool": "citeverify",
  "version": "0.1.0",
  "input": "references.bib",
  "summary": {
    "total_references": 0,
    "clean_references": 0,
    "exception_references": 0
  },
  "results": []
}
```

## CLI Design

Use `typer` for the CLI.

### Main Command

```bash
citeverify verify INPUT
```

Options:

```bash
--full-report PATH
--short-report PATH
--json-report PATH
--format bibtex|raw-text|latex|pdf|auto
--cache PATH
--no-cache
--offline
--fail-on-exceptions
--timeout SECONDS
--max-concurrency N
```

### Examples

```bash
citeverify verify references.bib

citeverify verify refs.txt \
  --format raw-text \
  --full-report full_report.md \
  --short-report short_report.md \
  --json-report report.json

citeverify verify references.bib --offline --cache .citeverify-cache.sqlite
```

### Exit Codes

```text
0: command completed; no exceptions found
1: command completed; exceptions found and --fail-on-exceptions was set
2: input parsing failed
3: lookup configuration failed
4: unexpected runtime error
```

Without `--fail-on-exceptions`, references with mismatches should not make the
process fail. They should be reported.

## Caching

Use SQLite for HTTP response caching.

### Cache Key

```text
provider_name
query_kind
normalized_query_value
provider_api_version_or_base_url
```

### Cache Value

```text
status_code
response_headers
response_body
created_at
expires_at
```

### Cache Behavior

- Cache successful lookup responses.
- Cache clear not-found responses for a shorter duration.
- Do not cache transient network errors.
- Allow `--offline` mode to use only cached records.
- Include cache hit/miss information in verbose logs, not in normal reports.

## HTTP and Rate Limits

Use `httpx.AsyncClient`.

Shared settings:

```text
timeout: 20 seconds by default
max_concurrency: 5 by default
retry attempts: 3
retry backoff: exponential
user agent: citeverify/{version} contact configurable
```

Provider clients should handle:

- 404 not found;
- 429 rate limit;
- 5xx server errors;
- malformed responses;
- timeout;
- connection errors.

Lookup errors should be captured in `VerificationResult.lookup_errors` and
reported as `LOOKUP_ERROR` only when no usable evidence can be produced.

## Parsing Strategy

### Phase 1 Parsers

Implement first:

- BibTeX parser;
- raw text parser with one reference per paragraph or numbered item.

### Phase 2 Parsers

Implement later:

- LaTeX `.bbl` and bibliography extraction;
- PDF reference extraction.

PDF parsing should be treated as best effort and should preserve raw extracted
reference text for auditability.

## Configuration

Support configuration from CLI flags and environment variables.

Suggested environment variables:

```text
CITEVERIFY_CACHE
CITEVERIFY_CONTACT_EMAIL
CITEVERIFY_TIMEOUT
CITEVERIFY_MAX_CONCURRENCY
CITEVERIFY_CROSSREF_MAILTO
CITEVERIFY_SEMANTIC_SCHOLAR_API_KEY
CITEVERIFY_NCBI_API_KEY
```

Do not require API keys for the MVP. Provider support requiring credentials
should degrade gracefully when credentials are absent.

## Testing Plan

### Unit Tests

Test:

- DOI normalization;
- title normalization;
- journal alias normalization;
- page range normalization;
- author parsing;
- initials matching;
- `et al.` handling;
- field comparison behavior;
- status selection.

### Fixture-Based Tests

Create static fixtures for provider responses:

```text
tests/fixtures/crossref/doi_found.json
tests/fixtures/crossref/doi_not_found.json
tests/fixtures/crossref/title_search_multiple.json
tests/fixtures/datacite/doi_found.json
```

Use fixtures for deterministic tests instead of live API calls.

### Integration Tests

Mark live provider tests separately, for example:

```bash
pytest -m integration
```

Integration tests should be optional and skipped by default unless explicitly
enabled.

### Golden Report Tests

For representative input files, compare generated Markdown/JSON reports against
approved expected outputs.

Golden cases:

- clean DOI reference;
- DOI not found;
- DOI found but title mismatch;
- title found with year mismatch;
- title ambiguous;
- journal locator found;
- journal locator not found;
- `et al.` author list;
- initials-only author names.

## MVP Milestones

### Milestone 1: Project Skeleton

Deliverables:

- `pyproject.toml`;
- `src/citeverify/` package;
- Typer CLI shell;
- pytest setup;
- README usage placeholder.

### Milestone 2: Models and Normalization

Deliverables:

- Pydantic models;
- DOI normalization;
- title normalization;
- author parsing and normalization;
- page and article-number normalization;
- unit tests.

### Milestone 3: BibTeX and Raw Text Parsing

Deliverables:

- BibTeX parser;
- raw reference parser;
- parsed reference fixtures;
- parser tests.

### Milestone 4: DOI Lookup

Deliverables:

- Crossref client;
- DataCite client;
- shared lookup provider interface;
- HTTP retry and timeout behavior;
- cache layer;
- DOI lookup tests using fixtures.

### Milestone 5: DOI-Based Verification

Deliverables:

- DOI lookup planner path;
- field comparison engine;
- status selection for DOI cases;
- full JSON output for DOI cases.

### Milestone 6: Title Lookup

Deliverables:

- Crossref title search;
- optional OpenAlex title search;
- deterministic candidate filtering;
- ambiguous match handling;
- title-based verification tests.

### Milestone 7: Journal Locator Lookup

Deliverables:

- journal locator construction;
- journal/ISSN matching;
- volume/issue/page/article filtering;
- journal locator verification tests.

### Milestone 8: Markdown Reports

Deliverables:

- full evidence report;
- short exception report;
- clean-run short report message;
- golden report tests.

### Milestone 9: CLI Polish

Deliverables:

- CLI options;
- exit codes;
- offline cache mode;
- helpful terminal output;
- packaging metadata.

### Milestone 10: Later Input Formats

Deliverables:

- LaTeX parser;
- `.bbl` parser;
- PDF reference extraction;
- extraction quality warnings.

## First Implementation Slice

The first useful end-to-end slice should be deliberately narrow:

```text
Input: references.bib
Supported identifiers: DOI only
Lookup sources: Crossref, then DataCite
Reports: JSON and full Markdown
Tests: fixture-based DOI found, DOI not found, DOI-title mismatch
```

This slice proves the central architecture before adding broader parsing and
search.

## Open Technical Decisions

- Which journal alias source to use for robust abbreviation handling.
- Whether to vendor a small local journal alias table for common publishers.
- How strict near-title matching should be before reporting ambiguity.
- Whether OpenAlex should be enabled in the MVP or added after Crossref title
  lookup works.
- Which PDF extraction backend to support first.
- Whether report JSON should include full raw provider responses by default or
  only behind a verbose flag.

## Non-Goals for MVP

- Proving that a not-found reference is fabricated.
- Assigning numeric confidence scores.
- Correcting references automatically.
- Building a web UI.
- Supporting every citation style.
- Perfect PDF bibliography extraction.

## Quality Bar

Before treating the MVP as usable:

- all deterministic normalization and comparison tests pass;
- golden reports are stable;
- live integration tests can be run manually;
- reports clearly separate lookup failures from mismatches;
- every mismatch includes both input and found values;
- clean references are omitted from the short exception report;
- no API key is required for basic DOI verification.
