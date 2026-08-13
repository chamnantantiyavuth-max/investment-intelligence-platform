# Capital Intelligence Live Office v1 — PHASE 2: SPATIAL OFFICE (13 Aug 2026)

> Founder: FIRST VISUAL CHECKPOINT = APPROVED / PASS → Phase 2 Spatial Office.
> H1–H3 hardening executed first; spatial floor + pixel avatars + state visuals
> + minimal event-tied animations + Founder Desk centerpiece + basic real
> handoff lines + compact activity rail. STOP for Founder visual review.
> Clock basis: artifact_timestamp.py (2026-08-13 17:58 +0700).

## H1 — Installed profile truth ✅

All 11 org profiles verified installed in the runtime (`%LOCALAPPDATA%/hermes/
profiles/` — incl. `org-options-strategist`): every desk `available: true`; no
desk shows a missing profile. The adapter distinguishes anyway: profile absent
→ `unavailable` (Not Installed), NEVER Idle (verified in code + desks API).

## H2 — Operational vs Diagnostics ✅

`PILOT-NONCANONICAL` / harness-canary / test / synthetic tasks → presentation
`diagnostics` layer per desk (badge, e.g. Data Steward `DIAG done:4 blocked:1`
= pilot failure-test residue), NOT the main desk state. Data Steward desk now
reads **Idle** (operational) with the pilot residue visible as a DIAG badge —
it no longer dominates the organizational view. Hermes truth untouched (tasks
remain on the board; nothing filtered from kanban).

## H3 — Runtime adapter isolation ✅

All DB access behind ONE `LiveOfficeDataAdapter` in plugin_api.py (kanban_db
helpers preferred; the read-only SELECTs on task_runs/task_events/task_links
isolated inside it). Frontend schema-independent (JSON API only). Direct SQLite
remains TEST-ORACLE-only (verification scripts).

## Spatial office (charter §Phase 2)

- Floor: Founder Desk (top, centerpiece) → Chief of Staff (center) → analyst
  row (Commodity/Macro/Equity) → support row (Options/Quant/Data) → IC
  Secretary (center) → review row (CRO/Auditor) → Radar Scout (bottom edge).
- Original pixel-style SVG avatars per role (role color + glyph), desk lamp
  color = state, state icon per presentation state.
- Founder Desk: "2 decisions waiting" + both [GATE] rows (0004/0012) — the
  awaiting-founder desks show floating document indicators; still read-only.
- 15 handoff lines drawn from REAL task_links (parent→child assignee edges);
  a packet animates along an edge when a spawned/linked event arrives.
- Animations tied ONLY to state/events: idle breathe, working typing dots +
  lamp pulse, blocked/error pulse, awaiting-founder document float, completed
  flash. No random movement.
- Recent Activity + Workers/Runs moved into a compact collapsible bottom rail.

## Acceptance (charter 10 items)

| # | Criterion | Result |
|---|---|---|
| 1 | 11 desks map to live Hermes state | ✅ 11/11 vs DB oracle (operational-only) |
| 2 | Founder gates match Native Kanban | ✅ 2 GATE rows = t_51e3be79 + t_2342aa1d (same as native) |
| 3 | State changes react live through WS | ✅ tasks 68→69 + "created 05:55 PM" at +2s, no refresh (bounded test archived) |
| 4 | Diagnostics don't dominate desk state | ✅ Data Steward Idle + DIAG badge (pilot residue separated) |
| 5 | Missing profile ≠ Idle | ✅ H1: available flag + unavailable state implemented; all 11 installed |
| 6 | No Office writes | ✅ 0 write routes (grep), 0 INSERT/UPDATE/DELETE |
| 7 | No Office persistent org state | ✅ no tables/files/caches; derived per request |
| 8 | No Hermes core patch | ✅ user-plugin mechanism only |
| 9 | Usable at 1440×900 | ✅ vision-QA clean (DIAG badges inline, no overlap, graceful truncation) |
| 10 | No animation contradicts state | ✅ animations keyed to presentation state/WS events only |

## Verification evidence

- `phase2-spatial-office-1440x900.png` — vision-confirmed layout + states +
  founder + handoff lines, no layout breaks.
- WS live proof + failure mode (DEGRADED, no fabricated states) re-run on the
  Phase 2 build.
- Zero-write: `grep @router.post|put|patch|delete` = 0; INSERT/UPDATE/DELETE = 0.
- H1/H2/H3 verified via desks API (available flags, diagnostics counts, oracle
  agreement 11/11).

## Deferred (unchanged)

Write controls, approve/unblock buttons, IPM room, sound, complex game
mechanics, autonomous random avatar movement, advanced orchestration graph,
Stage 8 work. Stage 7 = PASS WITH CONDITIONS, Stage 8 = HOLD (preserved).

<!-- 2026-08-13 17:59 UTC+7 (artifact_timestamp.py) -->
