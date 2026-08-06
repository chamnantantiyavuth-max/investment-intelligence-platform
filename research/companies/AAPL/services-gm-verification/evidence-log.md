# Apple Services Gross Margin — Evidence Log (ORG-2026-0010)

**Question (card):** Do Apple's newly disclosed Services sales and cost lines substantiate the previously unverified Services gross-margin claim (≈75.6% from the CRO buyback dissent), and how should tariff refunds and the absence of category-level operating expenses constrain its interpretation?
**Card:** ORG-2026-0010 (RADAR-001 round 2; 0011 share-count continuation FOLDED IN) · **Workspace:** research/companies/AAPL/services-gm-verification/
**Point-in-time rule (FD #58):** every figure valid only at its source date.

## Source register — Apple Q3 FY26 Form 10-Q (accession 0000320193-26-000020, filed 2026-07-31) + Q3 FY2026 release (published 2026-07-30)

Condensed consolidated statements of operations (in millions):

| Line | Q3 FY26 (2026-06-27) | Q3 FY25 (2025-06-28) | 9M FY26 | 9M FY25 |
|---|---|---|---|---|
| Net sales — Products | 78,678 | 66,613 | 272,629 | 233,287 |
| Net sales — Services | 30,739 | 27,423 | 91,728 | 80,408 |
| Total net sales | 109,417 | 94,036 | 364,357 | 313,695 |
| Cost of sales — Products | 47,153 | 43,620 | 163,810 | 147,097 |
| Cost of sales — Services | 7,494 | 6,698 | 21,765 | 19,738 |
| Total cost of sales | 54,647 | 50,318 | 185,575 | 166,835 |
| Gross margin | 54,770 | 43,718 | 178,782 | 146,860 |

Release disclosures (2026-07-30, apple.com/newsroom/2026/07/apple-reports-third-quarter-results/): total-company GM 50.1% incl. ~2pp FAVORABLE tariff-refund effect; diluted EPS $2.02 incl. $0.11 tariff-refund effect; revenue $109.4B.

## Derived Services gross margin (computed 2026-08-07)

- Q3 FY26: (30,739 − 7,494)/30,739 = 23,245/30,739 = **75.6205% ≈ 75.62%**
- Q3 FY25: (27,423 − 6,698)/27,423 = 20,725/27,423 = **75.5752% ≈ 75.58%**
- 9M FY26: (91,728 − 21,765)/91,728 = 69,963/91,728 = **76.2722% ≈ 76.27%**
- 9M FY25: (80,408 − 19,738)/80,408 = 60,670/80,408 = **75.4527% ≈ 75.45%**
- Q3 FY26 Products GM: (78,678 − 47,153)/78,678 = **40.0684% ≈ 40.1%**
- Total GM Q3 FY26: 54,770/109,417 = **50.0562% ≈ 50.1%** ✓ (matches disclosed 50.1%)

## The verification result (preliminary)

The disclosed segment cost lines SUBSTANTIATE the previously derived figures:
- The moat report's derived Services GM series (75.62% / 75.58% — `reports/apple-moat-2026-08-06.md`, "derived, path-dependent") is **exactly confirmed** by the 10-Q's disclosed Services cost of sales (Q3 FY26 75.6205%, Q3 FY25 75.5752%).
- The CRO buyback dissent's 75.6% Services GM claim (flagged "not source-cleared" in the buyback-mask cover note) is **substantiated** by the same lines.
- The claim is now directly source-cleared from Apple's own disclosures — no longer "derived".

## Interpretation constraints (must be in the note)

1. **No category-level operating expenses disclosed** → Services GM is a gross-margin figure; it does not measure Services profitability (marketing, R&D, G&A allocation not disclosed).
2. **Tariff-refund effect:** total-company GM 50.1% includes ~2pp favorable tariff refund; without it total GM ≈ 48.1%. The SEGMENT allocation of the tariff refund is NOT disclosed — Services GM 75.62% may embed an unknown tariff effect. The refund was ~$0.11 EPS.
3. **Services mix:** 9M FY26 Services revenue $91,728M = 25.2% of total ($364,357M); gross profit contribution = 69,963/178,782 = 39.1% (9M) — Services economics remain central to the moat thesis (42.2% of gross profit per the FY25-based moat report; 9M FY26 = 39.1%).
4. **Margin trend:** Services GM stable-to-rising (75.45% → 76.27% 9M YoY) — consistent with durable monetization, not deterioration.

## Bonus findings from the 10-Q (RADAR-001 round 2, Zone 2 — relevant to prior reports)

1. **NAND/DRAM + advanced semiconductor supply constraints CONFIRMED** in Item 1A risk factors: "supply constraints and increasing costs for components driven by factors such as industry supply-demand imbalances for components, including advanced semiconductors, storage (NAND) and memory (DRAM), which adversely affects the Company's ability to obtain sufficient quantities of components and products on commercially reasonable terms... The Company expects these trends to intensify." — **supports the CRO buyback dissent's memory-cost competing-claims evidence** (previously unverified).
2. **AI compute constraints CONFIRMED**: "Demand for cloud computing and artificial intelligence infrastructure has increased substantially... constrained supply, extended lead times, and increasing costs... reliance on third-party cloud service providers" — supports the AI-compute competing-claims evidence.
3. **Supreme Court granted cert** June 30, 2026 (Epic: legal standard for civil contempt) — the Ninth Circuit Dec-2025 ruling upheld the 2025 Injunction in part, allowed SOME commission on link-out, remanded; Apple petitioned May 21, 2026; cert granted June 30, 2026; stay sought. Regulatory path ACTIVE — relevant to the moat report's regulatory-erosion thesis.
4. **Share count (0011 folded):** 14,594,180,000 issued/outstanding as of 2026-07-17 vs 14,608,963,000 at 2026-06-27 (continued contraction; −14.8M in ~3 weeks) — consistent with the buyback mask staying operative.
5. DMA Article 6(4): preliminary findings April 23, 2025; no final determination yet (unchanged from prior reporting).

## Data gaps (named)

- Segment-level tariff-refund allocation (not disclosed)
- Category-level Services operating expenses (not disclosed)
- Services COGS composition (App Store vs advertising vs cloud vs licensing — not disclosed)
- Apple's own NAND/DRAM cost figures (dollar impact not quantified — risk factor is qualitative)

## Sources & limitations

Primary: Apple Q3 FY26 Form 10-Q (accession 0000320193-26-000020, filed 2026-07-31 — condensed consolidated statements, Item 1A risk factors, Item 2 repurchase table) — full text on disk (/tmp/apl-evidence/aapl-10q-q3fy26.txt, 10-Q Q3 FY26); Apple Q3 FY2026 release 2026-07-30. Analysis advisory-only, portfolio-blind — no price target, no buy/sell.

<!-- 2026-08-07 03:20 UTC+7 -->
