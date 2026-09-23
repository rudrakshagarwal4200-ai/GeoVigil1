"""
FastAPI Server & Real-time Web Dashboard Backend
Providing REST endpoints and live telemetry streaming for the Executive Command Center.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pathlib import Path
import json

from ai_company.core import company
from ai_company.database.repository import repo
from ai_company.database.schema import SessionLocal, HumanObjective, ProjectRecord, InstitutionalMemoryRecord, ReviewerLogRecord
from ai_company.council.seats import council_roster

app = FastAPI(title="AI Company Executive Command Center", version="1.0.0")

STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class ObjectiveRequest(BaseModel):
    prompt: str
    explicit_agent_count: Optional[int] = None
    force_new_capability: bool = False
    complexity_score: int = 1

class ReviewRequest(BaseModel):
    project_id: str
    accept: bool
    feedback: str = ""

class ModelSwitchRequest(BaseModel):
    model_name: str

@app.get("/", response_class=HTMLResponse)
def get_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>AI Company Dashboard Initializing...</h1>"

@app.get("/api/status")
def get_status():
    return company.get_status()

@app.get("/api/council")
def get_council():
    seats = [
        {
            "seat_id": s.seat_id,
            "specialty": s.specialty,
            "member_name": s.member_name,
            "is_core": s.is_core,
            "is_senior_leader": s.is_senior_leader,
            "rotation_projects": s.rotation_projects
        }
        for s in council_roster.seats
    ]
    return {"total_seats": len(seats), "seats": seats}

@app.post("/api/objectives")
def submit_objective(req: ObjectiveRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Objective prompt cannot be empty.")
    result = company.submit_objective(
        raw_prompt=req.prompt,
        explicit_agent_count=req.explicit_agent_count,
        force_new_capability=req.force_new_capability,
        complexity_score=req.complexity_score
    )
    return result

@app.post("/api/review")
def review_project(req: ReviewRequest):
    result = company.review_deliverables(
        project_id=req.project_id,
        accept=req.accept,
        feedback=req.feedback
    )
    return result

@app.post("/api/model")
def switch_model(req: ModelSwitchRequest):
    result = company.switch_global_model(req.model_name)
    return result

@app.get("/api/projects")
def list_projects():
    with SessionLocal() as session:
        projects = session.query(ProjectRecord).order_by(ProjectRecord.created_at.desc()).limit(20).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "objective_id": p.objective_id,
                "status": p.status,
                "total_agents": p.total_agents,
                "total_reviewers": p.total_reviewers,
                "revision_iteration": p.revision_iteration,
                "created_at": p.created_at.isoformat()
            }
            for p in projects
        ]

@app.get("/api/memory")
def get_memory():
    with SessionLocal() as session:
        memories = session.query(InstitutionalMemoryRecord).order_by(InstitutionalMemoryRecord.created_at.desc()).limit(20).all()
        return [
            {
                "project_id": m.project_id,
                "objective_summary": m.objective_summary,
                "decisions": m.decisions_summary,
                "successes": m.successes_summary,
                "failures": m.failures_summary,
                "created_at": m.created_at.isoformat()
            }
            for m in memories
        ]

@app.get("/api/logs")
def get_reviewer_logs():
    with SessionLocal() as session:
        logs = session.query(ReviewerLogRecord).order_by(ReviewerLogRecord.created_at.desc()).limit(30).all()
        return [
            {
                "id": l.id,
                "project_id": l.project_id,
                "reviewer_id": l.reviewer_id,
                "target_agent_id": l.target_agent_id,
                "severity": l.severity,
                "issue_type": l.issue_type,
                "details": l.details,
                "rollback_milestone": l.rollback_milestone,
                "rollback_executed": l.rollback_executed,
                "created_at": l.created_at.isoformat()
            }
            for l in logs
        ]
