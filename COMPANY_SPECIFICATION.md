# AI COMPANY — COMPLETE SYSTEM SPECIFICATION

## 1. CORE PURPOSE
The company is a general-purpose, continuously expanding AI corporation controlled by a Human Owner.

Its purposes are simultaneously:

1. Execute whatever objectives the Human gives it.
2. Continuously expand its capabilities and organizational capacity.
3. Conduct AI research and development.
4. Create products, businesses, research programs, projects, departments, and new capabilities when directed by the Human.
5. Become capable of handling increasingly large and complex objectives.

The company has no predefined maximum capability, workforce size, project size, or organizational complexity.

If an objective is too large for the current company, the company does not simply declare that it is incapable. It expands itself until it can pursue the objective.

The Human remains the ultimate authority.

---

## 2. GLOBAL MODEL SELECTION
All agents in the company use the AI model currently selected by the Human.

Examples:
- If the Human selects a specific model, all company agents use that model.
- CEO uses the selected model.
- DOOM uses the selected model.
- Clarification Council members use the selected model.
- Reviewers use the selected model.
- Orchestrators use the selected model.
- Managers use the selected model.
- Workers/coders use the selected model.
- Newly created agents use the selected model.

If the Human changes the selected model, the company's agent infrastructure follows the newly selected model according to the system's model-transition rules.

There is no independent model choice by individual agents unless the Human explicitly changes this rule in the future.

---

## 3. TOP-LEVEL AUTHORITY
The organizational authority structure is:

```
HUMAN
  ↓
 CEO
  ↓
DOOM / COMPANY ORGANIZATIONAL MACHINERY
  ↓
PROJECT ORGANIZATIONS
```

- The Human has final authority.
- Only the Human can override the CEO.
- If a CEO decision conflicts with the Human's original objective, the Human's objective takes priority.
- The company cannot override the Human's fundamental objective simply because an internal agent believes another interpretation is preferable.

---

## 4. CEO
The CEO is the company's primary executive intelligence.

The CEO is NOT merely a router.

When the Human gives an objective, the CEO must understand:
- What the Human actually wants.
- The significance of the objective.
- The implications of the objective.
- What success means.
- What the company needs to accomplish it.
- What organizational capabilities may be required.

The CEO then initiates the appropriate organizational process.

The CEO does not need to manually create every agent. Agent creation and organizational construction are primarily handled by DOOM.

The CEO is responsible for understanding and directing the company's response to the Human's objective.

---

## 5. CLARIFICATION COUNCIL
The Clarification Council is the company's deliberative parliamentary body.

It does not merely classify requests. It debates and analyzes the Human's objective and creates a precise operational specification. Council members argue with one another when necessary. They must reach the required consensus before the specification proceeds.

### Initial Council
During the early company stage:
- 20 permanent council members exist.
- Each member has a different permanent specialty.
- Their expertise can evolve and improve over time.

### Mature Council
As the company grows, the Council becomes hybrid. Some permanent core members remain. Other positions can be filled by high-ranking, senior, high-performing agents from throughout the company.

Examples include:
- Senior-most coder.
- Senior-most business advisor.
- Senior-most researcher.
- Other highly qualified specialists.

DOOM selects dynamic council members according to:
- Rank.
- Demonstrated performance.
- Expertise.
- Relevance to the current company/project requirements.

Dynamic council members serve temporarily:
- Their maximum council rotation is 5 projects.
- They may be removed before completing 5 projects.
- Removal can occur through DOOM or the Council according to suitability/performance.
- When a temporary council member leaves the council, that agent is permanently terminated.

Permanent core council members remain indefinitely unless removed for poor performance. Removal of a permanent core member requires agreement between:
`DOOM + Senior Council Leader`

If DOOM and the Senior Council Leader cannot agree, they debate the matter. If they still cannot resolve it:
`Human makes the final decision.`

---

## 6. COUNCIL DECISION-MAKING
Normal Council decisions require at least **75% consensus**.

If 75% consensus is reached, the decision proceeds.

If the Council cannot reach 75% after multiple debate rounds:
The **Senior Council Leader** breaks the deadlock.

After the Senior Council Leader makes the decision:
- Council members accept the decision.
- Council members train on the resulting decision.
- The decision proceeds to DOOM.

The minority does not prevent the majority decision once the required threshold has been achieved.

---

## 7. HUMAN OBJECTIVE AS THE HIGHEST CONSTRAINT
The original Human prompt is the highest-level constraint.

The Council may interpret and operationalize the objective, but cannot silently change it.

The Council cannot:
- Lower requirements.
- Remove requirements.
- Change the fundamental objective.
- Convert optional features into mandatory requirements without authorization.
- Ignore explicit Human constraints.

The finalized Council specification becomes the operational source of truth for execution. However, it cannot override the original Human requirements. The Human objective therefore sits above the operational specification.

---

## 8. DOOM
DOOM is the company's organizational engine.

After the Clarification Council finalizes its specification, DOOM receives it. DOOM then creates the entire project organization.

DOOM determines:
- Required agent count.
- Required specialties.
- Agent selection.
- Agent creation.
- Roles.
- Responsibilities.
- Leadership.
- Hierarchy.
- Project structure.
- Orchestrators.
- Managers.
- Reviewers.
- Worker distribution.
- Organizational relationships.

DOOM does not merely produce a list of agents. It builds the actual temporary company/project organization required to accomplish the objective.

After the organization is handed to the project orchestrators, DOOM's normal project-creation task is complete. DOOM remains available for escalations and company-level organizational work.

---

## 9. AGENT CREATION
DOOM can create agents whenever the company requires additional capacity.

If the Human explicitly specifies an agent count:
- DOOM creates the specified amount.
- Example: Human: "I want 500 agents working on this." → DOOM creates the required 500-agent project organization.

If the Human does not specify an agent count:
- DOOM determines how many agents are necessary.
- DOOM evaluates the project's complexity and required specialties.

There is no maximum number of agents in a project.
The only minimum is:
- **10 total agents per project** (includes everyone in the project organization).

There is no predefined upper limit. If an enormous project requires thousands, millions, or more agents, DOOM can expand the project accordingly.

---

## 10. AGENT PROJECT EXCLUSIVITY
An agent can belong to only one active project at a time.

Agents are not simultaneously shared between independent projects.

If another project requires additional agents:
DOOM creates the required agents.

This allows projects to operate simultaneously without forcing individual agents to divide their attention between projects.

---

## 11. PROJECT CREATION
Every Human objective that requires a project follows the same fundamental process:

```
HUMAN → CEO → CLARIFICATION COUNCIL → DOOM → PROJECT ORGANIZATION → EXECUTION
```

A new Human objective creates a new project process. Existing projects continue operating independently. Projects can therefore run simultaneously in separate organizational environments.

---

## 12. PROJECT ORGANIZATION
A normal project contains multiple layers:

```
PROJECT
│
├── ORCHESTRATOR 1
├── ORCHESTRATOR 2
├── ORCHESTRATOR 3
│
├── REVIEWERS (1 per 10 agents ratio)
│
├── MANAGERS
│
└── WORKERS / CODERS
```

Normally there are 3 orchestrators. The orchestrators divide and coordinate the project. Below the orchestrators are managers. Managers distribute work to workers/coders. The structure is designed as an organized temporary corporation rather than an undifferentiated swarm.

---

## 13. ORCHESTRATORS
Projects normally have 3 orchestrators.

The orchestrators collectively divide the project among themselves. They coordinate the managers and oversee the complete project.

At completion, the orchestrators review the complete project after receiving reviewer confirmation. The orchestrators formally decide that the project is complete.

---

## 14. MANAGERS
Managers receive work from the orchestrators.

Managers divide that work into tasks for the workers/coders beneath them. Managers are responsible for their project's workers.

If a serious worker problem is escalated by a reviewer:
```
Reviewer → Project Manager
```
The manager attempts to resolve it. If the manager cannot resolve it, the issue escalates to the project's orchestrator.

---

## 15. REVIEWER SYSTEM
Reviewers are a continuous supervisory layer.

**Reviewer ratio:**
- **1 reviewer per 10 agents.**
  - 1–10 agents = 1 reviewer
  - 11–20 agents = 2 reviewers
  - 21–30 agents = 3 reviewers
  - 31–40 agents = 4 reviewers
  - etc.
- Even projects with fewer than 10 agents have at least one reviewer.

Reviewers monitor agents at all organizational levels.

Reviewers continuously watch for:
- Deviation from the original Human objective.
- Deviation from the project's basic idea.
- Deviation from the assigned task.
- Agents becoming trapped in loops.
- Knowledge loss.
- Knowledge contamination.
- Dangerous reasoning drift.
- Other significant deviations.

Reviewers are not merely final quality-control workers; they continuously supervise the project.

---

## 16. REVIEWER INTERVENTION
The reviewer uses graduated intervention:

### Minor Problem
- Reviewer warns the agent.
- The agent attempts to correct itself.

### Serious Problem
- Reviewer immediately pauses/stops the agent.
- The reviewer investigates:
  - What the agent was doing.
  - What mistake occurred.
  - How much incorrect work was produced.
  - Where the last fully correct point occurred.
- The agent's progress is saved.
- The reviewer identifies the last known-good state.
- If required, the agent's work is rolled back to that last correct point.
- Correct work is preserved.
- The agent can then resume from the correct point.

---

## 17. REVIEWER ESCALATION
If a serious problem cannot be resolved at the worker level:

```
REVIEWER → PROJECT MANAGER → PROJECT ORCHESTRATOR → DOOM → CEO → HUMAN
```

- The manager involved must belong to the same project.
- DOOM is not the normal first destination for reviewer problems.
- DOOM becomes involved only after the project's normal management/orchestration structure cannot resolve the problem.

---

## 18. PROJECT COMPLETION
A project reaches completion when:
1. Managers report their work complete.
2. Reviewers have no outstanding issues.
3. Orchestrators review the complete project.
4. Orchestrators formally declare the project complete.

After completion:
- The project organization dissolves.
- Agents return to the general company workforce.

---

## 19. PROJECT OUTPUT OWNERSHIP
The CEO/company initially owns the project's output.

After completion, the result is delivered to the Human.

The Human can reject the completed output:
- If the Human rejects it: The same project team is reactivated. The existing team performs revisions.
- The Human can reject the result again. There is no fixed revision limit.
- The revision cycle continues until the Human is satisfied.
- Once the Human accepts the result: The project closes. The agents are released back into the general company workforce.

---

## 20. PROJECT KNOWLEDGE RETENTION
When a project finishes, all project information is retained.

The company retains:
- Complete project history.
- Decisions.
- Reasoning.
- Failures.
- Successes.
- Development history.
- Organizational information.
- Relevant project knowledge.
- Other project records.

The project itself may dissolve, but its history does not disappear. This creates persistent institutional memory across the company.

---

## 21. MULTIPLE SIMULTANEOUS PROJECTS
Multiple projects can run simultaneously.

Example:
- Human gives Objective A → CEO → Council → DOOM → Project A.
- While Project A is still running, Human gives Objective B → CEO → Council → DOOM → Project B.
- Project A continues independently.
- Project B operates in a separate project environment.
- Neither project needs to wait for the other.
- Agents are not shared between them. DOOM creates additional agents whenever necessary.

---

## 22. COMPANY EXPANSION
The company has no fixed capability ceiling.

If the Human gives an objective that is larger than the current company:
- The company expands itself.
- CEO determines what the company needs to accomplish the objective.
- DOOM creates the necessary organizational capacity:
  - New agents.
  - New specialties.
  - New projects.
  - New departments.
  - New research capabilities.
  - New organizational structures.
  - New technical capabilities.
  - Other necessary company infrastructure.

The company scales itself to match the Human's objective.

---

## 23. NEW CAPABILITIES
A special procedure exists for situations where the company must accomplish something it has never done before:

- **CEO + DOOM enter the Clarification Council.**
- CEO and DOOM participate as ordinary equal members for this special decision.
- Every participant has equal voting weight (no extra voting power for CEO, DOOM, seniority, or rank).
- They debate possible approaches.
- A proposal requires a **75% majority**.
- If 75% cannot be reached: **Human makes the final decision.**

---

## 24. COMPANY EVOLUTION
The company is not permanently locked into its initial organizational design.

The company can autonomously change its internal structure and rules as it grows:
- Restructure itself.
- Create new organizational mechanisms.
- Change operational hierarchy.
- Develop new roles.
- Develop new management systems.
- Adapt its organizational processes.
- Build new capabilities.

The company evolves as its scale and capabilities increase.

---

## 25. NEW BUSINESSES AND DIVISIONS
The company can create new businesses and divisions when directed by the Human.

- The Human has final authority over creation of entirely new businesses/divisions.
- The CEO and DOOM then determine how to build the requested business/division.
- The company can subsequently expand that new business/division using the same organizational machinery.

---

## 26. LONG-TERM COMPANY PURPOSE
The company simultaneously serves four major purposes:

### A. Objective Execution
Complete whatever objectives the Human gives it.

### B. Continuous Expansion
Continuously increase its organizational and technical capability.

### C. AI Research and Development
Research and develop better agents, better systems, better methods, new capabilities, and new organizational intelligence.

### D. General-Purpose Corporation
Create and operate products, businesses, research programs, projects, departments, new divisions, and new capabilities when directed by the Human.

---

## 27. ORGANIZATIONAL LIFECYCLE
The complete standard lifecycle is:

```
HUMAN
  ↓
CEO UNDERSTANDS OBJECTIVE
  ↓
CLARIFICATION COUNCIL
  ↓
COUNCIL DEBATES
  ↓
75% CONSENSUS (or Senior Council Leader deadlock breaker)
  ↓
DOOM VALIDATES AND ORGANIZES
  ↓
DOOM CREATES REQUIRED AGENTS (Min 10 agents, 1:10 reviewer ratio)
  ↓
DOOM CREATES PROJECT STRUCTURE (3 Orchestrators, Reviewers, Managers, Workers)
  ↓
PROJECT ORCHESTRATORS RECEIVE ORGANIZATION
  ↓
ORCHESTRATORS → MANAGERS → WORKERS
  ↓
REVIEWERS CONTINUOUSLY MONITOR EVERYTHING (Graduated intervention & rollback)
  ↓
WORK EXECUTION
  ↓
REVIEWER ISSUES RESOLVED
  ↓
MANAGERS REPORT COMPLETION
  ↓
ORCHESTRATORS REVIEW
  ↓
PROJECT COMPLETED
  ↓
OUTPUT DELIVERED TO HUMAN
  ↓
HUMAN ACCEPTS OR REJECTS
  ↓
IF REJECTED → SAME PROJECT REACTIVATED FOR INDEFINITE REVISIONS
  ↓
IF ACCEPTED → PROJECT DISSOLVES
  ↓
AGENTS RETURN TO GENERAL WORKFORCE
  ↓
COMPLETE PROJECT HISTORY RETAINED (Persistent institutional memory)
  ↓
COMPANY GROWTH & EXPANSION
  ↓
NEXT OBJECTIVE
```

---

## 28. SPECIAL AUTHORITY RULES
1. Human is the ultimate authority.
2. Human can override CEO.
3. Human's original objective has the highest priority.
4. CEO determines what the company needs at the executive level.
5. DOOM creates the organizational capacity required to execute the objective.
6. Clarification Council debates and formalizes requirements.
7. Normal Council decisions require 75% consensus.
8. Senior Council Leader breaks normal Council deadlocks.
9. Special new-capability Council decisions give every participant equal voting power.
10. Special new-capability decisions require 75%.
11. Human decides if the special council cannot reach 75%.
12. Projects are independent.
13. Agents belong to one project at a time.
14. There is a minimum of 10 agents per project.
15. There is no maximum project size.
16. DOOM can continuously create additional agents.
17. Reviewers continuously monitor projects (1 reviewer per 10 agents ratio).
18. Serious problems can be escalated all the way to Human.
19. Completed project organizations dissolve.
20. Project knowledge/history is retained.
21. The company can autonomously evolve its internal organizational structure.
22. The company has no predefined capability ceiling.

---

## 29. GLOBAL COMPANY MODEL
All agents operate using the AI model currently selected by the Human.

For example:
If Human selects a model:
- CEO → Selected Model
- DOOM → Selected Model
- Council → Selected Model
- Reviewers → Selected Model
- Orchestrators → Selected Model
- Managers → Selected Model
- Workers → Selected Model
- New agents → Selected Model

The selected model is a global company-level configuration rather than an individual-agent choice.

---

## 30. FINAL SYSTEM CONCEPT
The company is not simply an AI swarm. It is a dynamically expanding AI corporation.

The Human provides the objective.
The CEO understands the objective.
The Clarification Council debates and formalizes it.
DOOM constructs whatever organization is necessary.
The company creates whatever number of agents are required.
Projects operate independently and simultaneously.
Orchestrators coordinate projects.
Managers distribute work.
Workers execute.
Reviewers continuously supervise.
Failures are detected, paused, analyzed, and escalated.
Completed projects dissolve while their knowledge remains.
Rejected projects can be reactivated indefinitely.
The company can expand without a predefined ceiling.
The company can research, create, restructure, and evolve.
And every agent operates on the AI model selected by the Human.

```
HUMAN OBJECTIVE
  → CEO
  → COUNCIL
  → DOOM
  → SELF-EXPANDING ORGANIZATION
  → PROJECT EXECUTION
  → REVIEW
  → COMPLETION
  → HUMAN
  → KNOWLEDGE RETENTION
  → COMPANY GROWTH
  → NEXT OBJECTIVE
```
