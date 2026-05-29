# Getting Started With CiteVerify

This guide shows how to set up CiteVerify, run the CLI, and inspect the reports.

CiteVerify does not assign confidence scores. It reports what identifier was
used, whether a bibliographic record was found, and which supplied fields
mismatch the returned metadata.

## Requirements

- Python 3.11 or newer
- `uv`
- Network access for live Crossref, DataCite, and OpenAlex lookups

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Install The Project

From the repository root:

```bash
uv sync --dev
```

Confirm the CLI is available:

```bash
uv run citeverify --help
uv run citeverify verify --help
```

Run the test suite:

```bash
uv run pytest
```

## Quick Start: Verify A BibTeX File

Create a small BibTeX file:

```bibtex
@article{einstein1905,
  author = {Einstein, Albert},
  title = {On the Electrodynamics of Moving Bodies},
  journal = {Annalen der Physik},
  year = {1905},
  volume = {17},
  pages = {891--921},
  doi = {10.1002/andp.19053221004}
}
```

Save it as `example_refs.bib`, then run:

```bash
uv run citeverify verify example_refs.bib
```

By default, this writes:

```text
reports/full_report.md
reports/short_report.md
reports/report.json
```

CiteVerify creates the `reports/` directory if it does not already exist.

## Quick Start: Choose Output Paths

```bash
uv run citeverify verify example_refs.bib \
  --full-report reports/full_report.md \
  --short-report reports/short_report.md \
  --json-report reports/report.json
```

If the parent directory for a chosen report path does not exist, CiteVerify
creates it before writing the report artifact.

The full report includes every reference. The short report includes only
references with lookup failures, ambiguous matches, or supplied-field
mismatches.

## Provided Examples

The repository includes example inputs and generated reports for both synthetic
edge cases and real arXiv reference lists. These are useful as manual regression
checks when changing matching behavior.

| Example | Input | What It Demonstrates | Reports |
|---|---|---|---|
| Partially fake BibTeX | `examples/partially-fake-bib/partially_fake_references.bib` | One clean control reference plus targeted wrong DOI, wrong title, wrong journal metadata, combined mismatch, and partial-author-list cases. | `examples/partially-fake-bib/reports/` |
| More fake BibTeX | `examples/more-fake-bib/more_fake_references.bib` | A broader manual fixture with APS article numbers, DOI/title fallback, PDF-style references without DOI or title, journal-locator lookup, and abbreviated journals such as `Phys. Rev. Lett.` and `Nat. Comput. Sci.`. | `examples/more-fake-bib/reports/` |
| arXiv 2605.06178v1 | `examples/arXiv-2605.06178v1/mybib.bib` | A real paper reference list used to inspect author normalization, arXiv-vs-journal venue differences, and ambiguous provider matches. | `examples/arXiv-2605.06178v1/reports/` |
| arXiv 2605.30301v1 | `examples/arXiv-2605.30301v1/references.bib` | A larger real paper reference list used to inspect default field checks and short-report readability. | `examples/arXiv-2605.30301v1/reports/` |

Rerun an example and write artifacts back into its own report directory:

```bash
uv run citeverify verify examples/more-fake-bib/more_fake_references.bib \
  --cache examples/more-fake-bib/reports/citeverify-cache.sqlite \
  --full-report examples/more-fake-bib/reports/full_report.md \
  --short-report examples/more-fake-bib/reports/short_report.md \
  --json-report examples/more-fake-bib/reports/report.json
```

The short report is the fastest file to inspect by hand. It contains one table
row per exception reference with the reference label, status, identifier used,
clickable article link, and mismatch details.

## Quick Start: Raw Text References

Raw text mode accepts one reference per numbered item or paragraph.

Example `refs.txt`:

```text
[1] Einstein, A. "On the Electrodynamics of Moving Bodies." Annalen der Physik,
1905. doi:10.1002/andp.19053221004.

[2] Smith, J.; Wang, L.; et al. "A Made Up Citation Title." Journal of Imaginary
Results, 2024.
```

Run:

```bash
uv run citeverify verify refs.txt --format raw-text
```

The parser currently extracts DOI, quoted title, year, and a best-effort author
prefix from raw text. BibTeX is more reliable for structured metadata.

## Quick Start: Use The Cache

CiteVerify caches provider responses in SQLite so repeated runs do not repeat
the same network requests.

Use the default cache:

```bash
uv run citeverify verify example_refs.bib
```

Choose a cache path:

```bash
uv run citeverify verify example_refs.bib --cache .citeverify-cache.sqlite
```

Disable the cache:

```bash
uv run citeverify verify example_refs.bib --no-cache
```

Use only cached responses:

```bash
uv run citeverify verify example_refs.bib --offline
```

Offline mode is useful for reproducing previous results, but references without
cached lookup responses will be reported as lookup errors.

## Quick Start: CI-Friendly Failure Mode

By default, CiteVerify reports mismatches but exits successfully if the command
itself ran correctly.

For CI, use:

```bash
uv run citeverify verify example_refs.bib --fail-on-exceptions
```

Exit codes:

```text
0: command completed; no exceptions found
1: command completed; exceptions found and --fail-on-exceptions was set
2: input parsing failed or format is unsupported
```

## What CiteVerify Checks

CiteVerify chooses the best available identifier in this order:

```text
DOI
title
journal locator
```

The journal locator is built from fields such as:

```text
journal or ISSN
year
volume
issue
page range or article number
```

For each selected record, CiteVerify compares only fields supplied by the input
reference. Missing input fields are not treated as mismatches.

## Journal Abbreviations

CiteVerify normalizes a curated set of journal abbreviations before comparing
venues, querying journal locators, and inferring APS DOIs. The bundled seed list
uses the same semicolon-separated shape as JabRef abbreviation lists:

```text
full journal title;default abbreviation;shortest/common abbreviation
```

Examples currently covered include:

```text
Phys. Rev. Lett. -> Physical Review Letters
Rev. Mod. Phys. -> Reviews of Modern Physics
Nat. Comput. Sci. -> Nature Computational Science
npj Quantum Inf. -> npj Quantum Information
J. Phys. B -> Journal of Physics B: Atomic, Molecular and Optical Physics
Proc. Natl. Acad. Sci. U.S.A. -> Proceedings of the National Academy of Sciences
```

ISSN remains stronger evidence than a text abbreviation when it is supplied.

## Author Matching

Author comparison is intentionally partial.

If the input says:

```text
Smith, J.; Wang, L.; et al.
```

CiteVerify checks only `Smith, J.` and `Wang, L.`. It does not require the input
to list every registry author.

Initials and full names are compatible when the family name matches:

```text
Input: Smith, J.
Found: Smith, John
Result: match
```

Clear supplied-name conflicts are reported:

```text
Input: Smith, J.
Found: Wang, John
Result: mismatch
```

## Report Interpretation

Common statuses:

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
LOOKUP_ERROR
```

Important interpretation rules:

- `NOT_FOUND` does not prove a reference is fabricated.
- A DOI/title mismatch means the supplied identifier points to a different
  record than the supplied metadata describes.
- Registry-only metadata is reported as additional metadata, not as an error.
- The short report intentionally omits clean references.

## Current Limitations

- PDF, LaTeX, and `.bbl` extraction are planned but not implemented yet.
- Raw text parsing is best effort.
- arXiv and PubMed provider modules are placeholders for later implementation.
- Journal abbreviation handling uses a curated bundled seed list, not a complete
  external abbreviation authority.

## Developer Commands

Run all local checks:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Inspect the CLI:

```bash
uv run citeverify --help
uv run citeverify verify --help
```
