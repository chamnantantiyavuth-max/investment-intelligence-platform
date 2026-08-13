# Live Office v1 — First Checkpoint (13 Aug 2026)

> Capital Intelligence Live Office v1 first checkpoint per Founder directive.
> Native Kanban (Hermes Dashboard tab) = the human-visible reference surface.
> NO Office write controls in v1. Clock basis: artifact_timestamp.py.

## Checkpoint requirements (per directive)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| 1 | Native Kanban restored (Hermes Dashboard tab) | ✅ | `PHASE-MINUS1-RESTORATION-2026-08-13.md` — tab visible, board renders, 0 console errors, live WS |
| 2 | Capital Office skeleton | ✅ | `/org-office` (Org Office — 11 desks, read-only, data_source `hermes_kanban_board`) |
| 3 | Live 11-desk view | ✅ | org-queue → cards grouped by `principal_owner` (14 owners incl. 11 org desks + iip/ipm/harness pilots) |
| 4 | Sampled Office states agree 1:1 with Native Kanban | ✅ | Per-desk status counts below — **14/14 desks OK** |

## 1:1 agreement sample (13 Aug 17:0x +0700, live cross-check)

Method: auth'd `/api/org-queue` (Office surface) vs `kanban.db` at
`%LOCALAPPDATA%/hermes/kanban/boards/iip/kanban.db` (the exact table the native
Kanban plugin reads). Status key case-folded (Office returns display labels
`Done/Blocked/Archived`; DB stores lowercase). Sampled = ALL desks with cards.

| Desk | Office | Native | Match |
|---|---|---|---|
| harness-canary-ipm | done 1 | done 1 | OK |
| harness-docker-test | done 1 | done 1 | OK |
| iip | archived 2, done 10 | archived 2, done 10 | OK |
| ipm | done 1 | done 1 | OK |
| org-auditor | done 11 | done 11 | OK |
| org-commodity-analyst | done 3 | done 3 | OK |
| org-cos | blocked 2, done 18 | blocked 2, done 18 | OK |
| org-cro | done 2 | done 2 | OK |
| org-data-steward | blocked 1, done 6 | blocked 1, done 6 | OK |
| org-equity-analyst | done 5 | done 5 | OK |
| org-ic-secretary | blocked 1, done 2 | blocked 1, done 2 | OK |
| org-macro-strategist | blocked 1 | blocked 1 | OK |
| org-quant-validator | done 3 | done 3 | OK |
| org-radar-scout | archived 2 | archived 2 | OK |

Blocked-sample semantic check: the 5 blocked cards are identical on both
surfaces — t_2342aa1d ([GATE] 0012 needs_input), t_51e3be79 ([GATE] 0004
needs_input), t_d5019196 (0017), t_8411623f (0016), t_1ecfaaef (pilot fail).

## Checkpoint verdict

**LIVE OFFICE V1 FIRST CHECKPOINT = MET.** The Capital Office skeleton is the
existing read-only `/org-office` surface; it renders the live 11-desk view from
the Hermes board adapter, and sampled office states agree 1:1 with the native
Kanban reference (14/14 desks, blocked sample identical). No write controls
added. Stage 8 remains HOLD; board `other` untouched.

<!-- 2026-08-13 17:05 UTC+7 (artifact_timestamp.py) -->
