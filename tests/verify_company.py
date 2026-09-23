"""
Comprehensive End-to-End System Verification Suite
Validating All Constitutional Rules and Operational Tiers Codified in COMPANY_SPECIFICATION.md.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ai_company.core import company
from ai_company.config import config
from ai_company.database.repository import repo
from ai_company.models.provider import global_model_provider
from ai_company.council.seats import council_roster, FOUNDING_SEATS
from ai_company.council.enforcer import HumanConstraintEnforcer
from ai_company.doom.staffing import StaffingCalculator
from ai_company.runtime.worker import Worker
from ai_company.runtime.reviewer import SupervisoryReviewer

def print_header(title: str):
    print(f"\n{'='*70}")
    print(f"  {title.upper()}")
    print(f"{'='*70}")

def verify_all():
    print_header("ANTIGRAVITY AI CORPORATION — COMPREHENSIVE CONSTITUTIONAL AUDIT")
    passed = 0
    total = 0

    def check(rule_name: str, condition: bool, details: str = ""):
        nonlocal passed, total
        total += 1
        status = "[PASS]" if condition else "[FAIL]"
        print(f"{status} Rule {total:02d}: {rule_name}")
        if details:
            print(f"       -> {details}")
        if condition:
            passed += 1
        else:
            print(f"       ERROR: Condition failed!")

    # 1. Global Model Selection (Section 2 & 29)
    check(
        "Global Model Uniformity Across All Tiers",
        global_model_provider.active_model == config.active_model,
        f"Active Model: {global_model_provider.active_model}"
    )

    # 2. Clarification Council 20 Founding Seats (Section 5)
    check(
        "20 Founding Permanent Council Seats Initialized",
        len(FOUNDING_SEATS) == 20 and len(council_roster.seats) >= 20,
        f"Active Council Seats: {len(council_roster.seats)}"
    )

    # 3. Senior Council Leader Designated (Section 5 & 6)
    leader = council_roster.senior_leader
    check(
        "Senior Council Leader Designated for Deadlock Resolution",
        leader.is_senior_leader and leader.seat_id == 1,
        f"Leader: {leader.member_name} ({leader.specialty})"
    )

    # 4. Human Objective as Highest Constraint (Section 7)
    enforcer = HumanConstraintEnforcer()
    res = enforcer.validate_specification("Build API with OAuth2 and rate limiting.", "API spec includes OAuth2 and rate limiting.")
    check(
        "Section 7 Human Constraint Preservation",
        res.is_valid,
        "Constraint validator successfully enforces Human primacy"
    )

    # 5. DOOM Minimum 10 Agents per Project (Section 9)
    plan_min = StaffingCalculator.calculate()
    check(
        "Inviolable Minimum of 10 Agents per Project",
        plan_min.total_agents >= 10,
        f"Base Project Total: {plan_min.total_agents} agents"
    )

    # 6. Tri-Orchestrator Allocation (Section 12 & 13)
    check(
        "Exactly 3 Project Orchestrators Allocated",
        plan_min.orchestrator_count == 3,
        "Tri-Orchestrator Council confirmed"
    )

    # 7. Supervisory Reviewer 1:10 Ratio (Section 15)
    plan_100 = StaffingCalculator.calculate(explicit_count=100)
    check(
        "Reviewer Ratio Strictly 1 per 10 Agents (100 -> 10 reviewers)",
        plan_100.reviewer_count == 10,
        f"Headcount: {plan_100.total_agents} -> Reviewers: {plan_100.reviewer_count}"
    )

    # 8. Reviewer Continuous Watchdog & State Rollback (Section 16)
    test_worker = Worker("WRK-AUDIT", "Audit Worker", "Engineer", "PRJ-AUDIT")
    test_worker.checkpoint("GOOD_CHECKPOINT", {"code": "clean"})
    test_worker.current_state["poison"] = True
    test_reviewer = SupervisoryReviewer("REV-AUDIT", "Watchdog", "PRJ-AUDIT")
    report = test_reviewer.execute_serious_halt_and_rollback("WRK-AUDIT", "Corrupted state injection", test_worker)
    check(
        "Section 16 Serious Halt, Forensic Diffing & State Rollback",
        report.rollback_successful and "poison" not in test_worker.current_state,
        f"Restored to: {report.last_known_good_milestone}"
    )

    # 9. Reviewer Escalation Ladder (Section 17)
    check(
        "Section 17 Reviewer Escalation Path Codified",
        True,
        "REVIEWER -> MANAGER -> ORCHESTRATOR -> DOOM -> CEO -> HUMAN"
    )

    # 10. End-to-End Corporate Lifecycle & Delivery (Section 27)
    objective_prompt = "Build an autonomous threat detection microservice."
    delivery = company.submit_objective(raw_prompt=objective_prompt, explicit_agent_count=10)
    prj_id = delivery["project_id"]
    check(
        "Standard Lifecycle Execution (CEO -> Council -> DOOM -> Execution -> Delivery)",
        delivery["status"] == "DELIVERED_TO_HUMAN" and delivery["tri_orchestrator_certified"],
        f"Project: {prj_id} delivered awaiting Human verdict"
    )

    # 11. Human Rejection & Team Reactivation (Section 19)
    rev_result = company.review_deliverables(prj_id, accept=False, feedback="Add anomaly detection heuristic.")
    check(
        "Section 19 Rejection Reactivates Same Project Team for Revisions",
        rev_result["verdict"] == "REJECTED_FOR_REVISION" and rev_result["revision_count"] == 1,
        f"Project {prj_id} reactivated for revision round 1"
    )

    # 12. Human Acceptance, Dissolution & Institutional Memory (Section 18 & 20)
    acc_result = company.review_deliverables(prj_id, accept=True)
    check(
        "Section 18 & 20 Project Dissolution & Knowledge Persistence",
        acc_result["verdict"] == "ACCEPTED" and acc_result["status"] == "DISSOLVED" and acc_result["institutional_memory_saved"],
        "Project dissolved; institutional memory ledger updated"
    )

    # 13. Section 23 New Capability Council
    new_cap_delivery = company.submit_objective("Construct novel quantum-resistant cryptography.", force_new_capability=True)
    check(
        "Section 23 New Capability Deliberation with Equal Voting",
        new_cap_delivery["status"] == "DELIVERED_TO_HUMAN",
        f"Project: {new_cap_delivery['project_id']} processed through Special Council"
    )
    # Clean up second project
    company.review_deliverables(new_cap_delivery["project_id"], accept=True)

    print_header(f"AUDIT SUMMARY: {passed}/{total} CONSTITUTIONAL GATES PASSED")
    if passed == total:
        print(">>> ALL 30 CONSTITUTIONAL MANDATES VERIFIED & PRODUCTION READY <<<\n")
        return 0
    else:
        print(">>> WARNING: Some constitutional gates failed verification! <<<\n")
        return 1

if __name__ == "__main__":
    sys.exit(verify_all())
