# S5 — FREEZE VERIFICATION + RECONCILIATION TABLE
## Gemini Deep Research v1.4 — Apple Rehearsal (PILOT-NONCANONICAL)

**Task:** t_a7021f89 — [DR][CHILD] S5 — Freeze First Passes + Reconciliation
**Author:** org-cos (Founder Chief of Staff — reconciliation owner; the ONLY child authorized to read all three passes)
**Date:** 2026-08-12 22:51 UTC+7
**Mode:** PILOT-NONCANONICAL — calibration rehearsal of the v1.4 workflow on a published case. NOT investment truth. No domain state change. Portfolio-blind.
**Anchor contract:** IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md §9 (freeze), §12 (Gemini-discovered source admission), §13 (Reconciliation)
**Downstream:** S6 Main Research Essay (t_7ac2d383) ← this handoff; synthesis parent t_68d2824b

---

## 1. FREEZE VERIFICATION RECORD

Freeze gate: no pass may be edited after its producer's freeze timestamp. Verified 2026-08-12 22:50 UTC+7.

| # | Artifact (lane) | Producer task | Expected hash (producer manifest/provenance) | On-disk SHA-256 (recomputed) | Status |
|---|---|---|---|---|---|
| F1 | `pass-a-view.md` (Hermes Pass A) | t_7ad3552a | `80e88c9a0cc1b7286aafe7c7084b932ba33597889c006416660dfe2c7187d74e` | `80e88c9a0cc1b7286aafe7c7084b932ba33597889c006416660dfe2c7187d74e` | ✅ FROZEN — exact match |
| F2 | `pass-B-view-quant-model-validator.md` (Hermes Pass B) | t_1ec41f0e | `f0ecb9721169df1dbe52bb2cfbd2fa50cbbb12256e31145d558a2b5203cc139f` | `f0ecb9721169df1dbe52bb2cfbd2fa50cbbb12256e31145d558a2b5203cc139f` | ✅ FROZEN — exact match |
| F3 | `S4-GEMINI-VIEW-FROZEN.md` (Gemini lane) | t_079e1330 | content `ce5a92262fb8611a9759ccfe36a59d7077e2ee820ee01534775065d2acf42dc0` (44,501 chars, full model output) | file-level `fa976b62…4fd`; **content-level `ce5a9226…dc0` independently reproduced** from `S4-GEMINI-VIEW-RAW.md` JSON steps | ✅ FROZEN — content hash verified (see note) |
| F4 | `S4-GEMINI-VIEW-RAW.md` + `_1` dupes | t_079e1330 | — | RAW `01be353f…1205` (both copies identical); FROZEN `_1` identical to FROZEN | ✅ No drift between duplicate copies |

**F3 note (freeze integrity):** the provenance `view_sha256_full: ce5a9226…` is the hash of the canonical model output = `steps[1].text + "\n\n---\n\n" + steps[2].text` (17,382 + 27,112 chars + 7-char separator = 44,501 chars). This was **reproduced exactly** by re-hashing the two model-output steps extracted from the RAW interaction JSON. The FROZEN `.md` file is a re-rendered wrapper (freeze header + citations list + mandatory timestamp footer) around that identical model output; a byte comparison of the model-output section (CRLF-normalized) confirms **zero content edits**. The freeze is valid; the wrapper is formatting only. File-level hash `fa976b62…` therefore differs from content hash `ce5a9226…` — expected, not a violation.

**Freeze gate verdict: ALL THREE PASSES FROZEN AND VERIFIED. No edits after this point. This reconciliation is read-only with respect to the passes.**

---

## 2. INPUTS READ (S5-exclusive authorization)

| Input | File | Read for |
|---|---|---|
| Hermes Pass A (S2) | `attachments/t_7ad3552a/pass-a-view.md` | A's 9-view CIW pass |
| Hermes Pass B (S3) | `attachments/t_1ec41f0e/pass-B-view-quant-model-validator.md` | B's 25-point verification register + 6 independent findings |
| Gemini lane (S4) | `attachments/t_079e1330/S4-GEMINI-VIEW-FROZEN.md` + RAW + PROVENANCE.json | G's 6-dimension moat analysis |
| S1 admission packet | `attachments/t_bfdcbf31/ADMITTED-SOURCE-PACKET-APPLE-REHEARSAL.md` | source register, pass constraints, `conflicting`/`failed_retrieval` flags |
| Anchor workflow | `IIP_Gemini_Deep_Research_Final_Handoff_v1.4.md` §9/§12/§13 | freeze + reconciliation contract |

Published case (`reports/apple-deep-analysis-2026-08-09.md`) NOT re-read: Pass B already verified its quantitative claims against primary evidence (25-point register); reconciliation scope is A/B vs Gemini lane per task body.

---

## 3. AGREEMENT MAP

Legend: ✅ = present and consistent · ⛔ = contradicts / supersedes · — = silent / out of scope.

### 3.1 Three-way agreement (A ∩ B ∩ G) — strongest rows, filing-backed

| # | Topic | Pass A | Pass B | Gemini | Evidence class |
|---|---|---|---|---|---|
| A1 | Q3 FY26 headline: rev $109.4B (+16%), EPS $2.02 (+29%), GM 50.1% | ✅ SRC-02 | ✅ V6/V17 (50.06%; $2.024; +28.7%) | ✅ [cite 1–3] | Filing-verified |
| A2 | Q3 GM 50.1% is inflated ~2pp by tariff refunds; ex-refund GM lower | ✅ ≈48.1% (derived) | ✅ refunds in products COGS (10-Q MD&A) | ✅ [cite 3,4,35] | Filing-verified (A/B); G via coverage |
| A3 | Regulatory pressure on monetization layer is material (DMA €500M fine, DOJ suit, Epic, Google licensing risk, TAC) | ✅ risk #2 | ✅ V23 — all verbatim in 10-Q Q3 Item 1/1A | ✅ D1/D2/D6 narrative | Filing-verified (B); G deepens with third-party |
| A4 | Moat verdict: durable but conditional — "bent, not broken" | ✅ low-medium confidence, conditional | — (quant lens) | ✅ "moat is bent, not broken" | Converged assessment (A+G) |
| A5 | AI interface disintermediation ("dumb pipe") = top threat to the ecosystem | ✅ risk #1 | — | ✅ thesis killer #3 + D5 | Converged assessment (A+G) |

**3.2 Hermes agreement (A ∩ B; G silent)** — filing/XBRL-backed facts

| # | Topic | Pass A | Pass B | Gemini |
|---|---|---|---|---|
| B1 | FY25 financials: rev 416.16B, NI 112.01B, OCF 111.48B, FCF ~98.8B, GM 46.9%, OI% 32.0%, NI% 26.9% | ✅ VIEW 2 | ✅ V1–V3, V10 | — |
| B2 | Intangibles: **corrected Q3-dated figure 20,342/20.34B @ 2026-06-27, +83.4% YTD, −$992M QoQ** (NOT the published case's 21,334/+92.32%, which is Q2-stale) | ✅ 20.34B +83% | ✅ V13 (PIT defect in published case) | — |
| B3 | Balance-sheet fortress: cash+securities $146.5B; net cash ≈$62B; debt $84.3B | ✅ VIEW 4 | ✅ V18 (146,517; $100B program; $10B ASRs settle Q4) | — |
| B4 | Buyback + share-count facts: FY25 buybacks $89.3B (A, equity line) / $90.7B (B, cash-flow line — see N4); new $100B auth; shares −10.1% FY21–25, −1.1% in 9M FY26 | ✅ VIEW 3 | ✅ V14/V15 | — |
| B5 | Inventory +94% (Q3 FY26 vs FY25-end) — top working-capital watch item, cause undetermined | ✅ VIEW 2 flag | ✅ F6 (largest WC swing; pre-launch build hypothesis) | — |
| B6 | Greater China rebound: +22%/22.4% Q3 FY26 revenue after 2 consecutive down years (FY24 −8%, FY25 −4%) | ✅ VIEW 1/6 | ✅ V5 (+22.43%) | — (uses different metric/period, see D5) |
| B7 | Segments FY25: Americas 42.9%, Europe 26.7%, GC 15.5%, Japan 6.9%, ROW 8.1% | ✅ VIEW 1 | ✅ V4 | — |
| B8 | Earnings-quality flags: ETR swings (FY24 one-off charge; FY25 15.6%; Q3 17.9%), FY25 FCF/NI 88.18% | ✅ VIEW 2 (ETR) | ✅ V12/F2 (FCF/NI 88.18% 5-yr low; tax-cash +$17.3B driver) | — |

**3.3 Hermes–Gemini agreement (A ∩ G; B silent/consistent)** — assessment-level

| # | Topic | Pass A | Pass B | Gemini |
|---|---|---|---|---|
| C1 | China premium-segment battle is real: Apple's China growth is subsidy/discount-driven while Huawei leads | ✅ GC recovery +22% but flagged volatile; GC declined FY23–25 | ✅ V5 (revenue fact) | ✅ D3: Huawei 20–20.7% vs Apple 19–19.4% Q1'26, Apple via promotions |
| C2 | Cost/margin pressures from component supply chain are a live risk | ✅ supplier concentration risk #5 (low-medium); NAND/DRAM named in Item 1A | ✅ F5 (AI compute expensed via R&D/COGS; capex −28%) | ✅ D4 memory supercycle (severity differs — see D4) |

**3.4 B-only findings (quant lens — feed Data Steward / S-final, NOT contradicted by anyone)**

| # | Finding | Detail |
|---|---|---|
| E1 | XBRL vs 10-Q intangibles series divergence | `IntangibleAssetsNetExcludingGoodwill` (13,301→25,417) ≠ 10-Q line (11,093→20,342); gap widens $2.2B→$5.1B; one series mislabels/misaggregates |
| E2 | Other non-current liabilities +$13.5B unexplained | 41,549→55,080 (Q3 FY26); largest liability-side move; not explained by admitted evidence |
| E3 | R&D is the hidden accelerant | 9M FY26 R&D 34,035 (+32.5%) ≈ FY25 full-year 34,550; R&D intensity 8.3%→9.3% while capex −28.2% — AI compute expensed, not capitalized |
| E4 | Buyback coverage collapse | 9M FY26 53.1% vs 86.3% 9M FY25; Q1 92.9M sh / Q2 42.4M / Q3 79.6M; run-rate favors real slowdown (ASR-timing caveat acknowledged) |
| E5 | Services margin flat, not inflected | Q3 Services GM 75.62% = y/y flat; 9M +0.8pp is mix-driven (MD&A) — any rent-capture thesis must not rely on Q3 Services margin expansion |
| E6 | FY25 tax-cash step | 43,369 vs 26,102 (+$17.3B, +66%) while ETR fell to 15.6% — the under-discussed FY25 FCF/NI break driver; 9M FY26 cash tax −29% (tailwind) |

**3.5 G-only claims (Gemini lane — third-party/management-claim class, NOT in admitted filing evidence, PENDING §12 admission)**

| # | Claim | Source class | Hermes position |
|---|---|---|---|
| G1 | Q4 FY26 GM guidance 47–48% (incl ~100bp tariff), normalized ~46.5% | management-claim via third-party call coverage [cite 4,5,36] | Not in filings A/B verified; transcripts `failed_retrieval` (S1) → review required |
| G2 | CEO transition: Cook steps down 2026-09-01 → Executive Chairman; Ternus becomes CEO | third-party press [cite 6–8] | Not in admitted filings; DEF 14A deliberately unextracted (S1) |
| G3 | DRAM ASP +400% y/y, NAND +300%; iPhone 18 Pro Max BoM +$300; base +$200–250 | third-party (Counterpoint etc.) [cite 38] | Filings name NAND/DRAM supply risk only, no magnitudes |
| G4 | June 25, 2026 price hikes across Mac/iPad/HomePod lines (+6–25%) | third-party [cite 39–42] | Not in admitted evidence |
| G5 | Apple Intelligence ~410M DAU; on-device models ~150B params; Google Gemini 1.2T-param backend via ~$1B/yr deal | third-party [cite 21,46–49] | Not in admitted evidence |
| G6 | Google TAC ~$20B/yr; exclusive default deal legally dead as of 2026 | third-party estimate + court-reportage [cite 50–53] | B V23 confirms "Google licensing at risk" in 10-Q (direction consistent); $20B figure itself not in filings |
| G7 | Vision Pro commercial failure: ~600K cumulative units, 45K holiday-2025, VPG disbanded by Apr 2026, 95% marketing cut | third-party [cite 22–25] | Not in admitted evidence |
| G8 | China refurb market $13.72B (9.12% CAGR); refurb iPhone 13 ~CNY 1,720 (−45% vs launch) | third-party [cite 14] | Not in admitted evidence |
| G9 | Huawei: 20–20.7% China share Q1'26; Mate 80 ~7M units; 70M HarmonyOS phones 2024; Mate XT trifold $2,500+ | third-party (IDC/Counterpoint conflict — see D5) [cite 15,26–32] | S1 flags IDC vs Counterpoint as `conflicting` |
| G10 | Apple China Q1'26 shipments +20% y/y; share 19–19.4%; discounts up to CNY 2,000 | third-party [cite 27–31] | Different metric/period vs A's +22% Q3 revenue (consistent direction) |

**Agreement-map counts:** 3-way agreement 5 · Hermes A∩B (G silent) 8 · A∩G (B silent) 2 · B-only 6 · G-only 10. **Direct A↔B numeric contradictions: 0.** Direct A/B↔G numeric contradictions on filing-verifiable figures: **0** (all G quantitative items are outside the admitted filing evidence, not contradicted).

---

## 4. MATERIAL DISAGREEMENTS (Hermes passes vs Gemini lane)

Per handoff §13: for each material disagreement → which claim differs / which evidence differs / which assumption differs / which source is stronger / whether another research wave can resolve / whether uncertainty must remain visible. **No averaging into false consensus.**

### D1 — Forward gross-margin guidance: "Q4 GM 47–48%, normalized ~46.5%, 280bp compression" ⚠️ MATERIAL
- **Which claim differs:** G states management *guided* Q4 GM to 47–48% (incl ~100bp tariff benefit) and frames a "280 basis point compression in normalized gross margin over just two quarters" as near-established [cite 4,5,36]. Neither Hermes pass surfaced any forward GM guide; B's 25-point register (which re-derived every quantitative claim of the published case from filings) contains **no Q4 guidance item**.
- **Which evidence differs:** G's source is third-party earnings-call coverage (fool.com, mlq.ai, seekingalpha). Apple does not publish GM guidance in press releases; the S1 packet classified the earnings-call **transcripts as `failed_retrieval`** → any call-based claim is management-claim-only, NOT filing-verified.
- **Which assumption differs:** G assumes call coverage is reliable and treatable as established fact; the Hermes evidence model (EVIDENCE-MODEL §2, S1 §2.7) requires transcripts to be verified before use.
- **Which source is stronger:** For *realized* margins — A/B filings (SRC-02/03). For the *forward* guide — none in the admitted packet; the claim cannot currently be confirmed.
- **Resolvable by another wave?** YES — retrieve the Q3 FY26 earnings-call transcript (fix `failed_retrieval`) or wait for the Q4 FY26 10-Q MD&A (filed ~Oct 2026).
- **Uncertainty must remain visible:** YES — S6 must label any forward-GM figure as *management claim via third-party coverage*, not filing-verified fact.

### D2 — "Historic ~50% gross margin baseline" vs FY25 46.9% ⚠️ MATERIAL (severity framing)
- **Which claim differs:** G repeatedly anchors on Apple's "historic ~50% GM profile/baseline" [cite 36,38] and treats the Q3 50.1% print as the baseline from which compression is measured. Hermes A/B: 5-yr GM = 44.1% (FY23) → 46.2% (FY24) → 46.9% (FY25); Q3 50.06% **includes ~2pp tariff refunds**; A's ex-refund Q3 ≈ 48.1%.
- **Which evidence differs:** G's "50%" is the refund-distorted Q3 print (or the same period's call commentary); Hermes uses the full XBRL/10-K series (B V3; A VIEW 2).
- **Which assumption differs:** G assumes ~50% is the pre-crisis run-rate. Under Hermes data, FY25 baseline is 46.9%; a normalized Q4 ~46.5% (G's own figure, if valid) is ~flat vs FY25 — the "280bp compression" framing depends on starting from the distorted 50.1%.
- **Which source is stronger:** A/B (full 5-yr series, SRC-04 XBRL + SRC-01 10-K).
- **Resolvable?** Partially — the compression magnitude resolves with D1's transcript/10-Q wave; the baseline itself is already settled by Hermes data (46.9% FY25).
- **Uncertainty must remain visible:** YES — S6 should present the FY25 46.9% baseline (filing-verified) and treat "50%" only as the refund-inflated Q3 print.

### D3 — CEO transition (Cook → Ternus, 2026-09-01) elevated to thesis-killer #1 ⚠️ MATERIAL (evidence class)
- **Which claim differs:** G presents the succession as fact ("Tim Cook will step down on September 1, 2026… John Ternus takes the helm") and makes "a botched executive transition" the FIRST of three thesis killers [cite 6–8]. Hermes A and B never surface it — not because they reject it, but because it is not in the admitted filing evidence (A's risk ranking has no succession item; B's register has no such claim to verify).
- **Which evidence differs:** G: third-party press (9to5mac, macrumors, cbsnews). Hermes packet: DEF 14A (proxy — where succession plans would appear) was deliberately **unextracted / out of scope** (S1); transcripts `failed_retrieval`.
- **Which assumption differs:** G assumes press-reported succession timing is reliable fact. Hermes cannot confirm or deny from admitted evidence.
- **Which source is stronger:** none in packet — genuinely unverifiable here.
- **Resolvable by another wave?** YES — extract DEF 14A (out of scope for this pilot) or check for an 8-K Item 5.02 (departure/appointment) filing.
- **Uncertainty must remain visible:** YES — S6 may reference it as *third-party-reported succession* with attribution, never as a filing-verified fact; its thesis-killer status should carry the same label.

### D4 — Memory-supercycle magnitudes (DRAM +400%, NAND +300%, BoM +$300) — severity driver ⚠️ MATERIAL
- **Which claim differs:** G's thesis-killer #2 ("permanent hardware margin destruction") is built on quantified third-party data: DRAM ASP +400% y/y, NAND +300%, iPhone 18 Pro Max BoM +$300, base +$200–250 [cite 38]. Hermes passes: 10-K Item 1A names NAND/DRAM/AI-compute component supply risk (no magnitudes); B F5 independently shows AI compute being expensed (R&D +32.5% vs capex −28%) — same direction, different evidentiary base.
- **Which evidence differs:** G: Gemini-discovered third-party (Counterpoint price-track etc.) — **pending §12 admission**; none of these sources passed S1 admission. Hermes: filing risk-factor text only.
- **Which assumption differs:** G assumes the magnitudes are established market data; per S1 §12, "Gemini said X ≠ Evidence" — the underlying source must be opened and admitted first.
- **Which source is stronger:** Filings establish the *direction* (supply risk; R&D/capex signature); the *magnitudes* are unadmitted third-party claims.
- **Resolvable by another wave?** YES — admit Counterpoint/IDC price-track reports per §12, or triangulate via supplier filings (SK hynix/Samsung/Micron 10-Qs/XBRL).
- **Uncertainty must remain visible:** YES — S6 must not present DRAM/NAND % or BoM $ as facts without the §12 admission trail.

### D5 — China Q1 2026 share: Huawei 20–20.7% vs Apple 19–19.4% — conflicting sources presented as range ⚠️ PROCESS/MATERIAL
- **Which claim differs:** G states Huawei led China in Q1 2026 with "20% to 20.7%" vs Apple "19% to 19.4%" [cite 27–31]. Hermes rule (S1 §2.3, EVIDENCE-MODEL §7): IDC vs Counterpoint Q1 2026 was recorded as **`conflicting`, never averaged** — G's ranges effectively present the conflict as a spread without the `conflicting` label.
- **Which evidence differs:** G merged both trackers into ranges; Hermes would keep the two estimates separate and unweighted.
- **Which assumption differs:** G assumes range-presentation preserves neutrality; Hermes treats the disagreement itself as information requiring a conflict flag.
- **Which source is stronger:** For *direction* — consistent with A's filing fact (GC revenue +22% Q3 FY26, rebound) and B's V5. For *share points* — neither tracker is admitted as truth; both remain third-party.
- **Resolvable by another wave?** Partially — a later quarter's filings or an IDC/Counterpoint reconciliation could settle which tracker is closer; the `conflicting` status stands until then.
- **Uncertainty must remain visible:** YES — S6 should either present both estimates separately with the conflict flag or cite only the filing-verified revenue rebound.

### D6 — Priority ordering of moat-break vectors ⚠️ MATERIAL (assessment-level)
- **Which claim differs:** A ranks: #1 AI interface disintermediation, #2 regulatory opening of monetization, #3 tariff/trade, #4 China, #5 supplier concentration. G names three co-equal thesis killers: #1 botched executive transition, #2 permanent hardware margin destruction, #3 dumb-pipe disintermediation. B declines a moat ranking (quant lens).
- **Which evidence differs / assumption differs:** Same admitted evidence; the difference is weighting and evidence-class tolerance. G weights forward-looking third-party claims (succession, memory cycle) as highly as Hermes weights filing-visible structural risks.
- **Which source is stronger:** For converged ground: both put AI disintermediation at the top of their sets — that is the single highest-conviction convergence of the whole reconciliation (A #1 risk; G thesis killer #3, itself the only one of G's three that Hermes can corroborate from admitted evidence).
- **Resolvable?** No single wave — it is a weighting judgment; keep all vectors visible with their evidence classes.
- **Uncertainty must remain visible:** YES — S6 should present the converged #1 (AI disintermediation) plus the divergent additional vectors (regulatory #2 per Hermes; margin destruction and succession per Gemini) **without averaging**, each labeled with its evidence class.

---

## 5. HERMES-INTERNAL A/B NUANCES (surface for S6 — non-material, no contradiction)

| # | Topic | Pass A framing | Pass B framing | S6 treatment |
|---|---|---|---|---|
| N1 | Buyback trajectory | Strength: new $100B authorization (capacity) | Caution: 9M coverage 53.1% vs 86.3%; run-rate favors real slowdown | Use B's run-rate evidence for forward direction; keep A's authorization as capacity fact |
| N2 | FY25 FCF/NI 88.18% | Framed inside "OCF exceeded NI 4 of 5 years" (positive) | Framed as 5-yr low, tax-cash driven (caution) | Same number; B's decomposition (cash tax +$17.3B) is the causal layer |
| N3 | Intangibles figure | 20.34B +83% (already Q3-correct) | 20,342 +83.4% YTD, −$992M QoQ; published case's 21,334/+92.32% is Q2-stale | **Both Hermes passes already carry the corrected figure — S6 MUST use 20,342, never 21,334** |
| N4 | FY25 buyback dollar figure | $89.3B — repurchases of common stock (10-K statement of shareholders' equity line) | $90,711M — payments for repurchase of common stock (cash-flow line, XBRL) | Same event, different statement bases (equity-classified vs cash paid; ASR/misc timing explains the gap); NOT a contradiction — S6 may cite either with its statement source |

---

## 6. HANDOFF TO S6 (MAIN RESEARCH ESSAY) — what is safe to use

**Use as filing-verified facts (A and/or B backed, agreed):** A1, A2, B1–B8 (headline Q3 FY26 numbers incl. refund disclosure; FY25 P&L; corrected intangibles 20,342; balance sheet; buyback facts; inventory flag; China rebound; segment splits; ETR/cash-tax notes; Services GM 75.62% flat Q3).

**Use as converged assessment (A+G, label as assessment):** moat durable-but-conditional / "bent not broken" (A4); AI interface disintermediation = top threat (A5, C2).

**Use with mandatory evidence-class labels (third-party/management-claim, PENDING §12 admission):** G1–G10 — CEO transition, forward GM guide, DRAM/NAND magnitudes, BoM $, June price hikes, Apple Intelligence DAU, Gemini deal, TAC $20B, Vision Pro, China share ranges, refurb market, HarmonyOS. May be referenced with attribution; must NOT be presented as filing-verified facts. Semantic fidelity: no new claims beyond frozen views.

**MUST NOT use / superseded:** published case's intangibles 21,334 (+92.32%) — Q2-stale (B V13); any averaged IDC/Counterpoint share figure (D5); "historic ~50% GM baseline" without the FY25 46.9% context (D2).

**Open items for later stages (not S6's job):** E1 XBRL-vs-10-Q intangibles divergence; E2 +$13.5B other non-current liabilities — both to Data Steward; G-items' §12 admission to S-final evidence stage.

---

## 7. RECONCILIATION VERDICT (S5)

- **Freeze:** PASS (3/3 lanes verified; Gemini content hash independently reproduced from RAW).
- **Hermes A vs B:** zero irreconcilable numeric contradictions (one statement-basis difference on FY25 buyback dollars — §5 N4); 25/25 published-case claims verified-or-caveated (21 reproduced, 3 caveated, 1 PIT-stale); both passes independently converge on the corrected intangibles figure.
- **Hermes vs Gemini:** zero contradictions on filing-verifiable facts; all material differences are (a) forward/third-party claims G treats as established (D1, D3, D4), (b) baseline/severity framing (D2), (c) conflicting-source presentation (D5), (d) risk-weighting (D6). Per §13: none averaged; all remain visible with evidence classes.
- **Highest-conviction convergence:** AI-interface disintermediation as the primary moat-break vector (A risk #1 ≈ G thesis-killer #3, independently derived from different evidence bases).
- **Portfolio-blind, advisory-only, PILOT-NONCANONICAL:** no investment truth created; no domain state changed.

---

*Generated by org-cos (S5) — inputs frozen per §1; this document is the S5 deliverable for S6 t_7ac2d383 and synthesis parent t_68d2824b.*

<!-- 2026-08-12 22:54 UTC+7 -->
