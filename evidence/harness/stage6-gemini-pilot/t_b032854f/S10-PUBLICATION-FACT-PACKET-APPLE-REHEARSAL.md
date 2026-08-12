# S10 — PUBLICATION FACT PACKET (FACTS LOCKED)
## Gemini Deep Research v1.4 — Apple Rehearsal (PILOT-NONCANONICAL)

**Task:** t_b032854f — [DR][CHILD] S10 — Facts Locked + Publication Fact Packet
**Author:** org-ic-secretary (Investment Committee Secretary — Managing Editor / Publication Controller, handoff §17)
**Date:** 2026-08-12 23:45 UTC+7
**Mode:** PILOT-NONCANONICAL — calibration rehearsal of the v1.4 workflow on a **published** Apple case. **NOT investment truth.** No domain-state change. Portfolio-blind. Advisory only — no recommendation, no buy/sell/hold view, no target price.
**Anchor contract:** `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md` §15 (Publication Fact Packet — mandatory logical handoff), §16 (Gemini Thai editorial role), §18 (F1 token fidelity), §19 (Thai Publication Quality Gate P1–P5)
**Upstream (Facts-Locked inputs):** corrected main essay (S6, `3496b06e…`) + canonical CRO (S8, `b59ecd57…`) + S5 reconciliation (`15861e87…`) + three frozen first passes (Pass A `80e88c9a…`, Pass B `f0ecb972…`, Gemini content `ce5a9226…`) + S9 re-audit verdict (CLEAN, `bc3ffeb0…`)
**Downstream:** S11 — Gemini Thai Editorial A/B (t_5ac2b6a4) · synthesis parent (t_68d2824b)
**Status:** ══ FACTS LOCKED ══ — this packet is the **only analytical state** the editorial writer may rely on, plus specifically selected supporting primary sources (§16).

---

## 0. GATE DECLARATION — FACTS LOCKED (F1 Token Fidelity)

**Facts Locked gate = PASS.** All financial facts frozen at the corrected-essay + canonical-CRO state, verified by the S9 re-audit (PASS CLEAN — all 5 S7 findings F1–F5 closed; §23.9 discipline satisfied; no new claims; no numeric-token drift; frozen-pass fidelity preserved).

### 0.1 Facts-Locked artifact registry (SHA-256 verified on disk 2026-08-12 23:40 UTC+7)

| Artifact | File | SHA-256 | Status |
|---|---|---|---|
| Corrected main essay | `attachments/t_32b3949c/S6-MAIN-ESSAY-APPLE-REHEARSAL-CORRECTED.md` | `3496b06e522447163f308f37eb1bbcaa57cefeca4e9e4d2eae202805aaf2adc2` | ✅ LOCKED |
| Original essay (untouched, §23.9) | `attachments/t_7ac2d383/S6-MAIN-ESSAY-APPLE-REHEARSAL.md` | `9f29f189aa7a95f136075ee005be1947685c3d7f911518c7d843dee5c20e66f8` | ✅ preserved |
| Canonical CRO opposing thesis | `attachments/t_295cacba/S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL_1.md` | `b59ecd57a5fb5d499833e19969a994de1f95c7e16701c6694b20025ae6286bc1` | ✅ LOCKED |
| ⚠️ Corrupted CRO duplicate — **MUST NOT USE** | `attachments/t_295cacba/S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL.md` | `5bd25094…` (encoding defects §13/§12/FIRY-PASS/salready) | ❌ excluded |
| S5 reconciliation | `attachments/t_a7021f89/S5-RECONCILIATION-APPLE-REHEARSAL.md` | `15861e87a6be41d59cdba0fc7a4f1058885b9a03d8946719a61d9ae65c570703` | ✅ LOCKED |
| Frozen Pass A | `attachments/t_7ad3552a/pass-a-view.md` | `80e88c9a0cc1b7286aafe7c7084b932ba33597889c006416660dfe2c7187d74e` | ✅ FROZEN |
| Frozen Pass B | `attachments/t_1ec41f0e/pass-B-view-quant-model-validator.md` | `f0ecb9721169df1dbe52bb2cfbd2fa50cbbb12256e31145d558a2b5203cc139f` | ✅ FROZEN |
| Gemini lane (content) | `attachments/t_079e1330/S4-GEMINI-VIEW-FROZEN.md` (wrapper `fa976b62…`) | content `ce5a92262fb8611a9759ccfe36a59d7077e2ee820ee01534775065d2acf42dc0` | ✅ FROZEN |
| S9 re-audit verdict | `attachments/t_91eceed5/S9-REAUDIT-VERDICT-APPLE-REHEARSAL.md` | `bc3ffeb0…` | ✅ CLEAN |
| Corrections record | `attachments/t_32b3949c/CORRECTIONS-RECORD.md` | `4b45e226…` | ✅ complete |

### 0.2 F1 token-fidelity verification (performed at this gate)

- **~99 token checks** executed at S10: every financial figure, date, and derived metric locked in §13 below was transcribed verbatim from the corrected essay and/or canonical CRO, then machine-verified present in the facts-locked sources (essay / CRO / S5 / frozen passes). **0 failures.**
- Upstream arithmetic integrity: S7 hostile cross-exam re-derived **38/38 arithmetic checks PASS** on the original essay; S9 confirmed the correction diff touched **zero numeric tokens** (12 line-changes, C1–C5 + namespace + timestamp only) → all 38 checks remain valid on the corrected essay.
- Superseded-token handling verified: `21,334` appears in the essay **only** in superseded/must-not-use flagging context (4 occurrences, all negative references — S9 §3); `refund-adjusted` = **0** occurrences (C1 closed).
- Frozen-pass integrity re-verified at S9: Pass A / Pass B / Gemini / S5 hashes exact — none altered.

### 0.3 No-new-claims declaration

This packet is a **derived logical contract**: it adds **zero** new factual, causal, financial, competitive, or investment claims beyond the corrected essay + canonical CRO + frozen passes. Every entry in §§3–13 carries its lineage (essay section, CRO section, S5 row ID, and/or pass reference). Nothing is averaged, upgraded, downgraded, or inferred beyond the locked sources. Any figure not found in the locked sources was **excluded** (verified by token sweep).

### 0.4 Freeze discipline

Facts Locked is a freeze point. Further changes to the essay/CRO (if any later stage requires them) must follow §23.9: new artifact + CORRECTIONS-RECORD, never overwrite. The editorial writer must not "fix" or "improve" any locked token.

---

## 1. RESEARCH IDENTITY

| Field | Value |
|---|---|
| **Subject** | Apple Inc. (AAPL) — moat durability assessment |
| **Scope** | Filing-verified business & financial foundation; moat mechanics (six dimensions); converged primary threat + divergent vectors (D1–D6); capital-allocation and valuation **context only** |
| **RESEARCH_AS_OF** | 2026-08-12 (filing/quote timestamps per pass) |
| **Point-in-time (FD #58)** | Figures valid at filing dates: 10-K FY25 filed 2025-10-31 · Q1 FY26 10-Q filed 2026-01-30 · Q2 FY26 10-Q filed 2026-05-01 · Q3 FY26 10-Q filed 2026-07-31 · Q3 FY26 8-K furnished 2026-07-30. Re-verify before any forward use. |
| **Analytical horizon** | Structural moat durability / break-vector assessment (medium-to-long term). NOT a valuation, timing, or portfolio recommendation. |
| **Mode** | PILOT-NONCANONICAL — calibration rehearsal on a published case; **NOT investment truth**; portfolio-blind; advisory only |
| **Evidence classes** | **[F]** filing-verified · **[D]** derived metric (formula in source pass) · **[M]** management claim (issuer-reported, not independently verified) · **[3P]** third-party claim **pending §12 admission** · **[A]** analyst assessment (labeled; not evidence) |
| **Citation namespaces** | **G-Dim1…6** = Gemini moat dimensions · **D1–D6** = S5 material disagreements · **G1–G10** = S5 Gemini-only rows (pending §12) · **V1–V25** = Pass B verification register · **A1–A5 / B1–B8 / C1–C2 / E1–E6 / N1–N4** = S5 agreement-map rows |

---

## 2. CENTRAL FINDING

**Lead thesis (S6 — locked, with CRO challenge below):** Apple's moat is **durable but conditional — "bent, not broken"** (converged assessment, A+G) [A4]. The FY26 financials are objectively strong: Q3 FY26 revenue $109.4B (+16% y/y), diluted EPS $2.02 (+29%, incl. $0.11 tariff refund), gross margin 50.1% (incl. ~2pp tariff refunds) [F] [A1]; FY25 revenue $416.16B (+6%), net income $112.01B, ~$62B net cash [F] [B1, B3]. The business is **not in financial distress by any filing-visible measure** [A] [A VIEW 4, VIEW 9].

The single highest-conviction convergence of the whole reconciliation is the **threat ranking**, not the financials: **AI-interface disintermediation** — the "dumb-pipe" scenario in which a third-party intelligence layer becomes the consumer's primary interface and the iOS ecosystem's routing/monetization layer is bypassed — is Pass A's risk #1 and Gemini's thesis-killer #3, derived independently from different evidence bases [A5, D6]. Services is 25.2% of 9M FY26 revenue and carries a structurally higher margin — that is the value at risk [D] [A VIEW 8].

Confidence (locked): **HIGH** on balance-sheet resilience · **MEDIUM** on reported economics (24/25 reproduced-or-caveated + 1 PIT-stale (V13), 0 contradicted) · **LOW-MEDIUM** on moat-mechanism durability [A] [A VIEW 9].

**CRO dissent (locked — must remain visible, §9):** S6's lead thesis is **wrong in its ranking and too confident in its "bent, not broken" framing.** Primary break mechanism = **present-tense regulatory/commercial profit-pool erosion at the monetization layer** (already in disclosed legal motion [F], requires no consumer defection); AI-interface disintermediation ranks second (higher severity, behavioral transmission unobserved). Confidence must follow the moat mechanism (LOW-MEDIUM), not liquidity (HIGH). [CRO Dissent Preserved]

---

## 3. MATERIAL CLAIMS (authorized for publication — each maps to evidence lineage)

Atomic thesis-bearing claims the editorial writer MAY assert. **Class [F]/[D] = can be stated as fact; [3P] = must be attributed as third-party-reported, pending admission; [A] = must be framed as assessment.**

| # | Material claim | Class | Lineage |
|---|---|---|---|
| M1 | Apple's moat is durable but conditional — "bent, not broken" | [A+G] | Essay §2.7; S5 A4 |
| M2 | FY26 financials are objectively strong; no filing-visible financial distress | [F]+[A] | Essay Exec./§1; S5 A1/B1; A VIEW 4, VIEW 9 |
| M3 | The converged #1 moat-break vector is AI-interface disintermediation ("dumb pipe") | [A+G] | Essay §3; S5 A5/D6; A risk #1 ≈ G thesis-killer #3 |
| M4 | Services (25.2% of 9M FY26 revenue) is the highest-margin value at risk | [D] | Essay §1.3/§3; S5 A5; A VIEW 8; CRO |
| M5 | Regulatory opening of the monetization layer is a filing-verified, present-tense pressure (DMA fine, DOJ suit, Epic injunction, 9th Cir., SCOTUS cert, Google-licensing risk) | [F] | Essay §2.1/§4.1; S5 A3/B V23; CRO Mechanism A |
| M6 | CRO dissents: profit-pool erosion (not user defection) is the primary break; AI disintermediation is second | [A] | CRO §Dissent Preserved; S8 Principal Verdict |
| M7 | Q3 FY26 gross margin 50.1% includes ~2pp tariff refunds; ex-refund ≈48.1% — cross-period margin comparisons contaminated | [F]+[D] | Essay §1.3; S5 A2/B F3 |
| M8 | Intangibles $20,342M @ 2026-06-27 (+83.4% YTD, −$992M QoQ) — the Q3-dated corrected figure | [F] | Essay §1.4/§2.5; S5 B2/N3/V13 |
| M9 | Balance sheet is a fortress: cash+securities $146.5B, debt $84.3B, net cash ≈$62B | [F]+[D] | Essay §1.4; S5 B3; B V18 |
| M10 | Buyback run-rate favors a real slowdown (9M FY26 coverage 53.1% vs 86.3%), not a pause | [F]+[A] | Essay §5.1; S5 E4/N1; B F4 |
| M11 | AI compute is being expensed (R&D +32.5% ≈ FY25 full-year; capex −28.2%) — the clearest quantified signature of the AI transition in the packet | [F]+[A] | Essay §1.5/§2.4; S5 E3; B F5 |
| M12 | Moat behavioral mechanisms (switching costs, network effects) are real but not quantified in filings — durability is inferred, not proven | [F]+[A] | Essay §2 intro; S5; A VIEW 5 |
| M13 | Third-party break magnitudes (DRAM +400%, NAND +300%, BoM +$300; CEO transition 2026-09-01; Q4 GM guide 47–48%) are **unadmitted** — direction only is filing-supported | [3P] | Essay §4.2–4.3; S5 D1/D3/D4, G1–G3 |

**Boundary:** claims M1–M13 are the complete authorized claim set. The editorial writer may rephrase but must not alter meaning (F2 semantic fidelity), and must not introduce any other factual/causal/financial/competitive claim.

---

## 4. VERIFIED FACTS (admitted through IIP evidence rules — [F] filing-verified unless noted)

All $B unless stated. Every figure locked verbatim from the corrected essay (facts-locked artifact); lineage per S5 agreement map + pass rows.

### 4.1 Headline FY26 — Q3 and 9M (filing-verified [F])
- **Q3 FY26:** revenue **$109.4B (+16%)**; net income **$29.789B**; diluted EPS **$2.02 (+29%, incl. ~$0.11 tariff refund)**; diluted shares **14.7147B**; gross margin **50.1% (incl. ~2pp tariff refunds recorded as reduction of products cost of sales)**.
- **Q3 FY26 segments:** iPhone **+21.7% to $54.25B** · Mac **+28.6% to $10.35B** · Services **+12.1% to $30.74B** · iPad **−5.9%** · Wearables/Home/Accessories **+6.5%** · every geographic segment double-digit (CEO statement, [M]).
- **9M FY26:** revenue **$364.36B (+16.2% vs $313.70B)**; operating income **$122.43B (+21.7%)**; net income **$101.46B (+20.0%)**; diluted EPS **$6.88 (+22.4%)**.
- **Product mix 9M FY26:** iPhone **$196.52B (53.9%, +22.4%)** · Services **$91.73B (25.2%, +14.1%)** · Wearables $27.28B (+2.3%) · Mac $27.14B (+8.6%) · iPad $21.70B (+3.0%).

### 4.2 FY25 and the five-year series (filing-verified [F] [B1; A VIEW 2])
| Metric | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|
| Revenue | 365.82 | 394.33 | 383.29 | 391.04 | **416.16** |
| Gross profit | 152.84 | 170.78 | 169.15 | 180.68 | 195.20 |
| Operating income | 108.95 | 119.44 | 114.30 | 123.22 | **133.05** |
| Net income | 94.68 | 99.80 | 97.00 | 93.74 | **112.01** |
| Operating cash flow | 104.04 | 122.15 | 110.54 | 118.25 | **111.48** |
| Capex | 11.09 | 10.71 | 10.96 | 9.45 | **12.71** |
| R&D | 21.91 | 26.25 | 29.91 | 31.37 | **34.55** |
- FY25 margins (derived): GM 46.9%, OI% 32.0%, NI% 26.9% [D]. Five-year revenue CAGR ≈3.3% [D] — the FY26 acceleration is a sharp departure from that trend.
- FY25 geographic mix: Americas $178.35B (42.9%) · Europe $111.03B (26.7%) · Greater China $64.38B (15.5%) · Japan $28.70B (6.9%) · Rest of Asia Pacific $33.70B (8.1%) [F] [B7].

### 4.3 Balance sheet Q3 FY26 (filing-verified [F] [B3; A VIEW 4])
- Total assets **$383.27B**; shareholders' equity **$107.52B** (vs $73.73B FY25-end; retained earnings swing −$14.26B → +$11.33B, largely tariff/tax-related — flagged, not fully reconciled).
- Cash+securities **$146.5B** (cash $39.54B + ST securities $22.86B + LT securities $84.12B); total debt **$84.3B** (current term debt $11.01B + non-current $71.34B + commercial paper $2.00B) → **net cash ≈$62B (derived)**; cash+securities cover debt ~1.7×.
- **Flag 1 — Inventory +94%:** $11.09B at Q3 FY26 vs $5.72B at FY25-end — largest working-capital swing; cause undetermined from filings (tariff pre-buy vs AI-infrastructure build vs new-product ramp are all hypotheses) [A] [B F6].
- **Flag 2 — Intangibles (corrected):** "Intangible assets, net" **$20,342M @ 2026-06-27 = +83.4% YTD, −$992M QoQ** (vs $11,093M @ 2025-09-27) [F] [B2, N3]. +$9.25B build with no disclosed business-combination in the 10-Qs; acquisitions or capitalized internal-use software are working hypotheses [A] [A VIEW 9, B F1]. **The Q2-stale $21,334M (+92.32%) is superseded and must not be used** [B V13, N3].
- Negative working-capital model: AP $64.53B ≫ AR $31.40B + inventory [F] [A VIEW 4].
- Deferred revenue $9.54B vs $9.06B FY25-end (+5%) [F].
- Open items (Data Steward, out of publication scope): XBRL intangibles series divergence (E1, 13,301→25,417 vs 10-Q 11,093→20,342, gap $2.2B→$5.1B); other non-current liabilities +$13.5B (41,549→55,080) (E2).

### 4.4 Capital allocation (filing-verified [F] [B4, B V14/V15, A VIEW 3])
- FY25 repurchases $89.3B (statement-of-shareholders'-equity line) / $90,711M (cash-flow line — same event, different statement bases, **not** a contradiction) [N4]; FY21–25 cumulative buybacks **$438.6B**.
- New **$100B authorization (May 2025)**; **$10B ASRs settle in Q4 FY26**.
- Dividends raised $0.25→$0.26 (May 2025) → **$0.27 (Q3 FY26, payable 2026-08-13)**.
- Shares **−10.07% FY21–25** (16.4268B → 14.7733B); −1.1% in 9M FY26 (to 14.609B); 14.59418B @ 2026-07-17.

### 4.5 Margin structure (filing-verified + derived)
- FY25 GM 46.9%; 5-yr GM range 44.1% (FY23) → 46.2% (FY24) → 46.9% (FY25) [F] [B1].
- Q3 FY26 GM 50.1% incl. ~2pp tariff refunds; **ex-refund ≈48.1% (derived)** [F]+[D] [A2, B V6/F3].
- Q3 Products GM **40.07%** — highest in the 5-yr window, **refund-contaminated** (B F3 framing) [F] [B F3].
- Services GM: Q3 FY26 **75.62% — flat y/y**; 9M **76.3% vs 75.5% (+0.8pp, mix-driven per MD&A, not an inflection)** [F] [E5, B F3/V7].
- Derived CoS ratios: Services CoS ≈ **23.7%** of Services revenue vs Products CoS ≈ **60.1%** [D] [A VIEW 6].
- FY25 Services: **42.17% of gross profit at 75.41% GM** [D] [B V2; CRO].

### 4.6 Earnings quality (filing-verified)
- FY25 **FCF/NI 88.18% — the 5-yr low** (FY21–25: 98.18 / 111.66 / 102.67 / 116.08 / 88.18) [F] [B V10, E6].
- FY25 net income +19.5% while OCF −5.7% — the structural break [F] [B V12].
- Cash taxes: FY25 $43,369M vs $26,102M (**+$17.3B, +66%**) while ETR **fell to 15.6%** (FY24 24.1% incl. a large one-time charge; Q3 FY26 17.9%; 9M FY26 17.6%); 9M FY26 cash tax $26,555M vs $37,332M (**−29%**) — a FY26 conversion tailwind [F] [E6, B F2].
- 9M FY26 OCF **+43.1%** vs NI +20.0% — conversion re-accelerates [F] [B V16, F2].
- **R&D is the hidden accelerant:** 9M FY26 R&D **$34,035M (+32.5%)** ≈ FY25 full-year ($34,550M); R&D intensity 8.3% → 9.3% while capex fell **−28.2%** (9M FY26 $6,799M vs $9,473M); AI-compute risk-factor disclosure names third-party cloud providers → AI compute cost expensed through R&D/COGS, not capitalized [F] [E3, B F5].
- Earnings-quality grade: **ADEQUATE, not upgraded to HIGH** [A] [B §5.1].

### 4.7 Regulatory — filing-verified set (verbatim in Q3 FY26 10-Q Item 1/1A) [F] [B V23; A3; CRO]
- €500M DMA fine + cease-and-desist direction; DOJ suit; Epic 2025 injunction (temporarily bars commissions on external payment links); 9th Cir. action dated **2025-12-11**; SCOTUS certiorari development dated **2026-06-30**; Google-licensing risk. Direction is filing-verified; specific fee mechanics (Core Technology Commission 5% on promoted digital sales from 2026-01-01; Tier-2 opt-out 30% → 5–17%; €0.50/install CTF replacement) are third-party [3P].

### 4.8 Valuation context — price-implies only (advisory, no recommendation) [D] [A VIEW 7]
- Market (2026-08-12): price **$301.08**; 52-week range **$223.78–$344.57**; diluted shares ~14.75B → market cap ≈ **$4.44T (derived)**.
- Price-implies (coarse, analyst-scenario): P/E ~39.6× on FY25 NI; ~33× on 9M-FY26 annualized NI (~$135B derived); dividend yield ~0.36%; buyback yield ~2%. Market embeds durable mid-teens EPS growth + continued buyback — demanding vs FY21–25's ~4% NI CAGR [A].

---

## 5. VERIFIED CALCULATIONS (material derived metrics + approved interpretation)

| # | Calculation | Formula / basis | Result | Approved interpretation (locked) |
|---|---|---|---|---|
| C-01 | FY25 FCF | OCF 111.48 − capex 12.71 | **~$98.8B** | Strong absolute FCF; but FCF/NI 88.18% is the 5-yr low — cash conversion weakened in FY25 |
| C-02 | Net cash | cash+sec 146.5 − debt 84.3 | **≈$62B** | Fortress liquidity; drives HIGH balance-sheet-resilience confidence (must NOT be used to certify moat durability — CRO inversion) |
| C-03 | Q3 ex-refund GM | 50.1% − ~2pp refund | **≈48.1%** | Q3 50.1% is NOT a clean read on margin trend; refund-contaminated |
| C-04 | Q3 Products GM | 40.07% (filing) | **40.07%** | Highest in 5-yr window but refund-contaminated — provides no clean margin read (B F3; C1-closed framing) |
| C-05 | Services mix | 91.73 / 364.36 9M | **25.2%** | The margin-dense layer at risk; value at risk under disintermediation/regulation |
| C-06 | Services gross-profit share | FY25: 42.17% of gross profit @ 75.41% GM | **42.17% (FY25)** | FY25-derived [D]; 9M "~40%+" is an analyst estimate (CRO-1 advisory) — do not present 9M share as filing-derived |
| C-07 | Buyback coverage | repurchases / OCF | **53.1% (9M FY26) vs 86.3% (9M FY25)** | Steepest drop in 5+ years; run-rate favors real slowdown (ASR-timing caveat acknowledged) |
| C-08 | Market cap | 301.08 × ~14.75B | **≈$4.44T** | Price-implies context only; embeds demanding growth expectations |
| C-09 | Valuation multiples | P/E | **~39.6× FY25 / ~33× annualized** | Context only — no DCF/comparators/margin-of-safety attempted (valuation contracts not approved) |
| C-10 | R&D intensity | R&D / revenue | **8.3% → 9.3%** | R&D +32.5% ≈ FY25 full-year while capex −28.2% → AI compute expensed, not capitalized |
| C-11 | 5-yr revenue CAGR | FY21–FY25 | **≈3.3%** | FY26 +16% is a sharp departure from trend — do not extrapolate trend from FY26 alone |
| C-12 | Greater China rebound | Q3 FY26 y/y | **+22.4%** | After −8% (FY24) / −4% (FY25); growth is promotion/discount-driven while Huawei leads premium (C1) |

**Boundary:** these are the only derived metrics authorized for publication. The writer may re-derive them arithmetically but must not change the numbers or their approved interpretation.

---

## 6. CAUSAL CHAIN (locked — cause → business mechanism → financial manifestation → investment relevance)

**Chain 1 — AI-interface disintermediation (lead threat, converged A+G) [A5, D6]**
cause: third-party intelligence layer (assistant/search/agent) becomes the consumer's primary interface
→ business mechanism: OS/app-layer routing function of the ecosystem is bypassed ("dumb pipe")
→ financial manifestation: Apple's ability to extract rent from developers and Services erodes; Services (25.2% of 9M revenue, structurally higher margin) is the value at risk
→ investment relevance: moat economics degrade even while revenue/balance sheet look strong; response quality (all-new Siri at WWDC26) not assessable from filings [M]

**Chain 2 — Regulatory/commercial profit-pool erosion (CRO primary break) [F, V23]**
cause: regulators/courts force changes to app distribution, payment routing, interoperability, search licensing (DMA fine, DOJ, Epic, 9th Cir., SCOTUS cert, Google-licensing risk — all in 10-Q)
→ business mechanism: monetization rights — not device abandonment — become the decisive variable; users need not leave iPhone for the profit pool to be redistributed
→ financial manifestation: Services 25.2% of 9M revenue, 42.17% of FY25 gross profit at ~75–76% GM — the margin-dense layer exposed; App Store take-rate mechanics under pressure (5–17% opt-out ranges, third-party)
→ investment relevance: moat can remain behaviorally sticky while becoming economically less exclusive — "bent, not broken" may be too reassuring; CRO ranks this #1 (present-tense, filing-verified) over AI disintermediation #2 (severity high, transmission unobserved)

**Chain 3 — AI compute expensed (E3, B F5)**
cause: AI transition requires massive compute; Apple sources via third-party cloud providers (Item 1A)
→ business mechanism: AI compute cost expensed through R&D/COGS instead of capitalized capex
→ financial manifestation: R&D +32.5% ≈ FY25 full-year while capex −28.2%; R&D intensity 8.3%→9.3%
→ investment relevance: the clearest quantified signature of the AI transition in the packet; margin structure under structural pressure

**Chain 4 — China margin-for-share (C1, B6)**
cause: Huawei premium leadership + price competition in China (third-party shares conflicting, never averaged)
→ business mechanism: Apple trades margin for share via promotions/discounts (up to CNY 2,000, third-party)
→ financial manifestation: Greater China revenue rebound +22.4% Q3 FY26 after two down years
→ investment relevance: China recovery quality is discount-driven; watch for mix/margin leakage

---

## 7. MATERIAL UNCERTAINTY (what is unresolved / not provable — must remain visible)

| # | Uncertainty | Status / class | Resolution path |
|---|---|---|---|
| U1 | Cause of +94% inventory build | Undetermined from filings [A] | Next-quarter filings; tariff pre-buy vs AI build vs new-product ramp |
| U2 | Nature/ROI of +$9.25B intangible increase | Acquisitions vs capitalized software — unknown [A] | Subsequent filings/notes; XBRL-vs-10-Q series divergence (E1) to Data Steward |
| U3 | Ex-refund sustainable GM | Needs next-quarter confirmation [A] | Q4 FY26 filings |
| U4 | +$13.5B other non-current liabilities | Unexplained on admitted evidence (E2) | Data Steward investigation |
| U5 | Behavioral moat evidence (churn, migration cost, developer surplus) | Absent from filings [F] | Not disclosed; durability inferred from price/margin persistence |
| U6 | iPhone unit vs ASP split | Revenue-only disclosure [F] | Unit disclosures absent |
| U7 | Regulatory proceedings detail (DMA status, SCOTUS cert outcome) | Outcomes unresolved [F] | Court/regulatory developments |
| U8 | **G1–G10 pending §12 admission** — Q4 GM guide 47–48%/~46.5% (D1); CEO transition 2026-09-01 (D3); DRAM +400%/NAND +300%/BoM +$300 (D4); June-2026 price hikes +6–25% (G4); Apple Intelligence ~410M DAU / 1.2T-param Gemini backend (G5); Google TAC ~$20B (G6); Vision Pro ~600K units/VPG disbanded (G7); China share ranges IDC vs Counterpoint `conflicting` (D5/G9-G10); refurb market (G8); HarmonyOS 70M (G9) | All third-party claims, **NOT filing evidence** [3P] | §12 source admission wave; until admitted they remain labeled third-party claims |
| U9 | Forward-GM and succession items | Transcripts `failed_retrieval` (S1) → management-claim-only | Q3 FY26 earnings-call transcript retrieval; DEF 14A extraction; 8-K Item 5.02 |
| U10 | D1–D6 weighting | Assessment-level disagreement, never averaged (§13) | No single wave resolves weighting — keep all vectors visible with evidence classes |

**Editorial requirement:** uncertainty U1–U10 must remain visible in the published piece (P1). The writer must not compress uncertainty into confidence.

---

## 8. MANAGEMENT CLAIMS (attributable to management, not independently verified [M])

| # | Claim | Source | Status |
|---|---|---|---|
| MC1 | All-new Siri AI at WWDC26; CEO framing of AI response | 8-K / management framing [M] | Recognized threat confirmed; response quality not assessable from filings [A] |
| MC2 | Installed base of active devices at an all-time high across all major categories/geographies | 8-K (issuer-reported) [M] | Not independent behavioral proof (CRO) |
| MC3 | Every geographic segment grew double-digit in Q3 FY26 | CEO statement [M] | Consistent with segment facts [F] |
| MC4 | Q4 FY26 GM guide 47–48% (incl. ~100bp tariff), normalized ~46.5%, ~280bp compression | Third-party call coverage [M/3P, D1] — transcripts `failed_retrieval` | **Management-claim-only; NOT filing-verified.** Must be labeled if used; Hermes passes contain no such item |
| MC5 | CEO transition Cook → Ternus 2026-09-01 | Third-party press [3P, D3] | Not in admitted filings; DEF 14A deliberately unextracted; **must be labeled third-party-reported** |

**Editorial requirement:** any MC item used in publication must carry the epistemic-phrasing distinction per §16 (e.g. ฝ่ายบริหารระบุว่า… / รายงานข่าวระบุว่า…) — never as filing-verified fact.

---

## 9. MATERIAL DISSENT (CRO/challenger positions — MUST remain visible, P1)

1. **Opposing thesis (verbatim core):** S6 mistakes financial resilience and residual user attachment for proof that the economic moat remains intact. The more probable break mechanism is already operating at the point where Apple converts ecosystem participation into high-margin rent: regulators and courts are forcing changes to app distribution, payment routing, interoperability, and search licensing [F]. Consumers need not leave iPhone for Apple's profit pool to be redistributed. The moat can remain behaviorally sticky while becoming economically less exclusive. "Bent, not broken" defines breakage as ecosystem desertion when the evidence supports a narrower, more immediate form of breakage — loss of control over the tollbooths inside an ecosystem users may continue to inhabit.
2. **Mechanism A — Profit-pool erosion is primary:** the filing-verified legal set (DMA €500M fine, DOJ, Epic injunction, 9th Cir. 2025-12-11, SCOTUS cert 2026-06-30, Google-licensing risk) is present-tense and requires no behavioral change; AI disintermediation requires an unobserved consumer-interface shift. Regulatory opening ranks #1; AI disintermediation #2.
3. **Mechanism B — "Convergence" is shared framing:** A and G share the same evidence universe, moat vocabulary, and no independent outcome measure — the convergence demonstrates salience/coherence, not frequency/timing/probability. Visibility ≠ probability.
4. **Sub-challenge C — Confidence inversion:** the thesis is a moat thesis, not a solvency thesis. HIGH confidence on liquidity must not govern the strength of the moat conclusion; LOW-MEDIUM on moat-mechanism durability should. A fortress balance sheet funds adaptation; it does not preserve exclusive high-margin monetization rights.
5. **Principal final dissent (owned, verbatim):** S6's lead thesis is wrong in its threat ordering and too confident in its "bent, not broken" framing. Regulatory/commercial profit-pool erosion at the monetization layer is the primary break mechanism — it is already in disclosed legal motion [F] and requires no consumer defection; AI-interface disintermediation ranks second (higher severity, unobserved behavioral transmission). Confidence must follow the moat mechanism (LOW-MEDIUM), not liquidity (HIGH).
6. **Supersession rule:** this dissent may be superseded **only** by the specified evidence path (U8/U9 admissions; Q4 FY26 filings; transcript/DEF 14A resolution; observed user-interface substitution data) — not softened by financial strength or narrative convergence.

**Editorial requirement:** the publication must present the CRO challenge fairly (P1 material-dissent preservation); the piece may lead with the converged thesis but must not hide the primary-break challenge or the confidence inversion.

---

## 10. REJECTED / SUPERSEDED CLAIMS (MUST NOT resurrect)

| # | Forbidden | Reason | Correct alternative |
|---|---|---|---|
| R1 | Intangibles $21,334M / +92.32% | Q2-stale (2026-03-28), superseded per B V13 | **$20,342M @ 2026-06-27 (+83.4% YTD, −$992M QoQ)** |
| R2 | Any averaged IDC/Counterpoint China share figure | Sources `conflicting` per S1 (D5); never averaged | Present ranges separately with conflict flag, or cite filing fact only (GC +22.4% Q3) |
| R3 | "Historic ~50% GM baseline" without filing-verified FY25 46.9% context | D2 — baseline contested; 50.1% is refund-inflated Q3 print | FY25 46.9%; 5-yr range 44.1–46.9%; Q3 50.1% incl ~2pp refunds; ex-refund ≈48.1% |
| R4 | Any unlabeled forward-GM guidance (47–48% / ~46.5% / 280bp) as fact | Management-claim via third-party coverage; transcripts `failed_retrieval` (D1) | Label as management claim via third-party coverage, or omit |
| R5 | Any unlabeled DRAM/NAND/BoM magnitude as fact | Third-party, pending §12 admission (D4) | Label as third-party-reported; direction only is filing-supported |
| R6 | Any unlabeled CEO-transition statement as fact | Third-party-reported; DEF 14A unextracted (D3) | Label as third-party-reported, or omit |
| R7 | Any recommendation, target price, or portfolio direction | Portfolio-blind, advisory only, PILOT-NONCANONICAL | Never |
| R8 | "Refund-adjusted 40.07% reflects real margin pressure absorbed" (S7 F1) | Contradicted frozen B F3; refund-contaminated | B F3 framing: 40.07% is highest in 5-yr window, refund-contaminated — no clean margin read |
| R9 | 9M Services "~40%+ of gross profit" presented as filing-derived | CRO-1 advisory: FY25 42.17% is V2-derived; 9M framing = estimate | Use FY25 42.17% @ 75.41% GM [D]; 9M share only as analyst estimate |
| R10 | "25/25 reproduced-or-caveated" double-count | S7 F3; correct = 24 + 1 PIT-stale | "24/25 reproduced-or-caveated + 1 PIT-stale (V13); 0 contradicted" (only if the essay's verification register is referenced) |

---

## 11. THESIS-BREAK / FALSIFICATION CONDITIONS

**Essay §6.3 (analyst-selected thresholds, labeled per FD #53 — NOT Founder-approved values; keep the label):**
(a) Services revenue growth < total revenue growth for 2 consecutive quarters;
(b) ex-refund GM < 44%;
(c) Greater China re-enters decline while the rest grows;
(d) share count stops declining despite authorization;
(e) a single competitor's interface reaches disclosed default-status penetration metrics.

**CRO change-of-conclusion conditions (must stay visible alongside):**
- G1–G10 §12 admission (esp. App Store fee mechanics, Google-licensing magnitude, Apple Intelligence usage, Gemini-backend claims);
- Q4 FY26 filings: Services growth vs total growth, realized Services margin, ex-refund total margin, quantified litigation/licensing effect;
- Q3 FY26 earnings-call transcript retrieval (verifies/rejects call-based management claims);
- DEF 14A extraction or 8-K Item 5.02 (resolves succession claim);
- Evidence of actual user-interface substitution / default-status penetration / developer migration / routing displacement → upgrades the AI thesis (supplies the missing behavioral link);
- Disclosed regulatory outcomes preserving Apple's effective economics + sustained Services growth above total + stable Services margins → weakens the CRO profit-pool case.

**Editorial requirement:** thesis-break conditions may be summarized in publication but must not be deleted or downgraded where relevant to the reader (P1/P4).

---

## 12. EDITORIAL PRIORITY (what matters most to the Founder/reader — §15)

1. **The converged threat is not the financials — it is the interface:** the single most decision-relevant insight is that Apple's #1 moat-break vector (AI-interface disintermediation) is independently derived by two lanes, while the financials remain strong. Strong numbers + structural threat = the story.
2. **The CRO inversion must frame the confidence read:** the thesis is a moat thesis; LOW-MEDIUM moat-durability confidence governs, not HIGH liquidity confidence. Regulatory profit-pool erosion is the present-tense primary break.
3. **Q3 margin quality is distorted:** 50.1% GM includes ~2pp tariff refunds; Products GM 40.07% is refund-contaminated; Services GM flat y/y — don't let the headline margin mislead.
4. **The corrected intangibles figure:** $20,342M @ 2026-06-27 (+83.4% YTD, −$992M QoQ) — not the stale 21,334 — is a material watch item (undisclosed nature of the +$9.25B build).
5. **Capital-return run-rate favors slowdown, not pause:** buyback coverage 53.1% vs 86.3% — a real signal under the strong headline.
6. **AI compute is being expensed:** R&D +32.5% ≈ FY25 full-year while capex −28.2% — the clearest quantified AI-transition signature in the packet.
7. **Uncertainty discipline:** third-party magnitudes (DRAM/NAND/BoM, CEO transition, forward GM guide) are unadmitted — the piece must preserve their labeled status.

**Reader-facing framing (locked):** a professional Thai investment reader should finish knowing (a) what is happening, (b) why it matters now, (c) the central insight, (d) the strongest evidence, (e) the strongest reason the thesis could be wrong — within the opening 10–15% (§16 baseline editorial prompt).

---

## 13. FACTS LOCKED REGISTRY (F1 — authoritative token list)

Numbers / dates / source identifiers / uncertainty levels / dissent / conclusion boundaries. **Editorial writer MUST NOT alter these tokens.** (Class legend: [F]/[D]/[M]/[3P]/[A]; §12 = §12 source admission.)

| # | Token | As-of | Class | Source lineage | Uncertainty / boundary |
|---|---|---|---|---|---|
| T01 | Q3 FY26 revenue $109.4B (+16%) | Q3 FY26 (2026-06-27) | [F] | Essay §1.3; S5 A1; SRC-02/03 | None — filing fact |
| T02 | Q3 FY26 diluted EPS $2.02 (+29%, incl. ~$0.11 tariff refund) | Q3 FY26 | [F] | Essay §1.3; S5 A1; B V17 | Refund component disclosed |
| T03 | Q3 FY26 GM 50.1% (incl. ~2pp tariff refunds) | Q3 FY26 | [F] | Essay §1.3; S5 A1/A2 | Refund-contaminated; ex-refund ≈48.1% [D] |
| T04 | Q3 FY26 net income $29.789B | Q3 FY26 | [F] | Essay §1.3 | Filing fact |
| T05 | Q3 FY26 diluted shares 14.7147B | Q3 FY26 | [F] | Essay §1.3 | Filing fact |
| T06 | Q3 iPhone +21.7% to $54.25B · Mac +28.6% to $10.35B · Services +12.1% to $30.74B · iPad −5.9% · Wearables +6.5% | Q3 FY26 | [F] | Essay §1.3; S5 A1 | Filing facts |
| T07 | 9M FY26 revenue $364.36B (+16.2% vs $313.70B) | 9M FY26 | [F] | Essay §1.3; B1 | Filing facts |
| T08 | 9M FY26 OI $122.43B (+21.7%) · NI $101.46B (+20.0%) · EPS $6.88 (+22.4%) | 9M FY26 | [F] | Essay §1.3 | Filing facts |
| T09 | 9M FY26 mix: iPhone $196.52B (53.9%, +22.4%) · Services $91.73B (25.2%, +14.1%) · Wearables $27.28B (+2.3%) · Mac $27.14B (+8.6%) · iPad $21.70B (+3.0%) | 9M FY26 | [F] | Essay §1.3 | Filing facts |
| T10 | FY25 revenue $416.16B (+6%) · NI $112.01B · OCF $111.48B · OI $133.05B | FY25 | [F] | Essay §1.2; S5 B1 | Filing facts |
| T11 | FY25 GM 46.9% · OI% 32.0% · NI% 26.9% | FY25 | [D] | Essay §1.2; B1 | Derived |
| T12 | 5-yr GM: 44.1% (FY23) → 46.2% (FY24) → 46.9% (FY25) | FY23–25 | [F] | Essay §1.2/§2.4; D2 | Baseline for D2 framing |
| T13 | FY25 FCF ≈$98.8B · FCF/NI 88.18% (5-yr low) | FY25 | [D] | Essay §1.2/§1.5; B V10, E6 | FY21–25 series 98.18/111.66/102.67/116.08/88.18 |
| T14 | FY25 segment mix: Americas 42.9% · Europe 26.7% · GC 15.5% · Japan 6.9% · ROW 8.1% | FY25 | [F] | Essay §1.1; B7 | Filing facts |
| T15 | Intangibles $20,342M @ 2026-06-27 (+83.4% YTD, −$992M QoQ) | 2026-06-27 | [F] | Essay §1.4; S5 B2/N3/V13 | **21,334 superseded (R1)**; nature of +$9.25B build unresolved (U2/E1) |
| T16 | Cash+securities $146.5B · total debt $84.3B · net cash ≈$62B | Q3 FY26 | [F]+[D] | Essay §1.4; S5 B3; B V18 | Net cash derived; CRO inversion applies (M9) |
| T17 | Inventory $11.09B vs $5.72B FY25-end (+94%) | Q3 FY26 | [F] | Essay §1.4; B5/F6 | Cause undetermined (U1) |
| T18 | Total assets $383.27B · equity $107.52B (vs $73.73B FY25-end) | Q3 FY26 | [F] | Essay §1.4; A VIEW 4 | Retained-earnings swing flagged, not fully reconciled |
| T19 | AP $64.53B ≫ AR $31.40B | Q3 FY26 | [F] | Essay §2.6; A VIEW 4 | Negative working-capital model |
| T20 | Deferred revenue $9.54B vs $9.06B (+5%) | Q3 FY26 | [F] | Essay §2.1 | Indirect switching-cost measurability |
| T21 | Q3 Products GM 40.07% (highest in 5-yr window, refund-contaminated) | Q3 FY26 | [F] | Essay §2.4; B F3 | No clean margin read (R8) |
| T22 | Q3 Services GM 75.62% (flat y/y) · 9M 76.3% vs 75.5% (+0.8pp, mix-driven) | Q3/9M FY26 | [F] | Essay §1.3; E5, B V7/F3 | NOT an inflection |
| T23 | FY25 Services: 42.17% of gross profit @ 75.41% GM | FY25 | [D] | CRO; B V2 | 9M "~40%+" = analyst estimate (R9/CRO-1) |
| T24 | CoS: Services ≈23.7% vs Products ≈60.1% of revenue | 9M FY26 | [D] | Essay §1.3; A VIEW 6 | Derived |
| T25 | FY25 cash tax $43,369M vs $26,102M (+$17.3B, +66%) · ETR 15.6% (FY24 24.1% one-time; Q3 17.9%; 9M 17.6%) | FY25/9M FY26 | [F] | Essay §1.5; E6, B F2 | Tax-cash story; 9M FY26 cash tax −29% ($26,555M vs $37,332M) |
| T26 | 9M FY26 OCF +43.1% vs NI +20.0% | 9M FY26 | [F] | Essay §1.5; B V16 | Conversion re-accelerates |
| T27 | 9M FY26 R&D $34,035M (+32.5%) ≈ FY25 $34,550M · capex −28.2% ($6,799M vs $9,473M) · R&D intensity 8.3%→9.3% | 9M FY26 | [F]+[D] | Essay §1.5; E3, B F5 | AI compute expensed, not capitalized (M11) |
| T28 | Buyback coverage 53.1% (9M FY26) vs 86.3% (9M FY25); Q1 92.9M / Q2 42.4M / Q3 79.6M shares | 9M FY26 | [F] | Essay §5.1; E4, B F4, N1 | Run-rate favors slowdown; ASR-timing caveat |
| T29 | FY25 buybacks $89.3B (equity line) / $90,711M (cash-flow line) · cumulative FY21–25 $438.6B | FY25 | [F] | Essay §5.1; N4/B4 | Same event, different statement bases — not a contradiction |
| T30 | $100B authorization (May 2025) · $10B ASRs settle Q4 FY26 · dividend $0.25→$0.26→$0.27 (payable 2026-08-13) | 2025–26 | [F] | Essay §5.1 | Filing facts |
| T31 | Shares −10.07% FY21–25 (16.4268B→14.7733B) · −1.1% 9M FY26 (14.609B) · 14.59418B @ 2026-07-17 | FY21–26 | [F] | Essay §5.1; B V14/V15 | Filing facts |
| T32 | Greater China +22.4% Q3 FY26 (after FY24 −8%, FY25 −4%) | Q3 FY26 | [F] | Essay §2.3; B6/V5 | C1: discount-driven vs Huawei premium lead; D5 conflicting shares |
| T33 | Regulatory set: €500M DMA fine + cease-and-desist · DOJ suit · Epic 2025 injunction · 9th Cir. 2025-12-11 · SCOTUS cert 2026-06-30 · Google-licensing risk | Q3 FY26 10-Q | [F] | Essay §2.1/§4.1; B V23; CRO M-A | Direction filing-verified; fee mechanics third-party [3P] |
| T34 | Price $301.08 · 52-wk $223.78–$344.57 · mkt cap ≈$4.44T · P/E ~39.6× FY25 / ~33× annualized (~$135B) | 2026-08-12 | [D] | Essay §5.2; A VIEW 7 | Advisory context only; no recommendation |
| T35 | China share (Q1 2026): Huawei 20–20.7% vs Apple 19–19.4% | Q1 2026 | [3P] | Essay §4.4; S5 G9/G10, D5 | `conflicting` trackers — never averaged (R2) |
| T36 | Q4 GM guide 47–48% / normalized ~46.5% / ~280bp | forward | [M/3P] | S5 D1/G1 | Management-claim-only via third-party coverage; transcripts `failed_retrieval` (R4) |
| T37 | CEO transition Cook→Ternus 2026-09-01 | forward | [3P] | S5 D3/G2 | Third-party press; DEF 14A unextracted (R6) |
| T38 | DRAM ASP +400% y/y · NAND +300% · iPhone 18 Pro Max BoM +$300 (base +$200–250) | forward | [3P] | S5 D4/G3 | Pending §12 admission (R5); direction only is filing-supported |
| T39 | Google TAC ~$20B/yr; exclusive default deal legally dead | 2026 | [3P] | Essay §2.6; S5 G6 | Figure third-party; "Google licensing at risk" is filing-verified direction |
| T40 | Apple Intelligence ~410M DAU · on-device ~150B params · Siri backend ~1.2T-param Google Gemini ~$1B/yr | 2026 | [3P] | Essay §2.5; S5 G5 | Pending §12 admission |
| T41 | Vision Pro ~600K cumulative · 45K holiday-2025 · VPG disbanded ~Apr 2026 · ~95% marketing cut | 2025–26 | [3P] | Essay §2.3; S5 G7 | Pending §12 admission |
| T42 | Huawei 70M HarmonyOS phones 2024 · Mate 80 ~7M · refurb iPhone 13 ~CNY 1,720 (−45%) | 2024–26 | [3P] | Essay §2.2–2.3; S5 G8/G9 | Pending §12 admission |
| T43 | Confidence: HIGH balance-sheet · MEDIUM reported economics · LOW-MEDIUM moat durability | locked | [A] | Essay §6.1; A VIEW 9 | CRO inversion applies (M9) |
| T44 | Earnings-quality grade: ADEQUATE (not HIGH) | locked | [A] | Essay §1.5; B §5.1 | FY25 conversion break is real |

**Conclusion boundaries (locked):**
- No recommendation, target price, or portfolio direction — anywhere in the publication.
- "Bent, not broken" must appear **with** the CRO challenge and the LOW-MEDIUM moat-durability confidence (P1).
- All [3P] items must be attributed; no unadmitted magnitude may be stated as fact.
- PILOT-NONCANONICAL status: the piece is calibration on a published case — the editorial A/B is a workflow-calibration artifact, not new investment truth.

---

## 14. THAI EDITORIAL GATE READINESS (P1–P5 mapping — §19)

| Gate | What the gate requires | How this packet makes it ready | S11 editorial pass must verify |
|---|---|---|---|
| **P1 — Research Integrity** | Final thesis matches Facts Locked state; no rejected claim reappears; uncertainty preserved; material dissent preserved | §2 Central Finding (both layers); §10 Rejected/Superseded (R1–R10); §7 Material Uncertainty (U1–U10); §9 Material Dissent (1–6, verbatim) | Article thesis = §2 lead + dissent visible; no R1–R10 token resurrected; U-items not compressed; CRO challenge present |
| **P2 — Fact Fidelity** | Token fidelity (F1) passes; semantic fidelity (F2) passes; no new unauthorized claim | §13 Facts Locked Registry (T01–T44, authoritative tokens); §0.2 F1 verification record; §3 Material Claims = the only authorized claim set | Every figure in the article matches T01–T44; every material claim maps to M1–M13 as MATCHED or SUPPORTED_REPHRASE; zero ALTERED_MEANING / NEW_UNAUTHORIZED_CLAIM / omitted material uncertainty or dissent |
| **P3 — Natural Thai** | Sounds written in Thai, not translated; natural terminology; no literal calques/noun stacking/academic language; English finance terms retained where clearer | §16 baseline editorial prompt requirements; packet carries no AI prose patterns; evidence-class labels are writer-side instructions, not publication text | Thai reads natively; terms like moat/switching cost/network effect/gross margin/FCF/ROIC/capex/guidance/pricing power/unit economics/multiple/reverse DCF may stay English when natural; epistemic phrases per §16 (ข้อมูลยืนยันว่า / หลักฐานตอนนี้ชี้ว่า / ฝ่ายบริหารระบุว่า / เรายังพิสูจน์ไม่ได้ว่า / นี่เป็นการประเมิน… / หลักฐานยังไม่พอให้สรุปว่า) |
| **P4 — Causal Narrative** | Explains mechanism, not checklist; thesis easy to locate; numbers have "so what?"; background doesn't bury insight | §6 Causal Chains (4 locked chains); §12 Editorial Priority (7 ranked insights); §5 approved interpretations | Article built around chains 1–2 at minimum; each number answers what changed / how large / why it matters / what it reveals; thesis locatable in opening 10–15% |
| **P5 — Publication Craft** | Headline matches thesis; opening informs, not hype; deliberate flow; headings/bullets only when helpful; no AI clichés; **no internal IIP governance jargon** | Packet is free of governance IDs/FD references/mandate language in its publication-facing content; §12 gives the reader-facing framing | Headline reflects §2 (threat-ranking story, not a financials story); no internal jargon (no S1–S12, t_ IDs, § references, FD numbers, evidence-class letters in final prose); no "ไม่ใช่ X แต่คือ Y" repetition; no excessive headings/bullets |

**Note on jargon firewall:** the fact packet is an internal logical contract (evidence classes, lineage IDs, § references are for the writer). NONE of that machinery may appear in the published Thai prose. The P5 jargon firewall is applied at S11/IC Secretary QC.

---

## 15. SELECTED SUPPORTING PRIMARY SOURCES (per §16 — the writer may also consult these)

- SRC-01 · Apple FY2025 Form 10-K (accession 0000320193-25-000079) — FY25 financials, Item 1A
- SRC-02 · Q3 FY26 Form 10-Q (accession 0000320193-26-000020) — Q3/9M FY26, MD&A, Item 1/1A regulatory set
- SRC-03 · Q3 FY26 Form 8-K ex99.1 (accession 0000320193-26-000018) — Q3 FY26 press release, CEO statement
- SRC-04 · Q2 FY26 Form 10-Q (accession 0000320193-26-000013) — superseded intangibles provenance (do NOT cite 21,334 as current)
- SRC-05 · Q1 FY26 Form 10-Q (accession 0000320193-26-000006)
- SRC-06 · XBRL companyfacts CIK 0000320193 — series-level data (E1/E2 flags: use with Data Steward caveat)
- Admission packet: `ADMITTED-SOURCE-PACKET-APPLE-REHEARSAL.md` (S1, t_bfdcbf31) — full 15-source register, PIT stamps, `conflicting`/`failed_retrieval` flags
- **NOT for the writer's analysis:** published case (SRC-P1) and published CRO essay (SRC-P2) — the packet supersedes them for publication purposes; S4 Gemini raw view (44,501 chars) is the research lane record, not publication content.

---

## 16. HANDOFF NOTES FOR S11 (Gemini Thai Editorial A/B)

1. **Two variants from the SAME packet:** Candidate A (Gemini editorial) and Candidate B (Hermes/IC Secretary editorial) must be composed from this packet + the §15 primary sources only. No other analytical input.
2. **Fidelity gates apply to both variants:** F1 token fidelity (§13 registry) + F2 semantic fidelity (claim classification MATCHED / SUPPORTED_REPHRASE / ALTERED_MEANING / NEW_UNAUTHORIZED_CLAIM / OMITTED_MATERIAL_UNCERTAINTY / OMITTED_MATERIAL_DISSENT — §18). Publication fails on any ALTERED_MEANING, NEW_UNAUTHORIZED_CLAIM, or material omission.
3. **P1–P5 (§14) are the acceptance gates** for both variants; Founder preference on communication quality is the decisive signal for the A/B verdict (§21).
4. **Reader-facing:** professional Thai investor audience; natural Thai; English finance terms retained where natural; opening 10–15% must deliver what-is-happening / why-now / central insight / strongest evidence / strongest reason the thesis could be wrong.
5. **PILOT banner:** the A/B comparison is calibration on a published case — neither variant is new investment truth; no recommendation language in either variant.
6. **No-internal-jargon:** evidence-class labels, lineage IDs, S-stage references, t_ task IDs, FD numbers, and governance vocabulary must not appear in the prose.

---

*S10 Facts Locked gate passed (F1 token fidelity verified); Publication Fact Packet delivered as the mandatory logical contract per v1.4 §15. Derived artifact — no new claims. PILOT-NONCANONICAL — calibration only, not investment truth. Prepared by org-ic-secretary as Managing Editor / Publication Controller (§17).*

<!-- 2026-08-12 23:45 UTC+7 -->
