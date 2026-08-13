"""Capital Intelligence Live Office v1 — dashboard plugin backend (READ-ONLY).

Phase 2: Spatial Office. Phase 2.1: Semantic Hardening (S1–S4).
Pure read-only projection of the Hermes Capital Intelligence board.
No POST/PUT/PATCH/DELETE routes; no tables/files created; every response
derived per request.

S1 — handoffs are classified ACTIVE / RECENT / HISTORICAL (HISTORICAL hidden
by default; scope=all for the History toggle). Recorded task_links are NOT
live coordination.
S2 — state precedence puts Error above Recently Completed; failure detection
checks BOTH task_runs.status and task_runs.outcome.
S3 — diagnostics classification is structured (exact prefixes + known harness
profiles); no broad free-text substring matching.
S4 — profile root resolves through the Hermes runtime (HERMES_HOME), with the
Windows AppData path only as a last-resort fallback.

H3 — all DB access is encapsulated behind ONE adapter (LiveOfficeDataAdapter):
  * preferred: supported ``hermes_cli.kanban_db`` helpers (list_tasks, …)
  * fallback: read-only SELECTs on the kanban DB (isolated here, not in routes)
The frontend stays completely schema-independent (it only reads the JSON below).

H1 — profile truth: each desk reports ``available`` from the runtime profiles
dir. profile exists + no work -> ``idle``; profile absent -> ``unavailable``
(Never represent a missing profile as Idle).

H2 — operational vs diagnostics classification (presentation-only, never
persisted, never filters Hermes truth): PILOT-NONCANONICAL / harness-canary /
test / synthetic tasks are visible in a ``diagnostics`` layer but do NOT drive
the main desk state. Main desk state derives from Operational work only.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect

from hermes_cli import kanban_db

log = logging.getLogger(__name__)

router = APIRouter()

# The 11 organizational desks (canonical ROLE-REGISTRY v0.1) -> Hermes profile.
DESKS: list[dict[str, str]] = [
    {"role": "Chief of Staff", "profile": "org-cos", "registry_row": 1},
    {"role": "IC Secretary", "profile": "org-ic-secretary", "registry_row": 2},
    {"role": "Commodity Analyst", "profile": "org-commodity-analyst", "registry_row": 3},
    {"role": "Macro Strategist", "profile": "org-macro-strategist", "registry_row": 4},
    {"role": "Equity Alpha Analyst", "profile": "org-equity-analyst", "registry_row": 5},
    {"role": "Options Strategist", "profile": "org-options-strategist", "registry_row": 6},
    {"role": "Chief Risk Officer", "profile": "org-cro", "registry_row": 7},
    {"role": "Quant / Model Validator", "profile": "org-quant-validator", "registry_row": 8},
    {"role": "Data Steward", "profile": "org-data-steward", "registry_row": 9},
    {"role": "Internal Auditor", "profile": "org-auditor", "registry_row": 10},
    {"role": "Radar Scout", "profile": "org-radar-scout", "registry_row": 11},
]

_EVENT_POLL_SECONDS = 2.0
_OPEN_STATUSES = {"triage", "todo", "scheduled", "ready", "running", "blocked", "review"}

# H2 — diagnostics/test classification (presentation-only).
# Structured, in priority order (Phase 2.1 S3):
#   1. explicit structured task metadata — the tasks table exposes NO
#      type/kind/tags column (verified against the kanban schema 2026-08-13),
#      so this tier is currently unavailable; kept as the documented hook.
#   2. exact standardized title PREFIXES: [PILOT-NONCANONICAL] / [TEST] / [SYNTHETIC]
#   3. known harness/test profiles.
# NO broad free-text substring matching (e.g. "synthetic") — an operational
# task titled "Analyze synthetic data exposure" must remain operational.
_DIAGNOSTIC_PROFILES = {"harness-canary-ipm", "harness-docker-test", "harness-test"}
_DIAGNOSTIC_TITLE_PREFIXES = ("[PILOT-NONCANONICAL]", "[TEST]", "[SYNTHETIC]")


def _is_diagnostic(task: dict) -> bool:
    if task.get("assignee") in _DIAGNOSTIC_PROFILES:
        return True
    title = (task.get("title") or "").strip().upper()
    return any(title.startswith(p) for p in _DIAGNOSTIC_TITLE_PREFIXES)


# S2 — Hermes task_runs failure/success semantics (kanban_db.py schema
# docstring, verified 2026-08-13):
#   status:   running | done | blocked | crashed | timed_out | failed | released
#   outcome:  completed | blocked | crashed | timed_out | spawn_failed |
#             gave_up | reclaimed | (null while still running)
# A run is a FAILURE if EITHER field says so; success likewise. Checking only
# ``outcome`` (old code) missed status-only crashes.
_FAIL_STATUSES = {"crashed", "timed_out", "failed"}
_FAIL_OUTCOMES = {"crashed", "timed_out", "spawn_failed", "gave_up"}
_DONE_STATUSES = {"done", "completed"}
_DONE_OUTCOMES = {"completed"}


def _run_failed(r: dict) -> bool:
    return r.get("status") in _FAIL_STATUSES or r.get("outcome") in _FAIL_OUTCOMES


def _run_completed(r: dict) -> bool:
    return r.get("status") in _DONE_STATUSES or r.get("outcome") in _DONE_OUTCOMES


# ---------------------------------------------------------------------------
# H3 — LiveOfficeDataAdapter (single DB-access boundary)
# ---------------------------------------------------------------------------

class LiveOfficeDataAdapter:
    """One adapter owns every kanban-DB touch (helpers preferred, read-only
    SQL fallback isolated here). Board is resolved once per load."""

    def __init__(self, board: Optional[str] = None):
        self.board = board

    # -- supported helpers --------------------------------------------------
    def _connect(self):
        return kanban_db.connect(board=self.board)

    def list_tasks(self, conn, include_archived: bool = False) -> list:
        return kanban_db.list_tasks(conn, include_archived=include_archived)

    # -- read-only SQL fallbacks (isolated here) ----------------------------
    def task_runs(self, conn) -> list[dict]:
        rows = conn.execute(
            "SELECT id, task_id, profile, status, claim_expires, last_heartbeat_at, "
            "started_at, ended_at, outcome FROM task_runs ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]

    def recent_runs(self, conn, limit: int) -> list[dict]:
        rows = conn.execute(
            "SELECT id, task_id, profile, status, started_at, ended_at, "
            "last_heartbeat_at, outcome FROM task_runs ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def last_event_per_task(self, conn) -> dict[str, float]:
        out: dict[str, float] = {}
        try:
            rows = conn.execute(
                "SELECT task_id, MAX(created_at) AS m FROM task_events GROUP BY task_id"
            ).fetchall()
            for r in rows:
                out[r["task_id"]] = r["m"]
        except Exception:
            pass
        return out

    def recent_events(self, conn, limit: int) -> list[dict]:
        rows = conn.execute(
            "SELECT id, task_id, run_id, kind, payload, created_at "
            "FROM task_events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        out = []
        for r in rows:
            try:
                payload = json.loads(r["payload"]) if r["payload"] else None
            except Exception:
                payload = None
            out.append({
                "id": r["id"], "task_id": r["task_id"], "run_id": r["run_id"],
                "kind": r["kind"], "payload": payload, "created_at": r["created_at"],
            })
        return out

    def task_links(self, conn) -> list[dict]:
        try:
            rows = conn.execute("SELECT parent_id, child_id FROM task_links").fetchall()
            return [{"parent_id": r["parent_id"], "child_id": r["child_id"]} for r in rows]
        except Exception:
            return []

    def active_runs_count(self, conn) -> int:
        try:
            return conn.execute(
                "SELECT COUNT(*) AS c FROM task_runs WHERE status = 'running'"
            ).fetchone()["c"]
        except Exception:
            return 0

    def load_board(self, include_archived: bool = False) -> dict:
        """One pass over tasks/runs/events/links; returns normalized task dicts.

        include_archived=True (handoffs only): archived tasks stay in the
        classification universe so their links can be HISTORICAL — per the S1
        contract "both sides completed/archived". Desks/founder use the
        default (operational view, no archived tasks).
        """
        conn = self._connect()
        try:
            tasks = self.list_tasks(conn, include_archived=include_archived)
            now = time.time()
            runs = self.task_runs(conn)
            active_run_map: dict[str, dict] = {}
            run_by_task: dict[str, list] = {}
            for r in runs:
                run_by_task.setdefault(r["task_id"], []).append(r)
                if r["status"] == "running" or (
                    r["status"] == "claimed" and r["claim_expires"] and r["claim_expires"] > now
                ):
                    active_run_map[r["task_id"]] = r
            last_event = self.last_event_per_task(conn)
            task_dicts = []
            for t in tasks:
                task_dicts.append({
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "assignee": t.assignee,
                    "block_kind": getattr(t, "block_kind", None),
                    "blocked_reason": getattr(t, "blocked_reason", None),
                    "created_at": t.created_at,
                    "active_run": active_run_map.get(t.id),
                    "last_activity": last_event.get(t.id),
                })
            return {"tasks": task_dicts, "runs_by_task": run_by_task}
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# H1 — profile truth
# ---------------------------------------------------------------------------

def _profiles_dir() -> Path:
    # S4 — resolve through the Hermes runtime (HERMES_HOME) first, not a
    # hard-coded Windows path. The AppData absolute path remains ONLY as a
    # last-resort fallback for exotic deployments.
    try:
        from hermes_cli.config import get_hermes_home
        home = Path(get_hermes_home())
        if home.parent.name == "profiles":
            return home.parent
        return home / "profiles"
    except Exception:
        return Path.home() / "AppData/Local/hermes/profiles"


def _profile_installed(profile: str) -> bool:
    try:
        return (_profiles_dir() / profile).is_dir()
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Presentation-state derivation (H2: operational-only; 9 states; never persisted)
# ---------------------------------------------------------------------------

def _desk_state_for_tasks(tasks: list[dict], last_event_kind: Optional[str],
                          recent_run_failed: bool) -> tuple[str, Optional[dict]]:
    """Derive the desk presentation state from its OPERATIONAL tasks.

    Priority (Phase 2.1 S2): awaiting_founder > working > blocked > reviewing >
    queued > error > recently_completed > idle. A recent failure can NEVER be
    masked by a recently completed run (old order had recently_completed first).
    Missing data is handled by the caller (unavailable).
    """
    state = "idle"
    current = None
    open_tasks = [t for t in tasks if t["status"] in _OPEN_STATUSES]
    for t in tasks:
        if t["status"] == "blocked" and t.get("block_kind") in {"needs_input"}:
            state = "awaiting_founder"
            current = t
            break
    if state == "idle":
        for t in tasks:
            if t.get("active_run"):
                state = "working"
                current = t
                break
    if state == "idle":
        for t in tasks:
            if t["status"] == "blocked":
                state = "blocked"
                current = t
                break
    if state == "idle":
        for t in tasks:
            if t["status"] == "review":
                state = "reviewing"
                current = t
                break
    if state == "idle" and open_tasks:
        state = "queued"
        current = min(open_tasks, key=lambda t: t.get("created_at") or 0)
    if state == "idle" and recent_run_failed:
        state = "error"
    if state == "idle" and last_event_kind == "completed":
        state = "recently_completed"
    return state, current


# ---------------------------------------------------------------------------
# Routes (READ-ONLY)
# ---------------------------------------------------------------------------

def _active_board_slug() -> str:
    env = os.environ.get("HERMES_KANBAN_BOARD")
    if env:
        return env
    try:
        p = kanban_db.current_board_path()
        if p and p.exists():
            slug = p.read_text(encoding="utf-8").strip()
            if slug:
                return slug
    except Exception:
        pass
    return kanban_db.DEFAULT_BOARD


def _board_name(slug: str) -> str:
    try:
        p = kanban_db.current_board_path().parent / "boards" / slug / "board.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")).get("name") or slug
    except Exception:
        pass
    return slug


def _resolve_board(board: Optional[str]) -> Optional[str]:
    if board:
        try:
            normed = kanban_db._normalize_board_slug(board)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"unknown board: {board}")
        if normed and normed != kanban_db.DEFAULT_BOARD and not kanban_db.board_exists(normed):
            raise HTTPException(status_code=404, detail=f"board not found: {normed}")
        return normed
    return None


@router.get("/health")
def health(board: Optional[str] = Query(None)):
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    conn = adapter._connect()
    try:
        counts: dict[str, int] = {}
        for t in adapter.list_tasks(conn):
            counts[t.status] = counts.get(t.status, 0) + 1
        slug = _active_board_slug()
        return {
            "ok": True,
            "data_source": "hermes_kanban_board",
            "board": slug,
            "board_name": _board_name(slug),
            "task_counts": counts,
            "active_runs": adapter.active_runs_count(conn),
            "generated_at": time.time(),
        }
    finally:
        conn.close()


@router.get("/desks")
def desks(board: Optional[str] = Query(None)):
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    data = adapter.load_board()
    tasks = data["tasks"]
    by_profile: dict[str, list] = {}
    for t in tasks:
        by_profile.setdefault(t["assignee"] or "", []).append(t)

    out = []
    for desk in DESKS:
        profile = desk["profile"]
        all_desk_tasks = by_profile.get(profile, [])
        operational = [t for t in all_desk_tasks if not _is_diagnostic(t)]
        diagnostics = [t for t in all_desk_tasks if _is_diagnostic(t)]
        installed = _profile_installed(profile)

        if not installed:
            state, current = "unavailable", None
        else:
            # recent signal for recently_completed / error presentation states
            last_kind = None
            recent_failed = False
            run_map = data["runs_by_task"]
            for t in operational:
                for r in run_map.get(t["id"], []):
                    if _run_completed(r) and \
                       (r.get("ended_at") or 0) > time.time() - 600:
                        last_kind = "completed"
                    if _run_failed(r) and \
                       (r.get("ended_at") or 0) > time.time() - 1800:
                        recent_failed = True
            state, current = _desk_state_for_tasks(operational, last_kind, recent_failed)

        open_count = sum(1 for t in operational if t["status"] in _OPEN_STATUSES)
        active_worker = any(t["active_run"] for t in operational)
        last_activity = max((t.get("last_activity") or 0 for t in operational), default=None)
        diag_counts: dict[str, int] = {}
        for t in diagnostics:
            diag_counts[t["status"]] = diag_counts.get(t["status"], 0) + 1

        out.append({
            "role": desk["role"],
            "profile": profile,
            "registry_row": desk["registry_row"],
            "available": installed,
            "state": state,
            "current_task": current and {"id": current["id"], "title": current["title"], "status": current["status"]},
            "open_count": open_count,
            "active_worker": active_worker,
            "last_activity": last_activity,
            "task_count": len(operational),
            "diagnostics": diag_counts,
        })
    slug = _active_board_slug()
    return {"board": slug, "board_name": _board_name(slug),
            "data_source": "hermes_kanban_board", "desks": out}


@router.get("/founder-attention")
def founder_attention(board: Optional[str] = Query(None)):
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    data = adapter.load_board()
    items = []
    for t in data["tasks"]:
        if _is_diagnostic(t):
            continue
        is_gate = t["status"] == "blocked" and t.get("block_kind") in {"needs_input"}
        is_review = t["status"] == "review"
        if is_gate or is_review:
            items.append({
                "task_id": t["id"],
                "title": t["title"],
                "desk": t["assignee"],
                "status": t["status"],
                "gate": "founder_decision" if is_gate else "review",
                "block_reason": t.get("blocked_reason") or t.get("block_kind"),
            })
    slug = _active_board_slug()
    return {"board": slug, "board_name": _board_name(slug), "items": items}


@router.get("/activity")
def activity(board: Optional[str] = Query(None), limit: int = Query(25, ge=1, le=100),
             profile: Optional[str] = Query(None)):
    """Recent task_events (read-only). Optional ``profile`` filter narrows to
    events of tasks assigned to that profile — used by the Phase-3 agent
    detail drawer. Additive only; no semantics change."""
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    conn = adapter._connect()
    try:
        events = adapter.recent_events(conn, limit)
        tasks = adapter.list_tasks(conn)
        title_map = {t.id: t.title for t in tasks}
        if profile:
            assignee_map = {t.id: t.assignee for t in tasks}
            events = [e for e in events if assignee_map.get(e["task_id"]) == profile]
        for e in events:
            e["task_title"] = title_map.get(e["task_id"])
        slug = _active_board_slug()
        return {"board": slug, "board_name": _board_name(slug), "items": events}
    finally:
        conn.close()


@router.get("/workers")
def workers(board: Optional[str] = Query(None), limit: int = Query(15, ge=1, le=100)):
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    conn = adapter._connect()
    try:
        runs = adapter.recent_runs(conn, limit)
        title_map = {t.id: t.title for t in adapter.list_tasks(conn)}
        items = []
        for r in runs:
            items.append({
                "run_id": r["id"], "task_id": r["task_id"], "profile": r["profile"],
                "status": r["status"], "started_at": r["started_at"], "ended_at": r["ended_at"],
                "last_heartbeat_at": r["last_heartbeat_at"], "outcome": r["outcome"],
                "task_title": title_map.get(r["task_id"]),
            })
        slug = _active_board_slug()
        return {"board": slug, "board_name": _board_name(slug), "items": items}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# S1 — handoff semantics: ACTIVE vs RECENT vs HISTORICAL
# ---------------------------------------------------------------------------

# A relationship is RECENT when either side saw activity (event or finished
# run) within this window. Documented in LIVE-OFFICE-SOURCE-MAP.md.
_HANDOFF_RECENT_WINDOW = 1800  # 30 minutes
_HANDOFF_CLASS_ORDER = {"active": 0, "recent": 1, "historical": 2}


def _classify_handoff(parent: dict, child: dict, runs_by_task: dict, now: float) -> str:
    """Recorded task_links are NOT proof of live coordination.

    active:      either side is still open (open status) or has a live worker
    recent:      either side saw an event / finished run within the window
    historical:  both sides closed and no recent activity — hidden by default
    """
    if parent["status"] in _OPEN_STATUSES or child["status"] in _OPEN_STATUSES:
        return "active"
    if parent.get("active_run") or child.get("active_run"):
        return "active"
    last = max(parent.get("last_activity") or 0, child.get("last_activity") or 0)
    if last and now - last <= _HANDOFF_RECENT_WINDOW:
        return "recent"
    for t in (parent, child):
        for r in runs_by_task.get(t["id"], []):
            if r.get("ended_at") and now - r["ended_at"] <= _HANDOFF_RECENT_WINDOW:
                return "recent"
    return "historical"


@router.get("/handoffs")
def handoffs(board: Optional[str] = Query(None), scope: str = Query("active")):
    """Real task-link relationships mapped to desk-to-desk flow (read-only).

    scope=active (default): ACTIVE (normal line) + RECENT (subdued line) only;
    HISTORICAL relationships are NOT shown by default. scope=all additionally
    returns HISTORICAL edges (for the History/Diagnostics toggle). Never
    deletes task_links; the classification is derived per request.
    """
    if scope not in ("active", "all"):
        raise HTTPException(status_code=400, detail="scope must be 'active' or 'all'")
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    # include archived so completed relationships stay classifiable (S1)
    data = adapter.load_board(include_archived=True)
    conn = adapter._connect()
    try:
        links = adapter.task_links(conn)
    finally:
        conn.close()
    task_by_id = {t["id"]: t for t in data["tasks"]}
    profile_to_role = {d["profile"]: d["role"] for d in DESKS}
    desk_set = set(profile_to_role.keys())
    now = time.time()
    edges: dict[tuple, dict] = {}
    for lk in links:
        parent, child = task_by_id.get(lk["parent_id"]), task_by_id.get(lk["child_id"])
        if not parent or not child:
            continue
        pa, ca = parent["assignee"], child["assignee"]
        if pa in desk_set and ca in desk_set and pa != ca:
            key = (pa, ca)
            e = edges.setdefault(key, {"from": pa, "to": ca, "task_ids": [], "class": None})
            e["task_ids"].append(lk["child_id"])
            cls = _classify_handoff(parent, child, data["runs_by_task"], now)
            # worst-class wins: any active link keeps the edge ACTIVE
            if e["class"] is None or _HANDOFF_CLASS_ORDER[cls] < _HANDOFF_CLASS_ORDER[e["class"]]:
                e["class"] = cls
    items = [{"from": k[0], "to": k[1], "from_role": profile_to_role[k[0]],
              "to_role": profile_to_role[k[1]], "task_ids": v["task_ids"], "class": v["class"]}
             for k, v in sorted(edges.items())]
    historical = [i for i in items if i["class"] == "historical"]
    if scope == "active":
        items = [i for i in items if i["class"] != "historical"]
    slug = _active_board_slug()
    return {"board": slug, "board_name": _board_name(slug),
            "scope": scope, "historical_count": len(historical), "items": items}


@router.websocket("/events")
async def stream_events(ws: WebSocket):
    try:
        from hermes_cli import web_server as _ws
        authorized = bool(_ws._ws_auth_ok(ws))
    except Exception:
        authorized = True
    if not authorized:
        await ws.close(code=1008)
        return
    await ws.accept()
    try:
        ws_board = ws.query_params.get("board")
        adapter = LiveOfficeDataAdapter(ws_board)
        since_q = ws.query_params.get("since")
        if since_q:
            try:
                cursor = int(since_q)
            except ValueError:
                cursor = 0
        else:
            # Live tail: start from the current newest event so the full
            # history is NOT replayed through the 200-per-poll window (which
            # delayed genuine live events by minutes on boards with long
            # histories). Genuine-liveness fix exposed by Phase-3 visual work.
            conn = adapter._connect()
            try:
                cursor = conn.execute(
                    "SELECT COALESCE(MAX(id), 0) AS m FROM task_events"
                ).fetchone()["m"]
            finally:
                conn.close()

        def _fetch_new(cursor_val: int) -> tuple[int, list[dict]]:
            conn = adapter._connect()
            try:
                rows = conn.execute(
                    "SELECT id, task_id, run_id, kind, payload, created_at "
                    "FROM task_events WHERE id > ? ORDER BY id ASC LIMIT 200",
                    (cursor_val,),
                ).fetchall()
                out = []
                new_cursor = cursor_val
                for r in rows:
                    try:
                        payload = json.loads(r["payload"]) if r["payload"] else None
                    except Exception:
                        payload = None
                    out.append({
                        "id": r["id"], "task_id": r["task_id"], "run_id": r["run_id"],
                        "kind": r["kind"], "payload": payload, "created_at": r["created_at"],
                    })
                    new_cursor = r["id"]
                return new_cursor, out
            finally:
                conn.close()

        while True:
            cursor, events = await asyncio.to_thread(_fetch_new, cursor)
            if events:
                await ws.send_json({"events": events, "cursor": cursor})
            await asyncio.sleep(_EVENT_POLL_SECONDS)
    except WebSocketDisconnect:
        return
    except asyncio.CancelledError:
        return
    except Exception as exc:
        log.warning("Capital Office event stream error: %s", exc)
        try:
            await ws.close()
        except Exception:
            pass
