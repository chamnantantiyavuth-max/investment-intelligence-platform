/**
 * Capital Intelligence Live Office — Phase 2: Spatial Office (v1.1.0)
 *
 * Read-only projection of the Hermes Capital Intelligence board, rendered as
 * a virtual office floor: Founder Desk centerpiece, 11 role desks with
 * pixel-style avatars, presentation-state visuals, minimal event-tied
 * animations, real task-link handoff lines, compact activity rail.
 *
 * Animations are tied ONLY to real Hermes state/events. No random movement.
 * On data-source failure the office renders DEGRADED — never fabricates.
 */
(function () {
  "use strict";

  const SDK = window.__HERMES_PLUGIN_SDK__;
  if (!SDK) return;

  const { React } = SDK;
  const h = React.createElement;
  const { Card, CardContent } = SDK.components;
  const { useState, useEffect, useCallback, useRef } = SDK.hooks;

  const API = "/api/plugins/capital-intelligence-office";

  const STATE_META = {
    awaiting_founder: { label: "Awaiting Founder", cls: "co-st co-st--founder", icon: "DOC" },
    working: { label: "Working", cls: "co-st co-st--working", icon: "TYPING" },
    blocked: { label: "Blocked", cls: "co-st co-st--blocked", icon: "WARN" },
    reviewing: { label: "Reviewing", cls: "co-st co-st--reviewing", icon: "REVIEW" },
    queued: { label: "Queued", cls: "co-st co-st--queued", icon: "QUEUE" },
    recently_completed: { label: "Recently Completed", cls: "co-st co-st--done", icon: "CHECK" },
    idle: { label: "Idle", cls: "co-st co-st--idle", icon: "IDLE" },
    error: { label: "Error", cls: "co-st co-st--error", icon: "ALERT" },
    unknown: { label: "Unknown", cls: "co-st co-st--unknown", icon: "UNK" },
    unavailable: { label: "Not Installed", cls: "co-st co-st--unknown", icon: "UNK" },
  };

  // Role identity (color + simple pixel glyph index) — original CSS/SVG art.
  const ROLE_META = {
    "Chief of Staff": { color: "#818cf8", glyph: "COS" },
    "IC Secretary": { color: "#c084fc", glyph: "IC" },
    "Commodity Analyst": { color: "#fbbf24", glyph: "COMM" },
    "Macro Strategist": { color: "#38bdf8", glyph: "MACRO" },
    "Equity Alpha Analyst": { color: "#34d399", glyph: "EQ" },
    "Options Strategist": { color: "#2dd4bf", glyph: "OPT" },
    "Chief Risk Officer": { color: "#fb7185", glyph: "CRO" },
    "Quant / Model Validator": { color: "#22d3ee", glyph: "QUANT" },
    "Data Steward": { color: "#a3e635", glyph: "DATA" },
    "Internal Auditor": { color: "#fb923c", glyph: "AUDIT" },
    "Radar Scout": { color: "#e879f9", glyph: "RADAR" },
  };

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

  // ---------------------------------------------------------------------
  // Pixel-style avatar (original SVG, 16x20 grid-ish, role color)
  // ---------------------------------------------------------------------
  function PixelAvatar({ role, stateCls }) {
    const meta = ROLE_META[role] || { color: "#94a3b8" };
    const c = meta.color;
    return h("svg", { viewBox: "0 0 24 28", className: "co-avatar", width: 34, height: 40 },
      // head (pixel block)
      h("rect", { x: 8, y: 2, width: 8, height: 8, rx: 1, fill: c, opacity: 0.92 }),
      // shoulders
      h("rect", { x: 5, y: 11, width: 14, height: 5, rx: 1, fill: c, opacity: 0.75 }),
      // torso
      h("rect", { x: 7, y: 17, width: 10, height: 8, rx: 1, fill: c, opacity: 0.55 }),
      // desk line under
      h("rect", { x: 3, y: 26, width: 18, height: 1.6, rx: 0.8, fill: "#334155" }));
  }

  function StateIcon({ state, cls }) {
    const meta = STATE_META[state] || STATE_META.unknown;
    const common = { className: "co-stateicon " + cls };
    switch (meta.icon) {
      case "DOC": return h("span", common, "◈");
      case "TYPING": return h("span", { className: "co-typing " + cls },
        h("i", null), h("i", null), h("i", null));
      case "WARN": return h("span", common, "⚠");
      case "ALERT": return h("span", common, "✕");
      case "CHECK": return h("span", common, "✓");
      case "REVIEW": return h("span", common, "◐");
      case "QUEUE": return h("span", common, "▤");
      case "IDLE": return h("span", common, "·");
      default: return h("span", common, "?");
    }
  }

  // ---------------------------------------------------------------------
  // Desk card — at-a-glance on the floor
  // ---------------------------------------------------------------------
  function DeskCell({ desk }) {
    const meta = STATE_META[desk.state] || STATE_META.unknown;
    const cur = desk.current_task;
    const diag = desk.diagnostics || {};
    const diagCount = Object.keys(diag).length
      ? Object.keys(diag).map(function (k) { return k + ":" + diag[k]; }).join(" ") : null;
    const tooltip = [
      desk.role, " — " + meta.label,
      cur ? (" · " + cur.title) : "",
      " · open " + desk.open_count + (desk.active_worker ? " · worker active" : ""),
      diagCount ? (" · DIAG " + diagCount) : "",
    ].join("");

    return h("div", {
      className: "co-desk st-" + desk.state,
      title: tooltip,
    },
      h("div", { className: "co-desk-lamp " + meta.cls }, ""),
      h(PixelAvatar, { role: desk.role, stateCls: meta.cls }),
      h(StateIcon, { state: desk.state, cls: meta.cls }),
      h("div", { className: "co-desk-info" },
        h("div", { className: "co-desk-role" }, desk.role),
        h("div", { className: "co-desk-badge " + meta.cls }, meta.label),
        h("div", { className: "co-desk-meta" },
          h("span", null, "open " + desk.open_count),
          h("span", null, desk.active_worker ? "●" : "○"),
          h("span", null, fmtTime(desk.last_activity)),
          diagCount ? h("span", { className: "co-desk-diag", title: "diagnostics layer (pilot/test residue)" }, "DIAG " + diagCount) : null)));
  }

  // ---------------------------------------------------------------------
  // Founder Desk — centerpiece
  // ---------------------------------------------------------------------
  function FounderDesk({ items, degraded }) {
    const list = safeList(items);
    return h(Card, { className: "co-founder" },
      h(CardContent, { className: "co-founder-body" },
        h("div", { className: "co-founder-emblem" }, "◉"),
        h("div", { className: "co-founder-main" },
          h("div", { className: "co-founder-head" }, "FOUNDER DESK"),
          h("div", { className: "co-founder-count" },
            list.length ? (list.length + " decision" + (list.length > 1 ? "s" : "") + " waiting") : "Nothing awaiting")),
        h("div", { className: "co-founder-list" },
          list.length === 0
            ? h("div", { className: "co-founder-empty" }, degraded ? "Unavailable" : "—")
            : list.map(function (it) {
                return h("div", { key: it.task_id, className: "co-founder-row",
                    title: it.title },
                  h("span", { className: "co-founder-gate" }, it.gate === "founder_decision" ? "DECISION" : "REVIEW"),
                  h("span", { className: "co-founder-title" }, it.title.length > 70 ? it.title.slice(0, 70) + "…" : it.title),
                  h("span", { className: "co-founder-desk" }, it.desk));
              }))));
  }

  // ---------------------------------------------------------------------
  // Main office component
  // ---------------------------------------------------------------------
  function CapitalOfficePage() {
    const [health, setHealth] = useState({});
    const [desks, setDesks] = useState([]);
    const [founder, setFounder] = useState([]);
    const [activity, setActivity] = useState([]);
    const [workers, setWorkers] = useState([]);
    const [handoffs, setHandoffs] = useState([]);
    const [degraded, setDegraded] = useState(false);
    const [railOpen, setRailOpen] = useState(false);
    const [lastEvent, setLastEvent] = useState(null);
    const [pulseEdge, setPulseEdge] = useState(null);
    const floorRef = useRef(null);
    const [lines, setLines] = useState([]);
    const [showHistory, setShowHistory] = useState(false);
    const [handoffCount, setHandoffCount] = useState(0);
    const showHistoryRef = useRef(false);

    const refresh = useCallback(function () {
      const scopeQ = showHistoryRef.current ? "all" : "active";
      return Promise.all([
        authedFetch(API + "/health").catch(function () { return null; }),
        authedFetch(API + "/desks").catch(function () { return null; }),
        authedFetch(API + "/founder-attention").catch(function () { return null; }),
        authedFetch(API + "/activity?limit=14").catch(function () { return null; }),
        authedFetch(API + "/workers?limit=8").catch(function () { return null; }),
        authedFetch(API + "/handoffs?scope=" + scopeQ).catch(function () { return null; }),
      ]).then(function (res) {
        const ok = res[0] && res[1];
        setHealth(safeObj(res[0]));
        setDesks(safeList(res[1] && res[1].desks));
        setFounder(safeList(res[2] && res[2].items));
        setActivity(safeList(res[3] && res[3].items));
        setWorkers(safeList(res[4] && res[4].items));
        setHandoffs(safeList(res[5] && res[5].items));
        setHandoffCount(res[5] && typeof res[5].historical_count === "number"
          ? res[5].historical_count : 0);
        setDegraded(!ok);
      });
    }, []);

    // WS: live updates + pulse the handoff edge when a child task spawns/links
    useEffect(function () {
      refresh();
      let ws, closed = false;
      function connect() {
        if (closed) return;
        ws = new WebSocket(buildWsUrl());
        ws.onopen = function () { setDegraded(false); };
        ws.onmessage = function (ev) {
          try {
            const msg = JSON.parse(ev.data);
            if (msg.events && msg.events.length) {
              const last = msg.events[msg.events.length - 1];
              setLastEvent(last);
              if (last.kind === "spawned" || last.kind === "linked" || last.kind === "created") {
                setPulseEdge(last.task_id);
                setTimeout(function () { setPulseEdge(null); }, 3000);
              }
              refresh();
            }
          } catch (e) { /* ignore */ }
        };
        ws.onclose = function () { if (!closed) setTimeout(connect, 3000); };
        ws.onerror = function () { setDegraded(true); };
      }
      connect();
      return function () { closed = true; if (ws) ws.close(); };
    }, [refresh]);

    // Measure desk positions -> handoff SVG lines (real task-link edges only).
    // useEffect (not useLayoutEffect — not exposed by this SDK runtime).
    useEffect(function () {
      const floor = floorRef.current;
      if (!floor) return;
      const deskEls = floor.querySelectorAll("[data-profile]");
      const pos = {};
      deskEls.forEach(function (el) {
        const r = el.getBoundingClientRect();
        const fr = floor.getBoundingClientRect();
        pos[el.getAttribute("data-profile")] = {
          x: r.left - fr.left + r.width / 2,
          y: r.top - fr.top + r.height / 2,
        };
      });
      const drawn = [];
      safeList(handoffs).forEach(function (e) {
        const a = pos[e.from], b = pos[e.to];
        if (a && b) {
          const hist = e.class === "historical";
          drawn.push({ x1: a.x, y1: a.y, x2: b.x, y2: b.y,
            from: e.from_role, to: e.to_role, task_ids: e.task_ids,
            cls: e.class || "active",
            // packet animation ONLY when the event maps to an ACTIVE/RECENT edge
            active: !hist && pulseEdge && e.task_ids.indexOf(pulseEdge) >= 0 });
        }
      });
      setLines(drawn);
    }, [handoffs, pulseEdge, desks]);

    const hc = safeObj(health);
    const statusCounts = safeObj(hc.task_counts);
    const sum = Object.keys(statusCounts).reduce(function (a, k) { return a + statusCounts[k]; }, 0);
    const desksList = safeList(desks);
    const founderList = safeList(founder);
    const activityList = safeList(activity);
    const workersList = safeList(workers);

    // spatial floor — desk placement by profile (per Founder sketch)
    const byProfile = {};
    desksList.forEach(function (d) { byProfile[d.profile] = d; });
    function cell(profile, extraCls) {
      const d = byProfile[profile];
      return d ? h("div", { className: "co-desk " + extraCls, "data-profile": d.profile, key: d.profile },
        h(DeskCell, { desk: d })) : null;
    }

    return h("div", { className: "co-office" },
      h("div", { className: "co-header" },
        h("div", { className: "co-title-row" },
          h("span", { className: "co-title" }, "Capital Intelligence Live Office"),
          degraded
            ? h("span", { className: "co-live co-live--down" }, "DEGRADED — data source unavailable")
            : h("span", { className: "co-live co-live--up" }, "LIVE · " + (hc.board_name || hc.board || "iip"))),
        h("div", { className: "co-sub" },
          "source: " + (hc.data_source || "hermes_kanban_board") +
          " · tasks: " + sum + " · runs: " + (hc.active_runs ?? "—") +
          (lastEvent ? " · " + lastEvent.kind + " " + fmtTime(lastEvent.created_at) : ""))),

      h("div", { className: "co-floor-wrap" },
        h("div", { className: "co-floor", ref: floorRef },
          h("svg", { className: "co-handoff-lines" },
            lines.map(function (l, i) {
              return h("g", { key: i },
                h("line", { x1: l.x1, y1: l.y1, x2: l.x2, y2: l.y2,
                  className: "co-handoff-line"
                    + (l.cls === "recent" ? " co-handoff-line--recent" : "")
                    + (l.active ? " co-handoff-line--active" : "") }),
                l.active && h("circle", { className: "co-handoff-packet", cx: l.x1, cy: l.y1, r: 3 }));
            })),
          h(FounderDesk, { items: founderList, degraded: degraded }),
          h("div", { className: "co-row co-row--cos" }, cell("org-cos", "co-desk--center")),
          h("div", { className: "co-row co-row--analysts" },
            cell("org-commodity-analyst"), cell("org-macro-strategist"), cell("org-equity-analyst")),
          h("div", { className: "co-row co-row--support" },
            cell("org-options-strategist"), cell("org-quant-validator"), cell("org-data-steward")),
          h("div", { className: "co-row co-row--ic" }, cell("org-ic-secretary", "co-desk--center")),
          h("div", { className: "co-row co-row--review" },
            cell("org-cro"), cell("org-auditor")),
          h("div", { className: "co-row co-row--radar" }, cell("org-radar-scout", "co-desk--wide")))),

      // compact observability rail
      h("div", { className: "co-rail" },
        h("button", { className: "co-rail-toggle", onClick: function () { setRailOpen(!railOpen); } },
          railOpen ? "▾ Activity & Runs" : "▸ Activity & Runs"),
        h("label", { className: "co-rail-history",
            title: "Recorded task-links that are neither open nor recently active — shown for reference only" },
          h("input", { type: "checkbox", checked: showHistory,
            onChange: function () {
              showHistoryRef.current = !showHistory;
              setShowHistory(!showHistory);
              refresh();
            } }),
          " Handoff history (" + handoffCount + ")"),
        railOpen && h("div", { className: "co-rail-body" },
          h("div", { className: "co-rail-col" },
            h("div", { className: "co-rail-head" }, "Recent Activity"),
            activityList.length === 0
              ? h("div", { className: "co-muted" }, degraded ? "Unavailable" : "—")
              : activityList.slice(0, 10).map(function (e) {
                  return h("div", { key: e.id, className: "co-act-row", title: e.task_title || e.task_id },
                    h("span", { className: "co-act-kind" }, e.kind),
                    h("span", { className: "co-act-title" }, (e.task_title || e.task_id || "").slice(0, 42)),
                    h("span", { className: "co-act-time" }, fmtTime(e.created_at)));
                })),
          h("div", { className: "co-rail-col" },
            h("div", { className: "co-rail-head" }, "Workers / Runs"),
            workersList.length === 0
              ? h("div", { className: "co-muted" }, degraded ? "Unavailable" : "—")
              : workersList.map(function (w) {
                  return h("div", { key: w.run_id, className: "co-act-row", title: w.task_title || w.task_id },
                    h("span", { className: "co-act-kind" }, w.status),
                    h("span", { className: "co-act-title" }, (w.profile || "") + " · " + (w.task_title || w.task_id || "").slice(0, 30)),
                    h("span", { className: "co-act-time" }, fmtTime(w.started_at)));
                })))));
  }

  if (window.__HERMES_PLUGINS__ && typeof window.__HERMES_PLUGINS__.register === "function") {
    window.__HERMES_PLUGINS__.register("capital-intelligence-office", CapitalOfficePage);
  }
})();
