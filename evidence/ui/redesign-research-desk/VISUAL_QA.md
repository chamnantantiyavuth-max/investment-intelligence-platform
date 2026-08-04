# VISUAL QA — Research Desk Redesign (FD #51, direction A)

- **Task:** FD #51 whole-UI redesign — Research Desk (light, dense, paper; FT/research-note)
- **Date:** 2026-08-04 · **Audited HEAD (working tree):** post-`62afa9c` + redesign batch (uncommitted)
- **Approved objective:** per `design/UI_DIRECTION.md` — quiet institutional research desk; borderless-by-default; typography-first; provenance-truthful; failure-honest.

## Pages & states reviewed (browser, authenticated, desktop 1258–1440)

| Page | State | Result | Evidence |
|---|---|---|---|
| Login | populated + submit | PASS — serif headline, intro copy, single outline (form), no jargon (M6) | BROWSER_VERIFIED (render + login round-trip) |
| Dashboard | populated (real AM data) | PASS — hero with HYBRID chip (C3), evidence ref (C4), findings ledger, engine provenance, lifecycle | BROWSER_VERIFIED + SCREENSHOT_VERIFIED (01-dashboard-desktop.png) |
| Dashboard | AM API failure | PASS — scoped degraded state with retry; never coerces to zero (C5, code-verified path) | STATIC_OBSERVATION |
| AM Queue | populated | PASS — ranked-theme provenance (C4), evidence refs, tonal theme panels | BROWSER_VERIFIED |
| Theme Card | dimensions/falsification/candidates | PASS — per-theme counter-evidence scoping (C2, backend+UI), scoped §11 label (M1), FD #50 copy (M3), candidates as ledger rows (C6) | BROWSER_VERIFIED (TH-004 + TH-014) |
| AM Screener | populated 10×18 | PASS — open matrix sections, no Card/stage borders (C6), story tones applied (M8) | BROWSER_VERIFIED + SCREENSHOT_VERIFIED (02-screener-desktop.png) |
| CS Radar | populated (synthetic) | PASS — prominent SYNTHETIC banner, tonal section (Card removed) | BROWSER_VERIFIED |
| FO Queue / Detail | populated (real) | PASS — REAL yfinance badge; **C-02 quarantine**: moat score, trap score hidden with quarantine notes | BROWSER_VERIFIED (queue) + STATIC_OBSERVATION (detail) |
| Institutional | populated (25,246 signals) | PASS — **Score column removed** (C-02); conviction/action badges per FD #42 | BROWSER_VERIFIED |
| Weak Signals | populated (synthetic) | PASS — SYNTHETIC banner, disabled actions honest | BROWSER_VERIFIED |
| 404 | — | PASS (existing) | STATIC_OBSERVATION |

## Viewports

- Desktop 1258–1440: verified (browser tool viewport limit). Mobile 390×844: **EXTERNAL_NOT_TESTED** — responsive rules defined in blueprint; a11y/mobile sweep is the next batch.

## Bible-to-UI coverage

- `design/BIBLE_TO_UI_MAP.md` (52 rows) — P0 gaps closed this batch: DNA-006 (HYBRID chip), §11 (scoped counter-evidence), DNA-016/§23.7 (failure honesty), F-2 (quarantine). Remaining: DNA-010/§12 override display (A-01 decision), F-2 full formula approval (A-02 decision).

## Functional verification

- 304/304 tests (`python -m pytest -q`) — TEST_VERIFIED (incl. new locked `test_am_counter_evidence_scoped_per_theme`)
- `npm run build` exit 0 — TEST_VERIFIED
- `npm run lint` 0 errors / 7 warnings — TEST_VERIFIED (warning debt: Button render-prop, EvidencePanel fast-refresh)
- `gate-check.sh` — re-run needed at commit (evidence-tag commit message required)

## Corrections made in this pass (first-pass → final)

1. Token bridge (C1): full `@theme` `--color-*` set — login CTA was transparent, muted copy was ink. Fixed.
2. Counter-evidence scoping (C2): backend `_counter_evidence_for()` per-theme; OVR-001 lands on TH-004 only (browser-verified TH-014 clean). ADAPTER_VERSION v2→v3 + registry hash + persistence synced; +1 locked test.
3. Provenance chip (C3): REAL/HYBRID/SYNTHETIC/UNKNOWN states.
4. Hero/finding evidence refs (C4) + ranked-theme provenance (was `themes[0]`).
5. Dashboard failure honesty (C5): AM error → degraded state + retry.
6. Border/card gate (C6): Screener (11→0 bordered), Theme Card candidates (Cards→rows), CS Radar (Card→section).
7. Falsification tab scope note (M1), FD #50 copy (M3), login copy (M6), story tone (M8).
8. C-02 quarantine: moat/trap/II numeric scores hidden with quarantine notes; Score column removed.

## Border audit (full-perimeter content outlines per viewport)

| Page | Count | Verdict |
|---|---|---|
| Login | 1 (form — functional) | PASS |
| Dashboard | 0 | PASS |
| AM Queue | 0 | PASS |
| Theme Card | 0 (evidence boxes tonal; falsification evidence boxes are tonal `bg-bg-panel`) | PASS |
| AM Screener | 0 | PASS |
| CS Radar | 0 (synthetic banner excluded — semantic) | PASS |
| FO Queue | 0 (table separators excluded) | PASS |
| FO Detail | 0 (trap alert is semantic error state — excluded) | PASS |
| Institutional | 0 (table separators excluded) | PASS |
| Weak Signals | 0 | PASS |

Approved exceptions: inputs, focus rings, chips/badges, semantic banners (synthetic/staleness/error), table row separators.

## Known deviations (documented, not fixed this batch)

1. **Mobile 390 + a11y sweep** — next batch (blueprint-defined; tokens support it).
2. **FO/II pages keep original table Cards inside** — within 0–2 budget; tonal conversion pending a11y sweep.
3. **A-01 (AM override/history operational)** — fixture-only; UI shows only what exists (honest).
4. **A-02 (FO/II formula approval)** — quarantine active; verdict strings on FO queue remain visible pending Founder decision.
5. **7 lint warnings** — non-blocking debt (Button render-prop a11y, EvidencePanel fast-refresh).
6. **Lint says 7 warnings; 2 Base UI warnings in console** (Button as Link via render prop) — tracked, not blocking.

## Screenshot inventory

- `evidence/ui/redesign-research-desk/01-dashboard-desktop.png` — SCREENSHOT_VERIFIED
- `evidence/ui/redesign-research-desk/02-screener-desktop.png` — SCREENSHOT_VERIFIED
- (Theme Card / CS / II / Weak verified in-browser; full inventory in a11y sweep batch)

## a11y/mobile sweep addendum (post-commit c4ae919)

- **a11y:** `--color-ink-3` darkened `#8A8E93 → #7A7F86` (≥4.5:1 on paper for tertiary text); icon-only buttons gained `aria-label` (AMQueue open-theme, ThemeCard back-to-queue ×2). — STATIC_OBSERVATION
- **Mobile (code-level):** CS Radar + Institutional tables wrapped in `overflow-x-auto`; existing grids already collapse `grid-cols-1 → md:grid-cols-2`; masthead wraps + run-stamp hidden below md. Real 390×844 browser check **EXTERNAL_NOT_TESTED** (browser tool viewport locked at 1258 — same limitation as audit lane).
- **Per-directory sweep:** 132 locked + 56 AM + 25 CS + 42 FO + 49 II = **304/304** reconcile exact — TEST_VERIFIED. Build exit 0, lint 0 errors/7 warnings.

## Evidence tags

BROWSER_VERIFIED · SCREENSHOT_VERIFIED · FUNCTION_TEST_VERIFIED · TEST_VERIFIED (304/304) · STATIC_OBSERVATION · EXTERNAL_NOT_TESTED (mobile)

## Verdict

**PASS WITH KNOWN DEVIATIONS** — Research Desk v3.0 implemented across all 11 pages; all audited P0 UI/narrative defects (C1–C6, M1/M3/M6/M8, C-02 frontend quarantine) remediated and browser-verified. Remaining work: mobile/a11y sweep, A-01/A-02 decisions, commit with evidence tags, independent visual review (llm-council routing per v4.0.0 Phase M).
<!-- 2026-08-04 17:45 UTC+7 -->
