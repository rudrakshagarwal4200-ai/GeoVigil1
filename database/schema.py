"""
Database Schema for AI Company Institutional Memory & Runtime State
Codified using SQLAlchemy.
"""

from datetime import datetime, timezone
import json
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from ai_company.config import config

def utc_now():
    return datetime.now(timezone.utc)

Base = declarative_base()

class CompanyMeta(Base):
    """Global company-level configuration and statistics."""
    __tablename__ = "company_meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    active_model = Column(String(128), default=config.active_model, nullable=False)
    total_agents_spawned = Column(Integer, default=0, nullable=False)
    total_projects_completed = Column(Integer, default=0, nullable=False)
    evolution_stage = Column(String(64), default="Initial", nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class HumanObjective(Base):
    """The original Human prompt - highest constraint in the company."""
    __tablename__ = "human_objectives"

    id = Column(String(64), primary_key=True)
    raw_prompt = Column(Text, nullable=False)
    explicit_agent_count = Column(Integer, nullable=True)  # Section 9: if Human explicitly specifies count
    status = Column(String(64), default="SUBMITTED", nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    ceo_analyses = relationship("CEOAnalysis", back_populates="objective", cascade="all, delete-orphan")
    council_sessions = relationship("CouncilSession", back_populates="objective", cascade="all, delete-orphan")
    projects = relationship("ProjectRecord", back_populates="objective", cascade="all, delete-orphan")

class CEOAnalysis(Base):
    """Executive comprehension record created by the CEO."""
    __tablename__ = "ceo_analyses"

    id = Column(String(64), primary_key=True)
    objective_id = Column(String(64), ForeignKey("human_objectives.id"), nullable=False)
    actual_intent = Column(Text, nullable=False)
    significance = Column(Text, nullable=False)
    implications = Column(Text, nullable=False)
    success_criteria = Column(Text, nullable=False)
    required_capabilities = Column(Text, nullable=False)
    is_new_capability = Column(Boolean, default=False, nullable=False)  # Section 23 flag
    created_at = Column(DateTime, default=utc_now)

    objective = relationship("HumanObjective", back_populates="ceo_analyses")

class CouncilSession(Base):
    """Clarification Council parliamentary deliberation session."""
    __tablename__ = "council_sessions"

    id = Column(String(64), primary_key=True)
    objective_id = Column(String(64), ForeignKey("human_objectives.id"), nullable=False)
    rounds_count = Column(Integer, default=1, nullable=False)
    consensus_percentage = Column(Float, default=0.0, nullable=False)
    consensus_reached = Column(Boolean, default=False, nullable=False)
    senior_leader_ruled = Column(Boolean, default=False, nullable=False)  # Senior Council Leader deadlock break
    final_operational_spec = Column(Text, nullable=True)
    training_data_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    objective = relationship("HumanObjective", back_populates="council_sessions")
    debates = relationship("CouncilDebateTurn", back_populates="session", cascade="all, delete-orphan")

class CouncilDebateTurn(Base):
    """Individual debate turn from a Council Member."""
    __tablename__ = "council_debate_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), ForeignKey("council_sessions.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    seat_id = Column(Integer, nullable=False)
    seat_specialty = Column(String(128), nullable=False)
    member_name = Column(String(128), nullable=False)
    argument = Column(Text, nullable=False)
    vote = Column(String(16), nullable=False)  # APPROVE, DISSENT, REVISE
    created_at = Column(DateTime, default=utc_now)

    session = relationship("CouncilSession", back_populates="debates")

class AgentRecord(Base):
    """Agent entity record with project exclusivity tracking."""
    __tablename__ = "agents"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    role = Column(String(128), nullable=False)
    tier = Column(String(64), nullable=False)  # CEO, COUNCIL_CORE, COUNCIL_DYNAMIC, DOOM, ORCHESTRATOR, MANAGER, REVIEWER, WORKER
    assigned_project_id = Column(String(64), nullable=True)  # Section 10: Exclusive single project assignment
    status = Column(String(64), default="IDLE", nullable=False)  # IDLE, ACTIVE, PAUSED_BY_REVIEWER, TERMINATED
    rotation_projects_count = Column(Integer, default=0, nullable=False)  # For dynamic council members (max 5)
    model_name = Column(String(128), default=config.active_model, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class ProjectRecord(Base):
    """Temporary Project Corporation constructed by DOOM."""
    __tablename__ = "projects"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    objective_id = Column(String(64), ForeignKey("human_objectives.id"), nullable=False)
    status = Column(String(64), default="STAFFING", nullable=False)  # STAFFING, EXECUTING, REVIEWING, DELIVERED, REVISION, COMPLETED, DISSOLVED
    total_agents = Column(Integer, default=0, nullable=False)
    total_reviewers = Column(Integer, default=0, nullable=False)
    total_managers = Column(Integer, default=0, nullable=False)
    total_workers = Column(Integer, default=0, nullable=False)
    orchestrator_ids = Column(Text, default="[]", nullable=False)  # JSON list of 3 orchestrator IDs
    revision_iteration = Column(Integer, default=0, nullable=False)  # Section 19: revision counter
    output_deliverables = Column(Text, nullable=True)  # JSON summary of deliverables
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)

    objective = relationship("HumanObjective", back_populates="projects")
    reviewer_logs = relationship("ReviewerLogRecord", back_populates="project", cascade="all, delete-orphan")
    checkpoints = relationship("StateCheckpointRecord", back_populates="project", cascade="all, delete-orphan")
    institutional_memory = relationship("InstitutionalMemoryRecord", back_populates="project", cascade="all, delete-orphan")

class StateCheckpointRecord(Base):
    """Last known-good state checkpoint for agent rollback."""
    __tablename__ = "state_checkpoints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    agent_id = Column(String(64), nullable=False)
    milestone_name = Column(String(128), nullable=False)
    state_payload = Column(Text, nullable=False)  # JSON string of state data
    created_at = Column(DateTime, default=utc_now)

    project = relationship("ProjectRecord", back_populates="checkpoints")

class ReviewerLogRecord(Base):
    """Supervisory audit logs, graduated interventions, rollbacks, and escalations."""
    __tablename__ = "reviewer_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    reviewer_id = Column(String(64), nullable=False)
    target_agent_id = Column(String(64), nullable=False)
    severity = Column(String(32), nullable=False)  # MINOR_WARN, SERIOUS_HALT
    issue_type = Column(String(64), nullable=False)  # DRIFT, LOOP, CONTAMINATION, REASONING_ERROR
    details = Column(Text, nullable=False)
    rollback_milestone = Column(String(128), nullable=True)
    rollback_executed = Column(Boolean, default=False, nullable=False)
    escalation_path = Column(String(256), nullable=True)  # Reviewer -> Manager -> Orchestrator -> DOOM -> CEO -> Human
    created_at = Column(DateTime, default=utc_now)

    project = relationship("ProjectRecord", back_populates="reviewer_logs")

class InstitutionalMemoryRecord(Base):
    """Persistent institutional memory preserved across project dissolutions."""
    __tablename__ = "institutional_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    objective_summary = Column(Text, nullable=False)
    decisions_summary = Column(Text, nullable=False)
    failures_summary = Column(Text, nullable=True)
    successes_summary = Column(Text, nullable=True)
    architectural_records = Column(Text, nullable=True)
    deliverables_manifest = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    project = relationship("ProjectRecord", back_populates="institutional_memory")

# Engine and session initialization
engine = create_engine(config.db_url, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    """Initialize database tables and set up singleton metadata record."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        meta = session.query(CompanyMeta).first()
        if not meta:
            meta = CompanyMeta(
                active_model=config.active_model,
                total_agents_spawned=0,
                total_projects_completed=0,
                evolution_stage="Foundational"
            )
            session.add(meta)
            session.commit()
