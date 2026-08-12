# DISC Child B — Equity Universe Coverage Assessment

**Task:** t_2d5a911b · **Assignee:** org-equity-analyst · **Date:** 2026-08-12
**Methodology anchor:** `investment-intelligence-platform/ChatGPT/Integration 12 Aug 2026/IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md`
**Pilot constraints honored:** bounded sample only · NO state change · NO universe expansion · NO new thresholds
**Sources (evidence, all read from repo):**
- `discovery/equity_universe.py` — 98-name universe, FO-8 subset (CIKs verified 2026-08-11)
- `discovery/equity_inflection/output/universe-scan-2026-08-11.json` — E2 full-universe scan (98 names)
- `discovery/quality_asymmetry/output/shadow-evidence-2026-08-11.json` + `payloads-2026-08-11.json` — E3 shadow run
- `operational/hermes-organization/kanban/cards/ORG-2026-*.yaml` (21 cards) + radar digests 2026-08-07/10 — E1 lane
- `research/companies/` + `reports/` — deep-research coverage

---

## 1. The two universes (definitional)

| Universe | Size | Definition |
|---|---|---|
| FO-8 core (FD #81/#88/#89) | 8 | AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, JNJ — CIK-verified, data-proven |
| Shared equity universe (`equity_universe.py`) | 98 | FO-8 + US large/mid-cap + 19 ADRs — deterministic membership (FD #53), PIT 2026-08-11 |
| **Actual discovered universe** (every ticker IIP touched) | **12 unique** | union of all lanes' outputs below |

**Verified:** FO-8 ⊂ 98 (8/8). All 12 discovered tickers ∈ 98 (12/12).

## 2. Bounded sample — 12 discovered tickers vs universe membership

| Ticker | In 98? | In FO-8? | Discovery lane(s) | Reached |
|---|---|---|---|---|
| AAPL | ✅ | ✅ | E1 radar (EDGAR), E2 scan, E3 shadow | deep research (multiple reports) |
| MSFT | ✅ | ✅ | E1 radar (EDGAR/CIW), E3 shadow | card pilot ORG-0001 |
| NVDA | ✅ | ✅ | E1 radar, E3 shadow | scan only (E2 no signal) |
| GOOGL | ✅ | ✅ | E1 radar → ORG-0017 card | CoS triage → equity note |
| AMZN | ✅ | ✅ | E1 radar, E3 shadow | digest note only |
| META | ✅ | ✅ | E1 radar, E3 shadow | digest note only |
| TSLA | ✅ | ✅ | E1 radar, E3 shadow | scan only |
| JNJ | ✅ | ✅ | E1 radar → ORG-0015 card | deep research (talc) |
| ABBV | ✅ | ❌ (non-FO-8) | E2 candidate ORG-0018 | deep research (full 11-stage) |
| BMY | ✅ | ❌ | E2 candidate ORG-0019 | deep research |
| LLY | ✅ | ❌ | E2 candidate ORG-0020 | deep research |
| VRTX | ✅ | ❌ | E2 candidate ORG-0021 | deep research |

**Sample results:**
- **12/12 in-universe (100%)** — no discovered ticker sits outside the 98.
- 8/12 are FO-8; 4/12 (ABBV, BMY, LLY, VRTX) are non-FO-8 universe names surfaced only by E2.
- 4/4 E2 candidates flowed cards → CoS → deep research (zero triage loss in sample).
- 6/12 reached deep research (AAPL, ABBV, BMY, JNJ, LLY, VRTX).

## 3. Coverage of the 98-name universe by lane (funnel)

| Lane | Universe coverage | Evidence |
|---|---|---|
| E1 Radar — EDGAR filings pass (FD #81) | **8/98 (8.2%)** — wired ONLY for FO-8 CIKs | radar digests; FO-universe wording |
| E1 Radar — open-ended web scan | opportunistic, FO-8-centric (standing: Apple) | digests 08-07/08-10 |
| E2 Equity Inflection — deterministic scan | **98/98 scanned (100%)**, but 30/98 NOT EVALUABLE (data) | universe-scan JSON |
| E3 Quality & Asymmetry — shadow | 98/98 shadow-scanned, **no production card path** | shadow-evidence + payloads |
| Deep research (downstream) | 6/98 (6.1%) | research/companies + reports |

**E2 gate attribution** (universe-scan 2026-08-11, n=98):
- 4 eligible (4.1%) → all carded (ORG-0018..21) → all researched
- 39 any-signal-fired → 35 killed downstream (mostly stage filter)
- 56 stage-not-eligible (of evaluable names) — largest funnel gate
- 29 no signal fired (of evaluable) — detector design
- **30 data-miss (30.6%) — NOT EVALUABLE WITH CURRENT DATA**

## 4. Coverage gap classification (miss taxonomy M1–M7)

| Class | Finding | Count / evidence | Status |
|---|---|---|---|
| **M2 — Data Miss** ⚠️ HEADLINE | **30/98 (30.6%) NOT EVALUABLE in E2**: **19/19 ADRs (100%: ASML, AZN, BABA, BHP, BP, HDB, INFY, NVO, NVS, PDD, RIO, SAP, SHEL, SNY, SONY, TM, TSM, UL, VOD)** + 11 US names (BRK-B, CRWD, DDOG, DE, GS, NET, ROP, SHOP, TMO, V, WFC). Errors: 19× `insufficient data (q=0, p=251)`, 11× `HTTP 404` (companyfacts fetch). | 30 | **CONFIRMED** — the entire ADR layer of the universe is structurally invisible to E2 |
| M2 — Data Miss (wiring) | E1 EDGAR pass monitors only 8/98 CIKs → 90/98 universe names have NO filing-level radar coverage | 90 | CONFIRMED (bounded by FD #81 scope) |
| **M1 — Universe Miss** | 0/12 discovered tickers out-of-universe → **no observed M1 in sample**. But deterministic lanes (E2/E3) are universe-bounded by construction — the counterfactual was NOT run. | 0 observed / unmeasured | **NOT EVALUABLE WITH CURRENT DATA** — requires §11 out-of-universe probe (bounded, separate sample) |
| **M7 — Authority / Workflow Miss** | E3 Quality & Asymmetry produced shadow evidence for 98 names but thresholds remain PROPOSED (FD #53) → no authorized card path. Coverage exists but is non-actionable. | 98 | CONFIRMED (structural) |
| M3 — Detector Miss | 29/98 no signal; 56/98 stage-excluded — within-design filters. Sample shows no missed inflection (4/4 candidates caught). Sensitivity of definitions beyond sample: not assessed. | 0 observed | NOT EVALUABLE beyond sample |
| M4 — Judgment Miss | Radar equity output confined to FO-8; no non-universe equity ever surfaced → no sample evidence of judgment miss | 0 observed | NOT EVALUABLE (radar coverage too narrow to test) |
| M5 — Cadence/Latency | not assessed — bounded sample excludes temporal probe | — | NOT ASSESSED (out of scope for child B) |
| M6 — Triage Miss | 4/4 E2 cards approved at CoS → research; radar equity cards 0015/0017 processed | 0 observed | CONFIRMED no loss in sample |

## 5. Honest coverage statement

- Universe identity layer (98 names, FO-8 core): **sound** — deterministic, PIT-verified, all discovered activity within it.
- But **universe ≠ evaluable universe**: 30.6% of the 98 (every ADR + 11 US names) cannot be evaluated by the only production deterministic scanner (E2) with current data wiring. This is a real M2 gap, not a judgment call.
- E1 filing-level radar covers 8/98 — the other 90 names are invisible to event-driven filing discovery (M2 wiring).
- E3 is a shadow lane with no production path (M7) — its 98-name evidence cannot become cards.
- **M1 is unmeasured, not absent.** The discovered universe being 100% in-universe is an artifact of universe-bounded scanning; the out-of-universe counterfactual (§11) is the missing probe. Smallest recommended system change: bounded §11 counterfactual sample (10–15 eligible US/ADR names outside the 98) — audit-only, no expansion.

## 6. Sample denominator discipline (methodology §6)

All percentages above are bounded by their explicit denominators (12-ticker discovered sample; 98-name universe scan; 19-name ADR layer). **No claim of universal opportunity recall is made or implied.**
