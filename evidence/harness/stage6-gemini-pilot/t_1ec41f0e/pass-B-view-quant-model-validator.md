# DR REHEARSAL — S3 Independent Hermes Pass B — Quant & Model Validation View (AAPL)

**Rehearsal:** Gemini Deep Research v1.4 workflow — Apple rehearsal (PILOT-NONCANONICAL, calibration only, NOT new investment truth)
**Lane:** S3 — Independent Hermes Pass B (anti-anchoring) · Profile: org-quant-validator (Role 08 — Quant & Model Validator, research-Principal reviewer-side QA lens)
**Produced:** 2026-08-12 22:45 UTC+7
**Isolation statement:** This view was produced WITHOUT reading Hermes Pass A (S2) output, the Gemini lane (S4) output, or any prior first-pass view (`research/companies/AAPL/first-pass/*`, `deep-analysis-2026-08-09/*`). Sources admitted per S1 contract only (published case + SEC filings/XBRL workspace evidence + canonical Evidence Model). The published case report was read as an admitted source and its quantitative claims are the object of verification, not of adoption.
**Portfolio-blind:** no portfolio context received or processed. Advisory only.

---

## 1. Admitted sources used (input snapshot, SHA-256)

| Source | File | SHA-256 | PIT window |
|---|---|---|---|
| 10-K FY2025 | `apl-evidence/aapl-10k-fy2025.txt` (acc. 0000320193-25-000079) | `1d973ff69c666d3cc29cecbec42f3622f184726f1166249525e98292be31f2d7` | FY23–FY25 annual |
| 8-K Q3 FY26 (ex99.1) | `apl-evidence/aapl-8k-q3fy26-ex991.txt` (acc. 0000320193-26-000018) | `26c745f5f42e16161264c6b6a7ce38a2c7a11d944ca4fb6365fcc9d21dcc5224` | Q3 FY26 release |
| 10-Q Q3 FY26 | `apl-evidence/aapl-10q-q3fy26.txt` (acc. 0000320193-26-000020, filed 2026-07-31) | `1a993be97c297278333c630fed9c6faffb0348bfa6fadb36ba4702aabeee15df` | Q3 FY26 + 9M FY26 |
| 10-Q Q1 FY26 | `apl-upgrade/q1fy26-10q.txt` (acc. 0000320193-26-000006) | `e4d4e5104888f074c7866e7ccab4fc1f333341216f81248768b738bbf27f31db` | Q1 FY26 |
| 10-Q Q2 FY26 | `apl-upgrade/q2fy26-10q.txt` (acc. 0000320193-26-000013) | `800ce43256e7937a56bf5c3955bda01eabf08500707938a31034f6be2caa5ff2` | Q2 FY26 + 6M FY26 |
| XBRL company facts | `apl-evidence/aapl-xbrl-facts.json` (data.sec.gov CIK 0000320193) | `73a86c6aedc31f77cac2ea4df5f80f0b3bd7e6eb58bb4e01444fbedf3afb9c43` | FY21–FY25 annual core facts |
| Published case (admitted) | `reports/apple-deep-analysis-2026-08-09.md` | `eb47dbb5e245701addc999bdff899a917cceb1ac34cd79c876571a49e5915e92` | published 2026-08-09 |
| Evidence Model | `project-definition/EVIDENCE-MODEL.md` (v0.1) | admission rules: provenance, PIT, source independence | — |

All figures below are recomputed by me from the filings/XBRL above. Third-party transcript and market-share items (AlphaStreet, IDC, Counterpoint) were NOT used in this view — outside the S1 admitted filing evidence and not re-verifiable here.

---

## 2. Verification register — published-case quantitative claims re-derived from primary evidence

Legend: ✅ REPRODUCED (from admitted evidence) · ⚠️ REPRODUCED WITH CAVEAT · ❌ NOT REPRODUCED / CONTRADICTED · ⛔ NOT VERIFIABLE from admitted evidence

| # | Published-case claim (translated) | Recomputation (this pass, from filings/XBRL) | Verdict |
|---|---|---|---|
| V1 | FY25 revenue $416.2B; iPhone 50.4%, Services 26.2%, other products 23.4% | 416,161 ✓; 209,586/416,161 = **50.36%** ✓; 109,158/416,161 = **26.23%** ✓; 97,417/416,161 = **23.41%** ✓ [10-K] | ✅ |
| V2 | FY25 Products GM $112.9B @ 36.8%; Services $82.3B @ 75.4% — 42.2% of gross margin | (307,003−194,116) = 112,887 @ **36.77%**; (109,158−26,844) = 82,314 @ **75.41%**; 82,314/195,201 = **42.17%** [10-K] | ✅ |
| V3 | FY25 total GM 46.9% | 195,201/416,161 = **46.91%** [10-K] | ✅ |
| V4 | Americas 42.9%, Greater China 15.5% (down from 18.9% FY23) | 178,353/416,161 = **42.86%**; 64,377/416,161 = **15.47%**; FY23 GC 72,552/383,285 = **18.93%** [10-K Note 13] | ✅ |
| V5 | Greater China +22.4% y/y in Q3 FY26 (reversal) | 18,816/15,369 − 1 = **+22.43%** [10-Q Q3 Note 10] | ✅ |
| V6 | Q3 FY26 total GM 50.1% incl. ~2pp favorable tariff refunds | 54,770/109,417 = **50.06%**; 8-K: "50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds" ✓; 10-Q MD&A: refunds recorded "as a reduction of products cost of sales" ✓ | ✅ |
| V7 | Q3 FY26 Products GM 40.07%, Services GM 75.62% (computed from reported, not tax-adjusted) | Products: 31,525/78,678 = **40.07%** ✓; Services: 23,245/30,739 = **75.62%** ✓ — Apple's own MD&A discloses 40.1% / 75.6% for Q3, and notes refunds sit inside products GM | ✅ |
| V8 | Products GM 35.3→36.8% FY21–25 | FY23 **36.50%**, FY24 **37.18%**, FY25 **36.77%** verified from 10-K. FY21 ≈34.9%, FY22 ≈36.3% from XBRL COGS total minus estimated Services COGS — endpoints NOT directly verifiable from admitted 3-year window (segment COGS split is dimensioned, absent from companyfacts) | ⚠️ range verified FY23–25 only; FY21–22 endpoints by allocation, not direct |
| V9 | Services GM 69.7→75.4% FY21–25 | FY23 **70.83%**, FY24 **73.88%**, FY25 **75.41%** verified; FY21–22 same allocation caveat as V8 | ⚠️ |
| V10 | FCF/NI conversion FY21–25: 98/112/103/116/88.18% | (OCF−capex)/NI: 92,953/94,680=**98.18%**; 111,443/99,803=**111.66%**; 99,584/96,995=**102.67%**; 108,807/93,736=**116.08%**; 98,767/112,010=**88.18%** [XBRL + 10-K] | ✅ all five |
| V11 | FY24 ≈105% FCF/NI excluding Ireland State Aid $10.2B | (108,807−10,200)/93,736 = **105.2%** — arithmetic reproduces; the $10.2B Ireland figure itself is NOT in the FY25 10-K (FY24 event; FY24 tax cash paid 26,102 vs FY25 43,369 consistent with a large one-off FY24 payment) | ⚠️ arithmetic ✅, Ireland amount ⛔ |
| V12 | FY25 NI +19.50% vs OCF −5.73% (blocker to HIGH label) | 112,010/93,736−1 = **+19.50%**; 111,482/118,254−1 = **−5.73%** [10-K] | ✅ |
| V13 | Intangibles $11.093B→$21.334B (+92.32%), unexplained | 21,334 is the **Q2 FY26 10-Q** balance-sheet value @ 2026-03-28 (11,093 @ 2025-09-27 → **+92.32%** arithmetic correct). **The Q3 FY26 10-Q (the report's own stated evidence window) shows "Intangible assets, net" = 20,342 @ 2026-06-27 → +83.4% YTD, and −$992M QoQ** (21,334→20,342, consistent with ~$1B/qtr amortization and no new disclosed acquisition). | ❌ PIT-STALE: magnitude correct only for Q2; overstated vs the report's claimed Q3 evidence window |
| V14 | Buybacks FY25 $90.7B cash = 81.4% of OCF; FY21–25 cumulative $438.6B | 90,711 ✓; 90,711/111,482 = **81.37%** ✓; 85,971+89,402+77,550+94,949+90,711 = **438,583 ≈ $438.6B** ✓ [XBRL] | ✅ |
| V15 | Shares −10.1% FY21–25; −1.2% to 14.594B @ 2026-07-17 | 16,426,786K (2021-09-25) → 14,773,260K (2025-09-27) = **−10.07%** ✓ [XBRL]; 14,594,180/14,773,260−1 = **−1.21%** ✓ [10-Q Q3 cover] | ✅ |
| V16 | 9M FY26 buybacks −12.0% to $62.1B; OCF +43% to $117.0B; coverage 53% vs 86% | 62,094/70,579−1 = **−12.02%** ✓; 116,996/81,754−1 = **+43.10%** ✓; 62,094/116,996 = **53.07%** ✓; 70,579/81,754 = **86.33%** ✓ (9M FY25) [10-Q Q3] | ✅ |
| V17 | Q3 FY26 diluted EPS $2.02 +29% incl. $0.11 tariff refunds; EPS growth > NI growth by 1.6pp (EPS mask) | 29,789/14,714,676K = $2.024 ✓; +28.7% vs NI +27.1% → **+1.6pp** ✓ (reported EPS basis); exact-basis +29.1% vs +27.1% → +2.0pp; mechanism confirmed: share count −1.56% y/y | ✅ (mechanism); rounding basis noted |
| V18 | Cash+securities $146.5B Q3 FY26; new $100B program (Apr 30, 2026); $10B ASRs settle Q4 | 39,544+22,855+84,118 = **146,517** ✓; 10-Q Item 2: remaining availability $138.0B ($38.0B + $100B) ✓; ASRs "end in the fourth quarter of 2026" ✓ | ✅ |
| V19 | Q3 dividend $0.27/share (payable 2026-08-13) | 8-K ex99.1 ✓ | ✅ |
| V20 | R&D FY25 $34.6B | **34,550** ✓ [10-K] | ✅ |
| V21 | Q1 FY26 $143.8B +15.7%; iPhone 85,269 +23.3%; buybacks ~93M sh / ~$25B | 143,756 (+15.66%) ✓; 85,269/69,138−1 = **+23.33%** ✓; 92,894K sh ✓; May-2025 program utilized $25.2B, remaining $74.8B ✓ [10-Q Q1] | ✅ |
| V22 | Q2 FY26 $111.2B +16.6%; Services GM derived 76.68% | 111,184 (+16.59%) ✓; (30,976−7,224)/30,976 = **76.68%** ✓ [10-Q Q2] | ✅ |
| V23 | Regulatory/legal: €500M DMA fine + C&D; DOJ suit; Epic 2025 Injunction; 9th Cir. Dec 11 2025; SCOTUS cert Jun 30 2026; Google licensing at risk | All present verbatim in 10-Q Q3 Item 1 + Item 1A ✓ | ✅ |
| V24 | 6M FY26 buybacks 135M sh / $36B | 92,894+42,427 = **135,321K** ✓; $25.2B+$11.0B = **$36.2B** ✓ [10-Q Q1/Q2] | ✅ |
| V25 | Q3 FY26 cash EPS effect: diluted shares 14.7147B | 14,714,676K ✓ [10-Q Q3 Note 3] | ✅ |

**Register result: 21/25 fully reproduced, 3 caveated (V8/V9/V11), 1 point-in-time stale (V13).** No published figure was found arithmetically wrong on its own stated basis; the single material defect is the intangibles figure being Q2-dated inside a report claiming Q3 evidence (V13).

---

## 3. Independent findings (quant/model-validation lens)

### F1 — Intangibles: PIT defect + an unresolved XBRL-vs-10-Q reconciliation (MATERIAL, goes to S5)
- The case report's flagship "unexplained $11.1B→$21.3B (+92.32%)" flag uses the Q2 FY26 10-Q (2026-03-28) balance sheet. The Q3 FY26 10-Q, filed 2026-07-31 and inside the report's own evidence window, shows 20,342 @ 2026-06-27: **+83.4% YTD, −$992M QoQ**. The "unexplained build" thesis survives (no business-combination disclosure anywhere in the 10-Qs; Apple carries no goodwill line), but its magnitude is stale by one quarter and it misses the Q3 inflection (build paused, amortization dominating).
- **XBRL inconsistency (new, this pass):** XBRL `IntangibleAssetsNetExcludingGoodwill` = 13,301 (2025-09-27) → 25,797 (2026-03-28) → 25,417 (2026-06-27), which does NOT equal the 10-Q balance-sheet line (11,093 → 21,334 → 20,342) on any date; gap widens from ~$2.2B to ~$5.1B. Gross ex-goodwill intangibles per XBRL: 24,950 → 38,220 (+$13.3B YTD). One of the two series mislabels or misaggregates; a Data-Steward reconciliation item. Any downstream model using XBRL intangibles will compute a different (larger) build than one using the balance sheet.

### F2 — Earnings-quality regime: FY25 conversion break is real and getting worse in FY26
- FCF/NI 88.18% (FY25) is the 5-year low; FY26 YTD OCF is +43% while NI is +20% (101,464/84,544−1 = +20.0%) — the FY26 conversion re-accelerates, but the FY25 break is NOT explained by the admitted evidence: working capital swung −$25.2B (AR −6,682, other assets −9,197, other liabilities −11,076) and tax cash paid jumped 43,369 vs 26,102 (+$17.3B, the largest single swing). The case report's ADEQUATE (not HIGH) label is supportable; the FY25 tax-cash step is the under-discussed driver (FY25 effective tax rate fell to 15.6% while cash tax paid rose 66%).
- 9M FY26 tax cash 26,555 vs 37,332 prior-year (−29%) — FY26 conversion tailwind partly reverses the FY25 tax drag.

### F3 — Margin quality: Q3 FY26 margins are distorted, not inflected
- Products GM 40.07% (Q3) is the highest in the 5-yr window but includes tariff refunds recorded inside products COGS ("refunds received as a reduction of products cost of sales", 10-Q MD&A) plus "favorable ~2pp" total-GM impact per 8-K. Services GM 75.62% is FLAT y/y (75.6% vs 75.6% per Apple's own table) — the "Services margin inflection" narrative is NOT supported by Q3; the 9M 76.3% vs 75.5% (+0.8pp) is the only year-over-year improvement, and it is mix-driven per MD&A ("different mix of services").
- The refund allocation between Products and Services is undisclosed; the computed Services GM (75.62%) is therefore NOT refund-free (contrary to a possible reading of the report's "ไม่ได้ปรับภาษี" phrasing — correct, the category margins are not refund-adjusted, which is exactly why cross-period margin comparisons in Q3 FY26 are contaminated).

### F4 — Capital allocation: real slowdown in cash terms, timing caveat acknowledged
- 9M FY26 buyback coverage 53.1% vs 86.3% (9M FY25) is the steepest drop in the 5-yr+ series; even adding the full $10B ASR up-front (already inside the 62,094 via financing cash, settled shares in Q4), FY26 full-year buybacks project to ~$72–85B vs $90.7B FY25 — a genuine cash slowdown while OCF grows 43%. The report's "permanent slowdown not proven" framing is right (ASR settlement mechanics), but the run-rate evidence favors slowdown, not pause: Q1 92.9M sh, Q2 42.4M sh, Q3 79.6M sh.
- EPS-mask arithmetic confirmed (F17/V17): Q3 EPS growth exceeds NI growth by ~1.6–2.0pp on −1.56% y/y share count. Buyback optics persist after organic rent-growth slows — the mechanism is real, and 9M FY26 shows exactly this pattern at the margin level.

### F5 — Regime shift in the P&L: R&D is the hidden accelerant
- 9M FY26 R&D 34,035 vs 25,684 (+32.5%) — already ≈ FY25 full-year (34,550). FY25 R&D +10.1%. R&D intensity (R&D/revenue): FY25 8.3% → 9M FY26 9.3%. Meanwhile capex 9M FY26 6,799 vs 9,473 (−28.2%) with the AI-compute risk factor citing "third-party cloud service providers" — i.e., AI compute cost is expensed through R&D/COGS, not capitalized. This is the clearest quantified signature of the AI transition in the admitted evidence, and it is NOT prominent in the case report's quant sections.
- Effective tax rate: Q3 FY26 17.9% vs FY25 15.6%; 9M FY26 17.6%. Rising tax rate is a mild earnings-quality drag going forward.

### F6 — Working-capital/seasonality posture
- Inventories 11,092 vs 5,718 (+94% y/y at Q3 end) — pre-launch build (consistent with the case's hardware-cycle framing; not a red flag on its own, but the largest single WC swing along with AR −21% (39,777→31,398, seasonal collection)).
- Other non-current liabilities +13,531 (41,549→55,080) is the largest liability-side move and is not explained by the admitted evidence (possible deferred-tax/refund/tariff items) — a second unresolved balance-sheet item alongside intangibles.

---

## 4. Robustness / regime checks (reviewer-side checklist, direction §6)

- **Sample selection:** 5 fiscal years (FY21–25) + 3 quarters FY26. FY21–22 segment-level GM endpoints not directly verifiable (dimensioned XBRL absent from admitted evidence) — the published 35.3% and 69.7% anchors should be re-derived from FY21/FY22 10-Ks before any forward use.
- **Look-ahead/survivorship:** none — single-company, point-in-time filings only; no price series used, no −2σ value-trap test possible (agree with report: INCONCLUSIVE is the only honest verdict on admitted evidence).
- **Regime dependence:** FY23 (53-week year) and the FY24 Ireland tax payment materially distort the FCF/NI series endpoints; the FY25 88.18% is not regime-broken but is the only non-distorted recent observation — high-weight it.
- **Lag structure:** OCF→FCF conversion uses same-period capex; capex is lumpy (FY25 +34.6% y/y) — the FY25 conversion dip is partly capex-timing, not pure quality deterioration.
- **Reproducibility:** all V1–V25 computations rerunnable from the hashed files above (§7). No code was changed to make a result pass.

---

## 5. Independent conclusions (quant dimension only)

1. **Earnings quality ADEQUATE is confirmed, not contradicted** — the FY25 FCF/NI break is real, tax-cash driven, and materially the same story the case reports; nothing in Q3 FY26 filings upgrades it to HIGH.
2. **The intangibles finding needs a §23.9-style correction at reconciliation:** current figure 20,342 @ 2026-06-27 (+83.4% YTD, −$992M QoQ), not 21,334 (+92.32%). Thesis unchanged; magnitude and trajectory differ.
3. **Services margin "resilience" is flat, not inflected** — Q3 Services GM 75.62% = y/y flat; the 9M +0.8pp is mix. Any rent-capture-crosion thesis must not rely on Q3 Services margin expansion.
4. **Capital-allocation quality remains INCONCLUSIVE** — the case's grade-withdrawal reasoning is arithmetically sound (no synchronized price test; 9M coverage collapse); the quant evidence now mildly favors "real slowdown" over "timing only".
5. **Valuation remains INDETERMINATE** — agreed: no synchronized price/valuation model exists in the admitted evidence; no quant addition possible or attempted.
6. **Two new reconciliation items for S5/Data Steward:** (a) XBRL vs 10-Q intangibles series divergence (~$2.2B→$5.1B, widening); (b) +$13.5B other non-current liabilities unexplained on admitted evidence.

## 6. Limitations of this pass

- FY21/FY22 segment GM endpoints and the $10.2B Ireland item not directly re-verifiable from admitted evidence (⛔ V8/V9/V11).
- Transcript claims (installed base 2.5B+, paid subs 1.5B+, Sept guidance +9–11%, "hundred-year flood", Broadcom $30B+) deliberately excluded — third-party, outside S1 filing evidence; the case report correctly labels them management statements.
- No price/multiple series → no valuation or −2σ testing possible; no opinion rendered.
- This is a rehearsal; nothing here is investment truth or a buy/sell/hold view.

## 7. Reproducibility appendix (exact commands)

```bash
# input hashes (snapshot above)
sha256sum <each file in §1>

# annual core facts (FY21–25), from aapl-xbrl-facts.json
python - <<'PY'
import json
d = json.load(open(r'C:\Users\Admin\AppData\Local\Temp\apl-evidence\aapl-xbrl-facts.json', encoding='utf-8'))
u = d['facts']['us-gaap']
for tag in ['NetIncomeLoss','NetCashProvidedByUsedInOperatingActivities',
            'PaymentsToAcquirePropertyPlantAndEquipment','PaymentsForRepurchaseOfCommonStock']:
    print(tag, {it['end'][:4]: it['val'] for it in u[tag]['units']['USD']
                if it.get('start') and it['end'].endswith(('09-25','09-28','09-30')) and
                (datetime.date.fromisoformat(it['end'])-datetime.date.fromisoformat(it['start'])).days in range(350,381)})
PY
# then FCF = OCF − capex; FCF/NI per year (V10), buyback totals (V14), share series (V15)

# 10-K/10-Q income statements: read the CONSOLIDATED/CONDENSED STATEMENTS OF OPERATIONS blocks
# (10-K lines 925–1057; 10-Q Q3 lines 1–5 of the statements block) — all V1–V25 numerators/denominators.
```

**Point-in-time stamps:** all figures valid at their filing dates (10-K FY25 filed 2025-10-31; Q1/Q2/Q3 FY26 10-Qs filed 2026-01-30 / 2026-05-01 / 2026-07-31; 8-K Q3 FY26 filed 2026-07-30). Per FD #58, re-verify against current sources before any forward use.

---
<!-- 2026-08-12 22:45 UTC+7 -->
