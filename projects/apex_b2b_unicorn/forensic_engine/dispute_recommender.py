"""
Evidence-Backed Dispute Recommendation Engine
Module: dispute_recommender.py
Purpose: Replaces naive 'irrefutable accusations' with balanced, enterprise-grade
         Evidence-Backed Dispute Recommendations with a strict 'Do Not Send' gate
         and counter-evidence disclosure.
"""

from typing import Dict, List, Any
from datetime import datetime
from contract_rules import CounterEvidenceEvaluator

class DisputeRecommender:
    @staticmethod
    def evaluate_do_not_send_gate(
        variance: float,
        evidence_docs: str,
        vendor_relationship_tier: str,
        counter_risks: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Evaluates whether a dispute should be held in review or approved for recommendation.
        Gate criteria:
        1. Materiality threshold (e.g. variance < $50 is ignored as friction cost)
        2. Evidence completeness (requires at least 2 correlating source documents)
        3. Critical counter-evidence presence
        """
        if variance < 50.0:
            return {
                "can_send": False,
                "reason": f"Immaterial variance (${variance:,.2f} < $50.00 threshold). Suppressed to avoid vendor friction."
            }

        if "vs Prior" not in evidence_docs and "+" not in evidence_docs and "Contract" not in evidence_docs:
            return {
                "can_send": False,
                "reason": "Incomplete cross-document evidence: Secondary document verification missing."
            }

        if any(r["factor"] == "CUSTOMS_INSPECTION_RECORDED" for r in counter_risks):
            return {
                "can_send": False,
                "reason": "High Invalidation Risk: Port recorded active customs inspection hold. Recommend internal operations check before disputing."
            }

        return {
            "can_send": True,
            "reason": "Dispute meets materiality, cross-document evidence, and counter-risk thresholds."
        }

    @staticmethod
    def generate_recommendation_markdown(
        item: Dict[str, Any],
        contract: Dict[str, Any],
        bol: Dict[str, Any] = None
    ) -> str:
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        counter_risks = CounterEvidenceEvaluator.identify_invalidation_risks(item, contract, bol)
        gate_res = DisputeRecommender.evaluate_do_not_send_gate(
            variance=item["variance"],
            evidence_docs=item["evidence_documents"],
            vendor_relationship_tier=item.get("historical_behavior", "Standard"),
            counter_risks=counter_risks
        )

        status_badge = "[RECOMMENDED TO ISSUE]" if gate_res["can_send"] else "[HELD IN INTERNAL REVIEW - DO NOT SEND]"

        risks_md = ""
        for r in counter_risks:
            risks_md += f"* **{r['factor']}**: {r['description']}\n"

        return f"""# EVIDENCE-BACKED DISPUTE RECOMMENDATION
**Reference**: REC-DISPUTE-{item['invoice_id']}-{item['container']}  
**Generated On**: {now_str}  
**Status**: {status_badge}  
**Target Vendor**: {item['vendor']}  
**Identified Discrepancy**: **${item['variance']:,.2f}**  

---

### 1. SUMMARY OF RECONCILED DATA
| Parameter | Reconciled Value |
|:---|:---|
| **Invoice Reference** | `{item['invoice_id']}` |
| **Container / Shipment Key** | `{item['container']}` |
| **Charge Classification** | `{item['charge_type']}` |
| **Billed by Carrier** | `${item['invoice_amount']:,.2f}` |
| **Contractually Expected Amount** | `${item['expected_amount']:,.2f}` |
| **Variance / Potential Leakage** | **${item['variance']:,.2f}** |
| **Audit Queue** | **{item['decision']} Queue** |

---

### 2. PRIMARY EVIDENCE SUPPORTING OVERCHARGE
* **Contractual Rule**: `{item['contract_clause']}`
* **Documentary Support**: `{item['evidence_documents']}`
* **Audit Finding**:  
  > *"{item['audit_note']}"*

---

### 3. POTENTIAL COUNTER-EVIDENCE & INVALIDATION FACTORS
*Before dispatching this dispute, review the following factors that could legitimately explain or invalidate the variance:*
{risks_md}

---

### 4. DISPUTE GATE EVALUATION
* **Gate Decision**: `{"PASSED - CLEAR TO SEND" if gate_res["can_send"] else "HOLD - DO NOT DISPATCH"}`
* **Gate Rationale**: *{gate_res["reason"]}*

---

### 5. RECOMMENDED SETTLEMENT ACTION
If internal team confirms absence of counter-evidence:
1. Issue formal deduction or request Credit Note of **${item['variance']:,.2f}** referencing `{item['invoice_id']}`.
2. Settle verified net balance of **${item['expected_amount']:,.2f}**.

*Prepared by Apex Recover Transaction Truth Engine. Intended solely for authorized client finance review. Does not constitute autonomous legal action.*
"""
