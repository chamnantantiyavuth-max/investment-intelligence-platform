# S9 — RESEARCH AUDIT / RE-AUDIT VERDICT
## Gemini Deep Research v1.4 — Apple Rehearsal (PILOT-NONCANONICAL)

**Task:** t_91eceed5 — [DR][CHILD] S9 — Research Audit / Re-Audit
**Auditor:** org-auditor (Internal Auditor / Red Team)
**Audit targets:** S6-MAIN-ESSAY-APPLE-REHEARSAL.md (t_7ac2d383) + S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL.md (t_295cacba)
**Date:** 2026-08-12
**Mode:** Hostile re-audit — assume every claim is wrong until it reproduces against frozen evidence. Portfolio-blind. Advisory only.

---

## 0. VERDICT (SUMMARY)

| Target | Verdict | Gate |
|---|---|---|
| **S6 Main Essay** | 🔴 **BLOCKED — NOT CLEAN** | **C1–C5 (S7 required corrections) WERE NEVER APPLIED.** Essay byte-identical to the S7-blocked version (SHA-256 `9f29f189…` unchanged). All 5 S7 findings remain live in the text. The S9 "after corrections" premise is FALSE. |
| **S8 CRO Opposing Thesis** | 🟢 **PASS — clean (1 MINOR advisory, non-blocking)** | Source lineage ✅ · factual fidelity ✅ · no-new-claims ✅ · must-not-contain ✅ · anti-anchoring declaration consistent ✅ |

**Pipeline consequence:** S9 cannot certify the essay. Per "re-audit until clean," the essay must receive C1–C5 (by the essay author, org-equity-analyst, with §23.9 CORRECTIONS-RECORD discipline) and S9 must re-run. **S10 (Facts Locked) must NOT release on the uncorrected essay.** The CRO is not blocked and remains valid after the essay correction (its challenge targets S6's ranking/confidence structure, which C1–C5 do not alter).

---

## 1. INTEGRITY CHECKS (evidence chain)

| Check | Method | Result |
|---|---|---|
| S6 essay integrity | `sha256sum` on disk vs S7-audited hash | 🔴 `9f29f189aa7a95f136075ee005be1947685c3d7f911518c7d843dee5c20e66f8` — **EXACT match to the S7-blocked version.** No correction was applied (workspace mtime 22:57 = pre-S7; attachments identical). |
| S8 CRO integrity | `sha256sum` workspace vs parent metadata | ✅ `b59ecd57…bc1` exact match (workspace + attachment `_1`) |
| S8 duplicate attachment | diff of the two attachment files | ⚠️ `attachments/t_295cacba/S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL.md` (SHA `5bd25094…`) = **earlier corrupted draft** (`ç13`, `±12`, `FIRY-PASS`, `salready`, broken em-dashes); canonical final = `…_1.md` (b59ecd57). Downstream (S10/S11) MUST use `_1`; the corrupted duplicate should be ignored/removed. |
| Word count S8 | `wc -w` | ✅ 2,429 (matches parent metadata) |
| Frozen-pass integrity (S5-managed) | prior S7/S5 hash verification | ✅ Pass A `80e88c9a…d74e`, Pass B `f0ecb972…cc139f`, Gemini content `ce5a9226…dc0` — verified exact in S5/S7 runs; no re-hash needed since none of these files changed (mtime prior to S5 freeze). |
| S5 reconciliation | `sha256sum` | ✅ `15861e87…` matches parent metadata |

---

## 2. S6 ESSAY — FINDINGS (re-verified against the current file)

All five S7 findings **persist unchanged** in the essay file (verified by full re-read at 2026-08-12; hash identical to S7-audited bytes — no rework occurred).

### 🔴 F1 (BLOCKER) — new-claim / semantic-fidelity violation — STILL PRESENT
- §2.4 line 140: *"…and the Q3 FY26 **refund-adjusted Products GM 40.07% reflects real margin pressure absorbed**."*
- Unchanged. Contradicts Pass B F3 ("highest in the 5-yr window, refund-contaminated") and the essay's own §1.3 line 85 ("refund-contaminated"). "Refund-adjusted" is also terminologically wrong (40.07% is refund-*including*).
- **C1 NOT APPLIED.**

### 🔴 F2 (BLOCKER) — citation-namespace collision + misattribution — STILL PRESENT
- Line 116: `[3P] [G1 D1]` (DMA/CTC content misattributed; G1 in S5 = forward-GM guide) — unchanged.
- "G D1…D6" Gemini-dimension tokens still in text: lines 116, 120, 126, 128, 134, 158, 185, 205, 278. No "G-Dim1…6" namespace defined anywhere in the file (grep `G-Dim` → 0 hits in essay).
- **C2 NOT APPLIED.**

### 🟠 F3 (MATERIAL) — register double-count — STILL PRESENT
- §6.1 line 232: *"25/25 published-case claims reproduced-or-caveated by Pass B; 1 PIT-stale"* — unchanged; implies 26 slots for 25 claims. Correct: 21 reproduced + 3 caveated + 1 PIT-stale = 24+1, 0 contradicted (Pass B register V1–V25).
- **C3 NOT APPLIED.**

### 🟡 F4 (MINOR) — unlabeled assessment — STILL PRESENT
- Line 37: "The business is not in financial distress by any filing-visible measure." — no `[A] [A VIEW 4, VIEW 9]` appended.
- **C4 NOT APPLIED.**

### 🟡 F5 (MINOR) — [F] label mixed with inference — STILL PRESENT
- Line 140 paragraph opens `[F] [C2, E3]:` yet contains the analyst inference (F1 clause). Label mixing persists.
- **C5 NOT APPLIED.**

### §23.9 CORRECTION-DISCIPLINE CHECK — FAIL
- No CORRECTIONS-RECORD exists for the S6 essay (searched all DR attachments/workspaces for correction artifacts: none). Constitution §23.9 + AI-ORG-OPERATING-STANDARD v0.1 require: preserve original record + correction reason + replacement output + actor + timestamp + workflow version. Original IS preserved (unchanged file) ✅, but no correction, no reason record, no actor/timestamp ❌.
- **Root cause of the false premise:** S6 released BOTH S7 (cross-exam) and S8 (CRO) simultaneously as children; S7 found blockers at 23:03, but no correction task was created between S7 and S9, and S9 was released anyway. The pipeline skipped the correction step.

### What still PASSES (S7 acquittals carry over — bytes identical)
- 38/38 arithmetic re-derivations (S7, same bytes) ✅
- No averaging (D1–D6 unreconciled; China ranges kept separate with conflict flag) ✅
- Appendix B respected in-text (21,334 only in superseded/must-not-use context) ✅
- Anti-anchoring (no claim traceable only to SRC-P1/P2) ✅
- PIT discipline (FD #58) ✅
- No NEW claims entered during the (nonexistent) rework — file unchanged ✅

---

## 3. S8 CRO OPPOSING THESIS — AUDIT RESULT

### Source lineage — PASS
Every figure the CRO cites was spot-verified against frozen Pass B / Pass A rows:
- FY25 Services GM **75.41%**, gross-profit share **42.17%** → Pass B V2 ✅ (`82,314/195,201 = 42.17%`; `(109,158−26,844)/109,158 = 75.41%`)
- Q3 FY26 Services GM **75.62% flat y/y** → Pass B V7 ✅ (23,245/30,739 = 75.62%; "flat year over year" confirmed V7 line 75)
- 9M FY26 Services **$91.73B / 25.2% / ~76.3% GM** → Pass A VIEW 2 + Pass B V7 ✅ (91.73B, 25.2%, 76.3% vs 75.5% +0.8pp mix-driven)
- Q3 Services **+12.1% vs total +16%**; 9M Services **+14.1% vs total +16.2%** → Pass A VIEW 2 ✅
- Regulatory set (€500M DMA fine + C&D, DOJ suit, Epic injunction, 9th Cir. Dec 11 2025, SCOTUS cert Jun 30 2026, Google-licensing risk) → Pass B V23 ✅
- Q3 total GM 50.1% incl. ~2pp refunds; ex-refund ≈48.1% derived; FY25 46.9% → Pass B V6 + Pass A ✅
- EPS $2.02 +29% incl. ~$0.11 refunds → Pass B V17 ✅
- Cash+securities $146.5B, debt ≈$84.3B, net cash ≈$62B → Pass B V18 + B3 ✅ (146,517 − 84,300 = 62.2B)
- 9M FY26 R&D $34.035B +32.5% ≈ FY25 full-year; capex −28.2% → Pass B F5 ✅
- 9M buyback coverage 53.07% vs 86.33% → Pass B V16 ✅ (62,094/116,996 = 53.07%; 70,579/81,754 = 86.33%)

### Factual fidelity — PASS
No figure contradicts a frozen view. All derived metrics trace to filing arithmetic reproduced by Pass B.

### No-new-claims (semantic fidelity) — PASS
The CRO's challenges are weighting/ranking/confidence challenges over the same admitted evidence (regulatory #1 vs AI #2 re-ranking; convergence-as-shared-framing; confidence inversion). No new factual/causal/competitive/financial claim beyond the frozen views + S5.

### Must-not-contain (S6 Appendix B, binding for S8) — PASS
- No intangibles 21,334 / +92.32% anywhere ✅
- No averaged IDC/Counterpoint China share ✅ (no China-share claim at all)
- No unlabeled forward-GM / DRAM-NAND / CEO-transition as fact ✅ (take rates 5–17% and TAC ~$20B appear only as labeled [3P]; succession mentioned only as a resolution-path item)
- No recommendation / target price / portfolio direction ✅

### Anti-anchoring — PASS (declaration consistent)
Declares SRC-P1 (published case) + SRC-P2 (published CRO essay) NOT read; content is derived from challenge brief + S6 + S5 + frozen passes, matching the S8 challenge brief's scope and §9 prohibitions. No fingerprint of published-companion language in the text.

### Findings
| # | Severity | Finding |
|---|---|---|
| CRO-1 | 🟢 MINOR (advisory, non-blocking) | Line 16: "more than 40% of gross profit by mix … [D]" — the 40%+ figure is directly *derived* only for FY25 (42.17%, V2); for 9M FY26 it is an estimate (Pass A VIEW 8 "~40%+ … by mix" is an assessment). Label is defensible ([D] via FY25 derivation) but S10 fact-packet should cite V2 for 42.17% and keep the 9M framing as estimate. No correction required for the S8 artifact itself. |

### CRO verdict: **PASS** — no blockers, no required corrections.

---

## 4. REQUIRED ACTIONS (for the pipeline, not the audit)

1. **Create correction task** for the S6 essay author (org-equity-analyst): apply C1–C5 per S7 findings, with §23.9 CORRECTIONS-RECORD (preserve original `9f29f189` untouched, document reason/actor/timestamp/workflow version, produce corrected essay + record).
   - C1: §2.4 line 140 — delete/replace the "refund-adjusted … reflects real margin pressure absorbed" clause with the B F3 framing; do not re-insert "refund-adjusted 40.07%".
   - C2: define G-Dim1…G-Dim6 namespace once; fix `[G1 D1]` → `[G-Dim1; S5 A3; B V23]`; rename all "G D1…D6" → "G-Dim1…G-Dim6" (lines 116, 120, 126, 128, 134, 158, 185, 205, 278).
   - C3: §6.1 → "24/25 reproduced-or-caveated + 1 PIT-stale (0 contradicted)".
   - C4: line 37 append `[A] [A VIEW 4, VIEW 9]`.
   - C5: split [F]/[A] labels in §2.4 after C1.
2. **Re-run S9 re-audit** on the corrected essay (same audit scope: source lineage, factual fidelity, no-new-claims, §23.9 discipline). The corrected essay must keep the 38/38 arithmetic intact (token-independent rephrases only).
3. **S10 (Facts Locked) release order:** only after the re-audit returns CLEAN. S10 must read the canonical S8 attachment `S8-CRO-OPPOSING-THESIS-APPLE-REHEARSAL_1.md` (b59ecd57), NOT the corrupted duplicate (5bd25094).
4. CRO-1 advisory: S10 fact-packet should source the 40%+ gross-profit-share claim to V2 (42.17% FY25 derived) with the 9M framing labeled as estimate.

---

## 5. HANDOFF NOTES

- **To S10 (t_b032854f, org-ic-secretary):** DO NOT release until S9 re-audit is CLEAN. Use canonical S8 `_1` attachment. Carry CRO-1 advisory.
- **To synthesis parent (t_68d2824b, org-cos):** pipeline sequencing defect confirmed — correction step was skipped between S7 (23:03) and S9 release. Recommend the DR template add an explicit "corrections applied → re-audit" gate between Cross-Exam and Audit so this cannot recur.
- **To Founder:** the essay's evidentiary load remains SOUND (S7 acquittals carry over); corrections C1–C5 are editorial. The blocker is process (corrections never executed), not evidence.

---

*S9 audit verdict produced by org-auditor — all checks re-run against on-disk artifacts at 2026-08-12. PILOT-NONCANONICAL — calibration only, not investment truth.*

<!-- 2026-08-12 23:45 UTC+7 -->
