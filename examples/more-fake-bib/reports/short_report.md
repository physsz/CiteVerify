# CiteVerify Short Exception Report

## Summary

- Total references: `12`
- Clean references: `4`
- Exception references: `8`

## Exception References

| Reference | Status | Identifier Used | Article Link | Mismatch Details |
|---|---|---|---|---|
| `fakeBerryWrongDoiOnly` | `TITLE_FOUND_WITH_FIELD_MISMATCHES` | `title`: `Simulating Hamiltonian Dynamics with a Truncated Taylor Series` | [10.1103/physrevlett.114.090502](https://doi.org/10.1103/physrevlett.114.090502) | `doi`: input `10.9999/fake-berry-taylor-series`; found `10.1103/physrevlett.114.090502` |
| `fakeBerryWrongTitleOnly` | `DOI_RESOLVES_TO_DIFFERENT_WORK` | `doi`: `10.1103/physrevlett.114.090502` | [10.1103/physrevlett.114.090502](https://doi.org/10.1103/physrevlett.114.090502) | `title`: input `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`; found `Simulating Hamiltonian Dynamics with a Truncated Taylor Series` |
| `fakeBerryWrongJournalInfo` | `IDENTIFIER_CONFLICT` | `doi`: `10.1103/physrevlett.114.090502` | [10.1103/physrevlett.114.090502](https://doi.org/10.1103/physrevlett.114.090502) | `venue`: input `Journal of Imaginary Hamiltonian Methods`; found `Physical Review Letters`<br>`volume`: input `999`; found `114`<br>`issue`: input `42`; found `9`<br>`pages`: input `1-2`; found `090502` |
| `fakeBerryWrongDoiWrongTitleJournalCorrect` | `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES` | `journal_locator`: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}` | [10.1103/physrevlett.114.090502](https://doi.org/10.1103/physrevlett.114.090502) | `doi`: input `10.9999/fake-berry-taylor-series`; found `10.1103/physrevlett.114.090502`<br>`title`: input `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`; found `Simulating Hamiltonian Dynamics with a Truncated Taylor Series` |
| `pdfStyleBerryWrongTitleJournalLocator` | `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES` | `journal_locator`: `{"venue":"Physical Review Letters","issn":[],"year":2015,"volume":"114","issue":"9","pages":"090502","article_number":null}` | [10.1103/physrevlett.114.090502](https://doi.org/10.1103/physrevlett.114.090502) | `title`: input `Simulating Hamiltonian Dynamics with a Fabricated Polynomial Recipe`; found `Simulating Hamiltonian Dynamics with a Truncated Taylor Series` |
| `fakeAbbasWrongDoiWrongTitleJournalCorrect` | `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES` | `journal_locator`: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}` | [10.1038/s43588-021-00084-1](https://doi.org/10.1038/s43588-021-00084-1) | `doi`: input `10.9999/fake-abbas-qnn`; found `10.1038/s43588-021-00084-1`<br>`title`: input `The power of fabricated neural recipes`; found `The power of quantum neural networks` |
| `pdfStyleAbbasWrongTitleJournalLocator` | `JOURNAL_LOCATOR_FOUND_WITH_FIELD_MISMATCHES` | `journal_locator`: `{"venue":"Nature Computational Science","issn":[],"year":2021,"volume":"1","issue":"6","pages":"403-409","article_number":null}` | [10.1038/s43588-021-00084-1](https://doi.org/10.1038/s43588-021-00084-1) | `title`: input `The power of fabricated neural recipes`; found `The power of quantum neural networks` |
| `fakeAnshuPartiallyWrongAuthors` | `IDENTIFIER_CONFLICT` | `doi`: `10.1038/s42254-023-00662-4` | [10.1038/s42254-023-00662-4](https://doi.org/10.1038/s42254-023-00662-4) | `authors`: input `['Anshu, Anurag', 'Mallory, Fake']`; found `['Anshu, Anurag', 'Arunachalam, Srinivasan']`; note: Mallory, Fake: no compatible author found |
