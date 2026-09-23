"""
Clarification Council Seats & Membership Architecture
Section 5: 20 Founding Permanent Seats + Dynamic Senior Hybrid Roster.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from ai_company.database.repository import repo

class CouncilSeat(BaseModel):
    seat_id: int
    specialty: str
    member_name: str
    is_core: bool = True
    is_senior_leader: bool = False
    rotation_projects: int = 0  # Max 5 for dynamic members

# The 20 Founding Permanent Council Seats
FOUNDING_SEATS = [
    CouncilSeat(seat_id=1, specialty="Senior Council Leader & Parliamentary Chairperson", member_name="Leader Vance", is_core=True, is_senior_leader=True),
    CouncilSeat(seat_id=2, specialty="Lead Enterprise Systems Architect", member_name="Architect Thorne", is_core=True),
    CouncilSeat(seat_id=3, specialty="Security, Cryptography & Threat Modeling", member_name="Auditor Cross", is_core=True),
    CouncilSeat(seat_id=4, specialty="AI Research & Algorithmic Foundations", member_name="Scientist Mira", is_core=True),
    CouncilSeat(seat_id=5, specialty="Product Strategy & User Value Architecture", member_name="Director Scott", is_core=True),
    CouncilSeat(seat_id=6, specialty="Full-Stack Engineering & Microservices", member_name="Engineer Chen", is_core=True),
    CouncilSeat(seat_id=7, specialty="Data Persistence, Schemas & Distributed Storage", member_name="Data Specialist Mercer", is_core=True),
    CouncilSeat(seat_id=8, specialty="Formal Verification & Adversarial QA", member_name="Verifier Steele", is_core=True),
    CouncilSeat(seat_id=9, specialty="UI/UX, Sensory Interaction & Design Systems", member_name="Stylist Aria", is_core=True),
    CouncilSeat(seat_id=10, specialty="Regulatory Compliance, Safety & Governance", member_name="Counselor Blake", is_core=True),
    CouncilSeat(seat_id=11, specialty="Core Latency, Memory & Hardware Profiling", member_name="Optimizer Reyes", is_core=True),
    CouncilSeat(seat_id=12, specialty="Unit Economics, Financial Viability & Margins", member_name="Economist Sterling", is_core=True),
    CouncilSeat(seat_id=13, specialty="Brand Narrative, Copywriting & Culture", member_name="Storyteller Muse", is_core=True),
    CouncilSeat(seat_id=14, specialty="Distributed Resilience, SRE & Fault Recovery", member_name="SRE Calder", is_core=True),
    CouncilSeat(seat_id=15, specialty="Multi-Agent Concurrency & Orchestration Flow", member_name="Concurrency Lead Jax", is_core=True),
    CouncilSeat(seat_id=16, specialty="Telemetry, Tracing & Real-Time Observability", member_name="Observer Lin", is_core=True),
    CouncilSeat(seat_id=17, specialty="Protocols, External Integrations & Webhooks", member_name="Integration Specialist Novak", is_core=True),
    CouncilSeat(seat_id=18, specialty="Algorithmic Optimization & Computational Math", member_name="Mathematician Euler", is_core=True),
    CouncilSeat(seat_id=19, specialty="Human Intent Alignment & Ethical Guardrails", member_name="Alignment Officer Sol", is_core=True),
    CouncilSeat(seat_id=20, specialty="Runtime Environments & Edge Infrastructure", member_name="Runtime Architect Pierce", is_core=True),
]

class CouncilRoster:
    def __init__(self):
        self.seats: List[CouncilSeat] = list(FOUNDING_SEATS)
        self._register_members()

    def _register_members(self):
        for seat in self.seats:
            agent_id = f"COUNCIL-{seat.seat_id:02d}"
            tier = "COUNCIL_CORE" if seat.is_core else "COUNCIL_DYNAMIC"
            repo.register_agent(
                agent_id=agent_id,
                name=seat.member_name,
                role=seat.specialty,
                tier=tier,
                project_id=None
            )

    @property
    def senior_leader(self) -> CouncilSeat:
        for seat in self.seats:
            if seat.is_senior_leader:
                return seat
        return self.seats[0]

    def add_dynamic_member(self, specialty: str, name: str) -> CouncilSeat:
        """
        Section 5: DOOM selects high-performing senior agents for temporary council service (max 5 projects).
        """
        new_seat_id = len(self.seats) + 1
        seat = CouncilSeat(
            seat_id=new_seat_id,
            specialty=specialty,
            member_name=name,
            is_core=False,
            is_senior_leader=False,
            rotation_projects=0
        )
        self.seats.append(seat)
        agent_id = f"COUNCIL-DYN-{new_seat_id:02d}"
        repo.register_agent(
            agent_id=agent_id,
            name=seat.member_name,
            role=seat.specialty,
            tier="COUNCIL_DYNAMIC",
            project_id=None
        )
        return seat

    def advance_project_rotation(self) -> List[str]:
        """
        Section 5: Increment rotation for dynamic members.
        When reaching 5 projects, that agent is permanently terminated.
        """
        terminated_agents = []
        remaining_seats = []
        for seat in self.seats:
            if not seat.is_core:
                seat.rotation_projects += 1
                if seat.rotation_projects >= 5:
                    agent_id = f"COUNCIL-DYN-{seat.seat_id:02d}"
                    repo.register_agent(
                        agent_id=agent_id,
                        name=seat.member_name,
                        role=seat.specialty,
                        tier="TERMINATED",
                        project_id=None
                    )
                    terminated_agents.append(seat.member_name)
                    continue
            remaining_seats.append(seat)
        self.seats = remaining_seats
        return terminated_agents

council_roster = CouncilRoster()
