# QAD Operating Model

> **Contract:** M3-01 (M3 Domain Contract Set)
> **Status:** M3 FINAL DRAFT (CORRECTION COMPLETE — AWAITING INDEPENDENT RE-REVIEW)
> **Authority:** Constitution §1/§2/§3 (QAD mission); Constitution §14 (Candidate-First); FD #130; Frozen Architecture Decisions (ARCHITECTURE-DESIGN-GATE-FINAL.md); FD #131
> **Traceability:** CONSTITUTION-§1/§2/§3 · FD #130 · FROZEN-ARC-DEC-001..019 · NEW_M3_DERIVATION (operational flow specification)

---

## 1. North Star

> **IIP exists to identify, investigate, falsify, and monitor situations where a high-quality business may be priced as though temporary economic impairment is permanent.**

And equally:

> **The system must never presume that the impairment is temporary. Its central task is to determine whether it is temporary, structural, mixed, or unresolved.**

### Four Independently Supported Propositions

```
QUALITY            — Is this a genuinely high-quality business?
+
DISLOCATION        — Is the business experiencing material market/business dislocation?
+
IMPAIRMENT DIAGNOSIS — Is the impairment temporary, structural, or unresolved?
+
VALUATION ASYMMETRY — Does the price imply expectations far worse than the evidence warrants?
```

**No composite QAD score.** No assumption that "good company + low price" alone constitutes a QAD opportunity. Each proposition must be independently supported by evidence.

---

## 2. End-to-End Operating Flow

The complete QAD research and underwriting lifecycle:

```text
OBSERVATION
    │
    ▼
DISCOVERY
  ├─ Lane A: Quality-First
  ├─ Lane B: Dislocation-First
  └─ Lane C: External Discovery (Radar Scout, Founder, filings, ecosystem)
    │
    ▼
CANDIDATE
  └─ Selection Engine applies policy → AUTO_RESEARCH_NOW / WATCH_PRICE / WATCH_EVIDENCE / DATA_LIMITED_WATCH / REJECT
    │
    ▼
CASE OPEN
  └─ Research Charter created with Competing Hypotheses H1–H5
    │
    ▼
EVIDENCE FOUNDATION
  └─ Primary Source Foundation → Evidence Gap Map
    │
    ├──► DEEP RESEARCH / SCUTTLEBUTT (elastic investigators)
    │
    ▼
EVIDENCE GRAPH — Canonical Evidence Registry
    │
    ▼
ANALYTICAL WORK
  ├─ Quality Analysis (§ Business/Industry/Management)
  ├─ Industry Economics
  ├─ Financial & Management Analysis
  ├─ Dislocation Reconstruction
  ├─ Impairment Diagnosis
  ├─ Recovery Model
  ├─ Normalized Economics
  ├─ Permanent Loss Analysis
  └─ Valuation / Reverse DCF
    │
    ▼
STRUCTURAL RED TEAM (independent challenge — strongest value-trap case)
    │
    ▼
INDEPENDENT AUDIT (source existence, citation correctness, PIT integrity)
    │
    ▼
CHIEF UNDERWRITING (synthesis of all analytical work + Red Team + Audit)
    │
    ▼
THAI LONG-FORM PUBLICATION (journalism, not canonical database entry)
    │
    ▼
FOUNDER (final judgment authority)
    │
    ├──► RESEARCH COMPLETE / FOUNDER_READY / FOUNDER_ENDORSED
    │
    ▼
THESIS MONITORING (thesis-specific indicators, not generic news)
    │
    ▼
KNOWLEDGE COMPOUNDING (cross-case validation → approved knowledge)
    │
    ▼
EVALUATION (Type A: researched incorrectly? Type B: failed to discover?)
```

---

## 3. State Ownership & Stop Conditions

| Stage | State Owner | Stop Condition | Escalation |
|-------|-------------|----------------|------------|
| Discovery | Discovery Scout / Lane Owners | No candidate generated; `NO_NEW_MATERIAL_QAD_CANDIDATE` is valid | None (continue cadence) |
| Selection | Selection Engine (policy-governed service) | Candidate policy applied; output is selection state | Policy exception → Founder |
| Case Open | Research Director | Research Charter approved with H1–H5 | Budget exhaustion → Research Budget Controller |
| Evidence Foundation | Evidence Intelligence Lead | Evidence Gap Map complete; gaps may remain | Budget insufficient → Research Budget Controller |
| Deep Research | Research Director + Elastic Investigators | All evidence gaps closed OR budget exhausted OR falsification confirmed | Budget exhaustion → `INCOMPLETE`, not weakened quality |
| Analytical Work | Core Desk Researcher / Specialists | Each analytical box complete against contract | Hypothesis fails → case disposition |
| Red Team | Structural Red Team (independent) | Strongest value-trap case constructed | No veto; findings carried forward |
| Audit | Independent Auditor | Source/citation/PIT verification complete | May block `FOUNDER_READY` |
| Underwriting | Chief Underwriter | Research verdict state assigned | Escalation to Founder if QAD_UNRESOLVED |
| Publication | Thai Editor | Founder-ready publication produced | Founder-gated |
| Founder | Founder | Decision made | N/A (final authority) |
| Monitoring | Thesis / Knowledge Steward | Thesis indicators tracked; state updated | BROKEN state → notify Founder |
| Knowledge | Knowledge Steward | Cross-case validation → approved knowledge | Single case ≠ institutional knowledge |

---

## 4. Inputs & Outputs

### System-Level Inputs
- Raw corporate filings (SEC EDGAR, global equivalents)
- Market data (prices, volumes, corporate actions)
- Industry data (trade associations, government statistics, independent research)
- Ecosystem data (competitor filings, supplier/customer intelligence)
- Digital observable data (regulatory, patent, scientific, channel)
- Founder direction (entry_route = FOUNDER_DIRECTED)
- Radar Scout signals (non-authoritative discovery supplement)

### System-Level Outputs
- Published research (Thai long-form articles on `/library`)
- Case records (analytical state, evidence graph, decisions)
- Monitoring updates (thesis indicator tracking)
- Evaluation data (Type A/B metrics)
- Knowledge artifacts (cross-validated lessons, industry playbooks)

---

## 5. Canonical/Noncanonical Boundary

| Layer | Status | Comment |
|-------|--------|---------|
| Raw Source Archive | Canonical | Immutable primary evidence |
| Canonical Evidence Registry | Canonical | Curated, source-verified facts/claims |
| Evidence Graph | Canonical | Relationships, contradictions, gaps |
| Analytical State | Canonical | Quality/Impairment/Valuation determinations |
| Published Report | Noncanonical for investment truth | Publication ≠ canonical database update |
| Founder Decision | Canonical | Final authority; recorded in FD register |
| NotebookLM / Deep Research | Noncanonical | Research discovery layer only; must validate against original source |

---

## 6. Separation of Duties (System-Level)

| Separation | Rationale |
|------------|-----------|
| Discovery ≠ Selection | Discovery finds candidates; Selection applies policy |
| Selection ≠ Underwriting | Selection Engine cannot choose its own cases |
| Research ≠ Independent Audit | Auditor is independent; does not decide thesis |
| Primary Thesis ≠ Structural Red Team | Red Team constructs the opposing case |
| Evidence Discovery ≠ Canonical Admission | Finding evidence ≠ validating it as canonical |
| Calculation Production ≠ Independent Recalculation | Audit must reproduce calculations independently |
| Publication Editing ≠ Thesis Creation | Thai Editor edits; does not create thesis |
| Chief Underwriter ≠ Portfolio Manager | Underwriting is research output; no allocation authority |
| AI Research Result ≠ Founder Endorsement | AI produces Founder-ready; Founder alone endorses |

---

## 7. Reliability Contract

- **Idempotent stages:** Discovery scan, Selection engine, Evidence admission, Calculation, Auditor re-run
- **Checkpoints:** Every material transition records point-in-time state
- **Bounded retries:** Max 3 retries per stage; budget exhaustion → `INCOMPLETE`, not weakened quality gate
- **Stage restart:** Previous stage output preserved; restart from last checkpoint
- **Dependency tracking:** Every analytical output records its input dependencies
- **Case locking:** Case cannot be modified during active research; new as-of → new case version
- **De-duplication:** Signal/Candidate registries enforce uniqueness by source + key + as-of

### Failure States

| Failure Mode | Fallback | Quality Impact |
|--------------|----------|----------------|
|| Data source unavailable | Skip, document gap, continue | Gap flagged; no silent completeness. Material source unreachable may force `INCOMPLETE`. |
|| Budget exhausted | Case marked `INCOMPLETE` | Not published as complete research. Budget exhaustion must NOT weaken quality gates. |
|| Selection Engine failure | `SELECTION_ERROR` or `EVALUATION_UNAVAILABLE`; candidate remains pending/retryable | Technical failure must NEVER silently produce `SKIP` or `REJECT` (Type-B discovery miss). |
|| PIT mode violation | SEALED mode hard-blocks post-AS_OF evidence; LIVE mode requires explicit UPDATE tag | No future-information leakage into M4B fixtures. |
|| Evaluation Harness partial | `EVALUATION_INCOMPLETE` | Cannot satisfy an evaluation gate. Must not produce partial results labeled as complete. |
|| Retry limit exceeded | Stage marked `FAILED` | Escalation to Research Director |
|| Auditor blocks | Case blocked at `FOUNDER_READY` | Cannot reach Founder without resolution |
|| Model call fails | Retry (3×); fallback to alternate provider | Documented in Run Manifest |

---

## 8. Run Manifest

Every research run produces a mandatory manifest:

```text
research_run_id:       UUID v7
case_id:               CASE-YYYY-NNN
case_version:          semantic version (new as-of → new version)
as_of_date:            ISO date (point-in-time anchor)
universe_version:      U-YYYYMMDD-N
selection_policy_version: SP-V.N
models_used:           [model, model, ...]
model_versions:        {model: version, ...}
providers:             {model: provider, ...}
prompts/contracts:     [contract_hash, ...]
notebook_runs:         [run_id, ...]
deep_research_runs:    [run_id, ...]
sources_added:         N
calculation_version:   CALC-V.N
start_time:            ISO datetime
completion_time:       ISO datetime
token_usage:           {model: tokens, ...}
cost:                  {provider: cost, ...}
retries:               N
failures:              [{stage, reason, resolution}, ...]
output_version:        OUTPUT-V.N
```

Point-in-Time Lock: every case has an `AS_OF_DATE`. Historical evaluation must prohibit post-AS_OF_DATE evidence unless explicitly tagged as an update/replay exception.

---

## 9. Budget Discipline

The Research Budget Controller applies approved policy:

- Default research budget per case: configurable in policy
- Elastic investigation (Scuttlebutt) draws from the same case budget
- Budget exhaustion does NOT weaken quality gates — case becomes `INCOMPLETE`
- Budget may be increased by Founder override only
- Research Director proposes; Budget Controller approves; Director does not self-authorize

---

## 10. Forbidden Actions

The QAD system must NEVER:

- Execute trades or transmit orders
- Allocate portfolio capital or size positions
- Create authoritative BUY/SELL/POSITION SIZE state
- Collapse competing hypotheses into a single bullish thesis
- Allow Chief Underwriter to select its own cases
- Allow NotebookLM/Deep Research output to enter canonical truth without original-source validation
- Allow social evidence (L10) to independently support a material conclusion
- Silence or average away contradicting evidence
- Weaken quality gates on budget exhaustion (must use `INCOMPLETE`)
- Count Founder-directed cases as autonomous discovery recall

<!-- 2026-08-19 11:30 UTC+7 -->

> **M4A Cross-Reference:** Case schema fields are defined jointly with QAD-FULL-RESEARCH-PROTOCOL.md (M3-03 §3 Stages 1-2). This contract defines case_id, version, manifest, and stage state map. M3-03 defines charter content, H1-H5 lifecycle, and stage transitions. M4A implementers MUST read both contracts.