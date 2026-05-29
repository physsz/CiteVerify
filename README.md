# CiteVerify

CiteVerify is a planned Python tool for checking whether references in an
article correspond to real bibliographic records and whether the supplied
metadata matches authoritative sources.

The project principle is simple: report evidence, not confidence scores. For
each reference, CiteVerify should state which identifier was used, whether a
record was found, what metadata was returned, and which supplied fields
mismatched.

See [reference_verification_plan.md](reference_verification_plan.md) for the
current verification design and
[technical_implementation_plan.md](technical_implementation_plan.md) for the
implementation plan.

For setup and usage examples, see
[docs/getting_started.md](docs/getting_started.md).

## Current Implementation

The repository now contains the initial Python package and CLI scaffold. The
first implementation slice supports:

- BibTeX and raw text inputs;
- DOI, title, and journal-locator identifier candidates;
- Crossref, DataCite, and OpenAlex lookup clients;
- field-by-field comparison without confidence scores;
- partial author-list comparison with `et al.` and initials handling;
- full Markdown, short exception Markdown, and JSON reports.

## Development

Create the environment and run tests with `uv`:

```bash
uv sync --dev
uv run pytest
```

Run the CLI locally:

```bash
uv run citeverify verify references.bib
```

Example with explicit outputs:

```bash
uv run citeverify verify references.bib \
  --full-report full_report.md \
  --short-report short_report.md \
  --json-report report.json
```
