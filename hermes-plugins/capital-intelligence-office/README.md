# Capital Intelligence Live Office v1 — Hermes Dashboard plugin

Read-only live projection of the Hermes Capital Intelligence board: 11
organizational desks, Founder attention area, recent activity, worker/run
health. Owns NO organizational state; writes NOTHING.

## Layout

```
hermes-plugins/capital-intelligence-office/
├── LIVE-OFFICE-SOURCE-MAP.md   charter §3 source map (UI → source → rule → degraded)
└── dashboard/
    ├── manifest.json           plugin manifest (tab /capital-office, after:kanban)
    ├── plugin_api.py           READ-ONLY backend (health/desks/founder-attention/activity/workers + /events WS)
    └── dist/
        ├── index.js            plain IIFE via window.__HERMES_PLUGIN_SDK__
        └── style.css
```

## Install (this machine — user/dashboard plugin mechanism)

```bash
# source lives in this repo; installed copy in the Hermes user plugins dir:
cp -r hermes-plugins/capital-intelligence-office \
      "$LOCALAPPDATA/hermes/plugins/capital-intelligence-office"
# enable the user plugin (plugins.enabled) in $LOCALAPPDATA/hermes/config.yaml
# restart the dashboard:
unset HERMES_DESKTOP HERMES_WEB_DIST
hermes dashboard --skip-build --no-open
```

## Read-only guarantees

- Backend: GET + WS only (no POST/PUT/PATCH/DELETE anywhere in plugin_api.py).
- No tables/files/state created — every response derived per request from
  `hermes_cli.kanban_db` (same supported path as CLI/gateway).
- Frontend: fetch + WebSocket only; never reads SQLite.
- Failure: DEGRADED / UNKNOWN banner — no fabricated Working/Idle.

## Verification (first checkpoint)

See `evidence/ui/live-office-v1/LIVE-OFFICE-V1-CHECKPOINT-2026-08-13.md` (Phase -1)
and `evidence/ui/live-office-plugin/` (this feature's checkpoint evidence).

<!-- 2026-08-13 17:20 UTC+7 (artifact_timestamp.py) -->
