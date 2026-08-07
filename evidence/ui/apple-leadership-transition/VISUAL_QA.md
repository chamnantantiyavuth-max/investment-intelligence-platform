# VISUAL_QA — Apple Leadership Transition follow-up (published 2026-08-07)

**Task:** Apple evidence upgrade → follow-up note publication (FD #62 report pipeline)
**Commits:** `5f2a9b8` (evidence upgrade) · `144f78a` (draft + audit chain) · `c1c0192` (state sync) · (this: publish + remark-gfm fix)

## Browser verification (localhost:5173, real browser)

| Check | Result |
|---|---|
| `/library` index | ✅ 16 published; both new reports show `COMPANY · PUBLISHED` with correct title/date/author |
| Main article page `/library/apple-leadership-transition-2026-08-07` | ✅ typeset research note; title block (COMPANY RESEARCH NOTE / AAPL / PUBLISHED), sections 1–7 with border-rule headings, verdict + limits |
| §6 change-condition table | ✅ real bordered table (2 columns: Change-condition / Status as of Q3 FY26 evidence; 8 condition rows), no pipe-leak, wraps cleanly |
| CRO article page `/library/apple-leadership-transition-opposing-2026-08-07` | ✅ typeset; thesis paragraphs, sourced figures as bold inline, conclusion verdict FAIL, `← EARLIER AAPL NOTE` cross-link present |
| Raw markdown leak (pipes/`**`/`#`) | ✅ none detected (visual + DOM check `hasPipeLeak: false`) |
| Console errors | ✅ 0 runtime errors on current page (1 stale HMR artifact from file-edit mid-session, not reproducible on fresh load) |
| DOM integrity (main page) | articleLen 12,288 chars · 1 table · 9 table rows · H1 correct |

## Defect found & fixed during verification

**GFM tables rendered as raw pipe text** in `/library/:slug` — `ReportArticlePage.tsx` imported `react-markdown` but never passed `remarkPlugins={[remarkGfm]}`, so GFM table syntax (used in the new report's §6 change-condition table) leaked as literal `| ... |` lines. This is the first published report with a markdown table, exposing the latent defect (FD #62: reader never sees raw markdown).

**Fix:** added `import remarkGfm from "remark-gfm"` + `remarkPlugins={[remarkGfm]}` to `<ReactMarkdown>` in `frontend/src/pages/ReportArticlePage.tsx`. Verified table renders as real `<table>` (column headers + 8 rows), no leak.

## Build/lint

- `npm run lint` → 0 errors (7 pre-existing warnings)
- `npm run build` → exit 0 (2249 modules, 526ms)

## Screenshots

- `evidence/ui/apple-leadership-transition/main-article-table.png` — §6 change-condition table render
- `evidence/ui/apple-leadership-transition/cro-article-page.png` — CRO companion article page

<!-- 2026-08-07 12:50 UTC+7 -->
