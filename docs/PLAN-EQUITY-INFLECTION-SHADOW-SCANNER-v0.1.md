# Plan — Equity Inflection Discovery: Shadow Scanner Implementation (Phase 0)

> Version: v0.1 · 10 Aug 2026 · Critical Mode (new module + financial signal logic, shadow-gated)
> Basis: FD #88 (FOUNDERS-DECISIONS item 104, 10 Aug 2026) + `design/equity-inflection-discovery/FIRST-PASS-v0.1.md` v0.2 (Approved Spec: Stage Definition v0.1 + revenue confirmation)
> Direction source: `ChatGPT/FOUNDER-DIRECTION-EQUITY-INFLECTION-DISCOVERY-AUDITED.md` (§18J validation plan)
> Status: **DRAFT — awaiting Founder approval (T0 gate). No implementation until approved.**

---

## 1. Goal

Implement the deterministic Equity Inflection Discovery scanner in **SHADOW mode**: compute candidates on current data WITHOUT consuming research capacity (no Task Idea Cards, no CoS load, no recon, no publication), producing a validation report the Founder reviews before any standing behavior.

## 2. Authority and Constraints

| Source | Rule |
|---|---|
| FD #88 (item 104) | Capability AUTHORIZED as research-intake; scanner SHADOW-gated until Founder approves validation evidence; no new role/cron/UI/schema |
| Direction §18J | Validation before threshold hardening: PIT historical validation, bias tests, hypothesis separation, false-positive/missed-opportunity review, capacity load, stability/sensitivity, honest empty-output |
| Approved Spec v0.2 | Stage Definition v0.1 (deterministic); breakout = EPS breakout + revenue confirmation; Stage 1 + Early Stage 2 only; late-2/3/4 excluded |
| FD #53 | No invented thresholds — every threshold PROPOSED, Founder-approved with evidence before production |
| FD #58 | Point-in-time discipline mandatory |
| FD #65 | Frozen pipelines stay frozen — legacy code reused as INFRASTRUCTURE only, never revived as a pipeline |
| FD #75 (rest) | All non-superseded parts stand: no momentum trading signals, radar discovery-only, no momentum conclusions |
| Constitution | Portfolio-blind §23.8.1; no broker/allocation/execution; deterministic/AI separation §23.3 |

## 3. Material vs Non-Material

| Item | Classification | Reason |
|---|---|---|
| New `discovery/equity-inflection/scanner.py` | **Material** (new capability, financial signal logic) | Requires named FD — granted by FD #88 (shadow scope only) |
| Locked/regular tests for scanner invariants | Material | New test surface; must not regress existing 145/145 |
| Shadow run + validation report | Non-material (no capacity consumed, no cards) | FD #88 explicit |
| Threshold values in Stage Def v0.1 | Material (FD #53) | PROPOSED only — approval deferred until validation evidence |
| No code change to frozen pipelines/adapters/frontend | Non-material | Scope lock |

## 4. Proposed Architecture (Shadow Phase)

```
discovery/equity-inflection/
├── scanner.py          # deterministic scanner (new)
├── README.md           # semantics, lineage, firewall contract (new)
├── output/             # shadow run results (committed as evidence)
└── tests/ → tests/test_equity_inflection_scanner.py   # invariants (new)

SHADOW FLOW (no cards, no recon, no CoS):
  Universe (FO-universe 8 first → expand ~100–300 liquid names)
    → fetch (reuse alpha-momentum-v0/source_adapter.py conventions — yfinance,
      split-adjusted; read-only, NEVER run_real.py)
    → EPS breakout H1 (TTM level) + H2 (YoY rate) — COMPUTED SEPARATELY
    → revenue confirmation (revenue not shrinking)
    → Stage signature (Stage Def v0.1: S1/S2/S3/S4 + early-S2 recency/extension)
    → liquidity sanity (price, volume, float proxy)
    → enrichment signals (RS percentile, volume trend, extension) — ADVISORY,
      never gating
    → candidate JSON + human-readable shadow report
    → Founder review (this session) → decide next validation phase
```

**Firewall (binding):** scanner output = deterministic evidence block ONLY. It NEVER creates a Task Idea Card, never enters CoS triage, never auto-loads into research first passes (FD #64 item 7), never publishes. Radar Scout remains the only packaging path (future standing behavior, NOT in this phase).

## 5. File-by-File Plan

| File | Action | Details |
|---|---|---|
| `discovery/equity-inflection/scanner.py` | NEW | Deterministic scanner: `fetch_universe()`, `earnings_breakout()`, `revenue_confirmation()`, `stage_signature()`, `liquidity_sanity()`, `enrichment()`, `run_shadow()`. All outputs carry as-of availability stamps (FD #58). No LLM calls anywhere in the scanner. |
| `discovery/equity-inflection/README.md` | NEW | EPS semantics explicit (GAAP diluted primary; adjusted never silently substituted — lineage preserved); hypothesis separation documented; firewall contract; boundaries; proposed-threshold status (FD #53). |
| `tests/test_equity_inflection_scanner.py` | NEW | Locked-style deterministic invariants: breakout math (H1 vs H2 computed independently), revenue-confirmation logic, stage classification against constructed price series (S1/S2 early/late/S3/S4 cases), empty-output honesty (insufficient data → no candidate, never fabricated), PIT stamp presence, enrichment-never-gates assertion. |
| `discovery/equity-inflection/output/` | NEW | Shadow run results committed as evidence (candidate JSON + report). |
| `docs/PLAN-EQUITY-INFLECTION-SHADOW-SCANNER-v0.1.md` | NEW | This plan. |
| Frozen pipelines (`alpha-momentum-v0/`, `fundamental-opportunity-v0/`, `institutional-intelligence-v0/`, `close_system/`) | **UNTOUCHED** | Infra reuse read-only only. |
| `backend/`, `frontend/`, `operational/hermes-organization/`, `reports/` | **UNTOUCHED** | Scope lock. |

## 6. Assumptions and Deferred

| ID | Assumption | Risk |
|---|---|---|
| A1 | yfinance earnings history + price data sufficient for shadow-phase signal computation | Free-data limits: no restatement history, no delisting coverage → PIT bar scaled to purpose (research intake, not trading calibration); documented honestly in the shadow report |
| A2 | FO-universe 8 names adequate first test set | Small N → signal behavior on broader universe unknown until Phase 1 expansion |
| A3 | Threshold values in Stage Def v0.1 (±5% bands, 15% extension, 8-week recency, 0.5%/month slope) usable as initial PROPOSED values | FD #53: these are NOT approved production thresholds; validation evidence required before any standing use |
| D1 | Catalyst Recon template (template 13) | DEFERRED — needed only at first real triage, not in shadow phase (SMART-SCOPE) |
| D2 | Historical PIT backtest infra | DEFERRED to validation Phase 1 (separate plan); shadow phase = current-data only |
| D3 | Estimate-revision / guidance signals | DEFERRED — data availability + PIT complexity unproven |

## 7. Approval Requested (T0 Gate)

| Step | What | Material |
|---|---|---|
| T0 | **Approve this plan** (file-by-file scope + shadow-only constraint + threshold-status honesty) | Yes — stops here until Founder approval |
| T1 | Locked tests RED (test file written first, fails against absent module) | Material |
| T2 | Data layer (reuse source_adapter conventions, as-of stamps) | Material |
| T3 | EPS breakout H1 + H2 computed separately | Material |
| T4 | Revenue confirmation | Material |
| T5 | Stage signature (Stage Def v0.1) | Material |
| T6 | Enrichment signals (advisory) | Material |
| T7 | Shadow run: FO-universe 8 first | Non-material |
| T8 | Shadow report to Founder (candidates, false-positive eyeball, capacity-load estimate) — NO cards | Non-material |
| T9 | Verification (pytest full suite no regression — baseline 145/145) + commit | Non-material |

**Explicit non-authorization (mirroring FD #88):** this plan does NOT authorize (a) standing production scanning, (b) any threshold becoming a hard gate, (c) Task Idea Cards / CoS intake from scanner output, (d) cron/automation, (e) radar contract changes, (f) blog/UI/schema changes, (g) reuse of legacy O'Neil/Minervini entry/exit/stop-loss/position-sizing rules. Each requires a separate named Founder Decision after validation evidence.

## 8. Verification Plan

| Feature | Verification |
|---|---|
| Scanner determinism | Same input → byte-identical candidate output (test) |
| Hypothesis separation | H1 level-breakout and H2 rate-acceleration computed and reported independently; no silent combination |
| Stage classification | Constructed price-series unit tests: S1, early-S2, late-S2, S3, S4 cases classify correctly per Stage Def v0.1 |
| Empty-output honesty | Insufficient/missing data → no candidate + explicit reason; never fabricated signal (test) |
| PIT discipline | Every computed signal carries as-of availability stamp (test presence) |
| Enrichment never gates | Test: candidate set unchanged when enrichment values vary (advisory-only assertion) |
| No regression | `python -m pytest -q` full suite = 145/145 baseline intact |
| Scope lock | `git status` shows ONLY the planned files; frozen dirs untouched; isolation-scan clean |

## 9. Next After This Phase

Founder reviews shadow report → decide: (a) proceed to validation Phase 1 (PIT historical validation plan — separate), (b) adjust signal/stage definitions, (c) expand universe, (d) stop. Standing production behavior and any threshold approval require a further named FD (FD #88).

<!-- 2026-08-10 12:20 UTC+7 -->
