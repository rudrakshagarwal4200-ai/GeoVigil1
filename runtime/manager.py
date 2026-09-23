"""
Project Manager Runtime
Section 14: Work distribution, worker supervision, and first-tier reviewer escalation handling.
"""

from typing import List, Dict, Any, Optional
from ai_company.runtime.worker import Worker
from ai_company.database.repository import repo

class Manager:
    def __init__(self, agent_id: str, name: str, role: str, project_id: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.project_id = project_id
        self.assigned_workers: List[Worker] = []

    def assign_worker(self, worker: Worker) -> None:
        self.assigned_workers.append(worker)

    def distribute_work(self, initiative_title: str, context: str) -> List[Dict[str, Any]]:
        """Decompose higher-level initiative into atomic worker tasks."""
        results = []
        for i, worker in enumerate(self.assigned_workers, start=1):
            subtask = f"Subtask {i} for {initiative_title}: Implementation & verification of component {i}"
            res = worker.execute_task(subtask, context)
            results.append(res)
        return results

    def handle_reviewer_escalation(self, reviewer_id: str, target_agent_id: str, issue_details: str) -> Dict[str, Any]:
        """
        Section 14 & 17: Project Manager attempts to resolve escalated reviewer issue.
        If worker belongs to this manager, manager instructs rollback to last known-good milestone.
        If unable to resolve, escalates to Project Orchestrator.
        """
        target_worker = next((w for w in self.assigned_workers if w.agent_id == target_agent_id), None)
        if target_worker:
            # Manager resolves by executing state rollback to last known-good milestone
            last_milestone = target_worker.current_state.get("last_milestone", "START")
            restored = target_worker.restore_from_checkpoint(last_milestone)
            return {
                "resolved": restored,
                "handler": self.agent_id,
                "action": f"Rollback executed on {target_agent_id} to {last_milestone}",
                "escalate_to_orchestrator": not restored
            }
        
        # If worker is not under this manager, escalate to orchestrator
        return {
            "resolved": False,
            "handler": self.agent_id,
            "action": "Worker outside manager jurisdiction",
            "escalate_to_orchestrator": True
        }
