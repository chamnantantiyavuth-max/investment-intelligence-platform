# Apple Buyback Watch — Evidence Log (ORG-2026-0007)

**Question (card):** Is the 12% year-over-year decline in nine-month cash paid for repurchases merely settlement timing, or the start of a durable reduction in Apple's capital-return pace?
**Card:** ORG-2026-0007 (RADAR-001) · **Workspace:** research/companies/AAPL/buyback-watch/
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance.

## Source register

| # | Figure | Source | Date | Status |
|---|---|---|---|---|
| S1 | Q3 FY26 (ended 2026-06-27): revenue $109,417M (+16.4% YoY); net income $29,789M (+27.1%); diluted EPS $2.02 vs $1.57 (+28.7%) | FY26 Q3 10-Q (accession 0000320193-26-000020, filed 2026-07-31) | 2026-06-27 | VERIFIED (filing on disk, /tmp/apl-evidence/aapl-10q-q3fy26.txt) |
| S2 | 9M FY26: revenue $364,357M (+16.2%); net income $101,464M (+20.0%); diluted EPS $6.88 vs $5.62 (+22.4%) | same | 2026-06-27 | VERIFIED |
| S3 | 9M cash paid for repurchases: FY26 $62.094B vs FY25 $70.579B (derived −12.0%) | FY26 Q3 financial statements (cash-flow statement); radar pull | 2026-07-30 | VERIFIED (radar) — cash-flow line re-checked in evidence |
| S4 | Q3 FY26 share repurchase activity (Item 2): total 79,611K shares — May 2026 ASRs 26,468K; open market 26,920K @ $297.18 (May 3–30); open market 26,223K @ $296.18 (May 31–Jun 27) | FY26 Q3 10-Q Item 2 | 2026-06-27 | VERIFIED (filing on disk) |
| S5 | May 2026: new ASRs — up-front payments totaling $10.0B; delivery through Q4 FY26 | FY26 Q3 10-Q Item 2 note (2) | 2026-06-27 | VERIFIED |
| S6 | Authorization: May 1, 2025 $100B program — remaining $38.0B as of 2026-06-27; April 30, 2026 ADDITIONAL $100B program → total remaining $138.0B | FY26 Q3 10-Q Item 2 note (1) | 2026-06-27 | VERIFIED |
| S7 | Weighted avg basic shares: Q3 FY26 14,656,110K vs Q3 FY25 14,902,886K (−1.7% YoY); diluted 14,714,676K vs 14,948,179K (−1.6%) | same | 2026-06-27 | VERIFIED |
| S8 | Issued/outstanding: 14,608,963K (2026-06-27) vs 14,773,260K (2025-09-27) (−1.1%); 14,594,180K as of 2026-07-17 | same | 2026-07-17 | VERIFIED |
| S9 | FY2025 full-year cash paid for repurchases $90.7B = 81.4% of OCF (derived 90,711/111,482); FY21–25 ≈$438.6B; period-end shares −10.1% over FY21–25 | Apple FY2025 10-K + XBRL Company Facts (from published moat report) | 2026-08-06 | VERIFIED (prior pilot evidence) |
| S10 | CRO "buyback mask" claim: per-share resilience can outlast the organic economics funding it; April 2026 $100B program + $62.1B 9M FY26 cited | reports/apple-moat-opposing-2026-08-06.md | 2026-08-06 | VERIFIED (published claim under test) |
| S11 | Main essay caveat: cash-paid figure differs from 10-K Note 10 transaction value on settlement timing | reports/apple-moat-2026-08-06.md | 2026-08-06 | VERIFIED |

## Derived figures (arithmetic to re-run in cross-exam/audit)

- Q3 FY26 buyback spend estimate: $10.0B (ASR up-front) + 26,920K × $297.18 ≈ $7.998B + 26,223K × $296.18 ≈ $7.767B → ≈ $25.8B
- Q3 FY26 weighted basic share count −1.7% YoY → buyback contribution to EPS growth ≈ +1.7pp of the +28.7% (majority from revenue + margin, not buybacks)
- 9M FY26 cash paid $62.094B vs FY25 $70.579B = −$8.485B (−12.0%)
- Program capacity: $138.0B remaining (≈ 1.5× FY25 full-year spend)

## Draft findings (for cross-exam + audit)

- **F1 — Timing vs deceleration (core question):** The −12% 9M cash-paid decline is most plausibly ASR SETTLEMENT TIMING, not durable deceleration, as of Q3 FY26: (a) April 30, 2026 ADDITIONAL $100B authorization (S6) — programs expanded, not wound down; (b) May 2026 fresh $10B ASRs committing through Q4 FY26 (S5); (c) Q3 FY26 quarterly activity strong ≈ $25.8B incl. open market at ~$297/share (S4/S5/derived); (d) FY25 9M was inflated by heavy ASR settlements from the prior program (S9 context). Verdict: TIMING — but requires FY26 full-year confirmation (see watch items).
- **F2 — Buyback mask status (CRO claim test):** Mask still ON as of Q3 FY26 — shares still shrinking (S7/S8). But its contribution to the +28.7% EPS growth is modest (~+1.7pp of 28.7pp); the quarter's EPS growth was predominantly organic (revenue +16.4% + margin). The mask claim survives this quarter's test but is not strengthened; it neither falsifies nor confirms the CRO's compound-erosion thesis.
- **F3 — Watch items (what would change the verdict):** FY26 full-year cash paid vs FY25 $90.7B (a full-year number materially below ~$88-90B while authorization stays high would support deceleration); authorization remaining growth (if the $100B April 2026 program is used at prior pace, remaining should decline toward ~$100B by Q4 FY26); Q4 FY26 ASR settlement size; share-count trajectory in FY27 (flattening = mask thinning).
- **F4 — Caveat:** cash-paid ≠ Note 10 transaction value (S11) — settlement timing is the documented cause of divergence; the radar's −12% uses cash paid, the correct measure for the mask question but lagged.

## Data gaps (named)

- FY25 quarterly cash-paid split (to quantify how much of FY25 9M was ASR-settlement-heavy) — prior 10-Qs on disk? Not re-pulled this pass.
- Q4 FY26 ASR settlement amount — not yet reported (Q4 FY26 ends ~Sep 2026).
- Management commentary on buyback pace — earnings call transcript not re-pulled this pass.

## Sources & limitations

All figures from the FY26 Q3 10-Q (filing on disk, accession 0000320193-26-000020) unless noted; radar-derived S3 cross-checked against the cash-flow statement. Analysis is advisory-only, portfolio-blind — no valuation, no price target, no buy/sell.

<!-- 2026-08-06 21:20 UTC+7 -->
