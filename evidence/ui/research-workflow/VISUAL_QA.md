# Visual QA — Research Workflow UI (UI-1 + UI-2, FD #55)

**Task:** Research Workflow UI build — Briefing upgrade + `/research` + `/research/*` artifact detail + 7 shared components + 7-item nav (blueprint approved 5 Aug 2026, D3 Option A).
**Commits:** none yet (working tree; pending Founder acceptance + council artifact).
**Approved objective:** `design/research-workflow-ui/PAGE_BLUEPRINTS.md` v0.1 (3 pages) + FIT-GAP-v0.1.md (D1 adapter, FD #55).
**Design system:** MASTER.md v3.0 (Research Desk direction, FD #51) + UI_TOKENS.md.

## Pages / states reviewed

| Page | Route | States | Viewport |
|---|---|---|---|
| Briefing | `/` | populated (AM hero + 4 new sections), loading, org-error fallback | 1440 (browser) |
| Research Desk | `/research` | 5 views, filters, empty view (Archive), held/blocked filter | 1440 |
| Artifact Detail | `/research/ciw-pilot-msft/research-result.md` | 7 sections, 404, org-pilot (synthetic) + CIW (real) | 1440 |
| 390×844 mobile | all three | code-level responsive audit (browser tool locks 1258px — **EXTERNAL_NOT_TESTED**, per iip-ui-design) | — |

## Functional verification (browser)

- Login → 7-item nav renders (Briefing, Research Desk, AM, CS, FO, II, Weak Signals).
- Briefing: Decisions Required (1 real item ORG-2026-0004, links to packet), Material Changes (2 research results, cleaned version/status), Holds & Exceptions (0 active / 2 cleared, collapsed banners), Research Throughput (8-row ledger — honest counts per card YAML, not board.md display table).
- Research Desk: view counts derive from card `workflow_column` (Inbox 1 · Active 2 · Review 1 · Founder 1 · Archive 0 — matches card YAML, single source per KANBAN-CONTRACT §3); domain/sort filters + held/blocked toggle; rows link to artifact detail when `expected_artifact` resolves in the registry ("no artifact yet" otherwise, no dead links).
- Artifact Detail: REAL provenance chip on CIW files / SYNTHETIC on org-pilot; identity parsed from the artifact's own Identity-and-State table (CRR-2026-0001); Evidence tab extracts 11 SRC refs + links source-map; Independent Challenge lists challenge-review; Decision History timeline (modified → status → founder record); Validation/Data Quality honest empties; related-artifact family grouped by root+slice (familyOf fix — no cross-root flooding).
- Console: 0 errors / 0 warnings on all routes. `npm run build` exit 0, lint 0 errors (7 pre-existing warnings).

## First-pass findings + corrections (refinement pass ≥1)

1. **MaterialChangePanel raw markdown** (`**PROPOSED V1**…`) → `clean()` strips `**`/backticks + truncates (60/80 chars). Verified in browser.
2. **ResearchArtifactRow redundant status line** (data/validation/risk repeated above the ReviewGatePanel grid) → removed; meta line now single (changed · next · artifact link state). Verified in browser.
3. **Artifact Detail identity table 2-col misalignment** (long `research_status` value wrapped, rows drifted) → single-column label-left/value-right rows. Verified in browser (vision re-check: aligned).
4. **familyOf cross-root flooding** (org-pilot artifact showed 13 unrelated CIW artifacts) → group by root (`ciw-pilot-msft`/`org-pilot`) then slice. Verified in browser (MSFT result family = 5 first-slice files).
5. Related-artifact list: explicit "· type · modified" separator.

## Border / containment audit

- Full-perimeter content outlines per viewport: **0** (all new surfaces are open regions + hairline `border-rule` separators + tonal `bg-bg-panel` for hold/empty states — no `border`, no `ring`, no `bg-card` in new code).
- Approved functional exceptions (excluded by policy): provenance chips, input selects, focus rings, tab active states.
- No new Card primitives added; no KPI-card grids; no progress bars (ReviewGatePanel = text rows); no composite scores; no invented fields (throughput counts and readiness are display derivations of admitted card fields).

## Data-honesty notes

- Research Desk counts reflect **card YAML `workflow_column`** (operational record). `kanban/board.md`'s display table says "Closed (pilot complete)" for 4 cards while their YAML still shows In Research/Triage/Cross-Review — **board.md ↔ card YAML drift found** (org-pack kanban data note; UI follows the contract's card source; board upkeep is CoS/IC Secretary's write domain, not this task).
- Material Changes shows registry `research_version/research_status` as recorded in the artifact files (files still carry "proposed/Founder Review" headers; the governance transition to Published is documented in `founder-review-record*.md` — surfaced in Decision History).

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` (01-briefing, 02-research-desk, 03-artifact-detail) · `FUNCTION_TEST_VERIFIED` (console 0 errors, all sections exercised) · `ACCESSIBILITY_STATIC_CHECK` (focus-visible on links, aria-selected tabs, aria-label patterns, color+text statuses) · mobile 390 `EXTERNAL_NOT_TESTED` (browser tool lock; code-level responsive audit done) · backend suite 309/309 unchanged (no backend change in UI-1/2).

## Screenshot inventory

```
evidence/ui/research-workflow/
  01-briefing-desktop.png      — Briefing with 4 new sections
  02-research-desk-desktop.png — Research Desk Inbox view + filters + row
  03-artifact-detail-desktop.png — MSFT research-result Executive Summary + related
```

## Remaining deviations

- Artifact "Research" section renders markdown as raw mono `<pre>` (no markdown renderer installed; zero-dep rule — matches the research-note character; full renderer needs a dependency decision).
- Audit Trail tab deferred to UI-4 (needs git-history endpoint — out of D1 scope).
- Mobile 390 viewport not browser-tested (tool lock) — code-level audit only.

## Council Round 1 → RETEST (2026-08-05) — 7 findings, all remediated + re-verified

| # | Finding | Fix | Verified |
|---|---|---|---|
| 1 | Briefing sections lacked provenance labels | SectionStamp on all 4 sections (org_workflow_kanban / research_artifact_registry / org_workflow_holds + latest card update) | browser (01-briefing) |
| 2 | Research Desk used client wall-clock as-of | replaced with admitted `latest card update` = max(card.last_updated) | browser (02) |
| 3 | ORG-2026-0005 "no artifact yet" (annotated expected_artifact "(pass/fail)" broke match) | MD_PATH normalization in linkArtifact | browser: row now "OPEN →" links org-pilot/PILOT-REPORT.md |
| 4 | Material Changes unpaired + false-empty on registry failure | paired base+delta (v1 base, later slices "→ supplements … append-first") + scoped registry-error state (artifactsError, never coerced to []) | browser (01: CRR-2026-0001 base, CRR-2026-0002 delta) |
| 5 | Decision History hid the Founder transition | DecisionTimeline parses founder-record transition table (KEY_MAP prior/next/actor/timestamp — fixed key-mapping bug found during re-verify) | browser (04: "Founder Review … → Published / Current Authoritative v1" linked) |
| 6 | Validation/Data Quality generic empty on linkable artifacts | org-queue join via normalized expected_artifact; ReviewGatePanel + data_status surfaced | browser (IC-DECISION-PACK Validation shows card status) |
| 7 | 404 conflated with API failure | getJSON attaches HTTP status; detail page branches 404 vs scoped error+retry; registry-down states on all family sections | code-level + status404 branch |

Regression found during re-verify (my own): MaterialChangePanel sort put "-2.md" before ".md" lexicographically → v2 shown as base; fixed with slice-first comparator. Verified in browser.

## Council Round 2 → RETEST (2026-08-05) — 2 findings, all remediated + re-verified

| # | Finding | Fix | Verified |
|---|---|---|---|
| 1 | Briefing stamps lacked as-of on 3 of 4 sections | every stamp now carries an admitted as-of: Decisions/Throughput = latest card update (max last_updated), Material Changes = latest registry modified, Holds = **as-of unavailable** (hold YAML has no timestamp field — honest, per council's allowed wording) | browser console: all 4 stamps read back with as-of; screenshot 01 |
| 2 | /org-queue + founder-record failures silently degraded (false-empty / title-only) | queueDown scoped error + Retry in Validation/Data Quality; recordsQ tracks failed ids → Decision History renders scoped warning + Retry when transition content fetch fails | code-level (branches in ResearchArtifactDetailPage.tsx; build exit 0) |

## Verdict

**PASS (implementer claim) after council round-2 RETEST** — both findings remediated; browser re-verified; console 0 errors; build exit 0; backend 309/309. Independent review round 3 (final focused retest, HEAD-bound) via llm-council pending (Sol Medium).

<!-- 2026-08-05 16:55 UTC+7 -->
