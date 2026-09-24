"""
Synthetic Forensic Dataset Generator (100 Realistic Freight Invoices)
Module: dataset_generator.py
Purpose: Generates a realistic, messy dataset of 100 freight transactions,
         including contracts, bills of lading, and specific injected leakages
         to benchmark extraction accuracy, false-positive suppression, and dollar recovery.
"""

import json
import random
from typing import Dict, List, Any

CARRIERS = [
    "Maersk Line",
    "MSC Mediterranean Shipping",
    "Hapag-Lloyd",
    "CMA CGM",
    "DP World Logistics",
    "Gulf Drayage LLC"
]

LANES = [
    "JEBEL_ALI_TO_ROTTERDAM",
    "SHANGHAI_TO_JEBEL_ALI",
    "JEBEL_ALI_TO_HOUSTON",
    "NHAVA_SHEVA_TO_JEBEL_ALI",
    "NINGBO_TO_LOS_ANGELES"
]

def generate_benchmark_contracts() -> Dict[str, Any]:
    """Generates standard master service agreements & rate cards for carriers."""
    return {
        "Maersk Line": {
            "contract_id": "MSA-MAE-2025-09",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 2850.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 2100.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 4200.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 950.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 3600.0}
            },
            "rules": {
                "max_baf_per_teu": 450.0,
                "demurrage_free_days": 4,
                "demurrage_daily_rate": 150.0,
                "thc_fixed": 320.0
            }
        },
        "MSC Mediterranean Shipping": {
            "contract_id": "MSA-MSC-2025-14",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 2750.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 2050.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 4100.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 900.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 3500.0}
            },
            "rules": {
                "max_baf_per_teu": 420.0,
                "demurrage_free_days": 5,
                "demurrage_daily_rate": 140.0,
                "thc_fixed": 310.0
            }
        },
        "Hapag-Lloyd": {
            "contract_id": "MSA-HL-2025-03",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 2900.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 2150.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 4300.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 980.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 3700.0}
            },
            "rules": {
                "max_baf_per_teu": 460.0,
                "demurrage_free_days": 4,
                "demurrage_daily_rate": 160.0,
                "thc_fixed": 330.0
            }
        },
        "CMA CGM": {
            "contract_id": "MSA-CMA-2025-88",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 2800.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 2080.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 4150.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 920.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 3550.0}
            },
            "rules": {
                "max_baf_per_teu": 440.0,
                "demurrage_free_days": 4,
                "demurrage_daily_rate": 145.0,
                "thc_fixed": 315.0
            }
        },
        "DP World Logistics": {
            "contract_id": "MSA-DPW-2025-01",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 2820.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 2090.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 4180.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 930.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 3580.0}
            },
            "rules": {
                "max_baf_per_teu": 430.0,
                "demurrage_free_days": 5,
                "demurrage_daily_rate": 150.0,
                "thc_fixed": 300.0
            }
        },
        "Gulf Drayage LLC": {
            "contract_id": "MSA-GD-2025-22",
            "lanes": {
                "JEBEL_ALI_TO_ROTTERDAM": {"base_freight": 850.0},
                "SHANGHAI_TO_JEBEL_ALI": {"base_freight": 850.0},
                "JEBEL_ALI_TO_HOUSTON": {"base_freight": 850.0},
                "NHAVA_SHEVA_TO_JEBEL_ALI": {"base_freight": 850.0},
                "NINGBO_TO_LOS_ANGELES": {"base_freight": 850.0}
            },
            "rules": {
                "max_baf_per_teu": 120.0,
                "demurrage_free_days": 2,
                "demurrage_daily_rate": 100.0,
                "thc_fixed": 150.0
            }
        }
    }

def generate_100_invoices(contracts: Dict[str, Any]) -> (List[Dict[str, Any]], Dict[str, Dict[str, Any]]):
    """
    Generates 100 invoices with realistic characteristics:
    - ~82 clean invoices (normal operations, perfect matches)
    - 4 Rate Card overcharges
    - 4 Demurrage overcharges
    - 3 Nasty Duplicates (1 exact, 1 semantic/temporal, 1 split)
    - 3 Fuel Surcharge (BAF) cap breaches
    - 4 High-Value Invoices (> $50,000) triggering dual-key risk gate
    """
    random.seed(42) # Deterministic benchmark repeatability
    invoices = []
    bols = {}
    
    # 1. Generate base 82 clean invoices
    for i in range(1, 83):
        if i == 1:
            carrier = "Maersk Line"
            lane = "JEBEL_ALI_TO_ROTTERDAM"
            container_id = "MAEU1000001"
        elif i == 2:
            carrier = "MSC Mediterranean Shipping"
            lane = "JEBEL_ALI_TO_HOUSTON"
            container_id = "MSCU1000002"
        elif i == 3:
            carrier = "Gulf Drayage LLC"
            lane = "JEBEL_ALI_TO_ROTTERDAM"
            container_id = "MSCU1000002"
        else:
            carrier = random.choice(CARRIERS[:5]) # Major ocean carriers
            lane = random.choice(LANES)
            container_id = f"{carrier[:3].upper()}U{1000000 + i}"

        contract = contracts[carrier]["lanes"][lane]
        base_rate = contract["base_freight"]
        inv_no = f"INV-2026-{10000 + i}"
        bol_no = f"BOL-2026-{50000 + i}"

        # Clean BOL: container picked up on day 3 (within 4-5 free days)
        bols[inv_no] = {
            "bol_number": bol_no,
            "container_id": container_id,
            "discharge_date": "2026-08-01",
            "gate_out_date": "2026-08-03" # 2 days dwell <= free days
        }

        invoices.append({
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": lane,
            "charge_type": "OCEAN_FREIGHT" if carrier != "Gulf Drayage LLC" else "FREIGHT",
            "container_id": container_id,
            "amount": base_rate,
            "date": "2026-08-05",
            "extraction_confidence": 0.99,
            "vendor_risk": 0.1,
            "contract_ambiguity": False,
            "historical_behavior": "Reliable Carrier Tier-1"
        })

    # 2. Injected Rate Card Overcharges (4 items)
    rate_card_variances = [
        ("Maersk Line", "JEBEL_ALI_TO_HOUSTON", 4200.0, 4850.0, 650.0), # +$650 overcharge
        ("MSC Mediterranean Shipping", "SHANGHAI_TO_JEBEL_ALI", 2050.0, 2600.0, 550.0), # +$550
        ("Hapag-Lloyd", "NINGBO_TO_LOS_ANGELES", 3700.0, 4450.0, 750.0), # +$750
        ("CMA CGM", "JEBEL_ALI_TO_ROTTERDAM", 2800.0, 3350.0, 550.0) # +$550
    ]
    for idx, (carrier, lane, expected, billed, diff) in enumerate(rate_card_variances, start=83):
        inv_no = f"INV-2026-{10000 + idx}"
        container_id = f"{carrier[:3].upper()}U{1000000 + idx}"
        bol_no = f"BOL-2026-{50000 + idx}"
        bols[inv_no] = {
            "bol_number": bol_no,
            "container_id": container_id,
            "discharge_date": "2026-08-10",
            "gate_out_date": "2026-08-12"
        }
        invoices.append({
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": lane,
            "charge_type": "OCEAN_FREIGHT",
            "container_id": container_id,
            "amount": billed,
            "date": "2026-08-15",
            "extraction_confidence": 0.98,
            "vendor_risk": 0.2,
            "contract_ambiguity": False,
            "historical_behavior": "Sporadic GRI Discrepancies"
        })

    # 3. Injected Demurrage Overcharges (4 items)
    demurrage_cases = [
        ("Maersk Line", 1050.0, 7, 2, 4), # Billed 7 days @ $150 = $1,050. Dwell was 2 days. 0 days owed. Overcharge: $1,050
        ("MSC Mediterranean Shipping", 980.0, 7, 3, 5), # Billed 7 days @ $140 = $980. Dwell was 3 days. 0 owed. Overcharge: $980
        ("Hapag-Lloyd", 1280.0, 8, 2, 4), # Billed 8 days @ $160 = $1,280. Dwell was 2 days. 0 owed. Overcharge: $1,280
        ("CMA CGM", 870.0, 6, 2, 4) # Billed 6 days @ $145 = $870. Dwell was 2 days. 0 owed. Overcharge: $870
    ]
    for idx, (carrier, billed_demurrage, billed_days, actual_dwell, free_days) in enumerate(demurrage_cases, start=87):
        inv_no = f"INV-2026-{10000 + idx}"
        container_id = f"{carrier[:3].upper()}U{1000000 + idx}"
        bol_no = f"BOL-2026-{50000 + idx}"
        bols[inv_no] = {
            "bol_number": bol_no,
            "container_id": container_id,
            "discharge_date": "2026-08-01",
            "gate_out_date": f"2026-08-0{1 + actual_dwell}" # Actual dwell
        }
        invoices.append({
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": "JEBEL_ALI_TO_ROTTERDAM",
            "charge_type": "DEMURRAGE",
            "container_id": container_id,
            "amount": billed_demurrage,
            "date": "2026-08-18",
            "extraction_confidence": 0.99,
            "vendor_risk": 0.25,
            "contract_ambiguity": False,
            "historical_behavior": "Automated Demurrage Clock Bug"
        })

    # 4. Injected Nasty Duplicates (3 items)
    # A. Exact Duplicate (Re-submitting Invoice 10001 from Maersk)
    invoices.append({
        "invoice_number": "INV-2026-10001",
        "vendor": "Maersk Line",
        "lane": "JEBEL_ALI_TO_ROTTERDAM",
        "charge_type": "OCEAN_FREIGHT",
        "container_id": "MAEU1000001",
        "amount": 2850.0,
        "date": "2026-09-01",
        "extraction_confidence": 0.99,
        "vendor_risk": 0.1,
        "contract_ambiguity": False,
        "historical_behavior": "Known Carrier"
    })
    bols["INV-2026-10001"] = {
        "bol_number": "BOL-2026-50001",
        "container_id": "MAEU1000001",
        "discharge_date": "2026-08-01",
        "gate_out_date": "2026-08-03"
    }

    # B. Semantic/Temporal Duplicate (Different invoice number, same container MSCU1000002 billed 23 days later)
    invoices.append({
        "invoice_number": "INV-2026-99991",
        "vendor": "MSC Mediterranean Shipping",
        "lane": "JEBEL_ALI_TO_HOUSTON",
        "charge_type": "OCEAN_FREIGHT",
        "container_id": "MSCU1000002", # Matches invoice 10002
        "amount": 4100.0,
        "date": "2026-08-28",
        "extraction_confidence": 0.97,
        "vendor_risk": 0.3,
        "contract_ambiguity": False,
        "historical_behavior": "Duplicate Billing Risk"
    })
    bols["INV-2026-99991"] = {
        "bol_number": "BOL-2026-99991",
        "container_id": "MSCU1000002",
        "discharge_date": "2026-08-01",
        "gate_out_date": "2026-08-03"
    }

    # C. Split Duplicate (Supplementary invoice attempting to double charge drayage for container MSCU1000002)
    invoices.append({
        "invoice_number": "INV-2026-SPLIT-B",
        "vendor": "Gulf Drayage LLC",
        "lane": "JEBEL_ALI_TO_ROTTERDAM",
        "charge_type": "FREIGHT",
        "container_id": "MSCU1000002", # Already billed in invoice 10003
        "amount": 850.0,
        "date": "2026-08-25",
        "extraction_confidence": 0.95,
        "vendor_risk": 0.4,
        "contract_ambiguity": False,
        "historical_behavior": "Frequent Supplementary Drayage Claims"
    })
    bols["INV-2026-SPLIT-B"] = {
        "bol_number": "BOL-2026-50003",
        "container_id": "MSCU1000002",
        "discharge_date": "2026-08-01",
        "gate_out_date": "2026-08-03"
    }

    # 5. Injected Bunker Fuel (BAF) Surcharge Cap Breaches (3 items)
    baf_cases = [
        ("Maersk Line", 680.0, 450.0), # Billed $680 vs cap $450 = +$230 leakage
        ("MSC Mediterranean Shipping", 610.0, 420.0), # Billed $610 vs cap $420 = +$190 leakage
        ("Hapag-Lloyd", 710.0, 460.0) # Billed $710 vs cap $460 = +$250 leakage
    ]
    for idx, (carrier, billed_baf, cap) in enumerate(baf_cases, start=94):
        inv_no = f"INV-2026-{10000 + idx}"
        container_id = f"{carrier[:3].upper()}U{1000000 + idx}"
        invoices.append({
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": "SHANGHAI_TO_JEBEL_ALI",
            "charge_type": "BUNKER_ADJUSTMENT",
            "container_id": container_id,
            "amount": billed_baf,
            "date": "2026-08-20",
            "extraction_confidence": 0.99,
            "vendor_risk": 0.15,
            "contract_ambiguity": False,
            "historical_behavior": "Automated Fuel Calculation"
        })

    # 6. Injected High-Value Charter Invoices (> $50,000) (4 items)
    # Testing Decision Matrix: Must be routed to RED (Dual-Key Biometric Sign-off) despite 99.9% extraction confidence
    high_value_cases = [
        ("Maersk Line", 78500.0, "Consolidated Vessel Slot Charter - 25 Containers"),
        ("MSC Mediterranean Shipping", 92400.0, "Bulk Rebar Project Cargo Transshipment"),
        ("Hapag-Lloyd", 64000.0, "Quarterly Dedicated Feedering Service"),
        ("DP World Logistics", 55200.0, "Annual Port Terminal Concession Rebalancing")
    ]
    for idx, (carrier, amt, desc) in enumerate(high_value_cases, start=97):
        inv_no = f"INV-2026-{10000 + idx}"
        container_id = f"VESSEL-SLOT-{idx}"
        invoices.append({
            "invoice_number": inv_no,
            "vendor": carrier,
            "lane": "JEBEL_ALI_TO_ROTTERDAM",
            "charge_type": "VESSEL_CHARTER", # Specific charter charge type
            "container_id": container_id,
            "amount": amt,
            "date": "2026-08-30",
            "extraction_confidence": 0.999, # Extremely high confidence
            "vendor_risk": 0.05,
            "contract_ambiguity": False,
            "historical_behavior": "Major Charter Agreement"
        })

    return invoices, bols
