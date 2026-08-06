# Research Blog — Design Review & Report Catalog (FD #62 deliverable)

**Status:** FOR FOUNDER APPROVAL · **Date:** 2026-08-06 17:45 UTC+7
**Authority:** FD #62 ("full report catalog + blog design presented for Founder approval") · FD #60 (institutional standard)
**Scope:** presentation-layer review only — no code/API/schema changes in this document

---

## 1. Current state (verified this session)

The blog is live with **3 published reports**, all browser-verified (desktop 1258px + code-level mobile audit):

| Slug | Title | Type | Subject | Author |
|---|---|---|---|---|
| `silver-product-note-2026-08-06` | Silver — The Metals Trade Hiding in Plain Sight | product | Silver (SLV) | Commodity Research |
| `apple-moat-2026-08-06` | Apple's Moat: How Durable, and What Would Break It | company | AAPL | Equity Research (RM-2026-0001) |
| `apple-moat-opposing-2026-08-06` | The Case Against the Moat — Opposing Essay | company | AAPL | Chief Research Risk Officer |

Series structure: Apple = main essay + opposing essay, cross-linked both ways; article footer shows "← Earlier AAPL note" (series navigation). Silver = standalone (next note in series when an update lands).

## 2. Design review — visual verification results

**Library index page** (`/library`) — vision-verified **institutional-grade** (FD #60 standard met):
- Serif display headings + tracked uppercase sans UI labels (financial-editorial character)
- Borderless list rows with thin hairline dividers — 0 full-perimeter borders (borderless-by-default ✅)
- Restrained palette: off-white canvas, ink text, single muted accent (PUBLISHED status)
- Filter bar: STATUS + TYPE native selects (functional; styling is the one cosmetic gap noted below)
- No KPI cards, no hero banner, no icon tiles (no generic AI aesthetic ✅)

**Article page** (`/library/:slug`) — vision-verified **typeset research-note quality**:
- Title block: kicker (COMPANY RESEARCH NOTE) + ticker badge + PUBLISHED status + title + date/author
- Provenance callout (mandate id, horizon, advisory-only, portfolio-blind)
- Typography hierarchy: run-in bold dimension headings, 14.5px/1.75 body, 65–85 char line length, 820px max column
- Tables render with overflow-x-auto (mobile-safe); monospace tabular figures
- Cross-reference links (companion essay) + series footer navigation
- Zero visual defects observed (vision: "alignment, font rendering, borders, contrast, layout grid are clean and defect-free")

**Mobile (code-level audit — browser viewport locked to desktop per kanban precedent):**
- Both pages are fluid `max-w` containers (820/960px) — stack naturally, no fixed-width grids
- Filter bar uses `flex-wrap`; tables use `overflow-x-auto`; no horizontal overflow at desktop
- ✅ mobile-safe by construction; full mobile visual pass deferred to a browser-tool unlock

## 3. Findings & recommended improvements (smallest sufficient set)

| # | Finding | Severity | Recommendation | Action needed |
|---|---|---|---|---|
| D1 | Native select styling (STATUS/TYPE) is browser-default — the only element not matching the editorial system | Cosmetic | Restyle selects to match tokens (border-rule, font-mono, ink-2) | Code change (presentation-only, Quick) |
| D2 | Right-hand whitespace on wide desktops (~30% empty) | Cosmetic | Accept as reading-window design OR add a narrow right rail later (report stats / series list) — NOT now (SMART-SCOPE) | Decision |
| D3 | Library lacks a "series" grouping signal beyond the footer link | Minor | When a subject has ≥2 notes, show a "series: N notes" hint on the card | Code change (small) — could wait |
| D4 | Header wordmark wraps to two lines at some widths | Cosmetic | Reduce tracking or allow single-line lockup | Code change (trivial) — could wait |

**Not recommended now (SMART-SCOPE):** right rail with bookmarks/recent tickers; per-report comment/annotation; tags; full catalog pages beyond the flat list. The blog is 3 reports — the flat institutional list is the right shape for the pilot.

## 4. Report catalog — what's next (planned series)

| Subject | Next note | Trigger |
|---|---|---|
| AAPL | Apple evidence upgrade (Q1/Q2 FY26 10-Q, earnings-call transcripts, IDC/Counterpoint share data) — evidence-log §9 lists gaps | On-demand deep research mandate or quarterly refresh |
| Silver (SLV) | "What changed" update | Pipeline refresh / watch items move (ETF flows, physical premium, gold pause) |
| New company mandates | per Founder mandate (Plan A §6 on-demand deep research) | Founder call |
| Weekly Intelligence Letter | first letter this week (IC Secretary) | Plan A §7 cadence pilot |

## 5. Approval request

Approve the blog design as-is (institutional-grade, verified) with the option to:

- **A — Accept as-is** (recommended): no code changes; D1–D4 logged as cosmetic backlog for the next UI pass
- **B — Accept + D1 only**: restyle the two selects to match the editorial system (5-min Quick change, presentation-only)
- **C — Accept + D1/D3**: selects + series hint on library cards (small code change)
- **D — Return**: specific changes wanted

Evidence: vision analyses (library + article pages, institutional verdict, zero defects), console 0 errors, screenshots in `C:\Users\Admin\AppData\Local\hermes\profiles\iip\cache\screenshots\` (browser_screenshot_b3f10520f3c84f0499c3208564f0f643.png = library, browser_screenshot_4039f4a903724dc8971c2df7ceb6dcea.png = article).

<!-- 2026-08-06 17:45 UTC+7 -->
