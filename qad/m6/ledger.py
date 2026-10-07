"""M6.3 — Deep Research Run Ledger (``DeepResearchRunLedgerStore``).

FD #149 / M6.0 §7 durable, **non-canonical** operational/provenance authority
for M6 Deep Research runs.

Hard boundary (M6.0 §7.6)
-------------------------
This ledger is a NON-CANONICAL additive operational store. It is:

* **durable** — a real on-disk SQLite database, not an in-memory dict;
* **append-only during execution** and **immutable after terminalization**
  (except the explicit administrative tombstone path, which is not implemented
  in this cluster — see :meth:`DeepResearchRunLedgerStore` docstring);
* independent of the **Research Room** (``NonCanonicalResearchArtifactStore``)
  and of the provider **Notebook** lifetime;
* **NOT** a 69th canonical M4A schema and **NOT** registered in the canonical
  schema registry;
* **NOT** stored in git as runtime state (the caller supplies a runtime path
  outside the repository; :func:`assert_outside_repository` fails closed).

Backend choice: Python stdlib ``sqlite3`` ONLY (bounded M6 operational-ledger
implementation detail). No third-party DB dependency is introduced, and this
does **not** select SQLite as the persistence technology for the five canonical
M5.2 anchors (M5.2 §9.4 defers production adapter selection).

This cluster performs **no** provider transport, **no** Gemini/Notebook call,
**no** network I/O. It implements the durable *representation* of runs,
attempts, telemetry, source-candidate dispositions and terminalization.

See: design/qad-pivot/m6/QAD-M6.0-DESIGN-GATE-RECONCILIATION.md §7, §8;
FD #149, FD #150, FD #151.
"""

from __future__ import annotations

import datetime as _dt
import json
import sqlite3
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

# ---------------------------------------------------------------------------
# Vocabulary (bounded — reuses the M6.0 §8 failure-state vocabulary)
# ---------------------------------------------------------------------------


class TerminalStatus(str, Enum):
    """Bounded terminal statuses (M6.0 §8)."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RESEARCH_UNAVAILABLE = "RESEARCH_UNAVAILABLE"
    TRANSPORT_FAILURE = "TRANSPORT_FAILURE"
    PIT_BLOCK = "PIT_BLOCK"
    INCOMPLETE = "INCOMPLETE"


class CandidateDisposition(str, Enum):
    """Exactly one final disposition per discovered source candidate (M6.0 §7.5)."""

    IMPORTED = "IMPORTED"
    REJECTED = "REJECTED"
    UNAVAILABLE = "UNAVAILABLE"
    DEFERRED = "DEFERRED"


class TelemetryStatus(str, Enum):
    """Truthful telemetry exposure state (M6.0 §7.2)."""

    EXPOSED = "EXPOSED"
    NOT_EXPOSED = "NOT_EXPOSED"


class RetryMode(str, Enum):
    """Retry identity mode (M6.0 §1 / §3)."""

    INITIAL_ATTEMPT = "INITIAL_ATTEMPT"
    SAME_PROVIDER_RETRY = "SAME_PROVIDER_RETRY"
    PROVIDER_FALLBACK = "PROVIDER_FALLBACK"


#: Canonical schema-registry size BEFORE M6.3 (M4A frozen, 68 schemas). The
#: ledger must never add a 69th canonical schema.
CANONICAL_SCHEMA_COUNT = 68

#: Environment variable naming the runtime data root. Ledger runtime state is
#: written OUTSIDE the git repository.
RUNTIME_DATA_DIR_ENV = "QAD_RUNTIME_DATA_DIR"

#: This project's source-tree root (``qad/m6/ledger.py`` -> repo root). Used to
#: reject repository-internal runtime paths even when the tree carries no
#: ``.git`` metadata (e.g. a source copy / archive export). Module-level so tests
#: can substitute a synthetic root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def assert_outside_repository(path: str | Path) -> Path:
    """Fail closed if ``path`` resolves inside the project source tree or inside
    any git working tree.

    Runtime ledger state MUST NOT be written into the git repository
    (M6.0 §7.3, task §15). Two independent guards:

    1. no ancestor may carry a ``.git`` entry (file or directory — robust to
       worktrees, where ``.git`` is a file);
    2. the path must not live under this project's source-tree root
       (:data:`PROJECT_ROOT`) — this holds even when ``.git`` is absent, e.g. a
       disposable source copy or an archive export.
    """
    resolved = Path(path).resolve()
    for parent in [resolved, *resolved.parents]:
        if (parent / ".git").exists():
            raise LedgerStateError(
                f"ledger runtime path {resolved} is inside a git repository "
                f"({parent}); runtime ledger state must live outside the repo"
            )
    root = Path(PROJECT_ROOT).resolve()
    if resolved == root or root in resolved.parents:
        raise LedgerStateError(
            f"ledger runtime path {resolved} is inside the project source tree "
            f"({root}); runtime ledger state must live outside the repo"
        )
    return resolved


def default_runtime_ledger_path() -> Path:
    """The documented default runtime ledger path (outside any repository).

    Uses ``QAD_RUNTIME_DATA_DIR`` when set, else ``~/.qad/runtime``. Callers
    (and tests) are expected to pass an explicit path; this helper only names
    the convention. No repository-internal default is ever produced.
    """
    import os

    root = os.environ.get(RUNTIME_DATA_DIR_ENV)
    base = Path(root) if root else Path.home() / ".qad" / "runtime"
    return base / "deep_research_run_ledger.sqlite3"


# ---------------------------------------------------------------------------
# Typed errors
# ---------------------------------------------------------------------------


class LedgerError(Exception):
    """Base class for Deep Research Run Ledger errors."""


class LedgerIdentityConflict(LedgerError):
    """Duplicate durable identity (ledger_id / research_run_id / idempotency_key)."""


class LedgerTerminalError(LedgerError):
    """A mutation was rejected because the run is already terminalized, or a
    second terminalization was attempted."""


class LedgerValidationError(LedgerError):
    """A record failed a deterministic ledger contract rule."""


class LedgerNotFound(LedgerError):
    """The requested ledger run does not exist."""


class LedgerStateError(LedgerError):
    """The ledger store is misconfigured (e.g. repository-internal path)."""


# ---------------------------------------------------------------------------
# Read model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TelemetryMetric:
    """One truthful telemetry metric (M6.0 §7.2).

    ``status`` is always present. ``value`` is the exact exposed value or
    ``None``. ``reason`` is mandatory when ``status == NOT_EXPOSED``.
    """

    status: TelemetryStatus
    value: Any = None
    reason: str | None = None


@dataclass(frozen=True)
class AttemptRecord:
    attempt_number: int
    retry_mode: RetryMode
    provider_surface: str
    transport_type: str
    started_at: str
    completed_at: str | None
    outcome: str | None
    error: str | None
    telemetry: Mapping[str, TelemetryMetric] = field(default_factory=dict)


@dataclass(frozen=True)
class CandidateRecord:
    source_candidate_id: str
    url_or_identifier: str
    fingerprint: str | None
    discovery_timestamp: str
    original_source_verification_status: str
    pit_eligibility: str


@dataclass(frozen=True)
class DispositionRecord:
    source_candidate_id: str
    disposition: CandidateDisposition
    reason: str
    src01_id: str | None
    evidence_ids: tuple[str, ...]
    ear_ids: tuple[str, ...]
    disposed_at: str


@dataclass(frozen=True)
class RunRecord:
    """Deterministic materialized read model of one logical run."""

    ledger_id: str
    research_run_id: str
    rrm_manifest_id: str
    case_id: str
    case_version: str
    evidence_gap_id: str
    request_id: str
    idempotency_key: str
    notebook_identity: str
    pit_context_id: str
    pit_mode: str
    as_of: str
    input_snapshot_hash: str
    provider_surface: str
    transport_type: str
    started_at: str
    attempts: tuple[AttemptRecord, ...] = ()
    candidates: tuple[CandidateRecord, ...] = ()
    dispositions: tuple[DispositionRecord, ...] = ()
    terminal_at: str | None = None
    terminal_status: TerminalStatus | None = None
    result_artifact_ref: str | None = None
    result_sha256: str | None = None
    failure_detail: str | None = None

    @property
    def is_terminal(self) -> bool:
        return self.terminal_status is not None


# ---------------------------------------------------------------------------
# Telemetry validation
# ---------------------------------------------------------------------------


def _validate_telemetry(telemetry: Mapping[str, Any] | None) -> dict[str, TelemetryMetric]:
    """Validate + normalize a telemetry mapping (fail closed).

    Rules (M6.0 §7.2):
      * EXPOSED      -> exact value required (may be 0 — zero is a real value),
                        ``reason`` optional.
      * NOT_EXPOSED  -> ``value`` MUST be ``None`` and a non-empty ``reason``
                        REQUIRED.
      * never zero-as-unknown; never a guessed value.
    """
    out: dict[str, TelemetryMetric] = {}
    if not telemetry:
        return out
    for metric, spec in telemetry.items():
        if not isinstance(spec, Mapping):
            raise LedgerValidationError(f"telemetry[{metric}] must be a mapping")
        raw_status = spec.get("status")
        try:
            status = TelemetryStatus(raw_status)
        except ValueError:
            raise LedgerValidationError(
                f"telemetry[{metric}].status must be EXPOSED|NOT_EXPOSED, got {raw_status!r}"
            ) from None
        value = spec.get("value")
        reason = spec.get("reason")
        if status is TelemetryStatus.EXPOSED:
            if value is None:
                raise LedgerValidationError(
                    f"telemetry[{metric}] EXPOSED requires an exact value"
                )
            out[metric] = TelemetryMetric(status=status, value=value, reason=reason)
        else:  # NOT_EXPOSED
            if value is not None:
                raise LedgerValidationError(
                    f"telemetry[{metric}] NOT_EXPOSED must carry value=null"
                )
            if not reason or not str(reason).strip():
                raise LedgerValidationError(
                    f"telemetry[{metric}] NOT_EXPOSED requires a non-empty reason"
                )
            out[metric] = TelemetryMetric(status=status, value=None, reason=str(reason))
    return out


def _telemetry_to_json(telemetry: Mapping[str, TelemetryMetric]) -> str:
    return json.dumps(
        {
            k: {"status": v.status.value, "value": v.value, "reason": v.reason}
            for k, v in sorted(telemetry.items())
        },
        sort_keys=True,
    )


def _telemetry_from_json(raw: str | None) -> dict[str, TelemetryMetric]:
    if not raw:
        return {}
    data = json.loads(raw)
    return {
        k: TelemetryMetric(
            status=TelemetryStatus(v["status"]), value=v["value"], reason=v["reason"]
        )
        for k, v in data.items()
    }


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


_SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger_run (
    ledger_id          TEXT PRIMARY KEY,
    research_run_id    TEXT NOT NULL UNIQUE,
    rrm_manifest_id    TEXT NOT NULL,
    case_id            TEXT NOT NULL,
    case_version       TEXT NOT NULL,
    evidence_gap_id    TEXT NOT NULL,
    request_id         TEXT NOT NULL,
    idempotency_key    TEXT NOT NULL UNIQUE,
    notebook_identity  TEXT NOT NULL,
    pit_context_id     TEXT NOT NULL,
    pit_mode           TEXT NOT NULL,
    as_of              TEXT NOT NULL,
    input_snapshot_hash TEXT NOT NULL,
    provider_surface   TEXT NOT NULL,
    transport_type     TEXT NOT NULL,
    started_at         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ledger_attempt (
    ledger_id       TEXT NOT NULL REFERENCES ledger_run(ledger_id),
    attempt_number  INTEGER NOT NULL,
    retry_mode      TEXT NOT NULL,
    provider_surface TEXT NOT NULL,
    transport_type  TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    completed_at    TEXT,
    outcome         TEXT,
    error           TEXT,
    telemetry_json  TEXT,
    PRIMARY KEY (ledger_id, attempt_number)
);

CREATE TABLE IF NOT EXISTS ledger_candidate (
    ledger_id           TEXT NOT NULL REFERENCES ledger_run(ledger_id),
    source_candidate_id TEXT NOT NULL,
    url_or_identifier   TEXT NOT NULL,
    fingerprint         TEXT,
    discovery_timestamp TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    pit_eligibility     TEXT NOT NULL,
    PRIMARY KEY (ledger_id, source_candidate_id)
);

CREATE TABLE IF NOT EXISTS ledger_disposition (
    ledger_id           TEXT NOT NULL,
    source_candidate_id TEXT NOT NULL,
    disposition         TEXT NOT NULL,
    reason              TEXT NOT NULL,
    src01_id            TEXT,
    evidence_ids_json   TEXT,
    ear_ids_json        TEXT,
    disposed_at         TEXT NOT NULL,
    PRIMARY KEY (ledger_id, source_candidate_id),
    FOREIGN KEY (ledger_id, source_candidate_id)
        REFERENCES ledger_candidate(ledger_id, source_candidate_id)
);

CREATE TABLE IF NOT EXISTS ledger_terminal (
    ledger_id           TEXT PRIMARY KEY REFERENCES ledger_run(ledger_id),
    terminal_at         TEXT NOT NULL,
    terminal_status     TEXT NOT NULL,
    result_artifact_ref TEXT,
    result_sha256       TEXT,
    failure_detail      TEXT
);

CREATE TABLE IF NOT EXISTS ledger_event (
    seq         INTEGER PRIMARY KEY AUTOINCREMENT,
    ledger_id   TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

-- Datastore-level immutability (M6.0 §7.3): the durable tables are append-only.
-- These triggers reject UPDATE/DELETE at the SQLite boundary, so terminal
-- truth, disposition history and the event log cannot silently disappear even
-- through a direct/adversarial connection — not merely through store methods.
CREATE TRIGGER IF NOT EXISTS ledger_run_immutable_update
    BEFORE UPDATE ON ledger_run
    BEGIN SELECT RAISE(ABORT, 'ledger_run is immutable'); END;
CREATE TRIGGER IF NOT EXISTS ledger_run_immutable_delete
    BEFORE DELETE ON ledger_run
    BEGIN SELECT RAISE(ABORT, 'ledger_run is immutable (no silent GC)'); END;
CREATE TRIGGER IF NOT EXISTS ledger_attempt_immutable_update
    BEFORE UPDATE ON ledger_attempt
    BEGIN SELECT RAISE(ABORT, 'ledger_attempt is append-only'); END;
CREATE TRIGGER IF NOT EXISTS ledger_attempt_immutable_delete
    BEFORE DELETE ON ledger_attempt
    BEGIN SELECT RAISE(ABORT, 'ledger_attempt is append-only (no silent GC)'); END;
CREATE TRIGGER IF NOT EXISTS ledger_candidate_immutable_update
    BEFORE UPDATE ON ledger_candidate
    BEGIN SELECT RAISE(ABORT, 'ledger_candidate is append-only'); END;
CREATE TRIGGER IF NOT EXISTS ledger_candidate_immutable_delete
    BEFORE DELETE ON ledger_candidate
    BEGIN SELECT RAISE(ABORT, 'ledger_candidate is append-only (no silent GC)'); END;
CREATE TRIGGER IF NOT EXISTS ledger_disposition_immutable_update
    BEFORE UPDATE ON ledger_disposition
    BEGIN SELECT RAISE(ABORT, 'ledger_disposition is immutable'); END;
CREATE TRIGGER IF NOT EXISTS ledger_disposition_immutable_delete
    BEFORE DELETE ON ledger_disposition
    BEGIN SELECT RAISE(ABORT, 'ledger_disposition is immutable (no silent GC)'); END;
CREATE TRIGGER IF NOT EXISTS ledger_terminal_immutable_update
    BEFORE UPDATE ON ledger_terminal
    BEGIN SELECT RAISE(ABORT, 'terminal state is immutable'); END;
CREATE TRIGGER IF NOT EXISTS ledger_terminal_immutable_delete
    BEFORE DELETE ON ledger_terminal
    BEGIN SELECT RAISE(ABORT, 'terminal state is immutable (no silent GC)'); END;
CREATE TRIGGER IF NOT EXISTS ledger_event_immutable_update
    BEFORE UPDATE ON ledger_event
    BEGIN SELECT RAISE(ABORT, 'ledger_event is append-only'); END;
CREATE TRIGGER IF NOT EXISTS ledger_event_immutable_delete
    BEFORE DELETE ON ledger_event
    BEGIN SELECT RAISE(ABORT, 'ledger_event is append-only (no silent GC)'); END;
"""


def _utc_now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _iso(value: _dt.datetime | str) -> str:
    if isinstance(value, _dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=_dt.timezone.utc)
        return value.isoformat()
    return str(value)


class DeepResearchRunLedgerStore:
    """Durable, append-only, non-canonical Deep Research Run Ledger.

    Backend: a single on-disk SQLite database (stdlib ``sqlite3``). All writes
    are transactional; a run record is durably committed **before** any future
    provider invocation (create-before-provider invariant, §8).

    Immutability rules
    ------------------
    * ``ledger_run`` identity rows are written once and never updated.
    * After terminalization: attempt append, disposition append, telemetry
      mutation, and a second terminalization are all rejected.
    * No silent overwrite of history: appends either succeed durably or raise.

    No administrative tombstone/correction path exists in this cluster; adding
    one requires an explicit, auditable contract (M6.0 §7), so it is
    deliberately absent rather than silently destructive.
    """

    def __init__(
        self,
        db_path: str | Path,
        *,
        clock: Callable[[], _dt.datetime] | None = None,
    ) -> None:
        self._db_path = assert_outside_repository(db_path)
        self._clock = clock or _utc_now
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    # -- connection / transaction helpers --------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path), isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _now(self) -> str:
        return _iso(self._clock())

    def _write_event(self, conn: sqlite3.Connection, ledger_id: str,
                     event_type: str, payload: dict[str, Any]) -> None:
        """Append one durable event row (monkeypatchable failure seam)."""
        conn.execute(
            "INSERT INTO ledger_event (ledger_id, event_type, payload_json, created_at)"
            " VALUES (?, ?, ?, ?)",
            (ledger_id, event_type, json.dumps(payload, sort_keys=True), self._now()),
        )

    @staticmethod
    def _terminal_status(conn: sqlite3.Connection, ledger_id: str) -> str | None:
        row = conn.execute(
            "SELECT terminal_status FROM ledger_terminal WHERE ledger_id = ?",
            (ledger_id,),
        ).fetchone()
        return None if row is None else row["terminal_status"]

    def _require_run(self, conn: sqlite3.Connection, ledger_id: str) -> None:
        row = conn.execute(
            "SELECT 1 FROM ledger_run WHERE ledger_id = ?", (ledger_id,)
        ).fetchone()
        if row is None:
            raise LedgerNotFound(f"ledger run {ledger_id!r} not found")

    def _require_mutable(self, conn: sqlite3.Connection, ledger_id: str) -> None:
        status = self._terminal_status(conn, ledger_id)
        if status is not None:
            raise LedgerTerminalError(
                f"ledger run {ledger_id!r} is terminal ({status}); mutation rejected"
            )

    # -- create-before-provider ------------------------------------------

    def create_run(
        self,
        *,
        ledger_id: str,
        research_run_id: str,
        rrm_manifest_id: str,
        case_id: str,
        case_version: str,
        evidence_gap_id: str,
        request_id: str,
        idempotency_key: str,
        notebook_identity: str,
        pit_context_id: str,
        pit_mode: str,
        as_of: str,
        input_snapshot_hash: str,
        provider_surface: str,
        transport_type: str,
        started_at: str | None = None,
    ) -> str:
        """Durably create a logical run BEFORE any provider execution.

        Returns the ``ledger_id``. Raises :class:`LedgerIdentityConflict` when
        ``ledger_id``, ``research_run_id`` or ``idempotency_key`` already exist
        (no silent duplicate logical run). The whole operation is atomic.
        """
        for name, value in {
            "ledger_id": ledger_id,
            "research_run_id": research_run_id,
            "rrm_manifest_id": rrm_manifest_id,
            "case_id": case_id,
            "case_version": case_version,
            "evidence_gap_id": evidence_gap_id,
            "request_id": request_id,
            "idempotency_key": idempotency_key,
            "notebook_identity": notebook_identity,
            "pit_context_id": pit_context_id,
            "pit_mode": pit_mode,
            "as_of": as_of,
            "input_snapshot_hash": input_snapshot_hash,
            "provider_surface": provider_surface,
            "transport_type": transport_type,
        }.items():
            if not isinstance(value, str) or not value.strip():
                raise LedgerValidationError(f"create_run requires non-empty {name}")

        started = _iso(started_at) if started_at is not None else self._now()

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            if self._terminal_status(conn, ledger_id) is not None:
                raise LedgerTerminalError(f"ledger_id {ledger_id!r} already exists")
            try:
                conn.execute(
                    "INSERT INTO ledger_run (ledger_id, research_run_id, rrm_manifest_id,"
                    " case_id, case_version, evidence_gap_id, request_id, idempotency_key,"
                    " notebook_identity, pit_context_id, pit_mode, as_of,"
                    " input_snapshot_hash, provider_surface, transport_type, started_at)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        ledger_id, research_run_id, rrm_manifest_id, case_id,
                        case_version, evidence_gap_id, request_id, idempotency_key,
                        notebook_identity, pit_context_id, pit_mode, as_of,
                        input_snapshot_hash, provider_surface, transport_type, started,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerIdentityConflict(
                    f"duplicate ledger identity (ledger_id/research_run_id/"
                    f"idempotency_key): {exc}"
                ) from None
            self._write_event(conn, ledger_id, "RUN_CREATED", {
                "research_run_id": research_run_id,
                "idempotency_key": idempotency_key,
                "input_snapshot_hash": input_snapshot_hash,
            })
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()
        return ledger_id

    # -- attempts ---------------------------------------------------------

    def append_attempt(
        self,
        ledger_id: str,
        *,
        attempt_number: int,
        retry_mode: str | RetryMode,
        provider_surface: str,
        transport_type: str,
        started_at: str | None = None,
        completed_at: str | None = None,
        outcome: str | TerminalStatus | None = None,
        error: str | None = None,
        telemetry: Mapping[str, Any] | None = None,
    ) -> None:
        """Durably append one attempt. Append-only; prior attempts never rewritten."""
        if not isinstance(attempt_number, int) or attempt_number < 1:
            raise LedgerValidationError("attempt_number must be an integer >= 1")
        try:
            mode = RetryMode(retry_mode)
        except ValueError:
            raise LedgerValidationError(f"unknown retry_mode {retry_mode!r}") from None
        if outcome is not None:
            try:
                outcome = TerminalStatus(outcome).value
            except ValueError:
                raise LedgerValidationError(f"unknown attempt outcome {outcome!r}") from None

        metrics = _validate_telemetry(telemetry)
        if not metrics:
            # M6.0 §7.2: an attempt must carry an explicit truthful state for
            # each applicable metric. Silently storing "no metrics" makes
            # un-recorded indistinguishable from not-collected.
            raise LedgerValidationError(
                "append_attempt requires explicit telemetry states; use "
                "status=NOT_EXPOSED with value=null and a non-empty reason when "
                "the provider does not expose a metric"
            )
        started = _iso(started_at) if started_at is not None else self._now()

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            self._require_run(conn, ledger_id)
            self._require_mutable(conn, ledger_id)
            try:
                conn.execute(
                    "INSERT INTO ledger_attempt (ledger_id, attempt_number, retry_mode,"
                    " provider_surface, transport_type, started_at, completed_at, outcome,"
                    " error, telemetry_json) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        ledger_id, attempt_number, mode.value, provider_surface,
                        transport_type, started,
                        _iso(completed_at) if completed_at is not None else None,
                        outcome, error, _telemetry_to_json(metrics),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerIdentityConflict(
                    f"duplicate attempt identity ({ledger_id!r}, {attempt_number}): {exc}"
                ) from None
            self._write_event(conn, ledger_id, "ATTEMPT_APPENDED", {
                "attempt_number": attempt_number,
                "retry_mode": mode.value,
                "outcome": outcome,
            })
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    # -- source candidates + dispositions ---------------------------------

    def register_candidate(
        self,
        ledger_id: str,
        *,
        source_candidate_id: str,
        url_or_identifier: str,
        discovery_timestamp: str,
        original_source_verification_status: str,
        pit_eligibility: str,
        fingerprint: str | None = None,
    ) -> None:
        """Durably register a discovered source candidate (needs a disposition)."""
        for name, value in {
            "source_candidate_id": source_candidate_id,
            "url_or_identifier": url_or_identifier,
            "discovery_timestamp": discovery_timestamp,
            "original_source_verification_status": original_source_verification_status,
            "pit_eligibility": pit_eligibility,
        }.items():
            if not isinstance(value, str) or not value.strip():
                raise LedgerValidationError(f"register_candidate requires non-empty {name}")

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            self._require_run(conn, ledger_id)
            self._require_mutable(conn, ledger_id)
            try:
                conn.execute(
                    "INSERT INTO ledger_candidate (ledger_id, source_candidate_id,"
                    " url_or_identifier, fingerprint, discovery_timestamp,"
                    " verification_status, pit_eligibility) VALUES (?,?,?,?,?,?,?)",
                    (
                        ledger_id, source_candidate_id, url_or_identifier, fingerprint,
                        discovery_timestamp, original_source_verification_status,
                        pit_eligibility,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerIdentityConflict(
                    f"duplicate source candidate ({ledger_id!r}, {source_candidate_id!r}): {exc}"
                ) from None
            self._write_event(conn, ledger_id, "CANDIDATE_REGISTERED", {
                "source_candidate_id": source_candidate_id,
            })
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def dispose_candidate(
        self,
        ledger_id: str,
        source_candidate_id: str,
        *,
        disposition: str | CandidateDisposition,
        reason: str,
        src01_id: str | None = None,
        evidence_ids: Iterable[str] = (),
        ear_ids: Iterable[str] = (),
    ) -> None:
        """Durably record the ONE final disposition for a registered candidate.

        A second/conflicting disposition for the same candidate is rejected
        deterministically (no silent overwrite of disposition history).
        """
        if not reason or not str(reason).strip():
            raise LedgerValidationError("disposition requires a non-empty reason")
        try:
            disp = CandidateDisposition(disposition)
        except ValueError:
            raise LedgerValidationError(f"unknown disposition {disposition!r}") from None

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            self._require_run(conn, ledger_id)
            self._require_mutable(conn, ledger_id)
            cand = conn.execute(
                "SELECT 1 FROM ledger_candidate WHERE ledger_id = ? AND source_candidate_id = ?",
                (ledger_id, source_candidate_id),
            ).fetchone()
            if cand is None:
                raise LedgerValidationError(
                    f"candidate {source_candidate_id!r} was never registered"
                )
            try:
                conn.execute(
                    "INSERT INTO ledger_disposition (ledger_id, source_candidate_id,"
                    " disposition, reason, src01_id, evidence_ids_json, ear_ids_json,"
                    " disposed_at) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        ledger_id, source_candidate_id, disp.value, str(reason), src01_id,
                        json.dumps(list(evidence_ids)), json.dumps(list(ear_ids)),
                        self._now(),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerIdentityConflict(
                    f"candidate {source_candidate_id!r} already has a final disposition: {exc}"
                ) from None
            self._write_event(conn, ledger_id, "CANDIDATE_DISPOSED", {
                "source_candidate_id": source_candidate_id,
                "disposition": disp.value,
            })
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    # -- terminalization --------------------------------------------------

    def terminalize(
        self,
        ledger_id: str,
        *,
        terminal_status: str | TerminalStatus,
        terminal_at: str | None = None,
        result_artifact_ref: str | None = None,
        result_sha256: str | None = None,
        failure_detail: str | None = None,
    ) -> None:
        """Finalize the run. Rejected if already terminal or if any registered
        candidate lacks a disposition (no silently undisposed discovered source).
        """
        try:
            status = TerminalStatus(terminal_status)
        except ValueError:
            raise LedgerValidationError(f"unknown terminal_status {terminal_status!r}") from None

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            self._require_run(conn, ledger_id)
            if self._terminal_status(conn, ledger_id) is not None:
                raise LedgerTerminalError(
                    f"ledger run {ledger_id!r} is already terminalized"
                )
            undisposed = conn.execute(
                "SELECT c.source_candidate_id FROM ledger_candidate c"
                " LEFT JOIN ledger_disposition d"
                "   ON d.ledger_id = c.ledger_id AND d.source_candidate_id = c.source_candidate_id"
                " WHERE c.ledger_id = ? AND d.source_candidate_id IS NULL"
                " ORDER BY c.source_candidate_id",
                (ledger_id,),
            ).fetchall()
            if undisposed:
                ids = [r["source_candidate_id"] for r in undisposed]
                raise LedgerValidationError(
                    f"cannot terminalize: {len(ids)} registered source candidate(s) "
                    f"lack a disposition: {ids}"
                )
            try:
                conn.execute(
                    "INSERT INTO ledger_terminal (ledger_id, terminal_at, terminal_status,"
                    " result_artifact_ref, result_sha256, failure_detail) VALUES (?,?,?,?,?,?)",
                    (
                        ledger_id,
                        _iso(terminal_at) if terminal_at is not None else self._now(),
                        status.value, result_artifact_ref, result_sha256, failure_detail,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerTerminalError(
                    f"ledger run {ledger_id!r} already terminal: {exc}"
                ) from None
            self._write_event(conn, ledger_id, "RUN_TERMINALIZED", {
                "terminal_status": status.value,
                "result_sha256": result_sha256,
            })
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    # -- reads ------------------------------------------------------------

    def load_run(self, ledger_id: str) -> RunRecord:
        """Deterministic materialized read model, reloaded from durable state."""
        conn = self._connect()
        try:
            head = conn.execute(
                "SELECT * FROM ledger_run WHERE ledger_id = ?", (ledger_id,)
            ).fetchone()
            if head is None:
                raise LedgerNotFound(f"ledger run {ledger_id!r} not found")
            attempts = tuple(
                AttemptRecord(
                    attempt_number=r["attempt_number"],
                    retry_mode=RetryMode(r["retry_mode"]),
                    provider_surface=r["provider_surface"],
                    transport_type=r["transport_type"],
                    started_at=r["started_at"],
                    completed_at=r["completed_at"],
                    outcome=r["outcome"],
                    error=r["error"],
                    telemetry=_telemetry_from_json(r["telemetry_json"]),
                )
                for r in conn.execute(
                    "SELECT * FROM ledger_attempt WHERE ledger_id = ? ORDER BY attempt_number",
                    (ledger_id,),
                ).fetchall()
            )
            candidates = tuple(
                CandidateRecord(
                    source_candidate_id=r["source_candidate_id"],
                    url_or_identifier=r["url_or_identifier"],
                    fingerprint=r["fingerprint"],
                    discovery_timestamp=r["discovery_timestamp"],
                    original_source_verification_status=r["verification_status"],
                    pit_eligibility=r["pit_eligibility"],
                )
                for r in conn.execute(
                    "SELECT * FROM ledger_candidate WHERE ledger_id = ?"
                    " ORDER BY source_candidate_id",
                    (ledger_id,),
                ).fetchall()
            )
            dispositions = tuple(
                DispositionRecord(
                    source_candidate_id=r["source_candidate_id"],
                    disposition=CandidateDisposition(r["disposition"]),
                    reason=r["reason"],
                    src01_id=r["src01_id"],
                    evidence_ids=tuple(json.loads(r["evidence_ids_json"] or "[]")),
                    ear_ids=tuple(json.loads(r["ear_ids_json"] or "[]")),
                    disposed_at=r["disposed_at"],
                )
                for r in conn.execute(
                    "SELECT * FROM ledger_disposition WHERE ledger_id = ?"
                    " ORDER BY source_candidate_id",
                    (ledger_id,),
                ).fetchall()
            )
            term = conn.execute(
                "SELECT * FROM ledger_terminal WHERE ledger_id = ?", (ledger_id,)
            ).fetchone()
            return RunRecord(
                ledger_id=head["ledger_id"],
                research_run_id=head["research_run_id"],
                rrm_manifest_id=head["rrm_manifest_id"],
                case_id=head["case_id"],
                case_version=head["case_version"],
                evidence_gap_id=head["evidence_gap_id"],
                request_id=head["request_id"],
                idempotency_key=head["idempotency_key"],
                notebook_identity=head["notebook_identity"],
                pit_context_id=head["pit_context_id"],
                pit_mode=head["pit_mode"],
                as_of=head["as_of"],
                input_snapshot_hash=head["input_snapshot_hash"],
                provider_surface=head["provider_surface"],
                transport_type=head["transport_type"],
                started_at=head["started_at"],
                attempts=attempts,
                candidates=candidates,
                dispositions=dispositions,
                terminal_at=None if term is None else term["terminal_at"],
                terminal_status=None if term is None else TerminalStatus(term["terminal_status"]),
                result_artifact_ref=None if term is None else term["result_artifact_ref"],
                result_sha256=None if term is None else term["result_sha256"],
                failure_detail=None if term is None else term["failure_detail"],
            )
        finally:
            conn.close()

    def contains(self, ledger_id: str) -> bool:
        conn = self._connect()
        try:
            return conn.execute(
                "SELECT 1 FROM ledger_run WHERE ledger_id = ?", (ledger_id,)
            ).fetchone() is not None
        finally:
            conn.close()

    def list_runs(self) -> list[str]:
        conn = self._connect()
        try:
            return [
                r["ledger_id"]
                for r in conn.execute(
                    "SELECT ledger_id FROM ledger_run ORDER BY ledger_id"
                ).fetchall()
            ]
        finally:
            conn.close()

    def events(self, ledger_id: str) -> list[tuple[int, str, str]]:
        """The raw append-only event log for a run: (seq, event_type, created_at)."""
        conn = self._connect()
        try:
            return [
                (r["seq"], r["event_type"], r["created_at"])
                for r in conn.execute(
                    "SELECT seq, event_type, created_at FROM ledger_event"
                    " WHERE ledger_id = ? ORDER BY seq",
                    (ledger_id,),
                ).fetchall()
            ]
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# RRM-01 linkage (bounded reference-validation helper)
# ---------------------------------------------------------------------------


def validate_rrm_deep_research_runs(
    ledger_store: DeepResearchRunLedgerStore,
    deep_research_runs: Iterable[str] | None,
    *,
    require_resolvable: bool = True,
) -> list[str]:
    """Validate ``RRM-01.deep_research_runs[]`` as LEDGER ID STRINGS only.

    M6.0 §7.4: the frozen ``Optional[list[str]]`` field stores ledger IDs — no
    dictionaries, no embedded ledger objects. When ``require_resolvable`` each
    string must resolve to an existing ledger record.

    Raises:
        LedgerValidationError: a non-string entry, or an unresolvable ledger id
            when ``require_resolvable`` is set.
    """
    if deep_research_runs is None:
        return []
    out: list[str] = []
    for ref in deep_research_runs:
        if not isinstance(ref, str) or not ref.strip():
            raise LedgerValidationError(
                "RRM-01.deep_research_runs entries must be ledger-id strings"
            )
        if require_resolvable and not ledger_store.contains(ref):
            raise LedgerValidationError(
                f"RRM-01.deep_research_runs entry {ref!r} does not resolve to a ledger record"
            )
        out.append(ref)
    return out
