# Phase -1 — Native Hermes Kanban Dashboard Tab Restoration (13 Aug 2026)

> Precondition for Capital Intelligence Live Office v1. UI/plugin restoration
> ONLY — no Kanban DB / task model / dispatcher / Stage-7 / board-architecture
> change. Clock basis: `scripts/artifact_timestamp.py` (2026-08-13 17:04 +0700).

## 1. Diagnosis (verified against the ACTUAL v0.20.0 runtime — no guessing)

| Check | Result |
|---|---|
| Hermes version | v0.20.0 (2026.8.3) — install root `C:\Users\Admin\AppData\Local\hermes\hermes-agent` |
| Bundled kanban dashboard plugin | **PRESENT** — `plugins/kanban/dashboard/` = `manifest.json` (name=kanban, v1.0.0, tab `/kanban` after:skills, entry dist/index.js) + `plugin_api.py` (thin wrapper over `hermes_cli.kanban_db` — same code path as CLI/gateway; `/events` WS tails task_events) + `dist/index.js` (189,526 B) + `dist/style.css` (45,467 B) |
| Dashboard web_dist | `hermes_cli/web_dist/` built 12 Aug 17:20 — AFTER the plugin (17:18) → assets current |
| Profile config (iip) | `plugins.disabled: []` — NOT disabled |
| **GLOBAL config** | `$LOCALAPPDATA/hermes/config.yaml` → **`plugins.disabled: [kanban]` (line 320)** ← the gate. (Also `disabled_toolsets: kanban` line 18 — agent-toolset gate, left untouched; iip/org profiles override per-profile.) |
| Discovery (`/api/dashboard/plugins/rescan`) | `{ok:true, count:2}` → kanban IS discovered; `_is_active()` filtered it via the global `plugins.disabled` |
| Stale-server factor | The machine dashboard (PID 47152) predated the plugin build → its plugin-API routes were NOT mounted (404 on `/api/plugins/kanban/{config,boards,board}`) → restart required after config fix |

**Root cause (two-part):** (1) the earlier IIP iteration disabled the kanban
plugin in the GLOBAL config (`plugins.disabled: [kanban]`) → tab filtered from
every dashboard; (2) the running machine dashboard predated the plugin → its
`/api/plugins/kanban/*` routes were not mounted even after discovery.

## 2. Restoration (minimum compatible change — no core patch, no upstream copy, no rebuild)

1. `plugins.disabled: [kanban]` → `plugins.disabled: []` in `$LOCALAPPDATA/hermes/config.yaml`
   (backup: `config.yaml.bak-kanban-restore-2026-08-13`). The bundled plugin
   v1.0.0 is compatible with runtime v0.20.0 — no version mismatch (no STOP needed).
2. Restarted the machine dashboard (killed listener 47152 tree; relaunched
   `hermes dashboard --skip-build --no-open`) → plugin APIs mounted.

Left untouched: `disabled_toolsets: kanban` (agent-toolset isolation; profiles
that use the board override it), per-profile `plugins.disabled: [kanban]` in
capcmd/fxtrading/notebooklm/antigravity-orchestrator/close-system-learning-lab/
org-macro-strategist (intentional per-profile isolation — their dashboards may
hide the tab; the Capital Intelligence board is iip-scoped).

## 3. Acceptance (playwright headless chromium, port 9119, profile=iip)

| Criterion | Result |
|---|---|
| Dashboard nav visibly contains Kanban | ✅ (`…, Documentation, **Kanban**, Achievements`) |
| Kanban tab opens without console error | ✅ URL `/kanban?profile=iip`; console errors **0** |
| Board selector → Capital Intelligence / iip | ✅ header "Capital Intelligence · 68"; switcher lists `iip` |
| Native statuses render | ✅ Triage0+ Todo0+ Scheduled0+ Ready0+ In Progress0+ **Blocked5+** Review0+ **Done63+** |
| Tasks agree with `hermes kanban list/show` | ✅ Blocked 5 = t_51e3be79 [GATE] 0004, t_2342aa1d [GATE] 0012, t_8411623f 0016, t_d5019196 0017, t_1ecfaaef pilot-fail (identical to CLI); Done 63 |
| Live event updates | ✅ `/events` WebSocket OPEN; task_events streaming (created/claimed/attached) |
| No duplicate DB/state source | ✅ plugin wraps `hermes_cli.kanban_db` — same tables/keys as CLI + gateway |
| board `other` untouched / Stage 8 HOLD | ✅ read-only verification only |

Evidence: `dashboard-kanban-after.png`, `kanban-board-full.png` (this dir),
plugin discovery = `/api/dashboard/plugins` → `['hermes-achievements','kanban']`
(after rescan).

<!-- 2026-08-13 17:04 UTC+7 (artifact_timestamp.py) -->
