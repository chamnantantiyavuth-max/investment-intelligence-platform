# Alpha Momentum V0 Design

Status: Approved Design Area Index
Version: 0.1
Owner: Founder
Authority: Approved design-area index subordinate to the Constitution, Founder's Decisions, Approved Domain Specifications, and the Approved Stable Design Plan; it is not independent investment-rule authority
Derived from: Constitution v0.3 and Project Definition v0.1
Plan Approval: AM-V0-DESIGN-PLAN-v0.1
Repository Acceptance: AM-V0-FIRST-TRANCHE-REPOSITORY-ACCEPTANCE-v0.1

## Purpose

This directory contains the Alpha Momentum V0 Design artifacts. They translate the Constitution and approved Project Definition specifications into decision slots, contracts, fixtures, and acceptance criteria that will govern the V0 implementation.

This README is a design-area index. It contains no investment rules.

## Authority

- This directory and all artifacts within it are subordinate to the Constitution, Founder's Decisions, and Approved Domain Specifications (project-definition/).
- No artifact in this directory may override, narrow, or contradict a higher-authority document.
- When a conflict with higher authority is identified, the design path must stop and record UPSTREAM AMENDMENT REQUIRED.

## Artifact Map

| # | File | Type | Purpose |
|---|---|---|---|
| 1 | `README.md` | Approved Design Area Index | This index |
| 2 | `DESIGN-PLAN.md` | Approved Stable Design Plan | Phase objective, scope, non-scope, deliverable map, dependency order, Gate A–D structure, materiality policy, amendment process, Legacy Salvage insertion window, rollback and verification requirements |
| 3 | `TRACEABILITY-AND-DECISION-REGISTER.md` | Living Register | Decision slots with identifier, topic, decision obligation source, rule content authority, affected artifact, status, materiality classification, rationale, Founder decision required, approval reference, dependencies, verification evidence |
| 4 | `RULE-PACK-AND-QUALITY-CONTRACTS.md` | Decision Slots (Gate A) | Candidate Quality, Theme Quality, Entry Readiness, Alpha Momentum strategy-owned feature and rule semantics |
| 5 | `DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md` | Decision Slots (Gate A) | Data Confidence, public-availability semantics, timestamps, revision and vintage handling, missing and conflicting evidence, freshness and staleness, point-in-time visibility |
| 6 | `PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md` | Decision Slots (Gate A) | Stage contracts, inputs/outputs, enrichment vs. gate classification, queue assembly, adaptive-capacity behavior, empty-state behavior, explainability and audit output |
| 7 | `CONTROLLED-THEME-SET.md` | Gate B Artifact | Theme names, structural drivers, V0 inclusion rationale, assessment against approved Theme-selection criteria, intended lifecycle/Approval/Monitoring status, domain and acceptance cases covered |
| 8 | `THEME-CARD-AND-HUMAN-REVIEW-FLOW.md` | Decision Slots (Gate C) | Required Theme Card information, human-review flow, Human Override visibility, preservation of machine dissent, unresolved evidence visibility, Research State transitions |
| 9 | `FIXTURE-AND-ACCEPTANCE-SCENARIOS.md` | Acceptance Criteria (Gate C) | Technology-neutral fixture shapes, required fields and relationships, synthetic fixture category, Founder-approved fixed historical public snapshot category, known-answer scenarios, Given/When/Then acceptance cases, contradiction and missing-evidence cases, traceability to the 10 approved V0 acceptance criteria |
| 10 | `ADRs/` | On-Demand (Gate C/D) | Created only when a real cross-cutting decision arises; not pre-populated |

## Gate Structure

| Gate | Artifacts Reviewed | What Is Approved |
|---|---|---|
| **Plan Approval** | DESIGN-PLAN.md | Phase transition, file plan, scope, dependency order, gate structure, materiality policy, Legacy Salvage insertion window |
| **Gate A** | RULE-PACK, DATA-CONFIDENCE, PIPELINE, TRACEABILITY register | Core contract questions and decision slots; all Founder decisions required before deterministic V0 behavior |
| **Optional: Legacy Salvage** | Separately authorized read-only access | Historical inputs labeled UNTRUSTED HISTORICAL INPUT — NOT AUTHORITY |
| **Gate B** | CONTROLLED-THEME-SET.md | Theme definitions for V0 design and fixtures |
| **Gate C** | THEME-CARD-AND-HUMAN-REVIEW-FLOW, FIXTURE-AND-ACCEPTANCE-SCENARIOS, any required ADRs, updated TRACEABILITY register | Human Review flow, fixtures, acceptance scenarios |
| **Gate D** | All artifacts, completed TRACEABILITY register | Design completion and implementation readiness |

## Current State

| File | Status |
|---|---|
| `README.md` | Approved Design Area Index v0.1 |
| `DESIGN-PLAN.md` | Approved Stable Design Plan v0.1 |
| `TRACEABILITY-AND-DECISION-REGISTER.md` | Accepted Living Design Register v0.1 |
| All other artifacts | Not yet created or authorized for drafting |

## Reading Order

1. Start with `DESIGN-PLAN.md` for the phase objective, scope, and governance.
2. Read `TRACEABILITY-AND-DECISION-REGISTER.md` for the current state of all decisions.
3. Gate A artifacts define decision slots — read them before Gate A review.
4. Gate B and Gate C artifacts are drafted only after their predecessor gates are approved.

## Non-Scope (This Design Phase)

This design phase does not authorize:

- Investment rule population (thresholds, weights, formulas, lookbacks, benchmarks, taxonomies, cohorts, queue ordering, tie-breakers, fallback behavior, scoring aggregation)
- Technology stack selection
- Schema, migration, or persistence design
- Dependency installation
- Application code
- Live or current market data
- Production ingestion
- Broker or private-account data
- Fixture population or external data access
- Modification of any existing file outside this directory
- Automatic creation of any Git tag or checkpoint. Any tag or checkpoint requires a separate exact named Founder authorization after the relevant artifacts pass review.
