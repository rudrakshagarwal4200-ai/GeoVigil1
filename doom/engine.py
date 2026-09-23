"""
DOOM: The Company's Organizational Engine
Sections 8, 9, 10: Dynamic project structure builder, agent synthesizer, and exclusivity enforcer.
"""

import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ai_company.config import config
from ai_company.doom.staffing import StaffingCalculator, StaffingPlan
from ai_company.council.parliament import CouncilDecision
from ai_company.models.provider import global_model_provider
from ai_company.database.repository import repo

class BuiltProjectOrganization(BaseModel):
    project_id: str
    project_name: str
    objective_id: str
    staffing_plan: StaffingPlan
    orchestrator_ids: List[str]
    reviewer_ids: List[str]
    manager_ids: List[str]
    worker_ids: List[str]
    status: str = "INITIALIZED"

class DOOM:
    def __init__(self, agent_id: str = "DOOM-CORE", name: str = "DOOM Organizational Engine"):
        self.agent_id = agent_id
        self.name = name
        self.role = "DOOM"
        repo.register_agent(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            tier="DOOM",
            project_id=None
        )

    def build_organization(self, council_decision: CouncilDecision,
                           project_name: str,
                           explicit_agent_count: Optional[int] = None,
                           complexity_score: int = 1) -> BuiltProjectOrganization:
        """
        Build the complete temporary project corporation:
        - Determines headcount (min 10, no upper limit)
        - Synthesizes 3 Orchestrators
        - Allocates Reviewers (1:10 ratio)
        - Assigns Managers and Workers
        - Enforces single-project exclusivity
        """
        project_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"

        # Calculate staffing adhering strictly to rules
        staffing = StaffingCalculator.calculate(
            explicit_count=explicit_agent_count,
            complexity_score=complexity_score
        )

        orchestrator_ids = []
        reviewer_ids = []
        manager_ids = []
        worker_ids = []

        # 1. Synthesize 3 Orchestrators (Section 12, 13)
        orchestrator_roles = [
            ("Orchestrator Alpha", "Architecture & Strategic Alignment"),
            ("Orchestrator Beta", "Technical Execution & Systems Integration"),
            ("Orchestrator Gamma", "Verification, Reviewer Liaison & Quality")
        ]
        for i, (orch_name, orch_role) in enumerate(orchestrator_roles, start=1):
            agent_id = f"{project_id}-ORCH-{i}"
            repo.register_agent(
                agent_id=agent_id,
                name=f"{project_name} {orch_name}",
                role=orch_role,
                tier="ORCHESTRATOR",
                project_id=project_id
            )
            orchestrator_ids.append(agent_id)

        # 2. Synthesize Reviewers (Section 15: 1 per 10 agents ratio)
        for i in range(1, staffing.reviewer_count + 1):
            agent_id = f"{project_id}-REV-{i}"
            repo.register_agent(
                agent_id=agent_id,
                name=f"Supervisory Reviewer {i}",
                role="Continuous Supervisory Oversight & Rollback Sentinel",
                tier="REVIEWER",
                project_id=project_id
            )
            reviewer_ids.append(agent_id)

        # 3. Synthesize Managers (Section 14)
        for i in range(1, staffing.manager_count + 1):
            agent_id = f"{project_id}-MGR-{i}"
            repo.register_agent(
                agent_id=agent_id,
                name=f"Project Manager {i}",
                role=f"Workstream Manager (Track {i})",
                tier="MANAGER",
                project_id=project_id
            )
            manager_ids.append(agent_id)

        # 4. Synthesize Workers / Coders (Section 12)
        for i in range(1, staffing.worker_count + 1):
            agent_id = f"{project_id}-WRK-{i}"
            repo.register_agent(
                agent_id=agent_id,
                name=f"Technical Specialist {i}",
                role=f"Full-Stack Specialist & Coder {i}",
                tier="WORKER",
                project_id=project_id
            )
            worker_ids.append(agent_id)

        # Persist project structure in database
        repo.create_project_org(
            project_id=project_id,
            name=project_name,
            objective_id=council_decision.objective_id,
            total_agents=staffing.total_agents,
            total_reviewers=staffing.reviewer_count,
            total_managers=staffing.manager_count,
            total_workers=staffing.worker_count,
            orchestrator_ids=orchestrator_ids
        )

        repo.update_objective_status(council_decision.objective_id, "ORGANIZING")

        return BuiltProjectOrganization(
            project_id=project_id,
            project_name=project_name,
            objective_id=council_decision.objective_id,
            staffing_plan=staffing,
            orchestrator_ids=orchestrator_ids,
            reviewer_ids=reviewer_ids,
            manager_ids=manager_ids,
            worker_ids=worker_ids,
            status="ORGANIZED"
        )

# Global DOOM instance
doom = DOOM()
