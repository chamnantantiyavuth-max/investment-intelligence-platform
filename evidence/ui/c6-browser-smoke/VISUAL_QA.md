# VISUAL_QA — C6 browser smoke /kanban + /org-office (13 Aug 2026)

Method: Playwright headless chromium (real browser render), 1440×900, login via
IIP_AUTH_* (local .env), console + pageerror capture. Screenshots below.

## /kanban (KanbanBoardPage)

- ✅ H1 "Kanban Board"; read-only notice present
- ✅ Column headers render the FULL Hermes-native vocabulary:
  Triage 0 · Todo 0 · Scheduled 0 · Ready 0 · Running 0 · Blocked 5 · Review · Done · Archived
  (9/9 — direct statuses, no legacy 11-column names)
- ✅ Blocked column shows [GATE][ORG-2026-0012] + [GATE][ORG-2026-0004]
  with `blocked: needs_input` (C1 repair visible), plus migrated 0016/0017 cards
- ✅ [RADAR][INBOX] ORG-2026-0022 card present
- ✅ console errors: 0
- ⚠️ Cosmetic: long titles truncate in the 192px columns (pre-existing narrow-column
  design; board is horizontally scrollable per FD #59) — not a regression

## /org-office (OrgOfficePage — "The research floor")

- ✅ 11 desks render (Chief of Staff 20 · IC Secretary 3 · Commodity Analyst 3 ·
  Macro Strategist 1 · Equity Alpha 5 · Options Strategist standby · CRO 2 ·
  Quant Validator 3 · Data Steward 7 · Internal Auditor 10 · Radar Scout 2);
  "Desks active 10/11"
- ✅ "Awaiting you 5 (blocked · review · triage)" — native-status note
- ✅ "Active holds 0 (none is silent)" + "HOLDS & EXCEPTIONS: No active holds"
  (honest — both HOLD-* cleared/historical, relocated per C4)
- ✅ Org pulse "Attention (0 holds · 2 blocked)" — derived from board reality
- ✅ console errors: 0; no layout breaks

## Verdict

PASS — both surfaces render Hermes-native work-state directly; no legacy
11-column leakage; C1 gate semantics visible; honest empty/absence states.

Files: `evidence/ui/c6-browser-smoke/kanban.png`, `org-office.png`, `smoke.py`

<!-- 2026-08-13 17:00 UTC+7 -->
