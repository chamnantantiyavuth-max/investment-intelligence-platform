# S11 — Editorial A/B Comparison & Verdict (Gemini Thai Editorial A/B)

**Task:** t_5ac2b6a4 · **Stage:** S11 — Gemini Thai Editorial A/B (§21, v1.4)
**Author:** org-ic-secretary (Managing Editor / Publication Controller, §17)
**Date:** 2026-08-13 00:15 UTC+7 · **Mode:** PILOT-NONCANONICAL — calibration rehearsal on a published Apple case. Not investment truth. Portfolio-blind. Advisory only.
**Anchor:** IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md §16 (editorial prompt), §18 (F1/F2), §19 (P1–P5), §21 (A/B validation)
**Analytical input (both variants):** S10 Publication Fact Packet (SHA-256 `37b4158c…`) + selected primary sources (§15) — per S10 handoff note 1, no other analytical input.

## Candidates

| | Candidate A — Gemini editorial | Candidate B — Hermes / IC Secretary editorial |
|---|---|---|
| Writer | Gemini API agent `deep-research-max-preview-04-2026` (Interactions API, background job) — the pilot's external Gemini lane | org-ic-secretary (Managing Editor, §17) — direct editorial |
| Dispatch | Job `v1_Chd1Nko…`, prompt SHA-256 `d726a867…`, output SHA-256 `3c83fa5f…` | — (in-file declaration) |
| Analytical input | Packet embedded verbatim in prompt; no tools/grounding | Packet only |
| Artifact | `S11-CANDIDATE-A-GEMINI-THAI-EDITORIAL.md` | `S11-CANDIDATE-B-HERMES-THAI-EDITORIAL.md` |
| Editor pass | Minimal correction pass E1–E6 (Appendix A2 — objective defects only, no style rewrite) | Direct editorial (no prior draft) |
| Raw (frozen) | `S11-A-GEMINI-EDITORIAL-RAW.md` + `S11-A-INTERACTION-RAW.json` + `S11-A-PROVENANCE.json` | — |
| Body length | ~13.7K chars (article body) | ~8.3K chars (article body) |

---

## 1. Gate results — P1–P5 (both variants, same packet)

| Gate | Candidate A (Gemini) | Candidate B (Hermes/IC Sec) |
|---|---|---|
| **P1 Research Integrity** — thesis matches Facts Locked; no rejected claim; uncertainty + dissent preserved | ✅ PASS — "bent, not broken" conditional + dissenting view (profit-pool erosion, present-tense, no-defection-needed) + confidence inversion (HIGH liquidity ≠ LOW-MEDIUM moat); thesis-break conditions (1)–(5) + CRO-weakening condition; forbidden tokens 0 | ✅ PASS — same thesis + dissent + inversion; dedicated uncertainty section; thesis-break (a)–(e) summarized; forbidden tokens 0 |
| **P2 Fact Fidelity** — F1 numeric sweep vs T01–T44; F2 writer-side; no new claim | ✅ PASS — F1: 0 flagged of 162 unique tokens; forbidden scan 0/4; third-party items labeled (Q4 GM guide, CEO transition, DRAM/NAND/BoM, DAU, TAC, China shares); F2 writer-side clean (formal F2 → S12) | ✅ PASS — F1: 0 flagged of 132 unique tokens; forbidden scan 0/4; third-party items labeled; F2 writer-side clean (formal F2 → S12) |
| **P3 Natural Thai** | ✅ PASS (with note) — Thai-native composition, no calques; BUT explanatory glosses + metaphor-dense (ปราการเหล็ก/ขุมทรัพย์/สมรภูมิ/ท่อโง่ๆ) give a briefing/academic tint; trimmed in editor pass E6 | ✅ PASS — Thai-native analyst voice; English terms only where natural; minimal metaphor; zero over-explanation |
| **P4 Causal Narrative** | ✅ PASS — both mechanisms explained as chains; opening 10–15% carries all 5 elements; numbers carry "so what"; concept-definition detour (3 numbered definitions) slightly delays the argument | ✅ PASS — narrative arc on chains 1–2; opening delivers the 5 elements tightly; every number immediately followed by its implication |
| **P5 Publication Craft** | ✅ PASS (with note) — headline = structural-risk story; 6 headings (at guidance max); bullet list only for the third-party disclosure set (helpful); no AI clichés; no internal jargon; disclaimer present | ✅ PASS — headline = moat-erosion story; 3 headings; zero bullets; no clichés; no internal jargon; disclaimer present |
| **Overall** | ✅ PASS (publishable after E1–E6) | ✅ PASS (publishable as-is) |

## 2. A/B comparison (§21 dimensions)

| Dimension | Candidate A (Gemini) | Candidate B (Hermes/IC Sec) | Edge |
|---|---|---|---|
| **Natural Thai** | Good, but reads partially "explained-to-reader": heavy parenthetical glosses, English labels kept, metaphor-dense. After E6 trims it reads naturally. | Excellent — written in Thai from the argument; English finance terms appear only where a Thai analyst would naturally use them (moat, switching cost, capex, gross margin). | **B** |
| **Clarity** | Very high — exhaustive; every concept defined; nothing left implicit. | High — one idea per paragraph; sharper links between evidence and implication. | A (completeness) / B (directness) — **tie**, different flavors |
| **Causal flow** | Strong; mechanisms explained in depth; but the 3-concept definition section is a pedagogy detour before the argument moves. | Strongest — the piece is built as a single causal arc (numbers → why they mislead → where the real risk is → what would falsify it). | **B** |
| **Concision** | ~13.7K chars, 6 headings, 1 bullet set. Comprehensive but ~1.6× longer than B. | ~8.3K chars, 3 headings, 0 bullets. Every sentence earns its place. | **B** |
| **Investment usefulness** | Very high — most complete coverage: includes DAU, TAC, HarmonyOS, China share ranges, inventory + intangibles watch items, falsification conditions. | High — decision-relevant selection: margin quality, Services value-at-risk, buyback signal, AI-expensing, thesis-break; omits some third-party color (kept out deliberately to protect the narrative). | **A** (breadth) / **B** (focus) — depends on reader |
| **Preservation of uncertainty** | Strong — explicit third-party list, 2 numbered uncertainty items, falsification conditions. | Strong — dedicated uncertainty section + labeled third-party items; slightly less granular. | **A** (granularity) / **B** (integration) |
| **Factual/semantic fidelity** | F1 clean (0 flags); F2 writer-side clean; editor pass touched no tokens | F1 clean (0 flags); F2 writer-side clean | **tie** |

**Character summary:** A is the thorough, systematic, explanatory briefing — completeness-first, slightly academic, longer. B is the sharp, causal, focused article — argument-first, concise, Thai-analyst voice. Both are factually locked to the same packet and pass all five gates.

## 3. Chosen variant & recommendation

**RECOMMENDATION: Candidate B (Hermes / IC Secretary editorial) as the publication variant for this rehearsal.**

Reasoning (against the §21 dimensions that matter most for a professional Thai investor audience — natural Thai, clarity, causal flow, concision, investment usefulness):
1. B reads as originally written in Thai for an experienced investor; A (even after gloss trims) carries a briefing/translated tint and over-explains terms the target reader already knows.
2. B delivers the same thesis, evidence, uncertainty, and dissent in ~60% of the length with a tighter causal arc — higher signal density per minute of reading.
3. P1–P5 pass for both; on P3/P4/P5 craft dimensions B is the cleaner publication.

**Conditions and caveats (calibration honesty):**
- This is the FIRST A/B sample of the calibration series (§21: first 3–5 publications). One sample is not a trend. The verdict is a recommendation, not a lock-in.
- **Founder preference is the decisive signal (§21).** If the Founder prefers the explanatory-comprehensive style (A) for Thai publications — completeness, defined terms, structured briefing — then A wins on communication quality regardless of this recommendation.
- A retains unique value as the **completeness reference**: DAU/TAC/HarmonyOS/China-share detail and the granular falsification list are in A if the publication wants maximum coverage; B's focus choice is a deliberate editorial trade.
- If Gemini wins 2+ of the next calibration rounds and keeps passing fidelity gates → make Gemini the default Thai prose generator and stop routine A/B (§21). If Hermes keeps winning → retain Hermes default, use Gemini selectively (e.g., when completeness > concision).

**Next step:** S12 (t_300afea0, org-auditor) runs the formal F2 semantic-fidelity gate on the chosen variant (B) — and may cross-check A. Synthesis parent (t_68d2824b) consumes this comparison + both variants.

## 4. Handoff notes

- Article bodies are delimited in each artifact (`# ARTICLE A` … `## Appendix A1`; `# ARTICLE B` … `## Appendix B`). Neither body contains internal jargon (no S-IDs, t_ IDs, FD numbers, § references, evidence-class labels, role names).
- Both variants carry the reader-facing disclaimer; neither contains recommendation language.
- Provenance for A (raw output, prompt, job id, hashes) is on disk in this workspace for audit.
- f1_checker.py (this workspace) reproduces the F1 sweep on either variant.

*PILOT-NONCANONICAL — calibration artifact on a published case; neither variant is investment truth; no recommendation language in either. Prepared by org-ic-secretary as Managing Editor (§17).*
<!-- 2026-08-13 00:15 UTC+7 -->
