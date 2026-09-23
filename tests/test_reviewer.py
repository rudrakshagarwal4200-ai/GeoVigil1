"""
Unit Tests for Supervisory Reviewer & Graduated Intervention
Sections 15, 16, 17.
"""

import unittest
from ai_company.runtime.reviewer import SupervisoryReviewer
from ai_company.runtime.worker import Worker
from ai_company.runtime.manager import Manager
from ai_company.runtime.orchestrator import TriOrchestrator
from ai_company.database.repository import repo

class TestSupervisoryReviewer(unittest.TestCase):
    def setUp(self):
        self.project_id = "PRJ-REV-TEST"
        self.reviewer = SupervisoryReviewer(
            agent_id="REV-01",
            name="Senior Reviewer",
            project_id=self.project_id
        )
        self.worker = Worker(
            agent_id="WRK-01",
            name="Test Worker",
            role="Coder",
            project_id=self.project_id
        )

    def test_minor_intervention(self):
        """Section 16: Minor problem - Reviewer warns the agent. Agent attempts to correct."""
        audit = self.reviewer.audit_agent(
            target_agent_id=self.worker.agent_id,
            output_text="Valid code output",
            task_spec="Spec",
            raw_human_objective="Objective",
            force_issue="MINOR"
        )
        self.assertFalse(audit.is_clean)
        self.assertEqual(audit.severity, "MINOR")

        # Issue minor warning
        self.reviewer.issue_minor_warning(self.worker.agent_id, audit.details)
        # Verify agent is still active, not halted
        agent_rec = repo.get_latest_checkpoint(self.project_id, self.worker.agent_id)
        # Agent should not be paused
        self.assertNotEqual(self.worker.current_state.get("status"), "PAUSED_BY_REVIEWER")

    def test_serious_halt_and_rollback(self):
        """Section 16: Serious problem - pause agent, investigate, rollback to last known-good state, resume."""
        # 1. Worker reaches good milestone
        self.worker.checkpoint("MILESTONE_GOOD_1", {"clean_code": "def correct_logic(): pass"})

        # 2. Worker then generates corrupted state
        self.worker.current_state["tainted_code"] = "corrupted syntax error while True:"

        # 3. Reviewer detects serious issue
        audit = self.reviewer.audit_agent(
            target_agent_id=self.worker.agent_id,
            output_text="while True: pass\nwhile True: pass\nwhile True: pass\nwhile True: pass\nwhile True: pass\nwhile True: pass",
            task_spec="Spec",
            raw_human_objective="Objective",
            force_issue="SERIOUS"
        )
        self.assertFalse(audit.is_clean)
        self.assertEqual(audit.severity, "SERIOUS")

        # 4. Execute serious halt and rollback
        report = self.reviewer.execute_serious_halt_and_rollback(
            target_agent_id=self.worker.agent_id,
            issue_details=audit.details,
            worker_instance=self.worker
        )

        self.assertTrue(report.rollback_successful)
        self.assertTrue(report.resumed)
        self.assertEqual(report.last_known_good_milestone, "MILESTONE_GOOD_1")
        # Verify worker state restored and tainted code discarded
        self.assertIn("clean_code", self.worker.current_state)
        self.assertNotIn("tainted_code", self.worker.current_state)

    def test_reviewer_escalation_ladder(self):
        """Section 17: REVIEWER -> PROJECT MANAGER -> PROJECT ORCHESTRATOR -> DOOM -> CEO -> HUMAN"""
        manager = Manager(agent_id="MGR-01", name="Manager 1", role="Lead", project_id=self.project_id)
        manager.assign_worker(self.worker)
        orchestrator = TriOrchestrator(project_id=self.project_id, orchestrator_ids=["ORCH-1", "ORCH-2", "ORCH-3"])

        # 1. Test Manager Tier Resolution (Worker has saved milestone)
        self.worker.checkpoint("MILESTONE_ESCALATION", {"state": "healthy"})
        res = self.reviewer.escalate_issue(
            target_agent_id=self.worker.agent_id,
            issue_details="Worker deadlock",
            managers=[manager],
            orchestrator_layer=orchestrator
        )
        self.assertTrue(res["resolved"])
        self.assertEqual(res["stage"], "MANAGER")

        # 2. Test Orchestrator Tier Escalation (Worker not resolved by manager)
        res_orch = self.reviewer.escalate_issue(
            target_agent_id="WRK-EXTERNAL",
            issue_details="Unresolvable cross-team deadlock",
            managers=[manager],
            orchestrator_layer=orchestrator
        )
        self.assertTrue(res_orch["resolved"])
        self.assertEqual(res_orch["stage"], "ORCHESTRATOR")

if __name__ == "__main__":
    unittest.main()
