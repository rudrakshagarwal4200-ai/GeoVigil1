"""
New Capability & Corporate Evolution Protocol
Sections 23, 24, 25: Special procedures for novel capabilities, organizational evolution, and new business divisions.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ai_company.council.seats import CouncilSeat, council_roster
from ai_company.council.parliament import clarification_council, CouncilDecision
from ai_company.executive.ceo import ceo
from ai_company.doom.engine import doom

class EvolutionProposal(BaseModel):
    proposal_title: str
    rationale: str
    target_division: Optional[str] = None
    participating_seats: int
    passed_75_percent: bool
    escalated_to_human: bool
    final_resolution: str

class EvolutionEngine:
    @staticmethod
    def deliberate_new_capability(objective_id: str, raw_prompt: str, capability_name: str) -> CouncilDecision:
        """
        Section 23:
        1. CEO + DOOM enter Clarification Council as ordinary equal members.
        2. Equal voting weight (no extra power for CEO, DOOM, seniority, rank).
        3. Proposal requires 75% majority.
        4. If 75% cannot be reached: Human makes final decision.
        """
        # Create special seats for CEO and DOOM
        special_seats = list(council_roster.seats)
        ceo_seat = CouncilSeat(
            seat_id=len(special_seats) + 1,
            specialty=f"Executive Perspective ({ceo.role})",
            member_name=ceo.name,
            is_core=False
        )
        doom_seat = CouncilSeat(
            seat_id=len(special_seats) + 2,
            specialty=f"Organizational Architecture ({doom.role})",
            member_name=doom.name,
            is_core=False
        )
        special_seats.append(ceo_seat)
        special_seats.append(doom_seat)

        # Run parliamentary debate with expanded equal voting body
        decision = clarification_council.deliberate(
            objective_id=objective_id,
            raw_prompt=f"[NEW CAPABILITY CONVOCATION: {capability_name}]\n{raw_prompt}",
            ceo_brief=f"Novel capability assessment: {capability_name}. CEO & DOOM participating as equal members.",
            is_new_capability=True,
            custom_seats=special_seats
        )
        return decision

    @staticmethod
    def establish_new_division(human_command: str, division_name: str) -> Dict[str, Any]:
        """
        Section 25: The company can create new businesses and divisions when directed by the Human.
        Human has final authority; CEO and DOOM then determine how to construct it.
        """
        return {
            "division_name": division_name,
            "status": "CHARTERED_BY_HUMAN",
            "executive_direction": f"CEO and DOOM allocating organizational blueprint for division '{division_name}'.",
            "capacity": "ELASTIC"
        }

evolution_engine = EvolutionEngine()
