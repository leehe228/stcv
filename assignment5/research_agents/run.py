from __future__ import annotations

import argparse
from pathlib import Path

from .config import RUNS_ROOT, RuntimeConfig, configure_local_storage
from .schemas import UserRequest
from .workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="STCV Assignment 5 multi-agent research automation CLI")
    parser.add_argument("--topic", required=True, help="Natural-language research topic")
    parser.add_argument("--constraint", action="append", default=[], help="Optional constraint; can be repeated")
    parser.add_argument("--max-papers", type=int, default=8)
    parser.add_argument("--min-verified-papers", type=int, default=5)
    parser.add_argument("--max-revision-iter", type=int, default=2)
    parser.add_argument("--output", type=Path, default=None, help="Output run directory")
    parser.add_argument("--offline", action="store_true", help="Use only the curated offline paper catalog")
    parser.add_argument("--use-local-llm", action="store_true", help="Try local Hugging Face Transformers inference")
    parser.add_argument("--timeout", type=float, default=8.0)
    return parser.parse_args()


def main() -> None:
    configure_local_storage()
    args = parse_args()
    request = UserRequest(
        topic=args.topic,
        constraints=args.constraint,
        max_papers=args.max_papers,
        min_verified_papers=args.min_verified_papers,
        max_revision_iter=args.max_revision_iter,
    )
    config = RuntimeConfig(
        max_papers=args.max_papers,
        min_verified_papers=args.min_verified_papers,
        max_revision_iter=args.max_revision_iter,
        offline=args.offline,
        use_local_llm=args.use_local_llm,
        request_timeout_sec=args.timeout,
    )
    output = args.output or (RUNS_ROOT / "latest")
    brief, run_dir = run_workflow(request, config, output)
    print(f"Run complete: {run_dir}")
    print(f"Research brief: {run_dir / 'outputs' / 'research_brief.md'}")
    print(f"References: {len(brief.references)}")


if __name__ == "__main__":
    main()

