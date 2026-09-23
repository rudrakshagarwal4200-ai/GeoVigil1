"""
DOOM Staffing & Structural Calculator
Sections 8, 9, 10, 12, 13, 15: Sizing algorithms, 10-agent minimum, 1:10 reviewer ratio, 3 orchestrators.
"""

import math
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ai_company.config import config

class StaffingPlan(BaseModel):
    total_agents: int
    orchestrator_count: int = 3
    reviewer_count: int
    manager_count: int
    worker_count: int
    is_explicitly_set: bool = False

class StaffingCalculator:
    @staticmethod
    def calculate(explicit_count: Optional[int] = None, complexity_score: int = 1) -> StaffingPlan:
        """
        Compute project staffing adhering to constitutional constraints:
        - Minimum 10 agents per project (Section 9)
        - Exactly 3 orchestrators (Section 12, 13)
        - 1 reviewer per 10 agents ratio: ceil(total / 10) (Section 15)
        - Elastic scaling with no upper limit
        """
        if explicit_count is not None:
            total = max(config.min_agents_per_project, explicit_count)
            is_explicit = True
        else:
            # Complexity-based elastic determination
            base = config.min_agents_per_project # 10
            scale_factor = max(1, complexity_score)
            total = base * scale_factor
            is_explicit = False

        orchestrator_count = config.orchestrator_count # 3
        # Reviewer ratio: 1 per 10 agents
        reviewer_count = math.ceil(total / config.reviewer_agent_ratio)
        
        remaining = total - orchestrator_count - reviewer_count
        if remaining < 2:
            # Adjust total up if needed to satisfy minimum worker/manager staffing
            total = orchestrator_count + reviewer_count + 2
            remaining = 2

        # Allocate Managers and Workers
        # Target ~1 manager per 4-6 workers
        manager_count = max(1, remaining // 4)
        worker_count = remaining - manager_count

        return StaffingPlan(
            total_agents=total,
            orchestrator_count=orchestrator_count,
            reviewer_count=reviewer_count,
            manager_count=manager_count,
            worker_count=worker_count,
            is_explicitly_set=is_explicit
        )
