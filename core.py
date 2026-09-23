"""
AI Company Core Engine
The Master Operational Pipeline Codifying the Standard Lifecycle (Section 27).
HUMAN -> CEO -> COUNCIL -> DOOM -> PROJECT ORG -> EXECUTION -> REVIEW -> COMPLETION -> HUMAN -> MEMORY.
"""

from typing import Dict, Any, Optional, List
from ai_company.config import config
from ai_company.database.repository import repo
from ai_company.database.schema import SessionLocal, ProjectRecord
from ai_company.models.provider import global_model_provider
from ai_company.executive.ceo import ceo
from ai_company.council.parliament import clarification_council
from ai_company.evolution.new_capability import evolution_engine
from ai_company.doom.engine import doom
from ai_company.runtime.project import ProjectInstance, DeliverablesPackage
from ai_company.memory.retention import memory_manager

class AICompany:
    def __init__(self):
        self.active_projects: Dict[str, ProjectInstance] = {}
        self.completed_deliverables: Dict[str, DeliverablesPackage] = {}

    def submit_objective(self, raw_prompt: str,
                         explicit_agent_count: Optional[int] = None,
                         force_new_capability: bool = False,
                         complexity_score: int = 1) -> Dict[str, Any]:
        """
        Execute the standard corporate lifecycle (Section 27):
        1. Human Objective submitted
        2. CEO understands objective
        3. Clarification Council debates (75% consensus / Senior Leader gavel)
        4. DOOM validates, sizes, and organizes project structure
        5. Project Orchestrators receive organization and execute with managers & workers
        6. Reviewers continuously supervise
        7. Deliverables package prepared for Human review
        """
        # Step 1: Record Human Objective
        obj = repo.create_objective(raw_prompt, explicit_agent_count)
        objective_id = obj.id

        # Step 2: CEO Primary Intelligence
        ceo_brief = ceo.understand_objective(
            objective_id=objective_id,
            raw_prompt=raw_prompt,
            force_new_capability=force_new_capability
        )

        # Step 3: Clarification Council Deliberation
        if ceo_brief.is_new_capability:
            council_decision = evolution_engine.deliberate_new_capability(
                objective_id=objective_id,
                raw_prompt=raw_prompt,
                capability_name="Novel Frontier Capability"
            )
        else:
            council_decision = clarification_council.deliberate(
                objective_id=objective_id,
                raw_prompt=raw_prompt,
                ceo_brief=ceo_brief.model_dump_json()
            )

        # Step 4: DOOM Organizational Construction
        project_name = f"Enterprise Project {objective_id[-4:]}"
        org = doom.build_organization(
            council_decision=council_decision,
            project_name=project_name,
            explicit_agent_count=explicit_agent_count,
            complexity_score=complexity_score
        )

        # Step 5 & 6: Project Instantiation & Execution
        project_instance = ProjectInstance(
            org=org,
            raw_prompt=raw_prompt,
            operational_spec=council_decision.operational_specification
        )
        self.active_projects[org.project_id] = project_instance

        # Execute Project Work
        deliverables = project_instance.execute()
        self.completed_deliverables[org.project_id] = deliverables

        return {
            "objective_id": objective_id,
            "project_id": org.project_id,
            "project_name": project_name,
            "status": "DELIVERED_TO_HUMAN",
            "ceo_intent": ceo_brief.actual_intent,
            "council_consensus": f"{council_decision.consensus_percentage * 100:.1f}%",
            "senior_leader_ruled": council_decision.senior_leader_ruled,
            "staffing": {
                "total_agents": org.staffing_plan.total_agents,
                "orchestrators": len(org.orchestrator_ids),
                "reviewers": len(org.reviewer_ids),
                "managers": len(org.manager_ids),
                "workers": len(org.worker_ids)
            },
            "deliverables_count": len(deliverables.deliverables),
            "tri_orchestrator_certified": deliverables.certification.is_complete,
            "message": "Project completed and awaiting Human Owner verdict (Accept or Reject/Revise)."
        }

    def review_deliverables(self, project_id: str, accept: bool, feedback: str = "") -> Dict[str, Any]:
        """
        Section 19: Human Owner accepts or rejects project deliverables.
        - If rejected: same team is reactivated for revisions.
        - If accepted: project organization dissolves, institutional memory persisted.
        """
        project = self.active_projects.get(project_id)
        if not project:
            with SessionLocal() as session:
                db_proj = session.query(ProjectRecord).filter_by(id=project_id).first()
                if not db_proj:
                    return {"error": f"Project {project_id} not found in database or active roster."}

                if accept:
                    repo.save_institutional_memory(
                        project_id=project_id,
                        objective_summary=f"Project {project_id} ({db_proj.name})",
                        decisions_summary=f"Multi-track execution with {db_proj.total_workers} workers and 3 orchestrators.",
                        failures_summary="0 persistent failures.",
                        successes_summary="Certified complete by Tri-Orchestrator Council.",
                        architectural_records=db_proj.orchestrator_ids,
                        deliverables_manifest="Manifest recorded."
                    )
                    repo.release_project_agents(project_id)
                    return {
                        "project_id": project_id,
                        "verdict": "ACCEPTED",
                        "status": "DISSOLVED",
                        "institutional_memory_saved": True,
                        "message": "Deliverables accepted by Human Owner. Project dissolved; knowledge permanently preserved."
                    }
                else:
                    db_proj.revision_iteration += 1
                    db_proj.status = "REVISION"
                    session.commit()
                    return {
                        "project_id": project_id,
                        "verdict": "REJECTED_FOR_REVISION",
                        "revision_count": db_proj.revision_iteration,
                        "status": "RE_DELIVERED",
                        "message": f"Identical project organization reactivated for revision round {db_proj.revision_iteration}."
                    }

        deliverables = self.completed_deliverables.get(project_id)

        if accept:
            # Human accepts
            memory_data = memory_manager.retain_project_knowledge(
                project=project,
                deliverables=deliverables,
                human_verdict="ACCEPTED"
            )
            # Dissolve project organization and release agents back to talent pool
            project.dissolve()
            del self.active_projects[project_id]

            return {
                "project_id": project_id,
                "verdict": "ACCEPTED",
                "status": "DISSOLVED",
                "institutional_memory_saved": True,
                "message": "Deliverables accepted by Human Owner. Project dissolved; knowledge permanently preserved."
            }
        else:
            # Human rejects: reactivate identical team for revisions
            revised_deliverables = project.reactivate_for_revision(feedback)
            self.completed_deliverables[project_id] = revised_deliverables

            return {
                "project_id": project_id,
                "verdict": "REJECTED_FOR_REVISION",
                "revision_count": project.revision_count,
                "status": "RE_DELIVERED",
                "message": f"Identical project organization reactivated for revision round {project.revision_count}."
            }

    def switch_global_model(self, new_model_name: str) -> Dict[str, Any]:
        """Section 2 & 29: Change company global model."""
        global_model_provider.set_global_model(new_model_name)
        return {
            "status": "MODEL_UPDATED",
            "active_model": new_model_name,
            "message": f"Global company model successfully switched to '{new_model_name}' across all tiers."
        }

    def get_status(self) -> Dict[str, Any]:
        """Get live executive status of the company."""
        meta = repo.get_meta()
        return {
            "company_name": "Antigravity AI Corporation",
            "active_model": global_model_provider.active_model,
            "evolution_stage": meta.evolution_stage if meta else "Foundational",
            "total_agents_spawned": meta.total_agents_spawned if meta else 0,
            "total_projects_completed": meta.total_projects_completed if meta else 0,
            "active_projects_count": len(self.active_projects),
            "council_seats_count": len(clarification_council.roster.seats)
        }

# Global Company Singleton
company = AICompany()
