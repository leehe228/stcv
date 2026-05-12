from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from ..tools.cost_tracker import CostTracker
from ..tools.llm import LLMResult
from ..tools.llm import LLMRouter
from ..tools.logger import RunLogger


class AgentBase:
    name = "Agent"
    prompt_file = ""

    def __init__(self, logger: RunLogger, llm: LLMRouter, cost_tracker: CostTracker):
        self.logger = logger
        self.llm = llm
        self.cost_tracker = cost_tracker

    @property
    def prompt_path(self) -> Path:
        return Path(__file__).resolve().parents[1] / "prompts" / self.prompt_file

    def prompt_text(self) -> str:
        if self.prompt_path.exists():
            return self.prompt_path.read_text(encoding="utf-8")
        return self.name

    def timed_log(
        self,
        started: float,
        input_ref: str,
        output_ref: str,
        output_preview: str,
        tool_calls: list[dict[str, Any]] | None = None,
        error: str | None = None,
    ) -> None:
        elapsed = time.time() - started
        prompt = self.prompt_text()
        token_usage = self.cost_tracker.add(self.name, prompt, output_preview, elapsed)
        self.logger.event(
            agent_name=self.name,
            model=self.llm.model_for_agent(self.name),
            prompt_path=str(self.prompt_path),
            input_ref=input_ref,
            output_ref=output_ref,
            tool_calls=tool_calls or [],
            token_usage=token_usage,
            elapsed_sec=elapsed,
            error=error,
        )

    def run_local_llm(self, artifact_name: str, prompt: str, max_new_tokens: int = 256) -> tuple[LLMResult, list[dict[str, Any]]]:
        if not self.llm.config.use_local_llm:
            return LLMResult(text="", model=self.llm.model_for_agent(self.name), used_transformers=False), []
        result = self.llm.complete(self.name, prompt, max_new_tokens=max_new_tokens)
        ref = self.logger.write_json(
            f"llm/{artifact_name}.json",
            {
                "agent_name": self.name,
                "model": result.model,
                "used_transformers": result.used_transformers,
                "device_summary": result.device_summary,
                "prompt": prompt,
                "output": result.text,
                "error": result.error,
            },
        )
        return result, [
            {
                "tool": "transformers.generate",
                "model": result.model,
                "used_transformers": result.used_transformers,
                "device_summary": result.device_summary,
                "artifact": ref,
                "error": result.error,
            }
        ]
