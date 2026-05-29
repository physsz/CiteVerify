from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

from citeverify.config import CiteVerifyConfig
from citeverify.lookup.base import HttpLookupProvider, LookupResponse
from citeverify.models import JournalLocator, RegistryRecord
from citeverify.normalize.arxiv import extract_arxiv_id, normalize_arxiv_id
from citeverify.normalize.author import parse_author
from citeverify.normalize.doi import normalize_doi


class ArxivProvider(HttpLookupProvider):
    name = "arXiv"
    api_base = "https://export.arxiv.org/api/query"

    def __init__(self, config: CiteVerifyConfig, **kwargs: Any) -> None:
        super().__init__(config, **kwargs)

    async def get_by_doi(self, doi: str) -> LookupResponse:
        arxiv_id = extract_arxiv_id(doi)
        if not arxiv_id:
            return LookupResponse(source=self.name, query_kind="doi", query_value=doi)
        response = await self.get_by_arxiv_id(arxiv_id)
        return response.model_copy(update={"query_kind": "doi", "query_value": doi})

    async def get_by_arxiv_id(self, arxiv_id: str) -> LookupResponse:
        normalized = normalize_arxiv_id(arxiv_id) or arxiv_id
        text, status_code, error = await self._get_text(
            query_kind="arxiv_id",
            normalized_query_value=normalized,
            url=self.api_base,
            params={"id_list": normalized},
        )
        records = _records_from_feed(text, self.name) if text and not error else []
        return LookupResponse(
            source=self.name,
            query_kind="arxiv_id",
            query_value=normalized,
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    async def search_by_title(self, title: str) -> LookupResponse:
        # arXiv title search is rate-limit sensitive and noisy for broad
        # bibliography verification. arXiv is queried directly when an arXiv ID
        # is parsed from the reference.
        return LookupResponse(
            source=self.name,
            query_kind="title",
            query_value=title,
        )

    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse:
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=locator.model_dump_json(),
        )


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_NS = {"arxiv": "http://arxiv.org/schemas/atom"}


def _records_from_feed(text: str, source: str) -> list[RegistryRecord]:
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    records: list[RegistryRecord] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        record = _record_from_entry(entry, source)
        if record:
            records.append(record)
    return records


def _record_from_entry(entry: ET.Element, source: str) -> RegistryRecord | None:
    entry_id = _text(entry, "atom:id")
    arxiv_id = extract_arxiv_id(entry_id)
    if not arxiv_id:
        return None
    title = _clean_text(_text(entry, "atom:title"))
    published = _text(entry, "atom:published")
    year = int(published[:4]) if published and published[:4].isdigit() else None
    authors = []
    for index, author in enumerate(entry.findall("atom:author", ATOM_NS)):
        name = _text(author, "atom:name")
        if name:
            authors.append(parse_author(name, index))
    doi = normalize_doi(_text(entry, "arxiv:doi", ARXIV_NS))
    journal_ref = _text(entry, "arxiv:journal_ref", ARXIV_NS)
    return RegistryRecord(
        source=source,
        source_record_url=entry_id,
        title=title,
        authors=authors,
        year=year,
        venue=journal_ref or "arXiv",
        doi=doi or f"10.48550/arxiv.{arxiv_id}",
        arxiv_id=arxiv_id,
        url=entry_id,
        record_type="preprint",
        raw_response={
            "id": entry_id,
            "title": title,
            "published": published,
            "journal_ref": journal_ref,
        },
    )


def _text(
    element: ET.Element,
    path: str,
    namespace: dict[str, str] | None = None,
) -> str | None:
    found = element.find(path, namespace or ATOM_NS)
    if found is None or found.text is None:
        return None
    return found.text.strip()


def _clean_text(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(value.split())
