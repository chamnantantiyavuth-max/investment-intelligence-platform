# PLAN — Article Readability: Long-Report Navigation & Visual Hierarchy

**Status:** DRAFT (v0.1) — for Founder approval before implementation
**Date:** 10 Aug 2026
**Scope:** `frontend/src/pages/ReportArticlePage.tsx` + `frontend/src/index.css` + maybe `frontend/src/components/`
**Problem (Founder-reported, verified by vision 10 Aug 2026):** long reports (3,000+ words, 8 sections) render as a dense wall — no table of contents, heavy inline bolding creates noise, tight section spacing. Reader gets eyestrain ("ตาลาย").

## Verified root causes (browser vision on apple-deep-analysis-2026-08-09)

| # | Finding | Evidence |
|---|---|---|
| F1 | **No TOC / no jump navigation** | 8 numbered h2 sections; reader must scroll the whole article; only "← LIBRARY" and "← Earlier note" links exist |
| F2 | **Over-bolding** — nearly every paragraph has 2–4 `<strong>` phrases; `strong { color: foreground; font-weight: 600 }` in `.article-body` makes bold the default, not the emphasis | "heavy inline bolding… high visual noise" (vision) |
| F3 | **Tight section rhythm** | h2 margin-top 2.75rem + hairline is present but sections are text-dense; vision: "rhythm feels constrained" |

## Non-goals (SMART-SCOPE — stay out)

- No changes to report CONTENT (reports/*.md bodies — research content is governed; only presentation changes)
- No card grids, no decorative borders (borderless-by-default FD-032), no KPI widgets
- No Thai/translation work (reverted FD #91)
- No backend/API changes — TOC is derivable client-side from rendered h2s
- No new dependencies

## Options (Founder picks one direction)

### Option A — Article TOC (สารบัญ) — *recommended core*
Auto-generated table of contents from the article's h2 sections:
- Desktop: sticky left rail (or inline "In this note" block below the title) listing 8 sections with anchor links; scrollspy highlights the current section; click scrolls smoothly
- Mobile: collapsed "สารบัญ" row that expands (or a simple horizontal chip row)
- Pure client-side: `document.querySelectorAll('article h2')` → build list, assign ids; react-markdown headings need ids — add a small rehype plugin or post-render pass
- Fits magazine aesthetic: small-caps mono numerals + hairline separators, no boxes

### Option B — De-noise emphasis (reduce bold)
- CSS-level only: `strong` in `.article-body` keeps weight 600 but loses the `color: foreground` (stay ink-2 like body) → bold becomes subtle emphasis, not shouting
- Optionally reduce `.article-body strong` frequency is NOT possible via CSS alone (content-driven) — but a **content-level pass** on the longest reports (Apple Deep Analysis: 40+ bold phrases) could trim bold to verdicts + key numbers only. Content edits = governed (needs report-owner care), so CSS-first is safer.

### Option C — Section breathing + magazine numbering
- Increase h2 top-margin (2.75 → 4rem), add generous h3 spacing
- Magazine-style section number: oversized ghost numeral ("01"–"08") beside/instead of inline numbering — editorial break between sections
- Optional: first-paragraph drop cap on long reports (macro 05)

### Recommended: **A + B(CSS part) first**, C as polish pass if time remains.
Rationale: TOC fixes the "ต้อง scroll หา" pain directly (F1); CSS de-bold fixes the noise cheaply and safely (F2, no content governance); C is aesthetic — defer until A+B are seen on screen. All three are presentation-layer only (non-material per AGENTS.md UI rules).

## Implementation sketch (Option A + B)

1. `frontend/src/lib/articleToc.ts` — pure helper: given the article DOM, extract h2 texts → `[{id, text}]` (slugify: lowercase, strip numbers prefix optional)
2. `frontend/src/components/ArticleToc.tsx` — renders list; scrollspy via IntersectionObserver on h2s; anchor links `href="#id"`; sticky on desktop (`lg:sticky lg:top-8` in a right rail or above-title inline block)
3. `ReportArticlePage.tsx` — post-render pass assigns `id` to h2s (react-markdown: add a tiny `rehypeSlug`-style custom plugin, or `components={{ h2: ... }}` wrapper); render `<ArticleToc />` when ≥3 h2s
4. `index.css` — `.article-body strong { color: inherit }` (de-bold), h2 margin-top 4rem, toc styles (small-caps, hairline, scrollspy active state uses `text-primary` not a box)
5. Verify: tsc 0, lint 0, build ✓, suite 340/340, browser desktop + mobile (320/375) — TOC visible, anchors jump, scrollspy highlights, no horizontal scroll (Hallmark gates 34/51 still pass)

## Approval requested

Pick direction: **A** (TOC only) / **B** (de-bold only) / **C** (spacing+numbering) / **A+B** (recommended) / **A+B+C**
