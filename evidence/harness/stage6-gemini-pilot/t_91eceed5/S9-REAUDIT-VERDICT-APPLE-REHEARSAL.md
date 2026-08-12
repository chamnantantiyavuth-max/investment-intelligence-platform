# S9 RE-AUDIT VERDICT — Apple Rehearsal (Gemini DR v1.4 pilot)

**Stage:** S9 Research Audit / Re-Audit (after S7 corrections C1–C5 applied)
**Auditor:** org-auditor (Internal Auditor / Red Team)
**Task:** t_91eceed5 (run 42) · **Date:** 2026-08-12 23:33 UTC+7
**Inputs:** corrected essay (t_32b3949c) + CORRECTIONS-RECORD + frozen passes (Pass A 80e88c9a, Pass B f0ecb972, Gemini fa976b62/ce5a9226, S5 15861e87) + S7 findings F1–F5 + CRO (S8, b59ecd57)

---

## VERDICT: ✅ PASS — CLEAN (both artifacts)

- **S6 essay (corrected):** ✅ **CLEAN** — all 5 S7 findings (F1–F5) closed; §23.9 discipline satisfied; no new claims; no numeric-token drift; frozen-pass fidelity verified independently.
- **S8 CRO:** ✅ **PASS** (re-confirmed — unchanged since run-40 audit; canonical artifact b59ecd57 verified on disk; 1 MINOR advisory CRO-1 stands, non-blocking).

**SHA-256:** corrected essay `3496b06e522447163f308f37eb1bbcaa57cefeca4e9e4d2eae202805aaf2adc2` · original (untouched) `9f29f189aa7a95f136075ee005be1947685c3d7f911518c7d843dee5c20e66f8`

---

## 1. §23.9 Correction Discipline — PASS

| Requirement | Result |
|---|---|
| Original preserved byte-identical | ✅ re-hashed on disk = 9f29f189… exact (matches S7/S8/S9-run-40 records) |
| Corrected essay as NEW artifact | ✅ `S6-MAIN-ESSAY-APPLE-REHEARSAL-CORRECTED.md` (3496b06e…) |
| CORRECTIONS-RECORD.md with all fields | ✅ original SHA, reason (F1–F5), replacement output (old→new per record), actor (org-equity-analyst), timestamp (2026-08-12 23:26 UTC+7), workflow version (Gemini DR v1.4 pilot); CORR-001…005 (005 folded into 001, documented) |
| No changes beyond C1–C5 | ✅ full diff = exactly C1–C5 sites + namespace definition + file timestamp (12 line-changes); no numeric token changed |

## 2. Finding-by-Finding Closure (independent re-verification)

| S7 Finding | Required Correction | Closure Evidence (re-audit, not self-report) |
|---|---|---|
| **F1** BLOCKER — §2.4 new-claim "refund-adjusted 40.07% reflects real margin pressure absorbed" | **C1**: replace with frozen B F3 framing | ✅ `grep "refund-adjusted"` = **0**; `"reflects real margin pressure"` = **0**. §2.4 now: "Q3 Products GM 40.07% — the highest in the 5-yr window — is refund-contaminated (B F3)" + "no clean read on margin trend; the filing-visible margin-pressure direction is the R&D/capex signature (E3) plus the named NAND/DRAM/AI-compute supply risks (Item 1A)". Frozen Pass B F3 (line 74–76) read directly: "Products GM 40.07% (Q3) is the highest in the 5-yr window but includes tariff refunds…" — framing matches verbatim |
| **F2** BLOCKER — namespace collision G D1–D6 vs S5 D1–D6 + `[G1 D1]` misattribution | **C2**: define G-Dim1…6 once; rename all tokens | ✅ Namespace defined once (line 33): G-Dim1…6 = Gemini dimensions; D1–6 = S5 disagreements; G1–10 = S5 G-rows. `[G1 D1]` → `[G-Dim1; S5 A3; B V23]` (line 118). All 10 rename sites verified in full diff (118/122/128/130/136/160/187/204/206/280), incl. China row `(inside D3 share)` → `(inside G-Dim3 share)` (same defect class). `grep "G D[1-6]"` = **0**, `"G1 D1"` = **0** |
| **F3** MATERIAL — "25/25" double-count | **C3**: 24/25 + 1 PIT-stale | ✅ `"25/25"` = **0**; `"24/25"` = **1** (§6.1): "24/25 published-case claims reproduced-or-caveated + 1 PIT-stale (V13 intangibles, already corrected in §1.4); 0 contradicted". Matches frozen Pass B register line 60 verbatim: "21/25 fully reproduced, 3 caveated (V8/V9/V11), 1 point-in-time stale (V13)" (21+3=24 reproduced-or-caveated, +1 stale = 25, 0 contradicted — no double-count) |
| **F4** MINOR — unlabeled assessment line 37 | **C4**: append [A] [A VIEW 4, VIEW 9] | ✅ Line 39: "The business is not in financial distress by any filing-visible measure **[A] [A VIEW 4, VIEW 9]**". Support verified in frozen Pass A: VIEW 4 = Balance-Sheet Resilience (fortress liquidity, net cash ≈ $62B); VIEW 9 = "HIGH for balance-sheet resilience" — citation honest |
| **F5** MINOR — §2.4 [F] label mixing inference | **C5**: split [F]/[A] | ✅ §2.4 line 142: filing facts under **[F]** (Item 1A risks, R&D/capex signature, GM 40.07% fact), inference under **"Assessment [A]"** ("provides no clean read…", direction reading) — exactly one [A] assessment block |

## 3. No-New-Claims / Factual Fidelity / Source Lineage — PASS

- Full diff against original: only C1–C5 sites changed — **no new factual claims entered**; replacement text cites only frozen rows (B F3, E3/F5, Item 1A) already admitted.
- **38/38 arithmetic (S7) remains valid:** no numeric token changed in the diff (token-independent per S7); spot-checked key figures present & consistent with frozen passes: 109.4B (+16%), 416.16B, 112.01B, ~62B net cash, EPS 2.02, GM 50.1%, Services GM 75.62% (B F3: "FLAT y/y" — unchanged), Products GM 40.07%, R&D +32.5% / capex −28.2% (B F5).
- **Intangibles:** 20,342 @ 2026-06-27 (+83.4% YTD, −$992M QoQ) used throughout (§1.4, §2.5, §6, Appendix A); 21,334 appears **only** in "superseded / must not use / Q2-stale (B V13)" flagging context (4 occurrences, all negative references) — correct handling, not re-admission.
- **Word count:** 4,749 vs 4,680 original (+69 words = namespace definition + C1/C3 replacement text) — bounded editorial change, no scope creep.
- Frozen passes re-hashed on disk: Pass A `80e88c9a…` ✅, Pass B `f0ecb972…` ✅, Gemini wrapper `fa976b62…` ✅, S5 `15861e87…` ✅ — none altered.

## 4. CRO (S8 Opposing Thesis) — PASS (re-confirmed)

- Canonical artifact `S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL_1.md` re-hashed = **b59ecd57…** ✅ (matches parent metadata). Corrupted duplicate `5bd25094…` (encoding defects) still present in t_295cacba attachments — **S10 must use the `_1.md` canonical file only** (as flagged in run-40 verdict).
- Run-40 audit already verified: source lineage (all figures trace to frozen rows — V2 75.41%/42.17%, V7 75.62%, V23 regulatory, V16 buyback, F5 R&D/capex, V18 cash), factual fidelity, no-new-claims, must-not-contain all PASS. CRO file unchanged since — PASS stands. 1 MINOR advisory (CRO-1: "40%+ of gross profit" is FY25-derived V2; 9M framing = estimate) — advisory only, no correction required.

## 5. Residual Items / Handoff

1. **No open blockers.** Both artifacts clean → S10 (t_b032854f) released to proceed; must consume **corrected** essay (3496b06e) + **canonical** CRO (_1.md, b59ecd57).
2. **hotspot (unchanged):** S6-MAIN-ESSAY-APPLE-REHEARSAL* is the shared serial artifact for S6/S7/S8/S9/S10 — further edits (if any) must follow §23.9 (new file + CORRECTIONS-RECORD), never overwrite.
3. Process note (from run-40): DR template should add an explicit "corrections applied → re-audit" gate so the S6→S9 skip cannot recur.

---

*Re-audit complete: essay CLEAN, CRO PASS. All five S7 findings closed, §23.9 discipline verified, no new claims, no numeric drift, frozen-pass fidelity preserved.*
<!-- 2026-08-12 23:33 UTC+7 -->
