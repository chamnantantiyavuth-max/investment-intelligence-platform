"""QAD M6.3 — PUBLIC SUCCESS API HARDENING (FD #155, Path H) — acceptance suite.

FD #155 (14 Oct 2026) amends the accepted M6.3 contract so that NO standalone SUCCESS
write can be produced through the two supported generic PUBLIC mutation APIs:

* ``DeepResearchRunLedgerStore.append_attempt(outcome=SUCCESS)``      -> REFUSED
* ``DeepResearchRunLedgerStore.terminalize(terminal_status=SUCCESS)`` -> REFUSED

Every NEW SUCCESS write must go through FD #153's atomic finalizer
(``finalize_success_attempt_atomic``), which records the exact final SUCCESS attempt AND
the SUCCESS terminal result binding (+ both audit events) in ONE SQLite transaction.

Scope of the claim (Founder-set, honest): this is scoped to SUPPORTED PUBLIC APIs. It does
NOT claim to prevent deliberate raw SQLite corruption, private-helper abuse, or hostile
arbitrary in-process code execution. Legacy malformed records stay invalid and untrusted and
are never silently repaired. No schema expansion or migration is authorized — the attempt
table still carries no result-hash column, the table set is unchanged and no new SQLite
trigger exists (canonical schema count stays 68).

This module performs NO provider execution — no Gemini, no Notebook, no browser/CDP, no
network, no credentials. Everything is deterministic fixtures.
"""

from __future__ import annotations

import ast
import datetime as dt
import sqlite3
from pathlib import Path

import pytest

from qad.contract.canonical_boundary import CANONICAL_SCHEMAS
from qad.m6.ledger import (
    CANONICAL_SCHEMA_COUNT,
    CandidateDisposition,
    DeepResearchRunLedgerStore,
    LedgerError,
    LedgerIdentityConflict,
    LedgerTerminalError,
    LedgerValidationError,
    RetryMode,
    TelemetryStatus,
    TerminalStatus,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
_FIXED_NOW = dt.datetime(2026, 10, 14, 12, 0, 0, tzinfo=dt.timezone.utc)

_BROWSER = "BROWSER_UI_AUTOMATION"
_SURFACE = "gemini_notebook"

#: The exact pre-FD-#155 persistence shape. FD #155 is a PUBLIC API semantics correction
#: and adds NO table, NO column and NO trigger.
_FROZEN_LEDGER_TABLES = frozenset({
    "ledger_attempt", "ledger_candidate", "ledger_disposition",
    "ledger_event", "ledger_run", "ledger_terminal",
})
_FROZEN_TRIGGERS = frozenset({
    "ledger_run_immutable_update", "ledger_run_immutable_delete",
    "ledger_attempt_immutable_update", "ledger_attempt_immutable_delete",
    "ledger_candidate_immutable_update", "ledger_candidate_immutable_delete",
    "ledger_disposition_immutable_update", "ledger_disposition_immutable_delete",
    "ledger_terminal_immutable_update", "ledger_terminal_immutable_delete",
    "ledger_event_immutable_update", "ledger_event_immutable_delete",
    "ledger_run_no_replace", "ledger_event_no_replace", "ledger_event_terminal_backed",
    "ledger_attempt_guard_insert", "ledger_candidate_guard_insert",
    "ledger_disposition_guard_insert", "ledger_terminal_guard_insert",
    "ledger_attempt_telemetry_guard",
})


# =====================================================================
# Helpers (deterministic fixtures — mirror the M6.3 suite conventions)
# =====================================================================


def _clock() -> dt.datetime:
    return _FIXED_NOW


def _store(tmp_path: Path, name: str = "ledger.sqlite3") -> DeepResearchRunLedgerStore:
    return DeepResearchRunLedgerStore(tmp_path / name, clock=_clock)


def _create(store: DeepResearchRunLedgerStore, ledger_id: str = "L-001") -> str:
    return store.create_run(
        ledger_id=ledger_id,
        research_run_id="RR-001",
        rrm_manifest_id="RRM-2026-0001",
        case_id="CASE-2026-001",
        case_version="v1",
        evidence_gap_id="EG-001",
        request_id="REQ-001",
        idempotency_key="IDEM-001",
        notebook_identity="nb-01930000-0000-7000-8000-000000000001",
        pit_context_id="PITC-001",
        pit_mode="SEALED_HISTORICAL_EVALUATION",
        as_of="2026-10-01",
        input_snapshot_hash="a" * 64,
        provider_surface=_SURFACE,
        transport_type=_BROWSER,
    )


def _tel(**overrides) -> dict:
    """A complete, truthful contract telemetry record (M6.0 §7.2)."""
    base = {
        m: {"status": "NOT_EXPOSED", "value": None, "reason": "NOT_EXPOSED_BY_PROVIDER"}
        for m in ("model_identity", "prompt_tokens", "completion_tokens",
                  "cost", "model_version")
    }
    base.update(overrides)
    return base


def _append(store, ledger_id="L-001", n=1, **kw):
    base = dict(
        attempt_number=n,
        retry_mode=RetryMode.INITIAL_ATTEMPT,
        provider_surface=_SURFACE,
        transport_type=_BROWSER,
        telemetry=_tel(),
    )
    if "mode" in kw:  # convenience alias used by the retry-mode cases below
        base["retry_mode"] = kw.pop("mode")
    base.update(kw)
    return store.append_attempt(ledger_id, **base)


def _finalize_success(store, ledger_id="L-001", n=1, **kw):
    """The ONLY supported public NEW-SUCCESS write after FD #155."""
    base = dict(
        attempt_number=n,
        retry_mode=RetryMode.INITIAL_ATTEMPT,
        provider_surface=_SURFACE,
        transport_type=_BROWSER,
        result_sha256="b" * 64,
        telemetry=_tel(),
    )
    base.update(kw)
    return store.finalize_success_attempt_atomic(ledger_id, **base)


def _candidate(store, ledger_id="L-001", cid="C-1", **kw):
    base = dict(
        source_candidate_id=cid,
        url_or_identifier="https://example.com/a",
        discovery_timestamp="2026-10-14T12:00:00+00:00",
        original_source_verification_status="VERIFIED",
        pit_eligibility="ELIGIBLE",
    )
    base.update(kw)
    return store.register_candidate(ledger_id, **base)


def _dispose(store, ledger_id="L-001", cid="C-1",
             disp=CandidateDisposition.IMPORTED, **kw):
    return store.dispose_candidate(
        ledger_id, cid, disposition=disp, reason="unit-test disposition", **kw
    )


def _query(path: Path, sql: str, params=()) -> list[tuple]:
    conn = sqlite3.connect(str(path))
    try:
        return [tuple(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def _scalar(path: Path, sql: str, params=()) -> int:
    return _query(path, sql, params)[0][0]


def _attempt_count(path: Path) -> int:
    return _scalar(path, "SELECT COUNT(*) FROM ledger_attempt WHERE ledger_id = ?", ("L-001",))


def _event_count(path: Path) -> int:
    return _scalar(path, "SELECT COUNT(*) FROM ledger_event WHERE ledger_id = ?", ("L-001",))


def _terminal_count(path: Path) -> int:
    return _scalar(path, "SELECT COUNT(*) FROM ledger_terminal WHERE ledger_id = ?", ("L-001",))


def _fixture_state(store, path: Path) -> dict:
    """A complete ordered fingerprint of the durable run state."""
    rec = store.load_run("L-001")
    return {
        "attempts": [(a.attempt_number, a.outcome, a.retry_mode.value,
                      a.provider_surface, a.transport_type) for a in rec.attempts],
        "candidates": [(c.source_candidate_id, c.url_or_identifier,
                        c.original_source_verification_status, c.pit_eligibility)
                       for c in rec.candidates],
        "dispositions": [(d.source_candidate_id, d.disposition.value, d.reason)
                         for d in rec.dispositions],
        "events": [tuple(e) for e in store.events("L-001")],
        "terminal_status": rec.terminal_status,
        "is_terminal": rec.is_terminal,
        "result_sha256": rec.result_sha256,
        "raw_attempts": _query(
            path,
            "SELECT attempt_number, outcome, retry_mode FROM ledger_attempt"
            " WHERE ledger_id = ? ORDER BY attempt_number", ("L-001",)),
        "raw_events": _query(
            path, "SELECT seq, event_type FROM ledger_event WHERE ledger_id = ? ORDER BY seq",
            ("L-001",)),
    }


class _FailOn:
    """Connection proxy raising when a statement CONTAINS ``needle`` (injection seam)."""

    def __init__(self, conn, needle: str):
        self._conn = conn
        self._needle = needle

    def execute(self, sql, *a, **kw):
        if self._needle in sql:
            raise RuntimeError(f"INJECTED FAILURE on {self._needle!r}")
        return self._conn.execute(sql, *a, **kw)

    def __getattr__(self, item):
        return getattr(self._conn, item)


def _inject(monkeypatch, store, needle: str) -> None:
    real = store._connect
    monkeypatch.setattr(
        store, "_connect", lambda: _FailOn(real(), needle), raising=False
    )


# =====================================================================
# 1-4 / 9-10 : generic append_attempt refuses a standalone SUCCESS
# =====================================================================


class TestAppendAttemptRefusesStandaloneSuccess:
    def test_01_append_attempt_refuses_enum_success(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError) as ei:
            _append(store, "L-001", n=1, outcome=TerminalStatus.SUCCESS,
                    completed_at=_FIXED_NOW.isoformat())
        # typed, repository-consistent contract exception
        assert isinstance(ei.value, LedgerError)
        # and it says exactly what the caller must use instead
        assert "finalize_success_attempt_atomic" in str(ei.value)

    def test_02_append_attempt_refuses_string_success(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError) as ei:
            _append(store, "L-001", n=1, outcome="SUCCESS",
                    completed_at=_FIXED_NOW.isoformat())
        assert "finalize_success_attempt_atomic" in str(ei.value)

    def test_03_rejected_append_leaves_zero_new_attempts(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        for outcome in (TerminalStatus.SUCCESS, "SUCCESS"):
            with pytest.raises(LedgerValidationError):
                _append(store, "L-001", n=1, outcome=outcome)
        assert _attempt_count(path) == 0
        assert store.load_run("L-001").attempts == ()

    def test_04_rejected_append_leaves_zero_new_audit_events(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        before_count = _event_count(path)
        before_events = [tuple(e) for e in store.events("L-001")]
        for outcome in (TerminalStatus.SUCCESS, "SUCCESS"):
            with pytest.raises(LedgerValidationError):
                _append(store, "L-001", n=1, outcome=outcome)
        assert _event_count(path) == before_count
        assert [tuple(e) for e in store.events("L-001")] == before_events
        assert all(e[1] != "ATTEMPT_APPENDED" for e in before_events)

    def test_09_prior_attempts_unchanged_after_rejected_append(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.FAILED,
                error="boom", completed_at=_FIXED_NOW.isoformat())
        before = _fixture_state(store, path)
        with pytest.raises(LedgerValidationError):
            _append(store, "L-001", n=2, outcome=TerminalStatus.SUCCESS)
        assert _fixture_state(store, path) == before
        assert [a.outcome for a in store.load_run("L-001").attempts] == ["FAILED"]

    def test_10_candidate_and_disposition_state_unchanged_after_rejection(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _candidate(store, "L-001", cid="C-1")
        _dispose(store, "L-001", cid="C-1", disp=CandidateDisposition.REJECTED)
        before = _fixture_state(store, path)
        with pytest.raises(LedgerValidationError):
            _append(store, "L-001", n=1, outcome=TerminalStatus.SUCCESS)
        with pytest.raises(LedgerValidationError):
            store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS,
                              result_sha256="b" * 64)
        assert _fixture_state(store, path) == before
        rec = store.load_run("L-001")
        assert [c.source_candidate_id for c in rec.candidates] == ["C-1"]
        assert [d.disposition for d in rec.dispositions] == [CandidateDisposition.REJECTED]


# =====================================================================
# 5-8 / 10 : generic terminalize refuses SUCCESS
# =====================================================================


class TestTerminalizeRefusesSuccess:
    def test_05_terminalize_refuses_enum_success(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError) as ei:
            store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        assert isinstance(ei.value, LedgerError)
        assert "finalize_success_attempt_atomic" in str(ei.value)

    def test_06_terminalize_refuses_string_success(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError) as ei:
            store.terminalize("L-001", terminal_status="SUCCESS")
        assert "finalize_success_attempt_atomic" in str(ei.value)

    def test_07_non_empty_result_binding_does_not_bypass_rejection(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        cases = (
            dict(result_sha256="a" * 64),
            dict(result_artifact_ref="artifact://dr/report"),
            dict(result_sha256="a" * 64, result_artifact_ref="artifact://dr/report"),
        )
        for kw in cases:
            for status in (TerminalStatus.SUCCESS, "SUCCESS"):
                with pytest.raises(LedgerValidationError):
                    store.terminalize("L-001", terminal_status=status, **kw)
        assert _terminal_count(path) == 0
        assert store.load_run("L-001").terminal_status is None

    def test_08_rejected_terminalize_leaves_no_terminal_record(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.FAILED,
                completed_at=_FIXED_NOW.isoformat())
        before = _fixture_state(store, path)
        for status in (TerminalStatus.SUCCESS, "SUCCESS"):
            with pytest.raises(LedgerValidationError):
                store.terminalize("L-001", terminal_status=status)
        assert _terminal_count(path) == 0
        assert store.load_run("L-001").terminal_status is None
        assert store.load_run("L-001").is_terminal is False
        assert _fixture_state(store, path) == before


# =====================================================================
# 11-17 : FD #153 atomic finalizer retained (the ONLY new-SUCCESS path)
# =====================================================================


class TestAtomicFinalizerRetained:
    def test_11_atomic_success_finalization_still_accepted(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        _finalize_success(store, "L-001", n=1, result_artifact_ref="artifact://dr/r")
        rec = store.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.SUCCESS
        assert rec.is_terminal is True
        assert rec.result_artifact_ref == "artifact://dr/r"
        assert rec.result_sha256 == "b" * 64

    def test_12_atomic_writes_exactly_one_attempt_and_one_terminal(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _finalize_success(store, "L-001", n=1)
        rec = store.load_run("L-001")
        assert len(rec.attempts) == 1
        assert rec.attempts[0].outcome == TerminalStatus.SUCCESS.value
        assert _attempt_count(path) == 1
        assert _terminal_count(path) == 1
        kinds = [e[1] for e in store.events("L-001")]
        assert kinds.count("ATTEMPT_APPENDED") == 1
        assert kinds.count("RUN_TERMINALIZED") == 1

    def test_13_exact_result_binding_persists_after_process_reopen(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _finalize_success(store, "L-001", n=1,
                          result_artifact_ref="artifact://dr/report-xyz",
                          result_sha256="c" * 64)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.SUCCESS
        assert rec.result_sha256 == "c" * 64
        assert rec.result_artifact_ref == "artifact://dr/report-xyz"
        assert [a.outcome for a in rec.attempts] == [TerminalStatus.SUCCESS.value]

    def test_14_atomic_candidate_disposition_prerequisite_still_enforced(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _candidate(store, "L-001", cid="C-1")  # registered, deliberately NOT disposed
        with pytest.raises(LedgerValidationError):
            _finalize_success(store, "L-001", n=1)
        assert _attempt_count(path) == 0
        assert _terminal_count(path) == 0
        assert store.load_run("L-001").is_terminal is False
        # disposing the candidate unblocks the SAME atomic call
        _dispose(store, "L-001", cid="C-1")
        _finalize_success(store, "L-001", n=1)
        assert store.load_run("L-001").terminal_status is TerminalStatus.SUCCESS

    def test_15_injected_failure_rolls_back_both_records_and_events(
        self, tmp_path, monkeypatch
    ):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        before = _fixture_state(store, path)
        _inject(monkeypatch, store, "COMMIT")
        with pytest.raises(RuntimeError, match="INJECTED FAILURE"):
            _finalize_success(store, "L-001", n=1)
        monkeypatch.undo()
        assert _attempt_count(path) == 0
        assert _terminal_count(path) == 0
        assert _fixture_state(store, path) == before
        rec = store.load_run("L-001")
        assert rec.attempts == ()
        assert rec.is_terminal is False
        assert rec.result_sha256 is None
        assert all(e[1] != "ATTEMPT_APPENDED" for e in store.events("L-001"))
        # the run is still fully usable afterwards
        _finalize_success(store, "L-001", n=1)
        assert store.load_run("L-001").terminal_status is TerminalStatus.SUCCESS

    def test_16_second_atomic_finalization_of_a_terminal_run_refused(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _finalize_success(store, "L-001", n=1)
        before = _fixture_state(store, path)
        with pytest.raises(LedgerTerminalError):
            _finalize_success(store, "L-001", n=2, result_sha256="d" * 64)
        assert _fixture_state(store, path) == before
        assert store.load_run("L-001").result_sha256 == "b" * 64

    def test_17_post_terminal_append_candidate_and_disposition_refused(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _candidate(store, "L-001", cid="C-1")
        _dispose(store, "L-001", cid="C-1")
        _finalize_success(store, "L-001", n=1)
        before = _fixture_state(store, path)
        with pytest.raises(LedgerTerminalError):
            _append(store, "L-001", n=2, outcome=TerminalStatus.FAILED)
        with pytest.raises(LedgerTerminalError):
            _candidate(store, "L-001", cid="C-2")
        with pytest.raises(LedgerTerminalError):
            _dispose(store, "L-001", cid="C-1", disp=CandidateDisposition.UNAVAILABLE)
        assert _fixture_state(store, path) == before

    def test_17b_non_success_attempt_identity_and_ordering_still_enforced(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.FAILED)
        with pytest.raises(LedgerIdentityConflict):
            _append(store, "L-001", n=1, outcome=TerminalStatus.FAILED)
        with pytest.raises(LedgerValidationError):
            _append(store, "L-001", n=0, outcome=TerminalStatus.FAILED)
        assert [a.attempt_number for a in store.load_run("L-001").attempts] == [1]


# =====================================================================
# 18-20 : non-SUCCESS behaviour preserved exactly
# =====================================================================


class TestNonSuccessPathsRetained:
    def test_18_failed_attempt_recording_still_accepted(self, tmp_path):
        store = _store(tmp_path)
        path = tmp_path / "ledger.sqlite3"
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.FAILED,
                error="boom", completed_at=_FIXED_NOW.isoformat())
        rec = store.load_run("L-001")
        assert len(rec.attempts) == 1
        assert rec.attempts[0].outcome == TerminalStatus.FAILED.value
        assert rec.attempts[0].error == "boom"
        assert _attempt_count(path) == 1
        # telemetry truthfulness preserved
        m = rec.attempts[0].telemetry["model_identity"]
        assert m.status is TelemetryStatus.NOT_EXPOSED
        assert m.value is None and m.reason == "NOT_EXPOSED_BY_PROVIDER"

    def test_19_transport_failure_terminalization_still_accepted(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.TRANSPORT_FAILURE,
                error="CSRF token not found")
        store.terminalize("L-001", terminal_status=TerminalStatus.TRANSPORT_FAILURE,
                          failure_detail="CSRF token not found")
        rec = store.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.TRANSPORT_FAILURE
        assert rec.failure_detail == "CSRF token not found"
        assert rec.result_sha256 is None

    def test_20_research_unavailable_terminalization_still_accepted(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        _append(store, "L-001", n=1, outcome=TerminalStatus.TRANSPORT_FAILURE)
        _append(store, "L-001", n=2, mode=RetryMode.SAME_PROVIDER_RETRY,
                outcome=TerminalStatus.TRANSPORT_FAILURE)
        store.terminalize("L-001", terminal_status=TerminalStatus.RESEARCH_UNAVAILABLE,
                          failure_detail="budget exhausted")
        rec = store.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.RESEARCH_UNAVAILABLE
        assert [a.attempt_number for a in rec.attempts] == [1, 2]

    def test_20b_unknown_outcome_and_unknown_status_still_rejected(self, tmp_path):
        store = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError):
            _append(store, "L-001", n=1, outcome="NOT_A_STATUS")
        with pytest.raises(LedgerValidationError):
            store.terminalize("L-001", terminal_status="NOT_A_STATUS")
        assert store.load_run("L-001").attempts == ()
        assert store.load_run("L-001").terminal_status is None


# =====================================================================
# 22 / 24 / 25 : source-level confinement + frozen persistence shape
# =====================================================================

_PUBLIC_SUCCESS_WRITERS = frozenset({"append_attempt", "terminalize"})


def _public_success_call_sites(tree: ast.AST) -> list[tuple[int, str]]:
    """Calls to the two generic public mutators that carry a SUCCESS value."""
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else (
            fn.id if isinstance(fn, ast.Name) else None)
        if name not in _PUBLIC_SUCCESS_WRITERS:
            continue
        for arg in list(node.args) + [k.value for k in node.keywords]:
            if isinstance(arg, ast.Attribute) and arg.attr == "SUCCESS":
                found.append((node.lineno, name))
            elif isinstance(arg, ast.Constant) and arg.value == "SUCCESS":
                found.append((node.lineno, name))
    return found


def _called_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for inner in ast.walk(node):
        if isinstance(inner, ast.Call):
            f = inner.func
            names.add(f.attr if isinstance(f, ast.Attribute)
                      else getattr(f, "id", "?"))
    return names


class TestSourceConfinement:
    def test_22_m65_and_m66_never_invoke_standalone_generic_success_apis(self):
        """The accepted SUCCESS writer must be the atomic finalizer, only."""
        orch = ast.parse((REPO_ROOT / "qad" / "m6" / "orchestration.py")
                         .read_text(encoding="utf-8"))
        assert _public_success_call_sites(orch) == []

        accept_calls: set[str] = set()
        for node in ast.walk(orch):
            if isinstance(node, ast.FunctionDef) and node.name == "accept_success_result":
                accept_calls = _called_names(node)
        assert "finalize_success_attempt_atomic" in accept_calls
        assert not ({"append_attempt", "terminalize"} & accept_calls)

        # M6.6 bridge never writes SUCCESS at all (FD #154 condition, still true)
        bridge = ast.parse((REPO_ROOT / "qad" / "m6" / "source_bridge.py")
                           .read_text(encoding="utf-8"))
        assert _public_success_call_sites(bridge) == []
        assert "finalize_success_attempt_atomic" not in _called_names(bridge)

    def test_24_no_standalone_success_writer_remains_in_production_code(self):
        """Supported-public-API call-site audit over PRODUCTION code only.

        Negative regression tests legitimately call the guarded APIs with SUCCESS inside
        ``pytest.raises``; the audit therefore covers production modules (everything under
        ``qad/``), not the test tree.
        """
        offenders: list[str] = []
        scanned = 0
        for path in sorted((REPO_ROOT / "qad").rglob("*.py")):
            scanned += 1
            rel = path.relative_to(REPO_ROOT).as_posix()
            for lineno, name in _public_success_call_sites(
                ast.parse(path.read_text(encoding="utf-8"))
            ):
                offenders.append(f"{rel}:{lineno}:{name}")
        assert scanned > 0
        assert offenders == []

        # the two guards are enforced by the API itself (not by caller discipline)
        ledger_src = (REPO_ROOT / "qad" / "m6" / "ledger.py").read_text(encoding="utf-8")
        assert "append_attempt refuses a standalone SUCCESS attempt (FD #155)" in ledger_src
        assert "terminalize refuses terminal_status=SUCCESS (FD #155)" in ledger_src

    def test_25_canonical_schema_count_remains_68(self):
        assert len(CANONICAL_SCHEMAS) == CANONICAL_SCHEMA_COUNT == 68

    def test_25b_persistence_shape_is_unchanged(self, tmp_path):
        """No new table, no result-binding column, no new trigger, no migration."""
        store = _store(tmp_path)
        _create(store)
        path = tmp_path / "ledger.sqlite3"

        tables = frozenset(
            r[0] for r in _query(
                path, "SELECT name FROM sqlite_master WHERE type='table'")
        )
        assert {t for t in tables if t.startswith("ledger_")} == _FROZEN_LEDGER_TABLES

        triggers = frozenset(
            r[0] for r in _query(
                path, "SELECT name FROM sqlite_master WHERE type='trigger'")
        )
        assert triggers == _FROZEN_TRIGGERS

        attempt_cols = {r[1] for r in _query(path, "PRAGMA table_info(ledger_attempt)")}
        assert "result_sha256" not in attempt_cols
        assert "result_artifact_ref" not in attempt_cols
        terminal_cols = {r[1] for r in _query(path, "PRAGMA table_info(ledger_terminal)")}
        assert {"result_artifact_ref", "result_sha256"} <= terminal_cols
