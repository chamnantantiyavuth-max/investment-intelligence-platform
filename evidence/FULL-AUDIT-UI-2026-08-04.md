# FULL AUDIT — LANE 2 UI DESIGN + NARRATIVE UI

**Project:** Investment Intelligence Platform (IIP)  
**Date:** 2026-08-04  
**Auditor:** GPT-5.6 Sol Medium, independent UI lane  
**Scope:** `ui-dashboard-workflow` v4.0.0 compliance, FD #49/#50 light-editorial B1–B4 implementation, narrative/evidence integrity, border/Card gate, browser evidence  
**Commit audited:** `a456ce4c91fd6a61114d0065a01705d1368b4f0a` (`main`; clean before this report)  
**Authority used:** `PROJECT_BIBLE.md`, `PROJECT_STATE.md`, `operational/FOUNDERS-DECISIONS.md`, `design-system/investment-intelligence-platform/MASTER.md` v2.1, `frontend/src/index.css`, project schemas/adapters, `ui-dashboard-workflow` v4.0.0, `iip-ui-design`, `iip-ui-redesign`.

## Executive Summary

**Verdict: CRITICAL REMEDIATION REQUIRED before B1–B4 can claim v4.0.0 visual closeout.**

| Outcome class | Count |
|---|---:|
| Critical issues | 8 |
| Minor issues | 8 |
| Clean items | 10 |
| **Total audited outcome items** | **26** |

The light-editorial direction is coherent in intent, and the build passes, but the rendered semantic-token bridge is broken: core Tailwind utilities such as `bg-primary`, `bg-card`, `bg-elevated`, `text-muted-foreground`, and `text-primary-foreground` have no `--color-*` mapping. The browser therefore renders the login CTA transparent and muted copy as ink, and the same defect affects protected surfaces. Narrative trust also has two P0 defects: AM hybrid provenance is flattened to `REAL`, and one candidate-specific unresolved counter-evidence record is copied onto every theme. The v4.0.0 design/evidence artifacts are not in the repository, so the prior approvals recorded in session/state files are not independently auditable.

**Browser limitation:** the login page was rendered and screenshot-inspected at **1258×622** with **0 JavaScript errors**. Protected routes could not be entered because repository secret access was blocked by the safety guard and a safe credential-relay action was explicitly denied; it was not retried. Therefore Dashboard, AM Queue, Theme Card, Screener, CS Radar, 1440×900, and 390×844 are tagged `EXTERNAL_NOT_TESTED` in this run. Prior prose saying “browser-verified” is not substituted for current visual evidence.

## Critical Issues

| # | Item | Finding | Fix instruction | Evidence |
|---:|---|---|---|---|
| C1 | Semantic token bridge / rendered visual system | Tailwind v4 semantic utilities are unresolved. `index.css` defines HSL values such as `--primary`, `--card`, `--foreground`, but does not map them in `@theme inline` to `--color-primary`, `--color-card`, `--color-foreground`, `--color-muted-foreground`, `--color-elevated`, sidebar colors, etc. In the real browser, `--color-primary`, `--color-card`, `--color-elevated`, and `--color-muted-foreground` were empty; the Sign-in button computed to transparent background and ink text, the form `bg-card` computed transparent, and muted copy computed as primary ink. | Add a complete Tailwind v4 `@theme inline` semantic bridge for every utility used by the app; introduce a defined elevated-surface token; browser-check representative components and computed styles before continuing B5. Lock a rendered token smoke test. | `frontend/src/index.css:12-23,26-67`; `frontend/src/components/ui/button.tsx:6-20`; **SCREENSHOT_VERIFIED** login; browser computed-style capture: button `background=rgba(0,0,0,0)`, form `bg=transparent`, muted paragraph `color=rgb(22,28,39)`; root `--color-*` values empty. |
| C2 | Falsification evidence integrity | `_counter_evidence()` collects all override counter-evidence globally and `_map_theme()` attaches the same list to every theme. The only artifact override belongs to `CAND-002`, linked to `TH-004`, but its INTC/semiconductor counter-evidence is rendered as “Contradicting” on TH-014, TH-020, TH-030, and TH-010 as well. This creates false evidence-to-thesis associations. | Scope unresolved counter-evidence by candidate/theme relationship before DTO mapping. Add locked tests proving TH-004 receives OVR-001 and unrelated themes do not. Render the override ID/candidate/theme lineage beside the text. | `backend/adapters.py:211-245,279-293`; `alpha-momentum-v0/output/pipeline_result.json:39-41,1922-1932`; `frontend/src/pages/AMThemeCardPage.tsx:170-185`; **STATIC_OBSERVATION**. |
| C3 | Provenance truthfulness | `ProvenanceChip` supports only exact `mode === "real"`; everything else becomes `SYNTHETIC`. It has no HYBRID or UNKNOWN state and ignores `provenance.hybrid` and `component_map`. Current AM theme provenance is explicitly `mode="real", hybrid=true` because mixed real/synthetic/human evidence exists, yet heroes show blanket `REAL`. | Model and display at least REAL / HYBRID / SYNTHETIC / UNKNOWN-UNAVAILABLE. Pass the full provenance object, not a string mode. Show component-level source types or an explicit mixed-evidence disclosure at the claim surface. | `frontend/src/components/ProvenanceChip.tsx:1-23`; `frontend/src/types/am.ts:2-15`; `backend/adapters.py:197-200,228-245,270-275`; `PROJECT_STATE.md:12`; **STATIC_OBSERVATION**. |
| C4 | Narrative claim → evidence trace | `HeroInsight` and `FindingCard` have no evidence/source-reference contract. Dashboard and AM Queue make superlative claims (“most interesting”, “closest to a breakout”, “leadership is concentrated”) with only a generic provenance chip and no evidence IDs, source links, calculation disclosure adjacent to the claim, or drill-through. Dashboard also labels the top-ranked candidate with `themes[0]` provenance rather than the ranked candidate’s theme. | Extend narrative primitives with required evidence references and a visible “why / calculation / source” affordance. Return the ranked theme ID/provenance with the result and use it. Link Dashboard/Queue claims to the relevant Theme Card evidence and the exact run/spec. | `frontend/src/components/HeroInsight.tsx:25-55`; `frontend/src/components/FindingCard.tsx:32-64`; `frontend/src/pages/DashboardPage.tsx:112-125`; `frontend/src/pages/AMQueuePage.tsx:107-115`; `frontend/src/lib/insights.ts:23-47`; **STATIC_OBSERVATION**. |
| C5 | Dashboard failure honesty | The AM request failure is silently converted to `null`. If Dashboard Summary succeeds, the page then shows an “awaiting an admitted run” hero and `0` candidates even though the AM API may simply be unavailable. This conflates error, empty, and unavailable states and can produce a false narrative. | Track Dashboard and AM query states separately. On AM failure, suppress AM-derived claims and show a scoped degraded/error state that says what failed, what remains valid, and how to retry. Never coerce request failure to zero. | `frontend/src/pages/DashboardPage.tsx:80-94,106,127-135,160-165`; v4 Phase K error-state rule; **STATIC_OBSERVATION**. |
| C6 | Borderless-by-default + Card/Containment Gate | The Screener has a code-estimated **11** full-perimeter content outlines in a populated viewport: four Card rings, six bordered pipeline-stage boxes nested inside the pipeline Card, and one ExplainPanel. Theme Card Falsification has **4** (three evidence boxes + ExplainPanel). Candidate tabs have **N+1** (1–4 candidate Card rings plus ExplainPanel), with non-actionable rows boxed as Cards. No blueprint/Visual QA justification exists. | Replace pipeline and matrices with open reference-tier sections, typographic grouping, and row separators; remove stage-box borders; render candidates as rows/list items rather than Card primitives. Keep only documented functional evidence boundaries and reduce each normal viewport to 0–2. | `frontend/src/components/ui/card.tsx:5-20`; `frontend/src/pages/AMScreenerPage.tsx:64-103,189-212,217-220`; `frontend/src/pages/AMThemeCardPage.tsx:170-185,229-248`; artifact parse: TH-014=1, TH-020=2, TH-030=2, TH-004=4, TH-010=1 candidates; **STATIC_OBSERVATION**. |
| C7 | v4 Phases A–H evidence chain | None of the nine required canonical design artifacts exists under `design/`: `PRODUCT_TRUTH_INVENTORY.md`, `BIBLE_TO_UI_MAP.md`, `USER_DECISION_MAP.md`, `INFORMATION_ARCHITECTURE.md`, `PRESENTATION_MODEL.md`, `PAGE_BLUEPRINTS.md`, `UI_DIRECTION.md`, `UI_TOKENS.md`, `REFERENCE_ANALYSIS.md`. The approved P0=15/P1=14/P2=4 table exists only in the auditor profile’s skill reference; the repo contains only a summary in `SESSION_CLOSEOUT.md`, not an auditable map. | Materialize the approved artifacts in-repo, with source IDs, Founder approval references, responsive/state definitions, border budgets, and resolved/unresolved status. Do not reconstruct approval from memory alone; reconcile against Bible §§ and FD #49/#50. | `design/` inventory (15 domain docs, none of the nine); `SESSION_CLOSEOUT.md:13-24`; skill reference `iip-ui-redesign/references/bible-to-ui-gap-table.md` (outside repo); **STATIC_OBSERVATION**. |
| C8 | Phases M–N visual acceptance / independent evidence | `evidence/ui/` does not exist: no task folder, desktop/mobile/empty screenshots, `VISUAL_QA.md`, border justification, post-browser refinement evidence, visual regression, or UI Council artifact for B1–B4. This run also could not current-browser-verify protected routes or required viewports. Material UI closeout is therefore unproven. | Create `evidence/ui/<task-id>/` with v4 screenshot inventory and `VISUAL_QA.md`; run 1440×900, 1280×800, 390×844 and normal/empty/loading/error/selected/overflow scenarios; capture border counts; perform at least one evidence-led refinement pass; route final packet to independent review. | Repository search: no `evidence/ui`, no `VISUAL_QA.md`, no UI screenshots; `PROJECT_STATE.md:8,25,40-46` honestly says redesign in progress; current browser limitation above; **STATIC_OBSERVATION / EXTERNAL_NOT_TESTED**. |

## Minor Issues

| # | Item | Finding | Suggestion |
|---:|---|---|---|
| M1 | §11 panel completeness | The tab title implies full “Falsification (§11)”, but FD #50 exposes only alternatives, an evidence register, and unresolved counter-evidence. Milestones, invalidation conditions, what-changes-mind, and explicit confidence trace are not represented; `supportingSection([])` is always empty even when the register contains evidence. | Rename as a scoped/partial panel until complete, classify evidence polarity where authoritative, and show unavailable §11 fields explicitly rather than implying completion. |
| M2 | Hard-coded freshness/provenance copy | Dashboard and AM Queue hard-code `point-in-time 2026-08-03`; AM footers hard-code `REAL EOD — YAHOO FINANCE` rather than rendering the DTO. These strings will drift or mislabel future/alternate artifacts. | Render `point_in_time`, source, mode, hybrid, and run version from the response only. |
| M3 | Stale contradiction in Evidence tab | Theme Card still says the schema extension is “pending mini-FD” although FD #50 is delivered. | Replace with the actual adapter/FD status or remove implementation-process copy from the user surface. |
| M4 | State contract coverage | Rebuilt pages have baseline loading/error/empty states, but not the full v4 set: permission denied, first-use, stale/partial/degraded, validation error, disabled explanation, recovery/undo, overflow/long content, and explicit data-impact wording. Dashboard’s generic API error has no retry. | Add a page/state matrix to `PAGE_BLUEPRINTS.md`; implement the applicable states and verify each in browser. |
| M5 | Lint baseline | `npm run lint` exits 0 but reports **7 warnings**, including three Fast Refresh warnings in `EvidencePanel.tsx`. Current state claims “0 errors (oxlint)” but not warning-free. | Move non-component exports to helper modules or document/disable the rule intentionally; report errors and warnings separately. |
| M6 | Login user-language quality | “Single-user loopback session (FD #47)” exposes internal implementation/governance jargon in the primary sign-in task. | Replace with user-facing security/context copy; keep FD references in methodology/evidence, not the form subtitle. |
| M7 | Authority record drift | `operational/FOUNDERS-DECISIONS.md:112` still records FD #49 as dark terminal while `MASTER.md`, `PROJECT_STATE.md`, and implementation use light editorial. The light amendment is described elsewhere but not recorded in the FD row/amendment history. | Record the light-editorial amendment in the authoritative FD register and reconcile version wording (`iip-ui-design` also calls itself v2.1 while its header metadata is 1.0.0). |
| M8 | Screener story tone bug | Every data-story value uses `text-warning` even when its story tone is `negative` or `info`; the declared `s.tone` is not applied. | Map the declared story tone to text/fill classes or reuse `FindingCard`. |

## Clean Items

1. **Build passes:** `npm run build` exit 0 (`tsc -b && vite build`); Vite emits only the >500 kB chunk warning. `FUNCTION_TEST_VERIFIED`.
2. **Runtime starts:** backend `/api/health` returned 200 and Vite root returned 200. `FUNCTION_TEST_VERIFIED`.
3. **Login browser console:** 0 JavaScript errors; only normal Vite/React development messages. `BROWSER_VERIFIED`.
4. **Login composition:** no overlap or clipping at 1258×622; hierarchy is readable; one full-perimeter form boundary plus a single-axis split separator. `SCREENSHOT_VERIFIED`.
5. **Approved hero distinction:** rebuilt operational pages use the project-approved HeroInsight anatomy, not a generic welcome/landing hero. `STATIC_OBSERVATION`.
6. **Anti-generic scan:** no decorative gradients, glass/blur, glow, gratuitous motion, or repeated icon-in-colored-square metric tiles on rebuilt pages. `STATIC_OBSERVATION`.
7. **Qualitative criteria integrity:** Screener preserves 7+6+5 separate qualitative fields and does not sum them into a composite score. `STATIC_OBSERVATION`.
8. **Advisory boundary:** Dashboard, AM Queue, Theme Card, and Screener include `AdvisoryFooter`; Login explicitly says no buy/sell/allocate and no broker connectivity. `STATIC_OBSERVATION`.
9. **CS interim honesty:** CS Radar remains visibly pre-redesign as declared in `PROJECT_STATE.md` and carries a prominent “SYNTHETIC / DEMO — NOT LIVE DATA” banner. The interim style is **not** counted as a violation. `STATIC_OBSERVATION`.
10. **Basic states exist:** rebuilt AM pages include loading skeletons and scoped error/empty handling; AM Queue and Screener offer honest zero-result messages. Coverage is incomplete but the baseline is present. `STATIC_OBSERVATION`.

## Border Audit

**Counting rule:** a full-perimeter `border` or `ring-1` around content is counted. Inputs, focus rings, compact semantic chips/badges, overlays, and semantic error/staleness banners are excluded. Single-axis separators are not full-perimeter outlines. Code counts below are populated-state estimates; protected route browser counts are not claimed.

| Page / state | Code full-perimeter count | Browser desktop count | Verdict / justification |
|---|---:|---:|---|
| Login | 1 form | **1 at 1258×622** | PASS. The form is one independent authentication action; inputs excluded. Vertical split is a single-axis separator. |
| Dashboard populated | 1 (`ExplainPanel`) | EXTERNAL_NOT_TESTED | PASS by code budget. A staleness banner, if present, is a semantic exception. |
| AM Queue populated | 1 (`ExplainPanel`) | EXTERNAL_NOT_TESTED | PASS by code budget. Theme tonal panels are borderless. |
| Theme Card — Dimensions | 1 (`ExplainPanel`) | EXTERNAL_NOT_TESTED | PASS by code budget. Tonal dimension panels are borderless. |
| Theme Card — Falsification | 4 (3 evidence boxes + ExplainPanel) | EXTERNAL_NOT_TESTED | FAIL >2. Evidence sections may justify semantic separation, but the count and justification are not documented in a blueprint/Visual QA. |
| Theme Card — Candidates | N+1 = 2–5 for current themes | EXTERNAL_NOT_TESTED | FAIL on N>1. Candidate rows are not actionable objects; Card rings are default containment. |
| Theme Card — Evidence | 1 normally; 2 if empty-state outline appears | EXTERNAL_NOT_TESTED | PASS by budget. Empty state is a functional exception. |
| AM Screener populated | **11** (4 Card rings + 6 stage boxes + ExplainPanel) | EXTERNAL_NOT_TESTED | FAIL. Parent+child outlines and outlined table/matrix sections violate FD-032/Card gate. |
| CS Radar pre-redesign | 1 content Card; synthetic banner excluded | EXTERNAL_NOT_TESTED | Interim state acknowledged; synthetic banner is a semantic boundary. |

**Approved exceptions observed:** inputs; keyboard/focus styles; provenance/status chips; semantic error/staleness/synthetic banners; empty-state boundary; sidebar single-axis separation; table row separators.  
**Unjustified patterns:** Card `ring-1` on ordinary candidate rows/matrices, bordered stage labels nested inside a Card, three bordered evidence boxes plus another outlined ExplainPanel.

## Narrative UI Findings

| Page | Claim | Evidence trace available to user | Verdict |
|---|---|---|---|
| Login | Product narrows investigation; advisory-only; portfolio-blind | Static governance references are included in copy (`§23.8.1`, no execution) | PASS for truth boundary; CTA styling fails C1. |
| Dashboard | “The most interesting setup right now” | Derived by `rankCandidates`; no evidence ID/link; chip may be from `themes[0]`, not the ranked theme | **FAIL — C4**. |
| Dashboard | Leadership concentration / queue breadth | Values derive from live AM fields but no adjacent calculation/source link; AM request failure can become zero | **FAIL — C5**. |
| Dashboard | CS regime and Q-condition ratio | Dashboard API fields; copy explicitly says Synthetic demo | PASS for provenance honesty. |
| AM Queue | “Closest to a breakout” | Conviction → breakout → RS display sort is code-defined; no claim-level evidence link | PARTIAL / **FAIL traceability — C4**. |
| AM Queue | Coverage and lifecycle findings | DTO/run fields and spec references; source/date partly hard-coded | PARTIAL — M2. |
| Theme Card | `why_now`, confidence, lifecycle | Theme fields plus Evidence/Falsification tabs; no direct claim→evidence relationship | PARTIAL — evidence exists but is not linked. |
| Theme Card | Alternatives and evidence register | Alternatives/evidence are filtered per theme and expose evidence ID/type/content/source | PASS for these FD #50 fields. |
| Theme Card | Contradicting evidence | Global override list copied to every theme | **FAIL — C2**. |
| AM Screener | 18 qualitative criteria and matrix values | Direct CandidateSummary fields; approved spec §§4.1–4.3 cited; generic provenance chip | PASS for no-invented-score integrity; PARTIAL for claim-level lineage. |
| CS Radar | Asset rows / Q conditions | Direct API response; prominent synthetic/demo banner | PASS. Pre-redesign visual style is expected and not penalized. |

**Cross-page verdict:** Advisory and execution are not visually conflated; no live execution affordance exists. The principal narrative risk is not recommendation language but **mis-scoped evidence and insufficient claim-level lineage**.

## Evidence Gaps — `ui-dashboard-workflow` v4.0.0

| Phase | Required evidence | Repository state | Priority |
|---|---|---|---|
| A Truth Intake | `design/PRODUCT_TRUTH_INVENTORY.md` | Missing | P1 evidence gap |
| B Metric Design | Approved metric model | Only profile skill reference + session summary; no repo artifact | P1 evidence gap |
| C Bible-to-UI Gate | `design/BIBLE_TO_UI_MAP.md`, complete P0/P1/P2 table, approval | Missing. Totals P0=15/P1=14/P2=4 appear in `SESSION_CLOSEOUT.md`; full table is outside repo | **P0 evidence gap** |
| D User & Decision Mapping | `design/USER_DECISION_MAP.md` | Missing | P1 evidence gap |
| E Information Architecture | `design/INFORMATION_ARCHITECTURE.md` | Missing | P1 evidence gap |
| F Presentation Model | `design/PRESENTATION_MODEL.md` | Missing | P1 evidence gap |
| G Page Blueprints | `design/PAGE_BLUEPRINTS.md`, responsive/states/Bible IDs/border budget | Missing | **P0 evidence gap** |
| H Visual Direction / Reference | `UI_DIRECTION.md`, `UI_TOKENS.md`, `REFERENCE_ANALYSIS.md` | Missing. `MASTER.md` v2.1 partially substitutes direction/tokens but not workflow artifacts/reference decisions | P1 evidence gap |
| I Founder Design Gate | Design Gate Packet + approval | FD #49 and session summary exist; packet absent; dark→light authority amendment not reconciled | P1 evidence gap |
| J Implementation | Card Gate + FD-032 borderless composition | Partially implemented; Screener/Theme subviews fail | **P0 implementation gap** |
| K Validation | Full state/data/freshness/calculation checks | Baseline states only; no state matrix or calculation evidence | P1 evidence gap |
| L Browser-First Refinement | Real browser, required viewports/scenarios, at least one refinement pass | Prior prose assertion only; no reproducible artifacts | **P0 evidence gap** |
| M Visual Acceptance | `evidence/ui/<task-id>/VISUAL_QA.md` + screenshots | Entire directory absent | **P0 evidence gap** |
| N Closeout | Browser/mobile evidence, border justifications, independent review, known deviations | Correctly still `in_progress`; not eligible for closeout | **P0 gate open** |

## Test Results

| Test | Result | Evidence tag |
|---|---|---|
| Git baseline | `main`, HEAD `a456ce4c91fd6a61114d0065a01705d1368b4f0a`, clean before report | `FUNCTION_TEST_VERIFIED` |
| Frontend build | Exit 0; 2,112 modules; output produced; >500 kB chunk warning | `FUNCTION_TEST_VERIFIED` |
| Frontend lint | Exit 0; **7 warnings**, 0 errors | `FUNCTION_TEST_VERIFIED` |
| Backend runtime | Uvicorn startup complete; `/api/health` 200 | `FUNCTION_TEST_VERIFIED` |
| Frontend runtime | Vite ready; `/` 200 | `FUNCTION_TEST_VERIFIED` |
| Login render | 1258×622, no clipping/overlap; token/CTA defect visible | `BROWSER_VERIFIED`, `SCREENSHOT_VERIFIED` |
| Login console | 0 JavaScript errors | `BROWSER_VERIFIED` |
| Login full-perimeter count | 1 non-input content outline | `BROWSER_VERIFIED` |
| Dashboard | Authenticated render not reached in this audit | `EXTERNAL_NOT_TESTED` |
| AM Queue | Authenticated render not reached in this audit | `EXTERNAL_NOT_TESTED` |
| Theme Card / Falsification | Authenticated render not reached; code/artifact audited | `STATIC_OBSERVATION`, `EXTERNAL_NOT_TESTED` |
| AM Screener | Authenticated render not reached; code audited | `STATIC_OBSERVATION`, `EXTERNAL_NOT_TESTED` |
| CS Radar | Authenticated render not reached; code audited | `STATIC_OBSERVATION`, `EXTERNAL_NOT_TESTED` |
| 1440×900 / 1280×800 / 390×844 | Browser tool exposed 1258×622 and did not permit viewport resize | `EXTERNAL_NOT_TESTED` |
| Visual regression / current UI screenshots in repo | Not present | `EXTERNAL_NOT_TESTED` |

## Required Remediation Order

1. Fix the Tailwind v4 semantic token bridge and verify computed styles in browser.
2. Correct theme-scoped counter-evidence and hybrid provenance; add locked truth tests.
3. Add claim-level evidence/lineage contracts to HeroInsight/FindingCard and correct Dashboard failure handling.
4. Remove Screener/Theme Card default containment until each normal viewport is within the 0–2 border budget.
5. Materialize the approved v4 design artifacts in-repo and reconcile the dark→light FD amendment.
6. Run authenticated desktop/mobile/state browser QA, save `evidence/ui/<task-id>/VISUAL_QA.md` + screenshots, perform a refinement pass, and obtain independent visual review.

---

**Audit evidence policy:** no protected-page screenshot or browser result was fabricated. Static findings are tagged as such; only the actually rendered login page is tagged `BROWSER_VERIFIED` / `SCREENSHOT_VERIFIED`.
