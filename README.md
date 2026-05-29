<div align="center">

# CiteVerify

Evidence-based reference verification for scholarly citations.

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square)
![uv](https://img.shields.io/badge/package%20manager-uv-6340AC?style=flat-square)
![Reports](https://img.shields.io/badge/reports-Markdown%20%2B%20JSON-0F766E?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-111827?style=flat-square)

</div>

CiteVerify is a Python CLI for checking whether article references correspond
to real bibliographic records and whether the supplied metadata matches what
external registries return.

The project does **not** output confidence scores. It reports evidence: which
identifier was used, what record was found, and exactly which supplied fields
do not match.

## Why This Exists

LLM-generated references can look plausible while containing fake DOI values,
fabricated titles, wrong journal metadata, or subtly altered author lists.
CiteVerify is designed to make those problems inspectable:

| Problem | CiteVerify Behavior |
|---|---|
| Wrong DOI, correct title | Falls back to title and reports the DOI mismatch. |
| Correct DOI, wrong title | Resolves the DOI and reports the title mismatch. |
| No DOI or title | Uses journal locator metadata when enough venue, year, volume, issue, and page/article-number information is available. |
| Partial author list with `et al.` | Checks only the names supplied by the reference. |
| Journal abbreviations | Normalizes a curated seed list such as `Phys. Rev. Lett.` and `Nat. Comput. Sci.`. |

## Quick Start

Install dependencies:

```bash
uv sync --dev
```

Verify a BibTeX file:

```bash
uv run citeverify verify references.bib
```

By default, CiteVerify writes:

```text
reports/full_report.md
reports/short_report.md
reports/report.json
```

The report directory is created automatically if it does not already exist.

## What The Reports Show

The short report contains only references that need attention:

| Reference | Status | Identifier Used | Article Link | Mismatch Details |
|---|---|---|---|---|
| `fakeWrongDoi` | `TITLE_FOUND_WITH_FIELD_MISMATCHES` | `title` | DOI link | input DOI differs from found DOI |
| `fakeWrongTitle` | `DOI_RESOLVES_TO_DIFFERENT_WORK` | `doi` | DOI link | input title differs from found title |
| `fakeWrongJournalInfo` | `IDENTIFIER_CONFLICT` | `doi` | DOI link | venue, volume, issue, or pages differ |

The full report includes every reference, including clean entries and returned
provider metadata. The JSON report is intended for automation and downstream
inspection.

## Verification Flow

```text
Parse references
  -> try DOI
  -> if DOI is missing, not found, or conflicts, try title
  -> if title is missing, not found, or conflicts, try journal locator
  -> compare supplied fields only
  -> write full, short, and JSON reports
```

Lookup providers currently include Crossref, DataCite, and OpenAlex. The arXiv
and PubMed modules are present as extension points for later provider-specific
work.

## Examples

| Example | Purpose | Reports |
|---|---|---|
| [`examples/partially-fake-bib/`](examples/partially-fake-bib/) | Small fixture with one correct reference and targeted fake DOI, title, journal, combined, and author-list cases. | [`reports/`](examples/partially-fake-bib/reports/) |
| [`examples/more-fake-bib/`](examples/more-fake-bib/) | Broader fixture covering APS article numbers, PDF-style missing DOI/title references, journal-locator lookup, and journal abbreviations. | [`reports/`](examples/more-fake-bib/reports/) |
| [`examples/arXiv-2605.06178v1/`](examples/arXiv-2605.06178v1/) | Real arXiv reference list used for manual inspection of author and venue matching. | [`reports/`](examples/arXiv-2605.06178v1/reports/) |
| [`examples/arXiv-2605.30301v1/`](examples/arXiv-2605.30301v1/) | Larger real arXiv reference list used to inspect default field checks and short-report readability. | [`reports/`](examples/arXiv-2605.30301v1/reports/) |

Rerun the broader synthetic example:

```bash
uv run citeverify verify examples/more-fake-bib/more_fake_references.bib \
  --cache examples/more-fake-bib/reports/citeverify-cache.sqlite \
  --full-report examples/more-fake-bib/reports/full_report.md \
  --short-report examples/more-fake-bib/reports/short_report.md \
  --json-report examples/more-fake-bib/reports/report.json
```

## Supported Inputs

| Input | Status |
|---|---|
| BibTeX `.bib` | Supported and preferred. |
| Raw text `.txt` or `.refs` | Best-effort DOI, title, year, and author extraction. |
| LaTeX `.tex` / `.bbl` | Planned. |
| PDF | Planned. |

## Development

Run local checks:

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

## Design Notes

- CiteVerify reports mismatches honestly rather than compressing evidence into
  a score.
- Missing input fields are not treated as mismatches.
- Registry-only metadata is shown as additional evidence, not as an error.
- Ambiguous journal-locator results are reported as `AMBIGUOUS_MATCH` instead
  of forcing an unstable choice.
- ISSN is treated as stronger venue evidence than abbreviated journal text.

For the original verification design, see
[`reference_verification_plan.md`](reference_verification_plan.md). For the
implementation plan, see
[`technical_implementation_plan.md`](technical_implementation_plan.md). For
step-by-step usage, see
[`docs/getting_started.md`](docs/getting_started.md).
