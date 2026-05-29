from __future__ import annotations

import re

from citeverify.models import ParsedAuthor
from citeverify.normalize.text import collapse_whitespace, normalize_basic_text

ET_AL_PATTERN = re.compile(
    r"\b(?:et\.?\s*al\.?|and\s+others|others)\.?", re.IGNORECASE
)
SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}


def normalize_name_token(value: str | None) -> str | None:
    if not value:
        return None
    normalized = normalize_basic_text(value)
    normalized = normalized.replace("-", " ")
    return collapse_whitespace(normalized) or None


def extract_initials(tokens: list[str]) -> list[str]:
    initials: list[str] = []
    for token in tokens:
        cleaned = re.sub(r"[^A-Za-z]", "", token)
        if not cleaned:
            continue
        if len(cleaned) == 1 or token.endswith("."):
            initials.extend(ch.upper() for ch in cleaned)
        else:
            initials.append(cleaned[0].upper())
    return initials


def parse_author(raw_name: str, position: int | None = None) -> ParsedAuthor:
    raw_name = collapse_whitespace(raw_name.strip())
    if not raw_name or _is_et_al_text(raw_name):
        return ParsedAuthor(
            raw_name=raw_name or "et al.",
            position_in_list=position,
            is_et_al_marker=True,
        )

    if ET_AL_PATTERN.search(raw_name):
        author_part = ET_AL_PATTERN.sub("", raw_name).strip(" ,;.")
        if not author_part:
            return ParsedAuthor(
                raw_name=raw_name,
                position_in_list=position,
                is_et_al_marker=True,
            )
        raw_name = author_part

    suffix = None
    if "," in raw_name:
        parts = [
            collapse_whitespace(part)
            for part in raw_name.split(",")
            if part.strip()
        ]
        family_name = parts[0]
        given_text = " ".join(parts[1:])
    else:
        tokens = raw_name.split()
        if tokens and tokens[-1].lower() in SUFFIXES:
            suffix = tokens.pop()
        if len(tokens) == 1:
            family_name = tokens[0]
            given_text = ""
        else:
            family_name = tokens[-1]
            given_text = " ".join(tokens[:-1])

    given_tokens = [token for token in re.split(r"[\s.-]+", given_text) if token]
    return ParsedAuthor(
        raw_name=raw_name,
        family_name=family_name or None,
        given_names=given_tokens,
        given_initials=extract_initials(given_tokens),
        suffix=suffix,
        position_in_list=position,
        is_et_al_marker=False,
    )


def split_author_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if " and " in value:
        parts = re.split(r"\s+\band\b\s+", value)
    elif ";" in value:
        parts = value.split(";")
    else:
        comma_parts = [part.strip() for part in value.split(",")]
        if len(comma_parts) > 2 and len(comma_parts) % 2 == 0:
            parts = [
                f"{comma_parts[i]}, {comma_parts[i + 1]}"
                for i in range(0, len(comma_parts), 2)
            ]
        else:
            parts = [value]
    cleaned = [
        collapse_whitespace(part.strip(" ,"))
        for part in parts
        if part.strip(" ,")
    ]
    output: list[str] = []
    for part in cleaned:
        if ET_AL_PATTERN.search(part):
            before = ET_AL_PATTERN.sub("", part).strip(" ,;.")
            if before:
                output.append(before)
            output.append("et al.")
        else:
            output.append(part)
    return output


def parse_author_list(value: str | None) -> list[ParsedAuthor]:
    if not value:
        return []
    parts = split_author_list(value)
    return [parse_author(part, idx) for idx, part in enumerate(parts)]


def _is_et_al_text(value: str) -> bool:
    normalized = normalize_basic_text(value).replace(".", "")
    return normalized in {"et al", "etal", "others", "and others"}


def author_names_compatible(
    input_author: ParsedAuthor, found_author: ParsedAuthor
) -> bool:
    if input_author.is_et_al_marker:
        return True
    input_family = normalize_name_token(input_author.family_name)
    found_family = normalize_name_token(found_author.family_name)
    if not input_family or not found_family or input_family != found_family:
        return False
    input_initials = input_author.given_initials
    found_initials = found_author.given_initials
    if not input_initials or not found_initials:
        return True
    if len(input_initials) > len(found_initials):
        return False
    return input_initials == found_initials[: len(input_initials)]
