"""
Unit Tests for Corporate Lifecycle, Revisions, and Institutional Memory
Sections 2, 18, 19, 20, 21, 27, 29.
"""

import unittest
from ai_company.core import company
from ai_company.database.repository import repo
from ai_company.models.provider import global_model_provider

class TestCorporateLifecycle(unittest.TestCase):
    def test_end_to_end_lifecycle_with_revision(self):
        """
        Test complete standard lifecycle:
        1. Human Objective submitted
        2. CEO -> Council -> DOOM -> Project Execution -> Review -> Delivery
        3. Human rejects output with feedback -> same project team reactivated
        4. Human accepts revised output -> project dissolves, institutional memory persisted
        """
        # Step 1 & 2: Submit Objective
        prompt = "Develop an autonomous API security scanner with continuous vulnerability scanning."
        dispatch_res = company.submit_objective(
            raw_prompt=prompt,
            explicit_agent_count=10
        )
        project_id = dispatch_res["project_id"]
        self.assertEqual(dispatch_res["status"], "DELIVERED_TO_HUMAN")
        self.assertTrue(dispatch_res["tri_orchestrator_certified"])
        self.assertEqual(dispatch_res["staffing"]["total_agents"], 10)
        self.assertEqual(dispatch_res["staffing"]["orchestrators"], 3)
        self.assertEqual(dispatch_res["staffing"]["reviewers"], 1)

        # Step 3: Human rejects output (Section 19)
        rejection_res = company.review_deliverables(
            project_id=project_id,
            accept=False,
            feedback="Enhance payload injection fuzzing vectors."
        )
        self.assertEqual(rejection_res["verdict"], "REJECTED_FOR_REVISION")
        self.assertEqual(rejection_res["revision_count"], 1)

        # Verify project is still active in company roster
        self.assertIn(project_id, company.active_projects)

        # Step 4: Human accepts revised output (Section 18 & 20)
        acceptance_res = company.review_deliverables(
            project_id=project_id,
            accept=True
        )
        self.assertEqual(acceptance_res["verdict"], "ACCEPTED")
        self.assertEqual(acceptance_res["status"], "DISSOLVED")
        self.assertTrue(acceptance_res["institutional_memory_saved"])

        # Verify project has dissolved and agents are released
        self.assertNotIn(project_id, company.active_projects)

    def test_global_model_selection(self):
        """Section 2 & 29: Changing global model propagates to all company tiers."""
        initial_model = global_model_provider.active_model
        company.switch_global_model("nemotron-3-ultra")
        self.assertEqual(global_model_provider.active_model, "nemotron-3-ultra")
        meta = repo.get_meta()
        self.assertEqual(meta.active_model, "nemotron-3-ultra")

        # Revert back to gemini-2.5-flash
        company.switch_global_model("gemini-2.5-flash")
        self.assertEqual(global_model_provider.active_model, "gemini-2.5-flash")

if __name__ == "__main__":
    unittest.main()
