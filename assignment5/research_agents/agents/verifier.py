from __future__ import annotations

import time

from ..schemas import PaperCandidate, VerifiedPaper
from ..tools.text import normalize_title, paper_id
from .base import AgentBase


class CitationVerifier(AgentBase):
    name = "Citation Verifier"
    prompt_file = "verifier.md"

    def verify(self, candidates: list[PaperCandidate], min_verified: int) -> tuple[list[VerifiedPaper], list[VerifiedPaper]]:
        started = time.time()
        seen: dict[str, str] = {}
        verified: list[VerifiedPaper] = []
        rejected: list[VerifiedPaper] = []
        for candidate in candidates:
            key = normalize_title(candidate.title)
            duplicate_of = seen.get(key)
            notes: list[str] = []
            if duplicate_of:
                notes.append(f"duplicate of {duplicate_of}")
                paper = VerifiedPaper(
                    **candidate.model_dump(),
                    paper_id=paper_id(candidate.title, candidate.year),
                    verification_status="unverified",
                    verification_notes=notes,
                    duplicate_of=duplicate_of,
                )
                rejected.append(paper)
                continue
            seen[key] = paper_id(candidate.title, candidate.year)
            has_metadata = bool(candidate.title and candidate.authors and candidate.year)
            has_locator = bool(candidate.url or candidate.doi)
            if has_metadata and has_locator:
                status = "verified"
                notes.append("title, author/year metadata, and URL/DOI are present")
                if candidate.source == "offline_seed":
                    notes.append("manually curated seed citation")
            elif has_metadata:
                status = "partial"
                notes.append("metadata present but URL/DOI missing")
            else:
                status = "unverified"
                notes.append("missing required bibliographic metadata")
            paper = VerifiedPaper(
                **candidate.model_dump(),
                paper_id=paper_id(candidate.title, candidate.year),
                verification_status=status,
                verification_notes=notes,
                duplicate_of=None,
            )
            if status == "unverified":
                rejected.append(paper)
            else:
                verified.append(paper)
        selected = verified[: max(min_verified, min(len(verified), 5))]
        output_ref = self.logger.write_json("verified_papers.json", selected)
        self.logger.write_json("rejected_papers.json", rejected)
        self.timed_log(started, "paper_candidates.json", output_ref, f"{len(selected)} verified papers")
        return selected, rejected

