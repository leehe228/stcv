from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..schemas import AgentLogEvent


class RunLogger:
    def __init__(self, run_dir: Path, run_id: str):
        self.run_dir = run_dir
        self.run_id = run_id
        self.logs_dir = run_dir / "logs"
        self.artifacts_dir = run_dir / "artifacts"
        self.outputs_dir = run_dir / "outputs"
        for path in (self.logs_dir, self.artifacts_dir, self.outputs_dir):
            path.mkdir(parents=True, exist_ok=True)
        self.events_path = self.logs_dir / "agent_events.jsonl"
        self.errors_path = self.logs_dir / "errors.jsonl"
        self.step_index = 0

    def artifact_path(self, name: str) -> Path:
        return self.artifacts_dir / name

    def output_path(self, name: str) -> Path:
        return self.outputs_dir / name

    def write_json(self, relative: str, payload: Any) -> str:
        path = self.artifacts_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        def default(obj: Any) -> Any:
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            return str(obj)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=default), encoding="utf-8")
        return str(path.relative_to(self.run_dir))

    def write_markdown(self, relative: str, text: str, output: bool = True) -> str:
        base = self.outputs_dir if output else self.artifacts_dir
        path = base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return str(path.relative_to(self.run_dir))

    def event(
        self,
        agent_name: str,
        model: str,
        prompt_path: str,
        input_ref: str,
        output_ref: str,
        elapsed_sec: float,
        tool_calls: list[dict[str, Any]] | None = None,
        token_usage: dict[str, int] | None = None,
        error: str | None = None,
    ) -> None:
        self.step_index += 1
        event = AgentLogEvent(
            run_id=self.run_id,
            step_index=self.step_index,
            agent_name=agent_name,
            model=model,
            prompt_path=prompt_path,
            input_ref=input_ref,
            output_ref=output_ref,
            tool_calls=tool_calls or [],
            token_usage=token_usage,
            elapsed_sec=elapsed_sec,
            error=error,
        )
        line = event.model_dump_json() + "\n"
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(line)
        if error:
            with self.errors_path.open("a", encoding="utf-8") as handle:
                handle.write(line)

