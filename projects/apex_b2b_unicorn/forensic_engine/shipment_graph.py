"""
Shipment & Economic Event Graph Engine
Module: shipment_graph.py
Purpose: Elevates the core unit of truth from an isolated "Invoice" to the "Shipment Economic Event".
         Tracks total consumed spend across POs, BOLs, parent invoices, split invoices,
         supplementary drayage, and credit notes against contractual baseline obligations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

class ShipmentEconomicEvent:
    def __init__(self, shipment_id: str, container_id: str, bol_number: Optional[str] = None):
        self.shipment_id = shipment_id
        self.container_id = container_id
        self.bol_number = bol_number
        self.purchase_orders: List[Dict[str, Any]] = []
        self.invoices: List[Dict[str, Any]] = []
        self.credit_notes: List[Dict[str, Any]] = []
        self.terminal_events: List[Dict[str, Any]] = []
        self.contract_obligations: Dict[str, Any] = {}
        
    def add_invoice(self, inv: Dict[str, Any]):
        self.invoices.append(inv)

    def add_credit_note(self, cn: Dict[str, Any]):
        self.credit_notes.append(cn)

    def add_terminal_event(self, event: Dict[str, Any]):
        self.terminal_events.append(event)

    def compute_total_consumed_spend(self) -> float:
        """Calculates net spend consumed by this physical shipment."""
        total_billed = sum(float(inv.get("amount", 0.0)) for inv in self.invoices)
        total_credited = sum(float(cn.get("amount", 0.0)) for cn in self.credit_notes)
        return round(total_billed - total_credited, 2)

    def compute_contractual_obligation(self) -> float:
        """Calculates expected spend based on contracted rate cards and valid accessorials."""
        return round(float(self.contract_obligations.get("total_expected", 0.0)), 2)

    def get_shipment_variance(self) -> float:
        consumed = self.compute_total_consumed_spend()
        obligation = self.compute_contractual_obligation()
        variance = consumed - obligation
        return round(max(0.0, variance), 2)


class TransactionTruthGraph:
    """
    Graph of all physical shipments and their economic representations.
    Solves split duplicates, cumulative overbilling, and credit note leakages.
    """
    def __init__(self):
        self.shipments: Dict[str, ShipmentEconomicEvent] = {}
        self.container_to_shipment: Dict[str, str] = {}
        self.bol_to_shipment: Dict[str, str] = {}

    def get_or_create_shipment(self, container_id: str, bol_number: Optional[str] = None) -> ShipmentEconomicEvent:
        shipment_id = None
        if container_id and container_id in self.container_to_shipment:
            shipment_id = self.container_to_shipment[container_id]
        elif bol_number and bol_number in self.bol_to_shipment:
            shipment_id = self.bol_to_shipment[bol_number]
        else:
            shipment_id = f"SHIP-{container_id or bol_number or 'UNKNOWN'}"
            self.shipments[shipment_id] = ShipmentEconomicEvent(shipment_id, container_id, bol_number)
            if container_id:
                self.container_to_shipment[container_id] = shipment_id
            if bol_number:
                self.bol_to_shipment[bol_number] = shipment_id

        return self.shipments[shipment_id]

    def ingest_document(self, doc_type: str, data: Dict[str, Any]):
        container_id = data.get("container_id", "")
        bol_no = data.get("bol_number", "")
        shipment = self.get_or_create_shipment(container_id, bol_no)

        if doc_type == "INVOICE":
            shipment.add_invoice(data)
        elif doc_type == "CREDIT_NOTE":
            shipment.add_credit_note(data)
        elif doc_type == "TERMINAL_EVENT":
            shipment.add_terminal_event(data)
        elif doc_type == "CONTRACT":
            shipment.contract_obligations = data

    def evaluate_cumulative_leakage(self) -> List[Dict[str, Any]]:
        """
        Audits all shipments on the economic event level.
        Detects cumulative creep where individual invoices look small ($5k, $7k),
        but collectively blow past the contracted freight rate.
        """
        leakages = []
        for ship_id, shipment in self.shipments.items():
            variance = shipment.get_shipment_variance()
            if variance > 0.0:
                leakages.append({
                    "shipment_id": ship_id,
                    "container_id": shipment.container_id,
                    "bol_number": shipment.bol_number,
                    "total_consumed": shipment.compute_total_consumed_spend(),
                    "contractual_obligation": shipment.compute_contractual_obligation(),
                    "cumulative_variance": variance,
                    "invoices_involved": [inv.get("invoice_number") for inv in shipment.invoices],
                    "credits_applied": [cn.get("credit_note_number") for cn in shipment.credit_notes]
                })
        return leakages
