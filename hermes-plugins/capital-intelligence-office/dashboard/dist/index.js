/**
 * Capital Intelligence Live Office — Hermes Dashboard Plugin (v1.0.0)
 *
 * Pure READ-ONLY projection of the Hermes Capital Intelligence board.
 * Plain IIFE, no build step — uses window.__HERMES_PLUGIN_SDK__ (React +
 * shadcn primitives) exactly like the bundled kanban plugin.
 *
 * Never fabricates states: on API/WS failure the office renders DEGRADED /
 * UNKNOWN. Owns no state, writes nothing.
 */
(function () {
  "use strict";

  const SDK = window.__HERMES_PLUGIN_SDK__;
  if (!SDK) return;

  const { React } = SDK;
  const h = React.createElement;
  const { Card, CardContent, Badge } = SDK.components;
  const { useState, useEffect, useCallback, useRef } = SDK.hooks;
  const { timeAgo } = SDK.utils || {};

  const API = "/api/plugins/capital-intelligence-office";

  const STATE_META = {
    awaiting_founder: { label: "Awaiting Founder", cls: "co-state co-state--founder" },
    working: { label: "Working", cls: "co-state co-state--working" },
    blocked: { label: "Blocked", cls: "co-state co-state--blocked" },
    reviewing: { label: "Reviewing", cls: "co-state co-state--reviewing" },
    queued: { label: "Queued", cls: "co-state co-state--queued" },
    idle: { label: "Idle", cls: "co-state co-state--idle" },
    unknown: { label: "Unknown", cls: "co-state co-state--unknown" },
  };

  // Authed fetch — prefer SDK.fetchJSON (returns parsed JSON; proven by the
  // bundled kanban plugin). SDK.authedFetch returns a raw Response object in
  // this runtime, so it is a fallback only.
  function authedFetch(url) {
    if (typeof SDK.fetchJSON === "function") return SDK.fetchJSON(url);
    if (typeof SDK.authedFetch === "function") return SDK.authedFetch(url);
    const token = window.__HERMES_SESSION_TOKEN__ || "";
    const headers = token ? { Authorization: "Bearer " + token } : {};
    return fetch(url, { headers }).then(function (r) {
      if (!r.ok) throw new Error(r.status + ": " + r.statusText);
      return r.json();
    });
  }

  // Defensive list guard: missing/odd API shapes must never crash the office
  // (charter F — degrade to empty/Unknown, never fabricate).
  function safeList(v) { return Array.isArray(v) ? v : []; }
  function safeObj(v) { return v && typeof v === "object" ? v : {}; }

  function buildWsUrl() {
    const token = window.__HERMES_SESSION_TOKEN__ || "";
    const base = (location.protocol === "https:" ? "wss://" : "ws://") + location.host;
    return base + API + "/events?token=" + encodeURIComponent(token);
  }

  function fmtTime(ts) {
    if (!ts) return "—";
    const d = new Date(ts * 1000);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function DeskCard({ desk }) {
    const meta = STATE_META[desk.state] || STATE_META.unknown;
    const cur = desk.current_task;
    return h(Card, { className: "co-desk" },
      h("div", { className: "co-desk-top" },
        h("span", { className: "co-desk-role" }, desk.role),
        h(Badge, { className: meta.cls }, meta.label)),
      h(CardContent, { className: "co-desk-body" },
        h("div", { className: "co-desk-task", title: cur ? cur.title : "" },
          cur ? (cur.title.length > 60 ? cur.title.slice(0, 60) + "…" : cur.title)
              : (desk.state === "idle" ? "No open work" : "—")),
        h("div", { className: "co-desk-meta" },
          h("span", null, "open: " + desk.open_count),
          h("span", null, "worker: " + (desk.active_worker ? "active" : "idle")),
          h("span", null, "last: " + fmtTime(desk.last_activity)))),
      h("div", { className: "co-desk-bar " + meta.cls.replace("co-state", "co-desk-bar") }));
  }

  function FounderRow({ item }) {
    return h("div", { className: "co-founder-row" },
      h("span", { className: "co-founder-gate" }, item.gate === "founder_decision" ? "FOUNDER DECISION" : "REVIEW"),
      h("span", { className: "co-founder-title", title: item.title }, item.title),
      h("span", { className: "co-founder-desk" }, item.desk),
      h("span", { className: "co-founder-reason" }, item.block_reason || ""));
  }

  function CapitalOfficePage() {
    const [health, setHealth] = useState(null);
    const [desks, setDesks] = useState([]);
    const [founder, setFounder] = useState([]);
    const [activity, setActivity] = useState([]);
    const [workers, setWorkers] = useState([]);
    const [degraded, setDegraded] = useState(false);
    const [lastEvent, setLastEvent] = useState(null);
    const wsRef = useRef(null);

    const refresh = useCallback(function () {
      return Promise.all([
        authedFetch(API + "/health").catch(function () { return null; }),
        authedFetch(API + "/desks").catch(function () { return null; }),
        authedFetch(API + "/founder-attention").catch(function () { return null; }),
        authedFetch(API + "/activity?limit=12").catch(function () { return null; }),
        authedFetch(API + "/workers?limit=6").catch(function () { return null; }),
      ]).then(function (res) {
        const ok = res[0] && res[1];
        setHealth(safeObj(res[0]));
        setDesks(safeList(res[1] && res[1].desks));
        setFounder(safeList(res[2] && res[2].items));
        setActivity(safeList(res[3] && res[3].items));
        setWorkers(safeList(res[4] && res[4].items));
        setDegraded(!ok);
      });
    }, []);

    useEffect(function () {
      refresh();
      let ws;
      let closed = false;
      function connect() {
        if (closed) return;
        ws = new WebSocket(buildWsUrl());
        wsRef.current = ws;
        ws.onopen = function () { setDegraded(false); };
        ws.onmessage = function (ev) {
          try {
            const msg = JSON.parse(ev.data);
            if (msg.events && msg.events.length) {
              setLastEvent(msg.events[msg.events.length - 1]);
              refresh();
            }
          } catch (e) { /* ignore malformed */ }
        };
        ws.onclose = function () {
          if (!closed) setTimeout(connect, 3000);
        };
        ws.onerror = function () { setDegraded(true); };
      }
      connect();
      return function () { closed = true; if (ws) ws.close(); };
    }, [refresh]);

    const hc = safeObj(health);
    const statusCounts = safeObj(hc.task_counts);
    const sum = Object.keys(statusCounts).reduce(function (a, k) { return a + statusCounts[k]; }, 0);
    const founderList = safeList(founder);
    const desksList = safeList(desks);
    const activityList = safeList(activity);
    const workersList = safeList(workers);

    return h("div", { className: "co-office" },
      h("div", { className: "co-header" },
        h("div", { className: "co-title-row" },
          h("span", { className: "co-title" }, "Capital Intelligence Live Office"),
          degraded
            ? h(Badge, { className: "co-state co-state--unknown" }, "DEGRADED — data source unavailable")
            : h(Badge, { className: "co-state co-state--working" }, "LIVE · " + (hc.board_name || hc.board || "iip")),
        h("div", { className: "co-sub" },
          "source: " + (hc.data_source || "hermes_kanban_board") +
          " · tasks: " + sum + " · active runs: " + (hc.active_runs ?? "—") +
          (lastEvent ? " · last event: " + lastEvent.kind + " " + fmtTime(lastEvent.created_at) : ""))),

      // Founder attention area
      h("div", { className: "co-founder" },
        h("div", { className: "co-founder-head" }, "Founder Desk — Awaiting Human Attention"),
        founderList.length === 0
          ? h("div", { className: "co-founder-empty" }, degraded ? "Unavailable" : "Nothing awaiting you")
          : founderList.map(function (it) { return h(FounderRow, { key: it.task_id, item: it }); })),

      // 11-desk office floor
      h("div", { className: "co-floor" },
        desksList.map(function (d) { return h(DeskCard, { key: d.profile, desk: d }); })),

      // activity + workers strip
      h("div", { className: "co-strips" },
        h("div", { className: "co-strip" },
          h("div", { className: "co-strip-head" }, "Recent Activity"),
          activityList.length === 0
            ? h("div", { className: "co-muted" }, degraded ? "Unavailable" : "No recent events")
            : activityList.slice(0, 8).map(function (e) {
                return h("div", { key: e.id, className: "co-act-row" },
                  h("span", { className: "co-act-kind" }, e.kind),
                  h("span", { className: "co-act-title", title: e.task_title || e.task_id },
                    (e.task_title || e.task_id || "").slice(0, 50)),
                  h("span", { className: "co-act-time" }, fmtTime(e.created_at)));
              })),
        h("div", { className: "co-strip" },
          h("div", { className: "co-strip-head" }, "Workers / Runs"),
          workersList.length === 0
            ? h("div", { className: "co-muted" }, degraded ? "Unavailable" : "No recent runs")
            : workersList.map(function (w) {
                return h("div", { key: w.run_id, className: "co-act-row" },
                  h("span", { className: "co-act-kind" }, w.status),
                  h("span", { className: "co-act-title", title: w.task_title || w.task_id },
                    (w.profile || "") + " · " + (w.task_title || w.task_id || "").slice(0, 40)),
                  h("span", { className: "co-act-time" }, fmtTime(w.started_at)));
              })))));
  }

  if (window.__HERMES_PLUGINS__ && typeof window.__HERMES_PLUGINS__.register === "function") {
    window.__HERMES_PLUGINS__.register("capital-intelligence-office", CapitalOfficePage);
  }
})();
