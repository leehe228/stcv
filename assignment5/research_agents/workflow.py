from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from .agents.critic import CriticReviewer
from .agents.experiment_designer import ExperimentDesigner
from .agents.idea_generator import IdeaGenerator
from .agents.literature import LiteratureAgent
from .agents.manager import ResearchManager
from .agents.reviser import RevisionAgent
from .agents.summarizer import PaperSummarizer
from .agents.verifier import CitationVerifier
from .agents.writer import WriterAgent
from .config import RUNS_ROOT, RuntimeConfig, configure_local_storage
from .schemas import ResearchBrief, UserRequest
from .tools.cache import SQLiteCache
from .tools.cost_tracker import CostTracker
from .tools.llm import LLMRouter
from .tools.logger import RunLogger


def build_run_id(topic: str) -> str:
    stamp = time.strftime("%Y%m%d_%H%M%S")
    digest = hashlib.sha1(topic.encode("utf-8")).hexdigest()[:8]
    return f"{stamp}_{digest}"


def run_workflow(request: UserRequest, config: RuntimeConfig, output_dir: Path | None = None) -> tuple[ResearchBrief, Path]:
    configure_local_storage()
    run_id = output_dir.name if output_dir else build_run_id(request.topic)
    run_dir = output_dir or (RUNS_ROOT / run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    logger = RunLogger(run_dir, run_id)
    cost_tracker = CostTracker()
    llm = LLMRouter(config)
    cache = SQLiteCache(run_dir / "cache" / "metadata_cache.sqlite3")

    config_payload = {
        "request": request.model_dump(),
        "runtime": {
            "max_papers": config.max_papers,
            "min_verified_papers": config.min_verified_papers,
            "max_revision_iter": config.max_revision_iter,
            "offline": config.offline,
            "use_local_llm": config.use_local_llm,
            "request_timeout_sec": config.request_timeout_sec,
            "retry_count": config.retry_count,
        },
        "models": config.models.__dict__,
        "storage": {
            "run_dir": str(run_dir),
            "cuda_visible_devices": "2,3",
            "cache_policy": "All generated artifacts, Hugging Face cache, and temporary files are configured under /dataset/hoeun/stcv.",
        },
    }
    (run_dir / "config.json").write_text(json.dumps(config_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manager = ResearchManager(logger, llm, cost_tracker)
    literature = LiteratureAgent(logger, llm, cost_tracker)
    verifier = CitationVerifier(logger, llm, cost_tracker)
    summarizer = PaperSummarizer(logger, llm, cost_tracker)
    idea_generator = IdeaGenerator(logger, llm, cost_tracker)
    experiment_designer = ExperimentDesigner(logger, llm, cost_tracker)
    critic = CriticReviewer(logger, llm, cost_tracker)
    reviser = RevisionAgent(logger, llm, cost_tracker)
    writer = WriterAgent(logger, llm, cost_tracker)

    plan = manager.plan(request)
    candidates = literature.collect(plan, config, cache)
    papers, _ = verifier.verify(candidates, request.min_verified_papers)
    if len(papers) < request.min_verified_papers:
        expanded = literature.collect(
            plan.model_copy(update={"search_queries": plan.search_queries + [request.topic + " foundation benchmark"]}),
            config,
            cache,
        )
        papers, _ = verifier.verify(expanded, request.min_verified_papers)
    summaries, _ = summarizer.summarize(papers[: request.max_papers], request.topic)
    ideas = idea_generator.generate(summaries, request.topic)
    selected = sorted(ideas, key=lambda item: (item.novelty_score + item.feasibility_score, item.novelty_score), reverse=True)[0]
    experiment_plan = experiment_designer.design(selected)

    reviews = []
    revision_notes: list[str] = []
    for iteration in range(request.max_revision_iter + 1):
        review = critic.review(selected, experiment_plan, papers, iteration)
        reviews.append(review)
        if review.stop or iteration >= request.max_revision_iter:
            break
        revised = reviser.revise(selected, experiment_plan, review, iteration)
        selected = revised.idea
        experiment_plan = revised.experiment_plan
        revision_notes.extend(revised.revision_notes)

    brief = writer.write(
        request.topic,
        papers[: request.max_papers],
        summaries,
        ideas,
        selected,
        experiment_plan,
        reviews,
        revision_notes,
    )
    cost_tracker.write(run_dir / "logs" / "cost_summary.json")
    write_execution_report(run_dir, request, config, papers_count=len(papers), ideas_count=len(ideas), reviews_count=len(reviews))
    return brief, run_dir


def write_execution_report(
    run_dir: Path,
    request: UserRequest,
    config: RuntimeConfig,
    papers_count: int,
    ideas_count: int,
    reviews_count: int,
) -> None:
    cost_path = run_dir / "logs" / "cost_summary.json"
    cost = json.loads(cost_path.read_text(encoding="utf-8")) if cost_path.exists() else {}
    llm_artifacts = sorted(str(path.relative_to(run_dir)) for path in (run_dir / "artifacts" / "llm").glob("*.json"))
    llm_note = (
        "Actual local Hugging Face generation was enabled. Raw model outputs are stored under `artifacts/llm/`."
        if config.use_local_llm
        else "Local Hugging Face generation was disabled for this run."
    )
    text = f"""# Execution Report

## Run Summary
- Topic: {request.topic}
- Output directory: {run_dir}
- Verified or partially verified papers used: {papers_count}
- Generated research ideas: {ideas_count}
- Critic review rounds: {reviews_count}
- Offline mode: {config.offline}
- Local LLM enabled: {config.use_local_llm}
- Paid API usage: none

## Model Routing
- Manager/Critic/Writer: {config.models.manager_model}
- Idea/Experiment roles: {config.models.idea_model}
- Lightweight summarization role: {config.models.summarizer_model}
- Reproducible fallback: {config.models.fallback_model}

## Local LLM Evidence
- {llm_note}
- LLM artifacts: {len(llm_artifacts)}
- LLM artifact files: {llm_artifacts}

## Resource Controls
- Physical GPUs allowed by assignment: 2 and 3.
- Runtime sets `CUDA_VISIBLE_DEVICES=2,3`.
- Hugging Face cache root: `.hf_cache/` inside the repository.
- Conda environment target: `.conda/envs/stcv_hoeun` inside the repository.
- Max revision iterations: {config.max_revision_iter}
- Request timeout: {config.request_timeout_sec} seconds

## Cost and Time
```json
{json.dumps(cost, indent=2, ensure_ascii=False)}
```

## Failure Handling Notes
- Network search failures fall back to the manually curated offline seed catalog.
- Unverified or duplicate citations are written to `artifacts/rejected_papers.json`.
- If a local open-source model cannot be loaded, the event is recorded in `logs/agent_events.jsonl` with the error message.
"""
    (run_dir / "outputs" / "execution_report.md").write_text(text, encoding="utf-8")
