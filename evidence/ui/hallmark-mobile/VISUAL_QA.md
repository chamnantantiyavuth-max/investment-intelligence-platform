# VISUAL_QA — Hallmark Mobile Verification + Article Long Document Treatment (FD #85 closeout)

**Date:** 2026-08-10 · **Scope:** closes FD #85 "Known limits" (mobile verification at all four widths; article Long Document treatment) · **Status:** PRODUCTION VERIFIED

## 1. What changed

### A. Mobile verification pass (closes FD #85 Known limit 1)
- **`frontend/src/index.css`** — Hallmark mobile floor applied globally:
  - Gate 34: `overflow-x: clip` on both `html` and `body` (was `visible` — no horizontal scroll could silently appear).
  - Gate 51: `h1/h2/h3 { overflow-wrap: anywhere; min-width: 0 }` (display headers wrap inside long words).
- **New tool:** `scripts/verify-mobile.mjs` — headless Chrome CDP script that emulates 320/375/414/768 CSS-pixel widths, logs in via the real API (HttpOnly cookie in a temp profile), measures `scrollWidth vs clientWidth`, checks clickable elements for two-line wrapping, captures a screenshot per width. Reusable for every future UI pass.

### B. Article Long Document treatment (closes FD #85 Known limit 2)
- **`frontend/src/pages/ReportArticlePage.tsx`** — replaced ~20 inline arbitrary-class selectors with a single `article-body` class (readable, maintainable, Hallmark macro 02).
- **`frontend/src/index.css`** — `.article-body` (Long Document macro 02): continuous prose, single column, measure **65ch**, line-height 1.75; section heads emerge from the flow (display face, hairline rule, generous space — no boxes); **roman pull-quotes** (gate 38a — italic removed); tables inside the measure with horizontal scroll only when needed; every color/font via `var(--token)` (gate 48).

## 2. Verification performed

| Check | Result |
|---|---|
| tsc -b | exit 0 |
| npm run lint | 0 errors (7 pre-existing warnings) |
| npm run build | ✓ built in 429ms |
| pytest full suite | **340/340 passed** |
| Browser (localhost:5173, logged-in) | /library + article render; console 0 errors |

### Mobile gates — `scripts/verify-mobile.mjs` (320 / 375 / 414 / 768 × 2 pages)

| Gate | /library | Article |
|---|---|---|
| Gate 34 — horizontal scroll | NONE ✓ (scrollW == clientW at all 4 widths) | NONE ✓ |
| Gate 34 — overflow-x clip html+body | clip\|clip ✓ | clip\|clip ✓ |
| Gate 49 — clickable text 2-line wrap | NONE ✓ | NONE ✓ |
| Gate 51 — h1 overflow-wrap | anywhere ✓ | anywhere ✓ |
| Visual pass (vision ×3) | masthead/hero render clean at 320px; no overlap/clipping | long-form document structure confirmed; tables aligned; readable at 375px |

Screenshots: `evidence/ui/hallmark-mobile/library-{320,375,414,768}.png` + `article-{320,375,414,768}.png`.

## 3. Honest notes

- CDP sessions get a fresh cookie profile — the first run captured the login page (screenshots deleted/overwritten); fixed by logging in via the real `/api/auth/login` inside each CDP session before navigating. Final captures are the authenticated magazine pages (vision-confirmed).
- `--color-ink-1` token does not exist in `:root` (only ink/ink-2/ink-3) — the first `.article-body` draft referenced it; corrected to `--color-ink-2` before shipping (verify-first caught it).
- The chunk-size warning on `npm run build` is pre-existing (not from this change).

## 4. Status

**FD #85 closeout COMPLETE** — both Known limits from `evidence/ui/hallmark-magazine/VISUAL_QA.md` are now closed: mobile verified at all four widths per Hallmark floor; article body upgraded to Long Document treatment. Feature Magazine (Direction B) is now the verified production treatment on /library + /library/:slug.

<!-- 2026-08-10 15:20 UTC+7 -->
