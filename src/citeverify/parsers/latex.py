from __future__ import annotations

from citeverify.errors import UnsupportedInputError
from citeverify.models import ParsedReference


def parse_latex(_text: str) -> list[ParsedReference]:
    raise UnsupportedInputError("LaTeX bibliography extraction is not implemented yet.")
