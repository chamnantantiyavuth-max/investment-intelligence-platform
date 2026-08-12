# DISC Child B — Equity Universe Coverage Assessment

**Task:** t_2d5a911b <br>
- Methodology anchor: IIN_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md
- Pilot constraints: bounded sample only, NO state change, no expansion, no new thresholds

## 1. The two universes

| Universe | Size | Definition |
|---|---|---|
| FO-8 core (FD #81/#88/#89) | 8 | AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, JNJ |
| Shared universe (equity_universe.py) | 98 | FO-8 + US large/mid-cap + 19 ADRs |
| Actual discovered universe | 12 | Union of all lanes' outputs |

## 2. Bounded sample — 12 discovered tickers: 12/12 IN the 98-name universe (100%), 8/12 FO-8, zero out-of-universe

Sample: APPL, ABBV, AMZN, BMY, GOOGL, JNJ, LLY, META, MSFT, NVDA, TSLA, VRTX (All in universe)

## 3. Coverage of the 98-name universe by lane

| Lane | Universe coverage | Evidence |
|---|---|---|
| E1 Radar EDGAR pass (FD #81) | 8/98 (8.2%) — FO-8 CIKs only | radar digests |
| E2 Inflection | 98/98 scanned (100%), but 30/98 NOT EVALUABLE | universe-scan JSON |
| E3 Quality & Asymmetry | 98/98 shadow-scanned, no production card path | shadow-evidence |
| Deep research | 6/98 (6.1%) | research/companies + reports |

## 4. Coverage gap classification (M1-M7)

| Class | Finding | Count | Status |
|---|---|---|---|
| M2 Data Miss (HEADLINE) | 30/98 (30.6%) NOT EVALUABLE in E2: 19/19 ADRs (100%) + 11 US names. Errors: 19× insufficient data, 11× HTTP 404 | 30 | CONFIRMED |
| M2 Data Miss (wiring) | E1 EDGAR pass watches only 8/98 CIKs – 90/98 names have no filing-level radar coverage | 90 | CONFIRMED |
| M1 Universe Miss | 0/12 out-of-universe discovered -> no observed M1 in sample, but counterfactual NOT RUN | 0 observed | NOT EVALUABLE with CURRENT DATA (requires §11 probe) |
| M7 Authority/Workflow Miss | E3 produced shadow evidence for 98 names but thresholds proposed (FD #53) – no authorized card path | 98 | CONFIRMED (structural) |
| M3 Detector Miss | 29/98 no signal, 56/98 stage-excluded — within-design filters; sample caught 4/4 candidates | 0 observed | NOT EVALUABLE beyond sample |
| M4 Judgment Miss | Radar equity output confined to FO-8; no non-universe equity surfaced | 0 observed | NOT EVALUABLE |
| M5 Cadence | not assessed — out of scope for child B | — | NOT ASSESSED |
| M6 Triage Miss | 4/4 E2 candidates flowed through CoS to research; radar equity cards processed | 0 observed | CONFIRMED no loss in sample |

## 5. Honest statement

- Universe identity layer: sound (deterministic, PIT-verified, all discovered activity within it).
- But universe ≠ evaluable universe: 30.6% of the 98 (every ADR + 11 US) cannot be evaluated by E2 with current data wiring (M2).
- E3 shadow lane has no production path (M7) - its 98-name evidence cannot become cards.
- M1 is UNMEASURED, not absent: the discovered universe now 100% in-universe is an artifact of universe-bounded scanning.

smallest recommended system change: bounded §1 counterfactual sample (10-15 eligible US/ADR names outside the 98) — audit-only, no expansion.

## 6. Sample denominator discipline (·6)

All percentages bounded by explicit denominators (12-ticker sample; 98-name scan; 19-name ADR layer). No universal recall claim made or implied.
