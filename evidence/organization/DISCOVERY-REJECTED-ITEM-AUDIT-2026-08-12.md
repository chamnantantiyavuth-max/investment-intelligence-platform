# D — Rejected / Pre-Card Item Audit
## Independent Re-Review of Bounded Sample (Recall Proxy #2 — §12 v1.1)

**Auditor:** org-auditor (Internal Auditor / Red Team, role 10)
**Date:** 2026-08-12
**Methodology anchor:** `IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md` §12 (Rejected-Item Independent Audit), §24 (Discovery Challenger — audit use only)
**Task:** `t_553cc702` — [DISC][CHILD] D — Rejected / Pre-Card Item Audit
**Pilot constraints honored:** bounded sample only; NO state change; NO new thresholds; portfolio-blind; taxonomy preserved (M1–M7, §12 verdicts, §9 audit labels are audit language only).

---

## 1. Scope and Discovery History

Discovery history window available: **2026-08-07 → 2026-08-10** (3 Radar artifacts — weekly digest 8/7, mid-week watch note 8/7, weekly digest 8/10). No earlier digests exist in `operational/hermes-organization/kanban/digests/`. The Radar (FD #78 cron, role 11) is the only active pre-card discovery lane in the window; Equity Inflection / Quality & Asymmetry / CS Product produced no surfaced-but-rejected items in this window (their outputs are file-based, not digest-based — outside this sample).

**CoS triage note (M6 vs M4):** In this window cards ORG-2026-0012…0017 sat in Inbox; the only triage action was ORG-2026-0012 **DEFERRED at Founder triage** (re-test pending, do-not-reraise until macro window settles). There were **zero CoS rejections** in the window. Therefore **M6 (Triage Miss) is unmeasurable in this sample** — every sampled item was rejected pre-card at the Radar/Principal stage, so any miss here is **M4 (Judgment Miss)**, not M6. H6 (CoS as under-audited false-negative gate) remains unverified — flagged for parent synthesis.

## 2. Sample Selection (n=10, bounded)

All pre-card rejections documented in the 3 digests' "deliberately ignored" sections. Sample spans lanes (E1 Radar macro/gold/equity, C1 Close System silver), rejection causes (judgment, evidence-insufficiency, cadence, policy-reraise, authority), and market regimes (jobs-report day, Hormuz reversal).

| # | Item | Source digest | Lane | Original disposition |
|---|------|---------------|------|----------------------|
| 1 | META Form 4 cluster (4 filings 8/4–8/6) | 8/10 | E1 (EDGAR pass) | Resolved to routine small insider sales; below bar |
| 2 | US July jobs miss + Fed outlook | 8/10 | E1 (macro trigger) | Explains moves; not an anomaly; feeds 0012 |
| 3 | Hormuz continued standoff (strikes, traffic near-standstill) | 8/10 | E1 (event trigger) | Context for 0012/0016; no new research question |
| 4 | Oil standalone card (WTI −11% from 7/31 peak) | 8/7 | E1 (event trigger) | Explained by Hormuz deal optimism; folded into 0012 |
| 5 | Silver COT "2-year bullish extreme" (Finimize 8/9) | 8/10 | C1 | Unverified secondary source (CFTC primary 404); flag, don't file |
| 6 | AMZN S-4 business-combination registration (filed 7/31) | 8/10 | E1 (EDGAR pass) | Outside 7-day window; digest note only |
| 7 | Mining-equity moves (Wheaton dividend, TFPM results) | 8/7 | E1 | Routine; below the bar |
| 8 | Gold's continued rally (spot 4,335.40, +9.0% from 8/3) | 8/10 | E1 (gold) | Continuation of 0012; do-not-reraise until window settles |
| 9 | Apple — no material new event (smart-glasses delay, etc.) | 8/7 midweek | E1 | Below standing bar (FD #76 coverage unchanged) |
| 10 | Momentum screening / equity record highs | 8/7 + 8/10 | E1 | Out of scope by FD #75 reversal |

## 3. Independence Discipline

- **Blind challenger pass (§24):** 5 of 10 packets (1, 2, 3, 5, 6) re-reviewed by an independent model context (GPT-5.6 Sol, `openai-codex`, reasoning=high) that received **evidence-only** packets — no original disposition, no rationale, no downstream outcomes. Verdicts recorded before any disposition comparison.
- **Auditor's own pass:** verdicts formed from the evidence as logged; the auditor had read the digests (disposition anchoring risk is real and is acknowledged; the challenger pass is the genuinely blind control).
- **Point-in-time integrity (PIT):** no hindsight used — e.g., the 8/7 Hormuz de-escalation → 8/7 evening re-escalation reversal is NOT used to judge the 8/7 morning oil decision.
- **Question asked per item (§12):** "Did this evidence justify spending additional low-cost reconnaissance or research capacity?"

## 4. Independent Verdicts (evidence → verdict → disposition comparison)

### 1. META Form 4 cluster — **WELL-FOUNDED rejection (correct)**
- Evidence: 4 Form 4 filings 8/4–8/6 in an 8/3–8/10 window; one described: Andreessen 426 sh ≈ $252K @ $588–591.69 (8/4).
- Verdict: A $252K sale by a non-executive director at ~$1.5T market cap is noise. The radar resolved the cluster (read all 4; no officer/board concentration). No low-cost check would change the picture.
- **Challenger:** INSUFFICIENT (only one filing enumerated). Divergence explained by log granularity — the digest records the *conclusion* ("routine small insider sales, no concentration") but not the transaction details of the other 3 filings. See Finding F2.
- Classification: **correct rejection**. No miss taxonomy hit.

### 2. US July jobs miss + Fed outlook — **REASONABLE DISAGREEMENT (defensible rejection)**
- Evidence: jobs miss 8/7; September hike odds tumbled; DXY 99.60 (~2-month low); S&P record 7,757.64; ^TNX 4.66; gold +9.0% 8/3→8/10; DFII10 2.43% near cycle peak.
- Verdict: First-order macro regime event; a gold-surge-against-real-yields configuration is genuinely unusual. A card would have been defensible. HOWEVER the research question this evidence answers — "has the marginal gold driver rotated to rate-cut expectations, and does 0008's flow-dominance thesis survive?" — is **already live in ORG-2026-0012**. The rejection preserves precision without losing the information (0012 blocked/re-test window).
- **Challenger:** HIGH (would promote). Divergence is expected and itself a finding: a blind reviewer without card context cannot distinguish "missed" from "covered elsewhere" (F2).
- Classification: **correct rejection (with note)** — reasonable disagreement on whether a separate macro card was warranted; no false negative because the question is preserved in-card.
- Taxonomy: none (M4 not applicable — judgment used correctly).

### 3. Hormuz continued standoff — **PROBABLE JUDGMENT MISS (M4 candidate) — the sample's false-negative candidate**
- Evidence: Iran restrictive draft plan (8/6); reported strikes in the Strait (8/7); IRGC fire, explosions on Qeshm Island (8/7); US "largest strike since WWII" language (8/7); tanker traffic reportedly near-standstill vs 6 tankers/day (8/7, conflicting reports); oil 78.7 vs 75.22 low; gold 4,335.40.
- Verdict: Reported military escalation at a critical chokepoint with system-wide second-order effects (oil → inflation → rates → equities → gold) — AND the radar's own log notes *conflicting reports* on the standstill. Conflicting reports on a potentially systemic event are exactly what a cheap verification step exists for (AIS/shipping-transit count). The evidence justified low-cost reconnaissance (one check) that was not spent. The event also *reversed the premise of the live card* (0012 premised on de-escalation) — a premise-break is a new research trigger, not just context.
- **Challenger:** HIGH, highest false-negative cost of all packets (convergence).
- Mitigating factor: the event was flagged to CoS as context in the mid-week note — information was not erased, but no cheap check was run and no question card raised.
- Classification: **probable judgment miss (M4 candidate) — 1 of 10**. Disagreement = finding for human review (§24), NOT auto-promotion.
- Taxonomy: **M4 (Judgment Miss)** candidate; secondary M5 (cadence) not applicable (observed same day).

### 4. Oil standalone card (WTI −11%) — **WELL-FOUNDED rejection (correct)**
- Evidence: WTI −11% from 7/31 peak; Hormuz deal optimism (8/6–8/7); gold +7.7%; S&P records.
- Verdict: A large move with a coherent specific catalyst is precisely what should NOT be a card (precision protection). PIT: the evening reversal (re-escalation) is hindsight and excluded.
- Classification: **correct rejection**.

### 5. Silver COT "2-year bullish extreme" — **WELL-FOUNDED card rejection (correct) + system-level M2 Data Miss**
- Evidence: Finimize 8/9 claim; CFTC primary URLs 404 (site restructure); silver +11% week; LBMA vaults 907.059 Moz (~5-year high, +16.6% YoY).
- Verdict: Filing a card on an unverified secondary claim that *contradicts* official data direction (vaults high = no visible scarcity) would be noise. The radar's "flag, don't file" treatment is correct; the pointer feeds 0016's research question. **Challenger:** MAYBE (convergence — weak confidence).
- Classification: **correct rejection** of the card. BUT: the system's inability to verify CFTC COT (persistent 404) is a genuine **M2 (Data Miss)** at system level — positioning is a first-class squeeze signal that cannot currently be measured. Data Steward D2 register action (COT source), not a threshold change.
- Taxonomy: card = correct (no miss); data layer = **M2**.

### 6. AMZN S-4 (filed 7/31) — **REASONABLE DISAGREEMENT (low severity)**
- Evidence: S-4 business-combination registration filed 7/31; outside the 8/3–8/10 window; head read; counterparty/terms not in log.
- Verdict: An S-4 at a mega-cap can signal a material business combination; the cheapest check (cover page / transaction summary) is trivial. The radar read the head, found nothing to raise, and **digest-noted it to the equity side** — information preserved, not erased. Ambiguous evidence; no clear false negative.
- **Challenger:** MAYBE (convergence).
- Classification: **correct rejection (with note)** — reasonable disagreement on whether a question card was warranted; severity low because the item was surfaced in the digest, not silently dropped.
- Taxonomy: M5 (cadence) risk is inherent to the 7-day window rule but the digest-note path mitigated it.

### 7. Mining-equity moves (Wheaton dividend, TFPM results) — **WELL-FOUNDED rejection (correct)**
- Evidence: WPM dividend news; TFPM results; gold +7.7% / silver +11% week.
- Verdict: In a sharp precious-metals week, streaming/royalty names reporting dividends/results is expected correlated noise. Below the bar; correct filter.
- Classification: **correct rejection**.

### 8. Gold's continued rally (8/10) — **WELL-FOUNDED rejection (policy-compliant) + re-test trigger flag**
- Evidence: spot 4,335.40 / futures 4,397.2, +9.0% from 8/3; DFII10 2.43% near cycle peak; jobs miss; hike odds down; DXY 2-month low.
- Verdict: Continuation of the already-filed 0012 observation; do-not-reraise is a CoS/Founder-sanctioned policy (card-outcomes register). The driver-rotation question is 0012's. Re-filing would violate do-not-reraise and duplicate. Correct as policy application.
- **Flag (F4):** 0012's re-test is conditioned on "a settled macro window" (Hormuz live, CPI due 8/12). No explicit calendar trigger exists in the register — §13's "does 'not now' become 'never'?" risk is live. Recommend the parent synthesis propose a scheduled re-test trigger (monitoring-condition mechanism already exists; no new state machine).
- Classification: **correct rejection (policy)**.

### 9. Apple — no material new event — **WELL-FOUNDED rejection (correct)**
- Evidence: routine product news (smart-glasses delay, trade-ins, class-action payouts); Q4 FY26 ~Oct; Ternus transition eff. 1 Sep (FD #76); Q3 10-Q filed 7/31.
- Verdict: Apple already has live threads (0010 services margin, RM-2026-0004 deep analysis, monitoring conditions). Routine product noise adds nothing; the standing material-events-only mandate is a precision filter. Correct.
- Classification: **correct rejection**.

### 10. Momentum screening / record highs — **WELL-FOUNDED rejection (authority)**
- Evidence: FD #75 reversed momentum scanning; S&P/Dow/TSX records "explained by rate narrative."
- Verdict: Authority-based exclusion, not a judgment rejection; properly governed by an explicit Founder Decision. Not a false negative.
- Classification: **correct rejection (authority)**. Taxonomy: M7 not applicable — the authority is explicit and current (no drift).

## 5. Verdict Counts (n=10)

| §12 Verdict | Count | Items |
|---|---|---|
| Original rejection well-founded (correct rejection) | **7** | 1, 4, 5, 7, 8, 9, 10 |
| Reasonable disagreement (defensible; preserved in-card/in-digest) | **2** | 2, 6 |
| Probable judgment miss (false-negative candidate) | **1** | 3 (Hormuz) |
| Data insufficient | 0 | — |
| Cannot determine | 0 | — |

- **Correct rejections: 9/10** (7 well-founded + 2 reasonable-disagreement-but-defensible)
- **False-negative candidates: 1/10 (10%)** — Hormuz (M4 candidate; challenger-convergent)
- **Confirmed false negatives: 0** — no sampled item shows an erased opportunity with evidence of materiality at decision time

## 6. Challenger Comparison (blind Sol Medium pass, 5 packets)

| Packet | Challenger verdict | Auditor verdict | Agreement |
|---|---|---|---|
| 1 META Form 4s | INSUFFICIENT | Well-founded (correct) | Divergence → F2 |
| 2 Jobs miss + Fed | HIGH | Reasonable disagreement (covered by 0012) | Divergence → F2 |
| 3 Hormuz | **HIGH — highest FN cost** | **Probable judgment miss (M4)** | **Convergence** |
| 4 Silver COT | MAYBE | Well-founded (correct) + M2 data flag | Convergence |
| 5 AMZN S-4 | MAYBE | Reasonable disagreement | Convergence |

Challenger highest-FN-cost: **Packet 3 (Hormuz)** — matches the auditor's M4 candidate.

## 7. Findings (audit language only — no new state, no thresholds)

- **F1 — Hormuz = the sample's false-negative candidate (M4).** Reported strikes + near-standstill tanker traffic + conflicting reports + US strike language justified one cheap verification step (AIS transit count) that was not run, and the event broke the live card's (0012) de-escalation premise — a premise-break is a new research trigger, not context. Flag for human review (§24); challenger concurs.
- **F2 — Blind-review auditability gap (H7/H2 support).** The disposition trail does not record *checks performed* (e.g., META's other 3 Form 4s are not enumerated; only the conclusion "routine" is logged) nor *fold-links* (jobs-miss → 0012). A blind reviewer cannot distinguish "missed" from "covered elsewhere". Smallest fix (observability-first, §30): the digest/evidence log should record (a) checks performed with outcome, (b) explicit fold/reference links when an ignored item is covered by a live card.
- **F3 — M2 Data Miss: CFTC COT persistently unverifiable.** Silver positioning is a first-class squeeze signal; all newcot URL variants 404. Card rejection was correct; the data gap is a coverage finding for the Data Steward D2 register.
- **F4 — 0012 re-test trigger is implicit, not scheduled.** §13 "not now → never" risk. Recommend an explicit re-test trigger (monitoring-condition mechanism already exists).
- **F5 — M6 unmeasured in window.** No CoS rejections occurred 8/7–8/10; the second judgment gate remains unaudited (H6). Parent synthesis should scope a CoS-triage sample once triage history exists.

## 8. Precision Protection Confirmed

7–9 of 10 rejections are correct filters of routine/explained noise (META $252K sale, oil explained move, WPM/TFPM correlated noise, Apple routine news, momentum authority, gold continuation policy, COT contradiction). The radar's "honestly producing zero ideas when nothing clears the bar" (§5) behavior is preserved and observed. No threshold changes proposed — none needed.

## 9. Smallest System Changes (proposals for parent synthesis — NOT executed)

1. Evidence-log granularity: record checks performed + fold-links (F2) — observability first.
2. CFTC COT source registration (Data Steward D2) (F3).
3. Scheduled re-test trigger for 0012 (F4).
4. Optional §24 challenger sampling cadence (e.g., bounded sample per month) once disposition volume justifies it.
5. CoS triage sample (F5) once triage history accumulates.
All consistent with §9 (audit-only capture, no new canonical state machine) and §30 remediation order.

## 10. Limitations

- Discovery history window = 4 days (8/7–8/10); single-week, single-lane (Radar) sample; small n.
- Auditor's own pass carries anchoring risk (digests read in full); mitigated by the blind challenger control on 5 packets.
- No CoS rejections in window → M6 and H6 untestable here.
- No future information used; PIT integrity maintained.

---
*Artifact for task t_553cc702 — feeds parent t_500dd515 (synthesis). Challenger artifact: `discovery-challenger-review.md` (task attachment). Taxonomy preserved; audit language only.*
<!-- 2026-08-12 22:30 UTC+7 -->
