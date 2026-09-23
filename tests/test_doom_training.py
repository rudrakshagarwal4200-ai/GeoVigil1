"""
Unit & Integration Tests for DOOM Website Engineering Training
Tests:
- Video corpus ingestion and analysis
- 37-agent agency taxonomy coverage
- 3D canvas scrubber blueprint & interactive systems
- Multi-epoch training harness and persistence
- Blueprint synthesis and zero-generic role allocation
- Constitutional compliance during organizational builds
"""

import os
import unittest
from ai_company.doom.knowledge import WebsiteAgencyKnowledge
from ai_company.doom.curriculum import DOOMCurriculum
from ai_company.doom.brain import DOOMArchitecturalBrain
from ai_company.doom.trainer import DOOMTrainer
from ai_company.doom.engine import doom
from ai_company.council.parliament import CouncilDecision

class TestDOOMTraining(unittest.TestCase):
    def setUp(self):
        self.trainer = DOOMTrainer(output_path="e:/agy/ai_company/doom/doom_knowledge.json")

    def test_video_knowledge_corpus(self):
        """Verify all 9 YouTube videos are ingested with complete analysis."""
        videos = WebsiteAgencyKnowledge.VIDEO_SOURCES
        self.assertEqual(len(videos), 9, "Must contain exactly 9 YouTube training sources")
        
        video_ids = [v.video_id for v in videos]
        expected_ids = [
            "snErQUyqwCU", "_PtVROzu3_w", "DJMsXSr1jec",
            "h2MjhbwVKLk", "VMvZuhcDdnw", "h956KTuFKck",
            "nPxMF2YV77I", "dn6MDl86fRY", "GPpYwjMoLio"
        ]
        for vid in expected_ids:
            self.assertIn(vid, video_ids)

        for v in videos:
            self.assertTrue(len(v.title) > 0)
            self.assertTrue(len(v.creator) > 0)
            self.assertTrue(len(v.key_techniques) >= 3)
            self.assertTrue(len(v.architectural_takeaway) > 10)

    def test_agency_taxonomy_completeness(self):
        """Verify all 37 agency roles are categorized with quality gates."""
        roles = WebsiteAgencyKnowledge.AGENCY_ROLES
        self.assertEqual(len(roles), 37, "Must contain all 37 agency roles")

        orchestrators = WebsiteAgencyKnowledge.get_orchestrator_roles()
        reviewers = WebsiteAgencyKnowledge.get_reviewer_roles()
        self.assertEqual(len(orchestrators), 3, "Must have exactly 3 orchestrators in core taxonomy")
        self.assertGreaterEqual(len(reviewers), 3, "Must have at least 3 reviewers in core taxonomy")

        for r in roles:
            self.assertTrue(r.role_id.startswith("agency-"))
            self.assertTrue(len(r.core_deliverables) >= 1)
            self.assertTrue(len(r.quality_gates) >= 1)

    def test_design_system_and_motion_blueprints(self):
        """Verify luxury tokens, 3D canvas scrubber, and interactive blueprints."""
        tokens = WebsiteAgencyKnowledge.LUXURY_DESIGN_TOKENS
        self.assertGreaterEqual(len(tokens), 10)

        scrubber = WebsiteAgencyKnowledge.CANVAS_SCRUBBER_BLUEPRINT
        self.assertEqual(scrubber["fps_target"], 60)
        self.assertEqual(scrubber["format"], "WebP (80-85% quality, lossy with transparent alpha or obsidian backdrop)")

        interactive = WebsiteAgencyKnowledge.INTERACTIVE_BLUEPRINTS
        self.assertIn("interactive_configurator", interactive)
        self.assertIn("instant_pricing_calculator", interactive)
        self.assertIn("vip_reservation_pass", interactive)
        self.assertIn("live_telemetry_hud", interactive)

    def test_curriculum_structure(self):
        """Verify 5 training modules with comprehensive lessons and constitutional gates."""
        modules = DOOMCurriculum.MODULES
        self.assertEqual(len(modules), 5, "Must have 5 curriculum modules")

        all_lessons = DOOMCurriculum.get_all_lessons()
        self.assertEqual(len(all_lessons), 10, "Must have 10 comprehensive lessons across modules")

        for lesson in all_lessons:
            self.assertTrue(len(lesson.video_references) >= 1)
            self.assertTrue(len(lesson.constitutional_checks) >= 1)

    def test_architectural_brain_and_zero_generic_roles(self):
        """Verify DOOM's architectural brain produces blueprints with zero generic roles."""
        blueprint = DOOMArchitecturalBrain.synthesize_blueprint(
            project_name="Aura Swiss Horology",
            objective_text="Build an ultra-luxury 3D watch website with 360 exploded view and VIP pass",
            target_headcount=12
        )
        self.assertEqual(blueprint.archetype, "LUXURY_3D_SHOWCASE")
        self.assertTrue(blueprint.canvas_scrubber["enabled"])
        self.assertGreaterEqual(len(blueprint.interactive_systems), 2)
        self.assertEqual(len(blueprint.assigned_roles), 12)

        # Check constitutional constraints on assigned roles
        orch_count = sum(1 for r in blueprint.assigned_roles if r["tier"] == "ORCHESTRATOR")
        rev_count = sum(1 for r in blueprint.assigned_roles if r["tier"] == "REVIEWER")
        self.assertEqual(orch_count, 3, "Must have exactly 3 orchestrators")
        self.assertGreaterEqual(rev_count, 2, "Must have ceil(12/10)=2 reviewers")

        # Zero generic roles check
        for r in blueprint.assigned_roles:
            self.assertFalse(r["name"].startswith("Worker "), f"Found generic name: {r['name']}")
            self.assertFalse(r["name"].startswith("Technical Specialist"), f"Found generic name: {r['name']}")
            self.assertTrue(len(r["description"]) > 10)

    def test_full_multi_epoch_training_and_persistence(self):
        """Execute full 5-epoch training loop, verify persistence and 100% pass score."""
        report = self.trainer.run_training()
        self.assertEqual(report.epochs_completed, 5)
        self.assertEqual(report.overall_score, 100.0)
        self.assertTrue(os.path.exists(report.trained_artifacts_path))

        self.assertTrue(doom.is_trained())
        metadata = doom.get_trained_metadata()
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["video_sources_count"], 9)
        self.assertEqual(metadata["agency_roles_count"], 37)

    def test_build_organization_with_trained_agency(self):
        """Verify DOOM builds an organization using the trained agency taxonomy and attaches blueprint."""
        decision = CouncilDecision(
            session_id="SES-WEB-001",
            objective_id="OBJ-WEB-001",
            rounds_executed=1,
            consensus_percentage=0.95,
            consensus_reached=True,
            senior_leader_ruled=False,
            operational_specification="Build a high-converting roofing contractor quote engine with instant calculator",
            training_data="TRAINING RECORD: Consensus reached at 95%",
            participating_seats_count=20
        )
        built_org = doom.build_organization(
            council_decision=decision,
            project_name="Apex Shield Roofing",
            explicit_agent_count=10
        )
        self.assertEqual(built_org.staffing_plan.total_agents, 10)
        self.assertEqual(len(built_org.orchestrator_ids), 3)
        self.assertEqual(len(built_org.reviewer_ids), 1)
        self.assertIsNotNone(built_org.blueprint)
        self.assertEqual(built_org.blueprint.archetype, "HIGH_CONVERTING_LEAD_ENGINE")

if __name__ == "__main__":
    unittest.main()
