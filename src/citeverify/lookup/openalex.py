from __future__ import annotations

from typing import Any
from urllib.parse import quote

from citeverify.lookup.base import HttpLookupProvider, LookupResponse
from citeverify.models import JournalLocator, RegistryRecord
from citeverify.normalize.arxiv import arxiv_doi, extract_arxiv_id
from citeverify.normalize.author import parse_author
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import normalize_issn
from citeverify.normalize.pages import normalize_pages
from citeverify.normalize.title import normalize_title


class OpenAlexProvider(HttpLookupProvider):
    name = "OpenAlex"
    api_base = "https://api.openalex.org"

    async def get_by_doi(self, doi: str) -> LookupResponse:
        normalized = normalize_doi(doi) or doi
        doi_url = f"https://doi.org/{normalized}"
        body, status_code, error = await self._get_json(
            query_kind="doi",
            normalized_query_value=normalized,
            url=f"{self.api_base}/works/{quote(doi_url, safe='')}",
        )
        records = [self._record_from_work(body)] if body and not error else []
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
        records = response.records
        if not records:
            records = await self._search_arxiv_location(arxiv_id)
        return LookupResponse(
            source=self.name,
            query_kind="arxiv_id",
            query_value=arxiv_id,
            records=records,
            error=response.error,
            raw_status_code=response.raw_status_code,
        )

    async def search_by_title(self, title: str) -> LookupResponse:
        normalized = normalize_title(title) or title
        body, status_code, error = await self._get_json(
            query_kind="title",
            normalized_query_value=normalized,
            url=f"{self.api_base}/works",
            params={"search.title": title, "per-page": 5},
        )
        results = body.get("results", []) if body and not error else []
        records = [
            self._record_from_work(item) for item in results if isinstance(item, dict)
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
        filters: list[str] = []
        if locator.year:
            filters.append(f"publication_year:{locator.year}")
        if locator.issn:
            filters.append(f"primary_location.source.issn:{locator.issn[0]}")
        params: dict[str, Any] = {
            "per-page": 50,
            "search": _journal_locator_search(locator),
        }
        if filters:
            params["filter"] = ",".join(filters)
        body, status_code, error = await self._get_json(
            query_kind="journal_locator",
            normalized_query_value=_journal_locator_cache_key(locator),
            url=f"{self.api_base}/works",
            params=params,
        )
        results = body.get("results", []) if body and not error else []
        records = [
            self._record_from_work(item) for item in results if isinstance(item, dict)
        ]
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=locator.model_dump_json(),
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    def _record_from_work(self, item: dict[str, Any]) -> RegistryRecord:
        source = (item.get("primary_location") or {}).get("source") or {}
        primary_location = item.get("primary_location") or {}
        biblio = item.get("biblio") or {}
        doi = normalize_doi(item.get("doi"))
        arxiv_id = extract_arxiv_id(
            doi,
            primary_location.get("id"),
            primary_location.get("landing_page_url"),
            primary_location.get("pdf_url"),
        )
        return RegistryRecord(
            source=self.name,
            source_record_url=item.get("id"),
            title=item.get("title") or item.get("display_name"),
            authors=[
                parse_author(
                    author.get("author", {}).get("display_name", ""),
                    index,
                )
                for index, author in enumerate(item.get("authorships", []) or [])
                if isinstance(author, dict)
            ],
            year=item.get("publication_year"),
            venue=_venue_from_work(item),
            issn=[
                normalized
                for normalized in (
                    normalize_issn(value) for value in source.get("issn", []) or []
                )
                if normalized
            ],
            volume=biblio.get("volume"),
            issue=biblio.get("issue"),
            pages=_pages_from_biblio(biblio),
            doi=doi,
            arxiv_id=arxiv_id,
            url=item.get("doi") or item.get("id"),
            record_type=item.get("type"),
            raw_response=item,
        )

    async def _search_arxiv_location(self, arxiv_id: str) -> list[RegistryRecord]:
        body, _status_code, error = await self._get_json(
            query_kind="arxiv_id_location",
            normalized_query_value=arxiv_id,
            url=f"{self.api_base}/works",
            params={
                "filter": "locations.source.id:S4393918464",
                "search": arxiv_id,
                "per-page": 10,
            },
        )
        results = body.get("results", []) if body and not error else []
        return [
            self._record_from_work(item)
            for item in results
            if isinstance(item, dict)
            and extract_arxiv_id(
                str(item.get("primary_location", {}).get("landing_page_url", ""))
            )
            == arxiv_id
        ]


def _venue_from_work(item: dict[str, Any]) -> str | None:
    primary_location = item.get("primary_location") or {}
    primary_source = primary_location.get("source") or {}
    for location in item.get("locations", []) or []:
        if not isinstance(location, dict):
            continue
        source = location.get("source") or {}
        if source.get("type") and source.get("type") != "repository":
            return source.get("display_name") or location.get("raw_source_name")
    if primary_source.get("type") == "repository":
        return primary_location.get("raw_source_name") or primary_source.get(
            "display_name"
        )
    return primary_source.get("display_name") or primary_location.get("raw_source_name")


def _pages_from_biblio(biblio: dict[str, Any]) -> str | None:
    first_page = normalize_pages(biblio.get("first_page"))
    last_page = normalize_pages(biblio.get("last_page"))
    if first_page and last_page and first_page != last_page:
        return normalize_pages(f"{first_page}-{last_page}")
    return first_page or last_page


def _journal_locator_search(locator: JournalLocator) -> str:
    return " ".join(
        value
        for value in [
            locator.venue,
            str(locator.year) if locator.year else None,
            locator.volume,
            locator.issue,
            locator.pages,
            locator.article_number,
        ]
        if value
    )


def _journal_locator_cache_key(locator: JournalLocator) -> str:
    return f"journal-locator-v3:{locator.model_dump_json()}"
