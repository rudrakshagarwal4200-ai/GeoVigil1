"""
Database Repository for AI Company
Providing thread-safe helper operations for persistence, state transitions, and audit records.
"""

from typing import List, Optional, Dict, Any
import json
import uuid
from sqlalchemy.orm import Session
from ai_company.database.schema import (
    SessionLocal, init_db, CompanyMeta, HumanObjective, CEOAnalysis,
    CouncilSession, CouncilDebateTurn, AgentRecord, ProjectRecord,
    StateCheckpointRecord, ReviewerLogRecord, InstitutionalMemoryRecord
)

class CompanyRepository:
    def __init__(self):
        init_db()

    def get_meta(self) -> CompanyMeta:
        with SessionLocal() as session:
            meta = session.query(CompanyMeta).first()
            return meta

    def update_global_model(self, new_model_name: str) -> None:
        """Section 2 & 29: Propagate new model to company metadata and all existing agents."""
        with SessionLocal() as session:
            meta = session.query(CompanyMeta).first()
            if meta:
                meta.active_model = new_model_name
            # Update all agents
            session.query(AgentRecord).update({"model_name": new_model_name})
            session.commit()

    def create_objective(self, raw_prompt: str, explicit_agent_count: Optional[int] = None) -> HumanObjective:
        obj_id = f"OBJ-{uuid.uuid4().hex[:8].upper()}"
        with SessionLocal() as session:
            obj = HumanObjective(
                id=obj_id,
                raw_prompt=raw_prompt,
                explicit_agent_count=explicit_agent_count,
                status="SUBMITTED"
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def update_objective_status(self, objective_id: str, new_status: str) -> None:
        with SessionLocal() as session:
            obj = session.query(HumanObjective).filter_by(id=objective_id).first()
            if obj:
                obj.status = new_status
                session.commit()

    def save_ceo_analysis(self, objective_id: str, analysis_data: Dict[str, Any]) -> CEOAnalysis:
        analysis_id = f"CEO-{uuid.uuid4().hex[:8].upper()}"
        with SessionLocal() as session:
            analysis = CEOAnalysis(
                id=analysis_id,
                objective_id=objective_id,
                actual_intent=analysis_data.get("actual_intent", ""),
                significance=analysis_data.get("significance", ""),
                implications=analysis_data.get("implications", ""),
                success_criteria=analysis_data.get("success_criteria", ""),
                required_capabilities=analysis_data.get("required_capabilities", ""),
                is_new_capability=analysis_data.get("is_new_capability", False)
            )
            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            return analysis

    def create_council_session(self, objective_id: str) -> CouncilSession:
        session_id = f"CS-{uuid.uuid4().hex[:8].upper()}"
        with SessionLocal() as session:
            c_session = CouncilSession(
                id=session_id,
                objective_id=objective_id,
                rounds_count=0,
                consensus_percentage=0.0,
                consensus_reached=False,
                senior_leader_ruled=False
            )
            session.add(c_session)
            session.commit()
            session.refresh(c_session)
            return c_session

    def record_debate_turn(self, session_id: str, round_num: int, seat_id: int,
                           seat_specialty: str, member_name: str, argument: str, vote: str) -> None:
        with SessionLocal() as session:
            turn = CouncilDebateTurn(
                session_id=session_id,
                round_number=round_num,
                seat_id=seat_id,
                seat_specialty=seat_specialty,
                member_name=member_name,
                argument=argument,
                vote=vote
            )
            session.add(turn)
            session.commit()

    def finalize_council_session(self, session_id: str, rounds_count: int,
                                  consensus_pct: float, consensus_reached: bool,
                                  senior_leader_ruled: bool, final_spec: str,
                                  training_data: str) -> None:
        with SessionLocal() as session:
            c_session = session.query(CouncilSession).filter_by(id=session_id).first()
            if c_session:
                c_session.rounds_count = rounds_count
                c_session.consensus_percentage = consensus_pct
                c_session.consensus_reached = consensus_reached
                c_session.senior_leader_ruled = senior_leader_ruled
                c_session.final_operational_spec = final_spec
                c_session.training_data_summary = training_data
                session.commit()

    def create_project_org(self, project_id: str, name: str, objective_id: str,
                           total_agents: int, total_reviewers: int, total_managers: int,
                           total_workers: int, orchestrator_ids: List[str]) -> ProjectRecord:
        with SessionLocal() as session:
            proj = ProjectRecord(
                id=project_id,
                name=name,
                objective_id=objective_id,
                status="STAFFING",
                total_agents=total_agents,
                total_reviewers=total_reviewers,
                total_managers=total_managers,
                total_workers=total_workers,
                orchestrator_ids=json.dumps(orchestrator_ids),
                revision_iteration=0
            )
            session.add(proj)

            # Update meta spawned count
            meta = session.query(CompanyMeta).first()
            if meta:
                meta.total_agents_spawned += total_agents

            session.commit()
            session.refresh(proj)
            return proj

    def register_agent(self, agent_id: str, name: str, role: str, tier: str,
                       project_id: Optional[str] = None, model_name: str = "") -> AgentRecord:
        with SessionLocal() as session:
            meta = session.query(CompanyMeta).first()
            active_model = model_name or (meta.active_model if meta else "default")
            agent = AgentRecord(
                id=agent_id,
                name=name,
                role=role,
                tier=tier,
                assigned_project_id=project_id,
                status="ACTIVE" if project_id else "IDLE",
                model_name=active_model
            )
            session.merge(agent)
            session.commit()
            return agent

    def save_checkpoint(self, project_id: str, agent_id: str, milestone_name: str, payload: Dict[str, Any]) -> None:
        with SessionLocal() as session:
            cp = StateCheckpointRecord(
                project_id=project_id,
                agent_id=agent_id,
                milestone_name=milestone_name,
                state_payload=json.dumps(payload)
            )
            session.add(cp)
            session.commit()

    def get_latest_checkpoint(self, project_id: str, agent_id: str) -> Optional[Dict[str, Any]]:
        with SessionLocal() as session:
            cp = session.query(StateCheckpointRecord).filter_by(
                project_id=project_id, agent_id=agent_id
            ).order_by(StateCheckpointRecord.created_at.desc()).first()
            if cp:
                return {
                    "milestone_name": cp.milestone_name,
                    "payload": json.loads(cp.state_payload),
                    "created_at": cp.created_at.isoformat()
                }
            return None

    def log_reviewer_action(self, project_id: str, reviewer_id: str, target_agent_id: str,
                            severity: str, issue_type: str, details: str,
                            rollback_milestone: Optional[str] = None,
                            rollback_executed: bool = False,
                            escalation_path: Optional[str] = None) -> None:
        with SessionLocal() as session:
            log_rec = ReviewerLogRecord(
                project_id=project_id,
                reviewer_id=reviewer_id,
                target_agent_id=target_agent_id,
                severity=severity,
                issue_type=issue_type,
                details=details,
                rollback_milestone=rollback_milestone,
                rollback_executed=rollback_executed,
                escalation_path=escalation_path
            )
            session.add(log_rec)

            if severity == "SERIOUS_HALT":
                # Pause the agent
                agent = session.query(AgentRecord).filter_by(id=target_agent_id).first()
                if agent:
                    agent.status = "PAUSED_BY_REVIEWER"

            session.commit()

    def resume_agent_after_rollback(self, agent_id: str) -> None:
        with SessionLocal() as session:
            agent = session.query(AgentRecord).filter_by(id=agent_id).first()
            if agent:
                agent.status = "ACTIVE"
                session.commit()

    def save_institutional_memory(self, project_id: str, objective_summary: str,
                                   decisions_summary: str, failures_summary: str,
                                   successes_summary: str, architectural_records: str,
                                   deliverables_manifest: str) -> None:
        with SessionLocal() as session:
            mem = InstitutionalMemoryRecord(
                project_id=project_id,
                objective_summary=objective_summary,
                decisions_summary=decisions_summary,
                failures_summary=failures_summary,
                successes_summary=successes_summary,
                architectural_records=architectural_records,
                deliverables_manifest=deliverables_manifest
            )
            session.add(mem)

            # Update meta projects completed
            meta = session.query(CompanyMeta).first()
            if meta:
                meta.total_projects_completed += 1

            session.commit()

    def release_project_agents(self, project_id: str) -> None:
        """Section 18 & 20: Release agents back to the company workforce upon project completion."""
        with SessionLocal() as session:
            session.query(AgentRecord).filter_by(assigned_project_id=project_id).update({
                "assigned_project_id": None,
                "status": "IDLE"
            })
            proj = session.query(ProjectRecord).filter_by(id=project_id).first()
            if proj:
                proj.status = "DISSOLVED"
            session.commit()

repo = CompanyRepository()
