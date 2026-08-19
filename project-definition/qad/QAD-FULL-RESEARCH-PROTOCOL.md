# QAD Full Research Protocol

> **Contract:** M3-03 (M3 Domain Contract Set)
> **Status:** M3 FINAL DRAFT (CORRECTION COMPLETE — AWAITING INDEPENDENT RE-REVIEW)
> **Authority:** FD #130; Constitution §14 (Candidate-First); CIW Protocol (CAP-009 — ABSORB with lineage); FD #95 (WP3 Deep Research Contract); FD #87 (RM-2026-0004 protocol)
> **Traceability:** CAP-009 (ABSORB) · CIW §3 (Actor/Artifact Map) · CIW §5 (Quality Gates) · CIW Result Contract · FD #87 · FD #95 · EVIDENCE-DOCTRINE · CONSTITUTION-§16 · NEW_M3_DERIVATION (H1–H5 mandate, stage decomposition)
> **Inherits:** CIW protocol as lineage base; this contract evolves and supersedes the CIW protocol for QAD research.

---

## 1. Purpose

Define the complete, repeatable protocol for conducting full QAD research on a candidate company. The protocol ensures:

- Every case begins with explicit competing hypotheses
- Evidence is gathered systematically, not opportunistically
- Analytical work is structured but not mechanical
- Challenge and audit are independent from thesis creation
- The final research verdict is supported by evidence, not narrative

---

## 2. Competing Hypotheses (MANDATORY — Every Case)

Every full QAD case MUST begin with the five competing hypotheses documented in the Research Charter. The architecture must make it impossible for the workflow to silently collapse these into one bullish thesis.

```text
H1 = Temporary impairment  — quality business, temporary headwind, likely recovery
H2 = Structural deterioration — business model or industry permanently damaged
H3 = Mixed — genuine quality loss in some areas, intact in others; net direction unclear
H4 = Quality assumption itself is wrong — it was never a high-quality business
H5 = Problem is real but valuation is already fair/unattractive — impairment may be real
     but the market price already reflects it (no asymmetry)
```

### Hypothesis Handling Rules

- H1–H5 must be explicitly stated at Case Open, before any analytical work begins
- Each hypothesis gets an initial probability/plausibility assessment (qualitative: PLAUSIBLE / IMPLAUSIBLE / UNCLEAR)
- Analytical work must address at least H1 vs H2 as the primary fork
- The final verdict must explain why the dominant hypothesis was chosen over each alternative
- If evidence during research shifts probabilities materially, record the shift with timestamp and trigger

---

## 3. Research Stages

### Stage 1 — Case Open

**Action:** Case record created in CASE REGISTRY. Research Director assigned.

**Inputs:**
- Candidate from CANDIDATE REGISTRY with selection state = AUTO_RESEARCH_NOW
- Candidate evidence package (signals, quality flag, dislocation flag)

**Outputs:**
- Case ID (CASE-YYYY-NNN)
- Research Director assignment
- Initial priority and budget allocation
- `case_state = CASE_OPEN`

**Quality Gate:** Case must have a verifiable entity in SECURITY_MASTER. Minimum data requirements must be met (recent filings, price data, basic financials).

### Stage 2 — Research Charter

**Action:** Research Charter created. This is the binding research contract for the case.

**Inputs:**
- Candidate evidence package
- Preliminary entity overview

**Outputs:**
- Research Charter containing:
  - Case ID and entity
  - **Competing Hypotheses H1–H5** with initial plausibility
  - Key research questions
  - Evidence scope (what sources will be consulted)
  - Budget estimate
  - Expected timeline
  - Initial Evidence Gap Map (what is known vs unknown)
- `case_state = CHARTER_APPROVED`

**Quality Gate:** Charter must contain explicit H1–H5. If any hypothesis is absent, the case cannot proceed.

**Charter approval chain:**
- **Research Director** drafts/owns the Research Charter
- **Evidence Intelligence Lead** validates: H1–H5 presence, falsifiability of each hypothesis, evidence scope completeness, source plan appropriateness, material blind spots explicitly listed
- **Research Budget Controller** authorizes budget under policy
- **Chief Underwriter does NOT approve Charter** — preserves fresh judgment until underwriting stage

Evidence Lead validation is protocol/evidence completeness, NOT thesis approval.

> **M4A Note:** The Case schema is defined jointly across this contract and QAD-OPERATING-MODEL.md (M3-01). See M3-01 §3 (State Ownership) and M3-01 §8 (Run Manifest) for case_id, version, manifest fields. This contract defines stage states, charter content, and lifecycle transitions. M4A implementers MUST read both contracts.

### Stage 3 — Primary Source Foundation

**Action:** Gather and index primary source documents.

**Inputs:**
- Entity identity
- Filing history (10-K, 10-Q, 8-K, proxy, etc.)
- Industry reports
- Market data

**Outputs:**
- Source index (all primary documents collected)
- Raw Source Archive references
- Initial FACT/CLAIM/INFERENCE extractions
- `case_state = SOURCE_FOUNDATION_COMPLETE`

**Quality Gate:** At minimum, last 7–10 years of annual filings + most recent quarterly. If filings are insufficient for the company's history, document the gap.

### Stage 4 — Initial Analysis & Evidence Gap Map

**Action:** Analyst reads primary sources and identifies what is known, what is claimed, and what is unknown.

**Inputs:**
- Primary source foundation
- Research Charter with key questions

**Outputs:**
- Evidence Gap Map (structured: known facts / unresolved questions / evidence needed)
- Initial analytical notes per dimension (quality, industry, financial, management)
- `case_state = INITIAL_ANALYSIS_COMPLETE`

**Quality Gate:** Gap Map must be specific enough that a Scuttlebutt investigator could act on individual gaps. Vague "need more research" is insufficient.

### Stage 5 — Deep Research

**Action:** Systematic investigation to close evidence gaps. May involve multiple specialized investigators.

**Inputs:**
- Evidence Gap Map
- Research Charter

**Outputs:**
- Deep Research notes per gap
- Additional sources collected
- Updated Claim/Evidence graph
- Gap Map updated (closed gaps marked; new gaps may appear)
- `case_state = DEEP_RESEARCH_COMPLETE`

**Quality Gate:** Each original evidence gap has a disposition (CLOSED / PARTIALLY_CLOSED / DEFERRED / UNRESOLVED). Budget exhaustion → `INCOMPLETE`, not weakened gate.

### Stage 6 — Scuttlebutt (Elastic Investigation)

**Action:** Deploy elastic investigators for evidence gaps that cannot be closed by desk research alone.

**Inputs:**
- Evidence Gap Map (gaps requiring primary ecosystem intelligence)
- Scuttlebutt Charter per investigator

**Outputs:**
- Investigation reports
- New evidence objects admitted to Canonical Evidence Registry
- `case_state = SCUTTLEBUTT_COMPLETE` (may be skipped if no gaps require it)

**Quality Gate:** Each investigator has a specific evidence gap ID, falsifiable question, allowed sources, and stop rule. No open-ended investigation.

### Stage 7 — Canonical Admission

**Action:** Evidence from all research streams is validated and admitted to the Canonical Evidence Registry.

**Inputs:**
- All research outputs
- Raw source references
- NotebookLM/Deep Research results (non-canonical — must validate against original source)

**Outputs:**
- Canonical Evidence Registry entries (FACT / CLAIM / INFERENCE / HYPOTHESIS)
- Each entry tagged with source, PIT, confidence, and status
- `case_state = EVIDENCE_CANONICAL`

**Quality Gate:** Material finding discovered through AI synthesis must be validated against original source before canonical admission. L10 evidence (social/forum) cannot independently support a material conclusion.

### Stage 8 — Quality Analysis

**Action:** Systematic quality assessment (detailed in M3-06 Business/Industry/Management Contract).

**Inputs:**
- Canonical Evidence Registry (quality-relevant entries)
- Industry context

**Outputs:**
- Quality Assessment: `VERIFIED / PROBABLE / UNRESOLVED / FAILED`
- Moat analysis (mechanism, width, depth, trend)
- `case_state = QUALITY_ANALYSIS_COMPLETE`

### Stage 9 — Industry / Financial / Management Analysis

**Action:** Structured analysis across three dimensions (detailed in M3-06, M3-08).

**Inputs:**
- Canonical Evidence Registry
- Quality Assessment

**Outputs:**
- Industry Economics analysis (demand→supply→capacity→pricing→margins→ROIC→entry/exit)
- Financial Reconstruction (7-10+ years: revenue bridge, margins, FCF, ROIC, working capital, leverage, per-share)
- Management Assessment (Decision History Ledger, Capital Allocation, Promises vs Outcomes)
- `case_state = ANALYTICAL_WORK_COMPLETE`

### Stage 10 — Dislocation Reconstruction & Impairment Diagnosis

**Action:** Reconstruct what broke and diagnose severity (detailed in M3-07).

**Inputs:**
- Financial Reconstruction
- Industry context
- Market data

**Outputs:**
- Dislocation Reconstruction (what broke, cause, peer test, moat test, reversibility)
- Impairment Diagnosis: `TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED`
- Recovery Model (cause→mechanism→evidence→sequence→horizon→invalidation)
- `case_state = IMPAIRMENT_DIAGNOSIS_COMPLETE`

### Stage 11 — Normalized Economics & Valuation

**Action:** Construct normalized economics and estimate valuation asymmetry (detailed in M3-08).

**Inputs:**
- Financial Reconstruction
- Impairment Diagnosis
- Recovery Model

**Outputs:**
- Normalized Economics (CURRENT / NO_RECOVERY / PARTIAL_RECOVERY / NORMALIZATION / QUALITY_COMPOUNDING scenarios)
- Permanent Loss Analysis
- Balance-sheet runway assessment
- Reverse DCF (price-implied expectations)
- Economic Damage vs Price Damage comparison
- Valuation asymmetry estimate
- `case_state = VALUATION_COMPLETE`

### Stage 12 — Structural Red Team

**Action:** Independent challenge (detailed in M3-09).

**Inputs:**
- Full analytical package (Stages 8–11)
- Charter: assume QAD thesis is wrong

**Outputs:**
- Strongest value-trap case
- `challenge_outcome = ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED`
- `case_state = RED_TEAM_COMPLETE`

### Stage 13 — Independent Audit

**Action:** Verification of source, citation, PIT, calculation integrity (detailed in M3-09).

**Inputs:**
- Full research record (all stages)
- Raw sources

**Outputs:**
- Audit Report
- `audit_outcome = PASS / PASS_WITH_FINDINGS / FAIL`
- May block `FOUNDER_READY`
- `case_state = AUDIT_COMPLETE`

### Stage 14 — Chief Underwriting

**Action:** Synthesis of all analytical work, challenge, and audit into a final research verdict (detailed in M3-09).

**Inputs:**
- All stage outputs (8–13)
- Audit Report
- Red Team case

**Outputs:**
- Research Verdict: `QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION`
- `case_state = UNDERWRITING_COMPLETE`

### Stage 15 — Publication

**Action:** Thai long-form article written and prepared for Founder review.

**Inputs:**
- Full research record
- Verdict

**Outputs:**
- Thai long-form publication (draft)
- `case_state = FOUNDER_READY`

### Stage 16 — Founder Review

**Action:** Founder reviews the publication and makes final decision.

**Inputs:**
- Founder-ready publication
- Full research record (available for reference)

**Outputs:**
- `FOUNDER_ENDORSED` (Founder agrees with verdict)
- `FOUNDER_DISAGREES` (Founder disagrees — recorded as FD)
- `FOUNDER_REJECTS` (Founder rejects thesis entirely)
- `case_state = FOUNDER_DECIDED`

### Stage 17 — Thesis Monitoring

**Action:** Ongoing monitoring of thesis-specific indicators (detailed in M3-09/M3-10).

**Inputs:**
- Research verdict
- Thesis indicators defined during underwriting

**Outputs:**
- Monitoring updates
- Thesis state transitions: `RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN`
- `case_state = MONITORING`

### Stage 18 — Knowledge Compounding

**Action:** Cross-case learning (detailed in M3-10).

**Inputs:**
- Research findings from this and other cases

**Outputs:**
- Candidate Lesson → Cross-Case Validation → Independent Review → APPROVED KNOWLEDGE → Industry Playbook
- `case_state = CLOSED` (if research formally closed; monitoring may continue)

---

## 4. Stage State Lifecycle

```text
NOT_STARTED → IN_PROGRESS → COMPLETE → VERIFIED → (next stage)
                                    → FAILED → (escalation)
                                    → SKIPPED (documented reason)
```

- Each stage records: start timestamp, end timestamp, responsible role, outputs, issues, decisions
- Any stage may be restarted from its last checkpoint (previous stage outputs preserved)
- No stage may be skipped without a documented reason approved by Research Director

---

## 5. CIW Lineage

This protocol **evolves** the CIW (Company Intelligence Workbench) protocol (CAP-009 — ABSORB). The following CIW elements are preserved:

| CIW Element | QAD Protocol |
|-------------|--------------|
| CIW Result Contract | Preserved as Stage 14 output format |
| CIW Quality Gates | Preserved as stage quality gates (this document §5) |
| Claim/source lineage | Preserved in Canonical Evidence Registry (§Stage 7) |
| Deterministic calculations | Reused in Financial Reconstruction (§Stage 9, M3-08) |
| Point-in-time discipline | Preserved (Run Manifest, AS_OF_DATE) |
| Publication gates | Preserved as Stage 15–16 gates |
| 6 anti-anchoring views (CIW) | Evolved into separate analytical stages (8–11) |
| Cross-Exam (CIW) | Evolved into Structural Red Team (Stage 12) |
| CRO opposing thesis (CIW) | Preserved as companion publication pattern |
| Research audit (CIW) | Evolved into Independent Audit (Stage 13) |

What is NEW in QAD protocol (not in CIW):
- Competing Hypotheses H1–H5 mandate (Stage 2)
- Discovery & Selection as separate pre-research stage (M3-02)
- Elastic Investigator / Scuttlebutt protocol (M3-05)
- Impairment Diagnosis as first-class analysis (M3-07)
- Economic Underwriting with Permanent Loss Analysis (M3-08)
- Logical separation of Red Team vs Audit vs Underwriting (M3-09)
- Run Manifest (M3-01 §8)

<!-- 2026-08-19 12:00 UTC+7 -->