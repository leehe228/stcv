from __future__ import annotations

import time

from ..schemas import ExperimentPlan, ResearchIdea, ReviewReport, VerifiedPaper
from .base import AgentBase


class CriticReviewer(AgentBase):
    name = "Critic Reviewer"
    prompt_file = "critic.md"

    def review(self, idea: ResearchIdea, plan: ExperimentPlan, papers: list[VerifiedPaper], iteration: int) -> ReviewReport:
        started = time.time()
        citation_issues = []
        if len([p for p in papers if p.verification_status in {"verified", "partial"}]) < 5:
            citation_issues.append("Fewer than five verified or partially verified papers support the brief.")
        if any(p.verification_status == "unverified" for p in papers):
            citation_issues.append("Unverified citations must be excluded from the final references.")
        experiment_issues = []
        if len(plan.baselines) < 3:
            experiment_issues.append("At least three baselines are needed for a convincing comparison.")
        if not any("shift" in metric.lower() or "robust" in metric.lower() for metric in plan.metrics):
            experiment_issues.append("Metrics should explicitly measure robustness or distribution shift.")
        feasibility_issues = []
        if any("real robot" in risk.lower() for risk in plan.risks):
            feasibility_issues.append("Real robot validation may be too expensive; define an offline-first validation path.")
        novelty_issues = []
        if idea.novelty_score <= 3:
            novelty_issues.append("Novelty is moderate; the final proposal must state what is not already covered by prior agents or robotics systems.")
        required = citation_issues + experiment_issues + feasibility_issues + novelty_issues
        if iteration == 0:
            required.extend(
                [
                    "Add an explicit offline-first experiment path.",
                    "Tie each baseline to a cited prior paper.",
                    "State how the revision changes the risk/limitation section.",
                ]
            )
        score = 5 if not required else (4 if iteration > 0 and len(required) <= 2 else 3)
        report = ReviewReport(
            overall_score=score,
            novelty_issues=novelty_issues,
            feasibility_issues=feasibility_issues,
            experiment_issues=experiment_issues,
            citation_issues=citation_issues,
            required_revisions=required,
            stop=score >= 4,
        )
        llm_prompt = (
            "Act as a strict reviewer. Critique the proposed idea and experiment plan for novelty, feasibility, "
            "baseline quality, metrics, and citation risk. Return concrete required revisions.\n\n"
            f"Iteration: {iteration}\nIdea: {idea.model_dump()}\nExperiment plan: {plan.model_dump()}\n"
            f"Verified papers: {[p.title for p in papers]}"
        )
        llm_result, tool_calls = self.run_local_llm(f"critic_iter_{iteration}_raw", llm_prompt, max_new_tokens=420)
        output_ref = self.logger.write_json(f"review_report_iter_{iteration}.json", report)
        preview = report.model_dump_json() + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, "experiment_plan.json", output_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return report
