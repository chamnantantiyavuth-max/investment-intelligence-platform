# Evidence Log — ORG-2026-0016 (July 2026 LBMA Vault Print vs Squeeze Re-Pricing)

**Question:** Does the July 2026 LBMA London vault print — silver 907.059 Moz, the highest since the 2021 era and a new high for the 2023+ upswing, +16.6% YoY — landing during silver's sharpest weekly rally of the recovery leg (~+11%, to ~$64) further disconfirm the physical-liquidity-squeeze re-pricing (0006/0009/0013 convergence — "no visible scarcity signal as of 7 Aug"), and if so, what does that imply for the composition of the rally (positioning / reflation beta vs physical demand) and for the standing inventory-liquidity watch items (COMEX deliverable stocks, lease rates, available-stock vs gross-custody evidence)?

**Card:** ORG-2026-0016 (radar 2026-08-10 → CoS triage A 11 Aug → Research) · **Workspace:** research/commodities/SLV/july-vault-0016/
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance.
**Predecessors:** ORG-2026-0006 (silver deficit challenge, published) · ORG-2026-0009 (London vaults June watch, published) · ORG-2026-0013 (squeeze re-pricing test, published) — series convergence "no visible scarcity signal as of 7 Aug".

## Source register

| # | Figure | Source | Date | Status |
|---|---|---|---|---|
| S1 | Silver July 2026 = 907,058.963 koz (= 907.059 Moz); gold 306,526.611 koz (~9,534 t — re-derived 306,526,611 oz / 32,150.75 oz/t; card's "~9,533 t" was a loose round) | LBMA London Vault Holdings Data July 2026 (CDN xlsx — file SHA-256 `6360b53acc5f5d8ffe86294ed581ca829bfb952cfd59408af9cc2d54749913a4`, frozen in `raw/`) | 2026-08-13 download; data month-end 31 Jul 2026 | VERIFIED (re-parsed, arithmetic re-derived below) |
| S2 | Silver June 2026 = 902,843 koz (MoM base); July 2025 = 778,013 koz (YoY base) | S1 file, same extract | month-end Jun 2026 / Jul 2025 | VERIFIED |
| S3 | Gold June 2026 = 304,285 koz (MoM base); gold July 2025 = 285,015 koz (YoY base) | S1 file | month-end Jun 2026 / Jul 2025 | VERIFIED |
| S4 | Series peak silver 1,180,113 koz (2021-06); last month above 907.059 before Jul-26 = 2022-08 (916,497 koz) | S1 file, full series 2016-07..2026-07 (120 obs) | full history | VERIFIED |
| S5 | XAG spot 65.556; XAU spot 4,417.00 (spot ratio 67.38) | gold-api.com /price/XAG + /price/XAU | 2026-08-12 19:31 UTC | VERIFIED (pull) |
| S6 | SI=F closes: 57.67 (8/3) → 63.33 (8/7) → 65.74 (8/12); GC=F closes: 4,033.7 (8/3) → 4,340.7 (8/7) → 4,476.5 (8/12) | Yahoo Finance chart SI=F / GC=F | 2026-08-13 pull (daily closes) | VERIFIED (pull) |
| S7 | SLV Ounces in Trust 492,341,723.50 oz (= 492.342 Moz) | iShares SLV product page (Ounces in Trust field) | as of 2026-08-11 | VERIFIED (pull) |
| S8 | SLV 487.82 Moz (2026-08-06) — prior read in 0013 note; 8/6→8/11 delta = +4.52 Moz (+0.93%) | 0013 note SLV read + S7 | 2026-08-06 vs 2026-08-11 | RE-DERIVED from published figure + S7 |
| S9 | COMEX registered silver 99.8 Moz (+6.8 Moz/30d), eligible 234.8 Moz, total 334.6 Moz | metalcharts.org (third-party; CME primary IP-blocked) | 2026-08-06 | UNCHANGED from 0013/0014 (KNOWN-GAP; not re-pulled this pass) |
| S10 | Finimize 8/9: "Large speculators just hit a 2-year bullish extreme in silver" | Google News RSS secondary | 2026-08-09 | UNVERIFIED (CFTC primary 404 — known gap unchanged) |
| S11 | Radar claims for cross-check: +0.47% MoM / +16.6% YoY silver; +0.74% MoM / +7.6% YoY gold | Card ORG-2026-0016 radar_observation | 2026-08-10 | VERIFIED vs re-derivation (below) |

## Arithmetic re-derivation (mandatory — iip-evidence 38/38 pattern)

All from S1 raw koz figures; never trusted the summary numbers:

- Silver MoM: 907,058.963 / 902,843 − 1 = **+0.467%** (card claims +0.47% ✓)
- Silver YoY: 907,058.963 / 778,013 − 1 = **+16.587%** (card claims +16.6% ✓)
- Gold MoM: 306,526.611 / 304,285 − 1 = **+0.737%** (card claims +0.74% ✓)
- Gold YoY: 306,526.611 / 285,015 − 1 = **+7.549%** (card claims +7.6% ✓; base 285,015 koz read directly from extract row 2025-07)
- MoM delta silver: 907,058.963 − 902,843 = **+4,215.963 koz = +4.216 Moz**
- 2023+ upswing max before Jul-26: 902,843 (2026-06) → July 2026 (907,059) **exceeds → new upswing high ✓**
- "~5-year high / highest since 2021 era" claim: **IMPRECISE — precision correction** (see F1)

## Findings

- **F1 — Precision correction (FD #58), card title "~5-year high / highest since the 2021 era" is loose:** the full series shows silver was ABOVE 907.059 Moz continuously until 2022-08 (916.497 koz). Last month exceeding July-2026 level = **2022-08 → July 2026 is "highest since Aug 2022" = 47 months ≈ 3.9 years**, not ~5 years. It is also NOT a return to 2021-era levels (2021 monthly range 1,160–1,180 Moz). The precise claim: **new high for the 2023→2026 upswing; highest level since August 2022 (47 months); still ~23% below the 2021-era peak (1,180.1 Moz, 2021-06)**. Same class of error as the June "series high" framing corrected in the 8/10 digest — flag on every live surface.
- **F2 — Rally has EXTENDED past the card's snapshot:** card priced the 8/3→8/7 +9.8% week (57.67→63.33). Current: SI=F **65.74 (8/12 close, +14.0% vs 8/3)**; spot XAG 65.556; spot ratio **67.4** (vs ~69.1 on 8/3) — compression toward the ~65:1 median CONTINUED.
- **F3 — Gold caught up (ratio compression stalled then resumed):** 8/3→8/12: silver +14.0% vs gold +11.0% (GC=F 4,033.7→4,476.5). The 8/7 beta ≈1.4× narrowed to ≈1.27× over 8/3→8/12. Ratio 67.4 ≈ median neighborhood (~65) — consistent with normalization, not scarcity divergence.
- **F4 — SLV direction change (first visible accumulation of the rally):** 487.82 (8/6) → 492.34 Moz (8/11) = **+4.52 Moz (+0.93%)** — the 0013 "flat ETF flows" read has a first counter-signal. Small, but it is the first investor-absorption signal the series flagged as a watch item.
- **F5 — July print is month-end 31 Jul data; the rally ran 8/3 onward.** The July vault level PREDATES the sharpest weekly move (8/3–8/7) and its extension (8/8–8/12). It shows inventory at a multi-year high going INTO the rally — adverse to the depletion proxy — but does NOT measure what vaults did DURING the rally. The August print (~early Sep) is the true test of whether the rally drew visible inventory.

## Watch-item update (0006→0009→0013 standing list)

| Watch item | Status before (7 Aug) | Status now (13 Aug) | Read |
|---|---|---|---|
| LBMA London vaults (silver) | June 902.843 Moz — series-high read, adverse to depletion proxy | **July 907.059 Moz — new upswing high, highest since Aug 2022** | EXTENDS "no visible scarcity" with fresh official data ✓ RESOLVED for July |
| COMEX registered deliverable | 99.8 Moz (8/6, metalcharts 3P) | Unchanged — CME primary still IP-blocked | KNOWN-GAP unchanged |
| Silver lease rates | Not retrievable (free sources) | Not retrievable | KNOWN-GAP unchanged |
| Available-stock vs gross custody | Unresolved (CRO: gross ≠ free float) | Unresolved — July print is GROSS custody; free-float evidence still absent | UNRESOLVED — CRO dissent stands |
| ETF / SLV flows | Flat (487.82 Moz 8/6) | **+4.52 Moz to 492.34 Moz (8/11)** | FIRST direction change — watch for acceleration |
| Physical premiums | Not tracked this series | Not tracked | gap |
| CFTC COT positioning | Unverified (Finimize "2-yr bullish extreme") | Unverified (CFTC primary 404) | gap — feeds positioning-vs-physical question |

## Data gaps (named, not estimated)

- CME COMEX primary (403 IP-block) — third-party metalcharts 8/6 stands; no newer date.
- Silver lease rates — no free verifiable source; KNOWN-GAP.
- CFTC COT silver primary — all URL variants 404; Finimize 8/9 "2-year bullish extreme" UNVERIFIED.
- Free-float / available-stock evidence — absent (the CRO's standing point).
- Physical premiums (coin/bar vs paper) — not in this series' data.

## Freeze

- `raw/lbma-july-2026.xlsx` SHA-256: `6360b53acc5f5d8ffe86294ed581ca829bfb952cfd59408af9cc2d54749913a4` (frozen 2026-08-13 before analysis write-up)
- All figures above re-derived from that frozen file or the dated pulls listed.

<!-- 2026-08-13 02:40 UTC+7 -->
