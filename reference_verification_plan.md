# CiteVerify Reference Verification Plan

## Goal

Build Python code that verifies whether article references correspond to real
bibliographic records and whether the supplied metadata matches authoritative
sources.

The tool should not output confidence scores. It should honestly report:

- what identifier was used;
- whether a record was found;
- what metadata was returned;
- which supplied fields mismatch;
- which fields could not be checked.

## Core Principle

The verifier is an evidence reporter, not a judge.

It should avoid vague conclusions like "probably real" or numeric scores.
Instead, each reference gets a factual result:

```text
DOI found, but title mismatches.
Title found, but year and volume mismatch.
Journal location not found.
Title found with no mismatches in supplied fields.
```

## Identifier Candidates

Each reference may contain one or more identifier candidates.

### 1. DOI

The DOI is the strongest identifier when present.

Examples:

```text
10.1103/PhysRevLett.121.090502
https://doi.org/10.1103/PhysRevLett.121.090502
doi:10.xxxx/yyyy
```

### 2. Title

The title is used when the DOI is missing, or as a cross-check when DOI metadata
conflicts with the supplied reference.

Title matching should normalize:

- capitalization;
- punctuation;
- LaTeX markup;
- Unicode accents;
- whitespace;
- subtitle separators;
- math symbols where possible.

### 3. Journal Locator

The journal locator is used when DOI and title are absent or weak.

The journal locator is built from:

```text
journal name or ISSN
year
volume
issue
page range or article number
```

Example:

```text
Physical Review Letters, 121, 090502, 2018
```

## Lookup Strategy

### Case 1: DOI Provided

1. Normalize the DOI.
2. Query DOI metadata sources:
   - Crossref for most journal articles, proceedings, books, chapters, and
     reports.
   - DataCite for datasets, software, and some research objects.
   - DOI agency lookup if needed.
3. If the DOI is not found, report `DOI_NOT_FOUND`.
4. If the DOI is found, compare returned metadata against supplied metadata.
5. If the DOI title mismatches the supplied title, report that the DOI resolves
   to a different work.
6. If the title matches but other fields mismatch, report each mismatch
   individually.
7. Optionally search by supplied title or journal locator to see whether the
   input metadata points to a different DOI.

### Case 2: DOI Missing, Title Provided

1. Normalize the title.
2. Search title in metadata sources:
   - Crossref;
   - OpenAlex;
   - Semantic Scholar as an optional fallback;
   - arXiv if the reference looks like a preprint;
   - PubMed for biomedical references.
3. If no title match is found, report `TITLE_NOT_FOUND`.
4. If exactly one strong title match is found, compare all supplied fields.
5. If multiple plausible title matches are found, report
   `AMBIGUOUS_TITLE_MATCH` and list candidates.
6. If the matched source provides a DOI absent from the input, report it as
   additional metadata, not a mismatch.

### Case 3: DOI and Title Missing, Journal Locator Provided

1. Search by journal name or ISSN.
2. Filter by year, volume, issue, and page/article number.
3. If no record is found, report `JOURNAL_LOCATOR_NOT_FOUND`.
4. If a record is found, compare supplied title, authors, DOI, year, volume,
   issue, and pages.
5. If multiple records share the same location, report ambiguity.

## Field Comparison Rules

Compare only fields that are supplied in the input reference.

Fields to compare:

```text
DOI
title
authors
year
journal / venue
volume
issue
page range
article number
publisher
arXiv ID
PMID
ISBN
URL
```

Do not report missing input fields as mismatches. For example, if the input
reference has no issue number but the registry does, that is additional
metadata, not an error.

## Author Handling

Author lists require special treatment because references often abbreviate them.

### Author Input Examples

```text
Smith, J.; Wang, L.; et al.
Smith et al.
J. Smith
Smith J.
John Smith
Smith, J. A.
```

### Author Normalization Schema

Each parsed author should be normalized into:

```text
raw_name
family_name
given_names
given_initials
suffix
orcid
position_in_list
is_et_al_marker
```

### Author Comparison Rules

- Only check author names explicitly provided in the reference.
- If the reference uses `et al.`, do not require all remaining authors.
- If only the first author is supplied, only check the first author.
- Normalize capitalization, punctuation, accents, and spacing.
- Treat initials as compatible with full names.

Examples:

```text
Input: Smith, J.
Found: Smith, John
Result: no mismatch

Input: Smith, J. A.
Found: Smith, John Adam
Result: no mismatch

Input: Smith, J.
Found: Wang, John
Result: supplied author mismatch

Input: Smith et al.
Found: Smith, John; Wang, Li; Brown, Amy
Result: no mismatch

Input: Smith; Wang; et al.
Found: Smith, John; Wang, Li; Brown, Amy
Result: no mismatch
```

## Result Labels

Use factual labels, not scores.

Suggested labels:

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

## Full Evidence Report

The full report includes every reference.

Each entry should contain:

```text
reference number
raw input reference
parsed fields
identifier candidates found
identifier used for lookup
lookup source
lookup result
returned metadata
field-by-field comparison
mismatches
additional metadata found
final factual status
```

Example:

```md
## Reference 12

### Input Identifier Used

DOI: `10.xxxx/yyyy`

### Lookup Result

Found in Crossref.

### Returned Metadata

- Title: `...`
- Authors: `...`
- Journal: `...`
- Year: `2020`
- Volume: `15`
- Issue: `2`
- Pages: `100-112`
- DOI: `10.xxxx/yyyy`

### Mismatches

- Title:
  - Input: `...`
  - Found: `...`

- Year:
  - Input: `2021`
  - Found: `2020`

### Status

`DOI_RESOLVES_TO_DIFFERENT_WORK`
```

## Short Exception Report

The short report includes only problematic references.

Include references with:

```text
not found
ambiguous match
identifier conflict
DOI/title/journal locator mismatch
author mismatch
year mismatch
volume mismatch
issue mismatch
page mismatch
unsupported type
lookup error
insufficient metadata
```

Exclude clean references.

Example:

```md
# Short Exception Report

## Reference 7

Status: `DOI_RESOLVES_TO_DIFFERENT_WORK`

Identifier used: DOI `10.xxxx/yyyy`

Mismatches:

- Title:
  - Input: `...`
  - Found: `...`

- Year:
  - Input: `2021`
  - Found: `2020`
```

## Suggested Python Architecture

```text
src/citeverify/
  __init__.py
  cli.py
  models.py
  parsers/
    bibtex.py
    raw_text.py
    latex.py
    pdf.py
  normalize/
    doi.py
    title.py
    author.py
    journal.py
  lookup/
    crossref.py
    datacite.py
    openalex.py
    arxiv.py
    pubmed.py
  compare/
    fields.py
    authors.py
    references.py
  reports/
    markdown.py
    json.py
  cache.py
```

## Recommended Dependencies

Use `uv` for environment and dependency management.

Suggested packages:

```text
httpx
pydantic
typer
rich
rapidfuzz
tenacity
bibtexparser
lxml
python-slugify
```

Optional later:

```text
grobid-client-python
pymupdf
beautifulsoup4
```

## CLI Design

Example commands:

```bash
citeverify verify references.bib
citeverify verify article.pdf
citeverify verify refs.txt
```

Example output options:

```bash
citeverify verify references.bib \
  --full-report full_report.md \
  --short-report short_report.md \
  --json report.json
```

## MVP Implementation Order

1. Parse BibTeX and raw reference text.
2. Normalize DOI, title, journal, author, year, volume, issue, and pages.
3. Implement DOI lookup with Crossref and DataCite.
4. Compare DOI-returned metadata against supplied fields.
5. Implement title lookup.
6. Implement journal locator lookup.
7. Implement author normalization and partial author-list comparison.
8. Generate full Markdown report.
9. Generate short exception Markdown report.
10. Add JSON output.
11. Add caching, retries, and rate-limit handling.
12. Add PDF/LaTeX extraction later.

## Important Behavior Rules

- Do not produce confidence scores.
- Do not mark a reference fake just because it is not found.
- Report the exact source queried.
- Report exact returned metadata.
- Report every mismatch field by field.
- Only compare fields supplied by the reference.
- Treat `et al.` as an instruction to check only supplied authors.
- Treat initials and full names as compatible when family names match.
- Keep clean references out of the short exception report.
- Preserve enough evidence that a human can audit every decision.
