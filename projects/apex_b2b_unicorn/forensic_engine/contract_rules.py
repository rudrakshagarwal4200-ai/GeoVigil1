"""
Contract Rule Interpreter & Demurrage Clock Engine
Module: contract_rules.py
Purpose: Evaluates complex contractual clauses including demurrage start triggers
         (Discharge vs Availability vs Customs Release), working days vs calendar days,
         and identifies potential counter-evidence that could invalidate a dispute.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class DemurrageRuleInterpreter:
    def __init__(self, clause_config: Dict[str, Any]):
        self.clock_start_trigger = clause_config.get("clock_start_trigger", "DISCHARGE") # DISCHARGE, AVAILABILITY, CUSTOMS_RELEASE
        self.free_day_type = clause_config.get("free_day_type", "WORKING_DAYS") # WORKING_DAYS or CALENDAR_DAYS
        self.free_days = int(clause_config.get("demurrage_free_days", 4))
        self.daily_rate = float(clause_config.get("demurrage_daily_rate", 150.0))
        self.is_day_zero_inclusive = bool(clause_config.get("is_day_zero_inclusive", False))
        self.customs_hold_exempt = bool(clause_config.get("customs_hold_exempt", True))

    def _is_weekend(self, dt: datetime, jurisdiction: str = "UAE") -> bool:
        """Determines if a day is a statutory weekend based on jurisdiction."""
        if jurisdiction == "UAE":
            # UAE standard weekend: Saturday & Sunday (since 2022)
            return dt.weekday() in [5, 6]
        else: # US/Europe
            return dt.weekday() in [5, 6]

    def compute_chargeable_demurrage(
        self,
        discharge_dt: datetime,
        availability_dt: Optional[datetime],
        customs_release_dt: Optional[datetime],
        gate_out_dt: datetime,
        customs_hold_days: int = 0,
        port_strike_days: int = 0,
        jurisdiction: str = "UAE"
    ) -> Dict[str, Any]:
        """
        Determines the exact legally chargeable demurrage days considering triggers,
        statutory holidays/weekends, and exempt hold periods.
        """
        # Determine clock start date
        if self.clock_start_trigger == "CUSTOMS_RELEASE" and customs_release_dt:
            start_dt = customs_release_dt
            trigger_reason = f"Clock triggered by Customs Release on {start_dt.strftime('%Y-%m-%d')}"
        elif self.clock_start_trigger == "AVAILABILITY" and availability_dt:
            start_dt = availability_dt
            trigger_reason = f"Clock triggered by Terminal Availability Notice on {start_dt.strftime('%Y-%m-%d')}"
        else:
            start_dt = discharge_dt
            trigger_reason = f"Clock triggered by Vessel Discharge on {start_dt.strftime('%Y-%m-%d')}"

        if not self.is_day_zero_inclusive:
            start_dt = start_dt + timedelta(days=1)

        # Count days until gate out
        curr = start_dt
        elapsed_free_consumed = 0
        chargeable_days = 0
        exempt_days = 0

        while curr <= gate_out_dt:
            is_weekend_day = self._is_weekend(curr, jurisdiction)
            
            # Check if day is exempt under working-days clause
            if self.free_day_type == "WORKING_DAYS" and is_weekend_day:
                exempt_days += 1
            elif elapsed_free_consumed < self.free_days:
                elapsed_free_consumed += 1
            else:
                chargeable_days += 1
            curr += timedelta(days=1)

        # Apply specific operational exemptions (Customs hold, Force majeure / Port congestion strike)
        if self.customs_hold_exempt and customs_hold_days > 0:
            chargeable_days = max(0, chargeable_days - customs_hold_days)
            exempt_days += customs_hold_days

        if port_strike_days > 0:
            chargeable_days = max(0, chargeable_days - port_strike_days)
            exempt_days += port_strike_days

        expected_demurrage_amt = round(chargeable_days * self.daily_rate, 2)

        return {
            "clock_start_date": start_dt.strftime("%Y-%m-%d"),
            "trigger_reason": trigger_reason,
            "free_days_consumed": elapsed_free_consumed,
            "exempt_days": exempt_days,
            "chargeable_days": chargeable_days,
            "daily_rate": self.daily_rate,
            "expected_amount": expected_demurrage_amt
        }


class CounterEvidenceEvaluator:
    """
    Evaluates potential facts that could invalidate an AP dispute.
    Presents both SUPPORTING evidence and INVALIDATION risks to the CFO.
    """
    @staticmethod
    def identify_invalidation_risks(
        invoice: Dict[str, Any],
        contract: Dict[str, Any],
        bol: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        risks = []
        charge_type = invoice.get("charge_type")

        # 1. Customs Hold risk
        if charge_type == "DEMURRAGE":
            if bol and bol.get("customs_hold_flag"):
                risks.append({
                    "factor": "CUSTOMS_INSPECTION_RECORDED",
                    "description": "Port record indicates customs physical inspection hold. Carrier may argue container was not available for pickup due to regulatory clearance, invoking Clause 8.4 special storage tariff."
                })
            risks.append({
                "factor": "FORCE_MAJEURE_TERMINAL_CONGESTION",
                "description": "Terminal gate congestion or severe weather during this window could allow carrier to apply emergency yard storage surcharges if declared under Port Circular."
            })

        # 2. General Rate Increase (GRI) / Bunker adjustment risk
        if charge_type == "OCEAN_FREIGHT":
            risks.append({
                "factor": "PENDING_GRI_ADDENDUM",
                "description": "Check if an unrecorded General Rate Increase (GRI) or Peak Season Surcharge (PSS) notice was acknowledged via email by procurement."
            })

        # 3. Off-Invoice Rebate / Pending Credit Note
        risks.append({
            "factor": "UNAPPLIED_CREDIT_MEMO",
            "description": "Carrier AR ledger may already reflect an unapplied credit balance or quarterly volume rebate offsetting this variance."
        })

        return risks
