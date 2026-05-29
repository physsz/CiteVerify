# CiteVerify Full Evidence Report

## Summary

- Total references: `9`
- Clean references: `1`
- Exception references: `8`

## Reference correctBenedetti2019ParameterizedQC

Status: `FOUND_NO_SUPPLIED_FIELD_MISMATCH`

### Raw Input

```text
{'doi': '10.1088/2058-9565/ab4eb5', 'pages': '043001', 'number': '4', 'volume': '4', 'year': '2019', 'journal': 'Quantum Science and Technology', 'title': 'Parameterized quantum circuits as machine learning models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'correctBenedetti2019ParameterizedQC'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1088/2058-9565/ab4eb5`
- Normalized: `10.1088/2058-9565/ab4eb5`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

None.

### Field Comparisons

- `doi`: `match` (input: `10.1088/2058-9565/ab4eb5`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `match` (input: `Parameterized quantum circuits as machine learning models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `match` (input: `Quantum Science and Technology`, found: `Quantum Science and Technology`)
- `volume`: `match` (input: `4`, found: `4`)
- `issue`: `match` (input: `4`, found: `4`)
- `pages`: `match` (input: `043001`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongDoi

Status: `TITLE_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-parameterized-qc', 'pages': '043001', 'number': '4', 'volume': '4', 'year': '2019', 'journal': 'Quantum Science and Technology', 'title': 'Parameterized quantum circuits as machine learning models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongDoi'}
```

### Identifier Used

- Kind: `title`
- Value: `Parameterized quantum circuits as machine learning models`
- Normalized: `parameterized quantum circuits as machine learning models`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `12`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-parameterized-qc`
  - Found: `10.1088/2058-9565/ab4eb5`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-parameterized-qc`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `match` (input: `Parameterized quantum circuits as machine learning models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `match` (input: `Quantum Science and Technology`, found: `Quantum Science and Technology`)
- `volume`: `match` (input: `4`, found: `4`)
- `issue`: `match` (input: `4`, found: `4`)
- `pages`: `match` (input: `043001`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongTitle

Status: `DOI_RESOLVES_TO_DIFFERENT_WORK`

### Raw Input

```text
{'doi': '10.1088/2058-9565/ab4eb5', 'pages': '043001', 'number': '4', 'volume': '4', 'year': '2019', 'journal': 'Quantum Science and Technology', 'title': 'Fabricated quantum circuits as cooking models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongTitle'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1088/2058-9565/ab4eb5`
- Normalized: `10.1088/2058-9565/ab4eb5`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- title:
  - Input: `Fabricated quantum circuits as cooking models`
  - Found: `Parameterized quantum circuits as machine learning models`

### Field Comparisons

- `doi`: `match` (input: `10.1088/2058-9565/ab4eb5`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `mismatch` (input: `Fabricated quantum circuits as cooking models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `match` (input: `Quantum Science and Technology`, found: `Quantum Science and Technology`)
- `volume`: `match` (input: `4`, found: `4`)
- `issue`: `match` (input: `4`, found: `4`)
- `pages`: `match` (input: `043001`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongJournalInfo

Status: `IDENTIFIER_CONFLICT`

### Raw Input

```text
{'doi': '10.1088/2058-9565/ab4eb5', 'pages': '900--999', 'number': '7', 'volume': '99', 'year': '2019', 'journal': 'Journal of Made-Up Quantum Widgets', 'title': 'Parameterized quantum circuits as machine learning models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongJournalInfo'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1088/2058-9565/ab4eb5`
- Normalized: `10.1088/2058-9565/ab4eb5`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- venue:
  - Input: `Journal of Made-Up Quantum Widgets`
  - Found: `Quantum Science and Technology`
- volume:
  - Input: `99`
  - Found: `4`
- issue:
  - Input: `7`
  - Found: `4`
- pages:
  - Input: `900-999`
  - Found: `043001`

### Field Comparisons

- `doi`: `match` (input: `10.1088/2058-9565/ab4eb5`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `match` (input: `Parameterized quantum circuits as machine learning models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `mismatch` (input: `Journal of Made-Up Quantum Widgets`, found: `Quantum Science and Technology`)
- `volume`: `mismatch` (input: `99`, found: `4`)
- `issue`: `mismatch` (input: `7`, found: `4`)
- `pages`: `mismatch` (input: `900-999`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongDoiWrongTitle

Status: `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-parameterized-qc', 'pages': '043001', 'number': '4', 'volume': '4', 'year': '2019', 'journal': 'Quantum Science and Technology', 'title': 'Fabricated quantum circuits as cooking models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongDoiWrongTitle'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Quantum Science and Technology","issn":[],"year":2019,"volume":"4","issue":"4","pages":"043001","article_number":null}`
- Normalized: `{"venue":"Quantum Science and Technology","issn":[],"year":2019,"volume":"4","issue":"4","pages":"043001","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `102`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-parameterized-qc`
  - Found: `10.1088/2058-9565/ab4eb5`
- title:
  - Input: `Fabricated quantum circuits as cooking models`
  - Found: `Parameterized quantum circuits as machine learning models`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-parameterized-qc`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `mismatch` (input: `Fabricated quantum circuits as cooking models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `match` (input: `Quantum Science and Technology`, found: `Quantum Science and Technology`)
- `volume`: `match` (input: `4`, found: `4`)
- `issue`: `match` (input: `4`, found: `4`)
- `pages`: `match` (input: `043001`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongDoiWrongJournal

Status: `TITLE_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-parameterized-qc', 'pages': '900--999', 'number': '7', 'volume': '99', 'year': '2019', 'journal': 'Journal of Made-Up Quantum Widgets', 'title': 'Parameterized quantum circuits as machine learning models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongDoiWrongJournal'}
```

### Identifier Used

- Kind: `title`
- Value: `Parameterized quantum circuits as machine learning models`
- Normalized: `parameterized quantum circuits as machine learning models`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `12`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-parameterized-qc`
  - Found: `10.1088/2058-9565/ab4eb5`
- venue:
  - Input: `Journal of Made-Up Quantum Widgets`
  - Found: `Quantum Science and Technology`
- volume:
  - Input: `99`
  - Found: `4`
- issue:
  - Input: `7`
  - Found: `4`
- pages:
  - Input: `900-999`
  - Found: `043001`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-parameterized-qc`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `match` (input: `Parameterized quantum circuits as machine learning models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `mismatch` (input: `Journal of Made-Up Quantum Widgets`, found: `Quantum Science and Technology`)
- `volume`: `mismatch` (input: `99`, found: `4`)
- `issue`: `mismatch` (input: `7`, found: `4`)
- `pages`: `mismatch` (input: `900-999`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeWrongTitleWrongJournal

Status: `DOI_RESOLVES_TO_DIFFERENT_WORK`

### Raw Input

```text
{'doi': '10.1088/2058-9565/ab4eb5', 'pages': '900--999', 'number': '7', 'volume': '99', 'year': '2019', 'journal': 'Journal of Made-Up Quantum Widgets', 'title': 'Fabricated quantum circuits as cooking models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeWrongTitleWrongJournal'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1088/2058-9565/ab4eb5`
- Normalized: `10.1088/2058-9565/ab4eb5`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- title:
  - Input: `Fabricated quantum circuits as cooking models`
  - Found: `Parameterized quantum circuits as machine learning models`
- venue:
  - Input: `Journal of Made-Up Quantum Widgets`
  - Found: `Quantum Science and Technology`
- volume:
  - Input: `99`
  - Found: `4`
- issue:
  - Input: `7`
  - Found: `4`
- pages:
  - Input: `900-999`
  - Found: `043001`

### Field Comparisons

- `doi`: `match` (input: `10.1088/2058-9565/ab4eb5`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `mismatch` (input: `Fabricated quantum circuits as cooking models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `match` (input: `['Marcello Benedetti', 'Erika Lloyd', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `mismatch` (input: `Journal of Made-Up Quantum Widgets`, found: `Quantum Science and Technology`)
- `volume`: `mismatch` (input: `99`, found: `4`)
- `issue`: `mismatch` (input: `7`, found: `4`)
- `pages`: `mismatch` (input: `900-999`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeAllWrongDoiTitleJournal

Status: `DOI_NOT_FOUND`

### Raw Input

```text
{'doi': '10.9999/fake-parameterized-qc', 'pages': '900--999', 'number': '7', 'volume': '99', 'year': '2019', 'journal': 'Journal of Made-Up Quantum Widgets', 'title': 'Fabricated quantum circuits as cooking models', 'author': 'Marcello Benedetti and Erika Lloyd and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakeAllWrongDoiTitleJournal'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.9999/fake-parameterized-qc`
- Normalized: `10.9999/fake-parameterized-qc`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `0`

### Mismatches

None.

## Reference fakePartiallyWrongAuthors

Status: `IDENTIFIER_CONFLICT`

### Raw Input

```text
{'doi': '10.1088/2058-9565/ab4eb5', 'pages': '043001', 'number': '4', 'volume': '4', 'year': '2019', 'journal': 'Quantum Science and Technology', 'title': 'Parameterized quantum circuits as machine learning models', 'author': 'Marcello Benedetti and Mallory Fake and Stefan H. Sack and Mattia Fiorentini', 'ENTRYTYPE': 'article', 'ID': 'fakePartiallyWrongAuthors'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1088/2058-9565/ab4eb5`
- Normalized: `10.1088/2058-9565/ab4eb5`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Title: `Parameterized quantum circuits as machine learning models`
- Authors: `Benedetti, Marcello; Lloyd, Erika; Sack, Stefan; Fiorentini, Mattia`
- Venue: `Quantum Science and Technology`
- Year: `2019`
- Volume: `4`
- Issue: `4`
- Pages: `043001`
- DOI: `10.1088/2058-9565/ab4eb5`
- URL: `https://doi.org/10.1088/2058-9565/ab4eb5`
- Type: `journal-article`

### Mismatches

- authors:
  - Input: `['Marcello Benedetti', 'Mallory Fake', 'Stefan H. Sack', 'Mattia Fiorentini']`
  - Found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`
  - Note: Mallory Fake: no compatible author found

### Field Comparisons

- `doi`: `match` (input: `10.1088/2058-9565/ab4eb5`, found: `10.1088/2058-9565/ab4eb5`)
- `title`: `match` (input: `Parameterized quantum circuits as machine learning models`, found: `Parameterized quantum circuits as machine learning models`)
- `authors`: `mismatch` (input: `['Marcello Benedetti', 'Mallory Fake', 'Stefan H. Sack', 'Mattia Fiorentini']`, found: `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`)
  - Note: Mallory Fake: no compatible author found
- `year`: `match` (input: `2019`, found: `2019`)
- `venue`: `match` (input: `Quantum Science and Technology`, found: `Quantum Science and Technology`)
- `volume`: `match` (input: `4`, found: `4`)
- `issue`: `match` (input: `4`, found: `4`)
- `pages`: `match` (input: `043001`, found: `043001`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)
