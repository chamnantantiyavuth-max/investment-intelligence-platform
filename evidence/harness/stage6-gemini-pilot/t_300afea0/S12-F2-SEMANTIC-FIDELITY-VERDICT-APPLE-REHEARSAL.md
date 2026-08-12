# S12 — F2 SEMANTIC FIDELITY VERDICT (Thai Editorial vs Facts-Locked Packet)

**Task:** t_300afea0 — [DR][CHILD] S12 — Semantic Fidelity Gate F2
**Stage:** S12 · **Workflow:** Gemini DR v1.4 pilot (§18 Gate F2)
**Reviewer:** org-auditor (Internal Auditor / Red Team — independent of S11 writer context, per §18 "must not be the same context that wrote the article")
**Date:** 2026-08-13 00:20 UTC+7 · **Mode:** PILOT-NONCANONICAL — calibration rehearsal on a published Apple case. Not investment truth. Portfolio-blind. Advisory only.
**Anchor:** `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md` §18 (F2 Semantic Fidelity / No-New-Claims), §19 P1/P2

---

## 0. INPUTS — hash-verified on disk (Verify-First)

| Artifact | SHA-256 (on disk) | Matches recorded |
|---|---|---|
| S10 Publication Fact Packet (frozen facts, `37b4158c…`) | `37b4158c004103b734e88d3fa1e0927b3b873ab93a2d6756e84cc908d48c5be8` | ✅ S10 metadata |
| Candidate A (Gemini editorial) | `7e01e3189a8765806ed38594923643247e3a1f50fab475956cd48754d208abac` | ✅ S11 metadata |
| Candidate B (Hermes/IC Sec editorial) | `22ffcff45c2a3ac684498bdd228fa5a9dc4dbe075393a4e268d9561f4fd4b705` | ✅ S11 metadata |
| S11 A/B comparison & verdict | `15e1135a1d96eaafb8354dd55c6e1dd21f058d5ffc71fecdbada13ae39833391` | ✅ S11 metadata |

Reviewed bodies (delimited `# ARTICLE A/B` … `## Appendix`): B = 51 lines, A = 64 lines. Independent forbidden-token scan re-run by this reviewer: `21,334` / `92.32%` / `25/25` / `refund-adjusted` = **0 occurrences in both bodies** (R1/R10/R8 respected). No recommendation/target-price/portfolio language (only the buyback noun + the required disclaimer). No internal governance jargon (no t_ IDs, S-IDs, FD numbers, evidence-class labels, §-references, G-Dim/D1–D6/C-IDs/U-IDs in the prose).

---

## 1. METHOD (§18)

1. Extract every material claim from each article body (Thai/edited text).
2. Map each claim against the Publication Fact Packet (§3 Material Claims M1–M13, §4 Verified Facts, §5 Verified Calculations C-01–C-12, §6 Causal Chains, §7 Uncertainty U1–U10, §8 Management Claims, §9 Dissent, §13 Facts-Locked Registry T01–T44).
3. Classify per §18 taxonomy: `MATCHED` / `SUPPORTED_REPHRASE` / `ALTERED_MEANING` / `NEW_UNAUTHORIZED_CLAIM` / `OMITTED_MATERIAL_UNCERTAINTY` / `OMITTED_MATERIAL_DISSENT`.
4. **Fail condition (§18):** any material claim = `ALTERED_MEANING` or `NEW_UNAUTHORIZED_CLAIM`, or material omission of required uncertainty/dissent.
5. Chosen variant for the formal verdict = **Candidate B** (per S11 recommendation; Founder preference decisive per §21). Candidate A cross-checked (completeness reference).

---

## 2. CANDIDATE B (chosen variant) — CLAIM-BY-CLAIM CLASSIFICATION

Every material claim in Article B body, mapped to packet registry / claims. **Result: 0 ALTERED_MEANING · 0 NEW_UNAUTHORIZED_CLAIM.**

| # | Article B claim (Thai, condensed) | Packet mapping | Class |
|---|---|---|---|
| B1 | Q3 FY26 revenue $109.4B (+16% y/y) | T01 | MATCHED |
| B2 | Diluted EPS $2.02 (+29%, incl ~$0.11 tariff refund) | T02 | MATCHED |
| B3 | Q3 GM 50.1%, highest in 5 years | T03 + T12 (5-yr range 44.1–46.9%; 50.1% is arithmetically the max — verified) | SUPPORTED_REPHRASE |
| B4 | Cash+securities $146.5B vs debt $84.3B → net cash ≈$62B | T16 / C-02 | MATCHED |
| B5 | No filing-visible financial distress | M2 [F]+[A] | MATCHED |
| B6 | Moat durable but conditional — "bent, not broken" | M1 [A+G] | MATCHED |
| B7 | Two independent analyses converge on the same #1 threat: AI-interface disintermediation | M3 [A+G], S5 A5/D6 | MATCHED |
| B8 | AI as third-party interface layer; routing/monetization bypassed → "dumb pipe" | M3 + Chain 1 | SUPPORTED_REPHRASE |
| B9 | Services = 25.2% of 9M FY26 revenue; structurally higher margin = value at risk | T09 + M4 | MATCHED |
| B10 | Services = 42.17% of FY25 gross profit @ 75.41% GM | T23 [D] | MATCHED |
| B11 | CRO dissent: erosion may come from regulators/courts forcing open distribution/payment layer — filing-visible, present-tense, no user defection needed | M5/M6 + CRO Mechanism A | MATCHED |
| B12 | 9M FY26 revenue $364.36B (+16.2% vs $313.70B) | T07 | MATCHED |
| B13 | 9M FY26 NI $101.46B (+20.0%) | T08 | MATCHED |
| B14 | 9M OCF +43.1% vs NI +20.0% | T26 | MATCHED |
| B15 | FY25 NI +19.5% while OCF −5.7% (structural break) | §4.6 (B V12) | MATCHED |
| B16 | FY25 earnings quality ADEQUATE, not HIGH | T44 | MATCHED |
| B17 | Q3 GM 50.1% incl ~2pp refunds; ex-refund ≈48.1% | T03 + C-03 | MATCHED |
| B18 | Products GM 40.07% highest in 5-yr window, refund-contaminated — no clean read; no "margin pressure absorbed" claim | T21 + C-04 + R8 (B F3 framing) | MATCHED |
| B19 | Ex-refund GM sustainability needs next-quarter confirmation | U3 | MATCHED (uncertainty preserved) |
| B20 | Services GM Q3 75.62% flat y/y; 9M 76.3% vs 75.5% (+0.8pp, mix-driven per MD&A, not an inflection) | T22 | MATCHED |
| B21 | Services CoS ≈23.7% vs Products ≈60.1% of revenue | T24 | MATCHED |
| B22 | Services = most fragile profit layer (value at risk) | M4 | SUPPORTED_REPHRASE |
| B23 | Buyback coverage 53.1% (9M FY26) vs 86.3% (9M FY25); steepest drop in 5+ years; run-rate favors real slowdown, not pause | T28 + C-07 + M10 | MATCHED |
| B24 | $100B authorization (May 2025) | T30 | MATCHED |
| B25 | Shares −10.07% FY21–25 | T31 | MATCHED |
| B26 | 9M R&D $34,035M (+32.5%) ≈ FY25 $34,550M; capex −28.2% | T27 | MATCHED |
| B27 | AI compute expensed through R&D, not capitalized → margin structure under pressure | M11 + Chain 3 | SUPPORTED_REPHRASE |
| B28 | Disintermediation mechanism: assistant/agent picks apps → iOS routing bypassed, no one leaves iPhone; value at risk = Services | Chain 1 + M3 | MATCHED |
| B29 | CRO: real break may be profit-pool erosion via regulation/litigation already in motion | M6 + CRO Mechanism A | MATCHED |
| B30 | Regulatory set: €500M DMA fine + cease-and-desist; DOJ; Epic injunction; 9th Cir. 2025-12-11; SCOTUS cert 2026-06-30; Google-licensing risk | T33 [F] | MATCHED |
| B31 | Users need not leave iPhone for profit redistribution; moat behaviorally sticky but economically less exclusive | CRO core §9.1 | MATCHED |
| B32 | Confidence inversion: HIGH = liquidity/balance-sheet, not moat; moat durability LOW-MEDIUM; fortress funds adaptation, doesn't preserve rents | T43 + CRO Sub-challenge C | MATCHED |
| B33 | Filings prove numbers but not moat mechanics; switching costs/network effects inferred from price/margin persistence, not disclosed | M12 + U5 | MATCHED (uncertainty preserved) |
| B34 | Inventory +94% to $11.09B from $5.72B FY25-end; largest WC swing; cause undetermined; 3 hypotheses | T17 + U1 | MATCHED (uncertainty preserved) |
| B35 | Intangibles $20,342M @ 2026-06-27 (+83.4% YTD, −$992M QoQ); +$9.25B no disclosed M&A; acquisitions/capitalized-software hypotheses | T15 + U2 | MATCHED (corrected figure used; R1 respected) |
| B36 | Q4 GM guide 47–48% / ~46.5% / ~280bp — labeled ฝ่ายบริหาร…ผ่านรายงานข่าว (management claim via third-party coverage) | T36 / MC4 [M/3P] | MATCHED (epistemic label correct) |
| B37 | CEO transition Cook→Ternus 2026-09-01 — labeled ตามรายงานข่าว (third-party-reported) | T37 / MC5 [3P] | MATCHED (epistemic label correct) |
| B38 | DRAM +400% / NAND +300% / BoM +$300 — labeled รายงานข่าวระบุว่า; direction consistent with filing | T38 + M13 [3P] | MATCHED (direction-only framing correct) |
| B39 | Thesis-break conditions (a)–(e): Services < total 2 qtrs; ex-refund GM <44%; China re-decline while rest grows; share count stops declining; competitor default penetration | §11 (a)–(e) | MATCHED (summarized, not deleted) |
| B40 | CRO weakening condition: regulatory outcomes preserve economics + Services growth above total + stable margins → CRO case weakens | §11 CRO change-of-conclusion | MATCHED |
| B41 | Valuation context: $301.08; 52-wk $223.78–$344.57; mkt cap ≈$4.44T; P/E ~39.6× FY25 / ~33× annualized; market embeds demanding double-digit EPS growth vs ~4% NI CAGR FY21–25 | T34 + C-08/C-09/C-11 | MATCHED (verified: 4.44T, 39.6×, 32.8×, NI CAGR 4.3%) |
| B42 | No recommendation / no target price / no trade view | §13 Conclusion boundaries | MATCHED |
| B43 | Calibration-rehearsal disclaimer (not investment truth) | Pilot banner / §16 | MATCHED |

**Uncertainty/dissent preservation review (B):**
- U1 ✅ (inventory, B34) · U2 ✅ (intangibles, B35) · U3 ✅ (ex-refund GM, B19) · U5 ✅ (behavioral moat, B33) · U7 ✅-implicit (legal set presented as ongoing pressure, B30) · U8 ✅ (all third-party items used are labeled; unadmitted items not asserted) · U9 ✅ (Q4 guide + succession labeled management/3P, B36/B37) · U10 ✅ (CRO re-ranking visible, B29/B32).
- U4 (other non-current liabilities +$13.5B) and U6 (unit vs ASP split): **not surfaced in B.** Both are packet-tagged non-material for the moat thesis: U4/E2 is explicitly "out of publication scope" in §4.3; U6 is a data-availability limitation, not a thesis-bearing uncertainty. **Non-material omission — no gate impact.**
- Dissent: CRO core (B31) + Mechanism A primary-break (B29/B30) + confidence inversion (B32) + principal dissent — all present per the packet's §9 editorial requirement (must present primary-break challenge + confidence inversion; piece may lead with converged thesis). ✅
- Observation (non-blocking): CRO Mechanism B ("convergence = shared framing; visibility ≠ probability") is not explicitly surfaced in B; B asserts the two-lane convergence (B7) without the convergence-epistemology caveat. The packet's operative editorial requirement (§9) mandates primary-break + inversion (both present), so this is a MINOR NOTE for the synthesis stage, not a §18 material omission.

---

## 3. CANDIDATE A (cross-check — completeness reference)

Claim-by-claim classification of Article A body: all core claims map to the same packet tokens as B (T01/T02/T03/T07/T08/T13/T16/T17/T21/T22/T23/T24/T25/T26/T27/T28/T30/T31/T32/T33/T34/T35/T36/T37/T38/T39/T40/T42/T43/T44, M1–M13, C-03/C-04/C-07/C-08/C-09/C-11, Chains 1–3, §11 (1)–(5)) as MATCHED or SUPPORTED_REPHRASE. **0 ALTERED_MEANING · 0 NEW_UNAUTHORIZED_CLAIM.**

Specific A items verified:
- A's third-party set (DAU ~410M / 1.2T-param Gemini backend; TAC ~$20B; 5–17% opt-out rates; Huawei 20–20.7% vs Apple 19–19.4% conflicting; HarmonyOS 70M) — **all labeled 3P** per T33/T35/T39/T40/T42 ✅ (R2 no-averaging respected: ranges presented separately with conflicting flag).
- A's "Tim Cook เป็น Ternus" (E4 correction removed "John") — matches registry T37 exactly ✅.
- A's market-expectation comparison uses revenue CAGR ≈3.3% (C-11) instead of the packet's T34 NI-CAGR ≈4% reference — both are locked packet metrics, direction identical (demanding vs 5-yr trend). SUPPORTED_REPHRASE — minor note: T34's approved interpretation cites ~4% NI CAGR; A's 3.3% revenue CAGR is a permissible locked alternative (C-11), not a new claim.
- A's concept-definition detour (moat/disintermediation/dumb-pipe) is explanatory gloss — no factual additions.

**Minor findings (A only, non-blocking — A is the completeness reference, not the chosen variant):**
- A1: U5 epistemic basis (filings do not prove moat mechanics; durability inferred) is not explicitly surfaced in A — LOW-MEDIUM moat confidence is carried, but the *reason* (absent behavioral evidence) is implicit. Minor; B covers it explicitly.
- A2: U7 "outcomes unresolved" nuance is implicit in A's legal-set paragraph, not stated. Minor.

---

## 4. VERDICT

### ══ F2 GATE — PASS (Candidate B, chosen variant) ══

- **Candidate B (chosen for this rehearsal):** 43/43 material claims MATCHED or SUPPORTED_REPHRASE against the S10 Publication Fact Packet; **0 ALTERED_MEANING, 0 NEW_UNAUTHORIZED_CLAIM**; required uncertainty (U1/U2/U3/U5/U7/U8/U9/U10) and material dissent (CRO core + primary-break + confidence inversion) preserved; U4/U6 omissions non-material (out-of-scope/limitation); forbidden/superseded tokens 0 (R1/R8/R10 respected); third-party and management-claim items carry correct epistemic labels (ฝ่ายบริหาร…ผ่านรายงานข่าว / ตามรายงานข่าว / รายงานข่าวระบุว่า); no recommendation language.
- **Candidate A (cross-check):** PASS with 2 minor non-blocking notes (A1 U5 explicitness, A2 U7 nuance). No §18 fail condition triggered.
- **Conclusion:** Both variants are semantically faithful to the frozen facts. B is the cleaner F2 result and consistent with the S11 recommendation. No re-edit required at the F2 gate.

### Non-blocking observations for synthesis (t_68d2824b)
1. CRO Mechanism B (convergence-as-shared-framing; visibility ≠ probability) is not explicit in either variant — synthesis may add one sentence if the convergence claim is featured as the headline evidence.
2. A's U5-explicitness gap (A1) — if A's prose is ever published as-is, add the "filings do not prove moat mechanics" epistemic sentence.
3. A's CAGR comparison uses C-11 revenue CAGR (3.3%) where T34 prefers NI CAGR (~4%) — directionally identical; keep either, do not mix both in one sentence.
4. B's U4/U6 non-surfacing is accepted; do not re-add U4 without Data Steward closure of E2.

*Independent semantic-fidelity review by org-auditor — no editorial context shared with S11 writer (operational separation per §18). All inputs hash-verified. PILOT-NONCANONICAL — calibration only, not investment truth.*
<!-- 2026-08-13 00:20 UTC+7 -->
