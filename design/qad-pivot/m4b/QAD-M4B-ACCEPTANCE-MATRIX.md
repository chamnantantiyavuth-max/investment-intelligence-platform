# QAD-M4B Acceptance Matrix

> **Status:** DRAFT (AWAITING M4A FREEZE GATE)
> **Authority:** FD #133; M4B Evaluation Contract §4
> **Design Principle:** Two separate evaluation questions — Type A (research quality) and Type B (discovery recall)
> **Threshold Rule:** All material thresholds marked PROVISIONAL_M4B_THRESHOLD pending empirical calibration and Founder ratification per §8

---

## 1. Evidence Quality (Type A)

Tests whether the system discovers and correctly uses material evidence.

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 1.1 | **Source Recall** | % of material pre-AS_OF sources discovered by the system vs a manually compiled baseline | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types (baseline per fixture: manually curated evidence packages) | Manual baseline per fixture: curator compiles complete source list; system output compared for recall | A |
| 1.2 | **Citation Correctness** | % of citations in the system's research output that correctly reference the cited source, page, or paragraph | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (TEMPORARY), FIX-004 (FALSE_QUALITY), FIX-007 (COMPANY_SHOCK), FIX-009 (VALUATION_FAILURE) | Audit sampling: PROVISIONAL_M4B_THRESHOLD (empirical_basis = NOT_YET_CALIBRATED, sample_size = N/A, uncertainty = UNRESOLVED, Founder_ratification_required = true) of system citations per fixture traced back to original source and verified | A |
| 1.3 | **Claim Support** | % of factual claims in the research output that have an accompanying supporting evidence citation | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types | Automated check: parse claims from output, verify each has at least one cited evidence source | A |
| 1.4 | **Original-Source Validation** | % of AI-sourced or system-generated evidence that is validated against the original (non-processed) source document | `PROVISIONAL_M4B_THRESHOLD` | FIX-004 (FALSE_QUALITY), FIX-008 (AMBIGUOUS), FIX-009 (VALUATION_FAILURE) | Audit trail: compare system evidence excerpts against original source text for fidelity; PROVISIONAL_M4B_THRESHOLD (empirical_basis = NOT_YET_CALIBRATED, sample_size = N/A, uncertainty = UNRESOLVED, Founder_ratification_required = true) of AI-sourced evidence sampled | A |
| 1.5 | **Contradiction Coverage** | % of material contradictions present in the evidence base that were identified by the system in its output | `PROVISIONAL_M4B_THRESHOLD` | FIX-003 (MIXED), FIX-004 (FALSE_QUALITY), FIX-008 (AMBIGUOUS), FIX-010 (NARRATIVE_PANIC) | Manual baseline: curator pre-identifies key contradictions in evidence base; system output checked against these | A |
| 1.6 | **Decision-Changing Evidence Recall** | % of evidence items that would change the verdict that were actually captured by the system | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types (weighted: high-evidence fixtures FIX-002, FIX-004, FIX-008 carry higher weight) | Outcome analysis: curator designs "verdict-altering" evidence items per fixture; system is evaluated on whether these are in the research output | A |

---

## 2. Analytical Quality (Type A)

Tests the correctness and calibration of the system's analytical conclusions.

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 2.1 | **H1–H5 Coverage** | % of the 5 required hypotheses per fixture that the system explicitly addresses in its research output | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types (minimum 5 forced hypotheses per fixture per §3.2 schema) | Automated check: parse system output for each H1–H5 statement; verify explicit addressal (not implicit) | A |
| 2.2 | **Quality Verification Correctness** | % of fixtures where the system's quality state assignment matches the sealed label | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (VERIFIED), FIX-002 (FAILED), FIX-003 (PROBABLE), FIX-004 (FAILED), FIX-005 (VERIFIED), FIX-006 (VERIFIED), FIX-007 (PROBABLE), FIX-008 (UNRESOLVED), FIX-009 (VERIFIED), FIX-010 (VERIFIED) | Against sealed labels: compare system quality state (VERIFIED/PROBABLE/UNRESOLVED/FAILED) to fixture specification | A |
| 2.3 | **False-Quality Detection** | % of false-quality fixtures (FIX-004) where the system correctly identifies that quality is illusory | `PROVISIONAL_M4B_THRESHOLD` | FIX-004 (FALSE_QUALITY) — plus relevant comparisons against FIX-001, FIX-005, FIX-009 (genuine quality that must not be classified as false) | Against sealed labels: verify system output correctly identifies false-quality indicators and does not misclassify genuine quality as false | A |
| 2.4 | **Temporary-vs-Structural Calibration** | Accuracy of the system's impairment diagnosis — % of fixtures where impairment classification matches sealed label | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types (TEMPORARY: FIX-001, FIX-006, FIX-009; MOSTLY_TEMPORARY: FIX-005, FIX-007, FIX-010; MIXED: FIX-003; STRUCTURAL: FIX-002, FIX-004; UNRESOLVED: FIX-008) | Against known outcomes: compare system impairment diagnosis to fixture impairment label | A |
| 2.5 | **Recovery Mechanism Quality** | % of cases where the system articulates a specific (non-circular) recovery mechanism when impairment is temporary | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (temporary — recovery via lockdown reopening), FIX-005 (balance sheet — recovery via deleveraging), FIX-006 (industry — recovery via oil price normalization), FIX-009 (valuation — recovery via earnings realization), FIX-010 (panic — recovery via narrative normalization) | Review: expert assessor evaluates whether the recovery mechanism is specific, evidence-supported, and non-circular ("things get better" is insufficient) | A |
| 2.6 | **Thesis-Killer Detection** | % of thesis-killer evidence items per fixture that the system correctly identifies as material | `PROVISIONAL_M4B_THRESHOLD` | FIX-002 (STRUCTURAL — digital substitution evidence), FIX-004 (FALSE_QUALITY — accounting red flags), FIX-005 (BALANCE_SHEET — debt maturity/deleveraging), FIX-007 (COMPANY_SHOCK — regulatory/certification risk) | Against manual baseline: curator pre-identifies thesis-killer evidence per fixture; system output checked for explicit identification | A |
| 2.7 | **False-Confidence Rate** | % of fixtures where the system expresses high/confident verdict that is later contradicted by the known outcome window | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types, with weighted penalties on FIX-008 (AMBIGUOUS) where forced confidence is wrong | Against outcomes: cross-reference system confidence level (HIGH / MEDIUM / LOW) with fixture known outcomes; confident wrong verdicts are failures | A |

---

## 3. Financial Quality (Type A)

Tests the quality of financial analysis, calculations, and valuation.

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 3.1 | **Calculation Reproducibility** | % of financial calculations in the system's output that can be independently reproduced from the cited source data with identical results | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (revenue/margin normalization), FIX-005 (leverage/debt service ratios), FIX-006 (unit economics, cash flow breakeven), FIX-009 (burn rate analysis) | Independent recalculation: auditor replicates system calculations from source data; PROVISIONAL_M4B_THRESHOLD (empirical_basis = NOT_YET_CALIBRATED, sample_size = N/A, uncertainty = UNRESOLVED, Founder_ratification_required = true) tolerance for rounding | A |
| 3.2 | **Normalization Correctness** | % of adjustments to reported financials that the system correctly identifies as one-time/non-recurring vs ongoing | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (COVID-related one-time impacts), FIX-003 (segment-level normalization), FIX-004 (suspicious revenue recognition), FIX-010 (one-time charges vs structural margin decline) | Against manual baseline: curator identifies correct normalization adjustments per fixture; system adjustments compared | A |
| 3.3 | **Permanent-Loss Coverage** | % of fixtures where the system includes an analysis of permanent capital loss risk, even when impairment is found to be temporary | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — mandatory: FIX-005 (balance sheet explicit loss risk), FIX-002 (structural loss), FIX-004 (fraud loss) carry higher weight | Automated check: system output parsed for permanent loss analysis section or explicit statement | A |
| 3.4 | **Reverse-DCF Correctness** | % of reverse DCF calculations performed by the system that are mathematically correct and use consistent assumptions | `PROVISIONAL_M4B_THRESHOLD` | FIX-009 (VALUATION_FAILURE — market price vs DCF-implied expectations), FIX-010 (NARRATIVE_PANIC — price disconnect from fundamentals), FIX-001 (TEMPORARY — recovery price expectations) | Against independent model: auditor runs parallel DCF with same inputs; verify results match | A |
| 3.5 | **Scenario Consistency** | % of multi-scenario analyses where assumptions are internally consistent across scenarios (no contradictory base cases) | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (bull/bear/base on recovery), FIX-003 (segment divergence scenarios), FIX-008 (ambiguous-case scenario comparison), FIX-005 (leverage stress scenarios) | Cross-check: auditor reviews scenario assumptions for internal contradictions (e.g., revenue growth and margin assumptions in one scenario that conflict) | A |

---

## 4. Process Quality (Type A)

Tests compliance with the Point-in-Time sealed evaluation protocol.

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 4.1 | **PIT Correctness** | % of evidence items cited by the system that are within the AS_OF_DATE bounds (no post-AS_OF leakage) | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — mandatory leakage test per §2.4 | Automated PIT check: scan all evidence sources cited in output against the AS_OF_DATE; any post-AS_OF source is a failure | A |
| 4.2 | **Provenance Completeness** | % of evidence items in research output that include full provenance information (source title, date, author, URL/document ID, access date) | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types | Automated check: parse evidence citations for required provenance fields; count complete vs incomplete | A |
| 4.3 | **Failure-State Correctness** | % of fixtures where the system explicitly records failure states (insufficient data, ambiguous evidence, calculation not possible, verification required) when applicable | `PROVISIONAL_M4B_THRESHOLD` | FIX-008 (AMBIGUOUS — high failure-state expectation), FIX-003 (MIXED — segment-level insufficient data risk), FIX-004 (FALSE_QUALITY — sources may be unreliable) | Audit: curator reviews system output for explicit failure-state recording; correct recording vs unreported failures | A |
| 4.4 | **Research-Stop Quality** | % of fixtures where the system documents the reason research stopped (saturation reached / evidence sufficient / information value below threshold / no more data available) | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types | Audit: curator evaluates whether the stop decision has a documented, evidence-based rationale (not implicit) | A |
| 4.5 | **Audit-Gate Correctness** | % of audit gates (PIT lock verification, source verification, calculation check, internal consistency) that are correctly passed and documented | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — mandatory audit trail per fixture | Audit: curator checks audit gate log for each fixture; each gate must show explicit pass/fail and timestamp | A |
| 4.6 | **Report Factual-Error Rate** | Number of factual errors (incorrect data, mis-sourced claims, calculation errors, outdated metrics) per published report equivalent | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — weighted: higher data-density fixtures (FIX-001, FIX-005, FIX-006) carry more error-check weight | Post-publication audit: expert reviewer fact-checks PROVISIONAL_M4B_THRESHOLD (empirical_basis = NOT_YET_CALIBRATED, sample_size = N/A, uncertainty = UNRESOLVED, Founder_ratification_required = true) of claims in system output per fixture | A |

---

## 5. Discovery Quality (Type B)

Tests the system's ability to discover material companies and opportunities from a universe. Evaluated separately from Type A with different fixture sets.

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 5.1 | **Universe Coverage Rate** | % of eligible companies in a defined universe that the system scans (minimum evidence-gathering attempt) | `PROVISIONAL_M4B_THRESHOLD` | FIX-006 (INDUSTRY_SHOCK — scan all oil & gas peers), FIX-010 (NARRATIVE_PANIC — scan large-cap tech peer set) | Automated: check system output against defined universe list; verify each company received a discovery attempt | B |
| 5.2 | **Data-Ready Coverage** | % of scanned companies for which the system gathers sufficient data to proceed to a preliminary thesis | `PROVISIONAL_M4B_THRESHOLD` | FIX-006 (oil & gas universe — many companies, varying data availability), FIX-002 (print/directory cos — declining data quality) | Automated: system must output a data-readiness flag per company; curator validates | B |
| 5.3 | **Known-Opportunity Recall** | % of known material opportunities within the universe that the system correctly identifies as candidates | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (TEMPORARY — known opportunity in COVID-disrupted quality names), FIX-009 (VALUATION_FAILURE — known opportunity in dot-com survivors) | Against sealed list: curator pre-identifies known opportunities; system candidate list compared for recall | B |
| 5.4 | **Quality Candidate Recall** | % of quality companies in the universe that the system correctly identifies as quality candidates | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (SBUX — must identify as quality), FIX-006 (CVX — must identify as quality within industry), FIX-009 (AMZN — must identify as quality despite valuation panic), FIX-010 (AAPL — must identify as quality despite narrative) | Against sealed list: compare system quality identifications to pre-sealed list of quality companies in the universe | B |
| 5.5 | **Dislocation Detection Rate** | % of material price dislocations (temporary quality/valuation separation) in the universe that the system detects | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (COVID-driven dislocation), FIX-009 (tech-crash-driven dislocation), FIX-010 (narrative-driven dislocation), FIX-007 (MAX-crash-driven dislocation) | Against sealed list: curator pre-identifies known dislocations; system output checked for detection | B |
| 5.6 | **Signal-to-Candidate Conversion** | % of signals (price movement, news, fundamental deviation) generated by the system's discovery layer that advance to candidate status | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — benchmark: expected conversion range | Automated: count signals generated vs candidates created | B |
| 5.7 | **Candidate-to-Research Conversion** | % of candidates that advance to full research case status | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — benchmark: expected conversion range | Automated: count candidates vs research cases opened | B |
| 5.8 | **Discovery Cost per New Candidate** | Average cost (token spend, API cost, compute time) required to discover one new candidate | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — cost tracking across discovery process | Cost tracking: sum discovery-phase costs divided by number of unique candidates discovered | B |
| 5.9 | **False Positive Rate (Material)** | % of discovered candidates that consumed material research time but were ultimately determined to be non-material or false positives | `PROVISIONAL_M4B_THRESHOLD` | FIX-004 (FALSE_QUALITY — high risk of false positive), FIX-008 (AMBIGUOUS — uncertain cases may generate false positives), FIX-002 (STRUCTURAL — may appear as temporary value opportunities) | Review: curator evaluates each candidate that progressed to research; classify as true positive vs false positive | B |
| 5.10 | **Decision-Changing Candidate Recall** | % of candidates in the universe that would have changed a portfolio-relevant decision (add, avoid, position size, sell) that the system discovered | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — headline metric for Discovery Quality | Outcome analysis: curator defines "decision-important" candidates per universe; system recall against this list is the headline Type B metric | B |

---

## 6. Saturation / Information Value Metrics (Type A)

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 6.1 | **Research Depth vs Decision Impact** | Source count vs verdict-change frequency — correlation between evidence volume and decision certainty | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — compare source-dense (FIX-001, FIX-006) vs source-sparse (FIX-008, FIX-009) | Automated analysis: plot system's source count per fixture against verdict confidence level; identify diminishing-returns threshold | A |
| 6.2 | **Premature Stopping Rate** | % of fixtures where additional evidence beyond what the system collected would have changed the verdict | `PROVISIONAL_M4B_THRESHOLD` | FIX-008 (AMBIGUOUS — high premature stopping risk), FIX-004 (FALSE_QUALITY — early fraud evidence may be missed) | Review: curator identifies evidence items that were available but not collected; assess whether they would have changed verdict | A |
| 6.3 | **Excess Research Rate** | % of fixtures where the system collected evidence beyond the point where additional evidence changes the verdict (diminishing returns) | `PROVISIONAL_M4B_THRESHOLD` | FIX-009 (VALUATION_FAILURE — minimal evidence needed for strong verdict), FIX-010 (NARRATIVE_PANIC — strong verdict from first-order evidence) | Review: assess whether evidence collection past a saturation point adds decision value or is redundant | A |
| 6.4 | **EIV Threshold Accuracy** | % of fixtures where the system's stop decision matches the estimated information value threshold | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types | Against EIV model: compare system's actual stop point to the calculated expected-information-value-optimal stop point | A |

---

## 7. Cost / Model Routing Metrics (Type A)

| # | Metric | Definition | Pass Threshold | Fixture Type Tests It | Measurement Method | Type |
|---|--------|-----------|--------------|----------------------|--------------------|------|
| 7.1 | **Cost per Completed Case** | Total evaluation cost (tokens, API fees, compute, research model calls) divided by number of completed fixture evaluations | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — aggregate across all evaluations | Cost tracking: sum all costs across fixture evaluations; divide by N completed | A+B |
| 7.2 | **Tokens per Stage** | Token consumption broken down by research stage (discovery, evidence gathering, analysis, verification, writeup) | `PROVISIONAL_M4B_THRESHOLD` | FIX-001 (TEMPORARY — moderate sources), FIX-004 (FALSE_QUALITY — high source density), FIX-008 (AMBIGUOUS — high analysis cost) | Automated: instrument each research stage for token consumption; report per-stage averages | A+B |
| 7.3 | **Expensive-Model Escalation Rate** | % of fixture evaluations requiring Tier C/D model escalation (per §7.1 tier model) | `PROVISIONAL_M4B_THRESHOLD` | FIX-004 (FALSE_QUALITY — likely requires Tier C for fraud analysis), FIX-008 (AMBIGUOUS — likely requires Tier C for calibration), FIX-003 (MIXED — may require Tier C for segment analysis) | Automated: track model tier usage per fixture; calculate escalation frequency | A+B |
| 7.4 | **Retry Cost** | Cost of failed or retried operations (API errors, timeouts, verification failures, recalculation) | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — monitor retry rate across all evaluations | Cost tracking: log all failed/retried operations; compute total wasted cost | A+B |
| 7.5 | **Deep Research Cost** | Cost of Deep Research / NotebookLM / equivalent external deep-research tools used during evaluation | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — measure by frequency and cost of external research tool calls | Cost tracking: instrument deep-research tool usage separately from base model costs | A+B |
| 7.6 | **Decision-Changing Evidence per Research Cost** | Ratio of decision-changing evidence items captured to total research cost (efficiency metric) | `PROVISIONAL_M4B_THRESHOLD` | All 10 fixture types — primary cost-efficiency metric | Ratio: (decision-changing evidence count from 1.6) / (total research cost across evaluations) | A+B |

---

## Threshold Policy Notes

All `PROVISIONAL_M4B_THRESHOLD` values require the following in the Calibration Report per M4B Evaluation Contract §8.2:

```text
empirical_basis: [data source, sample size — to be populated during calibration]
sample_size: [to be populated during calibration]
uncertainty: [confidence interval — to be populated during calibration]
sensitivity: [impact of ±X% variation — to be populated during calibration]
failure_consequences: [what happens if threshold is wrong — to be populated during calibration]
```

Thresholds are proposed in the M4B Calibration Report (`QAD-M4B-CALIBRATION-REPORT.md`) and ratified via Founder decision before becoming production gates. M4B measures and proposes; it does not constitutionalize.

---

## Summary

| Type | Dimension | Metrics Count |
|------|-----------|--------------|
| A | Evidence Quality (§4.1) | 6 |
| A | Analytical Quality (§4.2) | 7 |
| A | Financial Quality (§4.3) | 5 |
| A | Process Quality (§4.4) | 6 |
| A | Saturation / EIV (§6) | 4 |
| B | Discovery Quality (§4.5) | 10 |
| A+B | Cost / Model Routing (§7) | 6 |
| **Total** | | **44** |

- **Type A failures:** Company discovered but research wrong — 28 metrics across Evidence, Analytical, Financial, and Process Quality, plus 4 EIV metrics, plus shared cost metrics
- **Type B failures:** Material company never discovered — 10 Discovery Quality metrics, plus shared cost metrics
- **Type A+B (Shared):** 6 Cost/Model Routing metrics apply to both evaluation types
- **Dimensions evaluated on Type-A fixtures only:** Evidence Quality, Analytical Quality, Financial Quality, Process Quality, Saturation/EIV
- **Dimensions evaluated on Type-B fixtures only:** Discovery Quality
- **Dimensions evaluated on both:** Cost/Model Routing

<!-- 2026-08-19 16:45 UTC+7 -->