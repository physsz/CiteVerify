from __future__ import annotations

from typing import Any
from urllib.parse import quote

from citeverify.config import CiteVerifyConfig
from citeverify.lookup.base import HttpLookupProvider, LookupResponse
from citeverify.models import JournalLocator, ParsedAuthor, RegistryRecord
from citeverify.normalize.arxiv import arxiv_doi, extract_arxiv_id
from citeverify.normalize.author import parse_author
from citeverify.normalize.doi import normalize_doi
from citeverify.normalize.journal import normalize_issn
from citeverify.normalize.pages import normalize_article_number, normalize_pages
from citeverify.normalize.title import normalize_title


class CrossrefProvider(HttpLookupProvider):
    name = "Crossref"
    api_base = "https://api.crossref.org"

    def __init__(self, config: CiteVerifyConfig, **kwargs: Any) -> None:
        super().__init__(config, **kwargs)
        self.mailto = config.crossref_mailto or config.contact_email

    async def get_by_doi(self, doi: str) -> LookupResponse:
        normalized = normalize_doi(doi) or doi
        url = f"{self.api_base}/works/{quote(normalized, safe='')}"
        params = {"mailto": self.mailto} if self.mailto else None
        body, status_code, error = await self._get_json(
            query_kind="doi",
            normalized_query_value=normalized,
            url=url,
            params=params,
        )
        records: list[RegistryRecord] = []
        if body and status_code != 404 and not error:
            message = body.get("message", {})
            if isinstance(message, dict) and message.get("DOI"):
                records.append(self._record_from_work(message))
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
        params: dict[str, Any] = {"query.title": title, "rows": 5}
        if self.mailto:
            params["mailto"] = self.mailto
        body, status_code, error = await self._get_json(
            query_kind="title",
            normalized_query_value=normalized,
            url=f"{self.api_base}/works",
            params=params,
        )
        records = self._records_from_search(body) if body and not error else []
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
        query_value = locator.model_dump_json()
        params: dict[str, Any] = {"rows": 20}
        filters: list[str] = []
        if locator.issn:
            filters.append(f"issn:{locator.issn[0]}")
        elif locator.venue:
            params["query.container-title"] = locator.venue
        if locator.year:
            filters.extend(
                [
                    f"from-pub-date:{locator.year}-01-01",
                    f"until-pub-date:{locator.year}-12-31",
                ]
            )
        if filters:
            params["filter"] = ",".join(filters)
        if self.mailto:
            params["mailto"] = self.mailto
        body, status_code, error = await self._get_json(
            query_kind="journal_locator",
            normalized_query_value=query_value,
            url=f"{self.api_base}/works",
            params=params,
        )
        records = self._records_from_search(body) if body and not error else []
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=query_value,
            records=records,
            error=error,
            raw_status_code=status_code,
        )

    def _records_from_search(self, body: dict[str, Any] | None) -> list[RegistryRecord]:
        if not body:
            return []
        items = body.get("message", {}).get("items", [])
        if not isinstance(items, list):
            return []
        return [
            self._record_from_work(item)
            for item in items
            if isinstance(item, dict)
        ]

    def _record_from_work(self, item: dict[str, Any]) -> RegistryRecord:
        title = _first_list_value(item.get("title"))
        container_title = _first_list_value(item.get("container-title"))
        authors = [
            _author_from_crossref(author, index)
            for index, author in enumerate(item.get("author", []) or [])
            if isinstance(author, dict)
        ]
        doi = normalize_doi(item.get("DOI"))
        return RegistryRecord(
            source=self.name,
            source_record_url=item.get("URL"),
            title=title,
            authors=authors,
            year=_crossref_year(item),
            venue=container_title,
            issn=[
                normalized
                for normalized in (
                    normalize_issn(value) for value in item.get("ISSN", [])
                )
                if normalized
            ],
            volume=_string_or_none(item.get("volume")),
            issue=_string_or_none(item.get("issue")),
            pages=normalize_pages(item.get("page")),
            article_number=normalize_article_number(
                _first_list_value(item.get("article-number"))
                or _string_or_none(item.get("article-number"))
            ),
            doi=doi,
            arxiv_id=extract_arxiv_id(doi, item.get("URL")),
            url=item.get("URL"),
            record_type=item.get("type"),
            raw_response=item,
        )


def _first_list_value(value: Any) -> str | None:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return None


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _crossref_year(item: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        date_parts = item.get(key, {}).get("date-parts")
        if date_parts and isinstance(date_parts, list) and date_parts[0]:
            year = date_parts[0][0]
            if isinstance(year, int):
                return year
    return None


def _author_from_crossref(author: dict[str, Any], index: int) -> ParsedAuthor:
    family = author.get("family")
    given = author.get("given")
    if family and given:
        parsed = parse_author(f"{family}, {given}", index)
    elif family:
        parsed = parse_author(str(family), index)
    elif author.get("name"):
        parsed = parse_author(str(author["name"]), index)
    else:
        parsed = ParsedAuthor(raw_name="", position_in_list=index)
    return parsed.model_copy(update={"orcid": author.get("ORCID")})
