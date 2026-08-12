# IIP Discovery Recall & Coverage v1.1 — Pilot Synthesis Packet (Founder-Ready)

**Task:** t_500dd515 · **Assignee:** org-cos (synthesis owner) · **Date:** 2026-08-12
**Mode:** STAGE 5 BOUNDED NON-CANONICAL PILOT — prove the workflow, change NO domain state
**Methodology anchor:** `IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md` (canonical)
**Children consumed:** A (t_5141c7a3, Data Steward), B (t_2d5a911b, Equity Analyst), C (t_5dd42ec0, Quant Validator), D (t_553cc702, Auditor), E (t_0668deda, Commodity Analyst), F (t_5627089d, CoS)
**Prohibited outcomes (§34):** all respected — no universe expansion, no threshold change, no auto-promote, no new canonical states/queues, no composite score, no look-ahead, no curve-fitting, no "bigger model" recommendation, portfolio-blind, missing data ≠ "no opportunity".

---

## 0. สรุปผู้บริหาร (Executive Summary — Thai)

Pilot นี้เป็นการทดสอบ **workflow** ของ Discovery Recall & Coverage v1.1 บนตัวอย่างแบบ bounded (ไม่แตะ domain state) — สรุป:

- **Workflow ใช้ได้** — ครบ 6 workstream (A–F) ทำงานจบในคืนเดียว, miss taxonomy M1–M7 ถูกใช้จริง, PIT integrity สะอาด 15/15, ไม่มีการเปลี่ยน state หรือ threshold ใดๆ
- **Miss ที่วัดได้จริง (CONFIRMED):**
  - **M2 Data Miss = ช่องโหว่ใหญ่สุด** — 30/98 (30.6%) ของ equity universe ถูก E2 ประเมินไม่ได้ (ADR 19/19 ทั้งหมด + US 11 ตัว); commodity lane มี data gap 8 จุด (CME 403, lease rates, CFTC COT 404, FRED lag…); Close System wrapper ไม่มี data field เลย
  - **M7 Authority/Workflow** — drift เอกสาร 6 จุด (D1–D6, 2 จุด HIGH) + WIP breach 4x ที่ triage batch
  - **M6 Triage** — deferral 0012 ไม่มี re-visit trigger → เสี่ยง "not now → never"
- **Miss ที่ยังวัดไม่ได้ (unmeasured) = ความเสี่ยงสูงสุด:**
  - **M1 Universe Miss** — ไม่เคย run out-of-universe counterfactual (พบ 0 นอก universe เพราะ scan อยู่ใน universe 98 ตัวโดย construction)
  - **M4 Judgment Miss** — ไม่มี rejected-item register; QA 71 evidence blocks → 0 cards โดยไม่มี disposition log (ประเด็น H2 ของ Founder)
- **Recall vs Precision:** E2 detector recall สัญญาณ 100% (4/4 benchmark) แต่ candidate-level recall แค่ 50% (stage gate เข้ม — precision-protective); CoS gate permissive (ไม่มี rejection เลยใน 16 cards) → เสี่ยงที่ deferral-erasure ไม่ใช่ rejection-erasure
- **สิ่งที่ต้องให้ Founder ตัดสิน (เล็กสุด):** 7 ข้อ — ดู Section 8
- **ไม่มีอะไรถูก implement** — ทุกอย่างเป็น audit evidence + recommendations

---

## 1. Executive Summary (full)

**Pilot purpose.** Exercise the v1.1 recall-and-coverage methodology on bounded samples to prove the workflow end-to-end — NOT to change any domain state, create thresholds, or expand universes. Six bounded child workstreams (A–F) ran in parallel, each under a distinct profile with an explicit methodology anchor and hard pilot constraints.

**What was exercised.**
- A — full as-built discovery & authority map (equity 98-name + CS 4-commodity universes → E1/E2/E3/C1 lanes → cards → CoS triage → RM → research → Founder gate), 6 authority/doc drifts catalogued (D1–D6).
- B — equity universe coverage: 12-ticker discovered sample, 12/12 in-universe; E2 scanned 98/98 but **30/98 NOT EVALUABLE** (headline M2); E1 filing-level radar wired 8/98 CIKs; E3 shadow has no production path (M7).
- C — Recall Proxy #1 (Historical PIT Benchmark): 15 PIT snapshots (5 quarter-ends × 3 tickers), signal-level bounded recall 100% (4/4), precision 80%; candidate-level recall 50% (2/4), precision 100%; 15/15 no-look-ahead clean.
- D — Rejected/pre-card item audit (challenger review): 5 digest-ignored packets → 2 HIGH, 2 MAYBE, 1 INSUFFICIENT; packet 3 (Hormuz) carries highest false-negative cost.
- E — Close System spec-to-implementation coverage matrix on SLV/TLT/GLD, underlying vs wrapper separated: underlying partially implemented; **every §18A wrapper dimension NOT EVALUABLE WITH CURRENT DATA** for all 3 products.
- F — CoS triage audit (5 high-judgment decisions) + data/source coverage scan (8 active M2 gaps, commodity lane worst); H6 partially confirmed.

**Verdict on workflow viability: VIABLE.** The methodology executed cleanly on bounded samples: the miss taxonomy produced a measurable risk map (M2/M7 CONFIRMED, M6 PARTIAL with concrete finding, M1/M4 unmeasured-but-now-scoped with explicit next probes), recall proxies proved executable (proxy 1 done with PIT integrity; proxy 2 partially — radar lane sampled, CoS lane unmeasurable because zero rejections exist; proxy 4 done via coverage matrices), and the smallest-remediation list emerged in §30 order. No domain state changed; no thresholds created; portfolio-blind throughout.

---

## 2. Current Discovery Map (from A)

```
UNIVERSE (deterministic denominators)
 ├─ Equity: equity_universe.py — 98 names (FO-8 core + US large/mid-cap + 19 ADRs), CIK-verified 2026-08-11 (FD #58/#95)
 └─ Close System: commodity watch (gold / silver / copper / oil) — CS Product Discovery v0.1 (FD #97)

DISCOVERY LANES
 E1 Radar Scout (role 11) — cron Mon 08:00 (FD #78) + Thu 08:00 (FD #80)
    EDGAR 8-CIK standing scan (FD #81) · feedback loop via card-outcomes.md (FD #82)
    output: 0–3 Task Idea Cards/pass → Inbox + Radar Digest
 E2 Equity Inflection — deterministic EPS-breakout scanner, STANDING (FD #89), run_universe_scan.py over 98 names
    firewall: deterministic evidence blocks only — CoS triage is the ONLY entry into research
 E3 Quality & Asymmetry — 4 archetype lenses, SHADOW only (thresholds PROPOSED, FD #53/#95) — never cards/CoS/publish
 C1 CS Product Discovery — watch-input + 5 spec patterns, SHADOW (FD #97) — honest-empty (LBMA silver 404 etc.)

CARDS → CoS TRIAGE (D1, role 01) → RESEARCH MANDATE (RM-####) → research cell → Founder gate → publish
 21 cards on disk (0001–0021); 6 awaiting triage/research (0016–0021); 6 published radar reports; RMs 0001–0004
```

**Authority ownership (A, key boundaries):** universe membership = shared layer (deterministic criteria, FD #53); E1 writes cards to Inbox only; E2 never auto-cards/RMs/publishes; E3/C1 thresholds PROPOSED only; CoS scopes/sequences but never approves conclusions; canonical state change = Founder only; audit execution via Sol Medium (FD-HERMES-007).

**Recall-loss points (A):** M4 (judgment/rejected-item trail) and M1 (universe breadth) are the highest **unmeasured** risks; M5 latency never systematically measured; M6 partially (deferral recorded, no independent re-review); M2 registered with retry policy but produces INSUFFICIENT_DATA classes; M7 material drifts D1/D3.

**Authority/documentation drifts (A, D1–D6):**

| # | Drift | Sev |
|---|---|---|
| D1 | workflow_column vocabulary violates KANBAN-CONTRACT §2 (cards use `Published`/`Research`; neither in §2 list) | HIGH |
| D2 | kanban/board.md stale — lists 0001–0011 only; 0012–0021 on disk | MEDIUM |
| D3 | equity_inflection README header still claims shadow/no standing — superseded by FD #89 standing behavior | HIGH |
| D4 | Card filing path drift — 0018–0021 filed directly from universe-scan (FD #97), radar packaging step not evidenced (FD #88/#89 design) | MEDIUM |
| D5 | QA shadow count — FD #97 says 62 evidence blocks; runtime = 98 rows / 71 with archetypes | LOW |
| D6 | RM-2026-0004 executed+published (FD #87) but no mandate file in research/mandates/ | LOW |

---

## 3. Miss Taxonomy Risk Map (M1–M7)

Consolidated from ALL six children. Every finding is classified by root cause. Severity = synthesis judgment on risk-to-recall impact.

### M1 — Universe Miss
| Evidence | Measured? | Severity |
|---|---|---|
| Equity: 0/12 discovered tickers out-of-universe (B) — but scanning is universe-bounded by construction, so this is an artifact, not proof. **Out-of-universe counterfactual (§11) NOT RUN.** | PARTIAL (universe count known; counterfactual absent) | **HIGH** |
| Close System: approved classes with zero radar representation — agriculture, energy/oil, uranium/strategic minerals beyond LIT/COPX, producer-ETF class (GDX-style), international broad-market beyond FXI (E). No products added (bound honored). | PARTIAL (class-level gap known) | HIGH |

**Verdict:** M1 is **unmeasured, not absent**. It is the first-order recall bound (methodology H1/H5). Smallest probe: bounded §11 counterfactual sample (10–15 eligible names outside the 98), audit-only.

### M2 — Data Miss ⚠️ HEADLINE CONFIRMED
| Evidence | Measured? | Severity |
|---|---|---|
| **30/98 (30.6%) of equity universe NOT EVALUABLE in E2** — 19/19 ADRs (100%: ASML, AZN, BABA, BHP, BP, HDB, INFY, NVO, NVS, PDD, RIO, SAP, SHEL, SNY, SONY, TM, TSM, UL, VOD) + 11 US (BRK-B, CRWD, DDOG, DE, GS, NET, ROP, SHOP, TMO, V, WFC). Errors: 19× insufficient-data, 11× HTTP 404 (B). | YES | **HIGH** |
| E1 EDGAR filing-level radar wired only 8/98 CIKs → 90 names invisible to event-driven filing discovery (B). | YES | HIGH (wiring) |
| Commodity lane — 8 active gaps (F): CME COMEX primary 403 (single-source metalcharts aggregator), silver lease rates missing, CFTC COT 404 (site restructure, new 8/10), FRED DFII10 lag, LBMA silver PM 404, tradingeconomics 403, LME/EIA copper-oil NOT WIRED, transcripts absent (accepted). | YES (known-gap register + retry policy) | MEDIUM–HIGH |
| Close System: zero wrapper data fields/sources anywhere (types+pages+lib grep=0); no live cost data for SLV/GLD (checkpoint only); no live silver/gold supply-demand feeds; no freshness monitor on static research (E, U-1/2/8). | YES | MEDIUM–HIGH |
| QA shadow: 27/98 rows INSUFFICIENT_DATA (A). | YES | MEDIUM |

**Verdict:** M2 is the largest **confirmed** gap. "Missing data = Data Miss / uncertainty, never 'no opportunity'" (§34) was respected by all children.

### M3 — Detector Miss
| Evidence | Measured? | Severity |
|---|---|---|
| JNJ false positive: H1 fired on one-time-item quarter (Kenvue tax-benefit EPS $10.21) — detector has no one-time-item filter by approved design; **candidate gate correctly suppressed (S3)** → no false candidate at surfacing layer (C). Diagnosed, NOT tuned. | YES (single case) | MEDIUM |
| NVDA@2023-09-30 & 2024-12-31: H1+rev both fired, stage UNCLASSIFIED (parabolic regime) → candidate-level recall 50%. Stage strictness, NOT detector miss (C). | YES | MEDIUM (recall-limiting by design) |
| Close System: no wrapper detector/gate in radar pipeline (spec REJECT_WRAPPER_BAD not executed); radar opportunityScore is proxy formula (35/25/30/10) — does NOT run approved close-system-fit-v0.1.0 hard gates; no cost/margin detector; no supply-demand detector (sample); no Layer-5 hidden-signal detector anywhere (E, U-3..U-6). | PARTIAL | MEDIUM–HIGH |
| Inflection thresholds validated on FO-8 only (Phase 1); full-98 validation absent (A). QA archetypes PROPOSED (FD #53) — no production detector yet. | PARTIAL | MEDIUM |

**Verdict:** No missed inflection observed in the benchmark sample (4/4 caught); the confirmed detector risk is one-time-item sensitivity (a known characteristic, gate-managed) + CS detector/score-path gap.

### M4 — Judgment Miss ⚠️ HIGHEST UNMEASURED
| Evidence | Measured? | Severity |
|---|---|---|
| Radar digests document "deliberately ignored and why" (prose only) — no structured rejected-item register (A, F). | NO | **HIGH** |
| QA 71 evidence blocks → 0 cards, no disposition log per block (A). | NO | HIGH |
| Challenger review (D) of 5 digest-ignored packets: **2 HIGH** (gold surge config; Hormuz chokepoint), 2 MAYBE (silver positioning; AMZN S-4), 1 INSUFFICIENT (META Form 4s) → some judgment risk exists at the radar-promotion layer; packet 3 (Hormuz) highest false-negative cost (oil→inflation→rates→equities→metals). | PARTIAL (5-item sample) | MEDIUM–HIGH |
| CoS lane: **zero rejections in 16-card sample** → rejected-item recall proxy for CoS = UNMEASURED (F). | NO | HIGH (H2 concern) |

**Verdict:** This is the Founder's key concern (H2) and the largest observability hole. No structured disposition trail exists for items that were surfaced but never carded.

### M5 — Cadence / Latency Miss
| Evidence | Measured? | Severity |
|---|---|---|
| Radar Mon+Thu cadence; filing→triage ~1 day observed (0016/17 filed 10 Aug, triage 11 Aug) (A). FRED lag = only systematic delay (F). | NO (T0–T5 never systematically measured) | MEDIUM |
| 0012's deferral = judgment latency, not scan latency (F). | — | — |

**Verdict:** No unexplained multi-day blind window observed in sample; but T0–T5 latency is unmeasured by construction → no evidence either way.

### M6 — Triage Miss
| Evidence | Measured? | Severity |
|---|---|---|
| **0012 DEFERRED without explicit re-visit trigger** — no re-test card/date/owner anywhere; re-visit depends on radar noticing the macro window settled → concrete "not now → never" risk (A, F T3). | PARTIAL | **MEDIUM–HIGH** |
| No rejection-erasure observed: 4/4 E2 candidates carded → CoS → research (B); folds (0011→0010, 0014→0013) well-founded with preserved trails (F T1/T2); paired approval well-founded (F T5). | YES | — |
| No independent triage re-review exists. | NO | MEDIUM |

**Verdict:** CoS gate is auditable + permissive (H6 partially confirmed) — the risk is **deferral-erasure + capacity concurrency**, NOT rejection-erasure.

### M7 — Authority / Workflow Miss
| Evidence | Measured? | Severity |
|---|---|---|
| Drifts D1–D6 (A) — D1 (column vocab vs KANBAN-CONTRACT §2) and D3 (README shadow vs FD #89 standing) are HIGH. | YES | MEDIUM |
| **WIP §5 non-conformance**: KANBAN-CONTRACT §5 limit = 1 M2/M3 per Principal in Research; 4 inflection cards (0018–21) sat in Research for one Principal simultaneously (F T4) — 4× breach; either bypassed for batch efficiency or contract needs explicit batch carve-out. | YES | MEDIUM |
| E3 shadow lane has no authorized card path → 98-name evidence non-actionable (B). | YES | MEDIUM (structural) |

**Verdict:** M7 confirmed as documentation/runtime conformance drift — cheap to fix, material to auditability.

### Taxonomy tally (findings → root cause)
| Miss | Findings (children) | Measured | Severity |
|---|---|---|---|
| M1 | 2 (equity counterfactual absent; CS class gaps) | PARTIAL | HIGH |
| M2 | 5 clusters / 30+ names / 8 commodity gaps / 1 CS wrapper void | **YES** | **HIGH** |
| M3 | 4 (JNJ FP; NVDA stage strictness; CS detector/score path; FO-8-only validation) | PARTIAL | MEDIUM |
| M4 | 3 (no register; QA no disposition; D 2/5 HIGH) | **NO** | **HIGH** |
| M5 | 1 (latency unmeasured) | NO | MEDIUM |
| M6 | 2 (0012 no re-visit; no independent re-review) | PARTIAL | MEDIUM-HIGH |
| M7 | 3 (D1–D6 drifts; WIP 4×; E3 no path) | YES | MEDIUM |

---

## 4. Blind Spots & White Space (from B, E)

**Equity (B):**
- **Universe ≠ evaluable universe.** 30.6% of the 98 cannot be evaluated by the only production deterministic scanner with current data wiring — every ADR + 11 US names. The ADR layer is *structurally invisible* to E2.
- E1 event-driven filing discovery covers 8/98 — the other 90 names are invisible to filing-level radar.
- E3 archetype evidence (98 rows / 71 blocks) exists but has no production path → white space between "evidence exists" and "actionable".
- Deep-research coverage: 6/98 (6.1%) — downstream capacity is the binding constraint after triage.
- M1 out-of-universe white space: entirely unmeasured (probe proposed, not run).

**Close System (E) — underlying vs wrapper separation:**
- **Underlying** (data/calculation): partially implemented — live price/momentum/valuation/crowd pipeline; TLT has live FRED macro (DGS10/T10YIE); GLD has review-gated ETF flow capture. Gaps: no live macro connector for SLV/GLD, cost layer checkpoint-only (no fresh AISC), no supply-demand detectors, no Layer-5 hidden signals, opportunityScore bypasses approved close-system-fit gates.
- **Wrapper** (product surface): **ALL §18A dimensions NOT EVALUABLE WITH CURRENT DATA** for SLV/TLT/GLD — zero wrapper fields in the data model (tracking difference, contango/backwardation, roll, issuer, liquidity, AUM/closure, tax mechanics, holdings-vs-thesis fit all ⛔). Classification: **Product/Wrapper Coverage Gap per §18A** — not "no opportunity".
- **Spec definitional gap:** P1/P2/P3 used as matrix rows but **undefined in the canonical doc** (E, F-7/U-7) — must be resolved before scaling the matrix.
- **M1 class white space:** agriculture, energy/oil, uranium/strategic minerals, producer-ETF, international broad-market beyond FXI — approved classes with zero radar representation.

---

## 5. Recall-vs-Precision Trade-off (from C, D)

### Recall Proxy #1 — Historical PIT Benchmark (C) — bounded denominator ONLY, never absolute recall
| Level | Bounded recall | Bounded precision | N |
|---|---|---|---|
| Signal (H1) | **100%** (4/4) | **80%** (4/5) | 5 labeled signals |
| Candidate (full gate: H1+rev+stage+liq) | **50%** (2/4) | **100%** (2/2) | 4 labeled candidates |

- 15/15 snapshots **no-look-ahead clean** (guard at source + independent audit + helper cross-check); identity stable (CIK-unique, split-basis PIT correct).
- Negative controls: NVDA@2022-06-30 (rate-hike selloff) correctly silent; JNJ@2023-12-31 (quiet quality) fired at signal layer but **suppressed by candidate gate (S3)** → no false candidate at surfacing layer. The §10 "false-positive exciting story" control works as intended: detector fires, gate filters.
- **Trade-off read:** the H1 detector is recall-rich at the signal layer (100%) but noisy (one-time-item sensitivity — JNJ). Precision is enforced downstream by the stage gate, which is strict (NVDA UNCLASSIFIED in parabolic regimes → candidate recall 50%). Net: **precision-protective by design; recall loss sits at the stage-gate timing filter, not the detector.**

### Rejected-item independent audit (D) — verdicts
| Packet | Verdict | False-negative cost |
|---|---|---|
| 1 — META Form 4s | **INSUFFICIENT** (only immaterial sale described; cheapest next check: read other 3 transaction tables) | Low (single issuer) |
| 2 — Gold 9% weekly surge vs near-peak real yields | **HIGH** — unusual cross-asset config warrants recon (cheapest next check: 5-day return outlier vs distribution) | Medium |
| 3 — **Hormuz chokepoint disruption reports** | **HIGH** — systemic cross-asset potential not reflected in modest WTI rise | **HIGHEST** (oil→inflation→rates→equities→metals simultaneously; recon cheap) |
| 4 — Silver "2y bullish extreme" positioning | **MAYBE** — unverified (CFTC COT 404), five-year-high vault stocks weaken confidence | Medium |
| 5 — AMZN S-4 | **MAYBE** — age + missing combination details; cheapest next check: S-4 cover | Low |

Verdict reading: 2/5 digest-ignored items would merit re-promotion (HIGH) with cheap next checks → **some judgment-layer recall risk exists at the radar promotion boundary**; the audit was done with zero hindsight (bounded, contemporaneous framing). No "probable judgment miss" can be proven on this sample alone — verdict class = *reasonable disagreement / cannot determine*, warranting the observability fix (disposition capture) before any judgment-layer change.

### CoS gate (F) — precision/recall character
- Permissive (fold/defer/approve; **zero rejections** in 16-card sample) → high recall through the gate.
- Risk profile: **deferral-erasure** (0012 has no re-visit trigger — "not now" can become "never") + **capacity concurrency** (WIP 4× breach at batch approval), NOT rejection-erasure.
- No over-preference for urgent/newsworthy: the most dramatic card (0012, gold+Hormuz) was the one braked — precision-protective.

---

## 6. Recall Proxies Used (methodology §6 — bounded denominators)

| Proxy | Status | Evidence | Verdict |
|---|---|---|---|
| (1) Historical PIT Benchmark Recall | **EXECUTED** | C — 15 snapshots, 6 labeled cases, 100% signal recall / 50% candidate recall, 15/15 clean | Methodology executable; PIT integrity holds; JNJ one-time-item = M3 characteristic surfaced, not tuned |
| (2) Rejected-Item Independent Audit | **PARTIAL** | D (radar lane: 5 packets, 2 HIGH/2 MAYBE/1 INSUFFICIENT) + F (CoS lane: **unmeasurable — zero rejections exist**) | Radar lane works; CoS lane needs a rejection/deferral-erasure sample that doesn't exist yet |
| (3) Out-of-Universe Counterfactual Scan | **NOT RUN** | B — proposed bounded sample (10–15 names outside 98), audit-only | Required to make M1 measurable (§11); smallest next probe |
| (4) Coverage Matrix / Blind-Spot Analysis | **EXECUTED** | A (authority map + lane coverage), B (equity 98-name funnel: E1 8/98, E2 98/98, E3 98/98 shadow, deep-research 6/98), E (CS spec-to-impl matrix, wrapper ⛔) | Uncovered the headline M2 (30/98) + wrapper void; P1/P2/P3 definitional gap surfaced |

**Proxy gaps:** no PIT benchmark for QA archetypes or CS lane (A); no latency (M5) probe; survivorship-free PIT universe deferred (Phase 1 D1).

---

## 7. Smallest Recommended System Changes (methodology §30 order — NOT implemented)

All recommendations are audit-only / documentation / bounded-probe in nature. **NO threshold changes, NO new canonical states, NO new queues/scores, NO universe expansion, NO "bigger model".**

### First — Fix observability (know what is being missed and why)
| # | What | Why | Cost | Addresses |
|---|---|---|---|---|
| R1 | **Rejected-item disposition capture** (audit-only): structured register per radar pass — each digest-ignored / QA-not-promoted item gets SURFACED_* label + one-line reason (labels from §9; no new state machine) | Cheapest observability fix; M4 is the highest unmeasured risk (H2); also feeds M6 | Low (digest convention + card field) | M4, M6 |
| R2 | **Deferral re-visit trigger on card**: deferred cards carry re-test condition + owner + target date/event (e.g. 0012 → "re-test after CPI 8/12 + settled Hormuz; owner org-macro-strategist; 12–14 Aug") | Prevents "not now → never" — the concrete §13 risk | Low (audit-only card field) | M6 |
| R3 | **Fix D1/D3 doc drifts**: align workflow_column vocabulary to KANBAN-CONTRACT §2 (or amend §2); refresh equity_inflection README header to FD #89 standing behavior; refresh board.md (D2) | Authority/runtime conflict is material to auditability | Low (documentation only) | M7 |
| R4 | **T0–T5 latency capture** on the card pipeline (filed→triage→scoped→research) | M5 is unmeasured; ~1 day observed but never logged | Low | M5 |

### Second — Fix universe / data coverage
| # | What | Why | Cost | Addresses |
|---|---|---|---|---|
| R5 | **Bounded §11 out-of-universe counterfactual sample**: 10–15 eligible US/ADR names outside the 98, audit-only, no expansion | Only way to make M1 measurable | Medium (one bounded scan) | M1 |
| R6 | **Data Steward D2 commodity de-risking**: hunt current CFTC COT URL + confirm metalcharts-vs-CME primary when unblocked | Largest commodity-lane data risk (single-source dependence) | Low | M2 |
| R7 | **CS copper/oil explicit `NOT EVALUABLE WITH CURRENT DATA`** classification until LME/EIA wiring decision | §18 discipline: never treat unmeasured as neutral | Trivial | M2 |
| R8 | **ADR data-wiring decision**: 19/19 ADRs invisible to E2 (companyfacts 404/insufficient) — Founder chooses accept-as-is vs pursue wiring | 19% of the universe is structurally invisible to the only production scanner | Medium (needs investigation) | M2 |

### Third — Fix deterministic detectors
| # | What | Why | Cost | Addresses |
|---|---|---|---|---|
| R9 | **Resolve P1/P2/P3 definitions in the canonical doc** before scaling the Close System matrix | Spec-definitional gap blocks matrix validity (E F-7/U-7) | Low (definitional) | Spec gap |
| R10 | **Close System wrapper data model fields per §18A** (tracking diff/error, roll/contango, issuer, liquidity, AUM, tax, holdings-vs-thesis) | Wrapper coverage is the void; per §18A each dimension reported separately, no composite score | HIGH — **design direction only (§31), NOT pre-approved for this pilot** | M2/M3 (CS) |

### Fourth — Improve judgment
Not now. §30 order: only after upstream coverage (observability + data) is adequate. D shows some judgment risk (2/5 HIGH) but the sample is too small to justify prompt changes; R1's disposition capture is the prerequisite evidence base.

### Fifth — Add independent sampled challenge
Only where evidence shows material judgment misses. D provides the first evidence point (2/5 HIGH) — propose a **bounded, next-round** challenger exercise on a larger digest-ignored sample, not a standing gate.

### Sixth — Consider persistent rejection/disposition history
Only if audit evidence shows ongoing value. R1 seeds this; decide after R1 has run 2–3 radar passes.

---

## 8. Founder Decisions Required (smallest explicit approvals)

1. **Approve R1 — rejected-item disposition capture** (audit-only register, §9 labels) as the cheapest observability fix. [RECOMMENDED]
2. **Approve R5 — bounded §11 out-of-universe counterfactual sample scope** (10–15 eligible names outside the 98, audit-only, no expansion). [RECOMMENDED]
3. **WIP §5 decision** (R: from F T4): enforce serialization (1 M2/M3 per Principal) OR document an explicit batch carve-out for same-day inflection batches. [RECOMMENDED: explicit batch carve-out — recall-friendly, matches observed practice]
4. **R8 — ADR wiring stance**: accept 30/98 NOT EVALUABLE as-is, or authorize investigation into ADR EDGAR companyfacts wiring. [RECOMMENDED: investigate — 19% of universe invisible]
5. **CS copper/oil**: accept explicit NOT EVALUABLE classification until LME/EIA wiring decision (or authorize wiring). [RECOMMENDED: classify NOT EVALUABLE now]
6. **P1/P2/P3 definitions**: resolve in canonical doc before scaling the Close System coverage matrix. [RECOMMENDED: resolve]
7. **R2 — deferral re-visit trigger**: apply to existing deferred card 0012 (owner+date+event). [RECOMMENDED: apply]

---

## 9. Pilot Findings on the Workflow Itself

**What worked.**
- Bounded-sample discipline held everywhere: no state change, no new thresholds, no universe expansion, portfolio-blind — verified across all six children and re-checked at synthesis.
- The taxonomy (M1–M7) proved usable as a shared classification language across six independent profiles — every finding mapped cleanly to a root cause.
- Parallel execution with explicit per-child methodology anchors + pre-seeded constraints produced high-quality, non-overlapping evidence; handoffs (summary+metadata+artifacts) were complete enough that synthesis needed no repo re-reads.
- PIT integrity machinery (FD #58 filed-date stamps, latest_by_filed guard, lookahead_violations check) held under adversarial re-testing — 15/15 clean.
- Underlying-vs-wrapper separation executed correctly (E) and produced a crisp, honest verdict (wrapper NOT EVALUABLE) instead of a fabricated score.
- Prohibited outcomes were respected even where tempting (e.g. D classified Hormuz HIGH but did not promote; E reported wrapper gaps without adding products).

**What broke.**
- **Dependency-direction fix (operator intervention, 22:06)**: the original graph had parent/child edges in the wrong direction (children were created as parents of t_500dd515); a human operator reversed the edges and the task re-promoted. Cause: edge direction chosen at card creation without a graph-validation step. **Improvement: validate edge direction at kanban_create/link time (a synthesis task must be a child of its workstreams, never their parent); add a graph sanity check to the dispatcher.**
- **CoS rejected-item proxy unmeasurable**: zero rejections exist in the 16-card sample → proxy 2 (CoS lane) cannot run until either a rejection occurs or the digest "deliberately ignored" lists are used as the sample (which D did). **Improvement: define the radar digest-ignored list as the standing rejected-item sample source for next round.**
- **M5 latency unmeasured by construction**: no T0–T5 timestamps existed to audit. **Improvement: add lightweight timestamp capture (R4) before the next round so M5 becomes measurable.**
- **P1/P2/P3 undefined** in the canonical doc blocked full Close System matrix validity (E flagged rather than invented). **Improvement: resolve definitions in the methodology doc before scaling.**

**Next-round candidates (bounded, audit-only, no expansion):**
1. Out-of-universe counterfactual scan (§11) — makes M1 measurable (R5).
2. Rejected-item audit on a larger radar digest-ignored sample (build on D's 5 packets).
3. PIT benchmark extension to QA archetypes + CS lane (per A's proxy status).
4. T0–T5 latency capture + re-audit (R4).

---

*Pilot synthesis — audit evidence only. No domain state changed, no thresholds created. Audit labels used: SURFACED_HIGH / SURFACED_MAYBE / NOT_PROMOTED / INSUFFICIENT_DATA (not canonical states).*
<!-- 2026-08-12 22:45 UTC+7 -->
