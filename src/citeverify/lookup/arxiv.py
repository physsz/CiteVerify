from __future__ import annotations

from citeverify.lookup.base import LookupResponse
from citeverify.models import JournalLocator


class ArxivProvider:
    name = "arXiv"

    async def get_by_doi(self, doi: str) -> LookupResponse:
        return LookupResponse(source=self.name, query_kind="doi", query_value=doi)

    async def search_by_title(self, title: str) -> LookupResponse:
        return LookupResponse(source=self.name, query_kind="title", query_value=title)

    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse:
        return LookupResponse(
            source=self.name,
            query_kind="journal_locator",
            query_value=locator.model_dump_json(),
        )
