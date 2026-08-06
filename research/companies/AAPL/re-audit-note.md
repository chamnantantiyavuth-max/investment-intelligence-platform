# Re-Audit Note — RM-2026-0001

## 1. Correction verification

### First-audit required corrections

| # | Required correction | Status | Re-audit evidence | Severity |
|---:|---|---|---|---|
| 1 | Correct footer timestamps and preserve prior values under Constitution §23.9 | **APPLIED** | The five footers now show 16:30–16:35 UTC+7 (`source-inventory.md:35`, `evidence-log.md:154`, `evidence-quant-appendix.md:130`, `first-pass/README.md:29`, `main-research-essay.md:78`). `CORRECTIONS-RECORD.md:7-19` preserves each original future-dated value and explains the correction. Git history confirms the original values and their later replacement in commit `6f140d1`. | — |
| 2 | Retain anti-anchoring dispatch evidence | **APPLIED** | `first-pass/README.md:5-11` records job `deleg_89b7126c`, model/provider, dispatch and completion times, six-task completion, input allowlist, isolation statement, output locations, and retained task-log location. This satisfies the specifically required README dispatch record. | — |
| 3 | Persist cross-examination and a coherent CRO opposing essay | **APPLIED** | `cross-examination.md` contains claim-by-claim hostile examination and ten required corrections. `cro-opposing-essay.md` is a standalone alternative causal thesis distinguishing ecosystem persistence from rent persistence and tracing years 1 through 5. Both files are tracked in commit `6f140d1`. | — |
| 4 | Correct the companion-artifact statement and mark the essay post-cross-examination | **APPLIED** | `main-research-essay.md:4` identifies v2 as post-cross-examination. Lines 56-58 point to the existing `research/companies/AAPL/cro-opposing-essay.md` and accurately summarize its disagreement. | — |
| 5 | Extract and reconcile the Q3 FY2026 10-Q | **APPLIED** | `evidence-log.md:90-112` records Part II Item 1 legal proceedings, Item 1A additions, Item 2 repurchases, and 14,594,180,000 shares outstanding. Direct inspection of accession `0000320193-26-000020` confirmed the €500M fine, $38.0B remaining under the May 2025 program, the additional $100B program, $10.0B ASRs, and share count. The 10-Q and 8-K contain matching $109,417M revenue, $54,770M gross profit, $29,789M net income, $2.02 diluted EPS, $78,678M Products revenue, $30,739M Services revenue, $116,996M nine-month OCF, and $62,094M repurchases. The disclosed open-market rows also reconcile to 53,143K shares: 26,920K + 26,223K, approximately $15.77B. | — |
| 6 | Correct €500M source lineage and Red Team Note 16 reference | **APPLIED** | The fine is recorded in `evidence-log.md:70,94-96`, `evidence-quant-appendix.md:14-16,99-107`, and `main-research-essay.md:42,68-70` as 10-K Item 3 / 10-Q Part II Item 1 Legal Proceedings. Direct filing inspection confirmed the amount, 2025-04-23 date, cease-and-desist order, and Article 6(4) preliminary findings. `first-pass/06-red-team-auditor.md:11` now cites Note 10 and expressly records the Note 16 correction. | — |
| 7 | Explicitly label derived figures and publish formulas | **PARTIAL** | The margin bridge is now identified as derived, gives the mix-first ordering, reports 1.37pp mix plus 1.40pp within-segment, and discloses path dependence (`main-research-essay.md:31`); re-performance produced 1.3734pp and 1.4007pp, with the alternative ordering at 1.5458pp and 1.2282pp. The refund adjustment is also stated as reported 50.1% less approximately 2pp, or about 48.1% (`:25,54`). However, the R&D/revenue comparison at `:19` is neither claim-level labeled “derived” nor accompanied by formulas, and the 81.4% buyback/OCF ratio at `:35` is labeled derived but has no published formula. Required formulas remain `(34.550 / 21.914) − 1 = 57.66%`, `(416.161 / 365.817) − 1 = 13.76%`, and `90.711 / 111.482 = 81.37%`. The blanket attestation at `:76` therefore remains inaccurate. | **MAJOR** |
| 8 | Distinguish cash paid for repurchases from transaction value | **APPLIED** | `main-research-essay.md:35,54`, `evidence-log.md:126,130,152`, and `evidence-quant-appendix.md:34,39,121` distinguish $90.711B of cash-flow-statement payments from Note 10’s $89.3B transaction value for approximately 402M shares and attribute the difference to settlement timing. Direct 10-K inspection confirmed Note 10’s wording. | — |
| 9 | Reframe recession/strong-dollar/tariff survival as a hypothesis | **APPLIED** | `main-research-essay.md:62` explicitly calls survival an “analytical hypothesis, not a demonstrated finding” and discloses that no stress test or scenario bridge was run. | — |
| 10 | Reconcile the compound-break conclusion | **APPLIED** | The thesis and conclusion distinguish observable regulatory opening and tariff exposure from undemonstrated AI disintermediation and state that the combined scenario has not reached moat-breaking scale (`main-research-essay.md:9,42,62`). | — |
| 11 | Preserve advisory-only, portfolio-blind, no-valuation, and no-composite boundaries | **APPLIED** | `main-research-essay.md:5` explicitly states advisory-only and portfolio-blind status. No reviewed artifact contains a price target, valuation output, allocation instruction, buy/sell recommendation, portfolio data, or composite moat score. | — |

### Additional cross-examination corrections

| Cross-examination correction | Status | Re-audit evidence | Severity |
|---|---|---|---|
| Share of Mind must be a plausible low-confidence hypothesis, not inferred pricing power | **APPLIED** | `main-research-essay.md:15` calls it a plausible low-confidence mechanism consistent with revenue and margin resilience, discloses absent brand/retention evidence, and avoids using pricing power as its proof. The generic reference to pricing power at `:52` is explicitly categorized as a hypothesis rather than a filing-proven fact. | — |
| Switching cost must be an unquantified plausible candidate | **APPLIED** | `main-research-essay.md:17` uses the required “plausible candidate” framing, states that strength and rank are unquantified, and identifies missing migration, retention, cohort, and multi-device evidence. | — |
| Separate AI disintermediation, regulatory opening, and rent impairment into testable legs | **APPLIED** | `main-research-essay.md:39-48` treats the mechanisms separately, describes independent evidence routes, and identifies Services growth, gross margin, transaction initiation, developer priority, and control over identity/payments as outcome indicators. | — |
| Replace “normalized 48.1%” with a refund-excluded arithmetic description | **APPLIED** | `main-research-essay.md:25,54` says reported gross margin less the stated approximately 2pp tariff-refund benefit was about 48.1%; it does not describe 48.1% as a normalized steady-state margin. | — |
| Describe the OCF attribution as operating-asset and liability cash-flow adjustments | **APPLIED** | `main-research-essay.md:33` uses that exact accounting characterization, identifies the included adjustment categories, and cautions that some changes may reflect growth or settlement patterns rather than purely reversible timing. | — |
| Treat Services margin as present monetization, not proof of moat | **APPLIED** | `main-research-essay.md:31-33` calls the figures evidence of increasing Services mix and present monetization and expressly says they are not proof of a stronger moat or deeper attachment. | — |
| Cost Advantage must remain unverified | **PARTIAL** | The detailed section is corrected to “a possible relative advantage—unverified against competitor unit economics” (`main-research-essay.md:25`). The thesis nevertheless still says “Cost Advantage and Efficient Scale are real” (`:9`), contradicting the corrected evidence calibration and the cross-examination disposition. | **MAJOR** |
| Network Effect must remain plausible, indirect, and unverified | **PARTIAL** | The detailed section correctly says “plausible,” “unquantified,” and not separable from other mechanisms (`main-research-essay.md:23`). The conclusion nevertheless calls it “a real but unquantified” network effect (`:62`), restoring the unsupported certainty the cross-examination required removing. | **MAJOR** |

## 2. Fresh findings

### RA-1 — Derived-figure correction remains incomplete (**MAJOR**)

`CORRECTIONS-RECORD.md:47` claims that every listed derived figure now has an explicit label and formula or input citation, while `main-research-essay.md:76` similarly attests that derived figures are marked in the text. The R&D/revenue growth comparison at `main-research-essay.md:19` has no derived label or formula, and the buyback/OCF ratio at `:35` lacks the required division formula. The arithmetic is correct—57.66%, 13.76%, and 81.37% on re-performance—but the explicit first-audit evidence-control correction was not fully implemented.

### RA-2 — Residual thesis and conclusion language contradict the cross-examination corrections (**MAJOR**)

The body appropriately weakens Cost Advantage and Network Effect at `main-research-essay.md:23-25`, but the controlling thesis still calls Cost Advantage “real” at `:9`, and the controlling conclusion calls Network Effect “real” at `:62`. These are not harmless historical quotations: they are live thesis statements that contradict the evidence limits and `CORRECTIONS-RECORD.md:51`’s claim that the unverified formulations were applied. The residual language materially overstates two moat mechanisms that the filing evidence cannot isolate or benchmark.

### RA-3 — Corrections record prematurely attests that this re-audit was already persisted (**MAJOR**)

`CORRECTIONS-RECORD.md:53-55` states in completed past tense that a re-audit delegation was dispatched and that its verdict was recorded in `re-audit-note.md`. Direct inspection found no such file in the artifact set, and it is not tracked by Git. The record must not assert completion or persistence before the re-audit note actually exists; after this note is persisted, the record should carry the real job/provenance fields and timestamp rather than a prewritten completion claim.

### RA-4 — Source inventory metadata is stale after the 10-Q correction (**MINOR**)

Although `source-inventory.md:13` marks the Q3 10-Q extracted and reconciled, its working-file inventory at `:25-28` omits both the downloaded HTML and converted 10-Q text, and its completion log at `:32-34` still describes only the 8-K/XBRL evidence build. Likewise, the primary-source list at `evidence-log.md:3-6` omits the 10-Q despite the later §6b extraction. The 10-Q evidence itself is present and verified, so this is a source-register completeness defect rather than a substantive evidence omission.

## 3. Overall verdict

## **REMAINS BLOCKED**

The corrected artifact set is not yet cleared for Secretary synthesis or Founder review because one of the eleven first-audit corrections remains only partial, two required cross-examination calibrations remain contradicted in the thesis/conclusion, and the corrections record contains a false completed re-audit attestation.

### Required corrections

1. Add claim-level `derived` labels and explicit formulas for:
   - R&D growth: `(34.550 / 21.914) − 1 = 57.66%`;
   - revenue growth: `(416.161 / 365.817) − 1 = 13.76%`;
   - FY2025 buyback/OCF ratio: `90.711 / 111.482 = 81.37%`.
   Then narrow `main-research-essay.md:76` and `CORRECTIONS-RECORD.md:47` so their attestations exactly match what is present.
2. Change the thesis at `main-research-essay.md:9` from saying Cost Advantage is real to the same possible/unverified formulation used in the body.
3. Change the conclusion at `main-research-essay.md:62` from “a real” Network Effect to a plausible, indirect, unquantified, and unverified formulation.
4. Persist the actual re-audit artifact before asserting that it exists; append the real dispatch/completion provenance and correct the premature statement in `CORRECTIONS-RECORD.md:53-55` under the §23.9 correction doctrine.
5. Refresh the source inventory and evidence-log source header to include the Q3 FY2026 10-Q working files and completed extraction.
6. Run a targeted final confirmation limited to these residual findings before synthesis.

Ten of the eleven first-audit corrections are fully applied, the Q3 FY2026 10-Q reconciliation is substantively sound, and the principal arithmetic re-performs correctly from the raw filings. Clearance is still withheld because the derived-formula control is incomplete, Cost Advantage and Network Effect remain overclaimed in controlling essay language, and the corrections record prematurely claims a persisted re-audit that does not yet exist. RM-2026-0001 therefore remains blocked pending the bounded corrections and one final targeted confirmation.