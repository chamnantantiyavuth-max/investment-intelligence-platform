/**
 * Capital Intelligence Live Office — Phase 3: Visual Polish / Living Office (v1.2.0)
 *
 * Read-only projection of the Hermes Capital Intelligence board, rendered as
 * a living pixel office: Founder Office focal point, pod zones (Research /
 * Intelligence / Review-Control / External Sensing), role-distinct pixel
 * avatars, truthful state-tied animations, real task-link handoffs with
 * Phase-2.1 semantics (ACTIVE / RECENT / HISTORICAL), compact observability
 * rail, and a read-only agent detail drawer.
 *
 * LOGIC FREEZE (Founder, 2026-08-13): data/state semantics are frozen —
 * this file only changes PRESENTATION. Animations are tied ONLY to real
 * Hermes state/events. Zero active handoffs => zero lines (no fake
 * coordination to look busy). On data-source failure the office renders
 * DEGRADED — never fabricates.
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

  // Role identity: color + workstation motif (original pixel art, no third-party).
  const ROLE_META = {
    "Chief of Staff": { color: "#818cf8", glyph: "COS", motif: "hub" },
    "IC Secretary": { color: "#c084fc", glyph: "IC", motif: "docs" },
    "Commodity Analyst": { color: "#fbbf24", glyph: "COMM", motif: "barrel" },
    "Macro Strategist": { color: "#38bdf8", glyph: "MACRO", motif: "globe" },
    "Equity Alpha Analyst": { color: "#34d399", glyph: "EQ", motif: "chart" },
    "Options Strategist": { color: "#2dd4bf", glyph: "OPT", motif: "candles" },
    "Chief Risk Officer": { color: "#fb7185", glyph: "CRO", motif: "shield" },
    "Quant / Model Validator": { color: "#22d3ee", glyph: "QUANT", motif: "monitors" },
    "Data Steward": { color: "#a3e635", glyph: "DATA", motif: "rack" },
    "Internal Auditor": { color: "#fb923c", glyph: "AUDIT", motif: "audit" },
    "Radar Scout": { color: "#e879f9", glyph: "RADAR", motif: "radar" },
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
  // Workstation motifs — original pixel SVG per role (monitor/server/radar…)
  // ---------------------------------------------------------------------
  function Motif({ motif, color }) {
    const c = color || "#94a3b8";
    const common = { viewBox: "0 0 32 20", className: "co-motif", width: 34, height: 20 };
    switch (motif) {
      case "monitors": // Quant — dual screens
        return h("svg", common,
          h("rect", { x: 1, y: 2, width: 13, height: 10, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("line", { x1: 3, y1: 5, x2: 12, y2: 5, stroke: c, strokeWidth: 1.4 }),
          h("line", { x1: 3, y1: 8, x2: 9, y2: 8, stroke: c, strokeWidth: 1.4, opacity: 0.6 }),
          h("rect", { x: 17, y: 2, width: 13, height: 10, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("path", { d: "M19 4 L23 8 L26 6 L29 9", stroke: c, strokeWidth: 1.3, fill: "none" }),
          h("line", { x1: 7, y1: 12, x2: 7, y2: 16, stroke: c, strokeWidth: 1.4 }),
          h("line", { x1: 24, y1: 12, x2: 24, y2: 16, stroke: c, strokeWidth: 1.4 }));
      case "rack": // Data — server stack
        return h("svg", common,
          h("rect", { x: 6, y: 1, width: 20, height: 5, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("circle", { cx: 10, cy: 3.5, r: 1.1, fill: c }),
          h("rect", { x: 6, y: 7, width: 20, height: 5, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("circle", { cx: 10, cy: 9.5, r: 1.1, fill: c }),
          h("rect", { x: 6, y: 13, width: 20, height: 5, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("circle", { cx: 10, cy: 15.5, r: 1.1, fill: c, opacity: 0.5 }));
      case "radar": // Radar Scout — dish + sweep
        return h("svg", common,
          h("path", { d: "M4 17 A 12 12 0 0 1 28 17", stroke: c, strokeWidth: 1.4, fill: "none" }),
          h("line", { x1: 16, y1: 17, x2: 23, y2: 8, stroke: c, strokeWidth: 1.3 }),
          h("line", { x1: 16, y1: 17, x2: 16, y2: 6, stroke: c, strokeWidth: 1.1, opacity: 0.55 }),
          h("circle", { cx: 16, cy: 17, r: 1.6, fill: c }));
      case "shield": // CRO — risk shield
        return h("svg", common,
          h("path", { d: "M16 1 L27 5 V12 C27 16.5 22.5 19.5 16 21 C9.5 19.5 5 16.5 5 12 V5 Z", fill: "#0f172a", stroke: c, strokeWidth: 1.3 }),
          h("line", { x1: 11, y1: 11, x2: 15, y2: 15, stroke: c, strokeWidth: 1.6 }),
          h("line", { x1: 21, y1: 11, x2: 15, y2: 15, stroke: c, strokeWidth: 1.6 }),
          h("line", { x1: 12, y1: 8, x2: 20, y2: 8, stroke: c, strokeWidth: 1.2, opacity: 0.5 }));
      case "audit": // Auditor — magnifier + checklist
        return h("svg", common,
          h("circle", { cx: 12, cy: 9, r: 6, fill: "#0f172a", stroke: c, strokeWidth: 1.3 }),
          h("line", { x1: 16.5, y1: 13.5, x2: 21, y2: 18, stroke: c, strokeWidth: 1.6 }),
          h("rect", { x: 22, y: 4, width: 8, height: 12, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.1 }),
          h("line", { x1: 24, y1: 8, x2: 28, y2: 8, stroke: c, strokeWidth: 1.2, opacity: 0.7 }),
          h("line", { x1: 24, y1: 11, x2: 27, y2: 11, stroke: c, strokeWidth: 1.2, opacity: 0.5 }));
      case "docs": // IC Secretary — document stack
        return h("svg", common,
          h("rect", { x: 8, y: 4, width: 17, height: 12, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }),
          h("line", { x1: 11, y1: 8, x2: 22, y2: 8, stroke: c, strokeWidth: 1.2 }),
          h("line", { x1: 11, y1: 11, x2: 19, y2: 11, stroke: c, strokeWidth: 1.2, opacity: 0.6 }),
          h("rect", { x: 5, y: 8, width: 17, height: 12, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.1, opacity: 0.55 }));
      case "hub": // CoS — coordination hub (headset + signal)
        return h("svg", common,
          h("circle", { cx: 16, cy: 9, r: 6, fill: "#0f172a", stroke: c, strokeWidth: 1.3 }),
          h("path", { d: "M10 9 V12 a6 6 0 0 0 12 0 V9", stroke: c, strokeWidth: 1.4, fill: "none" }),
          h("line", { x1: 16, y1: 15, x2: 16, y2: 18, stroke: c, strokeWidth: 1.4 }),
          h("circle", { cx: 16, cy: 19, r: 1.4, fill: c }));
      case "globe": // Macro — globe
        return h("svg", common,
          h("circle", { cx: 16, cy: 10, r: 8, fill: "#0f172a", stroke: c, strokeWidth: 1.3 }),
          h("ellipse", { cx: 16, cy: 10, rx: 3.4, ry: 8, stroke: c, strokeWidth: 1, fill: "none", opacity: 0.7 }),
          h("line", { x1: 8, y1: 10, x2: 24, y2: 10, stroke: c, strokeWidth: 1, opacity: 0.7 }));
      case "barrel": // Commodity — barrel
        return h("svg", common,
          h("path", { d: "M9 3 h14 v13 a7 7 0 0 1 -14 0 Z", fill: "#0f172a", stroke: c, strokeWidth: 1.3 }),
          h("line", { x1: 9, y1: 9, x2: 23, y2: 9, stroke: c, strokeWidth: 1.3 }),
          h("line", { x1: 10, y1: 13, x2: 22, y2: 13, stroke: c, strokeWidth: 1, opacity: 0.5 }));
      case "chart": // Equity — ascending chart
        return h("svg", common,
          h("line", { x1: 3, y1: 16, x2: 29, y2: 16, stroke: c, strokeWidth: 1.3, opacity: 0.7 }),
          h("path", { d: "M5 13 L11 9 L16 12 L21 6 L27 3", stroke: c, strokeWidth: 1.7, fill: "none" }),
          h("circle", { cx: 21, cy: 6, r: 1.5, fill: c }));
      case "candles": // Options — candles
        return h("svg", common,
          h("line", { x1: 8, y1: 4, x2: 8, y2: 16, stroke: c, strokeWidth: 1.1, opacity: 0.6 }),
          h("rect", { x: 5.5, y: 7, width: 5, height: 6, fill: c }),
          h("line", { x1: 16, y1: 2, x2: 16, y2: 18, stroke: c, strokeWidth: 1.1, opacity: 0.6 }),
          h("rect", { x: 13.5, y: 10, width: 5, height: 4, fill: "#0f172a", stroke: c, strokeWidth: 1 }),
          h("line", { x1: 24, y1: 6, x2: 24, y2: 15, stroke: c, strokeWidth: 1.1, opacity: 0.6 }),
          h("rect", { x: 21.5, y: 8, width: 5, height: 5, fill: c }));
      default:
        return h("svg", common, h("rect", { x: 8, y: 4, width: 16, height: 10, rx: 1, fill: "#0f172a", stroke: c, strokeWidth: 1.2 }));
    }
  }

  // ---------------------------------------------------------------------
  // Pixel avatar (original SVG — seated figure in role color)
  // ---------------------------------------------------------------------
  function PixelAvatar({ role }) {
    const meta = ROLE_META[role] || { color: "#94a3b8" };
    const c = meta.color;
    return h("svg", { viewBox: "0 0 24 26", className: "co-avatar", width: 24, height: 26 },
      h("rect", { x: 8, y: 1, width: 8, height: 8, rx: 1, fill: c, opacity: 0.92 }),   // head
      h("rect", { x: 5, y: 10, width: 14, height: 5, rx: 1, fill: c, opacity: 0.78 }), // shoulders
      h("rect", { x: 7, y: 16, width: 10, height: 8, rx: 1, fill: c, opacity: 0.55 })); // torso
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
  // Workstation (desk + motif + avatar + info) — the living unit
  // ---------------------------------------------------------------------
  function Workstation({ desk, onOpen }) {
    const meta = STATE_META[desk.state] || STATE_META.unknown;
    const roleMeta = ROLE_META[desk.role] || {};
    const cur = desk.current_task;
    const diag = desk.diagnostics || {};
    const diagCount = Object.keys(diag).length
      ? Object.keys(diag).map(function (k) { return k + ":" + diag[k]; }).join(" ") : null;
    const tooltip = [
      desk.role, " — " + meta.label,
      cur ? (" · " + cur.title) : "",
      " · open " + desk.open_count + (desk.active_worker ? " · worker active" : ""),
      diagCount ? (" · DIAG " + diagCount) : "",
      " · click for details",
    ].join("");

    return h("div", {
      className: "co-ws st-" + desk.state,
      "data-profile": desk.profile,
      title: tooltip,
      onClick: function () { if (onOpen) onOpen(desk); },
    },
      desk.state === "awaiting_founder"
        && h("div", { className: "co-ws-founder-chip", title: "awaiting Founder decision" }, "▲ FOUNDER"),
      h("div", { className: "co-ws-top" },
        h(Motif, { motif: roleMeta.motif, color: roleMeta.color }),
        h("div", { className: "co-ws-screen st-screen-" + desk.state }, "")),
      h("div", { className: "co-ws-mid" },
        h(PixelAvatar, { role: desk.role }),
        h(StateIcon, { state: desk.state, cls: meta.cls })),
      h("div", { className: "co-ws-desk" },
        h("div", { className: "co-ws-lamp " + meta.cls }, ""),
        h("div", { className: "co-ws-info" },
          h("div", { className: "co-desk-role" }, desk.role),
          h("div", { className: "co-desk-badge " + meta.cls }, meta.label),
          h("div", { className: "co-desk-meta" },
            h("span", null, "open " + desk.open_count),
            h("span", null, desk.active_worker ? "●" : "○"),
            h("span", null, fmtTime(desk.last_activity)),
            diagCount ? h("span", { className: "co-desk-diag", title: "diagnostics layer (pilot/test residue)" }, "DIAG " + diagCount) : null))));
  }

  // ---------------------------------------------------------------------
  // Founder Office — focal point
  // ---------------------------------------------------------------------
  function FounderOffice({ items, degraded }) {
    const list = safeList(items);
    return h("div", { className: "co-founder-office" },
      h("div", { className: "co-founder" },
        h("div", { className: "co-founder-body" },
          h("div", { className: "co-founder-emblem" }, "◉"),
          h("div", { className: "co-founder-main" },
            h("div", { className: "co-founder-head" }, "FOUNDER OFFICE"),
            h("div", { className: "co-founder-count" },
              list.length ? (list.length + " decision" + (list.length > 1 ? "s" : "") + " waiting") : "Nothing awaiting")),
          h("div", { className: "co-founder-list" },
            list.length === 0
              ? h("div", { className: "co-founder-empty" }, degraded ? "Unavailable" : "—")
              : list.map(function (it) {
                  return h("div", { key: it.task_id, className: "co-founder-row",
                      title: it.title },
                    h("span", { className: "co-founder-gate" }, it.gate === "founder_decision" ? "DECISION" : "REVIEW"),
                    h("span", { className: "co-founder-title" }, it.title.length > 64 ? it.title.slice(0, 64) + "…" : it.title),
                    h("span", { className: "co-founder-desk" }, it.desk));
                })))));
  }

  // ---------------------------------------------------------------------
  // Read-only agent detail drawer (Phase 3 §6)
  // ---------------------------------------------------------------------
  function DetailDrawer({ desk, events, edges, onClose }) {
    const meta = STATE_META[desk.state] || STATE_META.unknown;
    const roleMeta = ROLE_META[desk.role] || {};
    const cur = desk.current_task;
    const diag = desk.diagnostics || {};
    const diagCount = Object.keys(diag).length
      ? Object.keys(diag).map(function (k) { return k + ":" + diag[k]; }).join(" ") : null;
    const myEdges = safeList(edges).filter(function (e) {
      return e.from === desk.profile || e.to === desk.profile;
    });
    return h("div", { className: "co-drawer-backdrop", onClick: onClose },
      h("div", { className: "co-drawer", onClick: function (ev) { ev.stopPropagation(); } },
        h("div", { className: "co-drawer-head" },
          h("div", { className: "co-drawer-title" },
            h("span", { className: "co-drawer-dot", style: { background: roleMeta.color } }), " " + desk.role),
          h("button", { className: "co-drawer-close", onClick: onClose }, "✕")),
        h("div", { className: "co-drawer-body" },
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "profile"),
            h("span", { className: "co-drawer-v" }, desk.profile)),
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "state"),
            h("span", { className: "co-drawer-v" }, meta.label)),
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "open work"),
            h("span", { className: "co-drawer-v" }, String(desk.open_count))),
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "worker"),
            h("span", { className: "co-drawer-v" }, desk.active_worker ? "active" : "none")),
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "last activity"),
            h("span", { className: "co-drawer-v" }, fmtTime(desk.last_activity))),
          h("div", { className: "co-drawer-row" }, h("span", { className: "co-drawer-k" }, "diagnostics"),
            h("span", { className: "co-drawer-v" }, diagCount || "none")),
          cur && h("div", { className: "co-drawer-block" },
            h("div", { className: "co-drawer-k" }, "current task"),
            h("div", { className: "co-drawer-task" },
              h("span", { className: "co-drawer-v" }, cur.title),
              h("span", { className: "co-drawer-tag" }, cur.status))),
          h("div", { className: "co-drawer-block" },
            h("div", { className: "co-drawer-k" }, "handoffs"),
            myEdges.length === 0
              ? h("div", { className: "co-muted" }, "no recorded handoffs")
              : myEdges.map(function (e, i) {
                  return h("div", { key: i, className: "co-drawer-edge" },
                    h("span", { className: "co-drawer-edge-c " + (e.class === "active" ? "edge-a" : e.class === "recent" ? "edge-r" : "edge-h") }, e.class),
                    h("span", { className: "co-drawer-edge-t" },
                      e.from_role + " → " + e.to_role + " (" + e.task_ids.length + " link" + (e.task_ids.length > 1 ? "s" : "") + ")"));
                })),
          h("div", { className: "co-drawer-block" },
            h("div", { className: "co-drawer-k" }, "recent events"),
            safeList(events).length === 0
              ? h("div", { className: "co-muted" }, "no recent events")
              : safeList(events).map(function (e) {
                  return h("div", { key: e.id, className: "co-drawer-event" },
                    h("span", { className: "co-drawer-event-k" }, e.kind),
                    h("span", { className: "co-drawer-event-t" }, (e.task_title || e.task_id || "").slice(0, 46)),
                    h("span", { className: "co-drawer-event-time" }, fmtTime(e.created_at)));
                })))));
  }

  // ---------------------------------------------------------------------
  // Main office
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
    const [drawerDesk, setDrawerDesk] = useState(null);
    const [drawerEvents, setDrawerEvents] = useState([]);

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

    // WS: live updates + pulse a handoff edge when a child task spawns/links
    useEffect(function () {
      refresh();
      let ws, closed = false;
      // Phase 3.1 R1 — reconnect contract: remember the last processed event
      // cursor so a reconnect resumes from it (?since=) instead of jumping to
      // the current tail and skipping events that occurred while disconnected.
      const lastCursorRef = { current: null };
      function connect() {
        if (closed) return;
        let url = buildWsUrl();
        if (lastCursorRef.current != null) {
          url += (url.indexOf("?") >= 0 ? "&" : "?") + "since=" + lastCursorRef.current;
        }
        ws = new WebSocket(url);
        ws.onopen = function () { setDegraded(false); refresh(); }; // reconcile every (re)connect
        ws.onmessage = function (ev) {
          try {
            const msg = JSON.parse(ev.data);
            if (msg.cursor != null) lastCursorRef.current = msg.cursor;
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

    // Measure desk positions -> handoff lines + founder arrows (real state only)
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
          // draw from desk EDGE to desk EDGE (not center) so lines never hide
          // behind the workstation cards
          const R = 70;
          const dx = b.x - a.x, dy = b.y - a.y;
          const len = Math.sqrt(dx * dx + dy * dy) || 1;
          const sx = a.x + (dx / len) * R, sy = a.y + (dy / len) * R;
          const ex = b.x - (dx / len) * R, ey = b.y - (dy / len) * R;
          drawn.push({ x1: sx, y1: sy, x2: ex, y2: ey,
            from: e.from_role, to: e.to_role, task_ids: e.task_ids,
            cls: e.class || "active",
            // packet animation ONLY when the event maps to an ACTIVE/RECENT edge
            active: !hist && pulseEdge && e.task_ids.indexOf(pulseEdge) >= 0 });
        }
      });
      setLines(drawn);
    }, [handoffs, pulseEdge, desks]);

    // Detail drawer: fetch per-desk recent events (read-only)
    useEffect(function () {
      if (!drawerDesk) { setDrawerEvents([]); return; }
      let cancelled = false;
      authedFetch(API + "/activity?profile=" + encodeURIComponent(drawerDesk.profile) + "&limit=8")
        .catch(function () { return null; })
        .then(function (res) {
          if (!cancelled) setDrawerEvents(safeList(res && res.items));
        });
      return function () { cancelled = true; };
    }, [drawerDesk, activity, workers]);

    const hc = safeObj(health);
    const statusCounts = safeObj(hc.task_counts);
    const sum = Object.keys(statusCounts).reduce(function (a, k) { return a + statusCounts[k]; }, 0);
    const desksList = safeList(desks);
    const founderList = safeList(founder);
    const activityList = safeList(activity);
    const workersList = safeList(workers);

    // top summary strip — derived ONLY from existing truth
    const activeAgents = desksList.filter(function (d) { return d.active_worker; }).length;
    const runningRuns = hc.active_runs ?? 0;
    const blockedCount = desksList.filter(function (d) { return d.state === "blocked"; }).length;
    const awaitingCount = founderList.length;
    const recentKind = activityList.length ? activityList[0].kind + " " + fmtTime(activityList[0].created_at) : "—";

    // spatial floor — pod zones (per Founder Phase-3 sketch)
    const byProfile = {};
    desksList.forEach(function (d) { byProfile[d.profile] = d; });
    function ws(profile, extraCls) {
      const d = byProfile[profile];
      return d ? h("div", { className: "co-ws-slot " + (extraCls || ""), key: d.profile },
        h(Workstation, { desk: d, onOpen: function (dd) { setDrawerDesk(dd); } })) : null;
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
          " · tasks: " + sum + " · runs: " + runningRuns +
          (lastEvent ? " · " + lastEvent.kind + " " + fmtTime(lastEvent.created_at) : ""))),

      h("div", { className: "co-summary" },
        h("div", { className: "co-sum-item", title: "desks with a live worker" },
          h("span", { className: "co-sum-v" }, String(activeAgents)),
          h("span", { className: "co-sum-k" }, "Active Agents")),
        h("div", { className: "co-sum-item", title: "active runs" },
          h("span", { className: "co-sum-v" }, String(runningRuns)),
          h("span", { className: "co-sum-k" }, "Running")),
        h("div", { className: "co-sum-item co-sum--warn", title: "desks blocked (non-gate)" },
          h("span", { className: "co-sum-v" }, String(blockedCount)),
          h("span", { className: "co-sum-k" }, "Blocked")),
        h("div", { className: "co-sum-item co-sum--founder", title: "decisions awaiting Founder" },
          h("span", { className: "co-sum-v" }, String(awaitingCount)),
          h("span", { className: "co-sum-k" }, "Awaiting Founder")),
        h("div", { className: "co-sum-item co-sum--evt", title: "most recent event" },
          h("span", { className: "co-sum-v co-sum-v--sm" }, recentKind),
          h("span", { className: "co-sum-k" }, "Recent Event"))),

      h("div", { className: "co-floor-wrap" },
        h("div", { className: "co-floor", ref: floorRef },
          h("svg", { className: "co-handoff-lines" },
            lines.map(function (l, i) {
              return h("g", { key: "l" + i },
                h("line", { x1: l.x1, y1: l.y1, x2: l.x2, y2: l.y2,
                  className: "co-handoff-line"
                    + (l.cls === "recent" ? " co-handoff-line--recent" : "")
                    + (l.active ? " co-handoff-line--active" : "") }),
                l.active && h("circle", { className: "co-handoff-packet", cx: l.x1, cy: l.y1, r: 4.5 }));
            })),

          h(FounderOffice, { items: founderList, degraded: degraded }),

          h("div", { className: "co-lane co-lane--ic" },
            h("span", { className: "co-lane-label" }, "TRANSITION"),
            ws("org-ic-secretary", "co-ws-slot--center")),

          h("div", { className: "co-lane co-lane--cos" },
            h("span", { className: "co-lane-label" }, "ORCHESTRATION"),
            ws("org-cos", "co-ws-slot--center co-ws-slot--wide")),

          h("div", { className: "co-pods" },
            h("div", { className: "co-zone co-zone--research" },
              h("div", { className: "co-zone-label" }, "RESEARCH POD"),
              h("div", { className: "co-zone-grid" },
                ws("org-commodity-analyst"), ws("org-macro-strategist"),
                ws("org-equity-analyst"), ws("org-options-strategist"))),
            h("div", { className: "co-zone co-zone--intel" },
              h("div", { className: "co-zone-label" }, "INTELLIGENCE / VALIDATION POD"),
              h("div", { className: "co-zone-grid" },
                ws("org-quant-validator"), ws("org-data-steward")))),

          h("div", { className: "co-lane co-lane--review" },
            h("span", { className: "co-lane-label" }, "REVIEW / CONTROL"),
            ws("org-cro"), ws("org-auditor")),

          h("div", { className: "co-lane co-lane--radar" },
            h("span", { className: "co-lane-label" }, "EXTERNAL SENSING"),
            ws("org-radar-scout", "co-ws-slot--wide")))),

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
                })))),

      drawerDesk && h(DetailDrawer, {
        desk: drawerDesk,
        events: drawerEvents,
        edges: handoffs,
        onClose: function () { setDrawerDesk(null); },
      }));
  }

  if (window.__HERMES_PLUGINS__ && typeof window.__HERMES_PLUGINS__.register === "function") {
    window.__HERMES_PLUGINS__.register("capital-intelligence-office", CapitalOfficePage);
  }
})();
