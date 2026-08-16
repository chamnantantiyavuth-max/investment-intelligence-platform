# Exact Files to Create/Amend — REVISED

> **Status:** Resolution round — reduced from 77 to ~55 files.
> **Key changes:** 17 QAD specs → 9 core specs. Redundant files eliminated.
> **No destructive operations until M15 Cutover.**

---

## Phase M1 — Constitutional Pivot (Documentation Only)

### AMEND (Existing — Text)

| # | File | Change |
|---|------|--------|
| 1 | `02-PROJECT-CONSTITUTION.md` | §1, §2, §5, §13, §15, §20 per Constitution v0.5 revised draft |
| 2 | `00-FOUNDERS-MANIFESTO.md` | Add QAD specialization paragraph |
| 3 | `01-PROJECT-DNA.md` | Replace DNA-004, update DNA-005 |
| 4 | `AGENTS.md` | Domain Index → QAD specs; current phase → QAD-M1 |
| 5 | `PROJECT_STATE.md` | Current state → QAD design phase |
| 6 | `operational/FOUNDERS-DECISIONS.md` | Add FD #130 direction |
| 7 | `operational/EVIDENCE-DOCTRINE.md` | Add QAD evidence classes, source hierarchy (S1–S6), NotebookLM authority rule |

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 8 | `operational/QAD-PRODUCT-VISION.md` | QAD vision (supersedes old PRODUCT-VISION.md via header annotation) |
| 9 | `operational/QAD-SCOPE-AND-NON-SCOPE.md` | QAD scope document |
| 10 | `operational/QAD-ROADMAP.md` | Roadmap aligned to QAD-M0→M15 |

---

## Phase M3 — QAD Domain Specs (9 Core)

### CREATE NEW

| # | File | Absorbs |
|---|------|---------|
| 11 | `project-definition/qad/QAD-OPERATING-MODEL.md` | Mission, roles, separation of duties, budget, run manifest |
| 12 | `project-definition/qad/QAD-DISCOVERY-AND-SELECTION.md` | Discovery, Hard Gates, Priority Ordering, Selection Engine |
| 13 | `project-definition/qad/QAD-FULL-RESEARCH-PROTOCOL.md` | Case lifecycle, state machine, charter, termination |
| 14 | `project-definition/qad/QAD-EVIDENCE-AND-SOURCE-MODEL.md` | S1–S6, evidence/claim/hypothesis, NotebookLM invariant, provenance |
| 15 | `project-definition/qad/QAD-SCUTTLEBUTT-PROTOCOL.md` | Investigator spawning, questions, limits |
| 16 | `project-definition/qad/QAD-FUNDAMENTAL-ANALYSIS.md` | Business quality, QUALITY_VERIFICATION, false-quality, industry, financial, management |
| 17 | `project-definition/qad/QAD-ECONOMIC-UNDERWRITING.md` | Normalized economics, permanent loss, DCF, reverse DCF, valuation |
| 18 | `project-definition/qad/QAD-IMPAIRMENT-AND-RECOVERY.md` | Impairment diagnosis (dual), dislocation reconstruction, causal chain, recovery mechanism |
| 19 | `project-definition/qad/QAD-CHALLENGE-AUDIT-PUBLICATION-MONITORING.md` | Red Team, Auditor, publication pipeline, monitoring, knowledge compounding |

### AMEND (Existing — Header Only — Not Overwritten)

| # | File | Change |
|---|------|--------|
| 20 | `project-definition/CIW-CONCEPT.md` | Add header: "ABSORBED INTO QAD — lineage preserved. See project-definition/qad/" |
| 21 | `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` | Add header: "SUPERSEDED — replaced by QAD Operating Model" |
| 22 | `project-definition/DOMAIN-ARCHITECTURE.md` | Mark AM/CS/FO/II contexts as "FROZEN"; add QAD bounded context pointer |

---

## Phase M3 — Role Contracts (13 Files) + NotebookLM + Publication

### CREATE NEW

| # | File | Content |
|---|------|---------|
| 23 | `contracts/qad/research-director.md` | Role 1a — execution management, termination proposal |
| 24 | `contracts/qad/chief-underwriter.md` | Role 1b — synthesis, adjudication, confirmation |
| 25 | `contracts/qad/evidence-lead.md` | Role 2 |
| 26 | `contracts/qad/investigators/core-desk-research.md` | Role 3 |
| 27 | `contracts/qad/investigators/customer-product.md` | Role 4 |
| 28 | `contracts/qad/investigators/competitor.md` | Role 5 |
| 29 | `contracts/qad/business-industry-analyst.md` | Role 6 — includes QUALITY_VERIFICATION |
| 30 | `contracts/qad/financial-management-analyst.md` | Role 7 |
| 31 | `contracts/qad/impairment-analyst.md` | Role 8 — dual explanation requirement |
| 32 | `contracts/qad/valuation-analyst.md` | Role 9 |
| 33 | `contracts/qad/structural-red-team.md` | Role 10 — no veto, raw sources start |
| 34 | `contracts/qad/auditor.md` | Role 11 — integrity only, no budget |
| 35 | `contracts/qad/report-editor.md` | Role 12 |
| 36 | `contracts/qad/thesis-steward.md` | Role 13 |
| 37 | `contracts/notebooklm/research-request-contract.md` | NotebookLM request schema |
| 38 | `contracts/notebooklm/research-result-contract.md` | NotebookLM result schema |
| 39 | `contracts/notebooklm/source-import-contract.md` | Notebook→Registry admission + provenance |
| 40 | `contracts/publication/final-report-contract.md` | QAD report structure |
| 41 | `contracts/publication/thai-typography-standard.md` | Default language = Thai (operational, not constitutional) |

---

## Phase M4A — Schemas (~17 JSON Schema Files)

### CREATE NEW

| # | File | Content |
|---|------|---------|
| 42 | `schemas/qad/case.schema.json` | Including QUALITY_VERIFICATION state, versioning |
| 43 | `schemas/qad/research-run.schema.json` | Manifest |
| 44 | `schemas/qad/source.schema.json` | Source object |
| 45 | `schemas/qad/evidence.schema.json` | Evidence + discovery provenance (two-axis) |
| 46 | `schemas/qad/claim.schema.json` | Claim object |
| 47 | `schemas/qad/hypothesis.schema.json` | Hypothesis |
| 48 | `schemas/qad/quality-assessment.schema.json` | Quality + VERIFICATION |
| 49 | `schemas/qad/dislocation.schema.json` | Dislocation event |
| 50 | `schemas/qad/impairment.schema.json` | Impairment (dual) |
| 51 | `schemas/qad/recovery.schema.json` | Recovery mechanism |
| 52 | `schemas/qad/financial-fact.schema.json` | Financial fact |
| 53 | `schemas/qad/normalized-economics.schema.json` | Normalized econ |
| 54 | `schemas/qad/valuation.schema.json` | Valuation + reverse DCF |
| 55 | `schemas/qad/challenge.schema.json` | Challenge + adjudication |
| 56 | `schemas/qad/audit.schema.json` | Audit |
| 57 | `schemas/qad/underwriting.schema.json` | Underwriting |
| 58 | `schemas/qad/monitoring.schema.json` | Monitoring |

---

## Phase M4B — Evaluation (Pre-Code)

### CREATE NEW

| # | File | Content |
|---|------|---------|
| 59 | `evaluation/EVALUATION-CONTRACT.md` | Architecture, metrics, sealed outcomes, famous-case rules |
| 60–69 | `evaluation/input-fixtures/case-0*` | 10 PIT fixture directories (Named/Masked/Synthetic mix) |
| 70 | `evaluation-sealed/outcomes/case-0*/OUTCOME.md` | 10 sealed outcome files (separate directory, no agent access) |

---

## Never Touch (Protected)

- `reports/*.md` — historical
- `research/companies/*` — lineage
- `research/mandates/*` — lineage
- `docs/ciw-pilot-msft/*` — lineage
- `close_system/*`, `alpha-momentum-v0/*`, `fundamental-opportunity-v0/*`, `institutional-intelligence-v0/*` — frozen until M15
- `backend/*`, `frontend/*` — frozen
- `operational/hermes-organization/roles/*` — workforce roles unchanged until QAD logical roles approved + migration map

---

## Reduction Summary

| Metric | v1 | Revised | Delta |
|--------|----|---------|-------|
| Total files | 77 | ~70 | **−9%** (many were always necessary) |
| QAD domain specs | 17 | 9 | **−47%** |
| Role contracts | 13 | 13 | Same (each role distinct) |
| Schemas | 17 | 17 | Same (machine contracts) |
| Evaluation fixtures | 10 | 10 | Same (but better structured) |

The main reduction is spec fragmentation. Role contracts and schemas remain separate because they serve different purposes (human-readable authority boundaries vs machine-validatable data contracts).

<!-- 2026-08-16 UTC+7 -->