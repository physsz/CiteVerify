from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CachedResponse:
    status_code: int
    headers: dict[str, str]
    body: dict[str, Any]


class ResponseCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                create table if not exists responses (
                    provider_name text not null,
                    query_kind text not null,
                    normalized_query_value text not null,
                    api_base text not null,
                    status_code integer not null,
                    response_headers text not null,
                    response_body text not null,
                    created_at real not null,
                    expires_at real not null,
                    primary key (
                        provider_name,
                        query_kind,
                        normalized_query_value,
                        api_base
                    )
                )
                """
            )

    def get(
        self,
        *,
        provider_name: str,
        query_kind: str,
        normalized_query_value: str,
        api_base: str,
    ) -> CachedResponse | None:
        now = time.time()
        with self._connect() as conn:
            row = conn.execute(
                """
                select status_code, response_headers, response_body, expires_at
                from responses
                where provider_name = ?
                  and query_kind = ?
                  and normalized_query_value = ?
                  and api_base = ?
                """,
                (provider_name, query_kind, normalized_query_value, api_base),
            ).fetchone()
        if row is None:
            return None
        status_code, headers, body, expires_at = row
        if expires_at < now:
            return None
        return CachedResponse(
            status_code=status_code,
            headers=json.loads(headers),
            body=json.loads(body),
        )

    def set(
        self,
        *,
        provider_name: str,
        query_kind: str,
        normalized_query_value: str,
        api_base: str,
        status_code: int,
        headers: dict[str, str],
        body: dict[str, Any],
        ttl_seconds: int,
    ) -> None:
        now = time.time()
        expires_at = now + ttl_seconds
        with self._connect() as conn:
            conn.execute(
                """
                insert or replace into responses (
                    provider_name,
                    query_kind,
                    normalized_query_value,
                    api_base,
                    status_code,
                    response_headers,
                    response_body,
                    created_at,
                    expires_at
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    provider_name,
                    query_kind,
                    normalized_query_value,
                    api_base,
                    status_code,
                    json.dumps(headers),
                    json.dumps(body),
                    now,
                    expires_at,
                ),
            )
