from __future__ import annotations

import re
from difflib import SequenceMatcher

from citeverify.normalize.text import collapse_whitespace, normalize_basic_text


def normalize_title(value: str | None) -> str | None:
    if not value:
        return None
    value = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r"\1", value)
    value = re.sub(r"[{}$]", "", value)
    value = normalize_basic_text(value)
    value = re.sub(r"\s*:\s*", " ", value)
    value = value.strip(" .,:;")
    return collapse_whitespace(value) or None


def titles_match(input_title: str | None, found_title: str | None) -> bool:
    normalized_input = normalize_title(input_title)
    normalized_found = normalize_title(found_title)
    if not normalized_input or not normalized_found:
        return False
    if normalized_input == normalized_found:
        return True
    return SequenceMatcher(None, normalized_input, normalized_found).ratio() >= 0.96
