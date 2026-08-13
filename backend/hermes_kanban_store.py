"""Read-only store for Hermes Capital Intelligence board state (Stage 7.5, FD #106).

Serves operational tracking ONLY from the Hermes kanban board (iip = "Capital
Intelligence") as the ONE authoritative organizational work-state source.
Read-only: no writes, no schema changes; the Hermes kanban kernel owns all
mutations. Legacy repo-board YAML remains FROZEN (Stage 7.1) — this store does
not read it for live work-state (historical cards are not re-created as live).

Stage 7.5 contract (Founder):
  - /kanban + /org-office read the Hermes iip board as the ONE work-state source
  - READ-ONLY UI integration: no mutation endpoints exposed to the browser
  - do NOT recreate the legacy 11-column state machine — expose the Hermes
    board's real workflow columns
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

# Hermes board DB (canonical source). Resolved like the CLI does: env override
# -> board file -> default locations. The kanban root lives under the Hermes
# base dir (LOCALAPPDATA/hermes), NOT the profile dir — try candidates in order.
_HERMES_HOME = Path(os.environ.get("HERMES_HOME", "")) or (Path.home() / "AppData" / "Local" / "hermes")
_LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))

def _resolve_kanban_db() -> Path:
    env_db = os.environ.get("HERMES_KANBAN_DB", "")
    candidates = []
    if env_db:
        candidates.append(Path(env_db))
    candidates += [
        _LOCALAPPDATA / "hermes" / "kanban" / "boards" / "iip" / "kanban.db",
        _HERMES_HOME / "kanban" / "boards" / "iip" / "kanban.db",
        Path.home() / ".hermes" / "kanban" / "boards" / "iip" / "kanban.db",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]

KANBAN_DB = _resolve_kanban_db()

# Hermes board status -> UI column label (Hermes-native statuses, direct — NO
# collapse/replacement state machine). Source of truth = the installed Hermes
# runtime status vocabulary (hermes_cli/kanban_db.VALID_STATUSES):
#   triage, todo, scheduled, ready, running, blocked, review, done, archived
# Correction C6 (2026-08-13): triage/todo/ready/scheduled/review/archived are
# exposed directly; todo is NOT collapsed into Ready, archived is NOT collapsed
# into Done, cancelled is NOT used (the runtime has no such status).
STATUS_TO_COLUMN = {
    "triage": "Triage",
    "todo": "Todo",
    "scheduled": "Scheduled",
    "ready": "Ready",
    "running": "Running",
    "blocked": "Blocked",
    "review": "Review",
    "done": "Done",
    "archived": "Archived",
}
COLUMNS = ["Triage", "Todo", "Scheduled", "Ready", "Running", "Blocked", "Review", "Done", "Archived"]

# Legacy repo-board column is preserved as a provenance label only (from the
# frozen migration snapshot), never recreated as a live state machine.


def _connect() -> sqlite3.Connection:
    if not KANBAN_DB.exists():
        raise FileNotFoundError(f"Hermes kanban DB not found: {KANBAN_DB}")
    conn = sqlite3.connect(f"file:{KANBAN_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def list_tasks() -> list[dict]:
    """Read-only listing of Hermes board tasks mapped to the OrgCard shape."""
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT id, title, body, assignee, status, priority, created_by,
                   created_at, started_at, completed_at, tenant, result,
                   idempotency_key, block_kind, block_recurrences,
                   model_override, provider_override, skills
            FROM tasks
            ORDER BY created_at DESC
            """
        ).fetchall()
    finally:
        conn.close()

    cards = []
    for r in rows:
        cards.append(_to_card(dict(r)))
    return cards


def _to_card(r: dict) -> dict:
    """Map a Hermes task row to the frontend OrgCard contract (best effort)."""
    status = r.get("status") or "ready"
    created = r.get("created_at") or ""
    if isinstance(created, (int, float)):
        import datetime
        created = datetime.datetime.fromtimestamp(created).isoformat()
    card = {
        "card_id": r.get("id", ""),
        "title": r.get("title", ""),
        "research_question": r.get("body") or "",
        "decision_user": r.get("created_by") or "",
        "workflow_column": STATUS_TO_COLUMN.get(status, status.capitalize()),
        "approval_status": None,
        "monitoring_status": None,
        "thesis_status": None,
        "research_state": None,
        "artifact_state": None,
        "domain": (r.get("tenant") or "").upper(),
        "principal_owner": r.get("assignee") or "",
        "assistant_owner": None,
        "priority": r.get("priority") or "P3",
        "materiality": None,
        "created_at": created,
        "required_by": None,
        "expected_artifact": None,
        "evidence_standard": None,
        "data_status": None,
        "validation_status": None,
        "risk_status": None,
        "audit_status": None,
        "open_decision_slots": [],
        "dependencies": [],
        "blocked_reason": r.get("block_kind") or None,
        "next_action": None,
        "last_updated": created,
        "active_holds": [],
        "holds": [],
        "_path": f"kanban:board=iip/task={r.get('id', '')}",
    }
    # Provenance extras (honest — these are Hermes board facts, not legacy fields)
    if r.get("model_override"):
        card["model_override"] = r["model_override"]
    if r.get("provider_override"):
        card["provider_override"] = r["provider_override"]
    if r.get("idempotency_key"):
        card["idempotency_key"] = r["idempotency_key"]
    if r.get("skills"):
        card["skills"] = r["skills"]
    return card


def list_holds() -> list[dict]:
    """Hermes board has no holds concept — return empty (honest absence).

    Historical hold records (HOLD-DATA-001 / HOLD-RISK-001, both CLEARED) live in
    evidence/organization/holds/ and are served by /org-holds (org_store).
    """
    return []


def board_meta() -> dict:
    """Board identity for provenance (read board.json when present)."""
    board_json = KANBAN_DB.parent / "board.json"
    meta = {"slug": "iip", "name": "Capital Intelligence"}
    if board_json.exists():
        import json as _json
        try:
            meta.update(_json.loads(board_json.read_text(encoding="utf-8")))
        except Exception:
            pass
    meta["data_source"] = "hermes_kanban_board"
    meta["authoritative_since"] = "2026-08-13 (Stage 7.5, FD #106)"
    return meta
