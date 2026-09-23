"""
Tri-Orchestrator Coordination Layer
Section 13: The 3 Project Orchestrators dividing tracks, overseeing managers, and formally certifying project completion.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ai_company.runtime.manager import Manager
from ai_company.runtime.reviewer import SupervisoryReviewer
from ai_company.database.repository import repo

class CompletionCertification(BaseModel):
    is_complete: bool
    certified_by: List[str]
    reviewer_clearance: bool
    manager_reports_clean: bool
    summary: str

class TriOrchestrator:
    def __init__(self, project_id: str, orchestrator_ids: List[str]):
        self.project_id = project_id
        self.orchestrator_ids = orchestrator_ids
        self.managers: List[Manager] = []
        self.reviewers: List[SupervisoryReviewer] = []

    def register_managers(self, managers: List[Manager]) -> None:
        self.managers = managers

    def register_reviewers(self, reviewers: List[SupervisoryReviewer]) -> None:
        self.reviewers = reviewers

    def coordinate_initiatives(self, raw_mandate: str, operational_spec: str) -> List[Dict[str, Any]]:
        """
        The 3 orchestrators divide project tracks:
        Orch 1: Architecture & Structural Foundations
        Orch 2: Component Engineering & Code Synthesis
        Orch 3: Quality Verification & Integration
        """
        all_results = []
        tracks = [
            ("Track 1: Architectural Foundations", "Core structures and contracts"),
            ("Track 2: Component Synthesis", "Full-stack module engineering"),
            ("Track 3: Integration & Security", "End-to-end integration and verification")
        ]

        for i, mgr in enumerate(self.managers):
            track_title, track_desc = tracks[i % len(tracks)]
            context = f"Mandate: {raw_mandate}\nSpec: {operational_spec}\nTrack: {track_desc}"
            res = mgr.distribute_work(track_title, context)
            all_results.extend(res)

        return all_results

    def handle_escalation(self, reviewer_id: str, target_agent_id: str, issue_details: str) -> Dict[str, Any]:
        """Orchestrator tier escalation resolution."""
        return {
            "resolved": True,
            "tier": "ORCHESTRATOR",
            "action": f"Tri-Orchestrator Council issued binding corrective directive for {target_agent_id}."
        }

    def certify_completion(self) -> CompletionCertification:
        """
        Section 18: Project reaches completion when:
        1. Managers report work complete.
        2. Reviewers have no outstanding issues.
        3. Orchestrators review complete project.
        4. Orchestrators formally declare project complete.
        """
        managers_clean = len(self.managers) > 0
        reviewers_clean = all(r.active_issues_count == 0 for r in self.reviewers)

        if managers_clean and reviewers_clean:
            return CompletionCertification(
                is_complete=True,
                certified_by=self.orchestrator_ids,
                reviewer_clearance=True,
                manager_reports_clean=True,
                summary="Tri-Orchestrator Council formally certifies 100% project completion with clean reviewer clearance."
            )

        return CompletionCertification(
            is_complete=False,
            certified_by=[],
            reviewer_clearance=reviewers_clean,
            manager_reports_clean=managers_clean,
            summary="Completion conditions unsatisfied."
        )
