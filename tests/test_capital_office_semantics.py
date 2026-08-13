"""Phase 2.1 Semantic Hardening — bounded acceptance tests (S1–S4).

Covers the four Founder findings that gate visual polish:

S1 — handoff classification: ACTIVE / RECENT / HISTORICAL; recorded task_links
     are NOT live coordination; historical links hidden by default.
S2 — state precedence Error > Recently Completed; failure detection checks BOTH
     task_runs.status and task_runs.outcome (not outcome alone).
S3 — structured diagnostics classification: exact title prefixes + known harness
     profiles only; NO broad free-text substring (e.g. "synthetic").
S4 — profile root resolves through the Hermes runtime (HERMES_HOME).

Pure unit tests on synthetic data (no board writes; no runtime worker runs).
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(
    Path(__file__).resolve().parents[1]
    / "hermes-plugins" / "capital-intelligence-office" / "dashboard"))

from plugin_api import (  # noqa: E402
    _HANDOFF_RECENT_WINDOW,
    _classify_handoff,
    _desk_state_for_tasks,
    _is_diagnostic,
    _profiles_dir,
)

NOW = time.time()


# ---------------------------------------------------------------------------
# S3 — structured diagnostic classification
# ---------------------------------------------------------------------------

def test_s3_operational_title_with_natural_language_synthetic_stays_operational():
    # Founder's negative case: "Analyze synthetic data exposure" must NOT be
    # classified as diagnostics merely because the word "synthetic" appears.
    task = {"title": "Analyze synthetic data exposure for the Q3 pack",
            "assignee": "org-equity-analyst"}
    assert _is_diagnostic(task) is False


def test_s3_mid_title_substring_is_not_a_marker():
    # Old code matched "synthetic" ANYWHERE in the title. New code requires an
    # exact standardized PREFIX.
    task = {"title": "Review the synthetic dataset quality report",
            "assignee": "org-data-steward"}
    assert _is_diagnostic(task) is False


def test_s3_exact_prefixes_are_diagnostic():
    for prefix in ("[PILOT-NONCANONICAL]", "[TEST]", "[SYNTHETIC]"):
        task = {"title": prefix + " bounded probe 001", "assignee": "org-quant-validator"}
        assert _is_diagnostic(task) is True, prefix


def test_s3_prefix_is_case_insensitive():
    task = {"title": "[test] probe", "assignee": "org-auditor"}
    assert _is_diagnostic(task) is True


def test_s3_known_harness_profile_is_diagnostic():
    task = {"title": "unmarked task", "assignee": "harness-canary-ipm"}
    assert _is_diagnostic(task) is True


def test_s3_normal_operational_title_not_diagnostic():
    task = {"title": "JNJ talc litigation resolution — publish with dissent",
            "assignee": "org-cos"}
    assert _is_diagnostic(task) is False


# ---------------------------------------------------------------------------
# S2 — error precedence + crash detection
# ---------------------------------------------------------------------------

def _task(status="done", active_run=None, block_kind=None):
    return {"id": "t", "title": "x", "status": status, "assignee": "org-x",
            "block_kind": block_kind, "active_run": active_run,
            "created_at": NOW - 5000, "last_activity": None}


def test_s2_recent_failure_not_masked_by_recent_success():
    # Recent successful run AND recent crashed run on the same desk -> Error.
    tasks = [_task()]
    assert _desk_state_for_tasks(tasks, "completed", True)[0] == "error"


def test_s2_error_wins_over_recently_completed():
    # No open tasks; both signals present -> error (never recently_completed).
    assert _desk_state_for_tasks([], "completed", True)[0] == "error"


def test_s2_recently_completed_when_no_failure():
    assert _desk_state_for_tasks([], "completed", False)[0] == "recently_completed"


def test_s2_idle_when_no_signals():
    assert _desk_state_for_tasks([], None, False)[0] == "idle"


def test_s2_higher_live_states_beat_error():
    # Founder: higher live states (Awaiting Founder / Working / Blocked /
    # Reviewing / Queued) still outrank Error.
    assert _desk_state_for_tasks(
        [_task(status="todo")], "completed", True)[0] == "queued"
    assert _desk_state_for_tasks(
        [_task(status="blocked")], "completed", True)[0] == "blocked"
    assert _desk_state_for_tasks(
        [_task(status="blocked", block_kind="needs_input")], "completed", True)[0] \
        == "awaiting_founder"
    assert _desk_state_for_tasks(
        [_task(status="review")], "completed", True)[0] == "reviewing"
    assert _desk_state_for_tasks(
        [_task(active_run={"id": 1})], "completed", True)[0] == "working"


# ---------------------------------------------------------------------------
# S2 — dual-field run semantics (status AND outcome)
# ---------------------------------------------------------------------------

def test_s2_status_only_crash_is_a_failure():
    from plugin_api import _run_failed
    # Runtime can record failure in status without any outcome.
    assert _run_failed({"status": "crashed", "outcome": None}) is True
    assert _run_failed({"status": "timed_out", "outcome": None}) is True
    assert _run_failed({"status": "failed", "outcome": None}) is True


def test_s2_outcome_only_failure_is_a_failure():
    from plugin_api import _run_failed
    assert _run_failed({"status": "done", "outcome": "crashed"}) is True
    assert _run_failed({"status": "done", "outcome": "gave_up"}) is True
    assert _run_failed({"status": "done", "outcome": "spawn_failed"}) is True
    assert _run_failed({"status": "done", "outcome": "timed_out"}) is True


def test_s2_success_detection_both_fields():
    from plugin_api import _run_completed
    assert _run_completed({"status": "done", "outcome": None}) is True
    assert _run_completed({"status": "running", "outcome": "completed"}) is True
    assert _run_completed({"status": "running", "outcome": None}) is False
    assert _run_completed({"status": "released", "outcome": "reclaimed"}) is False


# ---------------------------------------------------------------------------
# S1 — handoff classification
# ---------------------------------------------------------------------------

def _h_task(status="done", last_activity=None, active_run=None, task_id="t"):
    return {"id": task_id, "status": status, "active_run": active_run,
            "last_activity": last_activity}


def test_s1_open_parent_is_active():
    parent = _h_task(status="running")
    child = _h_task(status="done", last_activity=NOW - 4000)
    assert _classify_handoff(parent, child, {}, NOW) == "active"


def test_s1_open_child_is_active():
    parent = _h_task(status="done", last_activity=NOW - 4000)
    child = _h_task(status="review")
    assert _classify_handoff(parent, child, {}, NOW) == "active"


def test_s1_live_worker_is_active():
    parent = _h_task(status="done", last_activity=NOW - 4000)
    child = _h_task(status="done", last_activity=NOW - 4000,
                    active_run={"id": 7})
    assert _classify_handoff(parent, child, {}, NOW) == "active"


def test_s1_recent_activity_is_recent():
    parent = _h_task(status="done", last_activity=NOW - 60)
    child = _h_task(status="done", last_activity=NOW - 4000)
    assert _classify_handoff(parent, child, {}, NOW) == "recent"


def test_s1_recent_finished_run_is_recent():
    parent = _h_task(status="done", last_activity=NOW - 4000)
    child = _h_task(status="done", last_activity=NOW - 4000)
    runs = {"t": [{"ended_at": NOW - 120}]}
    assert _classify_handoff(parent, child, runs, NOW) == "recent"


def test_s1_both_closed_no_recent_activity_is_historical():
    parent = _h_task(status="done", last_activity=NOW - 4000)
    child = _h_task(status="archived", last_activity=NOW - 9000)
    assert _classify_handoff(parent, child, {}, NOW) == "historical"


def test_s1_window_boundary_is_documented():
    assert _HANDOFF_RECENT_WINDOW == 1800  # 30 minutes — matches source map


# ---------------------------------------------------------------------------
# Phase 3.1 — R2 WS auth FAIL-CLOSED / R3 profile filter BEFORE LIMIT
# ---------------------------------------------------------------------------

def test_r2_ws_auth_accepts_when_helper_ok(monkeypatch):
    import types
    fake = types.SimpleNamespace(_ws_auth_ok=lambda ws: True)
    monkeypatch.setitem(sys.modules, "hermes_cli.web_server", fake)
    from plugin_api import _ws_authorized
    assert _ws_authorized(object()) is True


def test_r2_ws_auth_rejects_when_helper_denies(monkeypatch):
    import types
    fake = types.SimpleNamespace(_ws_auth_ok=lambda ws: False)
    monkeypatch.setitem(sys.modules, "hermes_cli.web_server", fake)
    from plugin_api import _ws_authorized
    assert _ws_authorized(object()) is False


def test_r2_ws_auth_rejects_when_helper_raises(monkeypatch):
    """Fail-CLOSED: auth-helper exception must NOT become authorization."""
    import types

    def boom(ws):
        raise RuntimeError("auth subsystem broken")

    fake = types.SimpleNamespace(_ws_auth_ok=boom)
    monkeypatch.setitem(sys.modules, "hermes_cli.web_server", fake)
    from plugin_api import _ws_authorized
    assert _ws_authorized(object()) is False


def test_r2_ws_auth_rejects_when_module_missing(monkeypatch):
    """Fail-CLOSED: helper module unavailable must reject, not allow."""
    monkeypatch.setitem(sys.modules, "hermes_cli.web_server", None)  # None => ImportError
    from plugin_api import _ws_authorized
    assert _ws_authorized(object()) is False


def test_r3_activity_profile_filter_before_limit():
    """R3 contract: profile filter applies BEFORE LIMIT — a target-profile
    event must survive even when >N newer events exist for other profiles."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE tasks (id TEXT PRIMARY KEY, title TEXT, assignee TEXT, status TEXT)")
    conn.execute("CREATE TABLE task_events (id INTEGER PRIMARY KEY, task_id TEXT, run_id TEXT,"
                 " kind TEXT, payload TEXT, created_at REAL)")
    conn.execute("INSERT INTO tasks VALUES ('t_target', 'target task', 'org-equity-analyst', 'todo')")
    conn.execute("INSERT INTO tasks VALUES ('t_noise', 'noise task', 'org-cos', 'todo')")
    conn.execute("INSERT INTO task_events VALUES (1, 't_target', NULL, 'created', NULL, 1000.0)")
    for i in range(20):
        conn.execute("INSERT INTO task_events VALUES (?, 't_noise', NULL, 'created', NULL, ?)",
                     (2 + i, 2000.0 + i))
    conn.commit()
    from plugin_api import LiveOfficeDataAdapter
    adapter = LiveOfficeDataAdapter("test")
    events = adapter.recent_events(conn, limit=8, profile="org-equity-analyst")
    assert len(events) == 1 and events[0]["task_id"] == "t_target", \
        "target-profile event must survive other desks' newer noise"
    # global path unchanged: newest 8 across the board
    global_events = adapter.recent_events(conn, limit=8)
    assert len(global_events) == 8 and all(e["task_id"] == "t_noise" for e in global_events)
    conn.close()


def test_r3_archived_task_events_included_in_drawer_history():
    """Documented rule: archived-task events ARE part of the desk's recent
    history (audit trail, consistent with handoffs include-archived)."""
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE tasks (id TEXT PRIMARY KEY, title TEXT, assignee TEXT, status TEXT)")
    conn.execute("CREATE TABLE task_events (id INTEGER PRIMARY KEY, task_id TEXT, run_id TEXT,"
                 " kind TEXT, payload TEXT, created_at REAL)")
    conn.execute("INSERT INTO tasks VALUES ('t_arch', 'archived probe', 'org-cro', 'archived')")
    conn.execute("INSERT INTO task_events VALUES (1, 't_arch', NULL, 'created', NULL, 1000.0)")
    conn.commit()
    from plugin_api import LiveOfficeDataAdapter
    adapter = LiveOfficeDataAdapter("test")
    events = adapter.recent_events(conn, limit=8, profile="org-cro")
    assert len(events) == 1 and events[0]["task_id"] == "t_arch"
    conn.close()

def test_s4_profiles_dir_resolves_and_contains_all_11_desks():
    root = _profiles_dir()
    assert root.exists() and root.is_dir()
    expected = {"org-cos", "org-ic-secretary", "org-commodity-analyst",
                "org-macro-strategist", "org-equity-analyst",
                "org-options-strategist", "org-cro", "org-quant-validator",
                "org-data-steward", "org-auditor", "org-radar-scout"}
    installed = {p.name for p in root.glob("org-*") if p.is_dir()}
    assert expected <= installed


# ---------------------------------------------------------------------------
# S1 — archived tasks stay in the handoff classification universe
# ---------------------------------------------------------------------------

def test_s1_load_board_include_archived_is_a_superset():
    # The /handoffs route reads with include_archived=True so completed/archived
    # relationships remain classifiable (S1 "both sides completed/archived").
    # Read-only check against the live board — must return at least as many
    # tasks as the operational view.
    from plugin_api import LiveOfficeDataAdapter
    adapter = LiveOfficeDataAdapter(board="iip")
    base = adapter.load_board()["tasks"]
    full = adapter.load_board(include_archived=True)["tasks"]
    assert len(full) >= len(base)
    base_ids = {t["id"] for t in base}
    assert base_ids <= {t["id"] for t in full}
