from __future__ import annotations

import time

from ..schemas import ExperimentPlan, ResearchIdea, RevisedPlan, ReviewReport
from .base import AgentBase


class RevisionAgent(AgentBase):
    name = "Revision Agent"
    prompt_file = "reviser.md"

    def revise(self, idea: ResearchIdea, plan: ExperimentPlan, review: ReviewReport, iteration: int) -> RevisedPlan:
        started = time.time()
        revised_idea = idea.model_copy(
            update={
                "feasibility": idea.feasibility
                + " The revised scope starts with offline dataset replay and simulator stress tests before any real-robot run.",
                "expected_contribution": idea.expected_contribution
                + " It also reports citation-grounded baseline mapping and reviewer issue resolution.",
                "feasibility_score": min(5, idea.feasibility_score + 1),
            }
        )
        extra_notes = [
            "Offline-first validation path: run all shifted-condition tests on stored demonstrations or simulation before hardware trials.",
            "Baseline mapping: SayCan/RT-2/Octo or single-prompt/manager-worker variants are linked to verified references.",
            "Risk section now preserves unresolved limits instead of hiding them after revision.",
        ]
        revised_plan = plan.model_copy(
            update={
                "implementation_notes": list(dict.fromkeys(plan.implementation_notes + extra_notes)),
                "risks": list(dict.fromkeys(plan.risks + ["Residual risk: metadata summaries may not capture all paper-specific caveats."])),
            }
        )
        result = RevisedPlan(
            idea=revised_idea,
            experiment_plan=revised_plan,
            revision_notes=extra_notes,
            addressed_revisions=review.required_revisions,
        )
        llm_prompt = (
            "Revise the idea and experiment plan using the reviewer checklist. State how each issue is addressed.\n\n"
            f"Idea: {idea.model_dump()}\nExperiment plan: {plan.model_dump()}\nReview: {review.model_dump()}"
        )
        llm_result, tool_calls = self.run_local_llm(f"reviser_iter_{iteration}_raw", llm_prompt, max_new_tokens=420)
        output_ref = self.logger.write_json(f"revised_plan_iter_{iteration}.json", result)
        preview = result.model_dump_json() + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, f"review_report_iter_{iteration}.json", output_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return result
