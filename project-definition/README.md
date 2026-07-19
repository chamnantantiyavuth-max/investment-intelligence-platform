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
| Constitution + Amendments | `02-PROJECT-CONSTITUTION.md`, `05-FOUNDATION-AMENDMENT-v0.2.md`, `06-CONSTITUTIONAL-AMENDMENT-v0.3.md` | Approved (v0.3) |
| Founder's Decisions | `operational/FOUNDERS-DECISIONS.md` | Approved |
| Operational Policies | `operational/*.md` | Approved |
| **Project Definition Index** | `project-definition/README.md` | **Approved (v0.1)** |
| **Approved Domain Specifications** | `project-definition/DOMAIN-ARCHITECTURE.md`, `project-definition/THEME-MODEL.md`, `project-definition/EVIDENCE-MODEL.md`, `project-definition/CANDIDATE-AND-QUEUE-MODEL.md`, `project-definition/HUMAN-REVIEW-AND-LEARNING-MODEL.md`, `project-definition/ALPHA-MOMENTUM-V0-SPEC.md` | **Approved (v0.1)** |
| ADRs | (not yet created) | Future |
| Implementation Plans | (not yet created) | Future |

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
- Canonical Theme-role ownership remains an unresolved Founder decision.
