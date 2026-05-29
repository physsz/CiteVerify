# CiteVerify Full Evidence Report

## Summary

- Total references: `12`
- Clean references: `4`
- Exception references: `8`

## Reference correctBerry2015TaylorSeries

Status: `FOUND_NO_SUPPLIED_FIELD_MISMATCH`

### Raw Input

```text
{'doi': '10.1103/PhysRevLett.114.090502', 'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Truncated Taylor Series', 'ENTRYTYPE': 'article', 'ID': 'correctBerry2015TaylorSeries'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1103/physrevlett.114.090502`
- Normalized: `10.1103/physrevlett.114.090502`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

None.

### Field Comparisons

- `doi`: `match` (input: `10.1103/physrevlett.114.090502`, found: `10.1103/physrevlett.114.090502`)
- `title`: `match` (input: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeBerryWrongDoiOnly

Status: `TITLE_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-berry-taylor-series', 'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Truncated Taylor Series', 'ENTRYTYPE': 'article', 'ID': 'fakeBerryWrongDoiOnly'}
```

### Identifier Used

- Kind: `title`
- Value: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Normalized: `simulating hamiltonian dynamics with a truncated taylor series`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `12`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-berry-taylor-series`
  - Found: `10.1103/physrevlett.114.090502`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-berry-taylor-series`, found: `10.1103/physrevlett.114.090502`)
- `title`: `match` (input: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeBerryWrongTitleOnly

Status: `DOI_RESOLVES_TO_DIFFERENT_WORK`

### Raw Input

```text
{'doi': '10.1103/PhysRevLett.114.090502', 'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe', 'ENTRYTYPE': 'article', 'ID': 'fakeBerryWrongTitleOnly'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1103/physrevlett.114.090502`
- Normalized: `10.1103/physrevlett.114.090502`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

- title:
  - Input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`
  - Found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`

### Field Comparisons

- `doi`: `match` (input: `10.1103/physrevlett.114.090502`, found: `10.1103/physrevlett.114.090502`)
- `title`: `mismatch` (input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeBerryWrongJournalInfo

Status: `IDENTIFIER_CONFLICT`

### Raw Input

```text
{'doi': '10.1103/PhysRevLett.114.090502', 'pages': '1--2', 'number': '42', 'volume': '999', 'journal': 'Journal of Imaginary Hamiltonian Methods', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Truncated Taylor Series', 'ENTRYTYPE': 'article', 'ID': 'fakeBerryWrongJournalInfo'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1103/physrevlett.114.090502`
- Normalized: `10.1103/physrevlett.114.090502`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

- venue:
  - Input: `Journal of Imaginary Hamiltonian Methods`
  - Found: `Physical Review Letters`
- volume:
  - Input: `999`
  - Found: `114`
- issue:
  - Input: `42`
  - Found: `9`
- pages:
  - Input: `1-2`
  - Found: `090502`

### Field Comparisons

- `doi`: `match` (input: `10.1103/physrevlett.114.090502`, found: `10.1103/physrevlett.114.090502`)
- `title`: `match` (input: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `mismatch` (input: `Journal of Imaginary Hamiltonian Methods`, found: `Physical Review Letters`)
- `volume`: `mismatch` (input: `999`, found: `114`)
- `issue`: `mismatch` (input: `42`, found: `9`)
- `pages`: `mismatch` (input: `1-2`, found: `090502`)
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeBerryWrongDoiWrongTitleJournalCorrect

Status: `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-berry-taylor-series', 'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe', 'ENTRYTYPE': 'article', 'ID': 'fakeBerryWrongDoiWrongTitleJournalCorrect'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`
- Normalized: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-berry-taylor-series`
  - Found: `10.1103/physrevlett.114.090502`
- title:
  - Input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`
  - Found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-berry-taylor-series`, found: `10.1103/physrevlett.114.090502`)
- `title`: `mismatch` (input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference pdfStyleBerryJournalLocatorOnly

Status: `FOUND_NO_SUPPLIED_FIELD_MISMATCH`

### Raw Input

```text
{'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'ENTRYTYPE': 'article', 'ID': 'pdfStyleBerryJournalLocatorOnly'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`
- Normalized: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

None.

### Field Comparisons

- `doi`: `additional_metadata` (input: `None`, found: `10.1103/physrevlett.114.090502`)
- `title`: `additional_metadata` (input: `None`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference pdfStyleBerryWrongTitleJournalLocator

Status: `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'pages': '090502', 'number': '9', 'volume': '114', 'journal': 'Physical Review Letters', 'year': '2015', 'author': 'Berry, Dominic W. and Childs, Andrew M. and Cleve, Richard and Kothari, Robin and Somma, Rolando D.', 'title': 'Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe', 'ENTRYTYPE': 'article', 'ID': 'pdfStyleBerryWrongTitleJournalLocator'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`
- Normalized: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Title: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`
- Authors: `Berry, Dominic W.; Childs, Andrew M.; Cleve, Richard; Kothari, Robin; Somma, Rolando D.`
- Venue: `Physical Review Letters`
- Year: `2015`
- Volume: `114`
- Issue: `9`
- Article number: `090502`
- DOI: `10.1103/physrevlett.114.090502`
- URL: `https://doi.org/10.1103/physrevlett.114.090502`
- Type: `journal-article`

### Mismatches

- title:
  - Input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`
  - Found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`

### Field Comparisons

- `doi`: `additional_metadata` (input: `None`, found: `10.1103/physrevlett.114.090502`)
- `title`: `mismatch` (input: `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`, found: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series`)
- `authors`: `match` (input: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`, found: `['Berry, Dominic W.', 'Childs, Andrew M.', 'Cleve, Richard', 'Kothari, Robin', 'Somma, Rolando D.']`)
- `year`: `match` (input: `2015`, found: `2015`)
- `venue`: `match` (input: `Physical Review Letters`, found: `Physical Review Letters`)
- `volume`: `match` (input: `114`, found: `114`)
- `issue`: `match` (input: `9`, found: `9`)
- `pages`: `match` (input: `090502`, found: `090502`)
  - Note: input pages matched found article number
- `article_number`: `additional_metadata` (input: `None`, found: `090502`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference correctAbbas2021PowerQNN

Status: `FOUND_NO_SUPPLIED_FIELD_MISMATCH`

### Raw Input

```text
{'doi': '10.1038/s43588-021-00084-1', 'pages': '403--409', 'number': '6', 'volume': '1', 'journal': 'Nature Computational Science', 'year': '2021', 'author': 'Abbas, Amira and Sutter, David and Zoufal, Christa and Lucchi, Aurelien and Figalli, Alessio and Woerner, Stefan', 'title': 'The power of quantum neural networks', 'ENTRYTYPE': 'article', 'ID': 'correctAbbas2021PowerQNN'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1038/s43588-021-00084-1`
- Normalized: `10.1038/s43588-021-00084-1`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Title: `The power of quantum neural networks`
- Authors: `Abbas, Amira; Sutter, David; Zoufal, Christa; Lucchi, Aurelien; Figalli, Alessio; Woerner, Stefan`
- Venue: `Nature Computational Science`
- Year: `2021`
- Volume: `1`
- Issue: `6`
- Pages: `403-409`
- DOI: `10.1038/s43588-021-00084-1`
- URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Type: `journal-article`

### Mismatches

None.

### Field Comparisons

- `doi`: `match` (input: `10.1038/s43588-021-00084-1`, found: `10.1038/s43588-021-00084-1`)
- `title`: `match` (input: `The power of quantum neural networks`, found: `The power of quantum neural networks`)
- `authors`: `match` (input: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`, found: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`)
- `year`: `match` (input: `2021`, found: `2021`)
- `venue`: `match` (input: `Nature Computational Science`, found: `Nature Computational Science`)
- `volume`: `match` (input: `1`, found: `1`)
- `issue`: `match` (input: `6`, found: `6`)
- `pages`: `match` (input: `403-409`, found: `403-409`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeAbbasWrongDoiWrongTitleJournalCorrect

Status: `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'doi': '10.9999/fake-abbas-qnn', 'pages': '403--409', 'number': '6', 'volume': '1', 'journal': 'Nature Computational Science', 'year': '2021', 'author': 'Abbas, Amira and Sutter, David and Zoufal, Christa and Lucchi, Aurelien and Figalli, Alessio and Woerner, Stefan', 'title': 'The power of fabricated neural recipes', 'ENTRYTYPE': 'article', 'ID': 'fakeAbbasWrongDoiWrongTitleJournalCorrect'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`
- Normalized: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `106`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Title: `The power of quantum neural networks`
- Authors: `Abbas, Amira; Sutter, David; Zoufal, Christa; Lucchi, Aurelien; Figalli, Alessio; Woerner, Stefan`
- Venue: `Nature Computational Science`
- Year: `2021`
- Volume: `1`
- Issue: `6`
- Pages: `403-409`
- DOI: `10.1038/s43588-021-00084-1`
- URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Type: `journal-article`

### Mismatches

- doi:
  - Input: `10.9999/fake-abbas-qnn`
  - Found: `10.1038/s43588-021-00084-1`
- title:
  - Input: `The power of fabricated neural recipes`
  - Found: `The power of quantum neural networks`

### Field Comparisons

- `doi`: `mismatch` (input: `10.9999/fake-abbas-qnn`, found: `10.1038/s43588-021-00084-1`)
- `title`: `mismatch` (input: `The power of fabricated neural recipes`, found: `The power of quantum neural networks`)
- `authors`: `match` (input: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`, found: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`)
- `year`: `match` (input: `2021`, found: `2021`)
- `venue`: `match` (input: `Nature Computational Science`, found: `Nature Computational Science`)
- `volume`: `match` (input: `1`, found: `1`)
- `issue`: `match` (input: `6`, found: `6`)
- `pages`: `match` (input: `403-409`, found: `403-409`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference pdfStyleAbbasJournalLocatorOnly

Status: `FOUND_NO_SUPPLIED_FIELD_MISMATCH`

### Raw Input

```text
{'pages': '403--409', 'number': '6', 'volume': '1', 'journal': 'Nature Computational Science', 'year': '2021', 'author': 'Abbas, Amira and Sutter, David and Zoufal, Christa and Lucchi, Aurelien and Figalli, Alessio and Woerner, Stefan', 'ENTRYTYPE': 'article', 'ID': 'pdfStyleAbbasJournalLocatorOnly'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`
- Normalized: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `106`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Title: `The power of quantum neural networks`
- Authors: `Abbas, Amira; Sutter, David; Zoufal, Christa; Lucchi, Aurelien; Figalli, Alessio; Woerner, Stefan`
- Venue: `Nature Computational Science`
- Year: `2021`
- Volume: `1`
- Issue: `6`
- Pages: `403-409`
- DOI: `10.1038/s43588-021-00084-1`
- URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Type: `journal-article`

### Mismatches

None.

### Field Comparisons

- `doi`: `additional_metadata` (input: `None`, found: `10.1038/s43588-021-00084-1`)
- `title`: `additional_metadata` (input: `None`, found: `The power of quantum neural networks`)
- `authors`: `match` (input: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`, found: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`)
- `year`: `match` (input: `2021`, found: `2021`)
- `venue`: `match` (input: `Nature Computational Science`, found: `Nature Computational Science`)
- `volume`: `match` (input: `1`, found: `1`)
- `issue`: `match` (input: `6`, found: `6`)
- `pages`: `match` (input: `403-409`, found: `403-409`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference pdfStyleAbbasWrongTitleJournalLocator

Status: `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES`

### Raw Input

```text
{'pages': '403--409', 'number': '6', 'volume': '1', 'journal': 'Nature Computational Science', 'year': '2021', 'author': 'Abbas, Amira and Sutter, David and Zoufal, Christa and Lucchi, Aurelien and Figalli, Alessio and Woerner, Stefan', 'title': 'The power of fabricated neural recipes', 'ENTRYTYPE': 'article', 'ID': 'pdfStyleAbbasWrongTitleJournalLocator'}
```

### Identifier Used

- Kind: `journal_locator`
- Value: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`
- Normalized: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `106`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Title: `The power of quantum neural networks`
- Authors: `Abbas, Amira; Sutter, David; Zoufal, Christa; Lucchi, Aurelien; Figalli, Alessio; Woerner, Stefan`
- Venue: `Nature Computational Science`
- Year: `2021`
- Volume: `1`
- Issue: `6`
- Pages: `403-409`
- DOI: `10.1038/s43588-021-00084-1`
- URL: `https://doi.org/10.1038/s43588-021-00084-1`
- Type: `journal-article`

### Mismatches

- title:
  - Input: `The power of fabricated neural recipes`
  - Found: `The power of quantum neural networks`

### Field Comparisons

- `doi`: `additional_metadata` (input: `None`, found: `10.1038/s43588-021-00084-1`)
- `title`: `mismatch` (input: `The power of fabricated neural recipes`, found: `The power of quantum neural networks`)
- `authors`: `match` (input: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`, found: `['Abbas, Amira', 'Sutter, David', 'Zoufal, Christa', 'Lucchi, Aurelien', 'Figalli, Alessio', 'Woerner, Stefan']`)
- `year`: `match` (input: `2021`, found: `2021`)
- `venue`: `match` (input: `Nature Computational Science`, found: `Nature Computational Science`)
- `volume`: `match` (input: `1`, found: `1`)
- `issue`: `match` (input: `6`, found: `6`)
- `pages`: `match` (input: `403-409`, found: `403-409`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)

## Reference fakeAnshuPartiallyWrongAuthors

Status: `IDENTIFIER_CONFLICT`

### Raw Input

```text
{'doi': '10.1038/s42254-023-00662-4', 'pages': '59--69', 'number': '1', 'volume': '6', 'journal': 'Nature Reviews Physics', 'year': '2023', 'author': 'Anshu, Anurag and Mallory, Fake', 'title': 'A Survey on the Complexity of Learning Quantum States', 'ENTRYTYPE': 'article', 'ID': 'fakeAnshuPartiallyWrongAuthors'}
```

### Identifier Used

- Kind: `doi`
- Value: `10.1038/s42254-023-00662-4`
- Normalized: `10.1038/s42254-023-00662-4`

### Lookup

- Sources queried: `Crossref`, `DataCite`, `arXiv`, `OpenAlex`
- Records returned: `2`

### Selected Record

- Source: `Crossref`
- Source URL: `https://doi.org/10.1038/s42254-023-00662-4`
- Title: `A survey on the complexity of learning quantum states`
- Authors: `Anshu, Anurag; Arunachalam, Srinivasan`
- Venue: `Nature Reviews Physics`
- Year: `2023`
- Volume: `6`
- Issue: `1`
- Pages: `59-69`
- DOI: `10.1038/s42254-023-00662-4`
- URL: `https://doi.org/10.1038/s42254-023-00662-4`
- Type: `journal-article`

### Mismatches

- authors:
  - Input: `['Anshu, Anurag', 'Mallory, Fake']`
  - Found: `['Anshu, Anurag', 'Arunachalam, Srinivasan']`
  - Note: Mallory, Fake: no compatible author found

### Field Comparisons

- `doi`: `match` (input: `10.1038/s42254-023-00662-4`, found: `10.1038/s42254-023-00662-4`)
- `title`: `match` (input: `A Survey on the Complexity of Learning Quantum States`, found: `A survey on the complexity of learning quantum states`)
- `authors`: `mismatch` (input: `['Anshu, Anurag', 'Mallory, Fake']`, found: `['Anshu, Anurag', 'Arunachalam, Srinivasan']`)
  - Note: Mallory, Fake: no compatible author found
- `year`: `match` (input: `2023`, found: `2023`)
- `venue`: `match` (input: `Nature Reviews Physics`, found: `Nature Reviews Physics`)
- `volume`: `match` (input: `6`, found: `6`)
- `issue`: `match` (input: `1`, found: `1`)
- `pages`: `match` (input: `59-69`, found: `59-69`)
- `article_number`: `not_checked` (input: `None`, found: `None`)
- `arxiv_id`: `not_checked` (input: `None`, found: `None`)
- `pmid`: `not_checked` (input: `None`, found: `None`)
- `isbn`: `not_checked` (input: `None`, found: `None`)
