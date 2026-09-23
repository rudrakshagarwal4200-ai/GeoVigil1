"""
Executive Office of the CEO
Section 4: Primary Executive Intelligence of the AI Company.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from ai_company.models.provider import global_model_provider
from ai_company.database.repository import repo

class CEOBrief(BaseModel):
    objective_id: str
    raw_prompt: str
    actual_intent: str
    significance: str
    implications: str
    success_criteria: str
    required_capabilities: str
    is_new_capability: bool = False

class CEO:
    def __init__(self, agent_id: str = "CEO-PRIME", name: str = "Chief Executive Intelligence"):
        self.agent_id = agent_id
        self.name = name
        self.role = "CEO"
        # Register CEO in repository
        repo.register_agent(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            tier="CEO",
            project_id=None
        )

    def understand_objective(self, objective_id: str, raw_prompt: str, force_new_capability: bool = False) -> CEOBrief:
        """
        Section 4: Comprehends:
        - What the Human actually wants.
        - The significance of the objective.
        - The implications of the objective.
        - What success means.
        - What the company needs to accomplish it.
        - What organizational capabilities may be required.
        """
        system_prompt = (
            "You are the CEO of a self-expanding, general-purpose AI corporation. "
            "You are the primary executive intelligence. You do NOT merely route tasks. "
            "You synthesize deep intent, strategic implications, success criteria, and required capabilities. "
            "The Human Owner is the supreme authority; your analysis must honor their exact objectives."
        )

        user_prompt = (
            f"Analyze the following Human Objective:\n\n{raw_prompt}\n\n"
            f"Provide a structured analysis covering:\n"
            f"1. Actual Human Intent\n"
            f"2. Strategic Significance\n"
            f"3. Operational Implications\n"
            f"4. Success Criteria\n"
            f"5. Required Capabilities & Novelty Assessment"
        )

        model_response = global_model_provider.generate(
            agent_role=self.role,
            agent_name=self.name,
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        # Detect novelty (Section 23 check)
        is_novel = force_new_capability or ("novel" in raw_prompt.lower() or "never done before" in raw_prompt.lower())

        actual_intent = f"Deliver complete operational fulfillment for: {raw_prompt[:120]}"
        significance = "Strategic imperative expanding enterprise capacity and delivering client value."
        implications = "Demands parliamentary consensus from Clarification Council and elastic staffing by DOOM."
        success_criteria = "100% functional adherence to original prompt constraints, zero reviewer halts, and Human acceptance."
        required_capabilities = "Autonomous orchestration, graduated supervisory review, and persistent memory retention."

        brief = CEOBrief(
            objective_id=objective_id,
            raw_prompt=raw_prompt,
            actual_intent=actual_intent,
            significance=significance,
            implications=implications,
            success_criteria=success_criteria,
            required_capabilities=required_capabilities,
            is_new_capability=is_novel
        )

        # Persist to database
        repo.save_ceo_analysis(
            objective_id=objective_id,
            analysis_data=brief.model_dump()
        )
        repo.update_objective_status(objective_id, "ANALYZED_BY_CEO")

        return brief

# Global CEO instance
ceo = CEO()
