"""
Isolated Project Corporation Runtime
Sections 10, 11, 18, 19, 21: Project lifecycle, isolated execution, revision loops, and dissolution.
"""

from typing import List, Dict, Any, Optional
import json
from pydantic import BaseModel
from ai_company.doom.engine import BuiltProjectOrganization
from ai_company.runtime.orchestrator import TriOrchestrator, CompletionCertification
from ai_company.runtime.manager import Manager
from ai_company.runtime.worker import Worker
from ai_company.runtime.reviewer import SupervisoryReviewer
from ai_company.database.repository import repo

class DeliverablesPackage(BaseModel):
    project_id: str
    project_name: str
    objective_id: str
    raw_prompt: str
    operational_spec: str
    revision_iteration: int
    deliverables: List[Dict[str, Any]]
    certification: CompletionCertification
    status: str

class ProjectInstance:
    def __init__(self, org: BuiltProjectOrganization, raw_prompt: str, operational_spec: str):
        self.project_id = org.project_id
        self.name = org.project_name
        self.objective_id = org.objective_id
        self.raw_prompt = raw_prompt
        self.operational_spec = operational_spec
        self.revision_count = 0
        self.status = "INITIALIZED"

        # Instantiate 3 Orchestrators
        self.tri_orchestrator = TriOrchestrator(
            project_id=self.project_id,
            orchestrator_ids=org.orchestrator_ids
        )

        # Instantiate Reviewers
        self.reviewers: List[SupervisoryReviewer] = [
            SupervisoryReviewer(agent_id=r_id, name=f"Reviewer-{i}", project_id=self.project_id)
            for i, r_id in enumerate(org.reviewer_ids, start=1)
        ]

        # Instantiate Managers
        self.managers: List[Manager] = [
            Manager(agent_id=m_id, name=f"Manager-{i}", role=f"Track Manager {i}", project_id=self.project_id)
            for i, m_id in enumerate(org.manager_ids, start=1)
        ]

        # Instantiate Workers
        self.workers: List[Worker] = [
            Worker(agent_id=w_id, name=f"Worker-{i}", role="Full-Stack Technical Specialist", project_id=self.project_id)
            for i, w_id in enumerate(org.worker_ids, start=1)
        ]

        # Wire up hierarchy: distribute workers evenly among managers
        for i, worker in enumerate(self.workers):
            target_mgr = self.managers[i % len(self.managers)]
            target_mgr.assign_worker(worker)

        # Connect managers and reviewers to orchestrator layer
        self.tri_orchestrator.register_managers(self.managers)
        self.tri_orchestrator.register_reviewers(self.reviewers)

        self.last_deliverables: Optional[DeliverablesPackage] = None

    def execute(self) -> DeliverablesPackage:
        """
        Execute project work:
        1. Orchestrators divide work to managers
        2. Managers distribute to workers
        3. Workers execute and checkpoint
        4. Reviewers audit outputs
        5. Orchestrators certify completion
        """
        self.status = "EXECUTING"
        repo.update_objective_status(self.objective_id, "EXECUTING")

        # Step 1 & 2: Execution
        raw_outputs = self.tri_orchestrator.coordinate_initiatives(self.raw_prompt, self.operational_spec)

        # Step 3: Reviewer continuous audit
        self.status = "REVIEWING"
        for output in raw_outputs:
            for reviewer in self.reviewers:
                audit = reviewer.audit_agent(
                    target_agent_id="SYSTEM",
                    output_text=output.get("output", ""),
                    task_spec=output.get("task", ""),
                    raw_human_objective=self.raw_prompt
                )
                if not audit.is_clean:
                    if audit.severity == "MINOR":
                        reviewer.issue_minor_warning("SYSTEM", audit.details)
                    else:
                        reviewer.execute_serious_halt_and_rollback("SYSTEM", audit.details)

        # Step 4: Formal Certification
        cert = self.tri_orchestrator.certify_completion()
        self.status = "DELIVERED"
        repo.update_objective_status(self.objective_id, "DELIVERED")

        self.last_deliverables = DeliverablesPackage(
            project_id=self.project_id,
            project_name=self.name,
            objective_id=self.objective_id,
            raw_prompt=self.raw_prompt,
            operational_spec=self.operational_spec,
            revision_iteration=self.revision_count,
            deliverables=raw_outputs,
            certification=cert,
            status=self.status
        )
        return self.last_deliverables

    def reactivate_for_revision(self, human_feedback: str) -> DeliverablesPackage:
        """
        Section 19: If Human rejects output:
        The SAME project team is reactivated for revisions.
        Indefinite revision support until Human is satisfied.
        """
        self.revision_count += 1
        self.status = "REVISION"
        repo.update_objective_status(self.objective_id, f"REVISION_ROUND_{self.revision_count}")

        # Update spec with Human revision feedback
        revision_spec = (
            f"{self.operational_spec}\n\n"
            f"### REVISION DIRECTIVE {self.revision_count} (From Human Owner):\n"
            f"{human_feedback}"
        )
        self.operational_spec = revision_spec

        # Re-execute with identical team
        return self.execute()

    def dissolve(self) -> None:
        """
        Section 18 & 20: Once Human accepts:
        1. Project organization dissolves.
        2. Agents return to general company workforce.
        3. History preserved in institutional memory.
        """
        self.status = "DISSOLVED"
        repo.release_project_agents(self.project_id)
