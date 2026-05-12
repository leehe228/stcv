from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


class CostTracker:
    def __init__(self) -> None:
        self.by_agent: dict[str, dict[str, float]] = defaultdict(
            lambda: {"prompt_tokens": 0, "completion_tokens": 0, "elapsed_sec": 0.0, "cost_usd": 0.0}
        )

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, int(len(text.split()) * 1.25))

    def add(self, agent_name: str, prompt: str, output: str, elapsed_sec: float) -> dict[str, int]:
        prompt_tokens = self.estimate_tokens(prompt)
        completion_tokens = self.estimate_tokens(output)
        row = self.by_agent[agent_name]
        row["prompt_tokens"] += prompt_tokens
        row["completion_tokens"] += completion_tokens
        row["elapsed_sec"] += elapsed_sec
        # Open-source local inference has no paid API cost.
        row["cost_usd"] += 0.0
        return {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        total = {
            "prompt_tokens": sum(v["prompt_tokens"] for v in self.by_agent.values()),
            "completion_tokens": sum(v["completion_tokens"] for v in self.by_agent.values()),
            "elapsed_sec": sum(v["elapsed_sec"] for v in self.by_agent.values()),
            "cost_usd": 0.0,
        }
        payload = {"by_agent": dict(self.by_agent), "total": total, "billing_note": "No paid API was used."}
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

