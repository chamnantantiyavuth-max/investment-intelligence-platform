# Corrections Record — RM-2026-0001 (audit response)

**Date:** 2026-08-06 16:47 UTC+7
**Trigger:** Audit Note (MAJOR FINDINGS) + Cross-Examination findings, both produced 2026-08-06 16:36–16:47 UTC+7
**Rule:** Constitution §23.9 — never rewrite history. Original metadata preserved; corrections appended/recorded here.

## P-1 / T-1 — Footer timestamp defect (MAJOR, fixed)

Original footers in this workspace were future-dated relative to the actual write clock:

| File | Original footer (incorrect) | Actual write time (verified 2026-08-06) |
|---|---|---|
| source-inventory.md | 2026-08-06 20:50 UTC+7 | 16:34 |
| evidence-log.md | 2026-08-06 21:15 UTC+7 | 16:30 |
| evidence-quant-appendix.md | 2026-08-06 21:20 UTC+7 | 16:34 |
| first-pass/README.md | 2026-08-06 21:25 UTC+7 | 16:35 |
| main-research-essay.md | 2026-08-06 21:40 UTC+7 | 16:35 |

Fix: footers corrected to actual times; this record preserves the erroneous values. No conclusion or figure was affected — the defect was in write-time metadata only.

## P-2 — Anti-anchoring evidence (MINOR, fixed)

Dispatch record added to `first-pass/README.md`: delegation job `deleg_89b7126c`, model gpt-5.6-sol (openai-codex), dispatched 2026-08-06 16:31:21, completed 16:34:15 (174.9s), 6 leaf tasks, each restricted to the shared evidence packet (evidence-log.md + /tmp/apl-evidence/ raw filings); per-task input allowlist + completion records now retained in the delegation cache (live transcripts: task-0..5 logs) and the six view files.

## P-3 / O-3 — Workflow sequencing (MAJOR, resolved)

The audit ran while cross-examination and the CRO opposing essay were still executing (dispatched 16:36, completed 16:47). Both artifacts now exist and are persisted:
- `cross-examination.md` (10 essay corrections required — all applied, see below)
- `cro-opposing-essay.md` (strongest coherent opposing essay)
- `audit-note.md` (this audit, kept verbatim)
The essay's "companion artifact" statement is now accurate. Essay status updated from "pre cross-examination" to "post cross-examination, corrections applied."

## O-1 — Q3 FY2026 10-Q (MAJOR, fixed)

Q3 FY2026 10-Q (accession 0000320193-26-000020, filed 2026-07-31) downloaded + converted (96KB text, /tmp/apl-evidence/aapl-10q-q3fy26.txt). Key additions reconciled against the 8-K:
- Legal proceedings detail (Item 1): €500M DMA fine dated 2025-04-23 + cease-and-desist; DMA Article 6(4) preliminary findings (fines up to 10% of worldwide net sales); DOJ antitrust suit (filed 2024-03-21); Epic 2021 Injunction → 2025 Injunction (2025-04-30) → Ninth Circuit upheld in part (2025-12-11) → Supreme Court granted certiorari 2026-06-30; Google search-licensing remedies risk (D.C. District Court 2025-09-02)
- New risk factors (Item 1A): NAND/DRAM/semiconductor supply constraints "expected to intensify"; AI compute dependence (third-party cloud, constrained capacity); developer-support dependence + minority share; App Store commission erosion via alternative distribution; DMA interoperability may prevent launching features such as Siri AI in certain jurisdictions; China data-localization rules; Google licensing revenue risk
- Buybacks (Item 2): May 2025 $100B program (as of 6/27/26 remaining $38.0B) + April 30, 2026 additional $100B program; May 2026 ASRs up-front $10.0B; Q3 FY26 open-market purchases 53,143K shares (~$15.8B at ~$297 avg)
- Shares outstanding: 14,594,180,000 as of 2026-07-17 (vs 14,773,260,000 at 2025-09-27)
- Reconciles to 8-K: revenue/GM/NI/EPS/segment figures identical

## Evidence integrity corrections (from audit + cross-exam)

1. **€500M fine sourcing:** cited as 10-K "Item 1A" in essay — corrected to **10-K Item 3 / 10-Q Item 1 (Legal Proceedings)**, and added to evidence log + appendix source register.
2. **Buyback terminology:** $90.7B is cash-flow-statement payments; 10-K Note 10 discloses 402M shares repurchased "for $89.3B" — essay/appendix now say "cash paid for repurchases" and note the settlement-timing difference.
3. **Red Team Note 16 → Note 10:** `first-pass/06-red-team-auditor.md` mislocated the $89.3B disclosure; corrected.
4. **Derived labels:** every derived figure in essay + appendix now explicitly marked "derived" with formula or input citation (GM bridge, R&D/revenue growth comparison, buyback/OCF ratio, normalized margin).
5. **GM bridge formula:** published — mix-first sequential bridge: mix ≈1.37pp + within-segment ≈1.40pp (path-dependent; alternative ordering 1.55pp/1.23pp; total invariant 2.77pp).
6. **"Survive a recession / strong dollar / tariff cycle" assertion:** reframed as analytical hypothesis, not demonstrated fact (no stress evidence in packet).
7. **"None of the compound-break ingredients present":** corrected — regulatory opening already observable (DMA + €500M fine + Epic injunctions); AI disintermediation not demonstrated; combined scenario not materialized at moat-breaking scale.
8. **Essay confidence calibration (cross-exam items 1–10):** Share of Mind recast as low-confidence hypothesis; switching cost "strongest mechanism" → "plausible candidate, unquantified"; Services margin = evidence of present monetization, not proof of moat strengthening; Cost Advantage/Network Effect explicitly unverified; "normalized 48.1%" → "approximately 48.1% excluding stated tariff-refund contribution"; OCF attribution → "year-over-year changes in operating-asset and liability cash-flow adjustments"; AI/regulatory/rent-impairment separated into testable mechanisms.

## Re-audit

Audit note required: "rerun this audit after the essay is revised." Re-audit delegation `deleg_127f9b61` (gpt-5.6-sol, dispatched 2026-08-06 16:51, completed 16:56) returned **REMAINS BLOCKED** with 3 bounded MAJORs (RA-1 derived formulas incomplete; RA-2 residual thesis/conclusion language; RA-3 premature attestation in this record) + 1 MINOR (RA-4 source inventory). All four corrections applied 2026-08-06 16:58: (1) derived labels + formulas for R&D/revenue growth + buyback/OCF ratio added to essay; (2) thesis/conclusion "Cost Advantage real" → "possible relative advantage — unverified"; "Network Effect real" → "plausible but indirect, unquantified, unverified"; (3) this record corrected to carry actual re-audit provenance (this edit); (4) source inventory + evidence-log header refreshed with 10-Q working files. Verdict recorded in `re-audit-note.md` (persisted 2026-08-06 16:58). Final targeted confirmation dispatched after corrections (delegation `deleg_2e47ba02`, gpt-5.6-sol).

<!-- 2026-08-06 16:47 UTC+7 -->
