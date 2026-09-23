"""
DOOM module for organizational synthesis, staffing, and agency engineering.
"""

from ai_company.doom.engine import doom, DOOM, BuiltProjectOrganization
from ai_company.doom.staffing import StaffingCalculator, StaffingPlan
from ai_company.doom.knowledge import WebsiteAgencyKnowledge
from ai_company.doom.brain import DOOMArchitecturalBrain, WebsiteBlueprint
from ai_company.doom.curriculum import DOOMCurriculum
from ai_company.doom.trainer import doom_trainer, DOOMTrainer

__all__ = [
    "doom",
    "DOOM",
    "BuiltProjectOrganization",
    "StaffingCalculator",
    "StaffingPlan",
    "WebsiteAgencyKnowledge",
    "DOOMArchitecturalBrain",
    "WebsiteBlueprint",
    "DOOMCurriculum",
    "doom_trainer",
    "DOOMTrainer"
]
