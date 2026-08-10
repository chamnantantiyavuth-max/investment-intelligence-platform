# VISUAL_QA — FD #92 Thai-Only Research Content

**Date:** 2026-08-10/11 UTC+7 · **Scope:** 24 published reports rewritten in Thai (UI stays English) · **Commits:** 65473ba → c30afcf (4 batches)

## What was verified

| Check | Result | Evidence |
|-------|--------|----------|
| /library renders Thai titles + summaries (24/24) | PASS | snapshot (all-Thai featured hero, This week's notes, Latest intelligence list; series counts Apple 10 / Silver 8 / JNJ 2 / Gold 2 / Weekly 2 = 24) |
| Article page Thai body rendering | PASS | vision: authentic Thai glyphs, no tofu, tone marks correctly placed, TOC (01–08) + tables + lists render, mixed Thai/EN terms flow naturally |
| Thai font fallback | PASS | `--font-sans`/`--font-display` now include Leelawadee UI + Tahoma after Inter/Georgia (index.css); rendered via clean sans fallback |
| Console errors | 0 | browser_console: 0 messages, 0 JS errors |
| Horizontal overflow | 0px | document.scrollWidth − clientWidth = 0 on article page |
| Number/accession/date preservation | 3,442 tokens / 0 missing | `evidence/qa/fd92-token-preservation.py` — every numeric token (incl. accessions 0000320193-26-…, ratios 88:1, %, $ amounts, dates) from English originals (6502b79) present in Thai rewrites |

## Screenshots

- `library-thai.png` — /library (desktop viewport 1258px)
- `article-deep-analysis-thai.png` — RM-2026-0004 deep-analysis article (desktop viewport 1258px)

## Honest limits

- Mobile (390px) live viewport NOT re-tested this session (browser viewport fixed at 1258; `window.resizeTo` blocked). Structural mobile guard present (html/body `overflow-x: clip` → 0 horizontal scroll at any width); Thai wraps per-cluster so no long-word overflow; prior i18n session (FD #90, before revert) verified Thai at mobile width. Classified EXTERNAL_NOT_TESTED for live 390px visual.
- Font fallback relies on OS-installed Thai fonts (Leelawadee UI/Tahoma on Windows). Non-Windows viewers fall back to system-ui — glyphs still render, style may differ.
- English originals remain in git history + `evidence/` + `research/` workspaces (Constitution §23.9 — never rewrite history).

## Verification tags

- TEST_VERIFIED: pytest 340/340; npm run build exit 0; npm run lint 0 errors (7 pre-existing warnings); token-preservation script 24/24 files PASS
- STATIC_OBSERVATION: browser console 0 errors; overflow 0
- EXTERNAL_NOT_TESTED: live mobile 390px visual
<!-- 2026-08-11 01:00 UTC+7 -->
