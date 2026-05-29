# CiteVerify Short Exception Report

## Summary

- Total references: `9`
- Clean references: `1`
- Exception references: `8`

## Exception References

| Reference | Status | Identifier Used | Article Link | Mismatch Details |
|---|---|---|---|---|
| `fakeWrongDoi` | `TITLE_FOUND_WITH_FIELD_MISMATCHES` | `title`: `Parameterized quantum circuits as machine learning models` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `doi`: input `10.9999/fake-parameterized-qc`; found `10.1088/2058-9565/ab4eb5` |
| `fakeWrongTitle` | `DOI_RESOLVES_TO_DIFFERENT_WORK` | `doi`: `10.1088/2058-9565/ab4eb5` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `title`: input `Fabricated quantum circuits as cooking models`; found `Parameterized quantum circuits as machine learning models` |
| `fakeWrongJournalInfo` | `IDENTIFIER_CONFLICT` | `doi`: `10.1088/2058-9565/ab4eb5` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `venue`: input `Journal of Made-Up Quantum Widgets`; found `Quantum Science and Technology`<br>`volume`: input `99`; found `4`<br>`issue`: input `7`; found `4`<br>`pages`: input `900-999`; found `043001` |
| `fakeWrongDoiWrongTitle` | `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES` | `journal_locator`: `{"venue":"Quantum Science and Technology","issn":[],"year":2019,"volume":"4","issue":"4","pages":"043001","article_number":null}` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `doi`: input `10.9999/fake-parameterized-qc`; found `10.1088/2058-9565/ab4eb5`<br>`title`: input `Fabricated quantum circuits as cooking models`; found `Parameterized quantum circuits as machine learning models` |
| `fakeWrongDoiWrongJournal` | `TITLE_FOUND_WITH_FIELD_MISMATCHES` | `title`: `Parameterized quantum circuits as machine learning models` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `doi`: input `10.9999/fake-parameterized-qc`; found `10.1088/2058-9565/ab4eb5`<br>`venue`: input `Journal of Made-Up Quantum Widgets`; found `Quantum Science and Technology`<br>`volume`: input `99`; found `4`<br>`issue`: input `7`; found `4`<br>`pages`: input `900-999`; found `043001` |
| `fakeWrongTitleWrongJournal` | `DOI_RESOLVES_TO_DIFFERENT_WORK` | `doi`: `10.1088/2058-9565/ab4eb5` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `title`: input `Fabricated quantum circuits as cooking models`; found `Parameterized quantum circuits as machine learning models`<br>`venue`: input `Journal of Made-Up Quantum Widgets`; found `Quantum Science and Technology`<br>`volume`: input `99`; found `4`<br>`issue`: input `7`; found `4`<br>`pages`: input `900-999`; found `043001` |
| `fakeAllWrongDoiTitleJournal` | `DOI_NOT_FOUND` | `doi`: `10.9999/fake-parameterized-qc` | None | identifier not found or insufficient metadata |
| `fakePartiallyWrongAuthors` | `IDENTIFIER_CONFLICT` | `doi`: `10.1088/2058-9565/ab4eb5` | [10.1088/2058-9565/ab4eb5](https://doi.org/10.1088/2058-9565/ab4eb5) | `authors`: input `['Marcello Benedetti', 'Mallory Fake', 'Stefan H. Sack', 'Mattia Fiorentini']`; found `['Benedetti, Marcello', 'Lloyd, Erika', 'Sack, Stefan', 'Fiorentini, Mattia']`; note: Mallory Fake: no compatible author found |
