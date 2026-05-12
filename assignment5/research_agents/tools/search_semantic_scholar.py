from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from ..config import RuntimeConfig
from ..schemas import PaperCandidate
from .cache import SQLiteCache


def search_semantic_scholar(
    query: str, limit: int, cache: SQLiteCache, config: RuntimeConfig
) -> tuple[list[PaperCandidate], dict]:
    key = cache.key("semantic_scholar", {"q": query, "limit": limit})
    cached = cache.get(key)
    if cached is not None:
        return [PaperCandidate(**item) for item in cached], {"source": "semantic_scholar", "cached": True}
    fields = "title,authors,year,venue,url,abstract,externalIds"
    params = urllib.parse.urlencode({"query": query, "limit": limit, "fields": fields})
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + params
    last_error = None
    for attempt in range(config.retry_count + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "stcv-assignment5/0.1"})
            with urllib.request.urlopen(request, timeout=config.request_timeout_sec) as response:
                payload = json.loads(response.read().decode("utf-8"))
            papers: list[PaperCandidate] = []
            for item in payload.get("data", []):
                external = item.get("externalIds") or {}
                papers.append(
                    PaperCandidate(
                        title=item["title"],
                        authors=[a.get("name", "") for a in item.get("authors", []) if a.get("name")],
                        year=item.get("year"),
                        venue=item.get("venue"),
                        url=item.get("url"),
                        doi=external.get("DOI"),
                        source="semantic_scholar",
                        abstract=item.get("abstract"),
                    )
                )
            cache.set(key, [paper.model_dump() for paper in papers])
            return papers, {"source": "semantic_scholar", "cached": False, "url": url}
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.5 * (attempt + 1))
    return [], {"source": "semantic_scholar", "cached": False, "error": last_error, "url": url}

