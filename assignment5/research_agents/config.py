from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parent
RUNS_ROOT = PACKAGE_ROOT / "runs"
HF_CACHE_ROOT = REPO_ROOT / ".hf_cache"
CONDA_ROOT = REPO_ROOT / ".conda"


def configure_local_storage() -> None:
    """Force model, dataset, and temporary caches to stay inside the repo."""
    HF_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    (HF_CACHE_ROOT / "hub").mkdir(parents=True, exist_ok=True)
    (HF_CACHE_ROOT / "datasets").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / ".tmp").mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2,3")
    os.environ.setdefault("HF_HOME", str(HF_CACHE_ROOT))
    os.environ.setdefault("HF_HUB_CACHE", str(HF_CACHE_ROOT / "hub"))
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(HF_CACHE_ROOT / "hub"))
    os.environ.setdefault("TRANSFORMERS_CACHE", str(HF_CACHE_ROOT / "hub"))
    os.environ.setdefault("HF_DATASETS_CACHE", str(HF_CACHE_ROOT / "datasets"))
    os.environ.setdefault("TMPDIR", str(REPO_ROOT / ".tmp"))
    os.environ.setdefault("XDG_CACHE_HOME", str(REPO_ROOT / ".cache"))


@dataclass(frozen=True)
class ModelConfig:
    manager_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    critic_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    writer_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    idea_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    experiment_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    summarizer_model: str = "Qwen/Qwen3-4B-Instruct-2507"
    fallback_model: str = "deterministic-local-rules"
    temperature: float = 0.2
    max_new_tokens: int = 768


@dataclass(frozen=True)
class RuntimeConfig:
    max_papers: int = 8
    min_verified_papers: int = 5
    max_revision_iter: int = 2
    request_timeout_sec: float = 8.0
    retry_count: int = 2
    offline: bool = False
    use_local_llm: bool = False
    models: ModelConfig = field(default_factory=ModelConfig)


configure_local_storage()
