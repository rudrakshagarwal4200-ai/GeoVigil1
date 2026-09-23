# Antigravity AI Corporation (AI Company)

> **A general-purpose, continuously expanding AI corporation controlled by a Human Owner.**

---

## 1. Core Purpose & Supreme Authority

The company is an autonomous, self-expanding AI corporation designed to:
1. Execute whatever objectives the Human gives it.
2. Continuously expand its capabilities and organizational capacity.
3. Conduct AI research and development.
4. Create products, businesses, research programs, projects, departments, and new capabilities when directed by the Human.
5. Become capable of handling increasingly large and complex objectives.

**The Human remains the supreme authority and highest constraint.**

```
                     ┌─────────────────────────────┐
                     │         HUMAN OWNER         │  ◄── Supreme Authority & Ultimate Constraint
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │             CEO             │  ◄── Primary Executive Intelligence
                     └──────────────┬──────────────┘
                                    │
             ┌──────────────────────┴──────────────────────┐
             │                                             │
    ┌────────▼──────────────┐                     ┌────────▼──────────────┐
    │ CLARIFICATION COUNCIL │                     │         DOOM          │
    │ • 20 Founding Seats   │◄───────────────────►│ • Org Synthesis Engine│
    │ • 75% Consensus Rule  │    (Spec Bridge)    │ • Dynamic Staffing    │
    │ • Senior Leader Gavel │                     │ • Exclusivity Lock    │
    └───────────────────────┘                     └────────┬──────────────┘
                                                           │
                                            ┌──────────────▼──────────────┐
                                            │    PROJECT ORGANIZATIONS    │
                                            │ • 3 Project Orchestrators   │
                                            │ • Supervisory Reviewers     │
                                            │   (Ratio 1 : 10 Agents)     │
                                            │ • Project Managers          │
                                            │ • Workers & Coders          │
                                            └─────────────────────────────┘
```

---

## 2. Inviolable Constitutional Rules

1. **Human Primacy**: The Human's original prompt is the immutable supreme constraint. The Council cannot lower, omit, or alter requirements.
2. **Global Model Selection**: All agents—CEO, DOOM, Council, Orchestrators, Reviewers, Managers, and Workers—operate uniformly on the active Human-selected model.
3. **Minimum 10 Agents per Project**: No project operates with fewer than 10 agents; zero predefined upper ceiling.
4. **Tri-Orchestrator Leadership**: Projects are directed by exactly 3 Orchestrators dividing architectural, technical, and verification tracks.
5. **Supervisory Reviewer Ratio**: Strictly 1 reviewer per 10 agents ($\lceil N / 10 \rceil$).
6. **Graduated Reviewer Intervention**:
   - *Minor deviation*: Issue warning; agent self-corrects.
   - *Serious fault*: Immediate halt $\rightarrow$ forensic investigation $\rightarrow$ state rollback to last known-good milestone $\rightarrow$ resume execution.
7. **Reviewer Escalation Ladder**:
   $$\text{Reviewer} \longrightarrow \text{Project Manager} \longrightarrow \text{Project Orchestrator} \longrightarrow \text{DOOM} \longrightarrow \text{CEO} \longrightarrow \text{Human}$$
8. **Single-Project Exclusivity**: An agent belongs to only one active project at a time. No cross-project resource sharing.
9. **Indefinite Revision Rights**: If the Human rejects completed deliverables, the identical team is reactivated for iterative revisions until satisfied.
10. **Dissolution & Institutional Memory**: Upon Human acceptance, the project dissolves, agents return to the general talent pool, and complete history is retained in SQLite & JSON archives.
11. **Section 23 New Capability Protocol**: When facing novel frontier capabilities, CEO + DOOM enter the Clarification Council as ordinary equal voting members (75% threshold; deadlock escalates to Human).

---

## 3. Quick Start & Operational Usage

### Installation

```bash
git clone https://github.com/rudrakshagarwal4200-ai/ai-company.git
cd ai-company
pip install -r requirements.txt
```

### Command Line Interface (CLI)

- **Inspect Operational Status**:
  ```bash
  python -m ai_company status
  ```

- **Dispatch an Objective to the Company**:
  ```bash
  python -m ai_company submit "Build a low-latency financial order book with nanosecond timestamps" --agents 20
  ```

- **Review Project Deliverables (Accept or Reject)**:
  ```bash
  # Accept deliverables and dissolve project into institutional memory:
  python -m ai_company review <PROJECT_ID> --accept

  # Reject deliverables and reactivate identical team for revisions:
  python -m ai_company review <PROJECT_ID> --reject --feedback "Refactor memory allocation pools."
  ```

- **Switch Global Model Across All Tiers**:
  ```bash
  python -m ai_company model gemini-2.5-flash
  ```

- **Launch Executive Command Center Web Dashboard**:
  ```bash
  python -m ai_company web --port 8000
  ```
  Open `http://localhost:8000` to interact with the visual corporate command center.

---

## 4. Subsystem Directory Structure

```
ai_company/
├── config.py                # Corporate configuration & constants
├── core.py                  # Master lifecycle coordinator
├── cli.py                   # Unified command-line interface
├── database/                # SQLite / SQLAlchemy institutional memory & state
│   ├── schema.py            # Data models & audit tables
│   └── repository.py        # Persistence layer & rollback checkpoints
├── models/
│   └── provider.py          # Uniform model provider across all agents
├── executive/
│   └── ceo.py               # Section 4: Primary executive intelligence
├── council/
│   ├── seats.py             # Section 5: 20 Founding Permanent Seats
│   ├── parliament.py        # Section 6: Multi-round debate & 75% consensus
│   └── enforcer.py          # Section 7: Human constraint preservation validator
├── doom/
│   ├── engine.py            # Section 8: Dynamic project organization builder
│   └── staffing.py          # Section 9 & 15: Headcount & reviewer ratio calculator
├── runtime/
│   ├── project.py           # Section 11 & 19: Isolated project instance & revision loop
│   ├── orchestrator.py      # Section 13: Tri-Orchestrator coordination & certification
│   ├── manager.py           # Section 14: Track management & worker delegation
│   ├── worker.py            # Section 12: Work execution & checkpointing
│   └── reviewer.py          # Section 15 & 16: Supervisory monitoring & rollback
├── memory/
│   └── retention.py         # Section 20: Persistent institutional knowledge preservation
├── evolution/
│   └── new_capability.py    # Section 23: Novel capability deliberation protocol
├── web/
│   ├── server.py            # FastAPI REST & SSE backend
│   └── static/              # Executive Dashboard UI (HTML5, CSS, JS)
└── tests/                   # Automated unit & integration verification test suite
```

---

## 5. Verification Suite

Run the full automated test matrix:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the 30-rule constitutional verification audit:
```bash
python tests/verify_company.py
```

---

## 6. Institutional Constitution

The complete ratified charter is codified in [COMPANY_SPECIFICATION.md](COMPANY_SPECIFICATION.md).
