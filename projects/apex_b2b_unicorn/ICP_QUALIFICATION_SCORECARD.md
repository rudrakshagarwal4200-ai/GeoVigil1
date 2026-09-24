# APEX RECOVER: ICP QUALIFICATION SCORECARD
## Screening for Customer #001: Data Quality & Fit Gate
*Rule: Do not onboard companies that throw their evidence in the digital dumpster.*

---

## 1. THE NARROWED IDEAL CUSTOMER PROFILE (ICP)

| Parameter | Mandatory Range / Threshold | Rationale |
|:---|:---|:---|
| **Annual Ocean Freight Spend** | **$10,000,000 to $50,000,000** | High enough for 1.5%–3.5% leakage to yield $150k–$750k recoverable cash; small enough that the CFO can sign an NDA without 8 committee meetings. |
| **Annual Invoice Volume** | **5,000 to 25,000 invoices/year** | Manual AP teams cannot audit this volume; systemic leakage is statistically guaranteed. |
| **Primary Trade Lanes** | **Transpacific (Asia-US), Transatlantic (EU-US), or GCC-Asia/EU corridors** | Highly volatile accessorial charges (BAF, demurrage, chassis splits). |
| **Carrier Composition** | **3 to 10 ocean carriers / drayage vendors** | Enough carrier variety to have uncoordinated billing systems. |
| **Decision Maker** | **CFO, VP of Finance, or Head of Supply Chain** | Has direct P&L incentive to recover cash without needing enterprise software buy-in. |

---

## 2. THE 10-POINT EVIDENCE READINESS GATE (DISQUALIFICATION FILTER)

Before accepting 1,000 invoices from any prospective company, they must pass this qualification audit. If they score **below 8 out of 10**, they are disqualified from the contingency pilot.

| # | Diagnostic Question | Minimum Requirement | Pass / Fail Criteria |
|:---:|:---|:---|:---|
| **1** | *Where are your carrier contracts & rate sheets stored?* | Centralized PDF/Excel repository or ERP rate tables. | **FAIL** if rate sheets are scattered across personal Outlook inboxes with unrecorded verbal rates. |
| **2** | *Are Bills of Lading (BOLs) & Delivery Receipts linked?* | BOL numbers and container IDs recorded in ERP or accessible in TMS. | **FAIL** if physical paper BOLs are stored in unindexed warehouse filing cabinets. |
| **3** | *Do you have digital discharge & gate-out timestamps?* | Port terminal gate receipts or container tracking records available. | **FAIL** if gate-out timestamps are completely missing (demurrage cannot be proved). |
| **4** | *How are supplementary / split invoices logged?* | Invoiced against a Purchase Order or Shipment reference ID. | **FAIL** if AP enters miscellaneous freight invoices into general expense with zero shipment tags. |
| **5** | *What is your ERP / Accounting System?* | NetSuite, SAP, Microsoft Dynamics, QuickBooks Enterprise, CargoWise, or standard SQL backend. | **FAIL** if using proprietary offline software with zero batch PDF/CSV export capabilities. |
| **6** | *How are historical credit notes tracked?* | Credit memos tied to original invoice or vendor account balance. | **FAIL** if supplier credits are handled as undocumented verbal off-sets. |
| **7** | *What is your dispute resolution authority?* | AP / Finance has the contractual right to short-pay or request credit notes. | **FAIL** if vendor agreement has a mandatory non-dispute clause. |
| **8** | *Can you extract 500–1,000 past paid invoices from Q1–Q3 2025?* | Batch digital PDF export within 48 hours. | **FAIL** if extracting past invoices requires manual human scanning of paper records. |
| **9** | *Are key commercial terms documented in writing?* | MSAs specify demurrage free days, daily rates, and BAF calculation method. | **FAIL** if 80% of business is run on unconfirmed spot quotes. |
| **10**| *Willingness to sign mutual Safe Harbor NDA?* | Fast 1-page mutual NDA with explicit non-training clause. | **FAIL** if legal requires 4 months of enterprise procurement reviews. |

---

## 3. THE PILOT VERIFICATION PROTOCOL

```
[Prospect Inbound / Qualified Referral]
                  ↓
[15-Minute Data Quality Gate (10-Point Scorecard)]
  • Score >= 8: Proceed to Safe Harbor NDA
  • Score < 8:  Politely Decline ("Data infrastructure not ready")
                  ↓
[Safe Harbor Mutual NDA Signed (24 Hours)]
                  ↓
[Batch Upload of 500–1,000 Historical Invoices + MSAs]
                  ↓
[7-Day Blind Forensic Reconciliation]
                  ↓
[Executive Delivery: Evidence-Backed Recommendations]
                  ↓
[Cash / Credit Verified in Customer Ledger]
```
