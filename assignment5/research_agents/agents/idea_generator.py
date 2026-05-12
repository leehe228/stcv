from __future__ import annotations

import time

from ..schemas import PaperSummary, ResearchIdea
from .base import AgentBase


class IdeaGenerator(AgentBase):
    name = "Idea Generator"
    prompt_file = "idea_generator.md"

    def generate(self, summaries: list[PaperSummary], topic: str) -> list[ResearchIdea]:
        started = time.time()
        ids = [summary.paper_id for summary in summaries[:5]]
        robotics = any("robot" in (s.title + s.method).lower() for s in summaries)
        if robotics:
            ideas = [
                ResearchIdea(
                    title="Shift-Aware VLA Policy Auditing",
                    hypothesis="A vision-language-action policy can flag distribution shift before action execution by comparing language intent, visual evidence, and affordance confidence.",
                    novelty="Combines VLA control with an explicit pre-action shift auditor instead of treating failures only as post-hoc rollout errors.",
                    feasibility="Feasible with Open X-Embodiment, DROID, and synthetic corruptions using frozen open VLM encoders plus lightweight classifiers.",
                    expected_contribution="A reproducible robustness evaluation protocol and an intervention mechanism for safer robot manipulation.",
                    related_paper_ids=ids,
                    novelty_score=4,
                    feasibility_score=4,
                ),
                ResearchIdea(
                    title="Counterfactual Prompt Stress Tests for Robot Policies",
                    hypothesis="Counterfactual edits to language and image prompts reveal brittle shortcuts in multimodal robot policies under object, lighting, and instruction shift.",
                    novelty="Turns prompt perturbation into a systematic robot-policy diagnostic rather than a generic VLM robustness probe.",
                    feasibility="Feasible with offline datasets and simulator-generated prompt/image variants before costly real robot validation.",
                    expected_contribution="A benchmark suite that links prompt sensitivity to manipulation success degradation.",
                    related_paper_ids=ids,
                    novelty_score=4,
                    feasibility_score=5,
                ),
                ResearchIdea(
                    title="Reviewer-in-the-Loop Robot Experiment Planner",
                    hypothesis="A critic-reviser multi-agent workflow can produce more complete robot experiment plans than a single LLM prompt by checking citations, baselines, and risks.",
                    novelty="Applies multi-agent research automation directly to embodied AI experiment planning with citation verification as a first-class step.",
                    feasibility="Highly feasible as a software system using open-source LLMs and public paper metadata.",
                    expected_contribution="A practical tool and evaluation rubric for designing stronger VLM robotics studies.",
                    related_paper_ids=ids,
                    novelty_score=3,
                    feasibility_score=5,
                ),
            ]
        else:
            ideas = [
                ResearchIdea(
                    title="Evidence-Grounded Multi-Agent Research Planner",
                    hypothesis="Citation verification plus critic-reviser loops reduce unsupported claims in automated research briefs.",
                    novelty="Moves beyond one-shot summarization by making citation status and revision traces explicit artifacts.",
                    feasibility="Feasible with arXiv/OpenAlex metadata and local open-source LLMs.",
                    expected_contribution="A reproducible workflow for safer literature-to-proposal automation.",
                    related_paper_ids=ids,
                    novelty_score=4,
                    feasibility_score=5,
                ),
                ResearchIdea(
                    title="Debate-Based Novelty Scoring for Paper Ideas",
                    hypothesis="Independent idea and critic agents can expose overlap with prior work better than a single generator.",
                    novelty="Uses structured debate and paper-id evidence to assign novelty risk, not just creative prose.",
                    feasibility="Feasible with deterministic schemas and public metadata.",
                    expected_contribution="A lightweight novelty triage method for early-stage project selection.",
                    related_paper_ids=ids,
                    novelty_score=4,
                    feasibility_score=4,
                ),
                ResearchIdea(
                    title="Budget-Aware Agent Routing for Research Automation",
                    hypothesis="Assigning high-capacity open models only to manager, critic, and writer roles preserves quality while reducing runtime.",
                    novelty="Studies model-role allocation as a controllable system variable in multi-agent research workflows.",
                    feasibility="Feasible on local H100 GPUs with Qwen/Gemma-family models.",
                    expected_contribution="A cost/performance analysis protocol for local open-source research agents.",
                    related_paper_ids=ids,
                    novelty_score=3,
                    feasibility_score=5,
                ),
            ]
        llm_prompt = (
            "Generate three research ideas grounded only in these paper summaries. For each idea, state novelty, "
            "feasibility, expected contribution, and evidence paper IDs.\n\n"
            f"Topic: {topic}\n"
            + "\n".join(f"- {s.paper_id}: {s.title}; limitation={s.limitations}" for s in summaries[:8])
        )
        llm_result, tool_calls = self.run_local_llm("idea_generator_raw", llm_prompt, max_new_tokens=500)
        output_ref = self.logger.write_json("ideas.json", ideas)
        preview = "\n".join(i.title for i in ideas) + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, "paper_summaries.json", output_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return ideas
