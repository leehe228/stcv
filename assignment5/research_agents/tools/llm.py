from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..config import RuntimeConfig, configure_local_storage


@dataclass
class LLMResult:
    text: str
    model: str
    used_transformers: bool
    error: str | None = None
    device_summary: str | None = None


class LLMRouter:
    """Optional local open-source LLM backend.

    The workflow is deterministic by default so tests are reproducible without
    a network download. Passing --use-local-llm enables Hugging Face
    Transformers with caches and temp files constrained to the repository.
    """

    def __init__(self, config: RuntimeConfig):
        configure_local_storage()
        self.config = config
        self._loaded: dict[str, tuple[Any, Any, str]] = {}
        self._load_error: str | None = None

    def model_for_agent(self, agent_name: str) -> str:
        lower = agent_name.lower()
        if "critic" in lower:
            return self.config.models.critic_model
        if "writer" in lower:
            return self.config.models.writer_model
        if "idea" in lower:
            return self.config.models.idea_model
        if "experiment" in lower:
            return self.config.models.experiment_model
        if "summary" in lower or "summarizer" in lower:
            return self.config.models.summarizer_model
        if "revision" in lower or "reviser" in lower:
            return self.config.models.critic_model
        if "manager" in lower:
            return self.config.models.manager_model
        return self.config.models.fallback_model

    def complete(self, agent_name: str, prompt: str, max_new_tokens: int | None = None) -> LLMResult:
        model = self.model_for_agent(agent_name)
        if not self.config.use_local_llm:
            return LLMResult(text="", model=model + " (configured; deterministic backend used)", used_transformers=False)
        try:
            tokenizer, loaded_model, device_summary = self._load(model)
            messages = [
                {
                    "role": "system",
                    "content": "You are a concise research automation agent. Return useful, citation-aware content only.",
                },
                {"role": "user", "content": prompt},
            ]
            if hasattr(tokenizer, "apply_chat_template"):
                prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                prompt_text = prompt
            inputs = tokenizer(prompt_text, return_tensors="pt")
            first_device = next(loaded_model.parameters()).device
            inputs = {key: value.to(first_device) for key, value in inputs.items()}
            import torch

            with torch.inference_mode():
                generated = loaded_model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens or self.config.models.max_new_tokens,
                    do_sample=self.config.models.temperature > 0,
                    temperature=self.config.models.temperature if self.config.models.temperature > 0 else None,
                    pad_token_id=tokenizer.eos_token_id,
                )
            new_tokens = generated[0][inputs["input_ids"].shape[-1] :]
            output = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
            return LLMResult(text=output, model=model, used_transformers=True, device_summary=device_summary)
        except Exception as exc:
            self._load_error = str(exc)
            return LLMResult(text="", model=model + " (fallback after local-load error)", used_transformers=False, error=str(exc))

    def _load(self, model_id: str) -> tuple[Any, Any, str]:
        if model_id in self._loaded:
            return self._loaded[model_id]
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=None)
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            cache_dir=None,
            device_map="auto",
            dtype=dtype,
            low_cpu_mem_usage=True,
        )
        model.eval()
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        device_summary = self._device_summary(model)
        self._loaded[model_id] = (tokenizer, model, device_summary)
        return self._loaded[model_id]

    @staticmethod
    def _device_summary(model: Any) -> str:
        if hasattr(model, "hf_device_map") and model.hf_device_map:
            return str(model.hf_device_map)
        try:
            return str(next(model.parameters()).device)
        except StopIteration:
            return "unknown"
