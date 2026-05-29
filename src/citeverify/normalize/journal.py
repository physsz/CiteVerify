from __future__ import annotations

import csv
import re
from functools import lru_cache
from importlib.resources import files
from io import StringIO

from citeverify.normalize.text import normalize_basic_text

BASE_JOURNAL_ALIASES = {
    "prl": "physical review letters",
    "phys rev lett": "physical review letters",
    "physical review letters": "physical review letters",
    "phys rev a": "physical review a",
    "physical review a": "physical review a",
    "phys rev b": "physical review b",
    "physical review b": "physical review b",
    "nature": "nature",
    "science": "science",
    "pnas": "proceedings of the national academy of sciences",
    "proc natl acad sci usa": "proceedings of the national academy of sciences",
}
ABBREVIATION_RESOURCE = "journal_abbreviations.csv"


def normalize_issn(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().upper()
    value = re.sub(r"[^0-9X]", "", value)
    if len(value) == 8:
        return f"{value[:4]}-{value[4:]}"
    return value or None


def normalize_journal(value: str | None) -> str | None:
    canonical = canonical_journal_name(value)
    if canonical:
        return _journal_key(canonical)
    return None


def canonical_journal_name(value: str | None) -> str | None:
    if not value:
        return None
    normalized = _journal_key(value)
    if not normalized:
        return None
    return _journal_aliases().get(normalized, normalized)


def venues_compatible(
    input_venue: str | None,
    found_venue: str | None,
    input_volume: str | None = None,
    found_volume: str | None = None,
) -> bool:
    normalized_input = normalize_journal(input_venue)
    normalized_found = normalize_journal(found_venue)
    if not normalized_input or not normalized_found:
        return False
    if normalized_input == normalized_found:
        return True
    for volume in _volume_variants(input_volume) | _volume_variants(found_volume):
        if _strip_trailing_volume(normalized_input, volume) == normalized_found:
            return True
        if _strip_trailing_volume(normalized_found, volume) == normalized_input:
            return True
    return False


def _volume_variants(value: str | None) -> set[str]:
    if not value:
        return set()
    normalized = normalize_basic_text(str(value)).replace(".", "").strip()
    if not normalized:
        return set()
    variants = {normalized}
    if normalized.startswith("vol "):
        variants.add(normalized.removeprefix("vol ").strip())
    else:
        variants.add(f"vol {normalized}")
    return {variant for variant in variants if variant}


def _strip_trailing_volume(value: str, volume: str) -> str:
    return re.sub(rf"\s+{re.escape(volume)}$", "", value).strip()


@lru_cache(maxsize=1)
def _journal_aliases() -> dict[str, str]:
    aliases = dict(BASE_JOURNAL_ALIASES)
    try:
        text = (
            files("citeverify.data")
            .joinpath(ABBREVIATION_RESOURCE)
            .read_text(encoding="utf-8")
        )
    except (FileNotFoundError, ModuleNotFoundError):
        return aliases
    for row in csv.reader(StringIO(text), delimiter=";"):
        if not row or not row[0].strip() or row[0].lstrip().startswith("#"):
            continue
        full_title = row[0].strip()
        full_key = _journal_key(full_title)
        if not full_key:
            continue
        aliases[full_key] = full_key
        for alias in row[1:]:
            alias_key = _journal_key(alias)
            if alias_key:
                aliases[alias_key] = full_key
    return aliases


def _journal_key(value: str | None) -> str | None:
    if not value:
        return None
    normalized = normalize_basic_text(value)
    normalized = normalized.replace(".", "")
    normalized = re.sub(r"\bu s a\b", "usa", normalized)
    normalized = re.sub(r"\bu k\b", "uk", normalized)
    normalized = re.sub(r"\bjournal\b", "journal", normalized)
    normalized = normalized.strip()
    return normalized or None
