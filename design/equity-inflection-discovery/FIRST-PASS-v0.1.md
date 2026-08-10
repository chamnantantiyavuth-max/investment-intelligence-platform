# Equity Inflection Discovery — First-Pass Deliverable (A–J)

**Status:** Direction review output — ANALYSIS ONLY. No code, no governance, no contract, no schema, no UI changed.
**Version:** 0.2 (10 Aug 2026) — **FD #88 APPROVED** (Stage Definition v0.1 + revenue confirmation adopted as design basis; scanner shadow-gated).
**Approval:** Founder Option A, 10 Aug 2026 → registered as FD #88 (FOUNDERS-DECISIONS item 104).
**Source direction:** `ChatGPT/FOUNDER-DIRECTION-EQUITY-INFLECTION-DISCOVERY-AUDITED.md`
**Repository truth verified:** 10 Aug 2026 (HEAD `54c3a1f`, 321 commits, fd_count 103, tests 145/145, push SYNCED)
**Author:** IIP profile (DeepSeek V4 Flash — planning/design per model routing)

---



---

## APPROVED SPEC — FD #88 (10 Aug 2026, Option A)

The Founder reviewed the first-pass deliverable and refined the core logic before approval:

> "Earning Breakout ออกจากกรอบ มันต้องมี fundamental บางอย่างที่สำคัญเปลี่ยนไปเป็นจุดเริ่มต้นที่น่าสนใจในการติดตาม โดยผมจะตัดหุ้นพวก late stage 2, กับ stage 3, stage 4 ออกไป แต่ผมว่าต้องมานิยามเรื่อง Stage ดีๆก่อน ซึ่งผมว่าการกรองแบบนี้เราจะได้หุ้นที่อาจจะมีการเปลี่ยนแปลงสำคัญในบริษัท + ราคายังวิ่งไปไม่ไกลมากนัก มาเข้า list ไว้"

### Approved design basis

1. **Breakout definition (with revenue confirmation):** latest quarterly EPS breaks above the earnings range of the prior ~2 years (earnings-power inflection, NOT a mechanical EPS print — seasonality, base effects, buybacks, tax, one-offs, accounting changes, M&A, cyclical peaks all handled explicitly). **Revenue confirmation required:** revenue must not be shrinking — a rising EPS with flat/falling revenue is treated as buyback/tax/one-off-driven, not a fundamental change. (Revenue confirmation is part of the breakout definition, not an extra gate.)
2. **Stage Definition v0.1 (deterministic, price/volume only):**
   - Stage 4 (excluded): price < 50MA < 150MA — declining structure.
   - Stage 3 (excluded): 50MA below 150MA (death-cross zone) or price below 50MA while 150MA not yet rising — topping/distribution.
   - Stage 1 (eligible — watch): price within ±5% of 50MA; 50MA within ±5% of 150MA; both slopes near-flat (|slope| < 0.5%/month); price in the 30–70% band of the 52-week range.
   - Stage 2 (eligible only if EARLY): price > 50MA > 150MA, both sloping up; EARLY = price ≤ ~15% above 50MA (not extended — "ราคายังวิ่งไปไม่ไกล") AND recent base breakout (≤ ~8 weeks since first crossing above both MAs, or 50MA turned up ≤ 4 weeks ago). LATE Stage 2 (excluded) = extended > 15–20% above 50MA, or > 8–12 weeks in Stage 2, or RS at extreme percentile.
   - All numeric thresholds above are PROPOSED values for the shadow scanner — subject to Founder approval with validation evidence before any production use (FD #53).
3. **Stage 1 vs Early Stage 2 treatment:** Stage 1 → watch / CoS triage / possible bounded Catalyst Recon; Early Stage 2 → priority triage / bounded recon / possible Full Research Mandate (direction §4B logic).
4. **Firewall, mandate neutrality, radar boundary, enrichment-advisory, theme-not-eligibility, PIT, portfolio-blind, no auto-mandates, shadow-gate:** all as specified in sections C–J below, now binding via FD #88.

## A. CURRENT-TRUTH RECONCILIATION

Established from: `AGENTS.md`, `PROJECT_STATE.md`, `operational/FOUNDERS-DECISIONS.md` (register items 100–103), `operational/hermes-organization/ROLE-REGISTRY-v0.1.md`, role contracts 05 + 11, `reports/README.md`, `design/alpha-momentum-v0/ONEIL-MINERVINI-RULE-PACK.md`.

### A.1 What is ACTIVE (authoritative current model)

| Layer | State | Evidence |
|---|---|---|
| **Research org = the product** (Plan A v0.3) | ACTIVE | FD #64/#65 (register items 80–81); role 05 "research Principal under Plan A v0.3 — the research organization is the product, not the frozen pipeline" |
| **Research workflow (RM-#### pattern)** | ACTIVE | Task Idea Card → CoS triage → RM → small research cell → independent first passes (anti-anchoring) → evidence build → main essay → cross-exam → CRO opposing → audit → re-audit → IC Secretary synthesis → Founder gate → blog. Proven end-to-end by RM-2026-0001 (Apple moat), RM-2026-0002/0003, RM-2026-0004 (Apple deep analysis, FD #87) |
| **Blog = primary Founder-facing product** | ACTIVE | FD #62 (reports-as-product), FD #84/B + #85 (Feature Magazine), FD #86 (blog primary, `/` → /library; legacy trimmed to Org Office + Kanban Board; 13 legacy page files deleted) |
| **Radar Scout (role 11)** | ACTIVE | FD #71 (dedicated role), FD #78 (weekly Mon 08:00 UTC+7 cron), FD #80 (mid-week Thu cron), FD #81 (EDGAR filings scan, 8 FO-universe CIKs), FD #82 (feedback loop via `kanban/card-outcomes.md`) |
| **Analytical Freedom Doctrine** | ACTIVE | Direction §5 encoded in role 05; FD #64 item 7 (specs/checklists NOT auto-loaded into first pass); "Not a checklist processor: no pass/fail, no scorecards" |
| **Point-in-time rule** | ACTIVE | FD #58 (Must Rule) + `operational/EVIDENCE-DOCTRINE.md` Aging section; reports contract requires date-stamped + sourced figures |
| **No invented thresholds (FD #53)** | ACTIVE | Universal constraint — any threshold in the new protocol needs explicit Founder approval with evidence |
| **Portfolio blindness** | ACTIVE | Constitution §23.8.1; radar + research never receive portfolio context |
| **Frontend** | ACTIVE | Standalone magazine shell (/library + /library/:slug), legacy Layout holds Org Office + Kanban; backend FastAPI (org_store.py, /api/reports, /audit UI-4) |

### A.2 What is FROZEN (present, archived in place — FD #65)

| Item | State |
|---|---|
| Alpha Momentum pipeline (`alpha-momentum-v0/`: pipeline.py, q_conditions.py, run.py, run_real.py, source_adapter.py, display.py) | FROZEN — real EOD data via yfinance, 35-slot; no longer a screening service |
| Fundamental & Opportunity pipeline (`fundamental-opportunity-v0/`) | FROZEN |
| Institutional Intelligence pipeline (`institutional-intelligence-v0/`) | FROZEN |
| Close System pipeline (`close_system/`) | FROZEN — labeled synthetic demo |
| Old platform routes/pages | DELETED from App.tsx (FD #86); backend API + data untouched |
| O'Neil/Minervini Rule Pack (`design/alpha-momentum-v0/ONEIL-MINERVINI-RULE-PACK.md`) | FROZEN as **spec document only** — "spec not code; exact formulas, windows, weights, thresholds, automated scoring implementation remain deferred until explicitly approved" (FD #39) |

### A.3 What is SUPERSEDED

| Item | Superseded by |
|---|---|
| Old platform-as-dashboard model | FD #62 platform pivot (reports = product) |
| Dark terminal design (FD #49) | FD #51 Research Desk → FD #85 magazine |
| FD #74 momentum-screen mandate | **FD #75 REVERSED** (history preserved, never deleted) |
| v2.1 light editorial / Research Desk for blog surfaces | FD #84/#85 Feature Magazine (blog surfaces) |

### A.4 What FD #75 currently PREVENTS

- **Any momentum screening anywhere in the org** (no RADAR-002, no momentum cards; role 11 momentum sections removed; radar restored to FD #71 discovery-only).
- Note the semantic overlap: the O'Neil "C — Current Quarterly Earnings" is a momentum/acceleration signal. An earnings-inflection scanner is precisely the kind of systematic screen FD #75 removed. **Therefore the new FD must explicitly supersede FD #75 to the minimum extent necessary** — authorizing earnings-inflection screening as *research intake*, NOT as a momentum-trading signal.
- FD #75 does NOT prevent: anomaly/divergence discovery, fundamental/moat research, or discretionary Founder chart reading. The new protocol must keep those intact.

### A.5 Any decision AFTER FD #87 changing the known checkpoint?

**No.** Register items 101–103 = FD #85/#86/#87 (9 Aug). fd_count 103. Nothing after FD #87. Next FD number = **#88** (verify at registration).

### A.6 Current Radar Scout behavior (role 11)

Discovery-only scanning (anomalies/divergences/filings → Task Idea Cards → Inbox), portfolio-blind, 0–3 cards/pass (Mon), 0–2 (Thu), feedback loop rules (do-not-reraise / known-gap / refine), EDGAR delta for the 8-CIK watchlist, MSFT = digest-only (CIW paused). Radar NEVER writes theses or analyzes.

### A.7 Current Equity Research behavior (role 05)

Research Principal: independent first pass → evidence build → main essay (free-form) + Evidence & Quant Appendix; may request cross-exam/CRO/audit; recommends disposition (continue/monitor/challenge/retire). No scorecards, no auto-loaded specs.

### A.8 Current full-company research capability

PROVEN — RM-2026-0004 (AAPL deep analysis, FD #87): 6 anti-anchoring views → 6-dimension essay → cross-exam 7/7 → CRO FAIL → audit MAJOR → re-audit CLEAN WITH MINORS → Founder gate A → published with dissent. Library 24 published reports (Apple 10, Silver 8, Gold 2, JNJ 2, Weekly 2). Company series work as `subject`-linked narrative.

### A.9 Current Blog architecture

Standalone magazine shell; `/library` (hero feature + asymmetric grid + latest stream + series chips + filters) + `/library/:slug` (typeset article + provenance chips + series prev/next); backend `/api/reports` read-only auth-gated, git single writer; reports contract: `reports/<slug>.md` frontmatter `type: company|product|weekly|quarterly|theme`, status draft → review → published (Founder approval).

---

## B. FIT-GAP (direction item → current behavior)

| # | Direction item | Classification | Basis |
|---|---|---|---|
| 1 | Preserve research org; no platform rebuild | **ALREADY EXISTS** | FD #62/#64/#65/#86 |
| 2 | STRUCTURE OPERATIONS, NOT THINKING | **ALREADY EXISTS** | Analytical Freedom Doctrine (role 05); FD #64 item 6/7 |
| 3 | Equity Inflection Discovery protocol (research intake) | **NEW CAPABILITY REQUIRED** | No discovery scanner exists in the research path |
| 4 | Earnings Inflection scanner, 2 hypotheses separate | **NEW CAPABILITY REQUIRED** | AM frozen; rule pack spec-only |
| 5 | Stage eligibility (1 + early 2 only) | **CONFLICTS WITH FD #75** (supersede minimally) | FD #75 removed momentum/stage screening; rule pack Stage Analysis is spec-only |
| 6 | Change-Driver / Catalyst Recon (bounded intake) | **NEW CAPABILITY (small)** | Radar cards carry suggested questions but no bounded intake-recon artifact between CoS triage and RM |
| 7 | Point-in-time integrity for scanner | **DOCTRINE EXISTS / INFRA NEW** | FD #58 + EVIDENCE-DOCTRINE apply to research; scanner-side PIT data handling is new infra |
| 8 | Intellectual firewall (discovery vs research) | **BOUNDARY EXISTS DE FACTO / NOT ENCODED** | Radar never analyzes (role 11); no explicit firewall contract for a scanner feed |
| 9 | O'Neil/Minervini as discovery LENS; minimal core; enrichment ≠ gate | **CONFLICTS WITH FD #75** for the screening act; **ALREADY EXISTS** as concept spec (FD #39) | Rule pack is spec-only; reuse concepts, not rules |
| 10 | Neutral mandate / anti-anchoring | **ALREADY EXISTS** | FD #64 item 7; role 05 prohibitions; RM-2026-0004 practice |
| 11 | Radar boundary preserved | **ALREADY EXISTS** | Role 11 contract |
| 12 | Scanner deterministic; AI interprets | **NEW CAPABILITY** (design principle) | No scanner infra in research path |
| 13 | Full company research stays free-form | **ALREADY EXISTS** | Role 05; FD #87 demonstrated |
| 14 | Checklists QA-only; no Founder scorecards | **ALREADY EXISTS** | Role 05 prohibitions; reports contract |
| 15 | Blog preserved; content families | **ALREADY EXISTS**; taxonomy = SMALL AMENDMENT (later) | reports/README.md type field |
| 16 | Don't publish every screen hit | **ALREADY EXISTS** | draft → review → published flow; radar cards = internal workpapers |
| 17 | Company research series | **ALREADY EXISTS** | subject-linked series (Apple 10) |
| 18 | "Why this reached our desk" brief | **SMALL AMENDMENT** (report convention, no code) | reports contract |
| 19 | Do-not-revive list | **ALREADY EXISTS as constraints** | Frozen platform (FD #65), no broker/scores (constitution + role prohibitions) |
| 20 | Coexists with Close System / other research | **ALREADY EXISTS** | Radar broad mission (role 11) |
| 21 | Research capacity protection | **ALREADY EXISTS de facto**; stage-tiered gating = SMALL AMENDMENT | CoS triage + RM gating |
| 22 | Validation & shadow pilot | **NEW CAPABILITY** | No PIT validation infra for discovery signals |
| 23 | Blog impact minimal | **PREFER NO UI CHANGE** | Direction §11/§18.I |

**Summary:** 12 items ALREADY EXIST, 7 NEW CAPABILITY (3/4/6/8/12/22 + scanner PIT infra), 2 CONFLICTS (5, 9 → resolved by one new FD superseding FD #75 minimally), 3 SMALL AMENDMENTS (15/18/21).

---

## C. MINIMUM-CHANGE DESIGN

**Principle:** one new deterministic scanner module + one thin intake-recon artifact + one new FD. Zero new roles, zero new cron (initially), zero frontend/schema change, zero new dependencies beyond existing yfinance adapter conventions.

```
┌────────────────────────────────────────────────────────────┐
│  DISCOVERY SIDE (structured, deterministic — new module)   │
│                                                            │
│  discovery/equity-inflection/scanner.py                     │
│   • Earnings Inflection signal (hypotheses SEPARATED)       │
│   • Stage eligibility proxy (deterministic components only) │
│   • data/liquidity sanity (price, volume, float proxy)      │
│   • PIT handling (as-of availability timestamps)            │
│   • enrichment signals COMPUTED but NOT gating (RS, est.    │
│     revisions, volume stats — advisory only)               │
└───────────────────────────┬────────────────────────────────┘
                            │ candidate list (deterministic output)
                            ▼
        Radar Scout (role 11 — UNCHANGED contract)
        signal/provenance sanity + "why unusual" + card
                            │ Task Idea Card (existing schema)
                            ▼
                      CoS Triage (UNCHANGED)
                            │
        ═══════════ INTELLECTUAL FIREWALL ═══════════
                            │
                            ▼
   Bounded Catalyst Recon (role 05 — new LIGHT artifact,
   1–2 pages max, owner = Equity Alpha; "no single
   catalyst" is a valid outcome)
                            │
              ┌─────────────┴─────────────┐
         weak/unclear                material/interesting
              │                              │
        Watch/Archive                   Neutral Big Question
                                              │
                                      Full Research Mandate
                                      (existing RM-#### chain)
```

**What is reused (direction §15: legacy code reusable as infrastructure):**
- `alpha-momentum-v0/source_adapter.py` (yfinance fetch + corporate-action handling) as data infra — read-only, NOT revived as a pipeline.
- Rule Pack (FD #39) concepts ONLY (stage characteristics, earnings acceleration, sales confirmation) — never its entry/exit/stop-loss/position-sizing/regime-veto/Theme-gate/scoring.
- Existing kanban card schema + CoS triage + RM workflow + reports contract — untouched.

**What is new (3 files-ish, all discovery-side):**
1. `discovery/equity-inflection/scanner.py` — deterministic, reproducible, PIT-honest.
2. `discovery/equity-inflection/README.md` — semantics, lineage, boundaries (firewall contract).
3. Optional thin template `templates/13-CATALYST-RECON.md` (org template set has 01–12).

**What is NOT built (explicit anti-regression):** no dashboard, no scores, no pass/fail, no automatic RM, no publish-on-hit, no blog change, no cron (until validation passes + named FD).

---

## D. FOUNDER DECISION DRAFT

> **FD #88 — Equity Inflection Discovery AUTHORIZED as Research-Intake Capability (NOT platform revival).**
>
> 1. **Scope:** The IIP research organization is authorized to operate a deterministic, point-in-time-honest **Equity Inflection Discovery scanner** whose sole purpose is to surface companies whose underlying earnings power may be changing **before/during earliest market recognition**, for disciplined intake into the existing free-form research organization (Task Idea Card → CoS triage → Catalyst Recon → RM). This is a **research-discovery protocol**, not an investment platform, not a portfolio system, not a buy/sell engine.
> 2. **Supersession (minimal, FD #75):** FD #75's prohibition on momentum screening is superseded **only to the extent necessary** for earnings-inflection discovery as research intake. All other FD #75 content stands: no momentum cards as trading signals, radar remains discovery-only, no momentum analysis in research conclusions, Founder still reads charts himself. FD #74/#75 preserved as history (amendment chain, never deleted).
> 3. **Boundaries (Anti-Regression Guardrails):**
>    - Scanner output NEVER auto-creates a Research Mandate, thesis, or publication. CoS triage is the only entry to research capacity.
>    - Discovery data lives in the audit trail; it is NEVER auto-loaded into independent first passes (FD #64 item 7 discipline).
>    - The scanner computes deterministic signals only. No LLM-reasoned scores. AI (radar) interprets, packages, and questions — it does not score.
>    - No thresholds, windows, weights, or formulas enter production without Founder approval supported by point-in-time validation evidence (FD #53).
>    - O'Neil/Minervini concepts (FD #39 rule pack) are a discovery LENS only — never entry/exit/stop-loss/position-sizing/regime-veto/Theme-gate/scoring inheritance.
>    - Enrichment signals (relative strength, volume, institutional proxies, estimate revisions) are advisory; none becomes a hard gate without separate Founder approval.
>    - Theme membership is enrichment by default, never eligibility.
>    - No new role, no new cron, no frontend change, no schema change, no broker/allocation/execution (constitution unchanged).
> 4. **Stage eligibility:** only Stage 1 (watch) and Early Stage 2 (priority candidate) enter the protocol; Late Stage 2/3/4 excluded. Stage definitions must be reproducible; deterministic components computed, interpretive components marked as such.
> 5. **Catalyst Recon:** bounded intake step owned by Equity Alpha (role 05); radar never owns company-economic interpretation; "no identifiable single catalyst" is a valid outcome.
> 6. **Validation:** the scanner runs in SHADOW mode (no cards, no research capacity consumed) until the Founder approves validation evidence per §J; then standing behavior with named FD.
> 7. **Portfolio blindness, point-in-time (FD #58), no invented rules (FD #53), audit/history preservation: unchanged and binding.**

---

## E. EARNINGS-INFLECTION DESIGN OPTIONS

**Shared semantics (mandatory, direction §4A):** define EPS explicitly — GAAP diluted vs adjusted; handle fiscal-quarter seasonality (compare same fiscal quarter YoY), stock splits/corporate actions (restated history), restatements, discontinued ops, M&A, large tax items, buyback-driven EPS (flag, don't silently accept), low/negative base effects. Never silently substitute adjusted for reported; preserve source + transformation lineage. Industries where EPS is not the right primary measure → exclude from v1 rather than force a formula.

| Criterion | Option 1: TTM/Normalized EPS Level Breakout | Option 2: Quarterly YoY Growth Acceleration | Option 3: Two-Stage Composite (1 OR 2) |
|---|---|---|---|
| **Definition (hypothesis 1: level)** | Latest TTM diluted EPS > the maximum TTM EPS over the prior 8 quarters (~2y) | — | Level rule from Option 1 |
| **Definition (hypothesis 2: rate)** | — | Latest quarter YoY EPS growth > max YoY growth over prior 8 quarters, OR YoY growth accelerating (latest > prior-quarter YoY) | Rate rule from Option 2 |
| **Signal quality** | Catches absolute earnings-power milestones; stable | Catches the "rate of change" moment early; classic O'Neil C | Broadest net; flags the most situations |
| **False positives** | Low-medium (TTM smooths noise) | Higher (low/negative bases, tax/one-offs amplify) | Highest of the three |
| **Seasonality** | Largely handled (TTM) | Must compare same-fiscal-quarter YoY; still base-effect sensitive | Combines both weaknesses unless filters applied |
| **Data requirements** | TTM EPS series, restated, PIT-dated | Quarterly EPS + prior-year quarterly EPS, PIT-dated | Both |
| **Backtestability** | High (fewer inputs, fewer revision traps) | Medium (revision/base handling critical) | Medium |
| **Simplicity** | High | Medium | Low |
| **Design verdict** | Best default core | Strong complementary signal | Only after 1+2 validated separately (direction: validate hypotheses separately BEFORE combining) |

**Recommendation:** start with **Option 1 as the core eligibility signal** (cleanest, most PIT-robust, lowest false-positive) and **Option 2 as a separate, independently-validated enrichment signal** (advisory, not gating) — matching the direction's explicit "validate separately, decide combination later." Revenue confirmation + margin direction + cash-conversion sanity = confirmation layer (also advisory in v1). Guidance/estimate-revision data deferred (data availability + PIT complexity) unless a free PIT source is proven.

---

## F. STAGE DESIGN OPTIONS

**Deterministic components (computable, reproducible):**
- Price vs 50-day vs 150-day MA (position + slope) — rule-pack §2 tables.
- Price vs 52-week high/low range position.
- RS vs market index (e.g., SPY) — RS line, deterministic.
- Volume statistics (average volume trend, up/down-day volume ratio).
- Distance-from-base / time-since-base-breakout statistics.

**Interpretive components (require judgment — mark as such, never auto-scored):**
- Base quality (VCP character, tightness).
- Distribution vs accumulation character (Stage 3 detection).
- "Early vs late" Stage 2: extension above MA50, time since breakout, RS percentile — interpretable as evidence, NOT a hard gate.

**Option A — Strict deterministic proxy (v1):** Stage 1 = price between flattening MAs, 52w-range mid-zone, flat RS; Early Stage 2 = price above both MAs with 50>150 and both sloping up AND within early-extent window (e.g., recent base breakout) — thresholds proposed WITH evidence, Founder-approved. Stage 3/4 = MA cross-down / price below both / RS deteriorating. **Pros:** reproducible, auditable, matches rule-pack tables. **Cons:** misclassifies some bases; "early" proxy crude.

**Option B — Deterministic core + interpretive review (recommended):** scanner computes the deterministic stage signature and outputs a stage *candidate* label (S1 / early-S2 / S2 / S3 / S4 + confidence from deterministic features only); the Radar Scout / Equity Alpha eyeballs the price chart for base character before the card is filed. Stage label is advisory input to triage, never a gate on research. **Pros:** honest about what's deterministic vs interpreted (direction §F explicitly asks this split), protects capacity, radar stays "packages and recommends". **Cons:** a human-in-the-loop step (but radar role already exists).

**Option C — Full interpretive stage call by analyst (no v1):** defers all stage logic to discretionary reading. **Pros:** zero formula risk. **Cons:** not systematic — fails the direction's "systematic method" goal.

**Recommendation: Option B.**

---

## G. CHANGE-DRIVER / CATALYST-RECON CONTRACT

**Purpose:** decide whether a candidate deserves Full Research Mandate — NOT a miniature company analysis.

**Owner:** Equity Alpha Analyst (role 05) — company-economic interpretation is research, not discovery (direction §8: radar packages the signal; ownership crosses to research at recon).

**Input:** Task Idea Card (scanner evidence block + radar provenance) + CoS triage scoping note.

**Output — `Catalyst Recon` (max ~1–2 pages, internal workpaper):**
1. **What changed in the underlying economics?** (free-form; the ONE question that matters)
2. **Signal character classification:** structural / cyclical / temporary / accounting-driven / financial-engineering-driven / macro-driven / company-specific / multi-causal-not-reducible — with one-line evidence each.
3. **Evidence surface:** filings/transcripts/sources consulted (bounded — no exhaustive evidence build at this stage).
4. **Catalyst candidates** (new product/platform/customer/capacity/market/pricing/market-share/competitor/regulatory/supply/management/operating leverage/distribution/estimate revisions/industry structure/emerging theme) — only if genuinely identifiable.
5. **"No identifiable single catalyst"** — VALID outcome, recorded as such. Never manufacture a catalyst/narrative/theme to complete the workflow (direction §4C).
6. **Disposition recommendation:** Watch / Archive / RM-worthy (advisory; CoS + Founder gate the RM).

**Prohibitions:** no valuation analysis, no moat essay, no score, no "good stock" verdict, no publication (recon is an internal workpaper unless it earns standalone value — editorial judgment).

---

## H. RESEARCH-MANDATE CONTRACT (neutral Big Question)

**Format (anti-anchoring, direction §7):**

> "[TICKER] displayed an unusual earnings inflection while its price structure remained in a base or transitioned into an early advancing stage. What changed in the underlying economics, is the change durable, and does the available market evidence represent genuine recognition of improvement or merely a temporary, cyclical, accounting, or narrative effect?"

**Mandatory components of every RM born from discovery:**
- Neutral Big Question (as above) — momentum is the reason the company reached the desk, NOT the conclusion.
- Provenance block (scanner signal + radar card + recon, with PIT stamps) attached to the audit trail — **preserved, not pre-loaded** into first passes.
- Explicit statement: no discovery checklist, ranking score, CAN SLIM scorecard, or rule-pack conclusions enter the independent first pass (FD #64 item 7).
- Standard RM-#### chain thereafter (unchanged).

**Forbidden mandate phrasing:** "Explain why XYZ is a great momentum stock after its earnings breakout" (confirmation-anchored).

---

## I. BLOG IMPACT

**Prefer NO UI change (direction §11, §18.I).** Assessment:
- Reports contract `type` field currently: `company | product | weekly | quarterly | theme`. A discovery-family note ("Equity Inflection Radar — Week of YYYY-MM-DD") fits `weekly` without schema change; company research fits `company` with `subject` ticker (series behavior already exists).
- Adding a `discovery` type or "Equity Inflection" content family is a **later taxonomy design decision** (direction §11: "Exact taxonomy is a design decision to review later") — defer.
- Discovery artifacts (cards, recon, rejected candidates) remain internal workpapers unless they earn standalone editorial value. Silence is valid.
- Ticker names stay search/subject/series, never top-level navigation (already true).

---

## J. VALIDATION & SHADOW-PILOT PLAN

**Primary success metric = research-discovery quality, NOT forward returns** (direction §18J). Return analysis is secondary evidence and must not become a trading-system backtest by stealth.

**Phase 0 — Shadow run (current data, zero capacity consumption):**
- Run scanner on FO-universe 8 names first (data-proven universe), then broaden to a PIT-investable US universe.
- Output hits only; NO cards, NO recon, NO CoS load. Measure: hit count, eyeball false-positive character.

**Phase 1 — Point-in-time historical validation:**
- Use earnings-release/filing availability timestamps (not fiscal period-end) as signal date.
- Universe = point-in-time investable (survivorship-safe: include later-delisted names via CRSP-like or exchange-delisting flag; free sources limited — document limits honestly).
- Tests: look-ahead bias (signal uses only as-of data), survivorship bias (delisted/universe), revision leakage (restated fundamentals used only post-publication), corporate-action handling (splits/actions on split-adjusted vs as-of prices — documented methodology).
- **A backtest that cannot prove PIT availability is not admissible** (direction §4D).

**Phase 2 — Hypothesis separation:** validate EPS-level breakout (Option 1) and EPS-growth acceleration (Option 2) independently; only then decide combination (direction §4A).

**Phase 3 — False-positive review:** which company types/signals repeatedly look interesting but fail deeper investigation? Feed results into the recon contract (tighten or keep — evidence-based).

**Phase 4 — Missed-opportunity review:** which important inflections would the design have failed to surface? (Known blind spots: low-float microcaps, adjusted-EPS-heavy stories, non-EPS industries.)

**Phase 5 — Capacity-load measurement:** how many candidates reach CoS / Catalyst Recon per cycle vs available deep-research capacity (direction §17). Tune the funnel (direction §12 illustrative: 5,000 → 40–60 → 10–15 → 4–8 → 1–3) — illustrative only, no hard thresholds without Founder approval.

**Phase 6 — Stability/sensitivity:** does a small threshold change radically alter the candidate set? Report ±X% perturbation sets.

**Phase 7 — Data-quality failure behavior:** honest empty output (no cards when data insufficient); source-gap handling per known-gap policy (FD #82 pattern).

**Gate:** Phase 0–7 evidence presented to Founder → only then standing production behavior + named FD (threshold hardening requires explicit approval per FD #53).

---

## Final Principle (direction §20 — binding)

> The scanner surfaces what may deserve attention.
> Radar packages and recommends; CoS decides what receives research-capacity consideration.
> The research team decides what it means.
> The Founder decides what to do with the knowledge.
> STRUCTURE THE DISCOVERY. PRESERVE THE THINKING. KEEP DECISION AUTHORITY HUMAN-GATED.

<!-- 2026-08-10 12:00 UTC+7 -->
