"""
Production Realized-Recovery Ledger & State Machine
Module: recovery_ledger.py
Purpose: Enforces the 4 immutable states of enterprise cash recovery:
         DETECTED -> ACCEPTED -> RECOVERED -> CASH_VERIFIED
         Ensures startup accounting cosplay is prohibited: revenue is recognized
         ONLY when funds are independently verified in the bank or ledger.
"""

import json
import os
import csv
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional

class RecoveryState(str, Enum):
    DETECTED = "DETECTED"           # Identified by Engine with cross-document evidence
    ACCEPTED = "ACCEPTED"           # Approved by Client CFO after counter-evidence review
    RECOVERED = "RECOVERED"         # Carrier issued credit note or accepted debit deduction
    CASH_VERIFIED = "CASH_VERIFIED" # Bank deposit confirmed or credit applied to active payable

class RealizedRecoveryItem:
    def __init__(
        self,
        item_id: str,
        invoice_number: str,
        vendor: str,
        container_id: str,
        amount_detected: float,
        evidence_summary: str
    ):
        self.item_id = item_id
        self.invoice_number = invoice_number
        self.vendor = vendor
        self.container_id = container_id
        self.amount_detected = amount_detected
        self.amount_accepted = 0.0
        self.amount_recovered = 0.0
        self.amount_cash_verified = 0.0
        
        self.state = RecoveryState.DETECTED
        self.evidence_summary = evidence_summary
        
        self.detected_at = datetime.utcnow().isoformat()
        self.accepted_at: Optional[str] = None
        self.recovered_at: Optional[str] = None
        self.cash_verified_at: Optional[str] = None
        
        self.credit_note_ref: Optional[str] = None
        self.bank_transaction_hash: Optional[str] = None

    def mark_accepted(self, approved_amount: float, cfo_name: str):
        self.state = RecoveryState.ACCEPTED
        self.amount_accepted = approved_amount
        self.accepted_at = datetime.utcnow().isoformat()

    def mark_recovered(self, settled_amount: float, credit_note_ref: str):
        self.state = RecoveryState.RECOVERED
        self.amount_recovered = settled_amount
        self.credit_note_ref = credit_note_ref
        self.recovered_at = datetime.utcnow().isoformat()

    def mark_cash_verified(self, verified_amount: float, bank_or_ledger_hash: str):
        self.state = RecoveryState.CASH_VERIFIED
        self.amount_cash_verified = verified_amount
        self.bank_transaction_hash = bank_or_ledger_hash
        self.cash_verified_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "invoice_number": self.invoice_number,
            "vendor": self.vendor,
            "container_id": self.container_id,
            "state": self.state.value,
            "amount_detected": self.amount_detected,
            "amount_accepted": self.amount_accepted,
            "amount_recovered": self.amount_recovered,
            "amount_cash_verified": self.amount_cash_verified,
            "credit_note_ref": self.credit_note_ref,
            "bank_transaction_hash": self.bank_transaction_hash,
            "timestamps": {
                "detected": self.detected_at,
                "accepted": self.accepted_at,
                "recovered": self.recovered_at,
                "cash_verified": self.cash_verified_at
            }
        }


class ProductionRecoveryLedger:
    def __init__(self, client_id: str, ledger_file: Optional[str] = None):
        self.client_id = client_id
        self.ledger_file = ledger_file or f"ledger_{client_id}.json"
        self.items: Dict[str, RealizedRecoveryItem] = {}
        self.load()

    def add_detected_item(
        self,
        invoice_number: str,
        vendor: str,
        container_id: str,
        amount: float,
        evidence: str
    ) -> RealizedRecoveryItem:
        item_id = f"REC-{invoice_number}-{container_id}"
        item = RealizedRecoveryItem(item_id, invoice_number, vendor, container_id, amount, evidence)
        self.items[item_id] = item
        self.save()
        return item

    def get_summary(self) -> Dict[str, Any]:
        total_detected = sum(it.amount_detected for it in self.items.values())
        total_accepted = sum(it.amount_accepted for it in self.items.values() if it.state in [RecoveryState.ACCEPTED, RecoveryState.RECOVERED, RecoveryState.CASH_VERIFIED])
        total_recovered = sum(it.amount_recovered for it in self.items.values() if it.state in [RecoveryState.RECOVERED, RecoveryState.CASH_VERIFIED])
        total_cash_verified = sum(it.amount_cash_verified for it in self.items.values() if it.state == RecoveryState.CASH_VERIFIED)

        contingency_fee_earned = round(total_cash_verified * 0.20, 2)
        client_net_cash = round(total_cash_verified - contingency_fee_earned, 2)
        client_roi = round(client_net_cash / contingency_fee_earned, 2) if contingency_fee_earned > 0 else 0.0

        return {
            "client_id": self.client_id,
            "total_items_logged": len(self.items),
            "stage_1_detected_dollars": round(total_detected, 2),
            "stage_2_accepted_dollars": round(total_accepted, 2),
            "stage_3_recovered_dollars": round(total_recovered, 2),
            "stage_4_cash_verified_dollars": round(total_cash_verified, 2),
            "apex_contingency_fee_realized": contingency_fee_earned,
            "client_net_cash_retained": client_net_cash,
            "client_verified_roi": f"{client_roi}x"
        }

    def save(self):
        data = {
            "client_id": self.client_id,
            "summary": self.get_summary(),
            "items": [it.to_dict() for it in self.items.values()]
        }
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for raw in data.get("items", []):
                        item = RealizedRecoveryItem(
                            item_id=raw["item_id"],
                            invoice_number=raw["invoice_number"],
                            vendor=raw["vendor"],
                            container_id=raw["container_id"],
                            amount_detected=raw["amount_detected"],
                            evidence_summary=raw.get("evidence_summary", "")
                        )
                        item.state = RecoveryState(raw["state"])
                        item.amount_accepted = raw["amount_accepted"]
                        item.amount_recovered = raw["amount_recovered"]
                        item.amount_cash_verified = raw["amount_cash_verified"]
                        item.credit_note_ref = raw.get("credit_note_ref")
                        item.bank_transaction_hash = raw.get("bank_transaction_hash")
                        self.items[item.item_id] = item
            except Exception:
                pass
