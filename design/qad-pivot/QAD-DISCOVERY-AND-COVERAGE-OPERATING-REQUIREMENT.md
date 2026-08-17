# QAD Discovery & Coverage Operating Requirement

> **Status:** APPROVED (M1 correction closeout, FD #130 — 2026-08-17). M1 = PASS.
> **Nature:** First-class production operating requirement for the QAD Discovery subsystem. Binds M3 (`QAD-DISCOVERY-AND-SELECTION.md` — the M3 contract must materialize this as a complete Discovery & Coverage Operating System, not a ranking/screener document) and M4B (Evaluation Contract — Part 7 Discovery & Coverage Evaluation).
> **Non-goal:** NOT permission to begin production implementation. M5 remains gated by the M5-IMPLEMENTATION-GATE.md evidence package.
> **Version:** 0.1 (2026-08-17)

---

## B1 — Core Principle (Frozen Doctrine)

> **Every eligible company must be observable by the system; not every company must be reasoned about by an LLM.**

Large-universe sensing uses deterministic/structured/cheap computation first. Expensive reasoning is progressively introduced only as candidate count falls. An LLM that reads thousands of companies individually is NOT the primary global scanner.

## B2 — Universe Layers (Six Registries)

| # | Registry | Content |
|---|----------|---------|
| 1 | `SECURITY_MASTER` | Every known security: issuer, exchange listing, share class, ADR, dual listing, ticker changes, corporate actions, delisting |
| 2 | `RESEARCHABLE_UNIVERSE` | Researchable operating companies; explicit inclusion/exclusion state + reason per company; no silent omissions; identity reconciled per Security Master |
| 3 | `SIGNAL_REGISTRY` | All detected anomalies/dislocations/quality signals with provenance (who/when/why/data version/rule version/model version/evidence) |
| 4 | `CANDIDATE_REGISTRY` | Companies that passed signal assembly into candidates; candidate state + priority + evidence freshness |
| 5 | `QUALITY_UNIVERSE` | Companies with accumulated evidence of high quality; membership does NOT require an active dislocation (DNA-017) |
| 6 | `CASE_REGISTRY` | Companies that opened Full QAD Research |

Every transition records: who, when, why, data version, rule version, model version, evidence.

## B3 — Hard Filters vs Soft Evidence

**Hard exclusion ALLOWED only for:** non-operating investment vehicles (ETF/fund), preferred/warrant, shell/pre-business SPAC, duplicate securities, unresolved entity identity, no usable financial history / severe unrecoverable source insufficiency, other explicitly approved non-QAD security classes.

**Hard exclusion FORBIDDEN (soft evidence only):** ROIC > X, FCF margin > X, revenue growth > X, debt/EBITDA < X, P/E < X, margin > X — these are ranking/evidence features, never automatic exclusions, unless future evaluation demonstrates an acceptable recall trade-off AND Founder approves the rule.

## B4 — Independent Discovery Lanes

- **Lane A — Quality-First:** Quality Discovery → Quality Universe → wait for Dislocation
- **Lane B — Dislocation-First:** Dislocation detected outside Quality Universe → Quick Quality Investigation
- **Lane C — External Discovery:** Radar/Discovery Scout, Founder, filings, competitors, suppliers/customers, regulators, industry data, institutional data, external research, other lawful public evidence

All lanes converge into the same canonical Signal/Candidate Registry and downstream gates.

## B5 — Quality Discovery

Cheap structured indicators as candidate-detection features (signals, NOT proof of moat): long-run capital returns, incremental ROIC, FCF persistence/conversion, margin resilience, revenue resilience, balance-sheet durability, dilution, reinvestment behavior, other industry-appropriate measures.

Quality states: `VERIFIED / PROBABLE / UNRESOLVED / FAILED`. Quality Universe membership does NOT require an active dislocation.

## B6 — Dislocation Radar

Signal families: price/relative-performance dislocation; multiple/expectations compression; earnings/guidance revision; revenue/volume/price/mix deterioration; margin/FCF/ROIC anomalies; inventory/working-capital anomalies; management/governance events; regulation/litigation/recalls/cyber; industry demand/capacity/destocking/price-war shocks; competitor divergence; market narrative/prospective-damage signals where lawfully measurable.

Reported business deterioration is NOT required — a material market dislocation with largely intact current economics may still create a QAD candidate.

## B7 — Data Architecture

`External Raw Data → Security/Entity Resolution → Raw Source Archive → Normalized Fact/Feature Layer → Quality/Dislocation Sensors → Signal Registry → Candidate Registry → Gate Inputs`

Preserve: PIT timestamp, source, data version, transformation version, rule version, model version (when AI used), missing-data state. **Data absence must never silently equal "no signal."**

---

## PART C — Operating Cadence: Hybrid (Scheduled Sensing + Event-Driven + Founder On-Demand + State-Triggered Research)

No fixed quota ("Every Friday research top 3"). Full Research begins because a candidate crosses approved gates AND capacity exists.

- **C1 Daily:** machine-first sensing — price/corporate-action refresh, filings/events refresh, dislocation feature refresh, Quality-Universe change monitor, new/changed signals ONLY to downstream AI triage. LLM inspects deltas, not unchanged companies.
- **C2 Weekly Discovery Cycle:** full coverage cycle (quality feature refresh, cross-sectional anomaly/dislocation, filing/event reconciliation, Scout external pass, candidate assembly, candidate-state update, rejected/ignored rationale). Valid output may be `NO_NEW_MATERIAL_QAD_CANDIDATE`. Never create artificial work.
- **C3 Monthly Coverage & Rejection Audit (mandatory):** eligible count, scanned %, stale %, unresolved identities, coverage gaps, exclusions by reason, new listings/delistings, Quality Universe churn, Signal→Candidate conversion, Candidate→Research conversion, cost metrics. **Plus stratified/random Rejected Sample Audit** (sample 50–100 from rejected/low-rank and ask: "Did the discovery system miss a potentially material quality/dislocation candidate?").
- **C4 Quarterly / filing-triggered Quality refresh:** Quality evidence/state dynamic; VERIFIED→PROBABLE→UNRESOLVED→FAILED transitions with lineage.
- **C5 Event-driven:** material events trigger immediate candidate-state evaluation without waiting for cadence. **Urgency changes cadence, not evidence standards.**
- **C6 Founder On-Demand:** Founder may nominate company/industry/geography/event. Record `entry_route = FOUNDER_DIRECTED`; founder-directed cases must NOT be counted as autonomous Discovery Recall. Founder authority may force priority; evidence/quality/red-team/audit/PIT/publication standards remain intact.
- **C7 Research initiation = state-triggered, not quota-cron:** `candidate_state → AUTO_RESEARCH_NOW` → Priority Ordering → Capacity Check → Research Budget Controller → Case Open. Capacity full → explicit ready/watch queue with state, priority, expiry/freshness, reason. Never open unlimited cases during a market-wide selloff. Priority considers: quality confidence, dislocation materiality, price-vs-economic damage gap, researchability, balance-sheet survivability, evidence freshness, reducible uncertainty, research cost.

---

## PART D — Radar Scout Disposition

- `org-radar-scout` is NOT deleted, frozen, renamed, or cron-changed during M1–M4B. Monday weekly + Thursday mid-week jobs remain transitional discovery infrastructure with named authorization.
- Radar principle retained: **"Radar raises questions; it never answers them."**
- M3 defines Radar/Scout as a **non-authoritative complementary discovery capability** — not a QAD underwriting authority. Purpose: catch signals structured sensors find difficult (regulatory context, competitor/supplier/customer commentary, unusual filing context, industry developments, source-specific anomalies, other lawful public evidence).
- Writes ONLY to the Signal/Candidate intake layer.
- MAY NOT: classify Temporary vs Structural; determine Quality; value; write investment thesis; approve candidate selection; allocate research budget; recommend trades.
- **No pre-decided retirement after M5/M6.** Require an evidence-based migration decision: `Legacy Radar vs QAD Discovery incremental recall evaluation`. If Radar discovers material candidates/signals QAD Discovery misses → absorb/retain the function. Freeze only after comparative evidence shows no material incremental value or full reproduction elsewhere.
- Hermes workforce profile reframe remains deferred to the approved Workforce Migration Map.

---

## PART E — Discovery & Coverage Evaluation (M4B First-Class)

The system must be evaluated on TWO separate questions:
1. **Type A:** Did it research the discovered company correctly? (Research Quality — existing)
2. **Type B:** Did it discover the company/opportunity at all? (Discovery Recall — NEW, first-class)

Metrics (minimum — materialize in M4B Evaluation Contract Part 7):

- Universe Coverage Rate
- Data-Ready Coverage
- Known-Opportunity Recall
- Quality Candidate Recall
- Dislocation Recall
- False-Negative / Miss Rate
- Rejected-Item Surprise Rate
- Time-to-Detection
- Signal→Candidate precision/yield
- Candidate→Full-Research yield
- Cost per meaningful candidate
- Source/feed failure detection
- **Decision-Changing Candidate Recall** (headline): "Did the system ever see the company that later became a real QAD opportunity — before it was obvious?"

Include historical/masked/synthetic discovery fixtures where practical. Add discovery recall + rejected-item audit results to the future M5 Gate Evidence Package.

---

## PART F — Universe Size and Scale

- Do NOT freeze arbitrary global universe size in the Constitution.
- M3 defines a configurable universe policy.
- M5 pilot begins with a bounded but broad researchable universe sufficient to measure recall/cost/data quality — **initial engineering target ~5,000–10,000 researchable operating companies**, subject to data-provider coverage and M4B/M5 evaluation. Quality Universe may initially target hundreds, calibrated empirically.
- Expansion depends on: universe coverage, false-negative evidence, data quality, signal volume, cost, operational capacity.
- Avoid both extremes: tiny founder-curated universe (blind spots) vs uncontrolled global universe (noise/cost).

---

## Scope Notes

- This document does NOT reopen the QAD architecture. Architecture remains frozen per ARCHITECTURE-DESIGN-GATE-FINAL.md.
- Discovery/Coverage instructions are requirements to be materialized in M3 contracts + M4B evaluation — NOT permission to begin production implementation.
- M2 (Logical Legacy Boundary) remains next; do not begin M2 until M1 = PASS.

<!-- 2026-08-17 17:30 UTC+7 -->