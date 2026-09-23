"""
Unit Tests for Clarification Council & Human Constraint Enforcer
Sections 5, 6, 7 & 23.
"""

import unittest
from ai_company.council.seats import council_roster, FOUNDING_SEATS
from ai_company.council.parliament import clarification_council
from ai_company.council.enforcer import HumanConstraintEnforcer

class TestClarificationCouncil(unittest.TestCase):
    def test_founding_seats_count(self):
        """Section 5: Initial council has 20 permanent council members with distinct specialties."""
        self.assertEqual(len(FOUNDING_SEATS), 20)
        self.assertEqual(len(council_roster.seats), 20)
        specialties = [s.specialty for s in FOUNDING_SEATS]
        # Verify all specialties are distinct
        self.assertEqual(len(specialties), len(set(specialties)))

    def test_senior_council_leader(self):
        """Section 5 & 6: Senior Council Leader is designated and breaks deadlocks."""
        leader = council_roster.senior_leader
        self.assertTrue(leader.is_senior_leader)
        self.assertEqual(leader.seat_id, 1)

    def test_council_consensus_deliberation(self):
        """Section 6: Normal Council decisions require at least 75% consensus."""
        decision = clarification_council.deliberate(
            objective_id="OBJ-TEST-001",
            raw_prompt="Design a high-throughput transaction ledger with zero data loss.",
            ceo_brief="Executive directive: Deliver resilient transaction ledger."
        )
        self.assertTrue(decision.consensus_reached)
        self.assertGreaterEqual(decision.consensus_percentage, 0.75)
        self.assertIn("RATIFIED OPERATIONAL SPECIFICATION", decision.operational_specification)
        self.assertIn("TRAINING RECORD", decision.training_data)

    def test_human_constraint_enforcer(self):
        """Section 7: Human objective sits above operational spec; constraints cannot be omitted."""
        raw_prompt = "Build a microservice.\n* MUST support TLS 1.3 encryption\n* MUST maintain sub-5ms latency"
        valid_spec = "Microservice specifications:\n- Architecture includes TLS 1.3 encryption\n- Guarantees sub-5ms latency"
        invalid_spec = "Microservice specifications:\n- Architecture includes standard HTTP\n- Average response time 50ms"

        enforcer = HumanConstraintEnforcer()
        res_valid = enforcer.validate_specification(raw_prompt, valid_spec)
        self.assertTrue(res_valid.is_valid)

        res_invalid = enforcer.validate_specification(raw_prompt, invalid_spec)
        self.assertFalse(res_invalid.is_valid)
        self.assertGreater(len(res_invalid.violations), 0)

if __name__ == "__main__":
    unittest.main()
