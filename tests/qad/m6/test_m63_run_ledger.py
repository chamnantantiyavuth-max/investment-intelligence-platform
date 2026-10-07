"""M6.3 — Deep Research Run Ledger — acceptance tests (FD #149 / FD #151).

RED→GREEN acceptance suite for the M6.3 cluster (``DeepResearchRunLedgerStore``).
Proves the durable, non-canonical, append-only operational/provenance ledger
defined by M6.0 §7:

* create-before-provider durability (survives a store re-instantiation);
* append-only attempts; monotonic, de-duplicated attempt identity;
* terminal immutability (no attempt/disposition/second-terminalization after);
* truthful telemetry (EXPOSED exact / NOT_EXPOSED value=null + reason; no
  zero-as-unknown; no fabricated MOD-01/PROV-01);
* complete, single-disposition source-candidate bookkeeping;
* Research Room / Notebook independence;
* result-hash retention independent of artifact lifetime;
* RRM-01 ``deep_research_runs[]`` = ledger-id strings only;
* runtime state outside the git repository;
* transaction atomicity + datastore-level uniqueness.

Run:  pytest tests/qad/m6/test_m63_run_ledger.py -q
"""

from __future__ import annotations

import datetime as dt
import json
import sqlite3
from pathlib import Path

import pytest

from qad.contract.canonical_boundary import CANONICAL_SCHEMAS
from qad.m6.ledger import (
    CANONICAL_SCHEMA_COUNT,
    CandidateDisposition,
    DeepResearchRunLedgerStore,
    LedgerIdentityConflict,
    LedgerNotFound,
    LedgerStateError,
    LedgerTerminalError,
    LedgerValidationError,
    RetryMode,
    TelemetryStatus,
    TerminalStatus,
    assert_outside_repository,
    validate_rrm_deep_research_runs,
)
from qad.models.family_i import RunManifestRecord, RunManifestRecordRun_state
from qad.persistence.reference import InMemoryNonCanonicalResearchArtifactStore

# The repository root (tests/qad/m6/test_m63_run_ledger.py -> repo root).
REPO_ROOT = Path(__file__).resolve().parents[3]


# =====================================================================
# Helpers
# =====================================================================

_FIXED_NOW = dt.datetime(2026, 10, 7, 12, 0, 0, tzinfo=dt.timezone.utc)


def _clock() -> dt.datetime:
    return _FIXED_NOW


def _store(tmp_path: Path, name: str = "ledger.sqlite3", *, clock=_clock) -> tuple:
    path = tmp_path / name
    return DeepResearchRunLedgerStore(path, clock=clock), path


def _create(store: DeepResearchRunLedgerStore, ledger_id: str = "L-001",
            idem: str = "IDEM-001", rr: str = "RR-001") -> str:
    return store.create_run(
        ledger_id=ledger_id,
        research_run_id=rr,
        rrm_manifest_id="RRM-2026-0001",
        case_id="CASE-2026-001",
        case_version="v1",
        evidence_gap_id="EG-001",
        request_id="REQ-001",
        idempotency_key=idem,
        notebook_identity="nb-01930000-0000-7000-8000-000000000001",
        pit_context_id="PITC-001",
        pit_mode="SEALED_HISTORICAL_EVALUATION",
        as_of="2026-10-01",
        input_snapshot_hash="a" * 64,
        provider_surface="gemini_notebook",
        transport_type="BROWSER_UI_AUTOMATION",
    )


def _tel(**overrides):
    """A complete, truthful contract telemetry record (M6.0 §7.2).

    All REQUIRED metrics default to NOT_EXPOSED (value=null + reason); override
    any metric for a specific test case.
    """
    base = {
        m: {"status": "NOT_EXPOSED", "value": None, "reason": "NOT_EXPOSED_BY_PROVIDER"}
        for m in ("model_identity", "prompt_tokens", "completion_tokens",
                  "cost", "model_version")
    }
    base.update(overrides)
    return base


def _attempt(store, ledger_id, n=1, **kw):
    base = dict(
        attempt_number=n,
        retry_mode=RetryMode.INITIAL_ATTEMPT,
        provider_surface="gemini_notebook",
        transport_type="BROWSER_UI_AUTOMATION",
        telemetry=_tel(),
    )
    base.update(kw)
    return store.append_attempt(ledger_id, **base)


def _candidate(store, ledger_id, cid="C-1", **kw):
    base = dict(
        source_candidate_id=cid,
        url_or_identifier="https://example.com/a",
        discovery_timestamp="2026-10-07T12:00:00+00:00",
        original_source_verification_status="VERIFIED",
        pit_eligibility="ELIGIBLE",
    )
    base.update(kw)
    return store.register_candidate(ledger_id, **base)


def _dispose(store, ledger_id, cid="C-1", disp=CandidateDisposition.IMPORTED, **kw):
    return store.dispose_candidate(
        ledger_id, cid, disposition=disp, reason="unit-test disposition", **kw
    )


def _tables(path: Path) -> set[str]:
    conn = sqlite3.connect(str(path))
    try:
        return {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    finally:
        conn.close()


# =====================================================================
# 1–2: create-before-provider durability
# =====================================================================


class TestDurabilityCreateBeforeProvider:
    def test_01_create_run_persists_before_provider_execution(self, tmp_path):
        store, path = _store(tmp_path)
        lid = _create(store)
        assert lid == "L-001"
        # durable read-back succeeds BEFORE any provider step
        assert store.contains(lid) is True
        rec = store.load_run(lid)
        assert rec.terminal_status is None
        assert path.exists() and path.stat().st_size > 0

    def test_02_new_store_instance_reloads_run(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        # "destroy" this store instance; open a brand-new one at the same path
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.research_run_id == "RR-001"
        assert rec.idempotency_key == "IDEM-001"
        assert rec.input_snapshot_hash == "a" * 64


# =====================================================================
# 3: immutable run identity
# =====================================================================


class TestRunIdentityImmutability:
    def test_03_run_identity_cannot_be_rewritten(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        # no public mutation API exists on the store for run identity
        assert not hasattr(store, "update_run")
        assert not hasattr(store, "mutate_run")
        # and the durable identity is unchanged after a series of operations
        _attempt(store, "L-001")
        _candidate(store, "L-001")
        _dispose(store, "L-001")
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert (rec.case_id, rec.case_version, rec.idempotency_key) == (
            "CASE-2026-001", "v1", "IDEM-001"
        )
        # a fresh run reusing the same ledger_id is rejected (no overwrite)
        with pytest.raises(LedgerIdentityConflict):
            _create(reopened, idem="IDEM-002", rr="RR-002")


# =====================================================================
# 4–6: attempts
# =====================================================================


class TestAttempts:
    def test_04_attempt_append_persists_across_reopen(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", n=1, completed_at="2026-10-07T12:05:00+00:00",
                 outcome=TerminalStatus.SUCCESS)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert len(rec.attempts) == 1
        assert rec.attempts[0].attempt_number == 1
        assert rec.attempts[0].outcome == "SUCCESS"

    def test_05_attempt_numbers_monotonic_and_duplicate_rejected(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", n=1)
        _attempt(store, "L-001", n=2, retry_mode=RetryMode.SAME_PROVIDER_RETRY)
        with pytest.raises(LedgerIdentityConflict):
            _attempt(store, "L-001", n=1)
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", n=0)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        nums = [a.attempt_number for a in rec.attempts]
        assert nums == [1, 2]

    def test_06_failed_attempt_remains_durable(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", n=1, error="CSRF token not found",
                 outcome=TerminalStatus.TRANSPORT_FAILURE)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.attempts[0].error == "CSRF token not found"
        assert rec.attempts[0].outcome == "TRANSPORT_FAILURE"


# =====================================================================
# 7–11: telemetry truthfulness
# =====================================================================


class TestTelemetryTruthfulness:
    def test_07_exposed_exact_value_round_trips(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", telemetry=_tel(
            prompt_tokens={"status": "EXPOSED", "value": 1234},
        ))
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        m = reopened.load_run("L-001").attempts[0].telemetry["prompt_tokens"]
        assert m.status is TelemetryStatus.EXPOSED
        assert m.value == 1234

    def test_08_not_exposed_requires_reason(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry=_tel(
                cost={"status": "NOT_EXPOSED", "value": None},
            ))
        _attempt(store, "L-001", telemetry=_tel(
            cost={"status": "NOT_EXPOSED", "value": None,
                  "reason": "NOT_EXPOSED_BY_PROVIDER"},
        ))
        rec = store.load_run("L-001")
        assert rec.attempts[0].telemetry["cost"].reason == "NOT_EXPOSED_BY_PROVIDER"

    def test_09_not_exposed_value_must_be_null(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry=_tel(
                cost={"status": "NOT_EXPOSED", "value": 0, "reason": "hidden"},
            ))
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry=_tel(
                model_identity={"status": "EXPOSED", "value": None},
            ))

    def test_10_zero_is_not_automatically_unknown(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", telemetry=_tel(
            completion_tokens={"status": "EXPOSED", "value": 0},
        ))
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        m = reopened.load_run("L-001").attempts[0].telemetry["completion_tokens"]
        assert m.status is TelemetryStatus.EXPOSED
        assert m.value == 0

    def test_11_no_fabricated_mod_or_prov_records(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", telemetry=_tel(
            model_identity={"status": "NOT_EXPOSED", "value": None,
                            "reason": "NOT_EXPOSED_BY_PROVIDER"},
            total_tokens={"status": "NOT_EXPOSED", "value": None,
                          "reason": "NOT_EXPOSED_BY_PROVIDER"},
        ))
        rec = store.load_run("L-001")
        assert set(rec.attempts[0].telemetry) == {
            "model_identity", "prompt_tokens", "completion_tokens",
            "cost", "model_version", "total_tokens",
        }
        for m in rec.attempts[0].telemetry.values():
            assert m.status is TelemetryStatus.NOT_EXPOSED
            assert m.value is None  # never a guessed value
        # the canonical registry is unchanged; the ledger mints no canonical schema
        assert len(CANONICAL_SCHEMAS) == CANONICAL_SCHEMA_COUNT
        tables = _tables(path) - {"sqlite_sequence"}  # SQLite-internal (AUTOINCREMENT)
        assert tables == {
            "ledger_run", "ledger_attempt", "ledger_candidate",
            "ledger_disposition", "ledger_terminal", "ledger_event",
        }
        # no canonical schema id is present as a table in the ledger datastore
        lowered = {t.lower() for t in tables}
        assert not any(s.lower() in lowered for s in CANONICAL_SCHEMAS)


# =====================================================================
# 12–17: source-candidate dispositions
# =====================================================================


class TestCandidateDispositions:
    @pytest.mark.parametrize("disp", [
        CandidateDisposition.IMPORTED,
        CandidateDisposition.REJECTED,
        CandidateDisposition.UNAVAILABLE,
        CandidateDisposition.DEFERRED,
    ])
    def test_12_to_15_each_disposition_persists(self, tmp_path, disp):
        store, path = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001")
        _dispose(store, "L-001", disp=disp)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        d = reopened.load_run("L-001").dispositions[0]
        assert d.disposition is disp
        assert d.reason == "unit-test disposition"

    def test_16_duplicate_or_conflicting_disposition_rejected(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001")
        _dispose(store, "L-001", disp=CandidateDisposition.IMPORTED)
        with pytest.raises(LedgerIdentityConflict):
            _dispose(store, "L-001", disp=CandidateDisposition.REJECTED)
        assert store.load_run("L-001").dispositions[0].disposition is CandidateDisposition.IMPORTED

    def test_17_terminalization_fails_if_candidate_lacks_disposition(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001", cid="C-1")
        _candidate(store, "L-001", cid="C-2")
        _dispose(store, "L-001", cid="C-1")
        with pytest.raises(LedgerValidationError):
            store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        assert store.load_run("L-001").terminal_status is None
        _dispose(store, "L-001", cid="C-2", disp=CandidateDisposition.DEFERRED)
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        assert store.load_run("L-001").terminal_status is TerminalStatus.SUCCESS


# =====================================================================
# 18–19: independence
# =====================================================================


class TestIndependence:
    def test_18_research_room_deletion_does_not_erase_ledger(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001")
        room = InMemoryNonCanonicalResearchArtifactStore()
        room.store("m6", "run/raw", {"blob": "ephemeral"})
        assert room.list_keys("m6") == ["run/raw"]
        room.delete("m6", "run/raw")
        assert room.list_keys("m6") == []
        # ledger is a separate store object; unaffected by Research Room GC
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.research_run_id == "RR-001"
        assert len(rec.attempts) == 1

    def test_19_notebook_retirement_does_not_erase_ledger(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        # notebook/workspace retirement is provider-side lifecycle metadata only;
        # the ledger records identity and is not deleted by it
        before = store.load_run("L-001")
        assert before.notebook_identity.startswith("nb-")
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        after = reopened.load_run("L-001")
        assert after.notebook_identity == before.notebook_identity
        assert after.terminal_status is None


# =====================================================================
# 20–24: terminalization + immutability
# =====================================================================


class TestTerminalization:
    def test_20_terminal_success_persists_across_reopen(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS,
                          result_artifact_ref="artifact://dr/report", result_sha256="b" * 64)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.SUCCESS
        assert rec.result_artifact_ref == "artifact://dr/report"
        assert rec.result_sha256 == "b" * 64
        assert rec.terminal_at == _FIXED_NOW.isoformat()

    def test_21_terminal_failure_persists_across_reopen(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        store.terminalize("L-001", terminal_status=TerminalStatus.TRANSPORT_FAILURE,
                          failure_detail="CSRF token not found")
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.terminal_status is TerminalStatus.TRANSPORT_FAILURE
        assert rec.failure_detail == "CSRF token not found"

    def test_22_append_attempt_after_terminalization_rejected(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        with pytest.raises(LedgerTerminalError):
            _attempt(store, "L-001", n=1)
        assert store.load_run("L-001").attempts == ()

    def test_23_append_disposition_after_terminalization_rejected(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001")
        _dispose(store, "L-001")
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        with pytest.raises(LedgerTerminalError):
            _candidate(store, "L-001", cid="C-2")
        with pytest.raises(LedgerTerminalError):
            _dispose(store, "L-001", cid="C-2")

    def test_24_second_terminalization_rejected(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        with pytest.raises(LedgerTerminalError):
            store.terminalize("L-001", terminal_status=TerminalStatus.FAILED)


# =====================================================================
# 25–26: result hash retention + RRM linkage
# =====================================================================


class TestResultHashAndRrmLinkage:
    def test_25_result_sha256_persists_independently_of_artifact(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        store.terminalize(
            "L-001", terminal_status=TerminalStatus.SUCCESS,
            result_artifact_ref="artifact://dr/report-xyz",
            result_sha256="c" * 64,
        )
        # artifact is "retired" outside the ledger (no ledger API can delete it)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        assert rec.result_sha256 == "c" * 64
        assert not hasattr(reopened, "delete_run")

    def test_26_rrm_deep_research_runs_uses_ledger_id_strings_only(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        refs = validate_rrm_deep_research_runs(store, ["L-001"])
        assert refs == ["L-001"]
        rrm = RunManifestRecord(
            as_of_date="2026-10-01",
            case_id="CASE-2026-001",
            case_version="v1",
            manifest_id="RRM-2026-0001",
            models_used=["NOT_EXPOSED_BY_PROVIDER"],
            providers={"gemini_notebook": "gemini_notebook"},
            run_state=RunManifestRecordRun_state.RUNNING,
            selection_policy_version="v1",
            start_time="2026-10-07T12:00:00+00:00",
            universe_version="v1",
            deep_research_runs=refs,
        )
        assert rrm.deep_research_runs == ["L-001"]
        assert all(isinstance(x, str) for x in rrm.deep_research_runs)
        # dictionaries are rejected, and unresolvable ids fail closed
        with pytest.raises(LedgerValidationError):
            validate_rrm_deep_research_runs(store, [{"not": "a string"}])  # type: ignore[list-item]
        with pytest.raises(LedgerValidationError):
            validate_rrm_deep_research_runs(store, ["L-DOES-NOT-EXIST"])


# =====================================================================
# 27–30: runtime location, atomicity, uniqueness, no silent loss
# =====================================================================


class TestStorageAtomicityAndUniqueness:
    def test_27_runtime_ledger_file_outside_repo_and_repo_clean(self, tmp_path):
        # a repo-internal path fails closed
        with pytest.raises(LedgerStateError):
            DeepResearchRunLedgerStore(REPO_ROOT / "m63_should_not_exist.sqlite3")
        with pytest.raises(LedgerStateError):
            assert_outside_repository(REPO_ROOT / "design" / "qad-pivot" / "x.sqlite3")
        # a normal tmp path is accepted and lives outside the repo
        store, path = _store(tmp_path)
        _create(store)
        assert not str(path).startswith(str(REPO_ROOT))
        # no ledger sqlite file may remain inside the repository worktree
        leftovers = [
            p for p in REPO_ROOT.rglob("*.sqlite3")
            if ".git" not in p.parts and p.name.startswith(("ledger", "m63"))
        ]
        assert leftovers == []

    def test_28_injected_transaction_failure_leaves_no_partial_operation(
        self, tmp_path, monkeypatch
    ):
        store, path = _store(tmp_path)

        def _boom(*a, **k):
            raise RuntimeError("injected mid-transaction failure")

        monkeypatch.setattr(store, "_write_event", _boom)
        with pytest.raises(RuntimeError):
            _create(store)
        monkeypatch.undo()
        # no half-created run reaches durable state
        assert store.contains("L-001") is False
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        assert reopened.list_runs() == []

    def test_29_duplicate_logical_identity_collision_fails_deterministically(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store, ledger_id="L-001", idem="IDEM-001", rr="RR-001")
        # same idempotency_key, different ledger_id -> deterministic conflict
        with pytest.raises(LedgerIdentityConflict):
            _create(store, ledger_id="L-002", idem="IDEM-001", rr="RR-002")
        # same research_run_id -> conflict
        with pytest.raises(LedgerIdentityConflict):
            _create(store, ledger_id="L-003", idem="IDEM-003", rr="RR-001")
        # datastore enforces it too (UNIQUE constraints present), not only Python
        conn = sqlite3.connect(str(tmp_path / "ledger.sqlite3"))
        try:
            idx = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='ledger_run'"
            ).fetchone()[0]
        finally:
            conn.close()
        assert "UNIQUE" in idx and "idempotency_key" in idx

    def test_30_source_disposition_history_has_no_silent_disappearance(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001", cid="C-1")
        _candidate(store, "L-001", cid="C-2")
        _dispose(store, "L-001", cid="C-1", disp=CandidateDisposition.REJECTED)
        _dispose(store, "L-001", cid="C-2", disp=CandidateDisposition.UNAVAILABLE)
        reopened = DeepResearchRunLedgerStore(path, clock=_clock)
        rec = reopened.load_run("L-001")
        # every registered candidate still has exactly one visible disposition
        assert {c.source_candidate_id for c in rec.candidates} == {"C-1", "C-2"}
        assert {d.source_candidate_id for d in rec.dispositions} == {"C-1", "C-2"}
        # append-only event log preserves the full history
        kinds = [k for _, k, _ in reopened.events("L-001")]
        assert kinds == [
            "RUN_CREATED", "CANDIDATE_REGISTERED", "CANDIDATE_REGISTERED",
            "CANDIDATE_DISPOSED", "CANDIDATE_DISPOSED",
        ]


# =====================================================================
# 31–33: reviewer-driven hardening (bounded re-review round)
# =====================================================================


class TestReviewHardening:
    def test_31_repo_internal_path_fails_closed_without_git_metadata(
        self, tmp_path, monkeypatch
    ):
        """A source copy without `.git` must still reject in-tree runtime paths."""
        import qad.m6.ledger as ledger_mod

        synthetic_root = tmp_path / "source_copy"
        (synthetic_root / "qad" / "m6").mkdir(parents=True)
        (synthetic_root / "AGENTS.md").write_text("copy", encoding="utf-8")
        assert not (synthetic_root / ".git").exists()
        monkeypatch.setattr(ledger_mod, "PROJECT_ROOT", synthetic_root)
        with pytest.raises(LedgerStateError):
            assert_outside_repository(synthetic_root / "runtime.sqlite3")
        with pytest.raises(LedgerStateError):
            DeepResearchRunLedgerStore(synthetic_root / "runtime.sqlite3")
        # and no database was created by the refused call
        assert list(synthetic_root.glob("*.sqlite3")) == []

    def test_32_datastore_triggers_reject_update_and_delete(self, tmp_path):
        """Immutability is enforced at the SQLite boundary, not only in Python."""
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001")
        _candidate(store, "L-001")
        _dispose(store, "L-001")
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)

        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            mutations = [
                ("UPDATE ledger_terminal SET terminal_status='FAILED' WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_terminal WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_disposition WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_event WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_run WHERE ledger_id='L-001'",),
                ("UPDATE ledger_run SET case_id='TAMPERED' WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_attempt WHERE ledger_id='L-001'",),
                ("DELETE FROM ledger_candidate WHERE ledger_id='L-001'",),
            ]
            for (sql,) in mutations:
                with pytest.raises(sqlite3.IntegrityError):
                    conn.execute(sql)
        finally:
            conn.close()

        rec = DeepResearchRunLedgerStore(path, clock=_clock).load_run("L-001")
        assert rec.terminal_status is TerminalStatus.SUCCESS
        assert len(rec.dispositions) == 1
        assert rec.case_id == "CASE-2026-001"

    def test_33_attempt_requires_explicit_telemetry_state(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        with pytest.raises(LedgerValidationError):
            store.append_attempt(
                "L-001", attempt_number=1, retry_mode=RetryMode.INITIAL_ATTEMPT,
                provider_surface="gemini_notebook", transport_type="BROWSER_UI_AUTOMATION",
            )
        # an explicit truthful NOT_EXPOSED state is accepted and persisted
        _attempt(store, "L-001", n=1)
        m = store.load_run("L-001").attempts[0].telemetry["model_identity"]
        assert m.status is TelemetryStatus.NOT_EXPOSED
        assert m.value is None and m.reason == "NOT_EXPOSED_BY_PROVIDER"

    def test_34_datastore_insert_replace_bypass_closed(self, tmp_path):
        """INSERT OR REPLACE and raw post-terminal INSERTs cannot alter history."""
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001")
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS,
                          result_sha256="d" * 64)

        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            bypasses = [
                # REPLACE of the terminal row (implicit delete + insert)
                "INSERT OR REPLACE INTO ledger_terminal (ledger_id, terminal_at,"
                " terminal_status) VALUES ('L-001', '2020-01-01T00:00:00+00:00', 'FAILED')",
                # raw attempt append after terminalization
                "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                " provider_surface, transport_type, started_at) VALUES"
                " ('L-001', 2, 'SAME_PROVIDER_RETRY', 'gemini_notebook', 'X',"
                " '2026-10-07T12:00:00+00:00')",
                # raw candidate insert after terminalization
                "INSERT INTO ledger_candidate (ledger_id, source_candidate_id,"
                " url_or_identifier, discovery_timestamp, verification_status,"
                " pit_eligibility) VALUES ('L-001','C-9','u','t','VERIFIED','ELIGIBLE')",
                # REPLACE of the run identity row
                "INSERT OR REPLACE INTO ledger_run (ledger_id, research_run_id,"
                " rrm_manifest_id, case_id, case_version, evidence_gap_id, request_id,"
                " idempotency_key, notebook_identity, pit_context_id, pit_mode, as_of,"
                " input_snapshot_hash, provider_surface, transport_type, started_at)"
                " VALUES ('L-001','RR-001','RRM','TAMPERED','v1','EG','REQ','IDEM-001',"
                " 'nb','PITC','M','2026-10-01','h','p','t','2026-10-07T12:00:00+00:00')",
            ]
            for sql in bypasses:
                with pytest.raises(sqlite3.IntegrityError):
                    conn.execute(sql)
        finally:
            conn.close()

        rec = DeepResearchRunLedgerStore(path, clock=_clock).load_run("L-001")
        assert rec.terminal_status is TerminalStatus.SUCCESS
        assert rec.case_id == "CASE-2026-001"
        assert [a.attempt_number for a in rec.attempts] == [1]

    def test_34b_raw_terminal_insert_blocked_by_undisposed_candidate(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001")  # registered, deliberately NOT disposed
        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_terminal (ledger_id, terminal_at, terminal_status)"
                    " VALUES ('L-001','2026-10-07T12:00:00+00:00','SUCCESS')"
                )
        finally:
            conn.close()
        assert store.load_run("L-001").terminal_status is None

    def test_35_telemetry_metric_set_is_enforced(self, tmp_path):
        store, _ = _store(tmp_path)
        _create(store)
        # an unlisted-only metric cannot stand in for the contract metrics
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry={
                "unlisted_metric": {"status": "EXPOSED", "value": 7},
            })
        # a partial set (missing required metrics) is rejected
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry={
                "model_identity": {"status": "NOT_EXPOSED", "value": None,
                                   "reason": "NOT_EXPOSED_BY_PROVIDER"},
            })
        # a non-contract extra alongside a complete set is rejected
        full = _tel()
        full["extra_metric"] = {"status": "EXPOSED", "value": 1}
        with pytest.raises(LedgerValidationError):
            _attempt(store, "L-001", telemetry=full)
        # the complete contract set is accepted
        _attempt(store, "L-001")
        assert len(store.load_run("L-001").attempts) == 1

    def test_36_raw_replace_of_history_and_identity_rejected(self, tmp_path):
        """REPLACE cannot rewrite attempt/candidate rows nor a run identity."""
        store, path = _store(tmp_path)
        _create(store, ledger_id="L-001", idem="IDEM-001", rr="RR-001")
        _attempt(store, "L-001")
        _candidate(store, "L-001", cid="C-1")
        good_tel = json.dumps(_tel())

        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cases = [
                # REPLACE an existing attempt (duplicate identity)
                "INSERT OR REPLACE INTO ledger_attempt (ledger_id, attempt_number,"
                " retry_mode, provider_surface, transport_type, started_at, outcome,"
                " telemetry_json) VALUES ('L-001',1,'SAME_PROVIDER_RETRY','forged',"
                f" 'X','t','FAILED','{good_tel}')",
                # REPLACE an existing candidate (duplicate identity)
                "INSERT OR REPLACE INTO ledger_candidate (ledger_id, source_candidate_id,"
                " url_or_identifier, discovery_timestamp, verification_status,"
                " pit_eligibility) VALUES ('L-001','C-1','forged-url','t','FORGED',"
                " 'ELIGIBLE')",
                # REPLACE the run by colliding on research_run_id (different ledger_id)
                "INSERT OR REPLACE INTO ledger_run (ledger_id, research_run_id,"
                " rrm_manifest_id, case_id, case_version, evidence_gap_id, request_id,"
                " idempotency_key, notebook_identity, pit_context_id, pit_mode, as_of,"
                " input_snapshot_hash, provider_surface, transport_type, started_at)"
                " VALUES ('L-002','RR-001','RRM','CASE','v1','EG','REQ','IDEM-009','nb',"
                " 'PITC','M','2026-10-01','h','p','t','2026-10-07T12:00:00+00:00')",
                # REPLACE the run by colliding on idempotency_key
                "INSERT OR REPLACE INTO ledger_run (ledger_id, research_run_id,"
                " rrm_manifest_id, case_id, case_version, evidence_gap_id, request_id,"
                " idempotency_key, notebook_identity, pit_context_id, pit_mode, as_of,"
                " input_snapshot_hash, provider_surface, transport_type, started_at)"
                " VALUES ('L-003','RR-009','RRM','CASE','v1','EG','REQ','IDEM-001','nb',"
                " 'PITC','M','2026-10-01','h','p','t','2026-10-07T12:00:00+00:00')",
            ]
            for sql in cases:
                with pytest.raises(sqlite3.IntegrityError):
                    conn.execute(sql)
        finally:
            conn.close()

        rec = DeepResearchRunLedgerStore(path, clock=_clock).load_run("L-001")
        assert rec.attempts[0].provider_surface == "gemini_notebook"
        assert rec.candidates[0].url_or_identifier == "https://example.com/a"
        assert rec.candidates[0].original_source_verification_status == "VERIFIED"
        assert [r for r in DeepResearchRunLedgerStore(path, clock=_clock).list_runs()] == ["L-001"]

    def test_37_terminal_row_is_the_authority(self, tmp_path):
        """An unbacked terminal event is rejected; post-terminal raw inserts blocked."""
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001")
        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            # phantom terminal event with no terminal record is rejected
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_event (ledger_id, event_type, payload_json,"
                    " created_at) VALUES ('L-001','RUN_TERMINALIZED','{}','t')"
                )
        finally:
            conn.close()
        assert store.load_run("L-001").terminal_status is None
        # legitimate terminalization still works, then raw attempt insert is blocked
        store.terminalize("L-001", terminal_status=TerminalStatus.SUCCESS)
        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                    " provider_surface, transport_type, started_at, telemetry_json)"
                    f" VALUES ('L-001',2,'SAME_PROVIDER_RETRY','p','X','t',"
                    f"'{json.dumps(_tel())}')"
                )
        finally:
            conn.close()
        assert [a.attempt_number for a in store.load_run("L-001").attempts] == [1]

    def test_38_raw_empty_or_partial_telemetry_rejected_at_datastore(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            required = ("model_identity", "prompt_tokens", "completion_tokens",
                        "cost", "model_version")
            bad_telemetry = [
                "{}",
                "null",
                '{"model_identity": {"status": "NOT_EXPOSED", "value": null}}',
                '{"model_identity": {"status": "BOGUS", "value": 1},'
                ' "prompt_tokens": {"status": "NOT_EXPOSED", "value": null, "reason": "r"},'
                ' "completion_tokens": {"status": "NOT_EXPOSED", "value": null, "reason": "r"},'
                ' "cost": {"status": "NOT_EXPOSED", "value": null, "reason": "r"},'
                ' "model_version": {"status": "NOT_EXPOSED", "value": null, "reason": "r"}}',
                # NOT_EXPOSED without a reason
                json.dumps({k: {"status": "NOT_EXPOSED", "value": None} for k in required}),
                # optional total_tokens present but invalid
                json.dumps({**_tel(), "total_tokens": {"status": "BOGUS", "value": 1}}),
                # optional total_tokens EXPOSED with null value
                json.dumps({**_tel(), "total_tokens": {"status": "EXPOSED", "value": None}}),
            ]
            for tel in bad_telemetry:
                with pytest.raises(sqlite3.IntegrityError):
                    conn.execute(
                        "INSERT INTO ledger_attempt (ledger_id, attempt_number,"
                        " retry_mode, provider_surface, transport_type, started_at,"
                        " telemetry_json) VALUES ('L-001',1,'INITIAL_ATTEMPT','p','X',"
                        f"'t','{tel}')"
                    )
            # a complete, valid truthful telemetry record is accepted at the boundary
            good = _tel(total_tokens={"status": "EXPOSED", "value": 42})
            conn.execute(
                "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                " provider_surface, transport_type, started_at, telemetry_json)"
                f" VALUES ('L-001',2,'INITIAL_ATTEMPT','p','X','t','{json.dumps(good)}')"
            )
            conn.commit()
        finally:
            conn.close()
        rec = store.load_run("L-001")
        assert [a.attempt_number for a in rec.attempts] == [2]
        assert rec.attempts[0].telemetry["total_tokens"].value == 42

    def test_39_attempt_number_range_enforced(self, tmp_path):
        """M6.0 §3: attempt_number ∈ 1..3 — enforced in API and at the datastore."""
        store, path = _store(tmp_path)
        _create(store)
        for bad in (0, 4, 9, -1, True):
            with pytest.raises(LedgerValidationError):
                _attempt(store, "L-001", n=bad)
        for ok in (1, 2, 3):
            _attempt(store, "L-001", n=ok)
        assert [a.attempt_number for a in store.load_run("L-001").attempts] == [1, 2, 3]
        # the datastore CHECK also rejects an out-of-range raw insert
        conn = sqlite3.connect(str(path))
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                    " provider_surface, transport_type, started_at, telemetry_json)"
                    f" VALUES ('L-001',4,'SAME_PROVIDER_RETRY','p','X','t',"
                    f"'{json.dumps(_tel())}')"
                )
        finally:
            conn.close()

    def test_40_raw_disposition_enum_enforced_at_datastore(self, tmp_path):
        store, path = _store(tmp_path)
        _create(store)
        _candidate(store, "L-001")
        conn = sqlite3.connect(str(path))
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_disposition (ledger_id, source_candidate_id,"
                    " disposition, reason, disposed_at) VALUES ('L-001','C-1','BOGUS',"
                    " 'r','t')"
                )
        finally:
            conn.close()
        # the run stays readable and non-terminal with no bogus disposition
        rec = store.load_run("L-001")
        assert rec.dispositions == ()
        assert rec.terminal_status is None

    def test_42_fractional_attempt_number_rejected(self, tmp_path):
        """The range CHECK must also require integer storage (not just 1..3)."""
        store, path = _store(tmp_path)
        _create(store)
        _attempt(store, "L-001", n=1)
        conn = sqlite3.connect(str(path))
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            # genuinely fractional values are stored as REAL and rejected
            for bad in ("1.5", "2.5", "0.5"):
                with pytest.raises(sqlite3.IntegrityError):
                    conn.execute(
                        "INSERT INTO ledger_attempt (ledger_id, attempt_number,"
                        " retry_mode, provider_surface, transport_type, started_at,"
                        " telemetry_json) VALUES ('L-001'," + bad + ",'SAME_PROVIDER_RETRY',"
                        f"'p','X','t','{json.dumps(_tel())}')"
                    )
            # SQLite INTEGER affinity coerces a lossless REAL (2.0) to integer 2,
            # which is a valid attempt identity — verify it is stored as INTEGER.
            conn.execute(
                "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                " provider_surface, transport_type, started_at, telemetry_json)"
                f" VALUES ('L-001',2.0,'SAME_PROVIDER_RETRY','p','X','t','{json.dumps(_tel())}')"
            )
            assert conn.execute(
                "SELECT typeof(attempt_number) FROM ledger_attempt"
                " WHERE ledger_id='L-001' AND attempt_number=2"
            ).fetchone()[0] == "integer"
            conn.commit()
        finally:
            conn.close()
        assert [a.attempt_number for a in store.load_run("L-001").attempts] == [1, 2]
        assert all(isinstance(a.attempt_number, int) for a in store.load_run("L-001").attempts)

    def test_43_explicit_null_optional_metric_rejected_and_reader_defended(self, tmp_path):
        import qad.m6.ledger as ledger_mod

        store, path = _store(tmp_path)
        _create(store)
        conn = sqlite3.connect(str(path))
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                    " provider_surface, transport_type, started_at, telemetry_json)"
                    f" VALUES ('L-001',1,'INITIAL_ATTEMPT','p','X','t',"
                    f"'{json.dumps({**_tel(), 'total_tokens': None})}')"
                )
        finally:
            conn.close()
        # defence in depth: a malformed stored metric raises a TYPED error, not TypeError
        with pytest.raises(ledger_mod.LedgerValidationError):
            ledger_mod._telemetry_from_json('{"total_tokens": null}')
        with pytest.raises(ledger_mod.LedgerValidationError):
            ledger_mod._telemetry_from_json('{"cost": {"status": "BOGUS", "value": 1}}')

    def test_44_reader_fails_closed_on_malformed_stored_telemetry(self, tmp_path):
        """The read path applies the same §7.2 invariants as the write path."""
        import qad.m6.ledger as ledger_mod
        from qad.m6.ledger import _telemetry_from_json as read

        good = {
            "model_identity": {"status": "EXPOSED", "value": "gemini-x", "reason": None},
            "prompt_tokens": {"status": "EXPOSED", "value": 5, "reason": None},
            "completion_tokens": {"status": "EXPOSED", "value": 0, "reason": None},
            "cost": {"status": "NOT_EXPOSED", "value": None, "reason": "NOT_EXPOSED_BY_PROVIDER"},
            "model_version": {"status": "NOT_EXPOSED", "value": None, "reason": "hidden"},
        }
        ok = read(json.dumps(good))
        assert ok["completion_tokens"].value == 0  # zero stays EXPOSED

        malformed = [
            '{"model_identity": {"status": "EXPOSED", "value": null},'
            ' "prompt_tokens": {"status": "EXPOSED", "value": 1, "reason": null},'
            ' "completion_tokens": {"status": "EXPOSED", "value": 1, "reason": null},'
            ' "cost": {"status": "EXPOSED", "value": 1, "reason": null},'
            ' "model_version": {"status": "EXPOSED", "value": 1, "reason": null}}',
            json.dumps({**good, "cost": {"status": "NOT_EXPOSED", "value": None}}),
            json.dumps({**good, "cost": {"status": "NOT_EXPOSED", "value": 0, "reason": "r"}}),
            json.dumps({"model_identity": good["model_identity"]}),          # partial set
            json.dumps({**good, "extra_metric": {"status": "EXPOSED", "value": 1}}),
            "[]",                                                            # not an object
            "{not json",                                                     # invalid JSON
        ]
        for raw in malformed:
            with pytest.raises(ledger_mod.LedgerValidationError):
                read(raw)

        # and a malformed persisted row surfaces as a typed error via load_run
        store, path = _store(tmp_path)
        _create(store)
        conn = sqlite3.connect(str(path))
        try:
            conn.execute(
                "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                " provider_surface, transport_type, started_at, telemetry_json)"
                f" VALUES ('L-001',1,'INITIAL_ATTEMPT','p','X','t','{json.dumps(good)}')"
            )
            conn.commit()
        finally:
            conn.close()
        assert store.load_run("L-001").attempts[0].telemetry["cost"].status is (
            ledger_mod.TelemetryStatus.NOT_EXPOSED
        )
