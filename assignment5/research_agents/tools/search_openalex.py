from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from ..config import RuntimeConfig
from ..schemas import PaperCandidate
from .cache import SQLiteCache


def search_openalex(query: str, limit: int, cache: SQLiteCache, config: RuntimeConfig) -> tuple[list[PaperCandidate], dict]:
    key = cache.key("openalex", {"q": query, "limit": limit})
    cached = cache.get(key)
    if cached is not None:
        return [PaperCandidate(**item) for item in cached], {"source": "openalex", "cached": True}
    params = urllib.parse.urlencode({"search": query, "per-page": limit})
    url = "https://api.openalex.org/works?" + params
    last_error = None
    for attempt in range(config.retry_count + 1):
        try:
            with urllib.request.urlopen(url, timeout=config.request_timeout_sec) as response:
                payload = json.loads(response.read().decode("utf-8"))
            papers: list[PaperCandidate] = []
            for item in payload.get("results", []):
                title = item.get("title")
                if not title:
                    continue
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in item.get("authorships", [])[:8]
                    if a.get("author", {}).get("display_name")
                ]
                papers.append(
                    PaperCandidate(
                        title=title,
                        authors=authors,
                        year=item.get("publication_year"),
                        venue=(item.get("primary_location") or {}).get("source", {}).get("display_name"),
                        url=item.get("doi") or item.get("id"),
                        doi=item.get("doi"),
                        source="openalex",
                        abstract=None,
                    )
                )
            cache.set(key, [paper.model_dump() for paper in papers])
            return papers, {"source": "openalex", "cached": False, "url": url}
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.5 * (attempt + 1))
    return [], {"source": "openalex", "cached": False, "error": last_error, "url": url}

