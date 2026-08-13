"""Capital Intelligence Live Office v1 — dashboard plugin backend (READ-ONLY).

Pure read-only projection of the Hermes Capital Intelligence board. This
module owns NO organizational state: every response is computed per request
from the supported ``hermes_cli.kanban_db`` interface (the same code path the
CLI and gateway use). No POST/PUT/PATCH/DELETE routes exist here by design
(Founder charter: Office never owns or mutates org state).

Routes (mounted by the dashboard plugin system at /api/plugins/capital-intelligence-office/):
    GET  /health             data source, board, status counts, active runs
    GET  /desks              the 11 organizational desks + derived presentation state
    GET  /founder-attention  human-gate tasks (blocked+needs_input, review)
    GET  /activity           recent task_events (read-only tail)
    GET  /workers            recent task_runs (worker/run health)
    WS   /events             live task_events tail (mirrors the kanban /events stream)

Presentation states are UI-only derivations computed here and never persisted:
    awaiting_founder / working / blocked / reviewing / queued / idle / unknown
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from hermes_cli import kanban_db

log = logging.getLogger(__name__)

router = APIRouter()

# The 11 organizational desks (canonical ROLE-REGISTRY v0.1) → Hermes profile.
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
_HUMAN_GATE_KINDS = {"needs_input"}


def _resolve_board(board: Optional[str]) -> Optional[str]:
    """Resolve a board slug; default to the active board."""
    if board:
        try:
            normed = kanban_db._normalize_board_slug(board)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"unknown board: {board}")
        if normed and normed != kanban_db.DEFAULT_BOARD and not kanban_db.board_exists(normed):
            raise HTTPException(status_code=404, detail=f"board not found: {normed}")
        return normed
    return None


def _active_board_slug() -> str:
    """Resolve the actual active board slug (env override → kanban/current → default)."""
    import os
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
    """Human name from board.json (e.g. 'Capital Intelligence' for slug iip)."""
    try:
        import json as _json
        p = kanban_db.current_board_path().parent / "boards" / slug / "board.json"
        if p.exists():
            return _json.loads(p.read_text(encoding="utf-8")).get("name") or slug
    except Exception:
        pass
    return slug


def _conn(board: Optional[str] = None):
    if board:
        kanban_db.init_db(board=board)
    return kanban_db.connect(board=board)


# ---------------------------------------------------------------------------
# WS auth (same canonical gate as the kanban plugin — never drifts from core)
# ---------------------------------------------------------------------------

def _ws_upgrade_authorized(ws: "WebSocket") -> bool:
    try:
        from hermes_cli import web_server as _ws
    except Exception:
        return True  # no dashboard context (tests) — accept so the tail is testable
    return bool(_ws._ws_auth_ok(ws))


# ---------------------------------------------------------------------------
# Desk state derivation (presentation-only, per-request, never persisted)
# ---------------------------------------------------------------------------

def _desk_state_for_tasks(tasks: list[dict]) -> tuple[str, dict]:
    """Derive the desk presentation state from its tasks.

    Priority (most-attention-wins):
      awaiting_founder > working > blocked > reviewing > queued > idle
    """
    state = "idle"
    current = None
    open_tasks = [t for t in tasks if t["status"] in _OPEN_STATUSES]
    for t in tasks:
        if t["status"] == "blocked" and t.get("block_kind") in _HUMAN_GATE_KINDS:
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
    return state, current


def _load_board(board: Optional[str]) -> dict:
    """Load tasks + runs + events for the board once, then aggregate per desk."""
    conn = _conn(board)
    try:
        tasks = kanban_db.list_tasks(conn)
        now = time.time()
        # Active runs + runs-by-task: read-only direct SELECT on task_runs
        # (same supported DB the kanban plugin tails for task_events).
        active_run_map: dict[str, dict] = {}
        run_by_task: dict[str, list] = {}
        try:
            rows = conn.execute(
                "SELECT id, task_id, profile, status, claim_expires, last_heartbeat_at, "
                "started_at, ended_at, outcome FROM task_runs ORDER BY id"
            ).fetchall()
            for r in rows:
                run_by_task.setdefault(r["task_id"], []).append(r)
                if r["status"] == "running" or (
                    r["status"] == "claimed" and r["claim_expires"] and r["claim_expires"] > now
                ):
                    active_run_map[r["task_id"]] = r
        except Exception:
            pass
        # last activity per task (task_events tail)
        last_event_map: dict[str, float] = {}
        try:
            rows = conn.execute(
                "SELECT task_id, MAX(created_at) AS m FROM task_events GROUP BY task_id"
            ).fetchall()
            for r in rows:
                last_event_map[r["task_id"]] = r["m"]
        except Exception:
            pass

        task_dicts = []
        for t in tasks:
            d = {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "assignee": t.assignee,
                "block_kind": getattr(t, "block_kind", None),
                "blocked_reason": getattr(t, "blocked_reason", None),
                "created_at": t.created_at,
                "active_run": active_run_map.get(t.id),
                "last_activity": last_event_map.get(t.id),
            }
            task_dicts.append(d)
        return {"tasks": task_dicts, "runs_by_task": run_by_task}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Routes (READ-ONLY)
# ---------------------------------------------------------------------------

@router.get("/health")
def health(board: Optional[str] = Query(None)):
    conn = _conn(board)
    try:
        tasks = kanban_db.list_tasks(conn)
        counts: dict[str, int] = {}
        for t in tasks:
            counts[t.status] = counts.get(t.status, 0) + 1
        active = 0
        try:
            active = conn.execute(
                "SELECT COUNT(*) AS c FROM task_runs WHERE status = 'running'"
            ).fetchone()["c"]
        except Exception:
            active = 0
        return {
            "ok": True,
            "data_source": "hermes_kanban_board",
            "board": _active_board_slug(),
            "board_name": _board_name(_active_board_slug()),
            "task_counts": counts,
            "active_runs": active,
            "generated_at": time.time(),
        }
    finally:
        conn.close()


@router.get("/desks")
def desks(board: Optional[str] = Query(None)):
    data = _load_board(board)
    tasks = data["tasks"]
    by_profile: dict[str, list] = {}
    for t in tasks:
        by_profile.setdefault(t["assignee"] or "", []).append(t)

    out = []
    for desk in DESKS:
        profile = desk["profile"]
        desk_tasks = by_profile.get(profile, [])
        state, current = _desk_state_for_tasks(desk_tasks)
        open_count = sum(1 for t in desk_tasks if t["status"] in _OPEN_STATUSES)
        active_worker = any(t["active_run"] for t in desk_tasks)
        last_activity = max((t.get("last_activity") or 0 for t in desk_tasks), default=None)
        out.append({
            "role": desk["role"],
            "profile": profile,
            "registry_row": desk["registry_row"],
            "state": state,
            "current_task": current and {"id": current["id"], "title": current["title"], "status": current["status"]},
            "open_count": open_count,
            "active_worker": active_worker,
            "last_activity": last_activity,
            "task_count": len(desk_tasks),
        })
    return {"board": _active_board_slug(),
            "board_name": _board_name(_active_board_slug()), "data_source": "hermes_kanban_board", "desks": out}


@router.get("/founder-attention")
def founder_attention(board: Optional[str] = Query(None)):
    data = _load_board(board)
    items = []
    for t in data["tasks"]:
        is_gate = t["status"] == "blocked" and t.get("block_kind") in _HUMAN_GATE_KINDS
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
    return {"board": _active_board_slug(),
            "board_name": _board_name(_active_board_slug()), "items": items}


@router.get("/activity")
def activity(board: Optional[str] = Query(None), limit: int = Query(25, ge=1, le=100)):
    conn = _conn(board)
    try:
        rows = conn.execute(
            "SELECT id, task_id, run_id, kind, payload, created_at "
            "FROM task_events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        title_map = {t.id: t.title for t in kanban_db.list_tasks(conn)}
        items = []
        for r in rows:
            try:
                payload = json.loads(r["payload"]) if r["payload"] else None
            except Exception:
                payload = None
            items.append({
                "id": r["id"], "task_id": r["task_id"], "run_id": r["run_id"],
                "kind": r["kind"], "payload": payload, "created_at": r["created_at"],
                "task_title": title_map.get(r["task_id"]),
            })
        return {"board": _active_board_slug(),
            "board_name": _board_name(_active_board_slug()), "items": items}
    finally:
        conn.close()


@router.get("/workers")
def workers(board: Optional[str] = Query(None), limit: int = Query(15, ge=1, le=100)):
    conn = _conn(board)
    try:
        rows = conn.execute(
            "SELECT id, task_id, profile, status, started_at, ended_at, "
            "last_heartbeat_at, outcome FROM task_runs ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        title_map = {t.id: t.title for t in kanban_db.list_tasks(conn)}
        items = []
        for r in rows:
            items.append({
                "run_id": r["id"], "task_id": r["task_id"], "profile": r["profile"],
                "status": r["status"], "started_at": r["started_at"], "ended_at": r["ended_at"],
                "last_heartbeat_at": r["last_heartbeat_at"],
                "outcome": r["outcome"],
                "task_title": title_map.get(r["task_id"]),
            })
        return {"board": _active_board_slug(),
            "board_name": _board_name(_active_board_slug()), "items": items}
    finally:
        conn.close()


@router.websocket("/events")
async def stream_events(ws: WebSocket):
    if not _ws_upgrade_authorized(ws):
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

        def _fetch_new(cursor_val: int) -> tuple[int, list[dict]]:
            conn = kanban_db.connect(board=ws_board)
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
