from citeverify.parsers.bibtex import parse_bibtex


def test_bibtex_parser_extracts_arxiv_id_from_journal_field() -> None:
    references = parse_bibtex(
        """
@article{huang2026low,
  title={Low-depth amplitude estimation via statistical eigengap estimation},
  author={Huang, Po-Wei and Koczor, B{\\'a}lint},
  journal={arXiv preprint arXiv:2603.05475},
  year={2026}
}
"""
    )
    assert references[0].arxiv_id == "2603.05475"


def test_bibtex_parser_does_not_treat_arxiv_abs_as_volume() -> None:
    references = parse_bibtex(
        """
@article{Benedetti2019ParameterizedQC,
  title={Parameterized quantum circuits as machine learning models},
  author={Marcello Benedetti and Erika Lloyd and Stefan H. Sack},
  journal={ArXiv},
  volume={abs/1906.07682},
  year={2019}
}
"""
    )
    assert references[0].volume is None
    assert references[0].arxiv_id is None


def test_bibtex_parser_extracts_doi_from_url() -> None:
    references = parse_bibtex(
        """
@article{schuld2014quest,
  title={The quest for a quantum neural network},
  author={Schuld, Maria and Sinayskiy, Ilya and Petruccione, Francesco},
  journal={Quantum Information Processing},
  year={2014},
  url={https://link.springer.com/article/10.1007/s11128-014-0809-8}
}
"""
    )
    assert references[0].doi == "10.1007/s11128-014-0809-8"
