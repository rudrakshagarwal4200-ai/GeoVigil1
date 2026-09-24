"""
Blind Adversarial Benchmark Evaluator (1,000-Invoice Blind Test)
Module: run_blind_benchmark.py
Purpose: Tests Apex Recover against the independent frozen ground truth across
         9 adversarial failure classes. Measures Dollar-Weighted Precision (DWP),
         Dollar-Weighted Recall (DWR), false positive suppression, and the 4-stage cash funnel.
"""

import json
import os
import csv
from datetime import datetime
from collections import defaultdict
from adversarial_ground_truth_generator import build_adversarial_1000_dataset
from expected_cost_engine import ExpectedCostEngine
from dataset_generator import generate_benchmark_contracts
from shipment_graph import TransactionTruthGraph
from dispute_recommender import DisputeRecommender
from contract_rules import CounterEvidenceEvaluator

def main():
    print("=" * 70)
    print("   APEX RECOVER :: 1,000-INVOICE ADVERSARIAL BLIND BENCHMARK")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    truth_file = os.path.join(base_dir, "frozen_ground_truth.json")
    results_csv = os.path.join(base_dir, "blind_audit_report.csv")

    # 1. Generate 1,000 adversarial transactions & freeze ground truth
    invoices, bols, ground_truth = build_adversarial_1000_dataset()
    with open(truth_file, "w", encoding="utf-8") as f:
        json.dump(ground_truth, f, indent=2)

    print(f"\n[+] Generated {len(invoices)} Adversarial Transactions across 9 Failure Classes")
    print(f"[+] Independent Ground Truth Frozen at: {truth_file}\n")

    # 2. Ingest Standard Contracts
    contracts = generate_benchmark_contracts()

    # 3. Initialize Engines
    engine = ExpectedCostEngine(contracts_db=contracts)
    graph = TransactionTruthGraph()

    # 4. Run Blind Audit
    audit_results = {}
    total_audited_spend = 0.0

    for inv in invoices:
        inv_no = inv.get("invoice_number")
        bol = bols.get(inv_no)
        amt = float(inv.get("amount", 0.0))
        total_audited_spend += amt

        # Ingest into Shipment Graph
        graph.ingest_document("INVOICE", inv)
        if bol:
            graph.ingest_document("TERMINAL_EVENT", bol)

        # Run line item audit
        audit_res = engine.audit_line_item(invoice=inv, bol=bol)

        # Evaluate Counter-Evidence & 'Do Not Send' Gate
        counter_risks = CounterEvidenceEvaluator.identify_invalidation_risks(inv, contracts.get(inv["vendor"], {}), bol)
        gate_res = DisputeRecommender.evaluate_do_not_send_gate(
            variance=audit_res["variance"],
            evidence_docs=audit_res["evidence_documents"],
            vendor_relationship_tier=inv.get("historical_behavior", "Standard"),
            counter_risks=counter_risks
        )

        audit_res["can_send_dispute"] = gate_res["can_send"]
        audit_res["gate_reason"] = gate_res["reason"]
        audit_res["counter_risks"] = [r["factor"] for r in counter_risks]

        audit_results[inv_no] = audit_res

    # 5. Evaluate Against Frozen Ground Truth
    class_stats = defaultdict(lambda: {"total": 0, "tp": 0, "fp": 0, "fn": 0, "tn": 0, "true_dollars": 0.0, "flagged_dollars": 0.0, "disputed_dollars": 0.0})

    total_actual_leakage_dollars = 0.0
    total_flagged_dollars = 0.0
    total_disputed_dollars = 0.0
    true_disputed_dollars = 0.0
    false_disputed_dollars = 0.0

    for inv_no, gt in ground_truth.items():
        res = audit_results.get(inv_no, {})
        true_cls = gt["true_class"]
        actual_leakage = gt["true_leakage_dollars"]
        is_actionable = gt["is_actionable_dispute"]

        detected_variance = res.get("variance", 0.0)
        can_send = res.get("can_send_dispute", False)

        stats = class_stats[true_cls]
        stats["total"] += 1
        stats["true_dollars"] += actual_leakage
        total_actual_leakage_dollars += actual_leakage

        if detected_variance > 0:
            stats["flagged_dollars"] += detected_variance
            total_flagged_dollars += detected_variance

        # Was a formal dispute recommended?
        if can_send and detected_variance > 0:
            stats["disputed_dollars"] += detected_variance
            total_disputed_dollars += detected_variance

            if is_actionable:
                stats["tp"] += 1
                true_disputed_dollars += min(actual_leakage, detected_variance)
            else:
                stats["fp"] += 1
                false_disputed_dollars += detected_variance
        else:
            if is_actionable:
                stats["fn"] += 1
            else:
                stats["tn"] += 1

    # 6. Compute Key Metrics
    dwp = (true_disputed_dollars / total_disputed_dollars * 100) if total_disputed_dollars > 0 else 0.0
    dwr = (true_disputed_dollars / total_actual_leakage_dollars * 100) if total_actual_leakage_dollars > 0 else 0.0

    # Funnel Realization Model
    identified_gross = total_flagged_dollars
    accepted_post_gate = total_disputed_dollars
    realized_recovery_est = accepted_post_gate * 0.82 # 82% carrier settlement rate
    apex_contingency_fee = realized_recovery_est * 0.20
    customer_net_cash = realized_recovery_est - apex_contingency_fee
    customer_roi = customer_net_cash / apex_contingency_fee if apex_contingency_fee > 0 else 0.0

    print("=" * 70)
    print("                    BLIND BENCHMARK SUMMARY (1,000 INVOICES)   ")
    print("=" * 70)
    print(f"Total Transactions Audited:         {len(invoices):,}")
    print(f"Total Spend Audited:                ${total_audited_spend:,.2f}")
    print(f"Actual Ground Truth Leakage:        ${total_actual_leakage_dollars:,.2f} ({(total_actual_leakage_dollars/total_audited_spend)*100:.2f}% of spend)")
    print("-" * 70)
    print(f"Identified Gross Variance:          ${identified_gross:,.2f}")
    print(f"Disputes Recommended Post-Gate:     ${accepted_post_gate:,.2f}")
    print(f"True Disputed Dollars:              ${true_disputed_dollars:,.2f}")
    print(f"False Disputed Dollars:             ${false_disputed_dollars:,.2f}")
    print("=" * 70)
    print("                    ADVANCED METRICS (THE NUMBERS THAT MATTER)  ")
    print("=" * 70)
    print(f"DOLLAR-WEIGHTED PRECISION (DWP):    {dwp:.2f}%")
    print(f"DOLLAR-WEIGHTED RECALL (DWR):       {dwr:.2f}%")
    print("-" * 70)
    print("CLASS-BY-CLASS PERFORMANCE:")
    print(f"{'Failure Class':<28} | {'Total':<5} | {'TP':<4} | {'FP':<4} | {'FN':<4} | {'Actual $':<11} | {'Disputed $'}")
    print("-" * 70)
    for c_name, c_s in sorted(class_stats.items()):
        print(f"{c_name:<28} | {c_s['total']:<5} | {c_s['tp']:<4} | {c_s['fp']:<4} | {c_s['fn']:<4} | ${c_s['true_dollars']:<10,.0f} | ${c_s['disputed_dollars']:,.0f}")

    print("=" * 70)
    print("                    REALIZED CASH RECOVERY FUNNEL               ")
    print("=" * 70)
    print(f"Stage 1: Gross Leakage Identified:       ${identified_gross:,.2f}")
    print(f"Stage 2: Post-Gate Accepted (Actionable):${accepted_post_gate:,.2f}")
    print(f"Stage 3: Realized Recovery (82% settle): ${realized_recovery_est:,.2f}")
    print(f"Stage 4: Apex 20% Contingency Fee:       ${apex_contingency_fee:,.2f}")
    print(f"Stage 5: Client Net Cash in Pocket:      ${customer_net_cash:,.2f}")
    print(f"Client Net Cash ROI:                     {customer_roi:.1f}x (${customer_net_cash:,.2f} net cash / ${apex_contingency_fee:,.2f} fee)")
    print("=" * 70 + "\n")

    # Write detailed CSV report
    with open(results_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["invoice_number", "vendor", "charge_type", "amount", "detected_variance", "can_send_dispute", "true_class", "actual_leakage", "is_actionable", "gate_reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for inv_no, res in audit_results.items():
            gt = ground_truth.get(inv_no, {})
            writer.writerow({
                "invoice_number": inv_no,
                "vendor": res.get("vendor"),
                "charge_type": res.get("charge_type"),
                "amount": res.get("invoice_amount"),
                "detected_variance": res.get("variance"),
                "can_send_dispute": res.get("can_send_dispute"),
                "true_class": gt.get("true_class"),
                "actual_leakage": gt.get("true_leakage_dollars"),
                "is_actionable": gt.get("is_actionable_dispute"),
                "gate_reason": res.get("gate_reason")
            })

if __name__ == "__main__":
    main()
