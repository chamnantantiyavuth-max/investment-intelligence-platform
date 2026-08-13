"""Capital Intelligence Live Office v1 — dashboard plugin backend (READ-ONLY).

Phase 2: Spatial Office. Pure read-only projection of the Hermes Capital
Intelligence board. No POST/PUT/PATCH/DELETE routes; no tables/files created;
every response derived per request.

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
_DIAGNOSTIC_PROFILES = {"harness-canary-ipm", "harness-docker-test", "harness-test"}
_DIAGNOSTIC_TITLE_MARKERS = (
    "[PILOT-NONCANONICAL]", "[TEST]", "[SYNTHETIC]", "synthetic", "test residue",
)


def _is_diagnostic(task: dict) -> bool:
    if task.get("assignee") in _DIAGNOSTIC_PROFILES:
        return True
    title = (task.get("title") or "").lower()
    return any(m.lower() in title for m in _DIAGNOSTIC_TITLE_MARKERS)


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

    def list_tasks(self, conn) -> list:
        return kanban_db.list_tasks(conn)

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

    def load_board(self) -> dict:
        """One pass over tasks/runs/events/links; returns normalized task dicts."""
        conn = self._connect()
        try:
            tasks = self.list_tasks(conn)
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
    # The dashboard process home is the same root kanban_db uses for boards.
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

    Priority: awaiting_founder > working > blocked > reviewing > queued >
    recently_completed > idle. ``error`` when a recent run crashed/gave up and
    there is no higher signal. Missing data is handled by the caller (unavailable).
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
    if state == "idle" and last_event_kind == "completed":
        state = "recently_completed"
    if state == "idle" and recent_run_failed:
        state = "error"
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
                    if r.get("status") in ("done", "completed") and \
                       (r.get("ended_at") or 0) > time.time() - 600:
                        last_kind = "completed"
                    if r.get("outcome") in ("crashed", "gave_up", "timed_out") and \
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
def activity(board: Optional[str] = Query(None), limit: int = Query(25, ge=1, le=100)):
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    conn = adapter._connect()
    try:
        events = adapter.recent_events(conn, limit)
        title_map = {t.id: t.title for t in adapter.list_tasks(conn)}
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


@router.get("/handoffs")
def handoffs(board: Optional[str] = Query(None)):
    """Real task-link relationships mapped to desk-to-desk flow (read-only)."""
    adapter = LiveOfficeDataAdapter(_resolve_board(board))
    conn = adapter._connect()
    try:
        links = adapter.task_links(conn)
        assignee_map = {t.id: t.assignee for t in adapter.list_tasks(conn)}
        profile_to_role = {d["profile"]: d["role"] for d in DESKS}
        desk_set = set(profile_to_role.keys())
        edges = {}
        for lk in links:
            pa, ca = assignee_map.get(lk["parent_id"]), assignee_map.get(lk["child_id"])
            if pa in desk_set and ca in desk_set and pa != ca:
                key = (pa, ca)
                e = edges.setdefault(key, {"from": pa, "to": ca, "task_ids": []})
                e["task_ids"].append(lk["child_id"])
        items = [{"from": k[0], "to": k[1], "from_role": profile_to_role[k[0]],
                  "to_role": profile_to_role[k[1]], "task_ids": v["task_ids"]}
                 for k, v in sorted(edges.items())]
        slug = _active_board_slug()
        return {"board": slug, "board_name": _board_name(slug), "items": items}
    finally:
        conn.close()


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
        cursor = 0
        try:
            cursor = int(ws.query_params.get("since", "0"))
        except ValueError:
            cursor = 0
        ws_board = ws.query_params.get("board")
        adapter = LiveOfficeDataAdapter(ws_board)

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
