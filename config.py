"""
AI Company Configuration
Codifying global company configuration, model selection, paths, and defaults.
"""

from pathlib import Path
from pydantic import BaseModel, Field
import os

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "ai_company.db"
DEFAULT_WORKSPACE = Path("e:/agy")

class CompanyConfig(BaseModel):
    # Section 2 & 29: Global Model Selection
    active_model: str = Field(default="gemini-3.8-flash", description="Human-selected global model name")
    fallback_to_simulation: bool = Field(default=True, description="Enable simulated reasoning if API keys are absent")
    
    # Section 9: Agent Creation rules
    min_agents_per_project: int = Field(default=10, description="Inviolable minimum agents per project")
    orchestrator_count: int = Field(default=3, description="Standard project orchestrators count")
    reviewer_agent_ratio: int = Field(default=10, description="1 reviewer per 10 agents")
    
    # Section 5 & 6: Council rules
    council_permanent_seats: int = Field(default=20, description="Founding permanent council seats")
    council_consensus_threshold: float = Field(default=0.75, description="75% consensus threshold")
    council_max_debate_rounds: int = Field(default=3, description="Rounds before Senior Council Leader breaks deadlock")
    dynamic_member_max_projects: int = Field(default=5, description="Max 5 projects before dynamic member termination")
    
    # Paths & storage
    db_url: str = Field(default=f"sqlite:///{DATABASE_PATH.as_posix()}", description="Database connection URL")
    log_dir: Path = Field(default=BASE_DIR / "logs")
    artifacts_dir: Path = Field(default=BASE_DIR / "artifacts")
    
    class Config:
        arbitrary_types_allowed = True

# Global configuration singleton
config = CompanyConfig()

# Ensure directories exist
config.log_dir.mkdir(parents=True, exist_ok=True)
config.artifacts_dir.mkdir(parents=True, exist_ok=True)
