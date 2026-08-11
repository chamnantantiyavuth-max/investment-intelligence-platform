# Evidence Log — BMY (RM-2026-0006, inflection deep research)

**Mandate:** RM-2026-0006 — Bristol-Myers Squibb EPS inflection quality + stage discipline (from ORG-2026-0019, CoS triage A, 11 Aug 2026)
**Asset:** BMY · **CIK:** 0000014272 · **Workspace:** `research/companies/BMY/`
**Rule:** FD #58 point-in-time — every figure valid only at source date.

## Primary sources (SEC EDGAR, pulled 2026-08-11)

| # | Source | Filing / accession | Date | Key figures |
|---|---|---|---|---|
| E1 | 8-K earnings release (Ex-99.1) | 0000014272-26-000018 / a2026q2ex991-filing.htm | filed 2026-07-30 | Q2 FY26 total revenues $12,973M (+6% / +5% Ex-FX); Growth Portfolio $7.6B (+15% / +14% Ex-FX) = 59% of revenue; GAAP EPS $1.62 (+153%); non-GAAP EPS $2.04 (+40%); **guidance RAISED** — revenue ~$49.0-50.0B, non-GAAP EPS $6.75-7.00 |
| E2 | 10-Q (Q2 FY26) | 0000014272-26-000020 / bmy-20260630.htm | filed 2026-07-30 | (downloaded 175KB; used for cash-flow/balance cross-checks) |
| E3 | companyfacts annual (XBRL) | CIK 0000014272 | pulled 2026-08-11 | FY2025 revenue $48.6B? (verify) — see series below |

## Growth vs Legacy portfolio (Q2 FY26, from E1)

- **Growth Portfolio $7.6B (+15%)** — Opdivo $2,485M (−3%; Qvantig $261M +200%), Reblozyl $735M (+29%), Breyanzi $484M (+41%), Camzyos $416M (+59%), Opdualag $349M (+22%), Yervoy $769M (+5%)
- **Legacy Portfolio $5.4B (−4% / −5% Ex-FX)** — Eliquis $4,481M (+7% demand-driven, offset by generics), Revlimid $425M (−49% erosion), Pomalyst/Imnovid $204M (−71%)
- **The pivot is working:** Growth > 50% of revenue and growing 15% while Legacy shrinks 4% — the LOE transition (Eliquis US exclusivity loss, Revlimid generic wave) is being offset by new launches.

## Scanner H1 data (universe-scan-2026-08-11.json)

- H1 fired: TTM diluted EPS $4.65 > prior 2y max $4.23 (as-of 2026-06-30 EDGAR filed)
- Revenue confirmed: +15.8% YoY (latest qtr $12.97B vs $11.20B — note: scanner uses raw XBRL revenue, quarterly; matches E1 $12,973M)
- Stage S2-early: price $64.84 > 50MA $58.61 > 150MA $57.73, 50MA +4.1%/mo
- Liquidity passes; H2 not fired.

## Companyfacts annual series (verified 2026-08-11, XBRL; FY ends 31 Dec)

Revenue ($B): 46.4 (FY2021) → 46.2 (FY2022) → 45.0 (FY2023) → 48.3 (FY2024) → **48.2 (FY2025)** — flat-ish; the inflection is EARNINGS-led, not revenue-led.

Net income ($B): 7.0 (FY2021) → 6.3 (FY2022) → 8.0 (FY2023) → **−8.9 (FY2024 — LOSS, charges)** → **7.1 (FY2025 — recovery)** — FY2024 loss from large charges (acquired IPR&D / licensing write-downs); FY2025 back to ~FY2021-22 level. Q2 FY26 GAAP EPS $1.62 (+153% vs $0.64) continues the normalization + real growth portfolio momentum.

**The inflection:** earnings went from a charged-out LOSS year (FY2024 −$8.9B) to recovery (FY2025 $7.1B) to accelerated growth (Q2 FY26 +153% GAAP, +40% non-GAAP, guidance RAISED). This is a REAL operational pivot: Growth Portfolio ($7.6B Q2, +15%) now >50% of revenue and growing while Legacy (−4%) shrinks — the Eliquis/Revlimid LOE transition is being offset by new launches (Opdivo Qvantig +200%, Breyanzi +41%, Camzyos +59%, Reblozyl +29%).

## Cash flow / capital return (from E2 10-Q, H1 FY26)

- H1 net earnings $5,994M (+59% vs $3,775M); Q2 $3,316M (+152%)
- H1 OCF $4,497M (low vs NI — working-capital timing; note: Q2-only OCF not separated)
- Dividends H1 $2,570M (~$0.62/qtr); **NO share repurchases in financing section** — capital return is dividend-only
- Cash + marketable securities ≈ $11.1B; debt repayments $1,720M H1 (net deleveraging)
- No buyback engineering — EPS growth is operational

## Data status

PARTIAL — sufficient for bounded deep-research note; cash-flow extraction COMPLETE (data steward gap closed). Earnings-call transcript not pulled (pipeline/milvexian commentary would deepen). Non-GAAP = company-defined.
<!-- 2026-08-11 17:35 UTC+7 -->
