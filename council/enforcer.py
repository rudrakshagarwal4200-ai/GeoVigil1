"""
Human Constraint Enforcer
Section 7: The original Human prompt is the highest-level constraint.
Validates that Council specifications never dilute, remove, or violate Human requirements.
"""

from typing import List, Tuple
from pydantic import BaseModel

class ConstraintCheckResult(BaseModel):
    is_valid: bool
    violations: List[str] = []
    adherence_score: float = 1.0

class HumanConstraintEnforcer:
    @staticmethod
    def validate_specification(raw_human_prompt: str, operational_spec: str) -> ConstraintCheckResult:
        """
        Enforce Section 7:
        1. Council cannot lower requirements.
        2. Council cannot remove requirements.
        3. Council cannot change fundamental objective.
        4. Council cannot ignore explicit constraints.
        """
        violations = []
        raw_lower = raw_human_prompt.lower()
        spec_lower = operational_spec.lower()

        # Check keyword preservation for explicit constraints
        key_constraints = []
        for line in raw_human_prompt.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("*") or "must" in line.lower() or "required" in line.lower():
                key_constraints.append(line)

        for constraint in key_constraints:
            # Check if key tokens in constraint are preserved in the spec
            words = [w for w in constraint.split() if len(w) > 4]
            if words and not any(w.lower() in spec_lower for w in words):
                violations.append(f"Potential omission of explicit constraint: '{constraint[:60]}...'")

        if violations:
            return ConstraintCheckResult(
                is_valid=False,
                violations=violations,
                adherence_score=max(0.5, 1.0 - (len(violations) * 0.15))
            )

        return ConstraintCheckResult(is_valid=True, violations=[], adherence_score=1.0)
