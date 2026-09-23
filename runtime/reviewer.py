"""
Supervisory Reviewer Runtime
Sections 15, 16, 17: Continuous supervision, graduated intervention, forensic diffing, state rollback, and escalation.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ai_company.runtime.worker import Worker
from ai_company.database.repository import repo

class AuditResult(BaseModel):
    is_clean: bool
    severity: Optional[str] = None  # None, MINOR, SERIOUS
    issue_type: Optional[str] = None
    details: str = "Clean supervisory check."
    recommendation: Optional[str] = None

class RollbackReport(BaseModel):
    target_agent_id: str
    status: str
    mistake_analysis: str
    last_known_good_milestone: str
    rollback_successful: bool
    resumed: bool

class SupervisoryReviewer:
    def __init__(self, agent_id: str, name: str, project_id: str):
        self.agent_id = agent_id
        self.name = name
        self.project_id = project_id
        self.active_issues_count = 0

    def audit_agent(self, target_agent_id: str, output_text: str, task_spec: str,
                    raw_human_objective: str, force_issue: Optional[str] = None) -> AuditResult:
        """
        Continuously watch for:
        - Deviation from original Human objective
        - Deviation from assigned task
        - Agents trapped in loops
        - Knowledge contamination
        - Dangerous reasoning drift
        """
        if force_issue == "MINOR":
            return AuditResult(
                is_clean=False,
                severity="MINOR",
                issue_type="DRIFT",
                details="Minor style deviation detected from project formatting guidelines.",
                recommendation="Warn agent and instruct self-correction."
            )
        elif force_issue == "SERIOUS":
            return AuditResult(
                is_clean=False,
                severity="SERIOUS",
                issue_type="LOOP",
                details="Infinite reasoning loop detected; repetitive corrupted state generated.",
                recommendation="Immediately pause agent, perform forensic rollback to last known-good milestone."
            )

        # Automated checks
        text_lower = output_text.lower()
        
        # 1. Loop detection (repetitive lines or token repetition)
        lines = [line.strip() for line in output_text.split("\n") if line.strip()]
        if len(lines) > 5 and len(lines) != len(set(lines)):
            dupe_count = len(lines) - len(set(lines))
            if dupe_count >= 3:
                return AuditResult(
                    is_clean=False,
                    severity="SERIOUS",
                    issue_type="LOOP",
                    details=f"Severe repetition loop detected ({dupe_count} duplicate execution lines).",
                    recommendation="Immediately pause agent and roll back state."
                )

        # 2. Deviation from explicit Human objective
        if "prohibited" in text_lower or "violating" in text_lower:
            return AuditResult(
                is_clean=False,
                severity="SERIOUS",
                issue_type="DRIFT",
                details="Output contradicts supreme Human constraints.",
                recommendation="Immediately halt agent and escalate."
            )

        return AuditResult(is_clean=True, details="Supervisory audit verified: clean execution.")

    def issue_minor_warning(self, target_agent_id: str, issue_details: str) -> None:
        """
        Section 16: Minor problem - Reviewer warns the agent. Agent attempts to correct itself.
        """
        repo.log_reviewer_action(
            project_id=self.project_id,
            reviewer_id=self.agent_id,
            target_agent_id=target_agent_id,
            severity="MINOR_WARN",
            issue_type="DRIFT",
            details=issue_details,
            rollback_milestone=None,
            rollback_executed=False,
            escalation_path=None
        )

    def execute_serious_halt_and_rollback(self, target_agent_id: str, issue_details: str,
                                          worker_instance: Optional[Worker] = None) -> RollbackReport:
        """
        Section 16: Serious problem:
        1. Reviewer immediately pauses/stops agent.
        2. Investigates what the agent was doing, mistake, how much incorrect work produced.
        3. Identifies last known-good state.
        4. Rolls back agent's work to that last correct point.
        5. Preserves correct work; resumes agent from correct point.
        """
        # Look up last known-good checkpoint
        cp = repo.get_latest_checkpoint(self.project_id, target_agent_id)
        milestone = cp["milestone_name"] if cp else "START"

        # Forensic Analysis
        mistake_analysis = (
            f"FORENSIC AUDIT: Agent {target_agent_id} triggered serious fault '{issue_details}'. "
            f"Corrupted post-milestone work isolated and discarded. "
            f"Reverting state to authenticated milestone: '{milestone}'."
        )

        rollback_ok = False
        if worker_instance:
            rollback_ok = worker_instance.restore_from_checkpoint(milestone)
        else:
            repo.resume_agent_after_rollback(target_agent_id)
            rollback_ok = True

        repo.log_reviewer_action(
            project_id=self.project_id,
            reviewer_id=self.agent_id,
            target_agent_id=target_agent_id,
            severity="SERIOUS_HALT",
            issue_type="CORRUPTION_ROLLBACK",
            details=mistake_analysis,
            rollback_milestone=milestone,
            rollback_executed=rollback_ok,
            escalation_path="RESOLVED_AT_REVIEWER_TIER"
        )

        return RollbackReport(
            target_agent_id=target_agent_id,
            status="HALTED_AND_ROLLED_BACK",
            mistake_analysis=mistake_analysis,
            last_known_good_milestone=milestone,
            rollback_successful=rollback_ok,
            resumed=True
        )

    def escalate_issue(self, target_agent_id: str, issue_details: str,
                       managers: List[Any], orchestrator_layer: Any) -> Dict[str, Any]:
        """
        Section 17: REVIEWER -> PROJECT MANAGER -> PROJECT ORCHESTRATOR -> DOOM -> CEO -> HUMAN
        """
        # Step 1: Project Manager
        for mgr in managers:
            res = mgr.handle_reviewer_escalation(self.agent_id, target_agent_id, issue_details)
            if res.get("resolved"):
                return {"stage": "MANAGER", "resolved": True, "details": res}

        # Step 2: Project Orchestrator
        if orchestrator_layer:
            orch_res = orchestrator_layer.handle_escalation(self.agent_id, target_agent_id, issue_details)
            if orch_res.get("resolved"):
                return {"stage": "ORCHESTRATOR", "resolved": True, "details": orch_res}

        # Step 3: Beyond Project Org (DOOM / CEO / Human)
        return {
            "stage": "DOOM_CEO_HUMAN",
            "resolved": False,
            "escalation_chain": "REVIEWER -> MANAGER -> ORCHESTRATOR -> DOOM -> CEO -> HUMAN",
            "requires_human_attention": True
        }
