# Audit Note — RM-2026-0001

## 1. Process findings

**P-1 — Material chronology metadata is inaccurate (MAJOR).** The artifact footers are future-dated relative to both the repository record and the system clock: `source-inventory.md` states 20:50 UTC+7, `evidence-log.md` 21:15, the appendix 21:20, the first-pass README 21:25, and the essay 21:40, while commit `f9bdd05c463adbaeb389eb9e6bad0a7ea69154ad` was created at 16:36:17 UTC+7 and the audit-time system clock was 16:41:56 UTC+7 on the same date. The first-pass files were written at approximately 16:34:55, consistent with the README’s stated 16:31–16:34 dispatch window but incompatible with its 21:25 footer. This is not evidence that the research conclusions were fabricated, but it is a material provenance defect under the requirement to preserve accurate timestamps and workflow history.

**P-2 — Anti-anchoring is plausible but not independently reproducible from the retained record (MINOR).** The sequence is internally consistent: the completed evidence packet was committed at 16:30:25, the six first-pass files share near-simultaneous write times around 16:34:55, and the README states that six parallel isolated subagents received only the evidence log and raw filings. The views do not cite one another, and no view visibly relies on a frozen-platform score or specification. However, the repository retains no dispatch prompts, job identifiers, per-agent input manifests, completion records, or pre-synthesis hashes; therefore “no Principal read another’s view” remains a process-owner attestation rather than independently verifiable evidence. The record should either preserve those artifacts or qualify the claim as self-attested.

**P-3 — The mandated workflow has not reached the audit stage required for a final clearance (MAJOR).** Plan A §6, FD #66, and the mandate require deep analysis → cross-examination → CRO opposing essay → audit. The essay identifies itself as “pre cross-examination,” no cross-examination artifact is present, and no separate CRO opposing essay exists; `first-pass/05-cro.md` is an independent first-pass risk view with a ranked risk table, not the required strongest coherent opposing essay. The essay’s statement that the CRO’s “full opposing essay is a companion artifact” is therefore inaccurate. This note can audit work produced so far, but it cannot serve as the final pre-publication audit until those stages are completed and the revised essay is re-audited.

No evidence was found that legacy specifications were auto-loaded into the first passes. Use of the six moat dimensions is traceable to the approved mandate itself, and the main essay remains connected prose without a composite score or pass/fail scorecard; no checklist-shaping governance deviation was identified on the face of the artifacts.

## 2. Evidence integrity findings

| Claim | Source trace | Verdict | Severity |
|---|---|---|---|
| FY2025 revenue **$416.2B** and total gross margin **46.9%** | FY2025 10-K, accession `0000320193-25-000079`, MD&A and financial statements: revenue $416.161B; gross profit $195.201B; $195.201B ÷ $416.161B = 46.905% | Verified and correctly rounded | — |
| Services **$109.2B**, **26.2%** of revenue, and **75.4%** gross margin | Same 10-K, Note 2 and MD&A: $109.158B revenue and $82.314B gross profit; shares calculate to 26.230% and 75.408% | Verified | — |
| Services supplied **42.2% of FY2025 gross profit** | $82.314B ÷ $195.201B = 42.169%; formula appears in appendix §4 and the essay identifies the figure as derived | Verified and appropriately labeled | — |
| iPhone **$209.6B**, **50.4%** of FY2025 revenue | Same 10-K, Note 2: $209.586B ÷ $416.161B = 50.362% | Verified | — |
| FY2021–FY2025 cumulative buybacks **$438.6B** and period-end shares down **10.1%** | SEC Company Facts `PaymentsForRepurchaseOfCommonStock`: $85.971B + $89.402B + $77.550B + $94.949B + $90.711B = $438.583B; shares 16.426786B → 14.773260B = −10.066% | Arithmetic verified, but terminology requires reconciliation: $90.711B is cash-flow-statement payments, while Note 10 says Apple repurchased 402M shares “for $89.3B.” The essay and appendix should say “cash paid for repurchases” and explain the settlement-timing difference. The Red Team first pass also mislocates the $89.3B disclosure in Note 16; it is in Note 10. | MINOR |
| FY2025 OCF **$111.5B** and FY2021–FY2025 OCF range approximately **$104B–$122B** | Company Facts and 10-K cash-flow statement: $111.482B in FY2025; five-year minimum $104.038B and maximum $122.151B | Verified | — |
| FY2025 PP&E capex **$12.7B** | 10-K cash-flow statement and Company Facts `PaymentsToAcquirePropertyPlantAndEquipment`: $12.715B | Verified; “PP&E purchases” is the precise label | — |
| FY2025 R&D **$34.6B**, **8.3%** of revenue; FY2021–FY2025 R&D +57.7% versus revenue +13.8% | 10-K and Company Facts: $34.550B ÷ $416.161B = 8.302%; $34.550B ÷ $21.914B − 1 = 57.66%; revenue growth = 13.76% | Arithmetic verified, but the two growth comparisons are derived and are not explicitly labeled as such in the essay | MINOR |
| Greater China **$64.4B / 15.5%** in FY2025, versus **18.9%** in FY2023 | 10-K geographic table: $64.377B ÷ $416.161B = 15.469%; $72.559B ÷ $383.285B = 18.931% | Verified | — |
| Q3 FY2026 revenue **+16.4%**, iPhone **+21.7%**, Greater China **+22.4%**, gross margin **50.1%**, including approximately **2pp** from tariff refunds | Q3 FY2026 8-K Exhibit 99.1, accession `0000320193-26-000018`: $109.417B/$94.036B; $54.252B/$44.582B; $18.816B/$15.369B; $54.770B/$109.417B; issuer’s explicit tariff-refund disclosure | All figures verified and correctly rounded | — |
| Nine-month FY2026 OCF **+43.1% to $117.0B** | Same 8-K cash-flow statement: $116.996B versus $81.754B, an increase of 43.107% | Verified | — |
| Approximately **$16.4B**, or **46%**, of the nine-month OCF increase came from year-over-year working-capital movements | Reperformance of the 8-K reconciliation: aggregate working-capital effect improved from −$19.293B to −$2.927B, a $16.366B change; $16.366B ÷ $35.242B OCF increase = 46.44% | Verified; the essay correctly identifies this as derived | — |
| Manufacturing purchase obligations **$56.2B** | FY2025 10-K, Liquidity and Capital Resources: $56.2B at 2025-09-27, including $55.4B due within 12 months | Verified | — |
| European Commission fine of **€500M in April 2025** | FY2025 10-K, **Item 3, Legal Proceedings**: €500M fine imposed 2025-04-23 in the Article 5(4) DMA investigation | Amount and date verified, but the essay cites Item 1A; the evidence log and source register omit the fine and Item 3 entirely. This breaks the stated claim-level source chain and must be corrected. | MINOR |
| Approximately **1.4pp mix / 1.4pp within-segment** contribution to the FY2023–FY2025 gross-margin increase | Inputs are in the 10-K, but neither the evidence log nor appendix gives the decomposition formula. A midpoint decomposition produces approximately 1.46pp from mix and 1.31pp from within-segment margins; other ordering conventions produce different allocations. | The “roughly” characterization is directionally defensible, but the bridge is not rerunnable and is convention-dependent | MINOR |
| Essay attestation that all material derived figures are marked and drawn through the evidence log | Essay lines containing the R&D growth comparison, margin bridge, FY2025 buyback/OCF ratio, and normalized tariff-refund margin do not consistently carry a `derived` label or formula; the €500M fine is absent from the evidence log | The blanket attestation is false even though most underlying arithmetic is correct | MAJOR |
| “The moat would survive a normal recession, a strong dollar, or one tariff cycle” | No historical stress test, elasticity analysis, scenario bridge, or comparable recession/tariff evidence appears in the evidence log or appendix | Unsupported predictive assertion stated with excessive certainty; it must be framed as an analytical hypothesis or supported by stress evidence | MAJOR |
| None of the compound-break ingredients is present as of Q3 FY2026 | The essay itself documents alternative app distribution and payment structures under the EU DMA, a €500M fine, and restrictions on Apple’s control of purchasing links | Internally inconsistent. A full compound break has not occurred, but regulatory opening is already observable; the conclusion must distinguish “present but not yet economically decisive” from “not present.” | MAJOR |

The re-performance found no arithmetic error in the principal financial figures specified for audit. The main integrity weaknesses are incomplete derived-metric labeling, a non-rerunnable margin bridge, two source-location errors, and thesis statements that exceed the evidence.

## 3. Point-in-time findings

The substantive financial data are generally period-stamped correctly: FY2025 figures refer to the year ended 2025-09-27; Q3 and nine-month FY2026 figures refer to the period ended 2026-06-27; and the relevant filing or furnishing dates are present in the source register. The fiscal-calendar correction—FY2025 and FY2024 at 52 weeks, FY2023 at 53 weeks—is verified against the 10-K.

**T-1 — False footer timestamps defeat otherwise adequate point-in-time controls (MAJOR).** The impossible 20:50–21:40 UTC+7 footers must not remain as asserted creation or verification times. Corrections must preserve the erroneous metadata and add a correction record rather than silently rewriting history, consistent with Constitution §23.9.

**T-2 — FD #58 reference-work compliance is satisfactory (no finding).** No quantitative figure in the essay or appendix was taken from `docs/Books/`, an industry handbook, or another stale reference work. The quantitative case is based on SEC filings and SEC Company Facts, and no unverified reference-work number was presented as current.

The Company Facts series is period-specific and its extraction date is recoverable from the 2026-08-06 source inventory, although a future version should put the retrieval timestamp directly in the appendix’s source-register row rather than relying on document-level context.

## 4. Omission findings

**O-1 — Available FY2026 10-Qs were not extracted, including the latest Q3 filing (MAJOR).** The source inventory identifies Q1, Q2, and Q3 FY2026 10-Qs, including accession `0000320193-26-000020` filed 2026-07-31, but the committed evidence set uses only the preceding 8-K earnings release. The omission is disclosed, which is honest, but it leaves interim footnotes, contingencies, tariff details, regulatory developments, and balance-sheet disclosures untested. A final audit cannot clear the “latest primary evidence” gate until at least the Q3 10-Q is examined and reconciled to the 8-K.

**O-2 — The moat-causality evidence remains materially incomplete (MAJOR).** No earnings-call transcripts, independent premium-tier market-share series, retention or switching surveys, developer economics, transaction or take-rate data, teardown/BOM comparisons, or quantified installed-base data were obtained. The essay and appendix disclose most of these gaps, and Apple’s filings do not provide an installed-base count; therefore this is not concealed evidence failure. It does, however, mean the financial statements establish scale and monetization more strongly than they establish Share of Mind, switching costs, network effects, or relative cost advantage, so the final confidence language must remain qualified unless independent evidence is added.

**O-3 — Required challenge artifacts are absent (MAJOR).** There is no documented cross-examination and no CRO opposing essay. This omission is especially material because the main thesis rests on mechanisms—AI disintermediation and regulatory rent migration—that the opposing essay is supposed to challenge coherently before audit and synthesis.

## 5. Governance findings

The mandate’s substantive non-scope was respected. The artifacts contain no price target, valuation formula, composite moat score, buy/sell recommendation, allocation instruction, portfolio-management action, or execution content. Cash-flow and capital-return ratios are business-quality evidence rather than valuation outputs.

Advisory-only and portfolio-blind framing is explicit in the essay, and the retained input description limits the first-pass agents to the shared evidence packet and raw filings. No portfolio holdings, cost bases, position sizes, or transaction history appear in any reviewed artifact. This complies with Constitution §23.8.1 and Plan A’s retained portfolio-blind boundary.

The main essay is connected prose rather than a mandatory checklist, and the six-dimensional discussion follows the Founder-approved research question rather than a frozen pipeline scorecard. No composite grade was produced. The material governance failure is instead sequencing: cross-examination and the independent opposing essay were skipped or remain unfinished while the essay inaccurately refers to the opposing essay as already existing. Founder publication review must remain blocked until the workflow is completed and the audit is rerun on the corrected artifact set.

## 6. Overall verdict

**MAJOR FINDINGS**

The reported financial backbone is substantially reliable: all specifically requested revenue, margin, mix, cash-flow, capex, R&D, China, quarterly-growth, obligation, buyback, share-count, and regulatory-fine amounts were re-performed successfully from the cited SEC materials. Clearance is nevertheless withheld because the workflow is incomplete, artifact timestamps are demonstrably inaccurate, the latest available 10-Q evidence was not reviewed, the opposing essay is absent despite being claimed as a companion, and several material conclusion statements exceed or contradict the evidence.

### Required corrections

1. Preserve and correct the impossible footer timestamps through an append-first correction record; do not silently overwrite the historical metadata.
2. Add durable anti-anchoring evidence—dispatch prompts or hashes, job identifiers, timestamps, model identity, input allowlist, and per-view completion records—or qualify the isolation claim as self-attested.
3. Complete and persist cross-examination, then produce a separate CRO opposing essay that is a coherent alternative thesis rather than a ranked risk list.
4. Remove the essay’s false companion-artifact statement until that artifact exists; rerun this audit after the essay is revised.
5. Extract and reconcile at least the Q3 FY2026 10-Q, accession `0000320193-26-000020`; review Q1/Q2 10-Qs where they bear on trend, regulation, contingencies, or tariff claims.
6. Add the €500M DMA fine to the evidence log and appendix source register, cite 10-K Item 3 rather than Item 1A, and correct the Red Team’s Note 16 reference to Note 10.
7. Mark every derived figure explicitly and publish inputs and formulas for the gross-margin bridge, R&D/revenue growth comparison, buyback ratios, normalized margin, and other material calculations.
8. Distinguish cash paid for share repurchases from the 10-K’s transaction-value disclosure and reconcile $90.711B with $89.3B.
9. Replace the unsupported recession/strong-dollar/tariff survival assertion with a bounded hypothesis or a sourced stress analysis.
10. Reconcile the conclusion with existing EU regulatory opening: state that the compound break has not occurred, not that none of its ingredients is present.
11. Maintain the existing advisory-only, portfolio-blind, no-valuation, no-recommendation, and no-composite-score boundaries through Founder review.

Arithmetic re-performance confirms that Apple’s principal reported figures are materially accurate and sourced to the identified SEC filings or Company Facts. The research nevertheless has major process and evidence-governance defects: false chronology metadata, incomplete challenge sequencing, an absent opposing essay, omission of available 10-Q evidence, and overconfident claims not supported by the evidence packet. Accordingly, RM-2026-0001 is not ready for Secretary synthesis or Founder publication review until the required corrections are completed and independently re-audited.