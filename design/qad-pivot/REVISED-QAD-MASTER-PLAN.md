# Revised QAD Migration Master Plan (M0 → M15)

> **Status:** Design artifact — M0/M1 phases COMPLETE + RATIFIED (16–17 Aug 2026); **M1 = FINAL PASS (17 Aug, independent review PASS WITH FINDINGS → all findings resolved)**; M2–M4B remain pre-code design phases; M5+ implementation gated.
> **Key change from original:** M4 split into M4A (Schemas) + M4B (Evaluation Contract before first code).

---

## Pre-Code Phase: M0 → M4B (Design Only)

### QAD-M0 ✅ (Complete — 16 Aug 2026)
- Current-State Snapshot & Dependency Audit
- Constitutional Pivot Amendment Map
- Reuse/Retirement Matrix
- Repository state reconciled with handoff

### QAD-M1 ✅ (COMPLETE + RATIFIED — 16–17 Aug 2026, FD #130; supersedes the original draft below)
**Original draft deliverables (16 Aug, executed in commit `e0b2143`):**
- Constitution **v0.6** QAD Amendment (§1/§2/§3 redefined QAD; §13/§15/§20 SUPERSEDED; ratified CA-v0.6-QAD-PIVOT)
- Revised 00-FOUNDERS-MANIFESTO.md (QAD Edition)
- Revised 01-PROJECT-DNA.md (v0.3; DNA-005/017 updated, DNA-021 added)
- Reconciled operational/PRODUCT-VISION.md + SCOPE-AND-NON-SCOPE.md (QAD)

**M1 correction closeout (17 Aug, FD #130):** Constitution lineage normalized (v0.6/CA-v0.6); §14 Theme-First → QAD Candidate-First; §5/§16/§17/§18/§21 reconciled; DNA lineage restored (v0.2 CIW + v0.3 QAD); Discovery & Coverage Operating Requirement v0.1 FROZEN. **M1 = FINAL PASS** (independent governance review PASS WITH FINDINGS, all findings resolved — see QAD-M1-CLOSEOUT.md).

### QAD-M2 — Logical Legacy Boundary (Documentation Only)
**Deliverables:**
- Capability-level dependency map (not module-name-based)
- Semantic state assignments: `ACTIVE / FROZEN / SUPERSEDED / VERIFIED_UNUSED / ARCHIVED`
- Legacy capability → QAD capability mapping
- No physical moves/deletion
- No destructive operations

### QAD-M3 — QAD Domain Contracts (Documentation Only)

**Deliverables:** 10 canonical QAD specifications (see `design/qad-pivot/LEAN-CANONICAL-SPEC-PLAN.md`; supersedes earlier 17-spec count). Spec #2 `QAD-DISCOVERY-AND-SELECTION.md` is a **complete QAD Discovery & Coverage Operating System** (not merely a ranking/screener) — must materialize the frozen requirements at `design/qad-pivot/QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md` (v0.1, 2026-08-17): 6 registries, hard filters, independent lanes, operating cadences, Radar Scout disposition, universe policy.

**Pack A — Production Role Contracts** (contained within M3)
**Pack B — NotebookLM Contracts** (Research Request, Result, Discovery Provenance, Source Validation, Notebook↔Registry boundary)

### QAD-M4A — Canonical Schemas & State Machines (Documentation Only)
**Pack B — Canonical Schemas:**
- Case, Research Run, Source, Evidence, Claim, Hypothesis
- Quality Assessment, Dislocation, Impairment, Recovery
- Financial Fact, Normalized Economics, Valuation
- Challenge, Adjudication, Audit, Underwriting, Monitoring
- ID scheme, versioning, lineage, PIT semantics
- State transitions, failure states, retry states
- Founder-Ready vs Founder-Endorsed distinction
- Calculation replay, case replay, append-first update behavior

### QAD-M4B — Pre-Code Evaluation Contract (Documentation Only)
**Pack C — Evaluation Contract:**
- Historical PIT case fixtures (minimum 10 types)
- Acceptance criteria for each analytical stage
- Cost/budget control design (QAD §37)
- Runaway research prevention (QAD §38)
- Baseline metrics: source recall, citation correctness, claim support, contradiction coverage, calculation reproducibility
- Temporary-vs-Structural calibration expectations
- Thesis-killer detection acceptance
- False-confidence rate baseline
- Decision-Changing Evidence Recall methodology
- **Discovery & Coverage Evaluation (Part 7, PACK-C):** Universe Coverage Rate, Data-Ready Coverage, Known-Opportunity Recall, Quality Candidate Recall, Dislocation Recall, False-Negative Rate, Rejected-Item Surprise Rate, Time-to-Detection, Signal→Candidate precision/yield, Candidate→Full-Research yield, cost per meaningful candidate, source/feed failure detection, Decision-Changing Candidate Recall — per QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 Part E (M1 correction, 2026-08-17)

---

## 🚧 PRE-CODE DESIGN GATE 🚧

**Packs A/B/C must pass:**
- Independent adversarial review
- Founder review
- All required changes confirmed satisfied

**Gate clears:**
- FD #131 — Constitution Amendment Artifact (with actual text)
- FD #132 — Legacy Boundary (with actual map)
- FD #133 — QAD Master Plan (with actual migration sequence)
- FD #134 — Autonomous Research Selection
- FD #135 — NotebookLM First-Class Status
- FD #136 — Model Tiers (reconciled with current routing)
- FD #137 — Role Contracts Approval

---

## Implementation Phase: M5 → M14 (Production Code)

### QAD-M5 — Autonomous Discovery
- Quality Discovery (open system per QAD §7)
- Quality Universe maintenance
- Dislocation Radar
- Autonomous Selection with Hard Gates (QAD §6)
- Candidate outcomes: AUTO_RESEARCH_NOW / WATCH_FOR_PRICE / WATCH_FOR_EVIDENCE / DATA_LIMITED_WATCH / REJECT
- Priority ordering per QAD §6.3

### QAD-M6 — Source Intelligence / Gemini Notebook Engineering

> **Founder direction (9 Sep 2026 — M6 planning clarification only, NOT an implementation authorization):**
> `deep_research_provider` → **Gemini Notebook Deep Research** (primary/default); `research_corpus_provider` → **Gemini Notebook** (formerly NotebookLM).
> The provider abstraction in frozen contracts (Evidence/Source Model §4) is RETAINED — Gemini Notebook is the M6 implementation binding, not a replacement for the abstract architecture.
> Gemini AI / Gemini App Deep Research and standalone paid Gemini Deep Research API = **OUT of default M6 scope** (no parallel Hermes → Gemini AI DR → export → Notebook pipeline; a future Founder Decision may authorize exceptions).
> Economic default = Founder-paid Google AI annual subscription capability; no duplicate DR runs across Gemini products; Deep Research allocated to material evidence gaps, not indiscriminately.
> M6 remains **NOT STARTED**. Historical/frozen "NotebookLM" references are preserved (lineage kept; no mass rename).

- SEC/IR/web source handling
- NotebookLM research lifecycle integration
- **Gemini Notebook Deep Research — evidence-gap-driven** (Full Research Protocol Stage 4 → Stage 5): each request traceable to existing anchors (case_id, case_version, research_run_id, evidence_gap_id equivalent, research question, AS_OF/PIT context, requester/role, timestamp, Notebook identity, result artifact, discovered + imported source lists, validation disposition)
- **Web-enabled external source discovery** — Gemini Notebook Deep Research is NOT corpus-only; it may discover sources outside the existing notebook corpus
- **Deep Research report + cited/uncited source-candidate handling → source review / selective import** (no blind "Import All" as production policy): prefer original/primary sources for material claims, preserve contradicting sources, deduplicate syndicated copies, record disposition (imported / rejected / unavailable / deferred)
- **Non-canonical boundary preserved** (M5.2 §3 `NonCanonicalResearchArtifactStore` / Research Room): Deep Research report, Notebook chat output, and discovered sources are NON-CANONICAL until original-source validation and canonical admission — never masquerade as the Canonical Evidence Registry
- **PIT isolation (LIVE vs SEALED/REPLAY):** dedicated PIT-isolated notebook/workspace per sealed case_version / AS_OF, or provable sealed source-snapshot mechanism — a persistent notebook must never backdoor Point-in-Time controls (upstream research-context leakage prevented, not just downstream admission)
- **Deep Research observability / run-manifest integration** — DR runs, notebook_runs, providers, model/token telemetry on RRM-01 existing MUTABLE fields; failure/retry semantics consistent with frozen contracts (S10/S8); browser/UI automation of the subscription surface, if needed, lives behind the adapter boundary (FD #105 R4 technical blocker recorded; one-time Founder Chrome remote-debugging approval required before any leaned-on automation)
- Source validation and deduplication
- Discovery provenance tracking
- Notebook → Canonical Evidence Registry admission bridge

### QAD-M7 — Research Workforce / Modern Scuttlebutt
- Core Desk Research
- Evidence Lead role
- Dynamic Scuttlebutt investigator spawning (per QAD §12)
- Elastic network: Customer/Product, Competitor, Supplier, Channel/Distributor, Employee/Organization, Digital/Social, Regulatory, Technology/IP, Scientific/Clinical, Geographic/Industry Specialist
- Every investigator receives falsifiable research question (QAD §12)

### QAD-M8 — QAD Analytical Core
- Business Quality & Moat Mechanism Protocol (QAD §18)
- Industry Economics & Capital Cycle (QAD §19)
- Financial Reconstruction 7–10 years (QAD §20)
- Management Claim Ledger + Capital Allocation Ledger (QAD §21)
- Dislocation Reconstruction + Timeline (QAD §22)
- Impairment Diagnosis — Temporary/Mostly/Mixed/Structural/Unresolved (QAD §23)
- Recovery Mechanism with causal chain (QAD §24)

### QAD-M9 — Normalization & Valuation
- Normalized Economics scenarios (Current/No Recovery/Partial/Normalization/Compounding)
- Permanent-Loss Analysis (Mild/Severe/Thesis-Break)
- Deterministic valuation methods
- Reverse DCF / Market-Implied Expectations
- Economic Damage vs Price Damage comparison

### QAD-M10 — Red Team & Audit
- Structural Deterioration Red Team (operationally independent)
- Red Team Adjudication (Accepted/Partially/Rejected/Unresolved)
- Independent Research Auditor (source exists, citation supports claim, PIT, calculation reproducible)
- Audit failure blocks Founder-ready publication

### QAD-M11 — Thai PDF Publication
- Chief Underwriter Synthesis (single coherent narrative voice)
- Thai Long-Form Editorial Pass
- Citation Pass
- Deterministic Numeric Pass
- PDF Renderer (selected via comparative benchmark: HTML/CSS→PDF, Playwright/Chromium, WeasyPrint, or other)
- Visual QA

### QAD-M12 — Thesis Monitoring
- Thesis-aware monitoring (not generic news feed)
- Recovery indicators tracking
- Monitoring states: Recovery-Confirming / On-Track / Uncertain / Weakening / Broken
- Thesis Killers (predefined falsification conditions)
- Founder-ready update reports

### QAD-M13 — Knowledge Compounding
- Industry Playbooks
- Cross-case validation before promotion
- Independent review before Approved Knowledge
- Research Finding → Candidate Lesson → Cross-Case Validation → Independent Review → Approved Knowledge → Industry Playbook
- Notebook/Obsidian sync where authorized

### QAD-M14 — Full Evaluation Lab
- Expanded historical case corpus
- Point-in-time fixture regression
- Source/citation/calculation test suite
- Temporary-vs-Structural calibration benchmarks
- Report factual error rate tracking
- Decision-Changing Evidence Recall metrics
- Report regressions

### QAD-M15 — Cutover
- QAD becomes canonical IIP identity
- Legacy paths → verified-unused → archived
- Final consistency audit
- Rollback verification
- Founder acceptance

<!-- 2026-08-16 UTC+7 -->
<!-- 2026-09-09 15:10 UTC+7 (M6 planning clarification — Gemini Notebook Deep Research direction; planning only, M6 NOT STARTED; patch isolated on docs/m6-gemini-notebook-dr pending M5.3 re-audit pin) -->
