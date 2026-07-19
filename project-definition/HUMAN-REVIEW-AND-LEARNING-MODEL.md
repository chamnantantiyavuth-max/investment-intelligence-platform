# Human Review and Learning Model

Status: Approved Domain Specification
Version: 0.1
Owner: Founder
Authority: Approved Domain Specification subordinate to the Constitution and Founder's Decisions
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## 1. Human Authority

The Founder has final authority (Constitution §12; DNA-010). The platform proposes and organizes; the Founder approves and decides.

Human authority must not erase machine dissent, contradictory evidence, or original system assessments. Overrides preserve, not replace.

## 2. Human Override

A Human Override is a Founder decision that differs from the system's assessment. It is not an error to be corrected — it is a deliberate exercise of human authority that must be preserved for learning.

### 2.1 Override Fields

Every Human Override records (Constitution §12; Human Review and Override operational file):

| # | Field | Description |
|---|---|---|
| 1 | **System assessment** | What the platform concluded before the override |
| 2 | **Machine dissent** | Any unresolved contradictions, alternative rankings, or warnings the system flagged |
| 3 | **Unresolved counter-evidence** | Evidence that contradicted the Founder's decision, preserved for future review |
| 4 | **Founder rationale** | The Founder's reasoning for the override |
| 5 | **Required confirmation** | What evidence or conditions would validate or invalidate the override |
| 6 | **Reassessment point** | When the override should be reviewed (date or condition) |
| 7 | **Eventual outcome** | What actually happened. May be **Pending** or **Not Yet Assessed** until the reassessment condition is reached. Populated in Later phases. V0 does not require real outcome tracking. |
| 8 | **Decision type and scope** | What was overridden (theme approval, candidate ranking, research priority, etc.) |

### 2.2 Override Rules

- Overrides do not rewrite prior system states.
- The original system assessment remains visible alongside the override.
- The platform may later analyze override patterns to **improve the decision process**, not to judge the Founder.
- Override history is preserved for postmortems and learning.

## 3. Learning Loop (Conceptual Contracts Only)

The Learning Loop is defined in the Constitution (§16) and Learning and Knowledge Loop operational file. Its **implementation is deferred to Later phases**.

V0 defines conceptual contracts for the entities in the loop. These contracts are intended to reduce avoidable redesign later. They do **not** guarantee that no future schema migration will be needed. Persistence schemas, migrations, and implementation technology remain deferred.

### 3.1 Loop Chain

```
Evidence → Hypothesis → Theme → Candidate → Research
  → Human Decision → Outcome → Postmortem
    → Lesson Draft → Human Approval → Approved Lesson
      → Rule, Skill, or Playbook Proposal
```

### 3.2 Decision

A formal record of a Founder decision.

| Field | Description |
|---|---|
| Decision identifier | Unique, stable reference |
| Decision type | Theme approval, candidate promotion, research priority, override, etc. |
| Context | Related Theme(s), Candidate(s), Evidence |
| Decision | What was decided |
| Rationale | Why it was decided |
| System recommendation | What the platform recommended (if different) |
| Actor | Founder |
| Timestamp | When the decision was made |
| Conditions or contingencies | Any conditions attached to the decision |

### 3.3 Outcome

The realized result of a decision or tracked hypothesis.

| Field | Description |
|---|---|
| Outcome identifier | Unique, stable reference |
| Related decision(s) | Which decision(s) this outcome relates to |
| Related theme(s) / candidate(s) | Domain context |
| Outcome type | Confirmed, invalidated, mixed, inconclusive, timed out |
| Measurement | Quantitative or qualitative result |
| Measurement date | When the outcome was assessed |
| Evidence references | Supporting evidence for the outcome assessment |

### 3.4 Postmortem

A structured review of a decision and its outcome.

| Field | Description |
|---|---|
| Postmortem identifier | Unique, stable reference |
| Case reference | Decision(s) and Outcome(s) under review |
| What was expected | The thesis or hypothesis at decision time |
| What happened | The actual outcome |
| Variance analysis | Why expectations and outcomes differed |
| Lessons identified | Potential learnings (draft stage) |
| Supporting evidence | Evidence relevant to the postmortem analysis |
| Author | AI (draft) or human |
| Status | Draft, Under Review, Approved |

### 3.5 Lesson

An approved learning from one or more postmortems.

| Field | Description |
|---|---|
| Lesson identifier | Unique, stable reference |
| Source postmortem(s) | Which cases produced this lesson |
| Lesson statement | What was learned |
| Evidence and case references | Supporting evidence |
| Proposed change | What rule, threshold, workflow, or playbook should change |
| Status | Draft (AI-generated), Under Human Review, Approved, Rejected |
| Approval | Founder approval required for Approved status |

### 3.6 Rule, Skill, or Playbook Proposal

A versioned change to official platform behavior, derived from Approved Lessons.

| Field | Description |
|---|---|
| Proposal identifier | Unique, stable reference |
| Source lesson(s) | Which Approved Lessons motivate this change |
| Affected rule / workflow | What is being changed |
| Current behavior | What the platform does now |
| Proposed behavior | What it should do instead |
| Impact analysis | Expected effect on themes, candidates, queue, decisions |
| Version | New version number |
| Status | Proposed, Approved, Implemented, Retired |
| Approval | Founder approval required |

## 4. AI Role in Learning

- AI may **draft** postmortems and lessons (AI Governance operational file).
- AI-generated lessons are **not official knowledge** until human-approved.
- AI may **propose** rule changes but may not enforce them automatically.
- AI may **not** change official rules, thresholds, or workflows without an approved, versioned proposal.

## 5. Knowledge Layers

| Layer | Purpose | Version |
|---|---|---|
| **Application** | Structured source of truth for evidence, states, lineage, decisions, overrides, outcomes, lessons, and rule versions | V0: contracts defined |
| **Obsidian / NotebookLM** | Narrative case studies, postmortems, approved lessons, patterns, anti-patterns, and playbooks | Later phases |

## 6. V0 Boundary

V0 defines the conceptual contracts described in §3 above. It does **not**:

- Implement a completed Learning Loop
- Track real outcomes
- Generate postmortems
- Draft lessons
- Propose rule changes
- Populate any learning entities with real data

V0 may include synthetic examples of these entities to validate the data model, but the loop is not closed. Learning Loop closure belongs to Later phases.

## 7. Version Boundaries for Human Review and Learning

| Capability | V0 | V0.5 | V1 | V1.5 | Later |
|---|---|---|---|---|---|
| Human Override recording (all 8 fields) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Override history preservation | ✅ | ✅ | ✅ | ✅ | ✅ |
| Decision and Outcome contracts defined | ✅ | ✅ | ✅ | ✅ | ✅ |
| Postmortem and Lesson contracts defined | ✅ | ✅ | ✅ | ✅ | ✅ |
| Learning Loop closure (real outcomes → lessons) | — | — | — | — | ✅ |
| AI-drafted postmortems and lessons | — | — | — | — | ✅ |
| Rule/playbook versioning and approval workflow | — | — | — | — | ✅ |
| Obsidian/NotebookLM narrative export | — | — | — | — | ✅ |
