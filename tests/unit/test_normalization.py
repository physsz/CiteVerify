from citeverify.normalize.arxiv import arxiv_doi, extract_arxiv_id, normalize_arxiv_id
from citeverify.normalize.author import parse_author_list
from citeverify.normalize.doi import extract_doi, normalize_doi
from citeverify.normalize.journal import venues_compatible
from citeverify.normalize.text import normalize_basic_text
from citeverify.normalize.title import normalize_title, titles_match


def test_normalize_doi_from_url() -> None:
    assert (
        normalize_doi("https://doi.org/10.1103/PhysRevLett.121.090502.")
        == "10.1103/physrevlett.121.090502"
    )


def test_extract_doi() -> None:
    assert extract_doi("See doi:10.1000/XYZ for details.") == "10.1000/xyz"


def test_normalize_title_removes_latex_and_case() -> None:
    assert normalize_title(r"{Observation} of \textit{Direct} Effects") == (
        "observation of direct effects"
    )


def test_near_title_match() -> None:
    assert titles_match(
        "Observation of directly interacting coherent two-level systems",
        "Observation of directly interacting coherent two level systems",
    )


def test_author_parser_et_al() -> None:
    authors = parse_author_list("Smith, J.; Wang, L.; et al.")
    assert [author.raw_name for author in authors] == [
        "Smith, J.",
        "Wang, L.",
        "et al.",
    ]
    assert authors[-1].is_et_al_marker


def test_latex_accent_normalization() -> None:
    assert normalize_basic_text(r'Braum{\"u}ller') == "braumuller"


def test_arxiv_id_extraction_and_doi() -> None:
    assert extract_arxiv_id("arXiv preprint arXiv:2603.05475") == "2603.05475"
    assert normalize_arxiv_id("https://arxiv.org/pdf/2603.05475v2.pdf") == "2603.05475"
    assert arxiv_doi("2603.05475") == "10.48550/arxiv.2603.05475"


def test_venue_matches_when_found_venue_embeds_volume() -> None:
    assert venues_compatible(
        "Advances in Neural Information Processing Systems",
        "Advances in Neural Information Processing Systems 35",
        input_volume="35",
    )
