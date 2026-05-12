from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class UserRequest(BaseModel):
    topic: str
    constraints: list[str] = Field(default_factory=list)
    target_domain: str | None = None
    max_papers: int = 8
    min_verified_papers: int = 5
    max_revision_iter: int = 2

    @field_validator("topic")
    @classmethod
    def topic_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("topic must not be empty")
        return value.strip()


class ResearchPlan(BaseModel):
    topic: str
    search_queries: list[str]
    constraints: list[str] = Field(default_factory=list)
    workflow: list[str]
    stopping_rule: str


class PaperCandidate(BaseModel):
    title: str
    authors: list[str]
    year: int | None = None
    venue: str | None = None
    url: str | None = None
    doi: str | None = None
    source: str
    abstract: str | None = None


class VerifiedPaper(PaperCandidate):
    paper_id: str
    verification_status: Literal["verified", "partial", "unverified"]
    verification_notes: list[str] = Field(default_factory=list)
    duplicate_of: str | None = None


class PaperSummary(BaseModel):
    paper_id: str
    title: str
    core_claim: str
    method: str
    experiments: str
    limitations: str
    relevance_to_topic: str


class ResearchIdea(BaseModel):
    title: str
    hypothesis: str
    novelty: str
    feasibility: str
    expected_contribution: str
    related_paper_ids: list[str]
    novelty_score: int = Field(ge=1, le=5)
    feasibility_score: int = Field(ge=1, le=5)


class ExperimentPlan(BaseModel):
    idea_title: str
    datasets: list[str]
    baselines: list[str]
    metrics: list[str]
    ablations: list[str]
    expected_failure_cases: list[str]
    risks: list[str]
    implementation_notes: list[str] = Field(default_factory=list)


class ReviewReport(BaseModel):
    overall_score: int = Field(ge=1, le=5)
    novelty_issues: list[str]
    feasibility_issues: list[str]
    experiment_issues: list[str]
    citation_issues: list[str]
    required_revisions: list[str]
    stop: bool = False


class RevisedPlan(BaseModel):
    idea: ResearchIdea
    experiment_plan: ExperimentPlan
    revision_notes: list[str]
    addressed_revisions: list[str]


class ResearchBrief(BaseModel):
    markdown: str
    references: list[VerifiedPaper]


class AgentLogEvent(BaseModel):
    run_id: str
    step_index: int
    agent_name: str
    model: str
    prompt_path: str
    input_ref: str
    output_ref: str
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    token_usage: dict[str, int] | None = None
    elapsed_sec: float
    error: str | None = None

