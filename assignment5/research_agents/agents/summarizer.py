from __future__ import annotations

import time

from ..schemas import PaperSummary, VerifiedPaper
from .base import AgentBase


class PaperSummarizer(AgentBase):
    name = "Paper Summarizer"
    prompt_file = "summarizer.md"

    def summarize(self, papers: list[VerifiedPaper], topic: str) -> tuple[list[PaperSummary], str]:
        started = time.time()
        summaries: list[PaperSummary] = []
        for paper in papers:
            abstract = paper.abstract or "No abstract was available from the metadata source."
            lower = (paper.title + " " + abstract).lower()
            if "robot" in lower or "manipulation" in lower:
                method = "Language-conditioned or multimodal robot policy design."
                experiments = "Robot manipulation, embodied reasoning, or cross-embodiment evaluation."
                limitations = "Robustness under distribution shift and transparent failure diagnosis remain hard."
            elif "agent" in lower or "multi-agent" in lower:
                method = "Role-based agent orchestration with memory, planning, conversation, or tool use."
                experiments = "Software task solving, simulated worlds, or benchmarked reasoning workflows."
                limitations = "Evaluation often depends on brittle prompts and sparse human validation."
            else:
                method = "Model and benchmark contribution relevant to the topic."
                experiments = "Reported benchmark or case-study evaluation."
                limitations = "The abstract-level summary may omit important implementation details."
            summaries.append(
                PaperSummary(
                    paper_id=paper.paper_id,
                    title=paper.title,
                    core_claim=abstract[:280],
                    method=method,
                    experiments=experiments,
                    limitations=limitations,
                    relevance_to_topic=f"Connects to '{topic}' through evidence about methods, baselines, or evaluation risks.",
                )
            )
        table = self._table(summaries)
        llm_prompt = (
            "Summarize the verified papers for the research topic. Include core claims, methods, limitations, "
            "and relevance. Do not invent citations.\n\n"
            f"Topic: {topic}\n"
            + "\n".join(f"- {p.title} ({p.year}): {p.abstract or 'metadata only'}" for p in papers[:8])
        )
        llm_result, tool_calls = self.run_local_llm("summarizer_related_work_raw", llm_prompt, max_new_tokens=420)
        summary_ref = self.logger.write_json("paper_summaries.json", summaries)
        self.logger.write_markdown("related_work_table.md", table)
        preview = table + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, "verified_papers.json", summary_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return summaries, table

    @staticmethod
    def _table(summaries: list[PaperSummary]) -> str:
        lines = [
            "# Related Work Table",
            "",
            "| Paper | Core claim | Method | Experiments | Limitations | Relevance |",
            "|---|---|---|---|---|---|",
        ]
        for item in summaries:
            cells = [
                item.title,
                item.core_claim,
                item.method,
                item.experiments,
                item.limitations,
                item.relevance_to_topic,
            ]
            safe = [c.replace("|", "/").replace("\n", " ") for c in cells]
            lines.append("| " + " | ".join(safe) + " |")
        return "\n".join(lines) + "\n"
