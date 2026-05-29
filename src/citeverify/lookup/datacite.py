from __future__ import annotations

from typing import Any
from urllib.parse import quote

from citeverify.lookup.base import HttpLookupProvider, LookupResponse
from citeverify.models import JournalLocator, ParsedAuthor, RegistryRecord
from citeverify.normalize.arxiv import arxiv_doi, extract_arxiv_id
from citeverify.normalize.author import parse_author
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import canonical_journal_name
from citeverify.normalize.title import normalize_title


class DataCiteProvider(HttpLookupProvider):
    name = "DataCite"
    api_base = "https://api.datacite.org"

    async def get_by_doi(self, doi: str) -> LookupResponse:
        normalized = normalize_doi(doi) or doi
        body, status_code, error = await self._get_json(
            query_kind="doi",
            normalized_query_value=normalized,
            url=f"{self.api_base}/dois/{quote(normalized, safe='')}",
        )
        records = []
        if (
            body
            and status_code != 404
            and not error
            and isinstance(body.get("data"), dict)
        ):
            records.append(self._record_from_item(body["data"]))
        return LookupResponse(
            source=self.name,
            query_kind="doi",
            query_value=normalized,
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    async def get_by_arxiv_id(self, arxiv_id: str) -> LookupResponse:
        doi = arxiv_doi(arxiv_id)
        if not doi:
            return LookupResponse(
                source=self.name,
                query_kind="arxiv_id",
                query_value=arxiv_id,
                error="invalid arXiv ID",
            )
        response = await self.get_by_doi(doi)
        return response.model_copy(
            update={"query_kind": "arxiv_id", "query_value": arxiv_id}
        )

    async def search_by_title(self, title: str) -> LookupResponse:
        normalized = normalize_title(title) or title
        body, status_code, error = await self._get_json(
            query_kind="title",
            normalized_query_value=normalized,
            url=f"{self.api_base}/dois",
            params={"query": title, "page[size]": 5},
        )
        data = body.get("data", []) if body and not error else []
        records = [
            self._record_from_item(item) for item in data if isinstance(item, dict)
        ]
        return LookupResponse(
            source=self.name,
            query_kind="title",
            query_value=title,
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse:
        venue = canonical_journal_name(locator.venue) or locator.venue
        query_terms = " ".join(
            str(value)
            for value in [
                venue,
                locator.year,
                locator.volume,
                locator.issue,
                locator.pages,
                locator.article_number,
            ]
            if value
        )
        body, status_code, error = await self._get_json(
            query_kind="journal_locator",
            normalized_query_value=locator.model_dump_json(),
            url=f"{self.api_base}/dois",
            params={"query": query_terms, "page[size]": 10},
        )
        data = body.get("data", []) if body and not error else []
        records = [
            self._record_from_item(item) for item in data if isinstance(item, dict)
        ]
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=query_terms,
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    def _record_from_item(self, item: dict[str, Any]) -> RegistryRecord:
        attributes = item.get("attributes", {})
        doi = normalize_doi(attributes.get("doi") or item.get("id"))
        creators = attributes.get("creators") or []
        titles = attributes.get("titles") or []
        return RegistryRecord(
            source=self.name,
            source_record_url=(
                f"https://doi.org/{doi}" if doi else attributes.get("url")
            ),
            title=_title_from_datacite(titles),
            authors=[
                _author_from_datacite(creator, index)
                for index, creator in enumerate(creators)
                if isinstance(creator, dict)
            ],
            year=attributes.get("publicationYear"),
            venue=attributes.get("publisher"),
            doi=doi,
            arxiv_id=extract_arxiv_id(doi, attributes.get("url")),
            url=attributes.get("url"),
            record_type=(attributes.get("types") or {}).get("resourceTypeGeneral"),
            raw_response=item,
        )


def _title_from_datacite(titles: list[dict[str, Any]]) -> str | None:
    if not titles:
        return None
    first = titles[0]
    return first.get("title") if isinstance(first, dict) else None


def _author_from_datacite(creator: dict[str, Any], index: int) -> ParsedAuthor:
    family = creator.get("familyName")
    given = creator.get("givenName")
    name = creator.get("name")
    if family and given:
        parsed = parse_author(f"{family}, {given}", index)
    elif name:
        parsed = parse_author(str(name), index)
    else:
        parsed = ParsedAuthor(raw_name="", position_in_list=index)
    identifiers = creator.get("nameIdentifiers") or []
    orcid = None
    for identifier in identifiers:
        if isinstance(identifier, dict) and "orcid" in str(identifier).lower():
            orcid = identifier.get("nameIdentifier")
            break
    return parsed.model_copy(update={"orcid": orcid})
