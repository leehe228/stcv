from __future__ import annotations

import time

from ..schemas import ExperimentPlan, ResearchIdea
from .base import AgentBase


class ExperimentDesigner(AgentBase):
    name = "Experiment Designer"
    prompt_file = "experiment_designer.md"

    def design(self, idea: ResearchIdea) -> ExperimentPlan:
        started = time.time()
        robotics = "robot" in idea.title.lower() or "vla" in idea.title.lower()
        if robotics:
            plan = ExperimentPlan(
                idea_title=idea.title,
                datasets=["Open X-Embodiment", "DROID", "Ravens/Transporter-style simulated manipulation tasks"],
                baselines=["RT-2-style VLA policy", "SayCan-style LLM plus affordance scorer", "Octo generalist robot policy"],
                metrics=[
                    "task success rate under in-distribution and shifted conditions",
                    "shift detection AUROC before action execution",
                    "false intervention rate",
                    "language-goal consistency score",
                ],
                ablations=[
                    "remove language-intent consistency check",
                    "remove visual corruption detector",
                    "replace affordance confidence with raw VLM score",
                    "train on single embodiment only",
                ],
                expected_failure_cases=[
                    "novel object categories absent from robot demonstrations",
                    "ambiguous instructions with multiple valid manipulation targets",
                    "visual shifts that preserve semantics but change low-level control affordances",
                ],
                risks=[
                    "offline datasets may not contain enough severe distribution shifts",
                    "VLM confidence can be poorly calibrated",
                    "real robot validation may be compute and hardware intensive",
                ],
                implementation_notes=[
                    "Use physical GPUs 2 and 3 only through CUDA_VISIBLE_DEVICES=2,3.",
                    "Cache all Hugging Face assets inside the repository-level .hf_cache directory.",
                ],
            )
        else:
            plan = ExperimentPlan(
                idea_title=idea.title,
                datasets=["arXiv/OpenAlex metadata snapshots", "manually verified seed-paper set", "synthetic noisy citation set"],
                baselines=["single-prompt proposal generator", "manager-worker workflow without critic", "critic-only post-hoc filter"],
                metrics=[
                    "verified citation precision",
                    "required-section coverage",
                    "reviewer issue resolution rate",
                    "wall-clock time and local token estimate",
                ],
                ablations=[
                    "remove citation verifier",
                    "remove critic-reviser loop",
                    "reduce paper count below five",
                    "use one shared prompt for all roles",
                ],
                expected_failure_cases=[
                    "paper metadata API downtime",
                    "topic with sparse public literature",
                    "critic gives vague revisions that cannot be operationalized",
                ],
                risks=[
                    "metadata-only summaries can miss nuanced claims",
                    "deterministic fallback is less creative than a full local LLM run",
                    "evaluation rubric may favor format completeness over scientific depth",
                ],
                implementation_notes=[
                    "Run with --use-local-llm when Qwen/Gemma weights are available in repo-local cache.",
                    "Run offline mode for deterministic grading and failure recovery.",
                ],
            )
        llm_prompt = (
            "Design a concrete experiment plan for this selected research idea. Include datasets, baselines, "
            "metrics, ablations, expected failure cases, and risks. Keep claims feasible.\n\n"
            f"Idea title: {idea.title}\nHypothesis: {idea.hypothesis}\nNovelty: {idea.novelty}\n"
            f"Feasibility: {idea.feasibility}"
        )
        llm_result, tool_calls = self.run_local_llm("experiment_designer_raw", llm_prompt, max_new_tokens=500)
        output_ref = self.logger.write_json("experiment_plan.json", plan)
        preview = plan.model_dump_json() + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, "ideas.json", output_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return plan
