# Evidence Log — ABBV (RM-2026-0005, inflection deep research)

**Mandate:** RM-2026-0005 — AbbVie EPS inflection quality + stage discipline (from ORG-2026-0018, CoS triage A, 11 Aug 2026)
**Asset:** ABBV · **CIK:** 0001551152 · **Workspace:** `research/companies/ABBV/`
**Rule:** FD #58 point-in-time — every figure valid only at source date; re-verify before reliance.

## Primary sources (SEC EDGAR, pulled 2026-08-11)

| # | Source | Filing / accession | Date | Key figures |
|---|---|---|---|---|
| E1 | 8-K earnings release (Ex-99.1) | 0001551152-26-000023 / abbv-20260630xexhibit991.htm | filed 2026-07-31 | Q2 FY26 GAAP diluted EPS $2.03 (+290.4% YoY); Adjusted diluted EPS $3.65 (+22.9%); Net revenues $16.990B (+10.2% reported / +9.5% operational); immunology $8.786B (+15.1%, Skyrizi $5.505B, Rinvoq $2.525B, Humira $756M); neuroscience $3.228B (+20.3%, Vraylar $1.071B, Botox Ther $1.042B); oncology $1.650B (−1.5%, Venclexta $771M, Imbruvica $532M, Elahere $211M); aesthetics $1.282B (+0.3%) |
| E2 | 10-Q (Q2 FY26) | 0001551152-26-000026 / abbv-20260630.htm | filed 2026-08-03 | H1 FY26 net earnings $4,313M vs $2,230M (H1 FY25) = +93.4%; Q2 net earnings $3,616M vs $941M = +284%; buyback ~$10M/quarter (treasury purchases); contingent consideration FV change $3,905M (H1) — non-cash, offsets; acquired IPR&D $1,035M H1; share count ~1.766B |
| E3 | 10-K (FY2025) | — | filed ~Feb 2026 | FY2025 revenue $61.2B; net income $4.2B (from EDGAR companyfacts annual, pulled 2026-08-11) |
| E4 | 8-K | 0001104659-26-091269 | 2026-08-05 | — (debt-related) |
| E5 | 424B5 ×2 / FWP | 0001104659-26-092114 etc. | 2026-08-04/05/06 | Debt offering activity (August 2026) — capital structure watch |

## EDGAR companyfacts annual series (pulled 2026-08-11, XBRL; fiscal year ends 31 Dec)

Revenue ($B): 45.8 (FY2020) → 56.2 (FY2021) → 58.1 (FY2022) → **54.3 (FY2023)** → 56.3 (FY2024) → **61.2 (FY2025)** — Humira erosion bottomed FY2023; FY2024 +3.7%, FY2025 +8.7% (Skyrizi/Rinvoq/neuro growth re-accelerating).

Net income ($B): 11.5 (FY2021) → 11.8 (FY2022) → **4.9 (FY2023)** → 4.3 (FY2024) → **4.2 (FY2025)** — depressed 3 years running by IPR&D/charges (e.g. $1,035M H1 FY26 IPR&D + contingent-consideration swings); NOT the clean run-rate.

**The inflection:** H1 FY26 net earnings $4,313M ≈ FY2025 FULL YEAR $4.2B — the earnings base was artificially depressed; Q2 FY26 GAAP EPS $2.03 vs $0.52 (Q2 FY25) = +290% is a LOW-BASE effect + real immunology growth, not a step-change in the underlying franchise. Adjusted EPS $3.65 (+22.9%) is the cleaner growth signal.

## H1 inflection scanner data (universe-scan-2026-08-11.json)

- H1 fired: TTM diluted EPS $3.54 > prior 2y max $3.00 (as-of 2026-06-30 EDGAR filed)
- Revenue confirmed: +10.2% YoY (latest qtr $16.99B vs $15.42B)
- Stage S2-early: price $247.97 > 50MA $240.71 > 150MA $222.39, 50MA +8.3%/mo, 150MA +2.4%/mo; close 8/10
- Liquidity passes. H2 not fired (hypothesis separation).

## Known gaps (honest)

- FY25 10-K full text not re-pulled this session (annual figures from companyfacts XBRL — reliable for revenue/NI but not segment detail beyond E1)
- Apogee acquisition (announced 7/31) — deal terms not yet in filings (8-K/A pending); guidance includes −$0.14 dilution
- Q2 FY26 cash flow statement details: OCF $19.0B TTM; contingent consideration swings $3.9B non-cash — EPS quality needs the adjusted view (Adjusted EPS $3.65 is the cleaner run-rate)
- No earnings-call transcript pulled (segment growth rates are reported-basis; operational 9.5% stated in release)

## Data status

PARTIAL — sufficient for a bounded deep-research note; segment detail + FY25 10-K would deepen. All figures date-stamped per FD #58.

## Reconciliation note (red-team A3, resolved 2026-08-11)

FY2025 revenue discrepancy (XBRL $61.2B vs red-team segment-sum ~$56-57B) RESOLVED: XBRL `Revenues` FY2025 (2025-01-01→2025-12-31, $61.2B, filed 2026-02-20) confirmed by both `Revenues` and `RevenueFromContractWithCustomerExcludingAssessedTax` tags; 10-Q confirms H1 FY26 $31,992M (Q1 ~$15.0B + Q2 $17.0B, both +~10-11% YoY). Segment sum in red-team view omitted Other/All-Other revenue — **$61.2B stands as FY2025 revenue**.
<!-- 2026-08-11 16:35 UTC+7 -->
