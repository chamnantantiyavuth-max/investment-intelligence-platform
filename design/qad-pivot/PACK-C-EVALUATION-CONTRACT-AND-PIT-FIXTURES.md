# Pack C — Evaluation Contract + PIT Fixtures

> **Status:** Design artifact — not approved. Pre-M5 Evaluation Contract.
> **M4B deliverable:** This contract defines how QAD is measured BEFORE any production code is written.
> Acceptance cases and PIT fixtures go here. Full M14 Evaluation Lab is a LATER expansion.

---

## Part 1: Evaluation Architecture

### Principle: Measure Before You Build

> No QAD discovery or analytical production code (M5+) may be considered implementation-ready until:
> 1. Evaluation Contract exists and passes review
> 2. Minimum 5 PIT historical fixtures exist (covering 5 of 10 required case types)
> 3. Baseline metrics are established
> 4. Cost/runaway controls are designed

### Evaluation Layers

```
Layer 1: Source & Citation     → Did we find the right evidence?
Layer 2: Claim Support         → Are our claims supported?
Layer 3: Calculation           → Can we reproduce numbers?
Layer 4: Classification        → Is Temporary/Structural calibration correct?
Layer 5: Thesis Detection      → Did we find thesis-killers?
Layer 6: Report Integrity      → Are reports factually accurate?
Layer 7: Decision-Changing Evidence → Did we miss material information?
```

---

## Part 2: Required PIT Historical Case Fixtures

### Minimum Fixture Set (M4B — pre-M5)

| # | Case Type | Example Company | Period | Key Feature |
|---|-----------|-----------------|--------|-------------|
| 1 | **True Temporary** | Any COVID-recovery name (e.g., airlines 2020) | Pre-COVID as-of, evaluate during trough | Recovery confirmed ex-post |
| 2 | **True Structural** | Blockbuster, Kodak | Before decline became obvious | Deterioration never reversed |
| 3 | **Mixed** | Intel 2021+ | Process node transition period | Partially recovered, partially structural |
| 4 | **False Quality** | Enron, Wirecard | Before fraud revealed | Quality appearance was fabricated |
| 5 | **Narrative Panic / Low Permanent Damage** | BP Deepwater Horizon 2010, Toyota 2010 recall | During event | Price damage > permanent economic damage |

### Expanded Fixture Set (M14 — Full Evaluation Lab)

| # | Case Type | Description |
|---|-----------|-------------|
| 6 | **Balance-Sheet Trap** | Good business, overleveraged, recovery requires refinancing |
| 7 | **Industry Cycle Deterioration** | Commodity/cyclical company at cycle trough |
| 8 | **Company-Specific Deterioration** | Single-company problem (product failure, lawsuit) |
| 9 | **Genuinely Unresolved** | Evidence insufficient to classify at as-of date |
| 10 | **Temporary + Unattractive Valuation** | Problem will pass but price still doesn't compensate |

### Fixture Format

Each fixture is a directory:

```
evaluation/historical-cases/{case-name}/
├── FIXTURE-MANIFEST.md          # case description, as-of date, known outcome
├── as-of-{YYYY-MM-DD}/
│   ├── sources/                  # only documents available before as-of date
│   │   ├── 10-K-2023.md
│   │   ├── Q-2024-Q1.md
│   │   └── ...
│   └── market-data/             # price, volume, ratios at as-of (not forward)
├── OUTCOME.md                   # what actually happened (sealed, for comparison post-evaluation)
└── ACCEPTANCE-CRITERIA.md       # what the QAD system should produce from this case
```

---

## Part 3: System-Level Metrics

### Source Recall

```
Metric:  % of decision-relevant public sources available at as-of date that 
          the system found and incorporated in evidence

Method:  Expert-constructed "should find" list for each fixture
Target:  >80% for S1–S3 sources
         >50% for S4 sources
         (S5–S6 not measured)
```

### Citation Correctness

```
Metric:  % of citations where the cited source actually supports the claim

Method:  Auditor verification on a random sample
Target:  >95%
```

### Claim Support

```
Metric:  % of material claims with at least one supporting S1–S3 source

Method:  Automated cross-check against Evidence Registry
Target:  100% for material claims
```

### Contradiction Coverage

```
Metric:  % of material claims where contradicting evidence is explicitly
          recorded when it exists at the as-of date

Method:  Expert comparison against known contradictions at as-of
Target:  >80%
```

### Calculation Reproducibility

```
Metric:  % of derived financial facts that can be re-derived from source
          inputs using the recorded formula

Method:  Automated re-derivation + comparison
Target:  100%
```

### Temporary vs Structural Calibration

```
Metric:  Agreement rate between system classification at as-of and
          ex-post outcome, measured at:
          - 1 year post-as-of
          - 3 years post-as-of
          - 5 years post-as-of

Method:  Compare IMPAIRMENT_DIAGNOSIS.classification vs OUTCOME.md
Target:  >70% at 3yr (TEMPORARY cases should still be temporary;
          STRUCTURAL should have become clearly broken)
```

### Thesis-Killer Detection

```
Metric:  % of predefined thesis-killer conditions that the system
          identified BEFORE the condition became obvious

Method:  Compare thesis_killers in underwriting vs OUTCOME.md
Target:  >60% of thesis-killers in the historical fixture are
          represented in the underwriting output
```

### False-Confidence Rate

```
Metric:  % of cases where system declared HIGH confidence but outcome
          contradicted the classification

Method:  Compare confidence fields vs outcomes
Target:  <20%
```

### Research-Stop Quality

```
Metric:  % of TERMINATED cases where the termination reason correlates
          with actual subsequent business outcomes

Method:  Compare Research Termination Memo vs outcomes
Target:  >80%
```

### Report Factual Error Rate

```
Metric:  Number of factual errors (wrong figures, mis-citations, 
          false claims) per 10,000 words in published reports

Method:  Audit random sample
Target:  <2 per 10,000 words
```

### Decision-Changing Evidence Recall (DCE Recall)

```
Metric:  Was there material evidence available at the as-of date that 
          should have changed the thesis, but the system failed to find 
          or incorporate it?

Method:  For each historical fixture, an independent expert reviews the
          system's evidence set vs all publicly available S1–S3 sources 
          at as-of. Any source that:
          (a) was publicly available at as-of date,
          (b) contained a material claim that would change the thesis,
          (c) was NOT in the system's evidence set
          → DCE Miss. Count = misses per case.

Target:  ≤1 DCE Miss per Full Research case (S1–S3 sources only)
```

---

## Part 4: Cost & Budget Control Design (QAD §37)

### Configurable Limits

```
Maximum concurrent Full Research cases:      3 (default)
Maximum concurrent Scuttlebutt cases:         2 (default)
Maximum Deep Research calls per case:         10 (soft), 15 (hard)
Maximum tokens per Research Run (total):      2,000,000 (soft), 3,000,000 (hard)
Maximum tokens per individual Deep Research:  500,000
Maximum retries per stage:                    3
Maximum total cost per Full Research case:    $50 (soft), $100 (hard)
```

### Budget Exhaustion Behavior

| Level | Action |
|-------|--------|
| Soft budget hit | Warning to Chief Underwriter. Proceed on discretion. |
| Hard budget hit | Mark `BUDGET_EXHAUSTED → INCOMPLETE`. Pause research. |
| Never publish as Founder-Ready | If budget exhausted before underwriting, case must enter `BUDGET_EXHAUSTED` state. |
| Budget can be overridden | Only by explicit Chief Underwriter decision with rationale. |

### Research Saturation (QAD §38)

```
Before every expensive investigation (Tier C/D call, NotebookLM Deep Research),
check:

  "Is the unresolved question decision-relevant?"
  "Is new evidence likely to change the material conclusion?"

If expected information value is LOW → skip. Log the gap.
```

---

## Part 5: Acceptance Cases

### Acceptance Criteria per Stage

| Stage | Acceptance Criteria |
|-------|---------------------|
| **Quality Discovery** | System identifies candidate. Hard Gates evaluated. Candidate outcome (AUTO_RESEARCH_NOW / WATCH / REJECT) recorded with rationale. |
| **Research Charter** | Charter contains: research objective, market fears, competing hypotheses, primary questions, decision-critical unknowns, initial source map. |
| **Evidence Building** | All S1–S3 sources for case identified and retrieved. Evidence entries created with proper PIT metadata. |
| **Analysis** | Business Quality Assessment complete with Moat Mechanism Protocol. Financial Reconstruction 7–10yr. Management/Capital Allocation Ledgers built. |
| **Impairment** | Dislocation reconstruction with timeline. Causal chain tests applied. Classification (TEMP/MOSTLY/MIXED/STRUCT/UNRES) with evidence. Recovery mechanism defined (if TEMP). |
| **Valuation** | Multiple scenarios. Reverse DCF complete. Market-implied vs evidence-supported economics compared. |
| **Red Team** | Operationally independent. Every thesis component challenged. Adjudication recorded. |
| **Audit** | Source exists check. Calculation reproducibility. PIT verified. No self-review. |
| **Underwriting** | Single coherent narrative. Verdict clear. Thesis killers defined. |
| **Publication** | Thai language. FACTS LOCKED verified. Jargon sweep clean. Visual QA pass. |

---

## Part 6: Evaluation Run Protocol

```
1. Select fixture
2. Freeze system state: git HEAD, config, model routing
3. Record: as_of_date, model versions, routing config, token/cost metrics
4. Run QAD workflow from Discovery through Underwriting
5. DO NOT reveal OUTCOME.md to any role during evaluation
6. Collect system output: all artifacts, confidence, thesis killers
7. Compare system output vs ACCEPTANCE-CRITERIA.md
8. Score metrics
9. THEN open OUTCOME.md for comparison
10. DCE Recall: independent expert reviews evidence set vs all public sources as-of
11. Record findings
```

### Prohibited in Evaluation

- Revealing OUTCOME.md to any evaluation role before scoring complete
- Using any source published after the as_of_date
- Adjusting thresholds mid-evaluation
- Running evaluation on a case that was already in the training set
- Look-ahead leakage through any channel (model training cutoff is NOT a guarantee — source freeze is mandatory)

<!-- 2026-08-16 UTC+7 -->