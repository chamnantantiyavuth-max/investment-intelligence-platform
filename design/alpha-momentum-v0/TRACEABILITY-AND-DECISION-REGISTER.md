# Traceability and Decision Register

Status: Accepted Living Design Register
Version: 0.3 (Gate A Structurally Accepted)
Owner: Founder
Authority: Accepted living non-authoritative register; individual entries gain authority only through their named approval references
Derived from: Constitution v0.3, Project Definition v0.1, and AM-V0-DESIGN-PLAN-v0.1
Repository Acceptance: AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1
Normalization Rewrite: AM-V0-GATE-A-SLOT-NORMALIZATION-REWRITE-v0.1
Structural Acceptance: AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1

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

---

## Governance Entries

### DR-001 — Phase Transition into Alpha Momentum V0 Design

- **Identifier:** DR-001
- **Topic:** Authorization to transition from Constitution and Product Definition into Alpha Momentum V0 Design
- **Decision Obligation Source:** ROADMAP.md Phase 2; Constitution §20; Founder's Decision #2
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION
- **Affected Artifact(s):** All artifacts under `design/alpha-momentum-v0/`
- **Status:** Approved
- **Resolution:** —
- **Materiality:** Material — phase-governance decision
- **Decision Category:** Governance
- **Founder Decision Required:** Yes
- **Approval Reference:** AM-V0-DESIGN-PLAN-v0.1
- **Dependencies:** foundation-v0.3, project-definition-v0.1
- **Verification Evidence:** Explicit Founder authorization message with complete markers; phase transition explicitly approved

### DR-002 — Design Plan Approval

- **Identifier:** DR-002
- **Status:** Approved
- **Approval Reference:** AM-V0-DESIGN-PLAN-v0.1
- **Dependencies:** DR-001

### DR-003 — Gate A Drafting Authorization

- **Identifier:** DR-003
- **Status:** Approved
- **Resolution:** —
- **Founder Decision Required:** Yes — completed
- **Approval Reference:** AM-V0-GATE-A-DRAFTING-v0.1
- **Verification Evidence:** Founder explicitly authorized drafting of the three Gate A decision-slot artifacts; Gate A completion remains a separate future decision

### DR-004 — Legacy Knowledge Salvage

- **Identifier:** DR-004
- **Status:** Deferred
- **Resolution:** Pending separate named read-only authorization

### DR-005 — Controlled Theme Set

- **Identifier:** DR-005
- **Status:** Proposed
- **Resolution:** UNRESOLVED — FOUNDER DECISION REQUIRED
- **Approval Reference:** (pending — Gate B)

### DR-006 — Canonical Theme-Role Ownership

- **Identifier:** DR-006
- **Status:** Deferred
- **Resolution:** Not required for V0; must be resolved before V1

### DR-007 — Technology Stack

- **Identifier:** DR-007
- **Status:** Deferred

### DR-008 — First Tranche Repository Acceptance

- **Identifier:** DR-008
- **Status:** Approved
- **Approval Reference:** AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1

### DR-009 — Gate A Completion and Decision-Slot Set Approval

- **Identifier:** DR-009
- **Topic:** Approval or rejection of the completeness and structure of the normalized Gate A decision-slot set — does not automatically approve the answers to individual material decision slots
- **Decision Obligation Source:** DESIGN-PLAN.md §6 Gate A; AM-V0-GATE-A-DRAFTING-v0.1
- **Rule Content Authority:** NOT APPLICABLE — GOVERNANCE DECISION
- **Affected Artifact(s):** RULE-PACK-AND-QUALITY-CONTRACTS.md; DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md; PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md; TRACEABILITY-AND-DECISION-REGISTER.md
- **Status:** Approved
- **Resolution:** —
- **Materiality:** Material — determines whether the normalized decision-slot set is structurally complete; does not approve slot answers
- **Decision Category:** Governance
- **Rationale:** DR-009 acknowledges that structural completeness is a separate decision from answering any specific slot. Approval confirms slots are correctly identified and scoped; it does not fill any UNRESOLVED slot
- **Founder Decision Required:** Yes — completed
- **Approval Reference:** AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1
- **Dependencies:** DR-003 and independent review of all Gate A artifacts
- **Verification Evidence:** Independent review confirmed 35 normalized active slots, 8 conditional templates, complete identifier supersession, correct ownership boundaries, no prohibited investment-rule content, and exact removal of all AI-authored alternatives; Founder explicitly approved Gate A structural completeness.

---

## Normalized Active Slot Inventory

### RULE-PACK-AND-QUALITY-CONTRACTS.md — 10 Active Slots

| Slot | Topic | Status |
|---|---|---|
| DS-301 | V0 Candidate Quality Domain Set | Proposed — UNRESOLVED |
| DS-302 | V0 Entry Readiness Domain Set | Proposed — UNRESOLVED |
| DS-303 | V0 Theme Quality Consumption Contract | Proposed — UNRESOLVED |
| DS-304 | Candidate Quality Output and Summary Policy | Proposed — UNRESOLVED |
| DS-305 | Entry Readiness Output and Summary Policy | Proposed — UNRESOLVED |
| DS-306 | Theme Quality Output and Summary Policy (Alpha Momentum Consumption) | Proposed — UNRESOLVED |
| DS-307 | Strategy-Relevance Policy While Preserving Separate Dimensions | Proposed — UNRESOLVED |
| DS-308 | Theme Context Operational Classification (canonical) | Proposed — UNRESOLVED |
| DS-309 | Operational V0 Universe Boundary | Proposed — UNRESOLVED |
| DS-310 | Additional Alpha Momentum Eligibility Criteria | Proposed — UNRESOLVED |

### DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md — 12 Active Slots

| Slot | Topic | Status |
|---|---|---|
| DS-401 | Freshness and Staleness | Proposed — UNRESOLVED |
| DS-402 | Completeness and Expected-Data Contract | Proposed — UNRESOLVED |
| DS-403 | Reliability | Proposed — UNRESOLVED |
| DS-404 | Source Independence and Derivation Classification | Proposed — UNRESOLVED |
| DS-405 | Conflict Detection and Preservation | Proposed — UNRESOLVED |
| DS-406 | Missing Evidence | Proposed — UNRESOLVED |
| DS-407 | Public-Availability Timestamp | Proposed — UNRESOLVED |
| DS-408 | Ingestion Timestamp | Proposed — UNRESOLVED |
| DS-409 | Effective / As-Of and Forecast-Target Periods | Proposed — UNRESOLVED |
| DS-410 | Revision and Vintage Handling | Proposed — UNRESOLVED |
| DS-411 | Point-in-Time Visibility | Proposed — UNRESOLVED |
| DS-412 | Data Confidence Scope Levels and Roll-Up Policy | Proposed — UNRESOLVED |

### PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md — 13 Active Slots

| Slot | Topic | Status |
|---|---|---|
| DS-501 | Operational V0 Universe Boundary in Pipeline Context | Proposed — UNRESOLVED |
| DS-502 | Theme Context Stage Behavior | Proposed — UNRESOLVED |
| DS-503 | Candidate Quality Assessment — Gate/Rank/Enrichment Effects | Proposed — UNRESOLVED |
| DS-504 | Entry Readiness Assessment — Gate/Rank/Enrichment Effects | Proposed — UNRESOLVED |
| DS-505 | Data Confidence Assessment — Gate/Warning Effects | Proposed — UNRESOLVED |
| DS-506 | Theme-First Queue Assembly | Proposed — UNRESOLVED |
| DS-507 | V0 Prioritization Output Form | Proposed — UNRESOLVED |
| DS-508 | Adaptive-Capacity Decision Policy | Proposed — UNRESOLVED |
| DS-509 | Queue Empty-State Operational Contract | Proposed — UNRESOLVED |
| DS-510 | Explainability, Audit, and Rule-Result Lineage Contract | Proposed — UNRESOLVED |
| DS-511 | Stock-First Discovery Path Preservation | Proposed — UNRESOLVED |
| DS-512 | Logical Stage Dependencies and Input/Output Contracts | Proposed — UNRESOLVED |
| DS-513 | Rule Lifecycle, Version, Authority, and Effective-Date Contract | Proposed — UNRESOLVED |

**Total Active Gate A Slots: 35** (10 + 12 + 13)

---

## Template Inventory

Templates are not active decisions. They carry TPL- identifiers. Instantiation requires a separate named authorization.

| Template ID | Purpose | Artifact | Activation Condition |
|---|---|---|---|
| TPL-RP-CANDIDATE-DOMAIN | Candidate Quality domain measurement contract | Rule-Pack | DS-301 includes the domain |
| TPL-RP-ENTRY-DOMAIN | Entry Readiness domain measurement contract | Rule-Pack | DS-302 includes the domain |
| TPL-RP-THEME-CONSUMPTION | Theme Quality per-dimension consumption contract | Rule-Pack | DS-303 identifies the dimension |
| TPL-RP-FEATURE-CONTRACT | Feature definition contract | Rule-Pack | A domain measurement contract requires features |
| TPL-REFERENCE-COHORT | Reference Cohort Contract | Rule-Pack | An approved relative rule requires a cohort |
| TPL-PIPELINE-WITHIN-THEME-ORDERING | Within-Theme Candidate Ordering Policy | Pipeline | DS-507 selects ordering-dependent output form |
| TPL-PIPELINE-THEME-LEVEL-ORDERING | Theme-Level Ordering Policy | Pipeline | DS-507 selects ordering-dependent output form requiring Theme ordering |
| TPL-PIPELINE-TIE-BEHAVIOR | Tie Behavior Policy | Pipeline | DS-507 selects ordering form creating tie cases |

**Template count: 8. None are active decisions.**

---

## Inherited Control Inventory

| Control | Source | Description |
|---|---|---|
| Higher-Authority Escalation | DESIGN-PLAN.md §13; AGENTS.md | Stop and record UPSTREAM AMENDMENT REQUIRED when a decision would change higher authority |
| Contradiction Visibility (Presentation) | EVIDENCE-MODEL §7; Constitution §10 | Contradictions must remain visible; not silently compressed. Gate C handles human-facing display |

**Inherited control count: 2. Not unresolved slots.**

---

## Deferred and Future-Gate Topics

### Deferred Beyond Gate A

| Topic | Old ID | Rationale |
|---|---|---|
| Stage Execution Order and Parallelism | DS-215 (old) | Physical runtime scheduling — deferred to architecture/implementation planning |

### Moved to Future Gate C (No Identifiers Assigned)

| Topic | Old ID | Rationale |
|---|---|---|
| Theme Card and Research Queue Relationship | DS-218 (old) | Gate C artifact THEME-CARD-AND-HUMAN-REVIEW-FLOW.md |
| Human-Facing Empty-State Presentation | (split from DS-208) | Gate C presentation |
| Human-Facing Contradiction Visibility and Display | (split from DS-113) | Gate C presentation |

---

## Slot Supersession Map (DS-001 through DS-218, RC-001)

| Old ID | Disposition | New Reference |
|---|---|---|
| DS-001 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-002 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-003 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-004 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-005 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-006 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-007 | Superseded by template | TPL-RP-CANDIDATE-DOMAIN |
| DS-008 | Superseded by | DS-303 |
| DS-009 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-010 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-011 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-012 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-013 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-014 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-015 | Superseded by template | TPL-RP-THEME-CONSUMPTION |
| DS-016 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-017 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-018 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-019 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-020 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-021 | Superseded by template | TPL-RP-ENTRY-DOMAIN |
| DS-022 | Superseded by | DS-304 |
| DS-023 | Superseded by | DS-305 |
| DS-024 | Superseded by | DS-306 |
| DS-025 | Superseded by | DS-307 |
| DS-026 | Merged into | DS-308 |
| DS-027 | Split and superseded by | DS-309 + DS-310 |
| DS-028 | Superseded by template | TPL-RP-FEATURE-CONTRACT |
| RC-001 | Removed; replaced by template | TPL-REFERENCE-COHORT |
| DS-101 | Merged into | DS-401 |
| DS-102 | Superseded by | DS-402 |
| DS-103 | Superseded by | DS-403 |
| DS-104 | Merged into | DS-405 |
| DS-105 | Merged into | DS-412 |
| DS-106 | Superseded by | DS-406 |
| DS-107 | Superseded by | DS-407 |
| DS-108 | Superseded by | DS-409 |
| DS-109 | Superseded by | DS-410 |
| DS-110 | Merged into | DS-401 |
| DS-111 | Superseded by | DS-411 |
| DS-112 | Superseded by | DS-408 |
| DS-113 | Merged into (data layer); moved to Gate C (presentation) | DS-405; Gate C (no identifier) |
| DS-114 | Merged into | DS-412 |
| DS-201 | Merged and superseded by | DS-501 |
| DS-202 | Merged into | DS-308 |
| DS-203 | Superseded by | DS-503 |
| DS-204 | Superseded by | DS-504 |
| DS-205 | Superseded by | DS-505 |
| DS-206 | Superseded by | DS-506 |
| DS-207 | Superseded by | DS-508 |
| DS-208 | Superseded by (operational); moved to Gate C (presentation) | DS-509; Gate C (no identifier) |
| DS-209 | Superseded by template | TPL-PIPELINE-WITHIN-THEME-ORDERING |
| DS-210 | Superseded by template | TPL-PIPELINE-THEME-LEVEL-ORDERING |
| DS-211 | Superseded by template | TPL-PIPELINE-TIE-BEHAVIOR |
| DS-212 | Merged into | DS-510 |
| DS-213 | Merged into | DS-510 |
| DS-214 | Superseded by | DS-511 |
| DS-215 | Deferred beyond Gate A | Architecture/implementation planning |
| DS-216 | Absorbed into | DS-512 |
| DS-217 | Absorbed into | DS-512 |
| DS-218 | Moved to Gate C | No identifier assigned |

**Old identifiers preserved: 60 DS + 1 RC. All mapped.**

---

## Unresolved Founder Decisions Summary

| Ref | Topic | Status |
|---|---|---|
| DR-005 | Controlled Theme Set selection | Proposed — UNRESOLVED |
| DR-006 | Canonical Theme-role ownership | Deferred |
| DR-007 | Technology stack | Deferred |
| DR-004 | Legacy Knowledge Salvage authorization | Deferred |

In addition, 35 active normalized decision slots (DS-301–DS-310, DS-401–DS-412, DS-501–DS-513) are registered across the three Gate A artifacts. All are Status: Proposed, Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED. None propose investment-rule answers, thresholds, weights, formulas, lookbacks, benchmarks, taxonomies, cohorts, queue ordering, tie-breakers, eligibility rules, aggregations, or fallbacks.

8 templates (TPL-*) await conditional instantiation. 2 inherited controls apply across all artifacts. 1 topic is deferred beyond Gate A. 3 topics are moved to future Gate C without identifiers.

No investment-rule decision has been approved. Gate A completion (DR-009) will confirm structural completeness; individual slot resolution requires separate Founder decisions.

---

## Amendment History

| Date | Change | Authority |
|---|---|---|
| 20 July 2026 | Initial draft with governance entries DR-001 through DR-007 | AM-V0-DESIGN-PLAN-v0.1 |
| 20 July 2026 | Micro-revision: DR-001/DR-002, DR-006 neutrality, DR-007, DR-008 added | AM-V0-FIRST-TRANCHE-MICRO-REVISION |
| 20 July 2026 | Final micro-revision: Decision Obligation Source / Rule Content Authority conversion; DR-003 narrowed and marked UNRESOLVED | AM-V0-FIRST-TRANCHE-FINAL-MICRO-REVISION |
| 20 July 2026 | First tranche repository acceptance; DR-008 approved | AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1 |
| 20 July 2026 | Gate A drafting: DR-003 approved; 60 DS + 1 RC created, all UNRESOLVED; DR-009 added | AM-V0-GATE-A-DRAFTING-v0.1 |
| 20 July 2026 | Gate A slot normalization rewrite: 60 DS + 1 RC → 35 DS + 8 templates; new ranges DS-301+, DS-401+, DS-501+; full supersession map; DR-009 remains Proposed; all slots UNRESOLVED | AM-V0-GATE-A-SLOT-NORMALIZATION-REWRITE-v0.1 |
| 20 July 2026 | AI-authored alternatives removed from all 35 active slots; exact replacement sentence applied | AM-V0-GATE-A-REMOVE-AI-ALTERNATIVES-v0.1 |
| 20 July 2026 | Gate A structural completeness approved; three Gate A artifacts accepted as decision-slot structures; DR-009 approved; all 35 individual slots remain Proposed and unresolved | AM-V0-GATE-A-STRUCTURAL-ACCEPTANCE-v0.1 |
