# QAD Challenge, Audit, Underwriting, Publication, Monitoring, Knowledge & Evaluation Contract

> **Contract:** M3-09 (M3 Domain Contract Set — combines M3-09 and M3-10 from lean spec)
> **Status:** M3 FINAL — FROZEN FOR M4 DERIVATION
> **Authority:** FD #130; Constitution §23 (AI Operating Constitution); CAP-009 (CIW ABSORB: Cross-Exam, audit); CAP-016 (REUSE: Audit Infrastructure); CAP-014 (REUSE: Thai Editorial Standard); FD #94 (Publication Firewall); FD #96 (Category/Library structure)
> **Traceability:** CONSTITUTION-§23 · CAP-009 (CIW: Cross-Exam/CRO) · CAP-014 (REUSE: Thai Editorial) · CAP-015 (REUSE: Live Office monitoring) · CAP-016 (REUSE: Audit Infrastructure) · CAP-017 (REUSE: Evidence Doctrine) · FD #94 · FD #96 · EVIDENCE-DOCTRINE · NEW_M3_DERIVATION (Red Team charter, Underwriting verdict states, Monitoring protocol, Evaluation typology)

---

## 1. Four Separate Functions

```text
STRUCTURAL RED TEAM     — Assume the thesis is wrong. Construct the strongest value-trap case.
INDEPENDENT AUDITOR     — Verify source/citation/PIT/calculation integrity. May block FOUNDER_READY.
CHIEF UNDERWRITER       — Synthesize all analysis into a research verdict.
PUBLICATION             — Transform research into Thai long-form journalism.
```

No function may be combined with another in the same logical role (Separation of Duties).

---

## 2. Structural Red Team

### 2.1 Mission

> **Assume the QAD thesis is wrong and the market may be correct.**

The Structural Red Team constructs the strongest structural/value-trap case against the primary thesis. It does NOT attempt to be "fair" or "balanced" — it argues the opposing side as forcefully as the evidence allows.

### 2.2 Charter

| Field | Value |
|-------|-------|
| **Assumption** | QAD thesis is WRONG |
| **Default Position** | Impairment is STRUCTURAL, not temporary |
| **Burden** | Construct the case that quality is absent, impairment is permanent, or valuation is already fair |
| **No Veto** | Red Team findings cannot veto the thesis — they are carried forward to Underwriting |
| **Final Outcome** | `ACCEPTED` / `PARTIALLY_ACCEPTED` / `REJECTED_WITH_EVIDENCE` / `UNRESOLVED` |

### 2.3 Required Analysis

The Red Team must address at minimum:

1. **Against Quality** — Is quality assumption wrong? Moat absent? Returns not durable?
2. **Against Temporary** — Why is the impairment structural, not temporary?
3. **Against Recovery** — What makes recovery unlikely even if impairment is temporary?
4. **Against Management** — What management failures make recovery improbable?
5. **Against Valuation** — Why is the current price fair or cheap for a reason?
6. **For Market Correctness** — What does the market see that the thesis misses?
7. **Hidden Risks** — Unknown unknowns, balance-sheet risks, regulatory, legal, technological
8. **Cost of Being Wrong** — What is the permanent loss if the Red Team is right?

### 2.4 Red Team Independence

- Red Team must have NO prior involvement in the research or thesis creation
- Red Team must not have participated in evidence gathering for this case
- Red Team's output is preserved verbatim alongside the final underwriting verdict
- The Research Director cannot dismiss or suppress Red Team findings

---

## 3. Independent Audit

### 3.1 Mission

Verify the integrity of the research record. The auditor checks what EXISTS, not whether it is correct.

### 3.2 Audit Checklist

| Check | What Is Verified | Pass/Fail |
|-------|------------------|-----------|
| Source Existence | Every cited source exists and is accessible | |
| Original-Source Inspection | Every material fact is traced to original source (not secondary) | |
| Citation Correctness | Every citation points to the correct source, page, and context | |
| PIT Integrity | As-of dates are correct; no post-AS_OF_DATE evidence used without tagging | |
| Calculation Reproducibility | Every derived calculation can be independently reproduced | |
| Contradiction Preservation | All contradictory evidence is preserved, not suppressed | |
| Model Provenance | AI model, version, provider recorded for every AI-generated output | |
| Self-Review Separation | No person/role reviewed their own work | |
| Publication Gates | Required gates (Red Team, Audit) completed before FOUNDER_READY | |

### 3.3 Audit Authority

| Authority | Detail |
|-----------|--------|
| **May block FOUNDER_READY** | If audit fails, case cannot reach Founder |
| **Does not decide the thesis** | Audit checks process, not substance |
| **May call for recalculation** | If calculation cannot be reproduced |
| **May call for source verification** | If source cannot be found |
| **Records all findings** | Audit report is part of the permanent case record |

### 3.4 Audit Outcomes

| Outcome | Meaning | Next Action |
|---------|---------|-------------|
| **PASS** | All checks pass with no material findings | Case proceeds to Founder |
| **PASS_WITH_FINDINGS** | Pass with minor, non-blocking findings | Findings recorded; case proceeds |
| **FAIL** | One or more blocking findings | Case blocked; must be resolved before FOUNDER_READY |

---

## 4. Chief Underwriter

### 4.1 Mission

Synthesize all analytical work, challenge, and audit into a final research verdict.

The Chief Underwriter reads and weighs:
- Quality Analysis (M3-06)
- Industry Economics (M3-06)
- Financial Reconstruction (M3-08)
- Management Assessment (M3-06)
- Dislocation Reconstruction (M3-07)
- Impairment Diagnosis (M3-07)
- Recovery Model (M3-07)
- Normalized Economics (M3-08)
- Valuation / Reverse DCF (M3-08)
- Structural Red Team findings (§2)
- Independent Audit report (§3)

### 4.2 Research Verdict States

| State | Meaning |
|-------|---------|
| **QAD_CONFIRMED** | All four propositions (Quality + Dislocation + Impairment + Valuation) are supported by evidence. High confidence in temporary impairment. |
| **QAD_PROBABLE** | Most evidence supports QAD thesis but material uncertainty remains. |
| **QAD_UNRESOLVED** | Cannot reach verdict — material evidence gaps or the diagnosis is genuinely ambiguous. |
| **NOT_QAD_STRUCTURAL** | Impairment is structural, not temporary. The business or industry is permanently damaged. |
| **NOT_QAD_QUALITY** | Quality assumption is wrong — the business was never high-quality. |
| **NOT_QAD_VALUATION** | The price already reflects the impairment (fair or unattractive even at this level). |

### 4.3 Chief Underwriter Forbidden Actions

| Forbidden | Why |
|-----------|-----|
| Choose its own cases | Selection Engine maintains separation |
| Allocate capital | Portfolio management is external |
| Size positions | No investment authority |
| Execute trades | No broker connectivity |
| Overrule Red Team findings | Red Team findings are preserved, not vetoed |
| Ignore contradictory evidence | All evidence must be weighed |

### 4.4 Underwriting Output

The full underwriting output includes:

1. Research Verdict (one of six states)
2. Synthesis narrative (why this verdict over alternatives)
3. Scenario weightings (subjective assessment of each scenario's likelihood)
4. Key uncertainties ranked by materiality
5. Thesis-specific monitoring indicators
6. Recommendation to Founder (advisory — does not equal endorsement)

---

## 5. Publication

### 5.1 Mission

Transform the research record into Thai long-form journalism for `/library`.

### 5.2 Publication States

| State | Meaning |
|-------|---------|
| **RESEARCH_COMPLETE** | Research is done; publication not yet written |
| **FOUNDER_READY** | Publication written, Red Team completed, Audit passed — ready for Founder review |
| **FOUNDER_ENDORSED** | Founder explicitly agrees with thesis (recorded as FD) |
| **FOUNDER_DISAGREES** | Founder disagrees with thesis (recorded as FD) |
| **FOUNDER_REJECTS** | Founder rejects thesis entirely (recorded as FD) |

**Never** `FOUNDER_ENDORSED` unless Founder explicitly acts. The system does not self-declare endorsement.

### 5.3 Publication Rules (per FD #94 Thai Editorial Standard)

- Thai language (per FD #92 — Thai research content unless Founder specifies English)
- No internal governance jargon (RM/ORG/FD/spec/§/workspace/audit-status/portfolio-blind) in reader-facing content (FD #94)
- Companion publication (CRO opposing thesis) nested under main article (FD #96)
- Category frontmatter field for library organization (FD #96)
- PDF is publication, not canonical truth

### 5.4 Companion Publication

For every main QAD thesis, a companion publication should be produced representing the strongest opposing case. The companion should be:

- Labeled as opposing view (slug convention: `<base>-opposing-<date>`)
- Linked from the main article
- Published alongside the main thesis
- Given equal prominence in `/library`

---

## 6. Thesis Monitoring

### 6.1 Mission

Monitor thesis-specific indicators, not generic news flow. Monitoring follows the thesis wherever it leads — it does not passively watch the company.

### 6.2 Monitoring Indicators

Indicators are defined during underwriting (Chief Underwriter defines what would confirm or refute the thesis):

- **Recovery indicators** — evidence that recovery is occurring as modeled
- **Warning indicators** — signs that recovery is off track
- **Thesis-killer indicators** — specific conditions that would invalidate the thesis

### 6.3 Monitoring States

| State | Meaning |
|-------|---------|
| **RECOVERY_CONFIRMING** | Thesis indicators tracking as expected; recovery on track |
| **ON_TRACK** | Mixed signals but overall thesis direction holds |
| **UNCERTAIN** | Evidence ambiguous; cannot determine direction |
| **WEAKENING** | Evidence points away from thesis; thesis becoming less probable |
| **BROKEN** | Thesis is no longer supported by evidence; should be abandoned |

### 6.4 Monitoring Protocol

- Monitoring is indicator-specific, not company-generic
- No monitoring update = no material change (valid outcome)
- State transitions require evidence, not time
- BROKEN state triggers notification to Founder
- Monitoring does NOT create new research mandates automatically

---

## 7. Knowledge Compounding

### 7.1 Knowledge Admission

```text
Research Finding
    → Candidate Lesson
    → Cross-Case Validation (3+ independent cases)
    → Independent Review (not original researcher)
    → APPROVED KNOWLEDGE
    → Industry Playbook (if industry-specific)
```

A single research case does NOT automatically become institutional knowledge.

### 7.2 Knowledge States

| State | Criteria |
|-------|----------|
| **Research Finding** | Observation from a single case |
| **Candidate Lesson** | Consistent pattern in 2+ cases |
| **Cross-Case Validated** | 3+ independent cases confirm pattern |
| **Independently Reviewed** | Reviewed by different role |
| **APPROVED KNOWLEDGE** | Cross-case + review + Chief Underwriter approval |

---

## 8. Evaluation

### 8.1 Two Separate Questions

```text
Type A — Did we research the discovered company correctly?
    (Research Quality — existing evaluation framework)
    
Type B — Did we fail to discover a material candidate?
    (Discovery Recall — NEW, first-class metric for QAD)
```

### 8.2 Type A — Research Quality Evaluation

Metrics:
- Decision-Changing Evidence Recall — did the research capture evidence that would change the verdict?
- Thesis-killer detection rate
- Contradiction coverage rate
- Citation correctness rate
- PIT correctness rate
- Temporary vs Structural calibration accuracy
- Report factual-error rate

### 8.3 Type B — Discovery Recall Evaluation

Metrics:
- Universe Coverage Rate
- Data-Ready Coverage
- Known-Opportunity Recall
- Quality Candidate Recall
- Dislocation Detection Rate
- Signal-to-Candidate Conversion Rate
- Candidate-to-Research Conversion Rate
- Discovery Cost per New Candidate
- False Positive Rate (Material)
- **Decision-Changing Candidate Recall** (headline metric — how often did we discover candidates that change portfolio-relevant decisions?)

### 8.4 Evaluation Protocol

- Evaluation requires a sealed outcome corpus (hidden until evaluation run)
- Historical evaluation must use point-in-time data only (as-of = evaluation date, not today)
- Pre-AS_OF_DATE evidence only — no forward-looking information
- Separate runs for Type A and Type B may use different PIT snapshots

### 8.5 Threshold Calibration

Quantitative pass/fail thresholds are NOT defined in this contract. They belong in M4B (Evaluation Contract — Part 7), where they are derived from historical data and Founder-approved calibration runs.

**Thresholds invented in M3 are void.**

<!-- 2026-08-19 13:30 UTC+7 -->