from __future__ import annotations

from typing import Any, Protocol

import httpx
from pydantic import BaseModel, Field
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from citeverify.cache import ResponseCache
from citeverify.config import CiteVerifyConfig
from citeverify.models import JournalLocator, RegistryRecord


class LookupResponse(BaseModel):
    source: str
    query_kind: str
    query_value: str
    records: list[RegistryRecord] = Field(default_factory=list)
    error: str | None = None
    raw_status_code: int | None = None


class LookupProvider(Protocol):
    name: str

    async def get_by_doi(self, doi: str) -> LookupResponse: ...

    async def search_by_title(self, title: str) -> LookupResponse: ...

    async def search_by_journal_locator(
        self, locator: JournalLocator
    ) -> LookupResponse: ...


class HttpLookupProvider:
    name: str
    api_base: str

    def __init__(
        self,
        config: CiteVerifyConfig,
        cache: ResponseCache | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.config = config
        self.cache = cache
        self._client = client

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.config.timeout,
                headers={"User-Agent": self.config.user_agent},
            )
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def _get_json(
        self,
        *,
        query_kind: str,
        normalized_query_value: str,
        url: str,
        params: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any] | None, int | None, str | None]:
        cached = None
        if self.config.use_cache and self.cache is not None:
            cached = self.cache.get(
                provider_name=self.name,
                query_kind=query_kind,
                normalized_query_value=normalized_query_value,
                api_base=self.api_base,
            )
        if cached is not None:
            return cached.body, cached.status_code, None
        if self.config.offline:
            return None, None, "offline mode: no cached response"

        try:
            response = await self._request(url, params=params)
        except httpx.HTTPError as exc:
            return None, None, str(exc)
        except Exception as exc:
            return None, None, f"provider request failed: {exc}"

        status_code = response.status_code
        if status_code == 404:
            body = {"message": "not found"}
            if self.config.use_cache and self.cache is not None:
                self.cache.set(
                    provider_name=self.name,
                    query_kind=query_kind,
                    normalized_query_value=normalized_query_value,
                    api_base=self.api_base,
                    status_code=status_code,
                    headers=dict(response.headers),
                    body=body,
                    ttl_seconds=60 * 60 * 24,
                )
            return body, status_code, None
        try:
            body = response.json()
        except ValueError:
            return None, status_code, "provider returned non-JSON response"

        if 200 <= status_code < 300:
            if self.config.use_cache and self.cache is not None:
                self.cache.set(
                    provider_name=self.name,
                    query_kind=query_kind,
                    normalized_query_value=normalized_query_value,
                    api_base=self.api_base,
                    status_code=status_code,
                    headers=dict(response.headers),
                    body=body,
                    ttl_seconds=60 * 60 * 24 * 30,
                )
            return body, status_code, None
        return body, status_code, f"provider returned HTTP {status_code}"

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
        reraise=True,
    )
    async def _request(
        self, url: str, params: dict[str, Any] | None = None
    ) -> httpx.Response:
        return await self.client.get(url, params=params)
