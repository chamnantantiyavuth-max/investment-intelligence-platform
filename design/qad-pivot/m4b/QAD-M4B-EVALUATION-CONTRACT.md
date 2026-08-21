# QAD-M4B Evaluation Contract

> **Status:** M4B FINAL / FROZEN — FOUNDER ACCEPTED
> **Authority:** FD #133, FD #134; M3 Frozen Domain Contracts; M3-09 §8 (Evaluation)
> **Execution rule:** M4B begins only after M4A Freeze Gate passes.
> **Design principle:** Two separate evaluation questions — Type A (research quality) and Type B (discovery recall).

---

## 1. Evaluation Typology

```text
TYPE A FAILURE
Company discovered → research wrong
Evaluates: research quality, analytical correctness, process compliance

TYPE B FAILURE
Material company never discovered
Evaluates: discovery recall, universe coverage, signal detection
```

These two types are evaluated separately with different PIT snapshots, different fixtures, and different metrics. A single evaluation score must never combine Type A and Type B.

---

## 2. Point-in-Time Sealed Evaluation Protocol

### 2.1 Sealed Corpus

Every evaluation uses a sealed historical corpus with:

```text
fixture_id
company/security identity
AS_OF_DATE (hard cutoff — no evidence after this date)
evidence allowed (pre-AS_OF only)
evidence forbidden (post-AS_OF — HARD BLOCKED)
expected material hypotheses
known outcome window (for calibration)
fixture type
evaluation labels
ambiguity notes
```

### 2.2 PIT Enforcement

Per M3-SERVICES S7 (PIT Lock):

```text
SEALED_HISTORICAL_EVALUATION mode
    → post-AS_OF evidence HARD BLOCKED
    → any query returning post-AS_OF data returns error
    → no future-information leakage
```

### 2.3 Evaluation Execution

```text
1. Load sealed corpus
2. Set PIT context to SEALED mode with AS_OF_DATE
3. Execute evaluation (Type A or Type B)
4. Collect metrics
5. Verify no post-AS_OF evidence was accessed
6. Generate evaluation report
```

### 2.4 Leakage Test

Every evaluation run MUST include a leakage test:

```text
1. Insert a known post-AS_OF fact into the query path
2. Verify the PIT lock blocks it
3. If it passes → evaluation data is contaminated
4. If it blocks → evaluation is clean
```

---

## 3. PIT Fixture Specifications

### 3.1 Fixture Types (10 minimum)

| # | Fixture Type | Description | AS_OF Example |
|---|-------------|-------------|---------------|
| 1 | **True Temporary Impairment** | Genuine high-quality business with temporary headwind; recovered within 2-4 years | Financial crisis 2008-09, COVID 2020 |
| 2 | **True Structural Deterioration** | Business model permanently damaged; never recovered | Retail/classifieds disrupted by digital |
| 3 | **Mixed Impairment** | Genuine quality loss in some areas, intact in others | Partial disruption |
| 4 | **False Quality** | Appeared high-quality but was not; moat was illusion | Accounting fraud, cyclical peak mistaken for quality |
| 5 | **Balance-Sheet Trap** | High quality but leverage/refinancing risk causes permanent loss | Over-leveraged cyclical |
| 6 | **Industry/Cycle Shock** | Industry-wide dislocation; company-specific vs industry effect | Commodity price crash, industry regulation |
| 7 | **Company-Specific Shock** | Company-specific event (product failure, lawsuit, management) | Product recall, CEO scandal |
| 8 | **Unresolved / Ambiguous Case** | Genuinely ambiguous; evidence supports both sides | Complex disruption |
| 9 | **Valuation Failure** | Price implies permanent damage but evidence supports temporary; market was wrong | Narrative panic |
| 10 | **Narrative Panic** | Price damage far exceeds economic damage; market overreaction | Panic selling, forced liquidation |

### 3.2 Fixture Schema

```text
fixture_id: FIX-YYYY-NNN
fixture_version: MAJOR.MINOR.PATCH (semantic version — increments on content change)
supersedes_fixture_version: [none | version string] (prior version this corrects, if any)
correction_reason: [string] (what was corrected and why)
adjudicator: [identity string] (who independently verified this fixture)
corpus_hash: [SHA-256 hex] (hash of the complete allowed-source manifest)
label_hash: [SHA-256 hex] (hash of all expected labels + rationale)
seal_hash: [SHA-256 hex] (hash of the entire sealed fixture document)
company: ticker, name, entity_id
as_of_date: YYYY-MM-DD (hard cutoff)
evidence_context:
  pre_as_of: [source_ids, evidence_ids] (allowed)
  post_as_of: [source_ids] (FORBIDDEN — leak test target)
expected_hypotheses:
  H1: statement, expected_plausibility
  H2: statement, expected_plausibility
  H3: statement, expected_plausibility
  H4: statement, expected_plausibility
  H5: statement, expected_plausibility
expected_quality_state: VERIFIED / PROBABLE / UNRESOLVED / FAILED
expected_impairment: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED
expected_verdict: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED /
                  NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION
known_outcome_window: [start_date, end_date]
fixture_type: TEMPORARY / STRUCTURAL / MIXED / FALSE_QUALITY / BALANCE_SHEET /
              INDUSTRY_SHOCK / COMPANY_SHOCK / AMBIGUOUS / VALUATION_FAILURE / NARRATIVE_PANIC
ambiguity_notes: [notes about edge cases, alternative interpretations]
```

### 3.3 Fixture Lifecycle

```text
DRAFT_UNSEALED → SOURCE_PACK_COMPLETE → INDEPENDENTLY_ADJUDICATED → SEALED → ACTIVE_EVALUATION → ARCHIVED
                                                                                 ↓
                                                                          SEALED → SUPERSEDED
                                                                          (correction path — never edit in place;
                                                                           superseding creates a new fixture version)
```

**State Descriptions**

| State | Meaning |
|-------|---------|
| DRAFT_UNSEALED | Fixture is a proposal, not yet assembled into a verifiable source pack. Labels are provisional and NOT scoring ground truth. |
| SOURCE_PACK_COMPLETE | All pre-AS_OF sources collected, hashed, and indexed; leak sentinels identified; source pack ready for review. |
| INDEPENDENTLY_ADJUDICATED | An independent adjudicator has reviewed the source pack and labels and confirmed the fixture meets the seal contract (§3.4). |
| SEALED | Fixture is immutable and may be used as scoring ground truth in evaluations. |
| ACTIVE_EVALUATION | Fixture is currently in use for live evaluations. |
| ARCHIVED | Fixture has been retired from active use but remains readable for audit. |
| SUPERSEDED | A newer version of this fixture has been sealed to correct errors. The older version is preserved and readable but no longer authoritative. |

### 3.4 Seal Contract

A fixture may enter the SEALED state only when ALL of the following are present and immutable:

```text
fixture_id                              — unique identifier
fixture_version                         — semantic version (MAJOR.MINOR.PATCH)
AS_OF_DATE                              — hard cutoff; no evidence after this date
immutable source IDs                    — each pre-AS_OF source has a unique, stable identifier
source content hashes                   — SHA-256 hash of each source's full content
source publication dates                — publication date for every source, verified ≤ AS_OF_DATE
allowed pre-AS_OF corpus manifest       — complete list of every evidence item admitted into the fixture
forbidden post-AS_OF leak sentinels     — known post-AS_OF facts that MUST be blocked (leak test targets)
expected quality/impairment/verdict labels — the scored ground-truth values for each dimension
label rationale                         — written justification for each expected label
material alternative interpretation     — the strongest competing interpretation and why it was not selected
ambiguity notes                         — any edge cases, limitations, or unresolved questions
adjudicator identity                    — who performed the independent adjudication
adjudication method                     — how the adjudication was conducted (e.g., desk review, panel vote)
adjudication timestamp                  — when the adjudication was completed
corpus_hash                             — SHA-256 of the complete allowed-source manifest
label_hash                              — SHA-256 of all expected labels + rationales
seal_hash                               — SHA-256 of the entire sealed fixture document
```

A fixture that meets all seal-contract requirements may be promoted from INDEPENDENTLY_ADJUDICATED to SEALED by the project lead or governance gate. Once SEALED, the fixture is immutable for evaluation purposes. Corrections require creating a new fixture version and superseding the old one — the original seal hash is preserved for audit.

---

## 4. Evaluation Dimensions

### 4.1 Evidence Quality (Type A)

| Metric | Definition | Measurement |
|--------|------------|-------------|
| Source Recall | % of material sources discovered | Manual baseline vs system output |
| Citation Correctness | % of citations pointing to correct source | Audit sampling |
| Claim Support | % of claims with supporting evidence | Automated check |
| Original-Source Validation | % of AI-sourced evidence validated against original | Audit trail |
| Contradiction Coverage | % of material contradictions identified | Manual baseline |
| Decision-Changing Evidence Recall | % of evidence that changes verdict that was captured | Outcome analysis |

### 4.2 Analytical Quality (Type A)

| Metric | Definition | Measurement |
|--------|------------|-------------|
| H1–H5 Coverage | % of required hypotheses explicitly addressed | Automated check |
| Quality Verification Correctness | % correct quality state assignment | Against sealed labels |
| False-Quality Detection | % of false-quality cases correctly identified | Against sealed labels |
| Temporary-vs-Structural Calibration | Accuracy of impairment diagnosis | Against known outcomes |
| Recovery Mechanism Quality | % of cases with specific (not circular) recovery mechanism | Review |
| Thesis-Killer Detection | % of thesis killers identified | Against manual baseline |
| False-Confidence Rate | % of confident verdicts that were wrong | Against outcomes |

### 4.3 Financial Quality (Type A)

| Metric | Definition | Measurement |
|--------|------------|-------------|
| Calculation Reproducibility | % of calculations reproducible | Independent recalculation |
| Normalization Correctness | % of adjustments correctly identified | Against manual baseline |
| Permanent-Loss Coverage | % of cases with permanent loss analysis | Automated check |
| Reverse-DCF Correctness | % of reverse DCF calculations correct | Against independent model |
| Scenario Consistency | % of scenarios with consistent assumptions | Cross-check |

### 4.4 Process Quality (Type A)

| Metric | Definition | Measurement |
|--------|------------|-------------|
| PIT Correctness | % of evidence within AS_OF_DATE bounds | Automated PIT check |
| Provenance Completeness | % of evidence with full provenance | Automated check |
| Failure-State Correctness | % of failure states correctly recorded | Audit |
| Research-Stop Quality | % of stop decisions with documented reason | Audit |
| Audit-Gate Correctness | % of audit gates correctly passed | Audit |
| Report Factual-Error Rate | Errors per published report | Post-publication audit |

### 4.5 Discovery Quality (Type B)

| Metric | Definition | Measurement |
|--------|------------|-------------|
| Universe Coverage Rate | % of eligible companies scanned | Automated |
| Data-Ready Coverage | % of companies with sufficient data | Automated |
| Known-Opportunity Recall | % of known material opportunities discovered | Against sealed list |
| Quality Candidate Recall | % of quality companies correctly identified | Against sealed list |
| Dislocation Detection Rate | % of material dislocations detected | Against sealed list |
| Signal-to-Candidate Conversion | % of signals that became candidates | Automated |
| Candidate-to-Research Conversion | % of candidates that became research cases | Automated |
| Discovery Cost per New Candidate | Cost per candidate discovered | Cost tracking |
| False Positive Rate (Material) | % of candidates that wasted material research | Review |
| **Decision-Changing Candidate Recall** | **Headline: % of candidates that changed portfolio-relevant decisions** | **Outcome analysis** |

---

## 5. Radar Scout Incremental-Recall Evaluation

### 5.1 Purpose

Determine whether the legacy Radar Scout (CAP-011 — TRANSITIONAL) provides incremental discovery value beyond QAD automated discovery.

### 5.2 Design

```text
QAD Discovery without Radar
    vs
QAD Discovery + Radar
```

### 5.3 Protocol

1. Run QAD automated discovery (Lanes A + B) on historical period
2. Run Radar (Lane C) on same historical period
3. Compare signal sets:
   - Signals found by both
   - Signals found ONLY by QAD automated
   - Signals found ONLY by Radar
4. Evaluate: Are Radar-only signals material?
   - Would they have changed candidate/research decisions?
   - What is the incremental cost per Radar-only signal?
5. Report:
   - Incremental recall rate
   - Incremental false positive rate
   - Cost per incremental signal
   - Recommendation: RETAIN / ABSORB / RETIRE

### 5.4 Rule

> Radar raises questions; it never answers them.

Do NOT retire Radar in M4B. Retirement/absorption requires later evidence and Founder decision.

---

## 6. Research Saturation / Expected Information Value

### 6.1 Saturation Measurement

Evaluate whether research stops at an appropriate point:

```text
Does another unit of research have a reasonable probability
of changing the decision?
```

### 6.2 Metrics

| Metric | Definition |
|--------|------------|
| Research Depth vs Decision Impact | Source count vs verdict change frequency |
| Premature Stopping Rate | % of cases where additional evidence would have changed verdict |
| Excess Research Rate | % of cases where evidence saturation was exceeded |
| EIV Threshold Accuracy | % of cases where stop decision matched EIV estimate |

### 6.3 Rule

Do not use "number of sources" as a completeness proxy.

---

## 7. Model / Cost Routing Evaluation

### 7.1 Tier Model

```text
Tier A — Bulk / cheap / free where reversible
Tier B — Operational
Tier C — Decision-critical
Tier D — Independent frontier challenge
```

### 7.2 Authority Restriction

Cheap/free models may NOT be sole authority for:

- Quality assessment
- Moat classification
- Impairment diagnosis
- Normalized earnings
- Permanent loss
- Valuation asymmetry
- Final underwriting
- Final Red Team adjudication

### 7.3 Cost Metrics

| Metric | Definition |
|--------|------------|
| Cost per completed case | Total cost / completed cases |
| Tokens per stage | Token consumption by research stage |
| Expensive-model escalation rate | % of cases requiring Tier C/D |
| Retry cost | Cost of failed/retried operations |
| Deep Research cost | NotebookLM/Deep Research spend |
| Decision-changing evidence per research cost | Evidence quality / cost ratio |

---

## 8. Threshold Policy

### 8.1 Rule

M4B may **measure and empirically propose** acceptance/calibration thresholds.

M4B must NOT silently constitutionalize thresholds.

### 8.2 Threshold Format

Any material threshold proposed for M5 must be labeled:

```text
PROVISIONAL_M4B_THRESHOLD
```

with:

```text
empirical_basis: [data source, sample size]
sample_size: N
uncertainty: [confidence interval]
sensitivity: [impact of ±X% variation]
failure_consequences: [what happens if threshold is wrong]
```

### 8.3 Ratification

Material thresholds require Founder ratification before becoming a production gate.

---

## 9. M4B Required Deliverables

| Artifact | File | Status |
|----------|------|--------|
| Evaluation Contract | This file | ✅ DRAFT |
| PIT Fixture Spec | `QAD-M4B-PIT-FIXTURE-SPEC.md` | ⏳ |
| Acceptance Matrix | `QAD-M4B-ACCEPTANCE-MATRIX.md` | ⏳ |
| Discovery Recall Evaluation | `QAD-M4B-DISCOVERY-RECALL-EVAL.md` | ⏳ |
| Calibration Report | `QAD-M4B-CALIBRATION-REPORT.md` | ⏳ |
| Cost / Model Evaluation | `QAD-M4B-COST-AND-MODEL-EVAL.md` | ⏳ |
| Validator | `validate-m4b-pack.py` | ⏳ |
| Closeout | `QAD-M4B-CLOSEOUT.md` | ⏳ |

Non-production evaluation scripts/fixtures are permitted. No live production system.

<!-- 2026-08-19 16:30 UTC+7 -->