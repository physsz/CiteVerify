from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CiteVerifyConfig:
    cache_path: Path | None = Path(".citeverify-cache.sqlite")
    use_cache: bool = True
    offline: bool = False
    timeout: float = 20.0
    max_concurrency: int = 5
    contact_email: str | None = None
    crossref_mailto: str | None = None
    semantic_scholar_api_key: str | None = None
    ncbi_api_key: str | None = None

    @classmethod
    def from_env(cls) -> CiteVerifyConfig:
        cache_value = os.getenv("CITEVERIFY_CACHE", ".citeverify-cache.sqlite")
        timeout = float(os.getenv("CITEVERIFY_TIMEOUT", "20"))
        max_concurrency = int(os.getenv("CITEVERIFY_MAX_CONCURRENCY", "5"))
        return cls(
            cache_path=Path(cache_value) if cache_value else None,
            timeout=timeout,
            max_concurrency=max_concurrency,
            contact_email=os.getenv("CITEVERIFY_CONTACT_EMAIL"),
            crossref_mailto=os.getenv("CITEVERIFY_CROSSREF_MAILTO"),
            semantic_scholar_api_key=os.getenv("CITEVERIFY_SEMANTIC_SCHOLAR_API_KEY"),
            ncbi_api_key=os.getenv("CITEVERIFY_NCBI_API_KEY"),
        )

    @property
    def user_agent(self) -> str:
        if self.contact_email:
            return f"citeverify/0.1.0 (mailto:{self.contact_email})"
        return "citeverify/0.1.0"
