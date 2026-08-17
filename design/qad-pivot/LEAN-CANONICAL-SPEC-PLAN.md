# Lean Canonical Spec Plan — 9 Core + 1 Evaluation = 10 Canonical QAD Specifications

> **Status:** Resolution round — 17 original specs consolidated to 10.
> **Rationale:** Reduce context fragmentation, duplicate semantics, conflicting updates, excessive preloading, and documentation bureaucracy.
> **Taxonomy:** 9 core QAD domain specifications + 1 QAD Evaluation specification = 10 canonical.

---

## Canonical Spec Set

| # | Spec | Old Specs Absorbed | Content |
|---|------|--------------------|---------|
| 1 | **QAD-OPERATING-MODEL.md** | (new — no predecessor) | Institution mission, role architecture (13 roles), separation of duties (Selection Engine independent of Underwriting, Red Team no veto, Budget Controller as policy), autonomous research boundaries, budget control design, research run manifest contract |
| 2 | **QAD-DISCOVERY-AND-SELECTION.md** | QAD-CANDIDATE-SELECTION.md, parts of CIW-CONCEPT | **Complete QAD Discovery & Coverage Operating System** (per QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 — NOT merely a ranking/screener): Quality Discovery (open system), Dislocation Radar, 6 registries (Security Master / Researchable Universe / Signal / Candidate / Quality Universe / Case), hard filters vs soft evidence, independent lanes (Quality-first / Dislocation-first / External), Hard Gates + Priority Ordering, candidate outcomes (AUTO_RESEARCH_NOW / WATCH / REJECT), Autonomous Selection Engine policy, Quality Universe maintenance, operating cadence (daily/weekly/monthly/quarterly/event), Radar Scout disposition |
| 3 | **QAD-FULL-RESEARCH-PROTOCOL.md** | QAD-FULL-RESEARCH-PROTOCOL.md, QAD-CASE-LIFECYCLE.md | Case state machine (including QUALITY_VERIFICATION, CASE_UPDATE), Research Charter template, case versioning (v1/v2 with new as-of), termination authority (3-tier), preconditions and quality gates per stage |
| 4 | **QAD-EVIDENCE-AND-SOURCE-MODEL.md** | QAD-EVIDENCE-MODEL.md, QAD-MODERN-SCUTTLEBUTT.md, parts of CIW-EVIDENCE-MODEL | Source classes (S1–S6), evidence/claim/hypothesis schemas, discovery provenance (two-axis: source authority + discovery route), NotebookLM admission invariant (S6 default), NotebookLM contract references, absence semantics |
| 5 | **QAD-SCUTTLEBUTT-PROTOCOL.md** | QAD-MODERN-SCUTTLEBUTT.md (scuttlebutt-specific sections) | Elastic investigator spawning rules, max concurrent investigators (3 unless Chief Underwriter approves), Evidence Gap ID requirement, 12 investigator types with triggering conditions, falsifiable research question mandate |
| 6 | **QAD-FUNDAMENTAL-ANALYSIS.md** | QAD-BUSINESS-QUALITY.md, QAD-INDUSTRY-ECONOMICS.md, QAD-FINANCIAL-RECONSTRUCTION.md, QAD-MANAGEMENT-ANALYSIS.md | Business Quality (6-type moat + Moat Mechanism Protocol), QUALITY_VERIFICATION (VERIFIED/PROBABLE/UNRESOLVED/FAILED), false-quality hypothesis, Industry Economics & Capital Cycle framework, Financial Reconstruction (7–10yr), Management Claim Ledger, Capital Allocation Ledger, Earnings Quality |
| 7 | **QAD-ECONOMIC-UNDERWRITING.md** | QAD-NORMALIZED-ECONOMICS.md, QAD-PERMANENT-LOSS.md, QAD-VALUATION.md | Normalized Economics scenarios (4 types), Permanent-Loss Analysis (3 scenarios), Valuation methods + Reverse DCF, Market-implied vs Evidence-supported comparison, Economic Damage vs Price Damage |
| 8 | **QAD-IMPAIRMENT-AND-RECOVERY.md** | QAD-TEMPORARY-VS-STRUCTURAL.md, parts of CIW-QUALITY-GATES | Impairment Diagnosis (TEMP/MOSTLY/MIXED/STRUCT/UNRESOLVED), Dual explanation requirement, Dislocation Reconstruction, Causal chain tests (peer, market-share, customer-behavior, moat-mechanism, capital-cycle, reversibility), Recovery Mechanism definition (root cause → failure condition) |
| 9 | **QAD-CHALLENGE-AUDIT-PUBLICATION-MONITORING.md** | QAD-RED-TEAM.md, QAD-QUALITY-GATES.md, QAD-PUBLICATION-STANDARD.md, QAD-MONITORING.md | Structural Red Team (independent, no veto, starts from raw sources), Adjudication states, Research Auditor (integrity only, no budget), Thai publication standard (default language = Thai at operational level), publication pipeline, Founder-Ready vs Founder-Endorsed, Thesis monitoring, Thesis Killers, Knowledge Compounding |
| 10 | **QAD-EVALUATION-AND-BENCHMARKING.md** | QAD-EVALUATION-LAB.md (M14 scope — created later) | Evaluation architecture (Named/Masked/Synthetic), 11 metrics, sealed outcomes, subsystem isolation rules, inter-rater agreement (simple rate initially, κ deferred to 30–50+ cases), famous-case leakage classification; **Discovery & Coverage Evaluation (Part 7 — per QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 Part E): Universe Coverage Rate, Data-Ready Coverage, Known-Opportunity Recall, Quality Candidate Recall, Dislocation Recall, False-Negative Rate, Rejected-Item Surprise Rate, Time-to-Detection, Signal→Candidate precision/yield, Candidate→Full-Research yield, cost per meaningful candidate, source/feed failure detection, Decision-Changing Candidate Recall** |

---

## What Remains Separate (NOT consolidated)

| Artifact | Reason |
|----------|--------|
| **Role contracts** (13 individual files) | Each role has distinct authority, tools, model tier, forbidden actions. Merging would increase ambiguity. |
| **JSON schemas** (~17 schema files) | Machine-readable contracts — separate for validation purposes. |
| **NotebookLM contracts** (3 files + 1 provenance contract) | External system interface — deserves own contract boundary. Approval via QAD-EVIDENCE-AND-SOURCE-MODEL + NotebookLM contracts, NOT Constitution. |
| **Publication Contract + Thai Typography Standard** | Operational standards, not domain specs. |
| **Model routing config** | Operational config, lives in Hermes config, not project specs. |

---

## Reduction Summary

| Metric | Original | Revised | Reduction |
|--------|----------|---------|-----------|
| QAD domain specs | ~17 | 9 core + 1 evaluation | **10 canonical** |
| Total estimated files (M1–M4B) | ~77 | ~70 | ~9% reduction (schemas + role contracts are necessary) |
| Spec fragmentation | High | Low | Consolidated by domain area |

### Authoritative Counts

- **9 core QAD domain specifications** (Operating Model, Discovery & Selection, Full Research Protocol, Evidence & Source Model, Scuttlebutt Protocol, Fundamental Analysis, Economic Underwriting, Impairment & Recovery, Challenge-Audit-Publication-Monitoring)
- **1 QAD Evaluation specification** (Evaluation Contract — meta-system for measuring QAD, not QAD analysis domain itself)
- **= 10 canonical QAD specifications total**

File count for M1–M4B is approximately 70 files including: 9 core specs + 1 evaluation spec + 13 role contracts + 3 NotebookLM contracts + 2 publication contracts + ~17 JSON schemas + 10 fixture directories + supporting docs. This is minimal for the scope — each file has a distinct purpose (governance, human-readable authority, machine-validatable contract, or test data).

<!-- 2026-08-16 UTC+7 -->