# Project Definition — Investment Intelligence Platform

Status: Approved Project Definition Index
Version: 0.1
Owner: Founder
Authority: Approved index subordinate to the Constitution and Founder's Decisions; it does not override the constituent Approved Domain Specifications
Derived from: Investment Intelligence Platform Constitution v0.3
Approval: PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS

## Purpose

This directory contains the Project Definition documents. They translate the Constitution and operational policies into formal domain models that bridge constitutional principles to implementation guidance.

The six substantive documents in this directory are **Approved Domain Specifications v0.1** under approval PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS. This README is an **Approved Project Definition Index**.

## Relationship to the Foundation

| Layer | Location | Status |
|---|---|---|
| Constitution + Amendments | `02-PROJECT-CONSTITUTION.md`, `05-FOUNDATION-AMENDMENT-v0.2.md`, `06-CONSTITUTIONAL-AMENDMENT-v0.3.md` | Approved (v0.4) |
| Founder's Decisions | `operational/FOUNDERS-DECISIONS.md` | Approved (#1-44) |
| Operational Policies | `operational/*.md` | Approved |
| **Project Definition Index** | `project-definition/README.md` | **Approved (v0.1)** |
| **Approved Domain Specifications** | `project-definition/DOMAIN-ARCHITECTURE.md`, `project-definition/THEME-MODEL.md`, `project-definition/EVIDENCE-MODEL.md`, `project-definition/CANDIDATE-AND-QUEUE-MODEL.md`, `project-definition/HUMAN-REVIEW-AND-LEARNING-MODEL.md`, `project-definition/ALPHA-MOMENTUM-V0-SPEC.md` | **Approved (v0.1)** |
| **Approved Operating Model** | `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` | **Approved (v0.1)** |
| ADRs | `.hermes/architecture/ADR-001-react-shadcn-frontend.md` | Approved retroactively (FD #44, 2 Aug 2026) |
| Implementation Plans | (per-phase plans; see `design/` and git history) | Future |

The Constitution is the authority. These documents derive from it without altering it.

## Document Map

| # | File | Content |
|---|---|---|
| 1 | `README.md` | This index |
| 2 | `DOMAIN-ARCHITECTURE.md` | Bounded contexts, entity relationships, Shared Core boundary, information flow |
| 3 | `THEME-MODEL.md` | Theme entity, lifecycle, governance, transitions, discovery, Weak Signal Inbox, Theme Card |
| 4 | `EVIDENCE-MODEL.md` | Information and record taxonomy, provenance, independence, aging, tombstoning, progression, Data Confidence |
| 5 | `CANDIDATE-AND-QUEUE-MODEL.md` | Candidate entity, four quality dimensions, three candidate axes, Theme-first Research Queue |
| 6 | `HUMAN-REVIEW-AND-LEARNING-MODEL.md` | Human Override entity, Learning contracts (Decision, Outcome, Postmortem, Lesson) |
| 7 | `ALPHA-MOMENTUM-V0-SPEC.md` | V0 specification: controlled universe, theme selection criteria, screening pipeline, acceptance criteria |
| 8 | `INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` | Dual intelligence operating model: Fundamental & Opportunity + Momentum & Market Leadership paths, Shared Core, Independent Challenge, Founder Decision Gate |

### CIW Specifications v0.2 (Phase 11 — company-intelligence-workbench/)

> **Approved v0.2 (FD-CIW-008, 2 Aug 2026).** CIW (Company Intelligence Workbench) is the deferred Phase 11 Deep Research Handoff workflow inside the Fundamental & Opportunity path — concept approved in principle only (FD-CIW-001..007). Phase 11 implementation remains deferred per FD #44; these documents are documentation-only and do not authorize implementation, pilot, schema, or Cron. Targeted amendments to existing approved documents require separate approval.

| # | File | Content |
|---|---|---|
| 9 | `company-intelligence-workbench/CIW-CONCEPT.md` | What CIW is: bounded deep-research handoff in FO path (not a 5th layer); authorization status; responsibility matrix; universe boundary; valuation advisory; pilot scope |
| 10 | `company-intelligence-workbench/CIW-RESEARCH-FRAMEWORK.md` | Research methodology (advisory, FD-CIW-003); required separations; applicability-based Modules A–Q; valuation discipline; portfolio-blind; source discipline; final challenge |
| 11 | `company-intelligence-workbench/CIW-LIFECYCLE.md` | CIW research statuses mapped to approved Candidate Research States; thesis status mapping; artifact authority states; transition matrix |
| 12 | `company-intelligence-workbench/CIW-REQUEST-CONTRACT.md` | Research Request contract: Research Gate, request fields, pilot source gate, automation limits, failure semantics, approval flow |
| 13 | `company-intelligence-workbench/CIW-RESULT-CONTRACT.md` | Structured Research Result contract: source-coverage report, claim/calculation lineage, evidence discipline, completeness states |
| 14 | `company-intelligence-workbench/CIW-QUALITY-GATES.md` | Mandatory independent review (executor/reviewer separation); minimum quality gates; completion standard; first-slice gate order |
| 15 | `company-intelligence-workbench/CIW-PUBLICATION-STANDARD.md` | Founder review for every canonical change (FD-CIW-004); deterministic-metadata allowlist; Cron Class A+B only (FD-CIW-005); append-first; Obsidian narrative-only (FD-CIW-006) |

## Version Boundaries

| Version | Data | Themes | Discovery |
|---|---|---|---|
| **V0** | Fully synthetic fixtures or Founder-approved fixed historical public snapshots | Founder-approved controlled set | None (manual) |
| **V0.5** | Real EOD with provenance, reconciliation, point-in-time | Same controlled set | None |
| **V1** | Real EOD | Controlled + Experimental | Human-assisted or deterministic |
| **V1.5** | Real EOD | Full spectrum | AI-driven hybrid |
| **Later** | Real EOD | Full spectrum | AI-driven hybrid + Learning Loop, Close System, Global, Deep Research |

## Reading These Documents

- Start with `DOMAIN-ARCHITECTURE.md` for the overall structure.
- Each model document defines entities, states, relationships, and constraints in technology-neutral terms.
- `ALPHA-MOMENTUM-V0-SPEC.md` defines what V0 must prove — read it last.
- All documents reference the Constitution; where they appear to extend it, the Constitution controls.

## Authority

- This README is an approved index and authority map. It is not an independent Domain Specification and does not override the Constitution, Founder's Decisions, or the constituent Approved Domain Specifications.
- The six substantive documents in this directory are Approved Domain Specifications v0.1, subordinate to the Constitution and Founder's Decisions.
- Omission in a specification does not cancel a higher-authority requirement.
- Canonical Theme-role ownership resolved by FD #26 (23 July 2026): Shared Core owns canonical Entity–Theme structural roles; Theme-level classification wins over stock-level.
<!-- 2026-08-02 23:48 UTC+7 -->
