# Visual QA — Magazine B Implementation (FD #84)

**Task:** Implement Modern Digital Magazine (direction B) on /library + /library/:slug
**Date:** 2026-08-07 · **Commit:** pending (this session)
**Approved direction:** `design/mockups/magazine-b-modern.html` (Founder pick, FD #84) — text/typography-driven editorial; **AI-generated art REJECTED** (Higgsfield option declined — no imagery anywhere).

## Files changed

- `frontend/src/pages/LibraryPage.tsx` — rebuilt as magazine index: minimal masthead ("Research Intelligence." + published count), hero feature (FEATURED badge + kicker + clamp display headline + standfirst + mono meta + CTA + CRO companion link), asymmetric 3-col feature grid (01/02/03), Latest intelligence stream (date/title/series, restyled STATUS+TYPE selects = D1 backlog), series chips (All/Apple/Silver/Weekly/JNJ/Gold = D3 series grouping backlog).
- `frontend/src/pages/ReportArticlePage.tsx` — article hero upgraded to B treatment (kicker + clamp display headline + standfirst + mono meta + provenance chips panel), typeset body unchanged (remark-gfm tables preserved), pull-quote blockquote styling, series footer nav preserved.
- `reports/jnj-talc-resolution-2026-08-07.md` — link label fixed: `jnj-talc-resolution-opposing-2026-08-07.md` → `JNJ's Talc Cleanup Can Fail by Sequence, Not Shock` (raw-filename leak, FD #62 "reader never sees raw markdown" violation; href already SPA route).

## Content logic (data-driven, no hardcoding)

- **Hero (cover):** latest published **main** research note — excludes `type=weekly` (cadence letter) and `-opposing` companions. Currently: Silver Valuation Anchor correction (7 Aug).
- **Feature grid:** next 3 main notes by date desc.
- **Stream:** all remaining published (incl. weekly + opposing companions, `+ opposing` tag).
- **Companion link:** true base-slug pair match (`{base}-opposing`), same subject — bug fixed during verification (first pass wrongly matched any series-sibling opposing essay).
- **Series grouping:** display-level subject-token map (AAPL→Apple, Silver, Gold, JNJ, weekly→Weekly). Chips filter the stream; Status/Type selects preserved.

## Browser verification (real app, :8000 production build)

| Check | Result |
|---|---|
| /library renders (login auth-gated) | ✅ hero + grid + stream + chips all present, real 22-report data |
| Series chip filter (Apple) | ✅ stream → 8 Apple rows, chip active state |
| Hero/feature exclusion logic | ✅ weekly + opposing excluded from cover; companion links correct |
| /library/jnj-talc-resolution-2026-08-07 article | ✅ B hero (kicker/headline/standfirst/provenance panel) + typeset body + blockquote + series nav |
| Companion label (md leak) | ✅ fixed → renders as title, not filename |
| Console errors | ✅ 0 messages / 0 errors |
| Horizontal overflow (1258px) | ✅ none (scrollWidth ≤ innerWidth) |
| Borderless audit | ✅ 0 full-perimeter bordered surfaces on library; article = 2 tonal panels (no outline) — within 0–2 budget |
| Generic-AI scan | ✅ no KPI cards, no hero banner, no icon tiles, no decorative gradients |
| Mobile | ⚠️ code-level audit only (browser tool viewport locked to desktop per kanban precedent): grid-cols-1 → md:3-col, clamp() type, flex-wrap, stream series tag hidden <sm — mobile-safe by construction; full mobile visual pass deferred to browser-tool unlock |

## Findings fixed during this pass

1. **Hero was Weekly Letter** (first build) — cover should be a main research note → `mains` filter added.
2. **Companion mismatch** — silver correction showed a CRO link for a different silver report → base-slug pair matching.
3. **Raw `.md` filename leak** in JNJ report companion label (pre-existing, FD #62 violation) → label fixed to report title.

## Evidence

- `evidence/ui/magazine-mockups/{a-classic,b-modern,c-hybrid}-desktop.png` — approved-direction mockups (B picked).
- `evidence/ui/magazine-b-implementation/02-library-desktop.png` — /library rendered.
- `evidence/ui/magazine-b-implementation/03-article-desktop.png` — article page rendered.
- Suite: pytest 305 passed + 6 skipped (311 total, unchanged); lint 0 errors; `npm run build` exit 0.

## Verdict

**PASS** — implementation matches approved mockup B; functionality (filters, series nav, tables, auth) preserved; borderless 0–2; no AI imagery per FD #84.

<!-- 2026-08-07 19:50 UTC+7 -->
