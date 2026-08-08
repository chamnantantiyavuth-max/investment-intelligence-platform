# VISUAL_QA — Hallmark Magazine Blog Mockups (FD #74 proposal)

**Date:** 2026-08-09 · **Skill:** hallmark v1.1.0 (installed from Nutlope/hallmark) · **Status:** DESIGN PROPOSAL — no production code (FD #74 decision pending)

## Deliverable

Three one-page HTML mockups applying Hallmark discipline to the magazine blog format + blog structure.
Each shows: library index (magazine format) + article treatment sample (blog structure). Real report data
(22 published reports, real titles/dates/authors/series — honest copy, slop-test gate 46).

| Direction | File | Macrostructure | Nav | Footer | Palette anchor |
|---|---|---|---|---|---|
| A — Broadsheet | `a-broadsheet.html` | Index-First | N6 Newspaper masthead | Ft4 Dense colophon | warm paper + bronze |
| B — Feature Magazine | `b-feature-magazine.html` | Ecosystem Index | N6 Masthead (single-rule) | Ft1 Mast-headed | IIP paper + steel blue (current system) |
| C — Research Ledger | `c-research-ledger.html` | Stat-Led (index ledger) | N9 Edge-aligned minimal | Ft2 Inline single line | IIP paper + steel blue |

## Verification performed

- **Browser render (desktop):** all three pages opened in real browser, console clean, no JS errors.
- **Visual pass (browser_vision ×3):** masthead/hero/grid/table/footer all render with correct hierarchy;
  no overlap, no broken alignment, no clipping.
- **Responsive discipline:** `overflow-x: clip` on `html` + `body` (gate 34) ✓ · media collapse at 60rem
  (grid → 1-col) and 40rem (rows → 1-col, stat figure step-down) ✓ · `prefers-reduced-motion` fallback ✓
  · display headers `overflow-wrap: anywhere` (gate 51) ✓ · no horizontal scroll at render width ✓
  · clickable text `white-space: nowrap` (gate 49) ✓
- **Honest copy (gate 46):** all titles/dates/authors/series from `reports/*.md` frontmatter verbatim;
  series counts verified (Apple 8, Silver 8, Gold 2, JNJ 2, Weekly 2 = 22 published). No invented metrics.
- **Slop-test pass (58 gates):** no Inter-everywhere (Georgia display + Inter body + JetBrains Mono outlier =
  permitted 2+1); no gradients; no icon tiles; no card-in-card; no eyebrows; roman display type (gate 38a);
  hairline rules not card borders; accent < 5% viewport; tokens via `:root` var() only (gate 48);
  no re-drawn chrome (gate 47); no fake metrics; no side-stripe cards; no aurora blobs.

## Status

**2026-08-09 — Direction B IMPLEMENTED in production (FD #85, Founder approved Option A):**
`LibraryPage.tsx` (full magazine treatment: single-rule masthead + hero feature + asymmetric 01/02/03 grid +
latest stream + series chips + Ft1 footer; all existing filter logic preserved) + `ReportArticlePage.tsx`
(TitleBlock provenance strip → borderless hairline, FD #84 no-box; typeset body + remark-gfm tables untouched).

Verification: `tsc -b` exit 0 · `npm run lint` 0 errors · `npm run build` exit 0 · pytest 141/141 · browser
(localhost:8000): /library renders magazine layout, series filter works (Apple → 8 rows, chip active),
console 0 errors, no horizontal scroll, article page typeset with table + borderless provenance.
Screenshot: `04-library-production-desktop.png`. Commit: see git log.

## Known limits

- Mockups are static HTML (design proposal only). Mobile screenshots at 320/375/414/768 not captured
  (browser tool viewport fixed at desktop); responsive rules verified by code inspection + computed styles.
  Production implementation would verify live at all four widths per Hallmark mobile floor.
- Article treatment is a sample block inside each mockup; full article page structure (ReportArticlePage)
  would get its own Long Document treatment in implementation.

## Recommendation

Direction **B (Feature Magazine)** — evolution of the accepted FD #84/B treatment with Hallmark polish:
steel-blue IIP accent, asymmetric feature grid, series chips, Ft1 footer. Closest to current system =
lowest-risk path to "magazine" feel. A (Broadsheet) = strongest editorial statement, most distinct from
current app. C (Ledger) = densest, most "research desk" — matches the Research Desk v3.0 pattern (FD #51).

<!-- 2026-08-09 01:15 UTC+7 -->
