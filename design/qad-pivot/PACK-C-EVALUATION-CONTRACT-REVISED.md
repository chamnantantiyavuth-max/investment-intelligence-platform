# Pack C — Evaluation Contract & PIT Fixtures (Revised)

> **Status:** Resolution round — corrected for Pre-Code Design Gate.
> **Key changes from v1:**
> - 3 evaluation layers: Named (workflow only) + Entity-Masked + Synthetic/Counterfactual
> - Pre-M5 fixtures expanded from 5 → 10 minimum
> - Outcomes physically sealed (separate directory, no agent access)
> - No κ threshold for initial corpus
> - Fixture selection must isolate subsystem being tested
> - Famous-case leakage explicitly classified
> - Budget control design aligned with Research Budget Controller policy

---

## Part 1: Evaluation Architecture — 3 Layers

### Layer A — Named Historical Cases

| Property | Value |
|----------|-------|
| **Purpose** | Source retrieval, provenance, workflow, calculation, citation, report-generation testing |
| **Companies** | Real names, real history |
| **Limitation** | NOT clean predictive tests for impairment reasoning (outcomes may be memorized by models) |
| **Suitable for** | Workflow orchestration, evidence sourcing, financial calculation, report format, audit chain |
| **Example** | Kodak, Intel, BP 2010 |

### Layer B — Entity-Masked Historical Cases

| Property | Value |
|----------|-------|
| **Purpose** | Reduce memorized-outcome leakage while preserving realistic business dynamics |
| **Method** | Replace/neutralize company name, product names, ticker, recognizable brand identifiers. Preserve economics, industry context, financial statements, competitive structure. |
| **Constraint** | Only information available at historical as-of date is included. No post-as-of data. |
| **Suitable for** | Impairment diagnosis, valuation, Red Team challenge testing |

### Layer C — Synthetic / Counterfactual Cases

| Property | Value |
|----------|-------|
| **Purpose** | Cleanest test of causal impairment reasoning |
| **Method** | Construct controlled business economics from real patterns but with perturbed variables. Assign known causal truth (this IS temporary, this IS structural). |
| **Variables** | Revenue, margin, debt, market share, industry, customer evidence, competitive dynamics |
| **Suitable for** | Temporary-vs-Structural calibration, thesis-killer detection, false-confidence measurement |
| **Constraint** | No company matches exactly. Causal truth predetermined by constructor. |

### Evaluation Rule per Layer

| Layer | Can measure | Cannot cleanly measure |
|-------|-------------|------------------------|
| A — Named | Source recall, citation correctness, calculation reproduction, workflow completeness, report quality | Predictive impairment calibration, Temporary-vs-Structural reasoning |
| B — Masked | Impairment diagnosis (reduced leakage), valuation, evidence mapping | Source recall (names removed) |
| C — Synthetic | Causal impairment reasoning, classification calibration, thesis-killer detection | Source retrieval, real-world citation |

---

## Part 2: Pre-M5 Fixture Set (Minimum 10)

### Required Case Types

| # | Type | Layer(s) | Subsystem Isolated | Example |
|---|------|----------|-------------------|---------|
| 1 | **Temporary (Quality pre-validated)** | B or C | Impairment Engine | Industry cycle trough for durable business |
| 2 | **Temporary (Quality pre-validated)** | B or C | Impairment Engine | Company-specific event for high-quality business |
| 3 | **Structural (Clear quality)** | B or C | Impairment Engine | Technological disruption of durable business |
| 4 | **Structural (Clear quality)** | A | Workflow + Source | Named workflow test for structural case |
| 5 | **Mixed** | B or C | Impairment + Valuation | Partial recovery, partial structural |
| 6 | **Mixed** | A | Workflow + Calculation | Named workflow for mixed case |
| 7 | **False Quality** | C | Quality Verification | Business that appeared high quality but wasn't (synthetic — cycle/leverage/accounting-driven returns) |
| 8 | **Balance Sheet Trap** | B or C | Survival + Valuation | Durable business, overleveraged, recovery requires refinancing |
| 9 | **Genuinely Unresolved** | C | Impairment Engine | Evidence insufficient to classify at as-of date |
| 10 | **Temporary + Unattractive Valuation** | B or C | Valuation | Problem will pass but price doesn't compensate |

### Fixture Selection Rules

- Each fixture must explicitly state: **"This fixture isolates: [subsystem(s)]"**
- Example: "This fixture isolates the Impairment Engine — Quality is pre-validated. The task is to classify the deterioration correctly."
- Do NOT test every subsystem simultaneously in every case
- Famous outcome cases (Kodak, Blockbuster) are Layer-A workflow fixtures only — NOT core calibration fixtures
- At least 5 of 10 pre-M5 fixtures should be Layer B or C (not susceptible to outcome memorization)

---

## Part 3: Sealed Outcomes

### Directory Structure

```
evaluation/
    input-fixtures/
        case-001-temporary-quality/
            FIXTURE-MANIFEST.md
            as-of-YYYY-MM-DD/
                sources/
                market-data/
            ACCEPTANCE-CRITERIA.md

evaluation-sealed/         ← SEPARATE directory, agent has NO access
    outcomes/
        case-001-temporary-quality/
            OUTCOME.md         ← sealed
            ACTUAL-EVIDENCE-FOUND.md  ← known-ground-truth sources at as-of
```

### Enforcement

| Layer | Sealing method |
|-------|----------------|
| **Directory permission** | `evaluation-sealed/` has OS-level ACL denying read to execution agent. Only Evaluation Harness can access. |
| **Harness boundary** | Evaluation Harness reads output AFTER run completes, compares to sealed outcome, reports metrics. Harness NEVER reveals outcome to evaluation agent. |
| **Fallback** | If permission sealing is technically infeasible (subagent, container), the harness MUST delete outcome files from the execution context before agent starts. |
| **Test** | Automated test: "evaluation_agent_cannot_read_sealed_outcomes" — verify read permission denied |

---

## Part 4: System-Level Metrics (Revised)

| Metric | Method | Target | Notes |
|--------|--------|--------|-------|
| Source Recall | Expert-constructed "should find" list for each fixture | >80% S1–S3, >50% S4 | Layer A only (names intact) |
| Citation Correctness | Auditor verification on sample | >95% | All layers |
| Claim Support | Automated cross-check | 100% material claims | All layers |
| Contradiction Coverage | Expert comparison | >80% | All layers |
| Calculation Reproducibility | Automated re-derivation | 100% | All layers |
| Temp-vs-Structural Calibration | Compare vs sealed outcome | >70% at 3yr | Layers B+C only (Layer A excluded for famous cases) |
| Thesis-Killer Detection | Compare vs outcome | >60% | Layers B+C |
| False-Confidence Rate | Compare confidence vs outcome | <20% | All layers |
| Research-Stop Quality | Compare termination vs outcome | >80% | All layers |
| Report Factual Error Rate | Audit sample | <2 per 10K words | All layers |
| Decision-Changing Evidence Recall | Independent expert review | ≤1 DCE Miss per case | Layers A+B (S1–S3 sources) |

### Inter-Rater Reliability (Initial Corpus)

```
For the initial 10-fixture corpus:
  - Two independent reviewers (Reviewer A, Reviewer B)
  - Record agreement/disagreement per metric
  - Preserve disagreements — do not average
  - Adjudicate only where required for metric computation
  - Track simple agreement rate (NOT Cohen's κ)
  
κ threshold is DEFERRED until:
  - Evaluation corpus expands to ≥30–50 appropriate cases
  - Label taxonomy is stable
  - Sufficient data exists for statistically meaningful κ
  - M14 Full Evaluation Lab may introduce κ/Krippendorff's α where suitable
```

---

## Part 5: Famous-Case Leakage Classification

| Case | Layer | Use | Impairment Calibration? |
|------|-------|-----|-------------------------|
| Kodak | A (Named) | Workflow, source retrieval, calculation | NO — model knows outcome |
| Blockbuster | A (Named) | Workflow, citation, report format | NO |
| Intel 2021+ | B (Masked, Entity-neutralized) | Impairment (reduced leakage) | CONDITIONAL — mask well |
| BP 2010 | A or B | Narrative Panic template | A: NO (workflow only). B: CONDITIONAL |
| COVID airlines | B (Masked) | Temporary | CONDITIONAL — mask industry + company |
| Synthetic | C (Synthetic) | Impairment, Quality, Valuation | YES — causal truth known |

---

## Part 5a: Mask Recognizability Check (NEW)

For Layer-B (entity-masked) fixtures, a leakage check is required before benchmark admission.

### Process

1. An independent evaluator (NOT the fixture constructor) receives the masked fixture
2. The evaluator attempts to identify the original company/entity
3. Outcome:
   - **Identity not recoverable** → mask passes. Fixture eligible for clean impairment calibration.
   - **Identity partially guessed** → review masking quality. Consider re-masking.
   - **Identity readily recovered** → classify as leakage-risk. Either re-mask with stronger obfuscation or exclude from clean reasoning calibration (use only as Layer-A workflow fixture).

### Rule

> If an independent evaluator can readily recover the entity identity from the masked fixture alone, that fixture MUST NOT be used as a clean test of causal impairment reasoning.

---

## Part 6: Budget Control Design (Revised)

```
Base Budget per case
    │
    ▼
Soft limit (80% of base)
    │
    ▼
Research Director: expected-information-value justification
    │
    ▼
Hard limit (100% of base)
    │
    ▼
Escalation request (Research Director → Chief Underwriter)
    │
    ▼
Exceptional extension (Chief Underwriter request → policy approval / Founder threshold)
    │
    ▼
Override LOGGED (reason, approver, amount, timestamp)
    │
    ▼
Auditor verifies post-hoc: was override properly authorized and logged?
```

Budget Controller is a policy/service — NOT an agent. No model dependency. Simple deterministic limits with escalation.

---

## Part 7: Discovery & Coverage Evaluation (M1 requirement — per QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 Part E)

### Two-Axis Evaluation

The system must be evaluated on two separate questions:
1. **Type A (Research Quality):** when the system finds a company, does it research it correctly? (covered by existing Parts 1–6)
2. **Type B (Discovery Recall):** did the system discover the company/opportunity at all? (NEW — this Part)

### Metrics

| Metric | Method | Target | Notes |
|--------|--------|--------|-------|
| Universe Coverage Rate | Eligible count vs actually scanned | BASELINE_REQUIRED | All registries; threshold PENDING_M4B_CALIBRATION |
| Data-Ready Coverage | Companies with sufficient data ≥ usable threshold | BASELINE_REQUIRED | Researchable Universe; threshold PENDING_M4B_CALIBRATION |
| Known-Opportunity Recall | Historical QAD-appropriate opportunities detected | BASELINE_REQUIRED | Masked/historical fixtures; threshold PENDING_M4B_CALIBRATION |
| Quality Candidate Recall | Companies with quality evidence correctly identified | BASELINE_REQUIRED | Quality Universe; threshold PENDING_M4B_CALIBRATION |
| Dislocation Recall | Material dislocations detected | BASELINE_REQUIRED | Cross-sectional; threshold PENDING_M4B_CALIBRATION |
| False-Negative / Miss Rate | Stratified rejected-sample audit | BASELINE_REQUIRED | Rejected-Sample Audit; threshold PENDING_M4B_CALIBRATION |
| Rejected-Item Surprise Rate | Independent review of rejected/low-rank sample | BASELINE_REQUIRED | Monthly; threshold PENDING_M4B_CALIBRATION |
| Time-to-Detection | Cadence between event first observable and signal registered | BASELINE_REQUIRED | Per cadence; threshold PENDING_M4B_CALIBRATION |
| Signal→Candidate Precision | Signals that pass candidate assembly | BASELINE_REQUIRED | Signal Registry; threshold PENDING_M4B_CALIBRATION |
| Candidate→Research Yield | Candidates that open Full Research | BASELINE_REQUIRED | Candidate Registry; threshold PENDING_M4B_CALIBRATION |
| Cost per meaningful candidate | Total discovery cost / meaningful candidates | BASELINE_REQUIRED | Budget Controller; threshold PENDING_M4B_CALIBRATION |
| Source/feed failure detection | Unplanned data stall or feed drop | alert ≤1 cycle | Operations |
| Decision-Changing Candidate Recall | "Did the system ever see the company that later became a real QAD opportunity — before it was obvious?" | BASELINE_REQUIRED | **Headline metric**; threshold PENDING_M4B_CALIBRATION |

### Hard Invariants (zero-tolerance, do not require calibration)

The following are hard invariants with no PENDING_M4B_CALIBRATION label — they are production acceptance requirements:

- **No silent omission:** every company in the Researchable Universe must have explicit inclusion/exclusion state and reason recorded in the registry.
- **Sealed-outcome isolation:** evaluation outcomes must remain inaccessible to the agent being evaluated (per Part 3 enforcement).
- **PIT violation = fail:** any point-in-time violation (look-ahead data, post-as-of information) in a fixture evaluation is an automatic failure.
- **Provenance integrity:** every candidate, signal, and case transition must record who, when, why, data version, rule version, model version, and evidence — missing or fabricated provenance = fail.

### Method

- Historical/masked/synthetic discovery fixtures (Layer A/B/C patterns, extended for discovery)
- Monthly rejected-sample audit (stratified random sample of 50–100 from rejected/low-rank; independent light review)
- Discovery recall and rejected-item audit results feed the M5 Gate Evidence Package
- Separate evaluation of type-A (research quality) and type-B (discovery recall) — never conflate
- **Calibration discipline (M4B):** `Metric → Baseline Measurement → Error Analysis → Threshold Proposal → Founder Approval → Production Acceptance Threshold`. No numeric acceptance target is adopted before an empirical baseline and error/trade-off analysis exists. Hard invariants above are exempt from calibration.
<!-- 2026-08-16 UTC+7 -->
<!-- 2026-08-17 17:30 UTC+7 -->