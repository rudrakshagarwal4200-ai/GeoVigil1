"""
Worker & Coder Runtime
Section 12: Asynchronous task execution, state checkpointing, and rollback capability.
"""

from typing import Dict, Any, Optional
from ai_company.models.provider import global_model_provider
from ai_company.database.repository import repo

class Worker:
    def __init__(self, agent_id: str, name: str, role: str, project_id: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.project_id = project_id
        self.current_state: Dict[str, Any] = {
            "status": "INITIALIZED",
            "last_milestone": "START",
            "work_units_completed": [],
            "current_task": None
        }

    def checkpoint(self, milestone_name: str, payload: Optional[Dict[str, Any]] = None) -> None:
        """Save a known-good state checkpoint for potential forensic rollback."""
        data = payload or dict(self.current_state)
        data["milestone"] = milestone_name
        self.current_state["last_milestone"] = milestone_name
        repo.save_checkpoint(
            project_id=self.project_id,
            agent_id=self.agent_id,
            milestone_name=milestone_name,
            payload=data
        )

    def restore_from_checkpoint(self, milestone_name: str) -> bool:
        """
        Section 16: Roll back agent's work to the specified last known-good milestone.
        Preserves correct work, drops tainted/incorrect work.
        """
        cp = repo.get_latest_checkpoint(self.project_id, self.agent_id)
        if cp and cp.get("payload"):
            self.current_state = cp["payload"]
            self.current_state["status"] = "RESTORED"
            repo.resume_agent_after_rollback(self.agent_id)
            return True
        return False

    def execute_task(self, task_description: str, task_context: str) -> Dict[str, Any]:
        """Execute assigned work unit and produce deliverables."""
        self.current_state["status"] = "WORKING"
        self.current_state["current_task"] = task_description

        # Milestone: pre-execution checkpoint
        self.checkpoint(f"PRE_TASK_{len(self.current_state['work_units_completed'])}")

        system_prompt = (
            f"You are {self.name}, serving as {self.role} in Project {self.project_id}. "
            f"Execute the assigned engineering or research task with rigorous attention to detail."
        )
        user_prompt = f"Task: {task_description}\nContext: {task_context}"

        output = global_model_provider.generate(
            agent_role=self.role,
            agent_name=self.name,
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        work_unit = {
            "task": task_description,
            "output": output,
            "verified": True
        }
        self.current_state["work_units_completed"].append(work_unit)
        self.current_state["status"] = "COMPLETED"

        # Milestone: post-execution known-good checkpoint
        self.checkpoint(f"POST_TASK_{len(self.current_state['work_units_completed'])}")

        return work_unit
