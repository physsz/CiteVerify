from __future__ import annotations

from pathlib import Path

from citeverify.errors import UnsupportedInputError
from citeverify.models import ParsedReference


def parse_pdf(_path: Path) -> list[ParsedReference]:
    raise UnsupportedInputError("PDF reference extraction is not implemented yet.")
