"""
Unit Tests for DOOM Organizational Engine & Staffing
Sections 8, 9, 10, 12, 13, 15.
"""

import unittest
from ai_company.doom.staffing import StaffingCalculator
from ai_company.doom.engine import doom
from ai_company.council.parliament import CouncilDecision

class TestDOOM(unittest.TestCase):
    def test_minimum_10_agents(self):
        """Section 9: The only minimum is 10 total agents per project."""
        plan_default = StaffingCalculator.calculate()
        self.assertGreaterEqual(plan_default.total_agents, 10)

        # Even if explicit count is requested as 4, DOOM enforces the 10 minimum
        plan_small = StaffingCalculator.calculate(explicit_count=4)
        self.assertGreaterEqual(plan_small.total_agents, 10)

    def test_reviewer_ratio(self):
        """Section 15: Reviewer ratio: 1 reviewer per 10 agents."""
        # 1-10 agents = 1 reviewer
        plan_10 = StaffingCalculator.calculate(explicit_count=10)
        self.assertEqual(plan_10.reviewer_count, 1)

        # 11-20 agents = 2 reviewers
        plan_15 = StaffingCalculator.calculate(explicit_count=15)
        self.assertEqual(plan_15.reviewer_count, 2)
        plan_20 = StaffingCalculator.calculate(explicit_count=20)
        self.assertEqual(plan_20.reviewer_count, 2)

        # 31-40 agents = 4 reviewers
        plan_35 = StaffingCalculator.calculate(explicit_count=35)
        self.assertEqual(plan_35.reviewer_count, 4)

        # 500 agents = 50 reviewers
        plan_500 = StaffingCalculator.calculate(explicit_count=500)
        self.assertEqual(plan_500.reviewer_count, 50)

    def test_three_orchestrators(self):
        """Section 12 & 13: Projects normally have 3 orchestrators."""
        plan = StaffingCalculator.calculate(explicit_count=25)
        self.assertEqual(plan.orchestrator_count, 3)

    def test_doom_build_organization(self):
        """Section 8: DOOM creates the entire temporary project organization."""
        mock_decision = CouncilDecision(
            session_id="CS-MOCK-1",
            objective_id="OBJ-MOCK-1",
            rounds_executed=1,
            consensus_percentage=1.0,
            consensus_reached=True,
            senior_leader_ruled=False,
            operational_specification="Build scalable search engine",
            training_data="Trained",
            participating_seats_count=20
        )
        org = doom.build_organization(
            council_decision=mock_decision,
            project_name="Test Enterprise Project",
            explicit_agent_count=12
        )
        self.assertEqual(len(org.orchestrator_ids), 3)
        self.assertEqual(len(org.reviewer_ids), 2) # 12 agents -> 2 reviewers
        self.assertEqual(org.staffing_plan.total_agents, 12)
        self.assertTrue(org.project_id.startswith("PRJ-"))

if __name__ == "__main__":
    unittest.main()
