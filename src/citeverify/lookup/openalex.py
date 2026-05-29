from __future__ import annotations

from typing import Any
from urllib.parse import quote

from citeverify.lookup.base import HttpLookupProvider, LookupResponse
from citeverify.models import JournalLocator, RegistryRecord
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
        params: dict[str, Any] = {"per-page": 20}
        if locator.venue:
            params["search"] = locator.venue
        if filters:
            params["filter"] = ",".join(filters)
        body, status_code, error = await self._get_json(
            query_kind="journal_locator",
            normalized_query_value=locator.model_dump_json(),
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
        biblio = item.get("biblio") or {}
        doi = normalize_doi(item.get("doi"))
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
            venue=source.get("display_name"),
            issn=[
                normalized
                for normalized in (
                    normalize_issn(value) for value in source.get("issn", []) or []
                )
                if normalized
            ],
            volume=biblio.get("volume"),
            issue=biblio.get("issue"),
            pages=normalize_pages(biblio.get("first_page")),
            doi=doi,
            url=item.get("doi") or item.get("id"),
            record_type=item.get("type"),
            raw_response=item,
        )
