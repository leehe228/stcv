from __future__ import annotations

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from ..config import RuntimeConfig
from ..schemas import PaperCandidate
from .cache import SQLiteCache


def search_arxiv(query: str, limit: int, cache: SQLiteCache, config: RuntimeConfig) -> tuple[list[PaperCandidate], dict]:
    key = cache.key("arxiv", {"q": query, "limit": limit})
    cached = cache.get(key)
    if cached is not None:
        return [PaperCandidate(**item) for item in cached], {"source": "arxiv", "cached": True}

    params = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    url = "https://export.arxiv.org/api/query?" + params
    last_error = None
    for attempt in range(config.retry_count + 1):
        try:
            with urllib.request.urlopen(url, timeout=config.request_timeout_sec) as response:
                raw = response.read()
            root = ET.fromstring(raw)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            results: list[PaperCandidate] = []
            for entry in root.findall("atom:entry", ns):
                title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
                abstract = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())
                year_text = (entry.findtext("atom:published", default="", namespaces=ns) or "")[:4]
                authors = [
                    author.findtext("atom:name", default="", namespaces=ns)
                    for author in entry.findall("atom:author", ns)
                ]
                link = entry.findtext("atom:id", default="", namespaces=ns)
                if title:
                    results.append(
                        PaperCandidate(
                            title=title,
                            authors=[a for a in authors if a],
                            year=int(year_text) if year_text.isdigit() else None,
                            venue="arXiv",
                            url=link or None,
                            source="arxiv",
                            abstract=abstract or None,
                        )
                    )
            cache.set(key, [item.model_dump() for item in results])
            return results, {"source": "arxiv", "cached": False, "url": url}
        except Exception as exc:  # network fallback is intentional
            last_error = str(exc)
            time.sleep(0.5 * (attempt + 1))
    return [], {"source": "arxiv", "cached": False, "error": last_error, "url": url}

