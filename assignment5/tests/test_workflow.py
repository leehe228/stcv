from pathlib import Path

from assignment5.research_agents.config import RuntimeConfig
from assignment5.research_agents.schemas import UserRequest
from assignment5.research_agents.workflow import run_workflow


def test_user_request_rejects_empty_topic():
    try:
        UserRequest(topic="   ")
    except ValueError as exc:
        assert "topic" in str(exc)
    else:
        raise AssertionError("empty topic should fail validation")


def test_end_to_end_offline_workflow():
    repo = Path(__file__).resolve().parents[2]
    request = UserRequest(
        topic="vision-language models for robot manipulation under distribution shift",
        max_papers=8,
        min_verified_papers=5,
        max_revision_iter=2,
    )
    config = RuntimeConfig(max_papers=8, min_verified_papers=5, max_revision_iter=2, offline=True)
    out = repo / ".tmp" / "pytest_offline_workflow"
    brief, run_dir = run_workflow(request, config, out)

    assert run_dir == out
    assert len(brief.references) >= 5
    assert (run_dir / "outputs" / "research_brief.md").exists()
    assert (run_dir / "logs" / "agent_events.jsonl").exists()
    assert (run_dir / "logs" / "cost_summary.json").exists()
    text = (run_dir / "outputs" / "research_brief.md").read_text(encoding="utf-8")
    for section in [
        "## Background",
        "## Related Work",
        "## Proposed Idea",
        "## Experiment Plan",
        "## Reviewer Critique and Revisions",
        "## Limitations",
        "## References",
    ]:
        assert section in text
    assert "Offline-first validation path" in text
