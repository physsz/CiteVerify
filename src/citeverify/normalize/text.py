from __future__ import annotations

import re
import unicodedata

LATEX_ACCENT_PATTERN = re.compile(
    r"\{?\\[\"'`^~=.uvHtcdb]\s*\\?([A-Za-z])\}?"
)


def normalize_latex_accents(value: str) -> str:
    return LATEX_ACCENT_PATTERN.sub(r"\1", value)


def strip_accents(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_unicode(value: str) -> str:
    return unicodedata.normalize("NFKC", value)


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_basic_text(value: str) -> str:
    value = normalize_latex_accents(value)
    value = strip_accents(normalize_unicode(value))
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[{}]", "", value)
    value = re.sub(r"[\u2010-\u2015]", "-", value)
    value = re.sub(r"[^\w\s/-]", " ", value)
    return collapse_whitespace(value)
