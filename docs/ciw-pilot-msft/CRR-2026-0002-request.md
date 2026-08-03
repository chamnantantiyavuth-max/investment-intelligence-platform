# CRR-2026-0002 — Research Request: Microsoft Corporation (MSFT) — Valuation Slice

**Status:** APPROVED v0.4 — Founder approval at the Research Gate, 2026-08-03 (FD-CIW-015, Constitution §21). Prior `Draft → Approved`; approval record below. **Phase 2R COMPLETE: PASS WITH FIXES** (3 rounds, Sol Medium). Execution authorized for the valuation second slice ONLY per FD-CIW-015 (supersedes FD #44 for this scope only).
**Version:** 0.4
**Date:** 2026-08-03
**Authority:** Founder scope direction (session 2026-08-03, Decision: second slice = Valuation, Option A — planning direction only, not a registered FD); `docs/CIW-FIRST-SLICE-DESIGN.md` v0.3 (lifecycle + gates precedent — first-slice scope only); CIW-REQUEST-CONTRACT §3–§4; CIW-RESEARCH-FRAMEWORK §3–§4 (Modules N/O/P advisory scope); FD-CIW-009 (pilot company), FD-CIW-012 (first slice published), FD-CIW-013/014 (monitoring contract live)
**Phase 2R:** FAIL (round 1, 2026-08-03) — 10 findings F1–F10 (see §9 Change Record). Re-review (round 2): F1–F5/F8–F10 ADDRESSED, F6/F7 PARTIAL → completed in v0.3. Targeted confirmation (round 3): **PASS WITH FIXES** — F6/F7 ADDRESSED; N1 (stale v0.2 version text) fixed in v0.4.
**Approval record (Research Gate, 2026-08-03):** prior state `Proposed for Research` (request approval_status `Draft`) → `Approved for Research` (request approval_status `Approved`); actor: **Founder**; reason: Research Gate approval + FD-CIW-015 (Decision, session 2026-08-03, Option A); evidence: this document (CRR-2026-0002 v0.4, SHA-256 `ce7ced52cd20c0530024a3c4fa341c84b63ecb35566ccb648d74040db44978c4`) + `operational/FOUNDERS-DECISIONS.md` item 59; timestamp 2026-08-03; workflow version: CIW v0.2 specs + first-slice design v0.3 (precedent). Source Map 2 may begin (LIFECYCLE §7).

---

## 1. Request Fields

```yaml
request_id: CRR-2026-0002
company_id: MSFT — Microsoft Corporation (NASDAQ: MSFT); Shared Core entity identity
universe: "US-listed common stocks (v0.3)"
origin:
  source_system: investment-intelligence-platform
  trigger_type: founder_commission (CIW second slice — valuation focus; scope direction 2026-08-03
    = draft/review ONLY; execution requires FD-CIW-015 per §7)
  originating_themes: none (portfolio-blind pilot — no theme coupling)
research_question:
  primary: "What is the defensible range of intrinsic value for Microsoft's common equity,
            assessed at advisory valuation depth (Modules N/O/P), and what does the current
            price imply about market expectations relative to that range?"
  secondary:
    - "What are normalized owner earnings, and what is the best-supported maintenance vs
       growth capex split — TESTED AND NARROWED if the evidence supports it; otherwise the
       first-slice disclosed range is retained and left unresolved (no invented split)?"
    - "Can the AI capex build (FY26 $115.9B → CY26 ~$175B) earn above the cost of capital —
       assessed as an explicit, versioned advisory scenario, never a de facto deterministic
       contract or canonical hurdle rate?"
    - "What does the current price embed (reverse-DCF expectations), and which assumptions
       are demanding?"
    - "How does MSFT compare against realistic alternatives on expected return — across ALL
       FIVE Module-P comparator categories (cash/short governments, broad index, strongest
       competitor AWS/AMZN, quality compounder NVDA, lower-risk value opportunity JNJ)?
       All candidates FIXED ex-ante in §4 cat. 8 (FD-CIW-007 shortlist)"
required_depth: valuation-second-slice — depth defined by the method matrix in §5 (required /
          optional-if-evidence-gate / out-of-scope); NOT an open-ended "full" mandate
required_outputs:
  - structured_research_result (research-result-2.md — separate request-bound artifact, §8)
  - source-map-2.md (Source Map for this slice, §4 gate + §8 lineage)
  - challenge-review-2.md (Independent Challenge artifact)
applicable_modules: [G-refinement, H, M-refresh, N, O, P]
justified_omissions:
  - module: A–F
    reason: "Covered at initial depth in CRR-2026-0001 (published v1, Current Authoritative
             for its request scope). NOT re-derived. G-refinement may extract narrowly
             necessary PP&E/depreciation inputs (see §4 cat. 6 + F4 constraint); any work
             that would re-derive an omitted module or change a settled first-slice finding
             is BLOCKED (see founder_constraints — material-new-evidence rule)"
  - module: I
    reason: "Growth decomposition covered in first slice; growth assumptions in N are
             parameterized from first-slice evidence, not re-derived"
  - module: J
    reason: "Normalization/stress cases covered at initial depth in first slice; N uses
             those cases as scenario inputs without re-running the stress analysis"
  - module: K
    reason: "Permanent-loss ranked list from first slice consumed into O downside framing;
             NOT re-ranked"
  - module: L
    reason: "Inversion/pre-mortem covered in first slice; not re-run"
  - module: Q
    reason: "Monitoring indicators governed by CIW-MONITORING-CONTRACT v0.1 (FD-CIW-014,
             Cron Class A live). This slice references the monitoring contract as approved
             monitoring-trigger CONTEXT only — never as deterministic valuation-contract
             authority (F5); it does not re-produce monitoring indicators"
priority: pilot continuation — second slice (workflow validated in first slice; valuation
          depth now tested per RESEARCH-FRAMEWORK §4 advisory scope)
founder_constraints:
  - "Time box: single bounded research pass; draft limited to one research session"
  - "Valuation output is advisory research context ONLY (RESEARCH-FRAMEWORK §4) — no
     'Attractive Below Price', no recommendation framing, no investable verdict, no
     official platform threshold"
  - "Deterministic valuation calculation contracts NOT approved — every assumption
     explicit, versioned, rerunnable, and epistemically labeled (observed / derived /
     analyst-selected scenario); no false precision; no selected WACC, required return,
     terminal assumption, or incremental-ROIC formula becomes an official platform
     contract; if evidence cannot support a range, the answer is INCONCLUSIVE (F4/F5)"
  - "Every material claim must carry claim-level evidence reference (source ID + location)"
  - "Material-new-evidence rule (F2): new evidence may be logged and used ONLY to test a
     selected-module assumption. Any work that would re-derive an omitted module (A–F/I–L),
     change a settled first-slice finding, re-rank K, re-run J/L, or affect a Phase 8
     canonical classification MUST PAUSE, remain `Review Required`, and obtain a versioned
     Founder-approved scope amendment or new request BEFORE execution. Materiality =
     evidence capable of changing a selected valuation input/conclusion — NOT permission
     to expand modules. No 'record deviation and continue' route exists."
portfolio_blind: true
approval_status:
  request: Draft (this document) → Approved (Founder, Research Gate) → Rejected / Superseded
  ciw_research: Proposed for Research (per LIFECYCLE §2 — request drafted, not approved)
     → Approved for Research (only after FD-CIW-015 + exact-request approval)
authority:
  autonomous_investment_decision: false
  founder_final_authority: true
```

## 2. Known Evidence (held by the platform — baseline, not re-derived)

First-slice published evidence (CRR-2026-0001, `research-result.md` v1 — Current Authoritative for its request scope; consumed here, never silently rewritten):

| Evidence | Source (platform record) | Provenance |
|---|---|---|
| Business quality HIGH; FY26 revenue $331.8B (+18%), Microsoft Cloud $214.4B (+27%), RPO $678B (+84%; +25% ex-OpenAI), 2.3-yr weighted duration | `docs/ciw-pilot-msft/research-result.md` v1 (Published) | CIW first slice — real SEC EDGAR primary sources |
| Owner earnings FY26: Low $56.3B ($7.56/sh) · Base $102.7B ($13.78/sh) · High $133.7B ($17.95/sh); 60% maintenance-split = least-supported assumption | same | First-slice Module G (verified rounds 1–2); G-refinement may narrow ONLY with PP&E/depreciation evidence (F4) |
| Capex: FY26 $115.9B → CY26 guided ~$175B; AI capex-return question = central unresolved | same | First-slice §4 Unresolved Q1 |
| Moat Wide/Deep/Widening (Phase 8 canonical, consumed) + initial-depth primary-source support | Phase 8 canonical + first slice | Phase 8 owns classification; CIW never re-classifies |
| Commitment stack: **separately disclosed categories with POTENTIAL OVERLAP — NOT additive.** Contractual obligations $743.8B; not-yet-commenced leases $329.1B. First-slice result v1 states they are not double-counted but exact non-overlap REQUIRES underlying schedules (Unresolved Q6). **Summing to $1.073T is PROHIBITED absent an evidenced reconciliation (F3)** | first-slice result §2 + §4 Q6 | First-slice (F5); caveat carried into this slice's valuation/downside work |
| FCF FY26 $67.0B ($8.99/sh); price $464.72 (7/31 close); trailing P/E ≈ 25.9×; P/OE base ≈ 33.7× | first-slice result §3 | SRC-MKT + computed |
| Monitoring contract v0.1 (I-1..I-14) LIVE — draft notes weekly, next real data-point Q1-FY27 (~Oct 2026) | `CIW-MONITORING-CONTRACT.md` v0.1 | FD-CIW-013/014; approved monitoring-trigger context only |

**CIW second slice adds valuation depth (Modules N/O/P + G/H/M refinement) on top of this published baseline. Settled first-slice findings stand unless a Founder-approved amendment permits change (F2).**

## 3. Known Counterevidence (visible from the start — REQUEST-CONTRACT §3)

- **Valuation-rich price:** trailing P/E ≈ 25.9×; P/OE base ≈ 33.7×; EV ≈ $3.42T conventional / $3.50T lease-adjusted. Market already embeds high expectations (first-slice Module M).
- **Capex-return uncertainty:** $115.9B FY26 → ~$175B CY26 build; durability of returns unproven at scale; owner-earnings spread $56B–$134B unresolved.
- **Commitment-stack rigidity:** $743.8B contractual obligations + $329.1B not-yet-commenced leases — **separate categories, potential overlap, not summed** (F3); fixed-cost obligations in a demand downturn.
- **OpenAI dependence:** ~25% as-converted equity, $13.0B commitments, FY26 related-party revenue $24.1B (7.3%); RPO +84% total vs +25% ex-OpenAI.
- **Regulatory:** antitrust scrutiny (US/EU), OpenAI exclusivity scrutiny, IDPC LinkedIn appeal ($553M accrued).
- **Accounting optics:** FY27 useful-life extension (15→25yr) + lease reclassification effects on reported capex/margins.
- **Competition:** AWS, Google Cloud, frontier-AI model commoditization, potential margin pressure.

These are recorded **now**, before research begins, and must remain visible in the draft and result (never averaged away — EVIDENCE-MODEL §7).

## 4. Source Gate (REQUEST-CONTRACT §4 — minimum source gate for this request)

| # | Source category | Requirement for this request |
|---|---|---|
| 1 | Latest annual filing (10-K) | Required — MSFT FY2026 10-K (SRC-001, first-slice reviewed; re-verified for valuation inputs) |
| 2 | Latest interim filing (10-Q) | Required — latest filed 10-Q within filing cycle (FY2026 Q3; SRC-002 reviewed). Q1-FY27 not yet filed (~Oct 2026) — recorded, not hidden |
| 3 | Earnings releases + transcripts | Required — four most recent quarters (SRC-003a–d reviewed); refresh only if new release since first slice (none expected pre-Q1-FY27) |
| 4 | Proxy/compensation (DEF 14A) | Not required for this slice (Module E out of scope; consumed from first slice SRC-004) |
| 5 | Regulatory sources | Required where material — consume first-slice SRC-005 statuses; refresh only on material new development |
| 6 | Historical filings + PP&E/depreciation evidence (F4) | Required — first-slice SRC-006a–e (10-Ks FY21–FY25) + SRC-XBR (XBRL company facts). **Source Map 2 MUST additionally seek by class and period: PP&E gross carrying value, accumulated depreciation, useful lives, depreciation expense, additions/retirements, finance leases, and any asset-age/replacement-cycle disclosures.** Explicit `not disclosed` / `incomplete` / `justified-absent` handling required; a missing field permits a ranged/inconclusive result — it does NOT authorize an invented maintenance-capex percentage |
| 7 | Market + valuation inputs (F5) | Required — current price/quote refresh (SRC-MKT, as-of 2026-08-03); US 10-yr Treasury (risk-free rate). **Bounded valuation-input schedule (see §5 Valuation-Input Discipline):** equity-risk-premium inputs, capital structure, debt cost, tax treatment, dilution/share count, terminal assumptions — each with source, as-of rule, formula/variant disclosure, sensitivity range, and epistemic label (`observed` / `derived` / `analyst-selected scenario`). If a required input cannot be supported by evidence, the affected answer is INCONCLUSIVE — never a defaulted point estimate |
| 8 | Peer/alternative comparator inputs (Module P — F6) | Required — **ALL FIVE Module-P categories, each with a FIXED ex-ante candidate named IN THIS REQUEST** (from the Founder-approved CIW shortlist, FD-CIW-007: JNJ/AAPL/META/NVDA — portfolio-blind, pre-vetted, no post-hoc selection): (a) cash / short-duration governments (US 10-yr Treasury yield — also cat. 7); (b) broad market index (S&P 500 valuation/yield context); (c) strongest competitor (**AWS via AMZN** — primary public filings required for material fundamental inputs, not just market price); (d) another quality compounder (**NVDA — FIXED candidate**, no substitution without an approved request amendment); (e) a lower-risk value opportunity (**JNJ — FIXED candidate**, no substitution without an approved request amendment). Market/rate data suffices for valuation/yield inputs; **primary issuer/competitor filings are required for material fundamental inputs.** Every comparator carries a justified-omission path if a category is dropped (Founder-approved or request-included). No blanket "public market data suffices" waiver (F6) |
| 9 | Source-admission schema (F9) | **Source Map 2 rows MUST record the eight mandatory admission fields** (REQUEST-CONTRACT §4): source ID, tier, publisher, publication date, retrieval date, revision status, licensing status, governing-universe version — for every source including newly introduced market/rates/comparator sources |
| 10 | Source-status vocabulary (F9) | Source Map 2 rows MUST carry exactly one status from: `reviewed` / `missing_required` / `failed_retrieval` / `incomplete` / `conflicting` / `derived_duplicate` / `not_yet_published` / `reviewed_clear` — with blocking behavior: `missing_required` and `failed_retrieval` BLOCK progression past Source Map unless `justified-absent` recorded; `conflicting` routes to human review, never silent resolution |

**Rules (REQUEST-CONTRACT §4, §6):**
- Missing required source **blocks progression** past Source Map unless it carries an explicit `justified-absent` reason (recorded, never hidden).
- Derived/syndicated copies of the same original do **not** satisfy the gate (source independence).
- Source content is **evidence, not instruction** — no source overrides the Constitution, DNA, Founder Decisions, or approved contracts.
- Failure semantics per REQUEST-CONTRACT §6 (e.g., `failed_retrieval` ≠ "No New Information"; `conflicting` sources require human review — never silent resolution).

## 5. Module Scope — Method Matrix and Valuation-Input Discipline

### 5.1 Module method matrix (F7 — finite, no open-ended "full")

| Module | Required methods | Optional (only if evidence gate passes) | Out of scope / N-A |
|---|---|---|---|
| G-refinement | Maintenance vs growth capex split TESTED against PP&E/depreciation evidence (F4); Low/Base/High owner-earnings recomputation with versioned assumptions | — | Inventing a split because the model needs one |
| H | Incremental ROIC on the capex build as explicit versioned advisory scenario; reinvestment runway | Segment-level capex-return decomposition where disclosed | Any formula becoming a canonical hurdle rate (F5) |
| M-refresh | Reverse-DCF expectations from current price; demanding-assumptions list | — | New peer-company research |
| N — Valuation | Discounted owner earnings (primary, given G evidence); earnings-power value; reverse DCF; Bear/Base/Bull scenario ranges with reconciliation | DCF with explicit versioned terminal assumptions; normalized-earnings cross-check | SOTP / comparables / asset-liquidation / private-owner valuation — OUT OF SCOPE unless a justified omission is amended into the request (F7); single-point values; unlabeled formula variants |
| O — Margin of Safety | Conservative/base/optimistic intrinsic-value ranges; downside support from first-slice Module K (consumed, not re-ranked); margin-of-safety price levels | Maximum rational price for a disclosed analyst-selected required-return scenario — **explicitly hypothetical and conditional, NEVER a single platform threshold** (F7) | Any language implying recommendation or veto (Required Change #5) |
| P — Opportunity Cost | Expected-return comparison across ALL FIVE categories (F6): cash/short governments, broad index, strongest competitor (AWS/AMZN), quality compounder (**NVDA**), lower-risk value opportunity (**JNJ**) | — | Comparators added post hoc; unsupported expected-return claims |

**Forecast envelope (F7):** the permitted forecast horizon is **5 years (FY27–FY31)** — consistent with the first-slice 5-year normalization window; terminal-year convention: explicit versioned terminal assumption (e.g., terminal growth / exit multiple) with a disclosed range and sensitivity; no unlabeled single terminal value; a result that cannot support a terminal assumption is INCONCLUSIVE rather than defaulted. No forecast beyond FY31 without a Founder-approved amendment.

**Aggregation rule (F7):** each method produces its own range; ranges are reconciled and presented as a disclosed spread with method-specific assumptions — never averaged into one opaque number, never hardened into an official threshold.

### 5.2 Valuation-Input Discipline (F5 — advisory, never de facto contracts)

- Every valuation input (WACC / required return, ERP, debt cost, capital structure, tax, terminal growth, maintenance split, share count/dilution) carries: source reference, as-of date, formula/variant disclosure, sensitivity range, and epistemic label (`observed` / `derived` / `analyst-selected scenario`).
- No selected input becomes an official platform contract or hurdle rate. If evidence cannot support a range → **INCONCLUSIVE** (recorded, never defaulted).
- Module-Q approved monitoring thresholds (incremental-ROIC proxy, 8–10% trigger range) may be referenced ONLY as approved monitoring-trigger context — never as valuation-contract authority (F5; CIW-CONCEPT §5).
- Deterministic calculation contracts remain deferred (RESEARCH-FRAMEWORK §4). Valuation ranges are research context for the Founder — never an official platform output.

## 6. Research Status Path (LIFECYCLE §2, §7 — two axes explicit, F8)

```
REQUEST AXIS:        Draft (v0.3, this document) → Approved (Founder, Research Gate) → Rejected / Superseded
CIW RESEARCH AXIS:   Proposed for Research (request drafted, not approved)
                       → Approved for Research (ONLY after BOTH:
                            (1) FD-CIW-015 named second-slice authorization recorded (§7), AND
                            (2) Founder approval of this exact request version/hash)
                       → Researching (only after approved scope + Source Map 2 gate pass)
                       → Draft → quality gates → Independent Review → Founder Review → Published / Current Authoritative v1
```

**Prohibited:** AI → Published; Cron → any authoritative state; Reviewer → Published; any transition without audit fields (prior state, new state, actor, reason, evidence reference, timestamp, workflow version).

## 7. Approval Flow (REQUEST-CONTRACT §7 + F1 — named FD REQUIRED)

1. AI drafts this request (Class B — v0.1, done).
2. **Phase 2R independent review** (mandatory — Critical Mode financial logic): round 1 FAIL (F1–F10, addressed v0.2) → round 2 F6/F7 PARTIAL (completed v0.3) → round 3 targeted confirmation: PASS WITH FIXES (F6/F7 ADDRESSED; N1 stale-version text fixed in v0.4).
3. **FD-CIW-015 — NEW NAMED FOUNDER DECISION (required, cannot be inherited):** FD-CIW-011 authorized the MSFT first slice ONLY. Second-slice execution requires a new FD that (a) identifies `CRR-2026-0002` by exact version/hash, (b) authorizes the valuation second-slice execution, (c) supersedes FD #44 for this scope only, (d) repeats the non-scope: no deterministic valuation contracts, no official state changes, no new automation/schema/profile, no autonomous action.
4. **Founder reviews** the 2R-passed request: scope, modules, omissions, source gate, method matrix, constraints, 2R disposition.
5. **Founder approves / rejects / returns for revision** — approval identifies request ID, final version, content hash, actor, reason, timestamp, evidence reference, workflow version, and FD-CIW-015 (Constitution §21 — casual agreement is not approval).
6. Approved request + recorded FD-CIW-015 activate `Approved for Research` → Source Map 2 proceeds.

## 8. Artifact Lineage (F10)

| Artifact | Path | Relationship to first slice |
|---|---|---|
| This request | `docs/ciw-pilot-msft/CRR-2026-0002-request.md` | Separate request-bound artifact (CRR-2026-0002) |
| Source Map 2 | `docs/ciw-pilot-msft/source-map-2.md` | Separate; consumes SRC-001..006 statuses, adds new sources (cat. 7–10) |
| Research draft 2 | `docs/ciw-pilot-msft/research-draft-2.md` | Separate request-bound draft |
| Independent Challenge | `docs/ciw-pilot-msft/challenge-review-2.md` | Separate review artifact (Sol Medium, separate context) |
| Research result 2 | `docs/ciw-pilot-msft/research-result-2.md` | **SUPPLEMENTAL, request-bound result — NOT a supersession of v1.** `research-result.md` v1 remains Current Authoritative, unchanged and retrievable, for its request scope (A–M initial depth). Where this slice refines an advisory figure (e.g., owner-earnings split, valuation ranges), the new figure appears in `research-result-2.md` marked as a valuation-slice refinement; the v1 figure remains visible with an explicit cross-reference. One Current Authoritative per artifact (LIFECYCLE §5); no in-place mutation of v1 (append-first, PUBLICATION-STANDARD §5) |
| Founder approval record | `docs/ciw-pilot-msft/founder-review-record-2.md` + FD-CIW-015/016 | New records referencing this request/version/hash lineage |

**Lineage rule:** request, Source Map 2, draft, challenge, result, and publication records MUST reference the same request ID + version lineage. Any change after Founder approval = new version + new review cycle (append-first).

## 9. Change Record (2R round 1 → v0.2; targeted confirmation → v0.3)

| Finding | Severity | Disposition |
|---|---|---|
| F1 | CRITICAL | ADDRESSED (v0.2) — §7: FD-CIW-015 named FD REQUIRED before `Approved for Research`; header states current direction = draft/review only |
| F2 | HIGH | ADDRESSED (v0.2) — founder_constraints: material-new-evidence rule rewritten — pause + `Review Required` + Founder-approved amendment; materiality defined; no "record and continue" |
| F3 | HIGH | ADDRESSED (v0.2) — §2/§3: commitment amounts restated as separate categories with potential-overlap caveat; summing prohibited; first-slice Q6 carried into valuation work |
| F4 | HIGH | ADDRESSED (v0.2) — §1 Q1 + §4 cat. 6 + §5.1: "test and narrow IF evidence supports; else retain range"; PP&E/depreciation field inventory added; inconclusive allowed |
| F5 | HIGH | ADDRESSED (v0.2) — §4 cat. 7 + §5.2 Valuation-Input Discipline added: full input schedule, epistemic labels, sensitivity ranges, inconclusive rule, Module-Q context-only rule |
| F6 | HIGH | ADDRESSED (v0.2) PARTIAL → **COMPLETED (v0.3)** — §4 cat. 8 + §5.1 P: all five comparator categories now carry FIXED ex-ante candidates named in the request (AMZN/AWS competitor, **NVDA** quality compounder, **JNJ** lower-risk value — from the FD-CIW-007 approved shortlist; no substitution without an approved amendment); waiver removed |
| F7 | HIGH | ADDRESSED (v0.2) PARTIAL → **COMPLETED (v0.3)** — §5.1: method matrix (required/optional/out-of-scope) + aggregation rule + **Forecast envelope added: 5-year horizon (FY27–FY31), explicit versioned terminal assumption with disclosed range + sensitivity, no unlabeled single terminal value, >FY31 requires amendment**; "maximum rational price" explicitly hypothetical/conditional |
| F8 | MEDIUM | ADDRESSED (v0.2) — §1 approval_status two-axis + §6 two-axis status path; approval record fields enumerated |
| F9 | MEDIUM | ADDRESSED (v0.2) — §4 cat. 9–10: eight admission fields + status vocabulary with blocking behavior |
| F10 | MEDIUM | ADDRESSED (v0.2) — §8 artifact lineage: paths, supplemental-not-supersession, v1 preserved, single Current Authoritative per artifact |

---

*Draft v0.4 (session 2026-08-03, second slice — valuation focus). Phase 2R COMPLETE: round 1 FAIL (F1–F10, Sol Medium) → round 2 F6/F7 PARTIAL → round 3 targeted confirmation PASS WITH FIXES (F6/F7 ADDRESSED; N1 fixed in v0.4). Sources: CIW-REQUEST-CONTRACT §2–§7; CIW-RESEARCH-FRAMEWORK §3–§4; CIW-CONCEPT §5–§6; CIW-LIFECYCLE §2/§7; CIW-QUALITY-GATES §2/§5; CIW-PUBLICATION-STANDARD §5; FD-CIW-007/009/010/011/012/013/014; first-slice published result v1.*
<!-- 2026-08-03 17:05 UTC+7 -->
