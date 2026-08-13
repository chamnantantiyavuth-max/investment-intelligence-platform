# PHASE 2.1 — SEMANTIC HARDENING (S1–S4)

> Live Office v1 · Phase 2 = **PASS WITH CONDITIONS** (Founder review 2026-08-13)
> Scope: close FOUR bounded semantic/robustness findings before visual polish.
> Preserve Phase-2 UI/architecture. Do NOT redesign. Do NOT reopen H1/H2/H3 generally.
> Not started: Phase 3 visual polish. Not touched: Stage 7 (PASS WITH CONDITIONS), Stage 8 (HOLD).

## Changes delivered

| Finding | Fix | Files |
|---|---|---|
| **S1** — handoff lines ≠ live coordination | `/handoffs` classifies every desk edge ACTIVE / RECENT / HISTORICAL per request; HISTORICAL hidden by default, exposed via `?scope=all` (History toggle); packet animation only on real event → rendered ACTIVE/RECENT edge; `load_board(include_archived=True)` keeps completed/archived relationships classifiable | `dashboard/plugin_api.py`, `dashboard/dist/index.js`, `dashboard/dist/style.css` |
| **S2** — Error masked by Recently Completed | Precedence: Awaiting Founder > Working > Blocked > Reviewing > Queued > **Error** > Recently Completed > Idle; failure detection checks BOTH `task_runs.status` (crashed/timed_out/failed) AND `outcome` (crashed/timed_out/spawn_failed/gave_up) | `dashboard/plugin_api.py` |
| **S3** — heuristic diagnostics classifier | Structured: (1) explicit task metadata — schema has NO type/kind/tags column → documented hook, (2) exact title prefixes `[PILOT-NONCANONICAL]`/`[TEST]`/`[SYNTHETIC]`, (3) known harness profiles. No free-text substring ("synthetic"). Zero live-board reclassification (verified: no matching titles) | `dashboard/plugin_api.py` |
| **S4** — hard-coded Windows profile path | `_profiles_dir()` resolves via `hermes_cli.config.get_hermes_home()` (HERMES_HOME) first; Windows AppData path = last-resort fallback only | `dashboard/plugin_api.py` |

## Acceptance evidence (10/10)

1. **ACTIVE ≠ HISTORICAL** — live probes: open task pair → `class=active` edge (Quant → Data); both-done pair → `class=recent`; 39 legacy links (DR/PILOT/DISC chains, all done) → 15 desk edges, ALL `historical` — the Phase-2 "15 live-looking lines" were stale relationships, exactly as the Founder suspected. [live API]
2. **Historical links do not clutter default Office** — default `scope=active` returns 0 items; `historical_count: 15`; `scope=all` returns all 15. [live API + browser: 0 line elements rendered]
3. **Packet animation maps to a genuine edge** — pulse only when WS event task_id ∈ rendered edge's `task_ids` AND class ≠ historical (frontend guard). [code + browser 0 console errors]
4. **Error cannot be masked by Recently Completed** — locked test: recent success + recent failure on same desk → `error`; precedence tests for queued/blocked/awaiting_founder/reviewing/working still outrank. [pytest]
5. **Crash detection follows runtime semantics** — dual-field checks on `task_runs.status` + `outcome` per actual schema (verified kanban_db.py docstring + live PRAGMA). [pytest]
6. **No broad diagnostics false-positive** — negative tests: "Analyze synthetic data exposure" and mid-title "synthetic" stay Operational; exact prefixes + harness profiles still classify. [pytest]
7. **11 profiles still resolve** — `_profiles_dir()` → `…\AppData\Local\hermes\profiles`, all 11 org-* present; desks API `available: 11/11`. [pytest + live API]
8. **11-desk state agreement intact** — desk states unchanged by probes (probes are `[TEST]` → diagnostics layer; Quant diag `todo:1`, Data diag `todo:1` only); badges in browser match API 11/11 (Blocked / Awaiting Founder ×2 / Idle ×8). [live API + browser]
9. **Founder GATEs identical to Native Kanban** — `[GATE][ORG-2026-0004]` + `[GATE][ORG-2026-0012]` (2 decisions waiting). [browser]
10. **Zero-write / no persistent state** — no new routes; all classification derived per request; no tables/files/caches. Probes archived + unlinked (zero residue). [code + git diff]

## Verification trail

- **Suite:** `pytest` → **229/229 passed** (was 206; +23 bounded tests in
  `tests/test_capital_office_semantics.py`).
- **Live probes (bounded synthetic):** created 4 `[TEST]` tasks (2 linked pairs:
  org-quant-validator→org-data-steward open; org-cro→org-auditor done),
  verified active/recent classification + desk-state isolation, then archived
  all 4 and unlinked both pairs → final clean state: 0 shown edges,
  15 historical.
- **Browser smoke** (`smoke-21.py`, Playwright headless chromium, 1440×900):
  nav Kanban → Capital Office; 11 desks; 2 Founder GATEs; **0 handoff line
  elements** (honest); History toggle "Handoff history (15)"; **0 console
  errors**; screenshot `phase2.1-semantic-hardening-1440x900.png`.
- **Dashboard profile corrected:** machine `active_profile` had drifted to
  `capcmd` (from an inter-session capital-command session); restored to `iip`
  (`hermes profile use iip`) + dashboard restart — banner verified
  `Managing profile "iip"`.

## Notes / deviations

- S3 tier 1 (explicit metadata) is a documented hook, not implemented: the
  `tasks` schema exposes no type/kind/tags column (verified via PRAGMA
  2026-08-13). Prefix + profile tiers cover today's markers.
- Archived-task inclusion (`include_archived=True`) was added after the first
  live pass: with archived tasks excluded, archived links vanished from
  `scope=all` — contradicting the S1 contract ("both sides completed/archived").
- RECENT edges stay visible (subdued) for the 30-minute window after
  completion, then transition to HISTORICAL — documented in
  `LIVE-OFFICE-SOURCE-MAP.md` §S1.

<!-- 2026-08-13 18:33 UTC+7 — artifact_timestamp.py (system clock) -->
