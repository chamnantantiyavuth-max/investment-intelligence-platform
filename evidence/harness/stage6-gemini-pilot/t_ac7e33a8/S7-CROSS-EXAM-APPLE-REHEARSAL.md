# S7 — HOSTILE CROSS-EXAMINATION FINDINGS
## Gemini Deep Research v1.4 — Apple Rehearsal (PILOT-NONCANONICAL)

**Task:** t_ac7e33a8 — [DR][CHILD] S7 — Cross Examination
**Examiner:** org-auditor (Internal Auditor / Red Team)
**Subject under exam:** `S6-MAIN-ESSAY-APPLE-REHEARSAL.md` (t_7ac2d383) — SHA-256 `9f29f189aa7a95f136075ee005be1947685c3d7f911518c7d843dee5c20e66f8`
**Evidence examined (all FROZEN):**
- Pass A `pass-a-view.md` — SHA-256 `80e88c9a…d74e` ✅ on-disk exact match
- Pass B `pass-B-view-quant-model-validator.md` — SHA-256 `f0ecb972…cc139f` ✅ on-disk exact match
- Gemini `S4-GEMINI-VIEW-FROZEN.md` — content hash `ce5a9226…dc0` (S5-reproduced); file-level `fa976b62…4fd` ✅ on-disk match
- S5 `S5-RECONCILIATION-APPLE-REHEARSAL.md` (t_a7021f89) — SHA-256 `15861e87…`
- Anchor contract: `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md` §13/§14/§18; Standing Contract #16

**Date:** 2026-08-12 23:30 UTC+7
**Mode:** Hostile cross-exam — assume every claim is wrong until it reproduces against frozen evidence. Portfolio-blind. Advisory only.

---

## 0. EXAM RIGOR — WHAT WAS INDEPENDENTLY RE-CHECKED

| Check | Method | Result |
|---|---|---|
| Essay integrity | `sha256sum` vs parent metadata | ✅ `9f29f189…` exact match |
| Freeze integrity (all 3 passes) | `sha256sum` on-disk vs S5 manifest | ✅ 3/3 exact |
| Word count | `wc -w` | ✅ 4,680 (matches S6 claim) |
| Arithmetic | 38 independent re-derivations from raw figures (EPS, FCF, FCF/NI 5-yr, intangibles +83.4%/−992M, inventory +94%, buyback coverage 53.07/86.33, R&D +32.5%, capex −28.2%, tax +66%/−29%, mix 25.2%, CoS 23.7/60.1, GM 50.06/40.07/75.62, net cash 62.2, shares −10.07%, CAGR 3.3%, mktcap 4.44T, P/E 39.6/33, cum buybacks 438.6B) | ✅ **38/38 PASS, 0 FAIL** |
| No-averaging discipline | D1–D6 unreconciled; China ranges kept separate with conflict flag | ✅ PASS |
| Appendix B compliance | 21,334 appears 3× — all in superseded/must-not-use context (lines 45, 93, 283); no recommendation/target price anywhere; "50% baseline" always accompanied by FY25 46.9% context | ✅ PASS |
| Anti-anchoring | Every material claim traced to a frozen pass or S5 row; zero orphan claims traceable only to SRC-P1/P2 | ✅ PASS (no anchoring fingerprints) |
| Evidence-class label consistency | [3P] applied to all G-only items; [F] only on A/B-filing items; [M] on 8-K issuer statements | ⚠️ 2 defects (F1, F3 below) |

---

## 1. CROSS-EXAM VERDICT (SUMMARY)

**The essay survives hostile cross-examination on its core evidentiary load: 38/38 arithmetic re-derivations pass, all frozen hashes verified, no averaging, no anchoring contamination, Appendix B respected. It is NOT publishable as-is because of one new-claim violation, one citation-namespace collision with one outright misattribution, and one precision defect — all correctable in one S6 rework pass.**

Severity rubric: **BLOCKER** (must fix before S8/S9) · **MATERIAL** (must fix) · **MINOR** (should fix) · **ADVISORY** (note for later stages)

---

## 2. FINDINGS

### 🔴 F1 — NEW CLAIM / SEMANTIC-FIDELITY VIOLATION (MATERIAL — required correction)

**Location:** Essay §2.4, line 140:
> "…and the Q3 FY26 **refund-adjusted Products GM 40.07% reflects real margin pressure absorbed**."

**Charge:** Two defects in one clause:

1. **New claim (violates the essay's own Declaration #2, "no new claims"):** No frozen pass states that Products GM 40.07% "reflects real margin pressure absorbed." The clause is an unsourced interpretation.
2. **Contradicts the frozen evidence it claims to rest on:** Pass B F3 states the OPPOSITE direction — *"Products GM 40.07% (Q3) is the **highest in the 5-yr window** but includes tariff refunds recorded inside products COGS."* The essay's own §1.3 (line 85) correctly says "Q3 Products GM 40.07% (**highest in 5-yr window**, refund-contaminated)" — so §2.4 directly contradicts §1.3 of the same document.
3. **Terminology error:** 40.07% is the refund-*including* reported figure, not "refund-adjusted." Refund-adjusted (ex-refund) would be lower. The essay's own §1.3 knows this ("refund-contaminated").

**Evidence:** B F3; essay lines 85 vs 140.

**Required correction:** Delete the clause "and the Q3 FY26 refund-adjusted Products GM 40.07% reflects real margin pressure absorbed" OR replace with the frozen framing: *"Q3 Products GM 40.07% — the highest in the 5-yr window, refund-contaminated (B F3) — provides no clean read on margin trend; the filing-visible margin-pressure direction is the R&D/capex signature (E3) plus the named NAND/DRAM/AI-compute supply risks (Item 1A)."* Do not re-insert the phrase "refund-adjusted 40.07%."

---

### 🔴 F2 — CITATION-NAMESPACE COLLISION + ONE MISATTRIBUTION (MATERIAL — required correction)

**Location:** §2.1 line 116 (`[G1 D1]`); §2.1 line 120 (`G D1 synthesis`); §2.2 lines 126/128 (`[G D2]`); §2.3 line 134 (`[G D3, G7, G9]`); §2.6 line 158 (`[G D6]`); §4.1 line 185 (`G D1/D2`); §4.5 line 205 (`inside D1/D2`); Appendix A line 278 (`A4 + G D1 synthesis`).

**Charge:** The essay uses the token "D1…D6" in TWO colliding namespaces without defining either:

- **S5 disagreement IDs** — D1 = forward-GM guide, D2 = 50% GM baseline, D3 = CEO transition, D4 = DRAM/NAND magnitudes, D5 = China share conflict, D6 = risk-weighting. Used correctly in §4.
- **Gemini Dimension numbers** — "G D1" (switching cost), "G D2" (network effect), "G D3" (share of mind), "G D6" (efficient scale). Used in §2 as "G D1 synthesis," "[G D2]," "[G D3, G7, G9]," "[G D6]."

A reader (S8 CRO, S9 audit, Founder) **cannot resolve "G D2"**: is it S5 disagreement D2 (GM baseline) or Gemini Dimension 2 (network effect)? These are different claims. The collision is real and material for traceability — the essay's own Appendix A promise ("every material claim maps to a frozen view row") breaks where the token is ambiguous.

**Worst case — outright misattribution:** line 116 tags the EU DMA/CTC fee-mechanics paragraph `[3P] [G1 D1]`. **G1 in S5 is "Q4 FY26 GM guidance 47–48%"** — a different claim entirely. The DMA/CTF content actually lives in (a) Gemini's Dimension 1 (High Switching Cost section), (b) S5 row A3 (regulatory pressure, filing-verified), (c) B V23 (verbatim 10-Q). Tagging it `[G1 D1]` sends the auditor to the wrong reconciliation rows.

**Required correction:** Define the namespace explicitly once (e.g., **G-Dim1…G-Dim6** for Gemini dimensions; keep **D1…D6** for S5 disagreements; keep **G1…G10** for S5 G-rows). Then:
- Line 116 `[G1 D1]` → `[G-Dim1; S5 A3; B V23]` (filing-verified part) / `[G-Dim1]` (fee-mechanics part)
- Lines 120/126/128/134/158/185/205/278 → replace "G D1…D6" with "G-Dim1…G-Dim6"
- Appendix A row (line 278) → `A4 + G-Dim1 synthesis`

---

### 🟠 F3 — PRECISION DEFECT: "25/25 reproduced-or-caveated" (MATERIAL — required correction)

**Location:** §6.1 line 232:
> "MEDIUM — reported economics (financials internally consistent, **25/25 published-case claims reproduced-or-caveated by Pass B; 1 PIT-stale**)."

**Charge:** Double-counts the register. Pass B's own register (V1–V25) is **21 reproduced + 3 caveated (V8/V9/V11) + 1 PIT-stale (V13) = 25 total, 0 contradicted.** "25/25 reproduced-or-caveated" plus "1 PIT-stale" implies 26 slots for 25 claims. The correct reading is 24 reproduced-or-caveated + 1 PIT-stale.

**Required correction:** Rephrase to the frozen register: *"24/25 reproduced-or-caveated + 1 PIT-stale (V13 intangibles, already corrected in §1.4); 0 contradicted."* Or enumerate: "21 reproduced, 3 caveated, 1 PIT-stale."

---

### 🟡 F4 — UNLABELED ASSESSMENT IN EXECUTIVE SUMMARY (MINOR)

**Location:** Line 37: "The business is not in financial distress by any filing-visible measure."

**Charge:** This is an assessment ([A]-class) but carries no evidence-class label and no anchor to a frozen view row. It is a fair synthesis of A VIEW 4/9, but per the essay's own fidelity contract it should carry `[A]` and a citation (A VIEW 4 fortress liquidity; A VIEW 9 HIGH balance-sheet confidence).

**Required correction:** Append `[A] [A VIEW 4, VIEW 9]`.

---

### 🟡 F5 — §2.4 paragraph labeled `[F]` contains assessment content (MINOR)

**Location:** Line 140 — the paragraph opens `**Filing-verified direction [F] [C2, E3]:**` but includes the unsupported clause (F1) and the analyst inference "real margin pressure absorbed." Even after F1 is fixed, the paragraph mixes [F] filing facts with [A] inference under a single [F] label.

**Required correction:** Split the labels — filing facts under [F] (Item 1A risks, R&D/capex signature), the inference under [A] (or delete it per F1).

---

### ⚪ F6 — ADVISORY (no correction required now)

1. **§2.1 line 116:** 8-K CEO framing labeled [M] ("issuer-reported") is consistent with the essay's own legend ([M] = "issuer-reported (8-K press release / call)") and with A VIEW 8's treatment — no change needed. Noting for S9 so it is not re-litigated as a defect.
2. **D1 coverage:** The forward-GM guidance 47–48% (S5 D1) has no standalone §4.x heading; it is folded into §4.2's `[D1, D2, D4]` tag and §2.4's "normalized Q4 ~46.5% (G's own figure, if valid)". Adequately labeled wherever it appears; structural only, optional rework.
3. **Pass B §6 limitation** (FY21–22 segment GM endpoints unverifiable from admitted evidence; Ireland $10.2B ⛔) is not surfaced in the essay's §6.2 unresolved list — acceptable (essay is A/B/G synthesis, not B's audit log), but S9 may want it in the audit trail.

---

## 3. ACQUITTALS — CLAIMS THAT WITHSTOOD HOSTILE ATTACK (verified against frozen evidence)

| Essay claim | Verdict |
|---|---|
| All 38 derived metrics (FCF, ratios, margins, mix, tax, buyback, CAGR, valuation) | ✅ PASS — independently re-derived, 0 failures |
| Intangibles 20,342 @ 2026-06-27 (+83.4% YTD, −$992M QoQ); 21,334 flagged superseded 3× in must-not-use context | ✅ PASS |
| No averaging: D1–D6 unreconciled with evidence classes; China share ranges separated with `conflicting` flag | ✅ PASS |
| Converged top threat = AI-interface disintermediation (A risk #1 ≈ G thesis-killer #3) | ✅ PASS — matches S5 §4-D6 exactly |
| "Bent, not broken" moat verdict (A4 + Gemini Dim-1 synthesis) | ✅ PASS — converged A+G per S5 A4 |
| All [3P] items correctly labeled: DRAM/NAND/BoM, price hikes, CEO transition, TAC $20B, Apple Intelligence, Vision Pro, HarmonyOS, refurb market, China ranges | ✅ PASS |
| All [F] items traceable to B V-rows / A VIEWs / S5 B-rows (headlines, balance sheet, regulatory set V23, R&D/capex E3, tax E6) | ✅ PASS |
| Appendix B must-not-contain list fully respected in-text | ✅ PASS |
| Anti-anchoring: no claim traceable only to SRC-P1/P2; all claims map to frozen passes | ✅ PASS |
| PIT discipline (FD #58): filing dates correct, RESEARCH_AS_OF correct, market data 2026-08-12 | ✅ PASS |

---

## 4. REQUIRED CORRECTIONS (for S6 rework — bounded, no re-research)

| # | Fix | Severity |
|---|---|---|
| C1 | §2.4 line 140: delete or replace "refund-adjusted Products GM 40.07% reflects real margin pressure absorbed" with the B F3 framing ("highest in 5-yr window, refund-contaminated") | BLOCKER |
| C2 | Define citation namespaces once; fix `[G1 D1]`→`[G-Dim1; S5 A3; B V23]`; rename all "G D1…D6"→"G-Dim1…G-Dim6" (lines 116, 120, 126, 128, 134, 158, 185, 205, 278) | BLOCKER |
| C3 | §6.1: "25/25 reproduced-or-caveated; 1 PIT-stale" → "24/25 reproduced-or-caveated + 1 PIT-stale (0 contradicted)" | MATERIAL |
| C4 | Line 37: append `[A] [A VIEW 4, VIEW 9]` to the distress sentence | MINOR |
| C5 | Line 140: split [F]/[A] labels after C1 | MINOR |

**Outcome after C1–C5:** essay should pass S7 re-exam and be releasable to S8 (CRO) with the frozen evidence intact.

---

## 5. HANDOFF NOTES

- **To S8 CRO (t_295cacba):** F1/F3 are the two spots where the essay strained against its own evidence; the CRO may attack the *weighting* (D6) and the *assessment-level claims* (bent-not-broken, "40%+ of gross profit by mix" is A's estimate not a filing number) — those are the softest remaining surfaces.
- **To S9 Audit (t_91eceed5):** verify C1–C5 were applied and that no new claims entered during rework; re-check §2.4 evidence-class labels; confirm the 38 arithmetic re-derivations still pass after any rephrase (they are token-independent, so should).
- **To synthesis parent (t_68d2824b):** this cross-exam found the essay's evidence load SOUND; corrections are editorial, not evidentiary.

---

*Cross-exam produced by org-auditor (S7) — inputs verified frozen per S5 §1; this document is the S7 deliverable for S6 rework, S8 CRO (t_295cacba), S9 audit (t_91eceed5), and synthesis parent t_68d2824b. PILOT-NONCANONICAL — calibration only, not investment truth.*

<!-- 2026-08-12 23:30 UTC+7 -->
