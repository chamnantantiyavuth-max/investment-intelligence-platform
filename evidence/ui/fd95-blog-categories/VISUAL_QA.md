# VISUAL QA — Blog category layout (FD #95, structure A)

**Date:** 2026-08-11 · **Browser:** local :8000, desktop 1258px viewport, authenticated

## What was verified

1. **Category sections render in Founder-approved order (structure A):**
   - `หุ้นที่คัดจากข้อมูลผิดปกติ` — DEEP RESEARCH · ANOMALY (3 rows: JNJ talc, Apple Services margin, Apple buyback mask)
   - `หุ้นที่คัดตามคำขอ (Buffett / Pabrai / Li Lu / 100 Baggers)` — DEEP RESEARCH · QUALITY & ASYMMETRY (3 rows: Apple deep-analysis, leadership, moat)
   - `Close System Products` — COMMODITY RESEARCH (6 rows: silver 5 + gold 1 mains)
   - `Weekly Intelligence` — WEEKLY (2 rows)
   - `All research notes` — flat searchable stream (14 mains)
2. **Companion nesting (the scatter fix):** main + opposing = ONE row; `+ OPPOSING ESSAY (CRO)` nested under the main title. Hero shows a paired "The opposing essay (CRO)" button. Rows WITHOUT a companion are correct-by-truth (correction note, pilot product note, org weekly letters genuinely have no opposing).
3. **Counts:** `14 research notes · 24 published` — 24 files, 10 companions hidden under mains (not 24 standalone rows).
4. **Console:** 0 errors / 0 warnings.
5. **No horizontal scroll** at 1258px; grid collapses to 1 column on mobile (sm: breakpoint) + overflow-x clip structural guard (prior mobile floor).
6. **Vision review:** sections prominent, rows clean 3-col (date | title+companion | series tag), no layout defects.

## Screenshots

- `library-sections.png` — full page with 4 category sections + all-notes stream
- `library-categories.png` — category headers + nested companion links

## Implementation notes

- `backend/report_store.py`: parses `category` frontmatter field; canonical
  `REPORT_CATEGORIES` + `CATEGORY_LABELS`; backward-compat default from type
  (product→cs_product, weekly→weekly, company→deep_research_quality).
- All 24 report files gained `category:` in frontmatter (deterministic mapping,
  YAML re-parse verified 24/24).
- `LibraryPage.tsx`: category-section grouping over mains; companion nested via
  pairing key `slug.replace("-opposing-", "-")` (handles the
  `<base>-opposing-<date>` naming convention — the old `-opposing$` regex never
  matched, this was a real bug in the previous companion matcher).
- `ReportMeta.category` added to the API client.

## Verification tags

- TEST_VERIFIED: 7 new locked category tests + 190 existing (28 focused pass)
- STATIC_OBSERVATION: tsc 0, build exit 0, lint 0 errors
- TEST_VERIFIED: browser console 0 errors; vision confirmed layout
- EXTERNAL_NOT_TESTED: mobile 390 live viewport (browser locked; structural
  guards + prior mobile baseline cover)

<!-- 2026-08-11 13:45 UTC+7 -->
