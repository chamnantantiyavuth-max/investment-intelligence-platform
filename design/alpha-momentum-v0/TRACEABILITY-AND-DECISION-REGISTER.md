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
- **Topic:** Whether canonical structural Theme roles (Direct Beneficiary, Enabler, Bottleneck Owner, Second-order Beneficiary) belong to Shared Core Entity–Theme relationships, Alpha Momentum Candidate–Theme relationships, or a layered combination
- **Decision Obligation Source:** DOMAIN-ARCHITECTURE §1.1 (\"Canonical Theme relationship ownership — pending Founder decision\"); CANDIDATE-AND-QUEUE-MODEL §3.4
- **Rule Content Authority:** Founder-provided rule (this decision)
- **Affected Artifact(s):** DOMAIN-ARCHITECTURE.md; CANDIDATE-AND-QUEUE-MODEL.md; RULE-PACK-AND-QUALITY-CONTRACTS.md (DS-308)
- **Status:** Approved
- **Resolution:** Shared Core owns canonical Entity–Theme structural roles as the authoritative baseline. Alpha Momentum consumes canonical roles and may refine or add strategy-specific context but must not silently contradict the canonical role. When Theme-level and Candidate-level classifications conflict, Theme-level (Shared Core canonical) wins — consistent with the momentum principle of not fighting the prevailing current.
- **Materiality:** Material — determines architecture ownership of classification authority
- **Decision Category:** Governance
- **Founder Decision Required:** Yes — completed
- **Approval Reference:** AM-V0-FIRST-DECISION-GROUP-v0.1
- **Dependencies:** None
- **Verification Evidence:** Founder explicitly approved in session; Rule: Theme-level classification wins over stock-level; Shared Core owns canonical roles; Alpha Momentum refines without contradicting

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
| DS-301 | V0 Candidate Quality Domain Set | Approved |
| DS-302 | V0 Entry Readiness Domain Set | Approved |
| DS-303 | V0 Theme Quality Consumption Contract | Approved |
| DS-304 | Candidate Quality Output and Summary Policy | Approved |
| DS-305 | Entry Readiness Output and Summary Policy | Approved |
| DS-306 | Theme Quality Output and Summary Policy (Alpha Momentum Consumption) | Approved |
| DS-307 | Strategy-Relevance Policy While Preserving Separate Dimensions | Approved |
| DS-308 | Theme Context Operational Classification (canonical) | Approved |
| DS-309 | Operational V0 Universe Boundary | Approved |
| DS-310 | Additional Alpha Momentum Eligibility Criteria | Approved |

### DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md — 12 Active Slots

| Slot | Topic | Status |
|---|---|---|
| DS-401 | Freshness and Staleness | Approved |
| DS-402 | Completeness and Expected-Data Contract | Approved |
| DS-403 | Reliability | Approved |
| DS-404 | Source Independence and Derivation Classification | Approved |
| DS-405 | Conflict Detection and Preservation | Approved |
| DS-406 | Missing Evidence | Approved |
| DS-407 | Public-Availability Timestamp | Approved |
| DS-408 | Ingestion Timestamp | Approved |
| DS-409 | Effective / As-Of and Forecast-Target Periods | Approved |
| DS-410 | Revision and Vintage Handling | Approved |
| DS-411 | Point-in-Time Visibility | Approved |
| DS-412 | Data Confidence Scope Levels and Roll-Up Policy | Approved |

### PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md — 13 Active Slots

| Slot | Topic | Status |
|---|---|---|
| DS-501 | Operational V0 Universe Boundary in Pipeline Context | Approved |
| DS-502 | Theme Context Stage Behavior | Approved |
| DS-503 | Candidate Quality Assessment — Gate/Rank/Enrichment Effects | Approved |
| DS-504 | Entry Readiness Assessment — Gate/Rank/Enrichment Effects | Approved |
| DS-505 | Data Confidence Assessment — Gate/Warning Effects | Approved |
| DS-506 | Theme-First Queue Assembly | Approved |
| DS-507 | V0 Prioritization Output Form | Approved |
| DS-508 | Adaptive-Capacity Decision Policy | Approved |
| DS-509 | Queue Empty-State Operational Contract | Approved |
| DS-510 | Explainability, Audit, and Rule-Result Lineage Contract | Approved |
| DS-511 | Stock-First Discovery Path Preservation | Approved |
| DS-512 | Logical Stage Dependencies and Input/Output Contracts | Approved |
| DS-513 | Rule Lifecycle, Version, Authority, and Effective-Date Contract | Approved |

**Total Active Gate A Slots: 35** (10 + 12 + 13) — **All 35 Approved** 🎉

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
| DR-006 | Canonical Theme-role ownership | Approved |
| DR-007 | Technology stack | Deferred |
| DR-004 | Legacy Knowledge Salvage authorization | Deferred |

In addition, of the 35 active normalized decision slots (DS-301–DS-310, DS-401–DS-412, DS-501–DS-513) registered across the three Gate A artifacts:
- **3 are now Approved** (DS-301, DS-302, DS-303 — First Decision Group)
- **32 remain Proposed, Resolution: UNRESOLVED — FOUNDER DECISION REQUIRED**
- None propose investment-rule answers, thresholds, weights, formulas, lookbacks, benchmarks, taxonomies, cohorts, queue ordering, tie-breakers, eligibility rules, aggregations, or fallbacks.

8 templates (TPL-*) await conditional instantiation. 2 inherited controls apply across all artifacts. 1 topic is deferred beyond Gate A. 3 topics are moved to future Gate C without identifiers.

**🎉 GATE A COMPLETE — All 35 investment-domain decision slots are Approved.** 1 governance decision (DR-006) also Approved. 8 templates (TPL-*) await conditional instantiation; ordering templates (TPL-PIPELINE-*) remain inactive per DS-507 (unordered). 2 inherited controls apply across all artifacts. 1 topic deferred beyond Gate A. 3 topics moved to future Gate C.

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
| 21 July 2026 | First Decision Group approved: DR-006 (Theme-role ownership), DS-301 (5 Candidate Quality domains: Relative Strength, Accumulation, Liquidity, Growth, Trend Quality), DS-302 (4 Entry Readiness domains: Base Quality, Volatility Contraction, Extension Risk, Breakout Proximity), DS-303 (Theme Quality consumption: all axes, display-only, Market Confirmation shown not filtered) | AM-V0-FIRST-DECISION-GROUP-v0.1 |
| 21 July 2026 | Wave 2 Output Policies approved: DS-304 (Candidate Quality output: Approach B — 2 groups: Trend & Participation, Tradeability & Growth), DS-305 (Entry Readiness output: Approach B — 2 groups: Pattern Quality, Entry Timing), DS-306 (Theme Quality output: Approach B — 3 groups: Theme Structure, Evidence & Confirmation, Risk & Meta) | AM-V0-WAVE-2-OUTPUT-POLICIES-v0.1 |
| 21 July 2026 | Wave 3a Timestamps approved: DS-407 (public-availability: fixture-defined, YYYY-MM-DD), DS-408 (ingestion: fixture-load-time, YYYY-MM-DD HH:MM:SS), DS-409 (effective period: fixture-defined, single date or range, period_type historical/forecast flag). All operational complexity deferred to V0.5. | AM-V0-WAVE-3A-TIMESTAMPS-v0.1 |
| 21 July 2026 | Wave 3b Data Confidence dimensions approved: DS-401 (freshness: fixture-assigned + Constitution §8 3yr narrative default), DS-402 (completeness: fixture-defined expected-field templates per type), DS-403 (reliability: fixture-assigned per source, 4 levels), DS-404 (independence: fixture-assigned per record, 4 EVIDENCE-MODEL categories), DS-405 (conflicts: fixture-injected, mandatory preservation — no averaging), DS-406 (missing evidence: fixture-defined inventory per Theme/Candidate, 3 categories). All operational complexity deferred to V0.5. | AM-V0-WAVE-3B-DIMENSIONS-v0.1 |
| 21 July 2026 | Wave 3c Data Confidence capstone approved: DS-410 (revision: EVIDENCE-MODEL §5.1 hard rules + V0 synthetic demo), DS-411 (visibility: pub_date <= eval_date, staleness is quality flag not visibility gate), DS-412 (scope: no roll-up, 3 levels independent, dimensions displayed separately). Data Confidence artifact: 12/12 complete. | AM-V0-WAVE-3C-CAPSTONE-v0.1 |
| 21 July 2026 | Wave 4 Architecture approved: DS-307 (Strategy-Relevance: 4 dimensions side-by-side, TQ→CQ→ER→DC, no composite score), DS-308 (Theme Context: Filter — Candidate must have Theme to enter pipeline), DS-511 (Stock-First Path: extension point — Universe stage independent of Theme, Theme filter isolated to Stage 2), DS-512 (Stage I/O: linear 6-stage pipeline with explicit contracts). Rule Pack: 8/10 complete. Pipeline: 2/13 resolved. | AM-V0-WAVE-4-ARCHITECTURE-v0.1 |
| 21 July 2026 | Wave 5 Stages approved: DS-309 (Universe: NYSE+NASDAQ+ADRs, fixture-defined), DS-310 (no additional eligibility), DS-501 (Universe stage: boundary filter pass-through), DS-502 (Theme Context stage: filter — Theme ≥ 1), DS-503 (CQ: enrichment), DS-504 (ER: enrichment), DS-505 (DC: warning). Rule Pack: 10/10 complete. Pipeline: 7/13 resolved. 6 slots remain. | AM-V0-WAVE-5-STAGES-v0.1 |
| 21 July 2026 | 🎉 Wave 6 Queue & Governance approved — GATE A COMPLETE: DS-506 (Queue Assembly: Theme-first grouping), DS-507 (Unordered — no prioritization, templates inactive), DS-508 (Show-all — no quality threshold, adaptive = no quota), DS-509 (Empty queue = valid honest output), DS-510 (Per-run audit + per-Candidate explanation), DS-513 (Rule lifecycle: identity, version, authority, effective-date). All 35/35 slots Approved. Gate A: DONE. | AM-V0-WAVE-6-QUEUE-v0.1 |
