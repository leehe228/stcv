from __future__ import annotations

import time

from ..config import RuntimeConfig
from ..schemas import PaperCandidate, ResearchPlan
from ..tools.cache import SQLiteCache
from ..tools.search_arxiv import search_arxiv
from ..tools.search_offline import search_offline
from ..tools.search_openalex import search_openalex
from ..tools.search_semantic_scholar import search_semantic_scholar
from ..tools.text import normalize_title
from .base import AgentBase


class LiteratureAgent(AgentBase):
    name = "Literature Agent"
    prompt_file = "literature.md"

    def collect(self, plan: ResearchPlan, config: RuntimeConfig, cache: SQLiteCache) -> list[PaperCandidate]:
        started = time.time()
        papers: list[PaperCandidate] = []
        tool_calls: list[dict] = []
        per_query_limit = max(4, config.max_papers)
        for query in plan.search_queries[:2]:
            offline = search_offline(query, per_query_limit)
            papers.extend(offline)
            tool_calls.append({"source": "offline_seed", "query": query, "count": len(offline)})
            if not config.offline:
                for search_fn in (search_arxiv, search_openalex, search_semantic_scholar):
                    found, call = search_fn(query, per_query_limit, cache, config)
                    papers.extend(found)
                    tool_calls.append(call | {"query": query, "count": len(found)})
        unique: dict[str, PaperCandidate] = {}
        for paper in papers:
            key = normalize_title(paper.title)
            if key and key not in unique:
                unique[key] = paper
        ranked = list(unique.values())[: max(config.max_papers * 2, config.min_verified_papers + 3)]
        output_ref = self.logger.write_json("paper_candidates.json", ranked)
        self.timed_log(started, "research_plan.json", output_ref, f"{len(ranked)} candidate papers", tool_calls)
        return ranked

