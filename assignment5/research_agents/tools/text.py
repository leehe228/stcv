from __future__ import annotations

import re
from hashlib import sha1


def normalize_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def paper_id(title: str, year: int | None) -> str:
    year_part = str(year or "unknown")
    digest = sha1(normalize_title(title).encode("utf-8")).hexdigest()[:8]
    first = normalize_title(title).split(" ")[:3]
    return "-".join(first + [year_part, digest])


def keyword_overlap(query: str, text: str) -> int:
    stop = {
        "the",
        "and",
        "for",
        "with",
        "under",
        "from",
        "using",
        "models",
        "model",
        "research",
        "learning",
        "agent",
        "agents",
    }
    q = {w for w in re.findall(r"[a-z0-9]+", query.lower()) if w not in stop and len(w) > 2}
    t = {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in stop and len(w) > 2}
    return len(q & t)

