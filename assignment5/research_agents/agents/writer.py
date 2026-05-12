from __future__ import annotations

import time

from ..schemas import ExperimentPlan, PaperSummary, ResearchBrief, ResearchIdea, ReviewReport, VerifiedPaper
from .base import AgentBase


class WriterAgent(AgentBase):
    name = "Writer Agent"
    prompt_file = "writer.md"

    def write(
        self,
        topic: str,
        papers: list[VerifiedPaper],
        summaries: list[PaperSummary],
        ideas: list[ResearchIdea],
        selected_idea: ResearchIdea,
        plan: ExperimentPlan,
        reviews: list[ReviewReport],
        revision_notes: list[str],
    ) -> ResearchBrief:
        started = time.time()
        base_md = self._markdown(topic, papers, summaries, ideas, selected_idea, plan, reviews, revision_notes)
        llm_prompt = (
            "Write a compact final research brief in Markdown, maximum 500 words. Use only the provided verified references and "
            "do not invent papers. Include background, related work, proposed method, experiment plan, critique, "
            "revisions, limitations, and references.\n\n"
            f"Topic: {topic}\n"
            f"Verified references: {[{'title': p.title, 'year': p.year, 'url': p.url} for p in papers]}\n"
            f"Selected idea: {selected_idea.model_dump()}\nExperiment plan: {plan.model_dump()}\n"
            f"Reviews: {[r.model_dump() for r in reviews]}\nRevision notes: {revision_notes}"
        )
        llm_result, tool_calls = self.run_local_llm("writer_research_brief_raw", llm_prompt, max_new_tokens=900)
        md = self._with_llm_synthesis(base_md, llm_result.text, llm_result.model, llm_result.device_summary)
        self.logger.write_markdown("research_brief.md", md)
        output_ref = self.logger.write_json("research_brief_manifest.json", {"references": [p.model_dump() for p in papers]})
        self.timed_log(started, "all_artifacts", "outputs/research_brief.md", md, tool_calls=tool_calls, error=llm_result.error)
        return ResearchBrief(markdown=md, references=papers)

    @staticmethod
    def _with_llm_synthesis(base_md: str, llm_text: str, model: str, device_summary: str | None) -> str:
        if not llm_text.strip():
            return base_md
        return (
            base_md.rstrip()
            + "\n\n## Local LLM Generated Synthesis\n"
            + f"- Model actually loaded: `{model}`\n"
            + f"- Device map: `{device_summary or 'not reported'}`\n\n"
            + llm_text.strip()
            + "\n"
        )

    @staticmethod
    def _markdown(
        topic: str,
        papers: list[VerifiedPaper],
        summaries: list[PaperSummary],
        ideas: list[ResearchIdea],
        selected_idea: ResearchIdea,
        plan: ExperimentPlan,
        reviews: list[ReviewReport],
        revision_notes: list[str],
    ) -> str:
        def bullets(items: list[str]) -> str:
            return "\n".join(f"- {item}" for item in items)

        related_rows = "\n".join(
            f"| {s.title} | {s.method} | {s.limitations} | {s.relevance_to_topic} |" for s in summaries
        )
        idea_rows = "\n".join(
            f"| {idea.title} | {idea.novelty_score} | {idea.feasibility_score} | {idea.expected_contribution} |"
            for idea in ideas
        )
        review_rows = "\n".join(
            f"| Iteration {idx} | {r.overall_score}/5 | {'; '.join(r.required_revisions) or 'No required revisions'} |"
            for idx, r in enumerate(reviews)
        )
        references = "\n".join(
            f"- {idx + 1}. {', '.join(p.authors[:6])} ({p.year}). {p.title}. {p.venue or p.source}. {p.url or p.doi} [{p.verification_status}]"
            for idx, p in enumerate(papers)
        )
        return f"""# Research Brief

## Background
Research topic: **{topic}**.

The system decomposes research automation into manager-worker steps plus a critic-reviser loop. It avoids paid APIs and records every prompt, tool call, citation status, and intermediate artifact for reproducibility.

## Related Work
| Paper | Method | Limitation | Relevance |
|---|---|---|---|
{related_rows}

## Research Gap
The verified literature suggests three recurring gaps: robustness under shifted inputs, incomplete baseline mapping, and weak traceability from generated ideas back to citations. A useful proposal should therefore couple idea generation with citation verification and reviewer-style revision.

## Candidate Ideas
| Idea | Novelty | Feasibility | Expected contribution |
|---|---:|---:|---|
{idea_rows}

## Proposed Idea
**{selected_idea.title}**

- Hypothesis: {selected_idea.hypothesis}
- Novelty: {selected_idea.novelty}
- Feasibility: {selected_idea.feasibility}
- Expected contribution: {selected_idea.expected_contribution}

## Experiment Plan
### Datasets
{bullets(plan.datasets)}

### Baselines
{bullets(plan.baselines)}

### Metrics
{bullets(plan.metrics)}

### Ablations
{bullets(plan.ablations)}

### Expected Failure Cases
{bullets(plan.expected_failure_cases)}

### Risks
{bullets(plan.risks)}

### Implementation Notes
{bullets(plan.implementation_notes)}

## Reviewer Critique and Revisions
| Review | Score | Required revisions |
|---|---:|---|
{review_rows}

Revision actions:
{bullets(revision_notes or ["No revision was needed after the final review."])}

## Limitations
- Metadata-level summaries are useful for reproducible triage but cannot replace a full-paper reading step.
- Local open-source LLM execution depends on model cache availability and GPU memory; this run records raw Qwen outputs alongside schema-controlled artifacts.
- Citation verification is conservative: unverified references are logged but excluded from final references.

## References
{references}
"""
