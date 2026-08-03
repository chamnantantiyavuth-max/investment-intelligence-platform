"""Persistence layer — SQLite (stdlib sqlite3), immutable, content-addressed (arch v0.4 §4, plan T2).

FD #47 D1: stdlib sqlite3 (zero new runtime dependencies). WAL, busy_timeout, per-operation
connections, PRAGMA foreign_keys=ON every connection. Immutable (module, run_id) semantics:
same key + different bytes -> REJECT. Composite lineage via api_read_runs.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1
ADAPTER_VERSION = "v1"

_DEFAULT_DB = Path(__file__).resolve().parent / "data" / "iip.db"


def _db_path() -> Path:
    return Path(os.environ.get("IIP_DB_PATH", str(_DEFAULT_DB)))


def _artifact_store() -> Path:
    return Path(os.environ.get("IIP_ARTIFACT_BASE", str(_DEFAULT_DB.parent))) / "artifacts"


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


_SCHEMA = """
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    run_id TEXT NOT NULL,
    point_in_time TEXT,
    fixture_category TEXT,
    artifact_sha256 TEXT NOT NULL,
    artifact_path TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    UNIQUE (module, run_id)
);
CREATE TABLE IF NOT EXISTS api_reads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    route_params TEXT,
    data_source TEXT NOT NULL,
    response_sha256 TEXT NOT NULL,
    status INTEGER NOT NULL,
    adapter_version TEXT NOT NULL,
    served_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS api_read_runs (
    api_read_id INTEGER NOT NULL REFERENCES api_reads(id),
    run_id_fk INTEGER NOT NULL REFERENCES pipeline_runs(id),
    component TEXT NOT NULL,
    PRIMARY KEY (api_read_id, component)
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(_SCHEMA)
    row = conn.execute("SELECT value FROM settings WHERE key='schema_version'").fetchone()
    if row is None:
        conn.execute("INSERT INTO settings(key, value) VALUES('schema_version', ?)", (str(SCHEMA_VERSION),))
        conn.commit()


def get_schema_version() -> int:
    conn = _connect()
    try:
        _init_db(conn)
        row = conn.execute("SELECT value FROM settings WHERE key='schema_version'").fetchone()
        return int(row["value"])
    finally:
        conn.close()


def set_schema_version(v: int) -> None:
    conn = _connect()
    try:
        _init_db(conn)
        conn.execute("UPDATE settings SET value=? WHERE key='schema_version'", (str(v),))
        conn.commit()
    finally:
        conn.close()


def check_schema_compatibility() -> None:
    """Refuse to operate if the DB schema is newer than this code supports (NF8)."""
    conn = _connect()
    try:
        _init_db(conn)
        row = conn.execute("SELECT value FROM settings WHERE key='schema_version'").fetchone()
        v = int(row["value"])
        if v > SCHEMA_VERSION:
            raise RuntimeError(
                f"DB schema_version={v} newer than code supports ({SCHEMA_VERSION}) — upgrade required")
    finally:
        conn.close()


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ingest_run(module: str, payload: bytes) -> str:
    """Store artifact bytes immutably; return canonical run_id.

    run_id = artifact's own run_id if present, else sha256[:16] (content-addressed).
    Same (module, run_id) with different bytes -> REJECT (immutable, plan C7 case a).
    Bytes without an embedded run_id -> hash-derived id; changed bytes -> new id (case b).
    """
    check_schema_compatibility()
    sha = _sha256(payload)
    try:
        parsed = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(f"artifact not valid JSON: {e}") from e

    embedded = None
    if isinstance(parsed, dict):
        embedded = parsed.get("run_id")
    run_id = str(embedded) if embedded else sha[:16]
    point_in_time = parsed.get("point_in_time") if isinstance(parsed, dict) else None
    fixture = parsed.get("fixture_category") if isinstance(parsed, dict) else None

    store = _artifact_store()
    store.mkdir(parents=True, exist_ok=True)
    artifact_path = store / f"{sha}.json"
    if not artifact_path.exists():
        artifact_path.write_bytes(payload)

    conn = _connect()
    try:
        _init_db(conn)
        row = conn.execute(
            "SELECT id, artifact_sha256 FROM pipeline_runs WHERE module=? AND run_id=?",
            (module, run_id)).fetchone()
        if row is not None:
            if row["artifact_sha256"] != sha:
                raise RuntimeError(
                    f"immutable run violated: (module={module}, run_id={run_id}) already registered "
                    f"with sha256={row['artifact_sha256']}, new bytes sha256={sha} — REJECTED")
            return run_id
        conn.execute(
            "INSERT INTO pipeline_runs(module, run_id, point_in_time, fixture_category, "
            "artifact_sha256, artifact_path, ingested_at) VALUES(?,?,?,?,?,?,?)",
            (module, run_id, point_in_time, fixture, sha, str(artifact_path), _now()))
        conn.commit()
        return run_id
    finally:
        conn.close()


def log_read(endpoint: str, params: str, data_source: str, response_sha256: str,
             status: int, adapter_version: str, runs: list[tuple[str, str]] | None = None) -> int:
    """Record an API read + its composite lineage (NF6). runs = [(run_id, component), ...]."""
    check_schema_compatibility()
    conn = _connect()
    try:
        _init_db(conn)
        cur = conn.execute(
            "INSERT INTO api_reads(endpoint, route_params, data_source, response_sha256, status, "
            "adapter_version, served_at) VALUES(?,?,?,?,?,?,?)",
            (endpoint, params, data_source, response_sha256, status, adapter_version, _now()))
        read_id = cur.lastrowid
        # dedupe by component (dashboard touches am via am_queue + dashboard_components)
        seen: dict[str, str] = {}
        for run_id, component in (runs or []):
            seen[component] = run_id
        for component, run_id in seen.items():
            run_row = conn.execute(
                "SELECT id FROM pipeline_runs WHERE module=? AND run_id=?",
                (component, run_id)).fetchone()
            if run_row is None:
                raise RuntimeError(f"lineage FK violation: run_id={run_id!r} component={component!r} not registered")
            conn.execute(
                "INSERT INTO api_read_runs(api_read_id, run_id_fk, component) VALUES(?,?,?)",
                (read_id, run_row["id"], component))
        conn.commit()
        return read_id
    finally:
        conn.close()


def get_read_runs(read_id: int) -> list[dict]:
    conn = _connect()
    try:
        _init_db(conn)
        rows = conn.execute(
            "SELECT ar.component, pr.run_id, pr.module FROM api_read_runs ar "
            "JOIN pipeline_runs pr ON pr.id = ar.run_id_fk WHERE ar.api_read_id=?",
            (read_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_active_nonce() -> str | None:
    conn = _connect()
    try:
        _init_db(conn)
        row = conn.execute("SELECT value FROM settings WHERE key='active_session_nonce'").fetchone()
        return row["value"] if row else None
    finally:
        conn.close()


def set_active_nonce(nonce: str | None) -> None:
    conn = _connect()
    try:
        _init_db(conn)
        conn.execute("DELETE FROM settings WHERE key='active_session_nonce'")
        if nonce is not None:
            conn.execute("INSERT INTO settings(key, value) VALUES('active_session_nonce', ?)", (nonce,))
        conn.commit()
    finally:
        conn.close()


def latest_run(module: str) -> dict | None:
    """Most recently ingested run for a module (dashboard per-component selection)."""
    conn = _connect()
    try:
        _init_db(conn)
        row = conn.execute(
            "SELECT id, run_id, point_in_time, fixture_category, artifact_sha256, artifact_path "
            "FROM pipeline_runs WHERE module=? ORDER BY id DESC LIMIT 1", (module,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
