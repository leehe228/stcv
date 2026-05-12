from __future__ import annotations

import re
import time

from ..schemas import ResearchPlan, UserRequest
from .base import AgentBase


class ResearchManager(AgentBase):
    name = "Research Manager"
    prompt_file = "manager.md"

    def plan(self, request: UserRequest) -> ResearchPlan:
        started = time.time()
        topic = request.topic
        tokens = [w for w in re.findall(r"[A-Za-z0-9-]+", topic.lower()) if len(w) > 3]
        priority = " ".join(tokens[:8]) or topic
        queries = [
            topic,
            f"{priority} recent survey benchmark",
            f"{priority} dataset baseline evaluation",
            f"{priority} robustness distribution shift",
        ]
        plan = ResearchPlan(
            topic=topic,
            search_queries=queries,
            constraints=request.constraints,
            workflow=[
                "manager",
                "literature",
                "citation_verifier",
                "summarizer",
                "idea_generator",
                "experiment_designer",
                "critic",
                "reviser",
                "writer",
            ],
            stopping_rule=f"Stop when reviewer score >= 4 or after {request.max_revision_iter} revision iterations.",
        )
        llm_prompt = (
            "Given this research topic, produce a concise multi-agent research plan with search keywords, "
            "citation verification requirements, and stopping criteria.\n\n"
            f"Topic: {request.topic}\nConstraints: {request.constraints}"
        )
        llm_result, tool_calls = self.run_local_llm("manager_plan_raw", llm_prompt, max_new_tokens=220)
        output_ref = self.logger.write_json("research_plan.json", plan)
        preview = plan.model_dump_json() + ("\n\nLLM raw:\n" + llm_result.text if llm_result.text else "")
        self.timed_log(started, "config.json", output_ref, preview, tool_calls=tool_calls, error=llm_result.error)
        return plan
