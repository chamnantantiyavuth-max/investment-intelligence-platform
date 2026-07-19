# Traceability and Decision Register

Status: Accepted Living Design Register
Version: 0.1
Owner: Founder
Authority: Accepted living non-authoritative register; individual entries gain authority only through their named approval references
Derived from: Constitution v0.3, Project Definition v0.1, and AM-V0-DESIGN-PLAN-v0.1
Repository Acceptance: AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1

## Purpose

This register records every design decision — proposed, approved, deferred, or rejected — for the Alpha Momentum V0 Design phase. It provides full traceability from every rule and contract to its decision obligation source and rule content authority.

Updating this register does not approve a Proposed decision. Approval requires a separate explicit Founder decision with a named approval reference.

## Status Definitions

| Status | Meaning |
|---|---|
| **Proposed** | Decision identified and described but not yet approved. May carry Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED |
| **Approved** | Founder has explicitly approved the decision with a named approval reference |
| **Deferred** | Decision intentionally postponed to a later phase |
| **Rejected** | Decision path considered and declined; rationale preserved |

There is no fifth "UNRESOLVED" status. "UNRESOLVED — FOUNDER DECISION REQUIRED" is a Resolution value carried by a Proposed entry.

## Entry Template

Each entry must contain:

| Field | Description |
|---|---|
| **Identifier** | Unique stable reference (e.g., DR-001, DS-XXX) |
| **Topic** | What the decision is about |
| **Decision Obligation Source** | The approved document explaining why the decision must exist |
| **Rule Content Authority** | The approved source that explicitly supplies the content of the rule. If none: NONE. For governance decisions: NOT APPLICABLE — GOVERNANCE DECISION; decision authority is established by the named Approval Reference where approved |
| **Affected Artifact(s)** | Which design file(s) this decision constrains |
| **Status** | Proposed, Approved, Deferred, or Rejected |
| **Resolution** | For Proposed: UNRESOLVED — FOUNDER DECISION REQUIRED, or blank if resolved in the proposal |
| **Materiality** | Material or Non-material, with rationale |
| **Decision Category** | Governance, Rule Slot, Cohort, Filter, Rank, Weight, Threshold, Formula, Period, Taxonomy, Eligibility, Fallback |
| **Rationale** | Why this decision exists and what it constrains |
| **Founder Decision Required** | Yes or No |
| **Approval Reference** | Named approval reference (blank until approved) |
| **Dependencies** | Which other entries this decision depends on |
| **Verification Evidence** | How approval was verified (blank until populated) |

---

## Governance Entries

### DR-001 — Phase Transition into Alpha Momentum V0 Design

- **Identifier:** DR-001
- **Topic:** Authorization to transition from Constitution and Product Definition into Alpha Momentum V0 Design
- **Decision Obligation Source:** ROADMAP.md Phase 2; Constitution §20; Founder's Decision #2
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION; decision authority is established by the named Approval Reference where approved
- **Affected Artifact(s):** All artifacts under `design/alpha-momentum-v0/`
- **Status:** Approved
- **Resolution:** —
- **Materiality:** Material — phase-governance decision authorizing a new phase and file plan
- **Decision Category:** Governance
- **Rationale:** The project has approved foundation documents (v0.3), approved domain specifications (v0.1), and a roadmap explicitly listing Alpha Momentum V0 Design as Phase 2. This decision authorizes the transition and the creation of design artifacts.
- **Founder Decision Required:** Yes
- **Approval Reference:** AM-V0-DESIGN-PLAN-v0.1
- **Dependencies:** foundation-v0.3, project-definition-v0.1
- **Verification Evidence:** Explicit Founder authorization message with complete start/end markers; phase transition explicitly approved; three-file first tranche independently verified; repository acceptance completed through DR-008

### DR-002 — Design Plan Approval

- **Identifier:** DR-002
- **Topic:** Approval of the AM-V0-DESIGN-PLAN-v0.1 umbrella-plan content and governance structure: file plan, scope, dependency order, gate structure, materiality policy, amendment process, and Legacy Salvage insertion window
- **Decision Obligation Source:** Constitution v0.3; ROADMAP.md Phase 2
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION; decision authority is established by the named Approval Reference where approved
- **Affected Artifact(s):** `DESIGN-PLAN.md` (the repository file is a transcription of this approved plan)
- **Status:** Approved
- **Resolution:** —
- **Materiality:** Material — establishes the governance framework for the entire design phase
- **Decision Category:** Governance
- **Rationale:** The AM-V0-DESIGN-PLAN-v0.1 umbrella plan defines the stable governance. The repository file DESIGN-PLAN.md transcribes it. Repository-file acceptance is tracked separately (see DR-008). After explicit Founder acceptance of the repository file following independent diff review, the transcribed DESIGN-PLAN.md becomes stable and amendable only through a named amendment.
- **Founder Decision Required:** Yes
- **Approval Reference:** AM-V0-DESIGN-PLAN-v0.1
- **Dependencies:** DR-001
- **Verification Evidence:** Umbrella-plan content approved via AM-V0-DESIGN-PLAN-v0.1; repository transcription accepted through DR-008

### DR-003 — Gate A Drafting Authorization

- **Identifier:** DR-003
- **Topic:** Authorization to draft the Gate A decision-slot artifacts: RULE-PACK-AND-QUALITY-CONTRACTS.md, DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md, PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md, and updated TRACEABILITY register
- **Decision Obligation Source:** DESIGN-PLAN.md; Constitution §13, §14; ALPHA-MOMENTUM-V0-SPEC §4, §6
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION; decision authority is established by the named Approval Reference where approved
- **Affected Artifact(s):** Gate A artifacts; updated TRACEABILITY register
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Materiality:** Material — Gate A drafting defines all Founder decisions required before deterministic V0 behavior
- **Decision Category:** Governance
- **Rationale:** Gate A must identify every unresolved decision slot before any behavior can be approved. It must not populate invented investment rules. Gate A completion and approval of the drafted decision-slot set will be recorded as a separate future decision.
- **Founder Decision Required:** Yes, before Gate A drafting begins
- **Approval Reference:** (blank pending a separate named drafting authorization)
- **Dependencies:** DR-008 (repository acceptance)
- **Verification Evidence:** (pending)

### DR-004 — Legacy Knowledge Salvage

- **Identifier:** DR-004
- **Topic:** Authorization to access legacy repository for historical Theme candidates, relationship examples, fixture realism, and failure cases
- **Decision Obligation Source:** DESIGN-PLAN.md §9; AM-V0-DESIGN-PLAN-v0.1
- **Rule Content Authority:** NONE — all outputs must be labeled UNTRUSTED HISTORICAL INPUT — NOT AUTHORITY
- **Affected Artifact(s):** May inform CONTROLLED-THEME-SET.md, FIXTURE-AND-ACCEPTANCE-SCENARIOS.md
- **Status:** Deferred
- **Resolution:** Pending separate named read-only authorization
- **Materiality:** Material — introduces untrusted historical input that could influence Theme selection
- **Decision Category:** Governance
- **Rationale:** Legacy salvage is optional and requires a separate authorization. It does not block Gate A. All outputs must be labeled UNTRUSTED HISTORICAL INPUT — NOT AUTHORITY. It may inform but not establish architecture, investment rules, weights, thresholds, benchmarks, or implementation requirements.
- **Founder Decision Required:** Yes (separate authorization)
- **Approval Reference:** (pending separate authorization)
- **Dependencies:** Separate Gate A completion approval (not merely DR-003 drafting authorization)
- **Verification Evidence:** (pending)

### DR-005 — Controlled Theme Set

- **Identifier:** DR-005
- **Topic:** Selection and approval of a controlled Theme set for V0 design and fixtures
- **Decision Obligation Source:** ALPHA-MOMENTUM-V0-SPEC §3; Theme Model (project-definition/)
- **Rule Content Authority:** NONE — Founder must supply Theme definitions
- **Affected Artifact(s):** `CONTROLLED-THEME-SET.md`; FIXTURE-AND-ACCEPTANCE-SCENARIOS.md; THEME-CARD-AND-HUMAN-REVIEW-FLOW.md
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Materiality:** Material — determines which Themes exercise V0 domain and acceptance cases
- **Decision Category:** Governance, Eligibility
- **Rationale:** V0 uses Founder-approved controlled themes only. Theme selection must satisfy four criteria: structural driver, identifiable beneficiaries, sufficient public-domain evidence, and domain coverage. This is a Gate B decision.
- **Founder Decision Required:** Yes
- **Approval Reference:** (pending — will be assigned at Gate B review)
- **Dependencies:** Separate Gate A completion approval; optionally DR-004 (Legacy Salvage)
- **Verification Evidence:** (pending)

### DR-006 — Canonical Theme-Role Ownership

- **Identifier:** DR-006
- **Topic:** Whether canonical structural Theme roles (Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary) belong to Entity–Theme relationships, Candidate–Theme relationships, or a layered combination
- **Decision Obligation Source:** CANDIDATE-AND-QUEUE-MODEL.md §3.4; DOMAIN-ARCHITECTURE.md §1.1; Constitution §5 (pending resolution)
- **Rule Content Authority:** NONE — Founder must supply the ownership model
- **Affected Artifact(s):** CANDIDATE-AND-QUEUE-MODEL.md; DOMAIN-ARCHITECTURE.md; future strategy modules
- **Status:** Deferred
- **Resolution:** Not required for V0; must be resolved before V1 or before a second strategy consumes Theme roles
- **Materiality:** Material — affects where role data is authored, how contradictions are resolved, and which context owns role transition history
- **Decision Category:** Governance
- **Rationale:** V0 may use simplified Candidate–Theme test relationships without establishing permanent canonical ownership. This decision is not required for V0. If resolution requires changing an Approved Domain Specification, record UPSTREAM AMENDMENT REQUIRED and follow the authority-amendment process.
- **Founder Decision Required:** Yes (before V1)
- **Approval Reference:** (pending)
- **Dependencies:** None blocking V0
- **Verification Evidence:** (pending)

### DR-007 — Technology Stack

- **Identifier:** DR-007
- **Topic:** Selection of programming language, frontend framework, database, cloud provider, data vendors, RAG architecture, MCP integrations, agent orchestration, and deployment topology
- **Decision Obligation Source:** DEFERRED-DECISIONS.md; AGENTS.md ("Do not select a final technology stack")
- **Rule Content Authority:** NONE — Founder must approve any technology selection
- **Affected Artifact(s):** Implementation-phase artifacts (not yet created)
- **Status:** Deferred
- **Resolution:** Deferred until a separately approved architecture or implementation-planning decision after Gate D
- **Materiality:** Material — determines implementation architecture, but not a design-phase decision
- **Decision Category:** Governance
- **Rationale:** All technology decisions are explicitly listed in DEFERRED-DECISIONS.md. The design phase must remain technology-neutral. Implementation must not invent or select a technology stack without explicit Founder approval.
- **Founder Decision Required:** Yes (before implementation)
- **Approval Reference:** (pending)
- **Dependencies:** DR-001 through Gate D
- **Verification Evidence:** (pending)

### DR-008 — First Tranche Repository Acceptance

- **Identifier:** DR-008
- **Topic:** Acceptance into the repository of README.md, DESIGN-PLAN.md, and TRACEABILITY-AND-DECISION-REGISTER.md after independent diff review
- **Decision Obligation Source:** AM-V0-DESIGN-PLAN-v0.1 first-tranche authorization
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION; decision authority is established by the named Approval Reference where approved
- **Affected Artifact(s):** `README.md`, `DESIGN-PLAN.md`, `TRACEABILITY-AND-DECISION-REGISTER.md`
- **Status:** Approved
- **Resolution:** —
- **Materiality:** Non-material repository acceptance, provided the files faithfully transcribe the approved plan and introduce no new observable behavior
- **Decision Category:** Governance
- **Rationale:** The three first-tranche files must be independently reviewed and explicitly accepted by the Founder before they become authoritative within the repository. Plan content approval (DR-002) is separate from repository-file acceptance (DR-008).
- **Founder Decision Required:** Yes — completed
- **Approval Reference:** AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1
- **Dependencies:** DR-001, DR-002, independent review
- **Verification Evidence:** Independent focused review confirmed exact three-file scope, matching SHA-256 values, valid UTF-8, no tracked-file changes, no investment-rule content, and governance consistency; Founder explicitly accepted the repository artifacts.

---

## Rule-Slot Entries

No rule-slot entries have been proposed. Rule slots will be added in Gate A artifacts and registered here with their corresponding DR identifiers.

Reserved identifier range for rule slots: DS-001 through DS-999.

---

## Reference Cohort Entries

No reference cohort entries have been proposed. Reference cohorts are defined as part of Gate A rule-slot contracts.

Reserved identifier range for reference cohorts: RC-001 through RC-999.

---

## ADR Entries

No ADRs have been created. ADRs will be registered here when a real cross-cutting design decision arises.

Reserved identifier range for ADRs: ADR-001 through ADR-999.

---

## Unresolved Founder Decisions Summary

The following decisions require explicit Founder resolution. This summary is derived from the register above and does not replace individual entries.

| Ref | Topic | Required By | Status |
|---|---|---|---|
| DR-003 | Gate A Drafting Authorization | Before Gate A drafting | Proposed — UNRESOLVED |
| DR-005 | Controlled Theme Set selection | Gate B | Proposed — UNRESOLVED |
| DR-006 | Canonical Theme-role ownership | V1 / second strategy | Deferred |
| DR-007 | Technology stack | After Gate D | Deferred |
| DR-004 | Legacy Knowledge Salvage authorization | Gate B (optional) | Deferred |

No investment-rule decisions (thresholds, weights, formulas, lookbacks, benchmarks, taxonomies, cohorts, queue ordering, tie-breakers, fallbacks, scoring aggregation) have been proposed. These will be identified as decision slots in Gate A artifacts.

---

## Amendment History

| Date | Change | Authority |
|---|---|---|
| 20 July 2026 | Initial draft with governance entries DR-001 through DR-007 | AM-V0-DESIGN-PLAN-v0.1 |
| 20 July 2026 | Micro-revision: DR-001/DR-002 verification wording corrected; DR-006 neutrality restored; DR-007 reworded; DR-008 added for repository acceptance | AM-V0-FIRST-TRANCHE-MICRO-REVISION |
| 20 July 2026 | Final micro-revision: all entries converted to Decision Obligation Source / Rule Content Authority; DR-003 narrowed to drafting authorization only and marked UNRESOLVED; DR-004 depends on separate Gate A completion; rollback reference made immutable | AM-V0-FIRST-TRANCHE-FINAL-MICRO-REVISION |
| 20 July 2026 | First tranche repository acceptance; README promoted to Approved Design Area Index v0.1; DESIGN-PLAN promoted to Approved Stable Design Plan v0.1; register promoted to Accepted Living Design Register v0.1; DR-008 approved | AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1 |
