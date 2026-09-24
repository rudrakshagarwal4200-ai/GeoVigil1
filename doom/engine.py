"""
DOOM: The Company's Organizational Engine
Sections 8, 9, 10, 12, 13, 15: Dynamic project structure builder, agent synthesizer,
exclusivity enforcer, and trained Master of the 37-Agent Website Agency Taxonomy.
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ai_company.config import config
from ai_company.doom.staffing import StaffingCalculator, StaffingPlan
from ai_company.doom.knowledge import WebsiteAgencyKnowledge
from ai_company.doom.brain import DOOMArchitecturalBrain, WebsiteBlueprint
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
    blueprint: Optional[WebsiteBlueprint] = None

class DOOM:
    def __init__(self, agent_id: str = "DOOM-CORE", name: str = "DOOM Organizational Engine"):
        self.agent_id = agent_id
        self.name = name
        self.role = "DOOM"
        self.trained_knowledge_path = "e:/agy/ai_company/doom/doom_knowledge.json"
        repo.register_agent(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            tier="DOOM",
            project_id=None
        )

    def is_trained(self) -> bool:
        """Check if DOOM has successfully internalized the website agency training."""
        return os.path.exists(self.trained_knowledge_path)

    def get_trained_metadata(self) -> Optional[Dict[str, Any]]:
        """Retrieve the persisted training metadata and weights."""
        if not self.is_trained():
            return None
        with open(self.trained_knowledge_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_organization(self, council_decision: CouncilDecision,
                           project_name: str,
                           explicit_agent_count: Optional[int] = None,
                           complexity_score: int = 1) -> BuiltProjectOrganization:
        """
        Build the complete temporary project corporation:
        - Determines headcount (min 10, no upper limit)
        - Synthesizes 3 Orchestrators
        - Allocates Reviewers (1:10 ratio)
        - Assigns Managers and Workers using specialized 37-agent agency roles
        - Enforces single-project exclusivity
        """
        project_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"

        # Safely resolve objective text from council decision
        objective_text = (
            getattr(council_decision, "operational_specification", None)
            or getattr(council_decision, "objective_text", "")
            or project_name
        )

        # Detect cognitive focus (Rule 27: Cognitive Role Elasticity)
        is_thinker_focused = any(w in objective_text.lower() for w in [
            "idea", "think", "ideat", "brainstorm", "concept", "philosophy", "strategy", "vision", "innovat", "hypothes"
        ])
        focus = "PURE_THINKER" if is_thinker_focused else "HYBRID"

        # Calculate staffing adhering strictly to rules
        staffing = StaffingCalculator.calculate(
            explicit_count=explicit_agent_count,
            complexity_score=complexity_score,
            archetype_focus=focus
        )

        # Generate specialized website agency & cognitive blueprint
        blueprint = DOOMArchitecturalBrain.synthesize_blueprint(
            project_name=project_name,
            objective_text=objective_text,
            target_headcount=staffing.total_agents
        )

        orchestrator_ids = []
        reviewer_ids = []
        manager_ids = []
        worker_ids = []

        # Allocate agents using the specialized blueprint roles (zero generic roles!)
        orch_idx = 1
        rev_idx = 1
        mgr_idx = 1
        wrk_idx = 1

        for role_assignment in blueprint.assigned_roles:
            tier = role_assignment["tier"]
            role_name = role_assignment["name"]
            role_desc = role_assignment["description"]

            if tier == "ORCHESTRATOR":
                agent_id = f"{project_id}-ORCH-{orch_idx}"
                orch_idx += 1
                orchestrator_ids.append(agent_id)
            elif tier == "REVIEWER":
                agent_id = f"{project_id}-REV-{rev_idx}"
                rev_idx += 1
                reviewer_ids.append(agent_id)
            elif tier == "MANAGER":
                agent_id = f"{project_id}-MGR-{mgr_idx}"
                mgr_idx += 1
                manager_ids.append(agent_id)
            else:
                agent_id = f"{project_id}-WRK-{wrk_idx}"
                wrk_idx += 1
                worker_ids.append(agent_id)

            repo.register_agent(
                agent_id=agent_id,
                name=f"{project_name} {role_name}",
                role=f"{role_name} — {role_desc}",
                tier=tier,
                project_id=project_id
            )

        # Persist project structure in database
        repo.create_project_org(
            project_id=project_id,
            name=project_name,
            objective_id=council_decision.objective_id,
            total_agents=staffing.total_agents,
            total_reviewers=len(reviewer_ids),
            total_managers=len(manager_ids),
            total_workers=len(worker_ids),
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
            status="ORGANIZED",
            blueprint=blueprint
        )

# Global DOOM instance
doom = DOOM()
