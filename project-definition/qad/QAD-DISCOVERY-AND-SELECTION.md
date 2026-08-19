# QAD Discovery & Autonomous Selection Contract

> **Contract:** M3-02 (M3 Domain Contract Set)
> **Status:** M3 FINAL DRAFT (CORRECTION COMPLETE — AWAITING INDEPENDENT RE-REVIEW)
> **Authority:** FD #130; QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 (FROZEN); Constitution §14 (Candidate-First); ARCHITECTURE-DESIGN-GATE-FINAL.md
> **Traceability:** DISCOVERY-REQ-B1..B7 · DISCOVERY-REQ-C1..C7 · DISCOVERY-REQ-D · DISCOVERY-REQ-E · FD #130 · CAP-001 (REUSE) · CAP-002 (ADAPT) · CAP-003 (ADAPT) · CAP-011 (TRANSITIONAL_RETAIN) · CIW §5 · CONSTITUTION-§14 · NEW_M3_DERIVATION (selection state machine, policy service)
> **Supersedes:** Legacy Discovery & Coverage Operating Requirement (v0.1 absorbed as foundation)

---

## 1. Core Principle (Immutable)

> **Every eligible company must be observable by the system; not every company must be reasoned about by an LLM.**

Large-universe sensing uses deterministic/structured/cheap computation first. Expensive reasoning is progressively introduced only as candidate count falls.

---

## 2. Universe Layers (Six Registries)

| # | Registry | Content | Owner | State |
|---|----------|---------|-------|-------|
| 1 | `SECURITY_MASTER` | Every known security: issuer, exchange, listing, share class, ADR, dual listing, ticker changes, corporate actions, delisting | Security/Entity Resolution Service | Persistent |
| 2 | `RESEARCHABLE_UNIVERSE` | Researchable operating companies; explicit inclusion/exclusion state + reason per company; no silent omissions; identity reconciled per Security Master | Discovery & Coverage System | Persistent |
| 3 | `SIGNAL_REGISTRY` | All detected anomalies/dislocations/quality signals with provenance (who/when/why/data version/rule version/model version/evidence) | Signal Detection Layer | Append-only |
| 4 | `CANDIDATE_REGISTRY` | Companies that passed signal assembly into candidates; candidate state + priority + evidence freshness | Candidate Assembly | Stateful |
| 5 | `QUALITY_UNIVERSE` | Companies with accumulated evidence of high quality; membership does NOT require an active dislocation (DNA-017) | Quality Discovery | Stateful |
| 6 | `CASE_REGISTRY` | Companies that opened Full QAD Research | Case Management | Stateful |

Every transition records: who, when, why, data version, rule version, model version, evidence reference.

### Registry Semantics

- **SECURITY_MASTER** is the ground truth for entity identity. All other registries reconcile to it.
- **RESEARCHABLE_UNIVERSE** can never omit a company silently — every exclusion has a documented reason.
- **SIGNAL_REGISTRY** is append-only. Signals are never deleted; they may be superseded by newer signals.
- **CANDIDATE_REGISTRY** tracks state per candidate. A rejected candidate retains its evidence for audit.
- **QUALITY_UNIVERSE** membership can change as evidence accumulates. Each membership change records lineage.
- **CASE_REGISTRY** is the authoritative list of companies that entered full research. Once a case is opened, it persists (may be closed, but never deleted).

---

## 3. Three Independent Discovery Lanes

### Lane A — Quality-First

```text
Quality Discovery (deterministic structured sensors)
    → Quality Universe membership (VERIFIED/PROBABLE signal)
    → Wait for Dislocation (price, fundamental, or event)
    → Dislocation detected → Candidate Assembly
```

Best for: well-understood high-quality businesses with temporarily compressed valuations. The Quality Universe pre-filters so that when dislocation hits, triage is fast.

### Lane B — Dislocation-First

```text
Dislocation Radar (price anomalies, fundamental deterioration, event-driven signals)
    → Outside Quality Universe → Quick Quality Investigation
    → If quality signal sufficient → Candidate Assembly
    → If quality signal insufficient → WATCH_EVIDENCE or REJECT with documented reason
```

Best for: businesses not previously identified as high quality but where dislocation is severe enough to warrant investigation. Prevents quality-blindness.

### Lane C — External Discovery

```text
Radar Scout (non-authoritative, transitional — CAP-011)
Founder direction (entry_route = FOUNDER_DIRECTED)
Filings, competitors, suppliers, customers, regulators
Industry data, institutional data, external research
Other lawful public evidence
```

All external signals converge into the same canonical Signal Registry → Candidate Registry → downstream gates.

---

## 4. Selection States (Canonical)

Selection Engine is a **policy-governed service** — NOT an AI judgment role.

| State | Meaning | Next Action |
|-------|---------|-------------|
| `AUTO_RESEARCH_NOW` | Candidate passes all policy gates; case should open as capacity allows | Priority ordering → Capacity check → Case Open |
| `WATCH_PRICE` | Quality + impairment potential confirmed; waiting for better price | Set price threshold → re-evaluate on breach |
| `WATCH_EVIDENCE` | Quality plausible but evidence insufficient; needs more data | Set watch conditions → re-evaluate on new data |
| `DATA_LIMITED_WATCH` | Interesting but data too sparse for confident triage | Low priority; re-evaluate on cadence |
| `REJECT` | Does not meet policy criteria for QAD investigation | Record reason; may be re-evaluated on evidence change |

### Selection Engine Rules

- Selection Engine is a **deterministic, policy-governed service**. It applies approved thresholds and rules.
- AI judgment is NOT involved in selection state assignment (AI generates evidence; selection is rule-based).
- **Chief Underwriter must not select its own cases.** The Selection Engine and Chief Underwriter are separate functions.
- **Founder-directed cases** must be labeled `entry_route = FOUNDER_DIRECTED` and must not be counted as autonomous Discovery Recall.
- **No AI-invented rules:** all selection thresholds, weights, formulas must be approved by Founder as policy.

---

## 5. Candidate Assembly Flow

```text
Signal(s) from any lane
    │
    ▼
Signal Correlation & Deduplication
  (multiple signals may point to same company)
    │
    ▼
Evidence Light Check
  (minimum data requirements met?)
    │
    ▼
Candidate Record Created
  ├─ entity_id (reconciled to Security Master)
  ├─ signal_ids (references to Signal Registry)
  ├─ quality_flag (Quality Universe membership or quick QC pass)
  ├─ dislocation_flag (dislocation type and magnitude)
  ├─ entry_route (QUALITY_FIRST / DISLOCATION_FIRST / EXTERNAL / FOUNDER_DIRECTED)
  ├─ entry_timestamp
  ├─ evidence_freshness
  └─ current_selection_state
    │
    ▼
Selection Engine (policy applied)
    │
    ▼
Selection State assigned → registry updated → next action triggered
```

---

## 6. Hard Filters vs Soft Evidence

### Hard Exclusion ALLOWED only for:
- Non-operating investment vehicles (ETF, fund, trust)
- Preferred stock, warrants, derivatives (not common equity)
- Shell companies, pre-business SPACs
- Duplicate securities (same operating company, different share class)
- Unresolved entity identity
- No usable financial history / severe unrecoverable source insufficiency
- Other explicitly approved non-QAD security classes (Founder-approved list)

### Hard Exclusion FORBIDDEN (soft evidence only):
- ROIC > X, FCF margin > X, revenue growth > X
- Debt/EBITDA < X, P/E < X, margin > X
- Any quantitative quality threshold as automatic exclusion

These are ranking/evidence features ONLY, never automatic exclusions — unless future evaluation demonstrates an acceptable recall trade-off AND Founder approves the rule.

---

## 7. Data Architecture

```text
External Raw Data
    │
    ▼
Security / Entity Resolution  →  SECURITY_MASTER
    │
    ▼
Raw Source Archive  (immutable original documents)
    │
    ▼
Normalized Fact / Feature Layer  (structured from raw sources)
    │
    ├──► Quality Sensors  →  QUALITY_UNIVERSE signals
    ├──► Dislocation Sensors  →  DISLOCATION signals
    └──► External Signals  →  Radar / ecosystem signals
    │
    ▼
SIGNAL REGISTRY  (all signals, unified)
    │
    ▼
Candidate Assembly  →  CANDIDATE REGISTRY
    │
    ▼
Selection Engine  →  Selection State
    │
    ▼
CASE REGISTRY  (selected for research)
```

### Data Semantics

- **PIT timestamp** on every data point
- **Source + data version + transformation version + rule version + model version** on every derived value
- **Missing-data state** explicitly recorded
- **Data absence must never silently equal "no signal"** — absence is a distinct state from zero/normal

---

## 8. Cadence Model (Hybrid)

| Cadence | What | Who | Valid Null Output |
|---------|------|-----|-------------------|
| **Daily** (machine-first) | Price/corporate-action refresh, filings/events refresh, dislocation feature refresh, Quality-Universe change monitor | Deterministic + LLM delta inspection | Yes — no new signals is valid |
| **Weekly** (discovery cycle) | Full coverage: quality refresh, cross-sectional anomaly/dislocation scan, filing/event reconciliation, Scout external pass, candidate assembly, candidate-state update | Scheduled evaluation | `NO_NEW_MATERIAL_QAD_CANDIDATE` is valid |
| **Monthly** (coverage audit) | Eligible count, scanned %, stale %, unresolved identities, coverage gaps, exclusions, new listings/delistings, Quality churn, conversion rates. **Stratified Rejected Sample Audit** (50-100 sample) | Mandatory evaluation | Never — audit always produces a report |
| **Quarterly** (quality refresh) | Quality evidence/state dynamic; VERIFIED↔PROBABLE↔UNRESOLVED↔FAILED transitions with lineage | Scheduled review | No changes is valid |
| **Event-driven** | Material events trigger immediate evaluation | Automated | Urgency changes cadence, not evidence standards |
| **Founder On-Demand** | Founder nominates company/industry/geography/event | Founder | Founder-directed; not counted as autonomous recall |

### Research Initiation (State-Triggered, Not Quota-Cron)

```
candidate_state = AUTO_RESEARCH_NOW
    → Priority Ordering
    → Capacity Check
    → Research Budget Controller
    → Case Open
```

- Capacity full → explicit ready/watch queue with state, priority, expiry/freshness, reason
- Never open unlimited cases during a market-wide selloff
- Priority considers: quality confidence, dislocation materiality, price-vs-economic damage gap, researchability, balance-sheet survivability, evidence freshness, reducible uncertainty, research cost

---

## 9. Radar Scout Disposition (Transitional — CAP-011)

**Preserved from frozen requirement:**

| Permitted | Forbidden |
|-----------|-----------|
| Detect | ✅ Declare Quality | ❌ |
| Surface | ✅ Declare Temporary/Structural | ❌ |
| Connect | ✅ Value Company | ❌ |
| Raise Question | ✅ Write Final Thesis | ❌ |
| | Approve Selection | ❌ |
| | Allocate Budget | ❌ |
| | Recommend Trade | ❌ |

- Radar Scout is TRANSITIONAL (CAP-011). Not deleted, frozen, renamed, or cron-changed during M3–M4B.
- Function: non-authoritative complementary discovery — catches signals structured sensors find difficult (regulatory context, competitor/supplier/customer commentary, unusual filing context, industry developments, source-specific anomalies).
- Writes ONLY to Signal Registry / Candidate Registry intake layer.
- Retirement decision requires evidence: `Legacy Radar vs QAD Discovery incremental recall evaluation` after M5/M6.

---

## 10. Evaluation Mandate

The system must be evaluated on TWO distinct questions:

- **Type A:** Did it research the discovered company correctly? (Research Quality)
- **Type B:** Did it discover the company/opportunity at all? (Discovery Recall — first-class metric)

### Minimum Metrics (M4B Evaluation Contract)

- Universe Coverage Rate
- Data-Ready Coverage
- Known-Opportunity Recall
- Quality Candidate Recall
- Dislocation Detection Rate
- Signal-to-Candidate Conversion Rate
- Candidate-to-Research Conversion Rate
- Discovery Cost per New Candidate
- False Positive Rate (Material)
- Decision-Changing Candidate Recall (headline)
- Decision-Changing Evidence Recall

Threshold calibration belongs to M4B — not invented in M3.

<!-- 2026-08-19 11:45 UTC+7 -->