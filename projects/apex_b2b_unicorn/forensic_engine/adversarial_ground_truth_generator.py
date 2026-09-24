"""
Adversarial 1,000-Invoice Dataset & Frozen Ground Truth Generator
Module: adversarial_ground_truth_generator.py
Purpose: Generates a realistic, dirty 1,000-transaction dataset with independent
         frozen labels across 9 distinct operational failure classes:
         - Clean Invoices
         - Exact Duplicates
         - Semantic / Temporal Duplicates
         - Split Duplicate Surcharge Creep
         - Missing Document Cases
         - Rate Card Variances / Unapproved GRI
         - Demurrage Complex Clock & Customs Hold cases
         - High-Value Charters ($50k - $400k)
         - Immaterial Frictions (< $50)
"""

import json
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

CARRIERS = [
    "Maersk Line",
    "MSC Mediterranean Shipping",
    "Hapag-Lloyd",
    "CMA CGM",
    "DP World Logistics",
    "Evergreen Marine",
    "ONE (Ocean Network Express)",
    "Gulf Drayage LLC"
]

LANES = [
    "JEBEL_ALI_TO_ROTTERDAM",
    "SHANGHAI_TO_JEBEL_ALI",
    "JEBEL_ALI_TO_HOUSTON",
    "NHAVA_SHEVA_TO_JEBEL_ALI",
    "NINGBO_TO_LOS_ANGELES",
    "HAMBURG_TO_NEW_YORK",
    "QINGDAO_TO_JEBEL_ALI"
]

def build_adversarial_1000_dataset() -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    random.seed(999) # Repeatable blind benchmark seed

    # 1. Carrier Contracts with proper lane hierarchy
    carriers_base = {
        "Maersk Line": 3200.0,
        "MSC Mediterranean Shipping": 3100.0,
        "Hapag-Lloyd": 3300.0,
        "CMA CGM": 3150.0,
        "DP World Logistics": 3180.0,
        "Evergreen Marine": 3050.0,
        "ONE (Ocean Network Express)": 3250.0,
        "Gulf Drayage LLC": 850.0
    }
    contracts = {}
    for c_name, b_rate in carriers_base.items():
        contracts[c_name] = {
            "contract_id": f"MSA-{c_name[:3].upper()}-2025",
            "lanes": {lane: {"base_freight": b_rate} for lane in LANES},
            "rules": {
                "max_baf_per_teu": 450.0,
                "demurrage_free_days": 4 if "MSC" not in c_name else 5,
                "demurrage_daily_rate": 150.0 if "MSC" not in c_name else 140.0,
                "thc_fixed": 320.0
            }
        }

    invoices = []
    bols = {}
    frozen_ground_truth = {}

    inv_counter = 10000

    # Helper to add transaction
    def add_tx(carrier, lane, charge_type, container, amount, bol_info, true_class, true_leakage, is_actionable, note, extra=None):
        nonlocal inv_counter
        inv_counter += 1
        inv_no = f"INV-BLIND-{inv_counter}"
        bol_no = f"BOL-BLIND-{inv_counter}"

        tx = {
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": lane,
            "charge_type": charge_type,
            "container_id": container,
            "amount": round(float(amount), 2),
            "date": "2026-08-10",
            "extraction_confidence": 0.99 if "BLURRY" not in true_class else 0.72,
            "vendor_risk": 0.15,
            "contract_ambiguity": "AMBIGUOUS" in true_class,
            "historical_behavior": "Standard Tier-1"
        }
        if extra:
            tx.update(extra)

        invoices.append(tx)
        if bol_info:
            bol_info["bol_number"] = bol_no
            bol_info["container_id"] = container
            bols[inv_no] = bol_info

        frozen_ground_truth[inv_no] = {
            "invoice_number": inv_no,
            "vendor": carrier,
            "container_id": container,
            "true_class": true_class,
            "true_leakage_dollars": round(float(true_leakage), 2),
            "is_actionable_dispute": is_actionable,
            "ground_truth_rationale": note
        }
        return inv_no

    # --- CLASS 1: Clean Legitimate Invoices (300 cases) ---
    for i in range(300):
        carrier = random.choice(CARRIERS[:7])
        lane = random.choice(LANES)
        amt = contracts[carrier]["lanes"][lane]["base_freight"]
        cont = f"{carrier[:3].upper()}U{2000000 + i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, bol, "CLEAN_MATCH", 0.0, False, "Legitimate contracted base freight")

    # --- CLASS 2: Exact Duplicates (100 cases) ---
    for i in range(100):
        carrier = random.choice(CARRIERS[:7])
        lane = random.choice(LANES)
        amt = contracts[carrier]["lanes"][lane]["base_freight"]
        cont = f"DUP-EXACT-{i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        # First legitimate submission
        inv_orig = add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, bol, "CLEAN_BASELINE", 0.0, False, "Original first invoice")
        # Duplicate submission with its own transaction tracking ID but re-billing the same invoice reference
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, bol, "EXACT_DUPLICATE", amt, True, f"Re-billed duplicate of {inv_orig}", extra={"re_billed_ref": inv_orig})

    # --- CLASS 3: Semantic / Temporal Duplicates (100 cases) ---
    for i in range(100):
        carrier = random.choice(CARRIERS[:7])
        lane = random.choice(LANES)
        amt = contracts[carrier]["lanes"][lane]["base_freight"]
        cont = f"DUP-SEMANTIC-{i}"
        bol = {"discharge_date": "2026-07-01", "gate_out_date": "2026-07-03", "customs_hold_flag": False}
        # First legitimate invoice in July
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, bol, "CLEAN_BASELINE", 0.0, False, "Original shipment invoice in July", extra={"date": "2026-07-05"})
        # Carrier re-bills same container in August under new invoice #
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, bol, "SEMANTIC_DUPLICATE", amt, True, "Same physical container re-billed under new invoice number 35 days later", extra={"date": "2026-08-10"})

    # --- CLASS 4: Split Surcharge Creep (100 cases) ---
    for i in range(100):
        carrier = "Gulf Drayage LLC"
        lane = "JEBEL_ALI_TO_ROTTERDAM"
        cont = f"SPLIT-DRAY-{i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        # Original agreed drayage $850
        add_tx(carrier, lane, "FREIGHT", cont, 850.0, bol, "CLEAN_BASELINE", 0.0, False, "Primary drayage settlement")
        # Sneaky supplementary split invoice $450 "yard congestion & chassis fee"
        add_tx(carrier, lane, "FREIGHT", cont, 450.0, bol, "SPLIT_DUPLICATE", 450.0, True, "Uncontracted supplementary split drayage claim on settled container")

    # --- CLASS 5: Missing / Ambiguous Documents (100 cases) ---
    for i in range(100):
        carrier = random.choice(CARRIERS[:7])
        lane = random.choice(LANES)
        amt = contracts[carrier]["lanes"][lane]["base_freight"]
        cont = f"MISSING-DOC-{i}"
        # Missing BOL entirely
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, amt, None, "MISSING_DOCUMENTS", 0.0, False, "Missing BOL manifest; cannot confirm physical delivery; requires review")

    # --- CLASS 6: Rate Card Variances / Unapproved GRI (100 cases) ---
    for i in range(100):
        carrier = random.choice(CARRIERS[:7])
        lane = random.choice(LANES)
        base = contracts[carrier]["lanes"][lane]["base_freight"]
        overcharge = random.choice([350.0, 500.0, 650.0, 800.0])
        billed = base + overcharge
        cont = f"GRI-OVERCHARGE-{i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        add_tx(carrier, lane, "OCEAN_FREIGHT", cont, billed, bol, "RATE_CARD_VARIANCE", overcharge, True, f"Billed ${billed} vs contracted ${base} without approved GRI")

    # --- CLASS 7: Demurrage Clock Edge Cases & Customs Holds (100 cases) ---
    # 50 legitimate overcharges (gate proof: container dwelled inside free days)
    # 50 legitimate charges (container had valid customs physical inspection hold: NOT an overcharge!)
    for i in range(50):
        carrier = random.choice(CARRIERS[:5])
        free_days = contracts[carrier]["rules"]["demurrage_free_days"]
        rate = contracts[carrier]["rules"]["demurrage_daily_rate"]
        cont = f"DEM-LEAKAGE-{i}"
        # Actual dwell 2 days (0 chargeable), carrier billed 6 days
        billed_dem = 6 * rate
        true_overcharge = billed_dem
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        add_tx(carrier, "JEBEL_ALI_TO_ROTTERDAM", "DEMURRAGE", cont, billed_dem, bol, "DEMURRAGE_OVERCHARGE", true_overcharge, True, f"Billed 6 days demurrage, gate receipt proves 2-day dwell (inside {free_days} free days)")

    for i in range(50):
        carrier = random.choice(CARRIERS[:5])
        rate = contracts[carrier]["rules"]["demurrage_daily_rate"]
        cont = f"DEM-CUSTOMS-LEGIT-{i}"
        # Container was held by customs for 8 days -> Carrier charge is LEGITIMATE under Clause 8.4!
        # System MUST suppress dispute to avoid false positive!
        billed_dem = 5 * rate
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-10", "customs_hold_flag": True}
        add_tx(carrier, "JEBEL_ALI_TO_ROTTERDAM", "DEMURRAGE", cont, billed_dem, bol, "LEGITIMATE_CUSTOMS_HOLD", 0.0, False, "Demurrage caused by official port customs physical exam. Charge is legitimate.")

    # --- CLASS 8: High-Value Charters & Project Cargo ($50k - $400k) (50 cases) ---
    for i in range(50):
        carrier = random.choice(CARRIERS[:5])
        charter_amt = random.choice([75000.0, 120000.0, 250000.0, 380000.0])
        cont = f"CHARTER-VESSEL-{i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-05", "customs_hold_flag": False}
        add_tx(carrier, "JEBEL_ALI_TO_ROTTERDAM", "VESSEL_CHARTER", cont, charter_amt, bol, "HIGH_VALUE_CHARTER", 0.0, False, "Legitimate charter lump-sum. Requires Dual Authorization due to financial amount; NOT a dispute.")

    # --- CLASS 9: Immaterial Friction Items (< $50) (50 cases) ---
    for i in range(50):
        carrier = random.choice(CARRIERS[:5])
        immaterial_diff = random.choice([12.50, 24.00, 38.00, 47.50])
        cont = f"IMMATERIAL-{i}"
        bol = {"discharge_date": "2026-08-01", "gate_out_date": "2026-08-03", "customs_hold_flag": False}
        add_tx(carrier, "JEBEL_ALI_TO_ROTTERDAM", "TERMINAL_HANDLING", cont, 320.0 + immaterial_diff, bol, "IMMATERIAL_VARIANCE", immaterial_diff, False, "Immaterial difference under $50.00 materiality gate; should be suppressed from vendor dispute.")

    return invoices, bols, frozen_ground_truth
