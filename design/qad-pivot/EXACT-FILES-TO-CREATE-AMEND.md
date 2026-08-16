# Exact Files to Create/Amend — QAD Pivot

> **Status:** Proposed. All amendments are presentation-layer/documentation only during M1–M4B.
> No destructive operations until M15 Cutover.

---

## Phase M1 — Constitutional Pivot (Draft Only — No Ratification)

### AMEND (existing files — text only)

| # | File | Change Type | Scope |
|---|------|-------------|-------|
| 1 | `02-PROJECT-CONSTITUTION.md` | Material amendment | §1, §2, §5, §7, §13, §15, §16, §20 as per Draft Amendment |
| 2 | `00-FOUNDERS-MANIFESTO.md` | Extension | Add QAD specialization paragraph (preserve existing) |
| 3 | `01-PROJECT-DNA.md` | Amendment | Replace DNA-004, update DNA-005 |
| 4 | `AGENTS.md` | Amendment | Domain Index → add QAD specs; Current Phase → QAD-M1; checkpoint sequence |
| 5 | `PROJECT_STATE.md` | Amendment | Current state → QAD design phase; next allowed action |
| 6 | `operational/FOUNDERS-DECISIONS.md` | Addition | Add FD #130 direction |
| 7 | `operational/PRODUCT-VISION.md` | Rewrite | QAD vision (or create separate file) |
| 8 | `operational/EVIDENCE-DOCTRINE.md` | Extension | Add QAD evidence classes, source hierarchy (S1–S6), NotebookLM authority rule |
| 9 | `operational/hermes-organization/ROLE-REGISTRY.md` | Amendment | Add QAD logical roles as reference (not replacement of workforce roles) |
| 10 | `operational/hermes-organization/templates/16-DEEP-RESEARCH-STANDING-CONTRACT.md` | Extension | Add QAD-specific stages |

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 11 | `operational/QAD-SCOPE-AND-NON-SCOPE.md` | New QAD scope document |
| 12 | `operational/QAD-ROADMAP.md` | Roadmap aligned to QAD-M0→M15 |

---

## Phase M2 — Logical Legacy Boundary

### AMEND

| # | File | Change |
|---|------|--------|
| 13 | `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` | Add "SUPERSEDED — replaced by QAD Operating Model" header |
| 14 | `project-definition/DOMAIN-ARCHITECTURE.md` | Add QAD bounded context; mark AM/CS/FO/II contexts as "FROZEN" |
| 15 | `project-definition/EVIDENCE-MODEL.md` | Extend with QAD evidence/claim object definitions |
| 16 | `project-definition/CANDIDATE-AND-QUEUE-MODEL.md` | Add "SUPERSEDED — replaced by QAD Candidate Selection" header |
| 17 | `project-definition/CIW-CONCEPT.md` | Add "ABSORBED INTO QAD — lineage preserved" |

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 18 | `project-definition/qad/QAD-OPERATING-MODEL.md` | M3 deliverable |
| 19 | `project-definition/qad/QAD-CANDIDATE-SELECTION.md` | M3 deliverable |
| 20 | `project-definition/qad/QAD-FULL-RESEARCH-PROTOCOL.md` | M3 deliverable |
| 21 | `project-definition/qad/QAD-CASE-LIFECYCLE.md` | M3 deliverable |
| 22 | `project-definition/qad/QAD-EVIDENCE-MODEL.md` | M3 deliverable |
| 23 | `project-definition/qad/QAD-MODERN-SCUTTLEBUTT.md` | M3 deliverable |
| 24 | `project-definition/qad/QAD-BUSINESS-QUALITY.md` | M3 deliverable |
| 25 | `project-definition/qad/QAD-INDUSTRY-ECONOMICS.md` | M3 deliverable |
| 26 | `project-definition/qad/QAD-FINANCIAL-RECONSTRUCTION.md` | M3 deliverable |
| 27 | `project-definition/qad/QAD-MANAGEMENT-ANALYSIS.md` | M3 deliverable |
| 28 | `project-definition/qad/QAD-TEMPORARY-VS-STRUCTURAL.md` | M3 deliverable |
| 29 | `project-definition/qad/QAD-NORMALIZED-ECONOMICS.md` | M3 deliverable |
| 30 | `project-definition/qad/QAD-PERMANENT-LOSS.md` | M3 deliverable |
| 31 | `project-definition/qad/QAD-VALUATION.md` | M3 deliverable |
| 32 | `project-definition/qad/QAD-RED-TEAM.md` | M3 deliverable |
| 33 | `project-definition/qad/QAD-PUBLICATION-STANDARD.md` | M3 deliverable |
| 34 | `project-definition/qad/QAD-MONITORING.md` | M3 deliverable |

---

## Phase M3 — Role Contracts

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 35 | `contracts/qad/research-director.md` | Role 1: Chief Underwriter |
| 36 | `contracts/qad/evidence-lead.md` | Role 2: Evidence Intelligence |
| 37 | `contracts/qad/investigators/core-desk-research.md` | Role 3: Core Desk |
| 38 | `contracts/qad/investigators/customer-product.md` | Role 4: Customer/Product Scuttlebutt |
| 39 | `contracts/qad/investigators/competitor.md` | Role 5: Competitor Scuttlebutt |
| 40 | `contracts/qad/business-industry-analyst.md` | Role 6: Business & Industry |
| 41 | `contracts/qad/financial-management-analyst.md` | Role 7: Financial & Management |
| 42 | `contracts/qad/impairment-analyst.md` | Role 8: Impairment Diagnosis |
| 43 | `contracts/qad/valuation-analyst.md` | Role 9: Valuation & Expectations |
| 44 | `contracts/qad/structural-red-team.md` | Role 10: Red Team |
| 45 | `contracts/qad/auditor.md` | Role 11: Research Auditor |
| 46 | `contracts/qad/report-editor.md` | Role 12: Thai Report Editor |
| 47 | `contracts/qad/thesis-steward.md` | Role 13: Thesis/Knowledge Steward |
| 48 | `contracts/notebooklm/research-request-contract.md` | NotebookLM research request schema |
| 49 | `contracts/notebooklm/research-result-contract.md` | NotebookLM result schema |
| 50 | `contracts/notebooklm/source-import-contract.md` | Notebook→Registry admission schema |
| 51 | `contracts/notebooklm/discovery-provenance.md` | Discovery provenance tracking |
| 52 | `contracts/publication/final-report-contract.md` | QAD report structure contract |
| 53 | `contracts/publication/thai-typography-standard.md` | Thai PDF typography requirements |

---

## Phase M4A — Schemas

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 54 | `schemas/qad/case.schema.json` | Case state machine + data |
| 55 | `schemas/qad/research-run.schema.json` | Research Run manifest |
| 56 | `schemas/qad/source.schema.json` | Source object |
| 57 | `schemas/qad/evidence.schema.json` | Evidence object |
| 58 | `schemas/qad/claim.schema.json` | Claim object |
| 59 | `schemas/qad/hypothesis.schema.json` | Hypothesis object |
| 60 | `schemas/qad/quality-assessment.schema.json` | Business Quality Assessment |
| 61 | `schemas/qad/dislocation.schema.json` | Dislocation event |
| 62 | `schemas/qad/impairment.schema.json` | Impairment Diagnosis |
| 63 | `schemas/qad/recovery.schema.json` | Recovery Mechanism |
| 64 | `schemas/qad/financial-fact.schema.json` | Financial Fact |
| 65 | `schemas/qad/normalized-economics.schema.json` | Normalized Economics |
| 66 | `schemas/qad/valuation.schema.json` | Valuation + Reverse DCF |
| 67 | `schemas/qad/challenge.schema.json` | Red Team Challenge |
| 68 | `schemas/qad/audit.schema.json` | Audit report |
| 69 | `schemas/qad/underwriting.schema.json` | Underwriting verdict |
| 70 | `schemas/qad/monitoring.schema.json` | Monitoring event |

---

## Phase M4B — Evaluation

### CREATE NEW

| # | File | Description |
|---|------|-------------|
| 71 | `evaluation/EVALUATION-CONTRACT.md` | Evaluation architecture + metrics |
| 72 | `evaluation/historical-cases/case-001-temporary/` | True Temporary fixture |
| 73 | `evaluation/historical-cases/case-002-structural/` | True Structural fixture |
| 74 | `evaluation/historical-cases/case-003-mixed/` | Mixed fixture |
| 75 | `evaluation/historical-cases/case-004-false-quality/` | False Quality fixture |
| 76 | `evaluation/historical-cases/case-005-narrative-panic/` | Narrative Panic fixture |
| 77 | `evaluation/regression/` | Regression test suite structure |

---

## Phase M3 Design Artifacts (Created This Session)

| # | File | Status |
|---|------|--------|
| D1 | `design/qad-pivot/FD-DIRECTION-QAD-DESIGN-AUTHORIZATION.md` | ✅ Created |
| D2 | `design/qad-pivot/REVISED-QAD-MASTER-PLAN.md` | ✅ Created |
| D3 | `design/qad-pivot/CAPABILITY-LEGACY-REUSE-MAP.md` | ✅ Created |
| D4 | `design/qad-pivot/PACK-A-PRODUCTION-ROLE-CONTRACTS.md` | ✅ Created |
| D5 | `design/qad-pivot/PACK-B-CANONICAL-SCHEMAS-AND-STATE-MACHINES.md` | ✅ Created |
| D6 | `design/qad-pivot/PACK-C-EVALUATION-CONTRACT-AND-PIT-FIXTURES.md` | ✅ Created |
| D7 | `design/qad-pivot/DRAFT-CONSTITUTION-V0.5-QAD-AMENDMENT.md` | ✅ Created |
| D8 | `design/qad-pivot/INDEPENDENT-ADVERSARIAL-REVIEW.md` | Upcoming |

---

## NEVER TOUCH (Protected)

| File | Reason |
|------|--------|
| `reports/*.md` | Existing reports — historical/pre-QAD artifacts |
| `research/companies/*` | Research workspaces — preserve lineage |
| `research/mandates/*` | Mandate records — preserve lineage |
| `docs/ciw-pilot-msft/*` | CIW pilot — lineage records |
| `close_system/*`, `alpha-momentum-v0/*`, `fundamental-opportunity-v0/*`, `institutional-intelligence-v0/*` | Frozen until M15 verified-unused |
| `backend/*`, `frontend/*` | Frozen infrastructure |
| `operational/hermes-organization/roles/*` | Workforce roles — unchanged until QAD logical roles approved + migration map created |

<!-- 2026-08-16 UTC+7 -->