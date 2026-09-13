"""M5.3 S8 — Retry Kernel (CORRECTION PASS 2 — FD #138, RE-AUDIT FAIL 2 corrections).

Corrected implementation per the Founder independent RE-AUDIT (9 Sep 2026),
remaining under FD #138 as the governing authority (NO new Founder decision):

- **RSR-01 is the SOLE execution authority.**  Execution identity =
  (case_id, case_version, stage_name); case_version resolved from the
  authoritative RRM-01 run context.  Retry accounting and terminal replay are
  DRIVEN BY RSR-01, never by RR-01 count alone.
  Re-audit §2: a persisted IN_PROGRESS RSR (initial already ran, retry
  workflow pending) resumes as RETRY #N — the initial execution NEVER runs
  twice after an interrupted transient failure.
- **SM-3 stage lifecycle via ONE stable stage_id.**  RSR-01.stage_id is minted
  once per execution and UPDATED across attempts using the M5.2
  APPEND_ONLY_STATE version mechanism (prior versions recoverable).  State
  transitions: IN_PROGRESS while retryable-failing/checkpointing; COMPLETE
  only on final success; FAILED only when terminal (deterministic failure or
  retries exhausted).  No FAILED→COMPLETE transition; no fresh canonical
  identity to dodge a state transition.
- **Checkpoint genuinely flows into the next retry.**  After every RSR write
  the execution state (checkpoint_ref, cumulative previous_output_ids) is
  carried forward, so the next retry — inside one execute() call or after
  process restart — resumes from the authoritative, just-persisted checkpoint.
- **Case-version isolation.**  RSR lookup is scoped to
  (case_id, stage_name, case_version-from-checkpoint_prefix).  A new
  case_version starts its OWN stage chain; it must not inherit the prior
  version's outputs/checkpoint and must not false-replay.
- **Execution-identity scoping of RR terminal replay.**  RR-01 terminal state
  by invocation_id alone is NEVER used to short-circuit an execution.  A
  different stage or case_version under the same invocation executes fresh.
- **RRM lineage keeps accumulating.**  Every RR/RRM atomic batch re-loads the
  CURRENT authoritative RRM-01, appends the new retry_id, and store_batches
  (RR-01 + RRM-01 are same-store — M5.2 §7.1).  No stale-object overwrite.
- **Fixed retry budget (FD #138 §1):** INITIAL + max 3 retries = max 4 stage
  executions.  ESCALATED never produced; `escalated_to` never populated.
- **Fail-closed history:** unreadable RSR/RR state raises typed errors — the
  stage never executes on unreadable history.
- **Retried-write idempotency contract:** StageContext exposes a STABLE
  noncanonical `execution_id` string (case_id|case_version|stage_name|
  stage_id) that stages use to derive deterministic canonical write
  identities (see qad.ids.deterministic_uuid7).  The kernel does not own
  downstream stores; it supplies the stable execution/idempotency context.

Cross-anchor write order (documented honestly — NO cross-anchor transaction
framework, per re-audit §9): RSR (stage authority) is written FIRST, then the
RR-01 + RRM-01 atomic batch.  If the RR/RRM batch fails after the RSR update,
the stage state is honest (IN_PROGRESS while retrying; COMPLETE/FAILED only
terminal) and resume reconciles via RSR.retry_count — the missing RR record is
rewritten with a fresh retry_id.  Within one store, RR+RRM atomicity is
guaranteed by store_batch; across anchors (stage_store vs RunManifestStore)
no atomicity exists and the RSR-first ordering keeps the execution authority
correct under every failure mode.

Noncanonical only: ExecutionContext / StageContext / RetryOutcome /
RetryPolicy (+ StageContext.execution_id) — service-layer types, not
canonical schemas (FD #138 §5; re-audit §8).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from qad.ids import deterministic_uuid7, generate_uuid7
from qad.models.family_c import (
    ResearchFailureRecord,
    ResearchFailureRecordFailure_type,
    ResearchFailureRecordResolution,
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import (
    RetryRecord,
    RetryRecordStatus,
    RunManifestRecord,
    ServiceInvocation,
    ServiceInvocationStatus,
)
from qad.persistence import (
    ImmutabilityViolation,
    IntegrityConflict,
    MissingForeignKey,
    RunManifestStore,
)
from qad.persistence.interfaces import CanonicalRecordStore


class RetryableError(Exception):
    """Marker for a transient, retry-worthy failure (network, rate-limit,
    timeout, 5xx).  Deterministic contract failures (ValidationFailure,
    IntegrityConflict, ImmutabilityViolation, MissingForeignKey) are NOT
    retryable and MUST be raised as their own typed errors.
    """


@dataclass(frozen=True)
class RetryPolicy:
    """Bounded retry policy (FD #138: max 3 RETRIES per stage — the initial
    execution is separate, so a stage may execute at most 4 times)."""

    max_retries: int = 3

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")


@dataclass(frozen=True)
class ExecutionContext:
    """Noncanonical logical execution identity (FD #138 §4)."""

    case_id: str
    case_version: str
    stage_name: ResearchStageRecordStage_name


@dataclass
class StageContext:
    """Noncanonical context handed to the stage callback.

    ``execution_id`` is the STABLE machine-readable execution identity
    (case_id|case_version|stage_name|stage_id).  It is identical across
    retries and across process restarts within one execution lifecycle, and
    is the deterministic source for stage-owned canonical write identities
    (re-audit §8).

    ``anchor_ts_ms`` (FD #139 R5 — Correction Pass 3): the REAL Unix epoch
    milliseconds of the persisted RSR-01 execution anchor (``started_at``).
    Deterministic UUID v7 stage-owned identities MUST use this anchor as the
    48-bit timestamp (RFC-9562 §5.7) — never hash-derived bits (F5 fix).
    """

    execution: ExecutionContext
    execution_id: str
    checkpoint_ref: str | None = None
    previous_output_ids: list[str] = field(default_factory=list)
    produced_output_ids: list[str] = field(default_factory=list)
    anchor_ts_ms: int = 0


@dataclass(frozen=True)
class RetryOutcome:
    """Deterministic result of one ``RetryKernel.execute`` cycle."""

    invocation_id: str
    attempt_records: list[RetryRecord] = field(default_factory=list)
    status: RetryRecordStatus = RetryRecordStatus.FAILED
    retried: bool = False
    error: str | None = None


# Noncanonical mutable execution-state carrier (per execute() cycle).
@dataclass
class _ExecState:
    stage_id: str
    started_at: str
    completed_at: str
    checkpoint_ref: str
    previous_outputs: list[str] = field(default_factory=list)
    retry_count: int = 0


_TERMINAL_STATES = {
    ResearchStageRecordStage_state.COMPLETE,
    ResearchStageRecordStage_state.FAILED,
}
_CP_PREFIX = "cp"  # checkpoint_ref encoding: "cp:<case_version>:<stage_id>"


def _enum_str(value: Any) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _cp_encode(case_version: str, stage_id: str) -> str:
    return f"{_CP_PREFIX}:{case_version}:{stage_id}"


def _started_at_to_ms(started_at: str | None) -> int:
    """Real Unix epoch milliseconds for the RSR-01 ``started_at`` execution
    anchor (FD #139 R5).

    The kernel mints ``started_at`` as RFC3339 second-precision
    (``%Y-%m-%dT%H:%M:%SZ``); per ruling R5 second-level precision may map
    to milliseconds ending in ``000``.  Deterministic UUID v7 stage-owned
    identities use this anchor for the 48-bit timestamp.  If the anchor is
    missing or unparseable, return 0 so the caller fails closed rather than
    silently deriving a fake timestamp.
    """
    if not started_at:
        return 0
    text = str(started_at).strip()
    try:
        # RFC3339 second precision (kernel now() format) — parse UTC.
        from datetime import datetime, timezone
        dt = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
        return int(dt.replace(tzinfo=timezone.utc).timestamp()) * 1000
    except (ValueError, TypeError):
        return 0


def _cp_version(ref: str | None) -> str | None:
    """Extract the case_version from a checkpoint_ref (None if unparseable)."""
    if not ref:
        return None
    parts = str(ref).split(":")
    if len(parts) < 3 or parts[0] != _CP_PREFIX:
        return None
    return parts[1]


class RetryKernel:
    """Bounded deterministic retry controller (M3-SERVICES S8, FD #138).

    ``store`` (RunManifestStore) holds SI-01 / RR-01 / RRM-01; ``stage_store``
    (CanonicalRecordStore) holds RSR-01 (the stage/checkpoint authority).
    """

    def __init__(
        self,
        store: RunManifestStore,
        stage_store: CanonicalRecordStore,
        *,
        policy: RetryPolicy | None = None,
        now: Callable[[], str] | None = None,
        uuid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._stage_store = stage_store
        self._policy = policy or RetryPolicy()
        self._now = now or (
            lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        self._uuid = uuid_factory or (lambda: str(generate_uuid7()))

    # -- public API ---------------------------------------------------------

    def execute(
        self,
        invocation: ServiceInvocation,
        stage_name: ResearchStageRecordStage_name,
        stage: Callable[[StageContext], None],
        *,
        manifest_id: str,
    ) -> RetryOutcome:
        """Run ``stage`` under the bounded retry policy.

        Preflight (BEFORE any stage execution):
            1. SI-01 must exist (RR-01.invocation_id FK).
            2. RRM-01 must exist, be RUNNING, and match the invocation's
               case_id (authoritative case_version source).
            3. RSR-01 history for the execution identity must be readable.

        Resume semantics (re-audit §2):
            no RSR chain            -> INITIAL execution
            last RSR COMPLETE       -> replay SUCCEEDED (no re-execution)
            last RSR FAILED         -> replay FAILED   (no re-execution)
            last RSR IN_PROGRESS    -> resume as RETRY #(retry_count+1)

        Raises:
            MissingForeignKey: invocation or manifest not present.
            ImmutabilityViolation: manifest is terminal.
            <typed store errors>: RSR/RR history unreadable (fail closed).
            <original non-retryable error>: deterministic/unknown failure —
                recorded honestly (RSR FAILED + RR FAILED when on a retry),
                then re-raised.
        """
        # -- Manifest preflight (BEFORE any stage execution / any write) ----
        # CP3 F3 (FD #139 R3): pre-existing SI-01 is NO LONGER required for
        # the INITIAL attempt.  The kernel persists the authoritative SI-01
        # with the ACTUAL outcome (never the caller object's stale status)
        # after the initial callback, BEFORE any retry processing.
        manifest = self._load_running_manifest(manifest_id)
        if manifest.case_id != invocation.case_id:
            raise IntegrityConflict(
                f"RRM-01/{manifest_id}.case_id ({manifest.case_id}) != "
                f"SI-01.invocation case_id ({invocation.case_id}) — "
                f"run context mismatch (fail closed)",
                schema_id="RRM-01",
                record_id=manifest_id,
            )
        case_version = manifest.case_version
        execution = ExecutionContext(
            case_id=invocation.case_id,
            case_version=case_version,
            stage_name=stage_name,
        )

        chain = self._rsr_history(execution)

        # -- Resume / replay decision (RSR is the execution authority) ------
        if chain:
            last = chain[-1]
            if _enum_str(last.stage_state) == "COMPLETE":
                # CP3 F2 (FD #139 R2): terminal replay is permitted ONLY after
                # retry provenance is complete or deterministically reconciled
                # (for retry_count > 0).  retry_count == 0 is a valid INITIAL
                # terminal execution and requires no RR provenance.
                self._reconcile_terminal_provenance(
                    invocation, execution, last,
                    terminal=ResearchStageRecordStage_state.COMPLETE,
                    manifest_id=manifest_id,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=last.retry_count > 0,
                    error=None,
                )
            if _enum_str(last.stage_state) == "FAILED":
                self._reconcile_terminal_provenance(
                    invocation, execution, last,
                    terminal=ResearchStageRecordStage_state.FAILED,
                    manifest_id=manifest_id,
                )
                # CP3 F4: restart/replay of a terminal FAILED must NOT
                # duplicate the RFR — _ensure_rfr() is deterministic and
                # returns None when the logical failure is already recorded.
                # (F2 reconciliation later must also not duplicate RFR: the
                # same deterministic failure_id guard applies.)
                self._ensure_rfr(
                    execution, self._exec_state_view(last), error=last.failure_reason,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.FAILED,
                    retried=True,
                    error=last.failure_reason,
                )
            # IN_PROGRESS -> F3 crash-state recovery (FD #139 R3).  The RSR
            # anchor + the authoritative SI-01 initial outcome are the
            # execution authority; the caller-supplied object is NOT trusted
            # for outcome status.  Load SI-01 by invocation_id from the store.
            si01 = self._load_si01(invocation.invocation_id)
            if si01 is None:
                # STATE A: RSR IN_PROGRESS anchor persisted but no
                # authoritative SI-01 outcome -> FAIL CLOSED.  Never rerun the
                # initial callback, never start retry #1, never invent
                # SUCCESS/FAILURE, never mint a new stage_id.
                raise IntegrityConflict(
                    f"RSR-01/{last.stage_id}: IN_PROGRESS anchor without "
                    f"authoritative SI-01 outcome — initial execution was "
                    f"anchored but its result was never durably persisted "
                    f"(recovery required; fail closed per FD #139 R3)",
                    schema_id="RSR-01",
                    record_id=last.stage_id,
                )
            state = _ExecState(
                stage_id=last.stage_id,
                started_at=last.started_at,
                completed_at=last.completed_at or last.started_at,
                checkpoint_ref=last.checkpoint_ref or _cp_encode(case_version, last.stage_id),
                previous_outputs=list(last.output_ids or []),
                retry_count=last.retry_count or 0,
            )
            if si01.status is ServiceInvocationStatus.SUCCESS:
                # STATE B: authoritative SI-01 SUCCESS -> the initial callback
                # already succeeded; the crash happened between the SI-01 write
                # and the RSR COMPLETE write.  Reconcile RSR forward WITHOUT
                # re-executing the callback.
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.COMPLETE,
                    error=None,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=state.retry_count > 0,
                    error=None,
                )
            # STATE C: authoritative SI-01 FAILURE/TIMEOUT -> the initial
            # outcome is a known failure.  Do NOT rerun the initial callback;
            # enter the retry path only if the retry policy allows it.
            next_retry = state.retry_count + 1
            if next_retry > self._policy.max_retries:
                # Corrupted/over-budget resume -> terminal FAILED, no re-exec.
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.FAILED,
                    error="retry budget already exhausted at resume — fail closed",
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.FAILED,
                    retried=True,
                    error="retry budget already exhausted at resume — fail closed",
                )
            return self._retry_loop(
                invocation, execution, stage, state, next_retry, manifest_id,
            )

        # -- INITIAL execution (NOT an RR-01) — CP3 F3 sequence (FD #139 R3) -
        state = _ExecState(
            stage_id=self._uuid(),
            started_at=self._now(),
            completed_at=self._now(),  # FIELD_IMMUTABLE: captured once, stable
            checkpoint_ref="",  # set below with the true stage_id encoding
            previous_outputs=[],
            retry_count=0,
        )
        state.checkpoint_ref = _cp_encode(case_version, state.stage_id)
        # R3 B: persist the RSR-01 IN_PROGRESS anchor BEFORE the initial stage
        # callback (stable stage_id / started_at / checkpoint / execution
        # identity binding).  The anchor must precede stage-owned canonical
        # writes.
        self._write_rsr(
            execution, state, ResearchStageRecordStage_state.IN_PROGRESS,
            error=None,
        )
        ctx = self._build_ctx(execution, state, initial=True)
        try:
            stage(ctx)
        except RetryableError as exc:
            # R3 D: persist the authoritative immutable SI-01 with the ACTUAL
            # initial outcome (retryable failure -> FAILURE).  NEVER trust the
            # caller object's pre-populated status.
            self._persist_si01_actual(
                invocation, status=ServiceInvocationStatus.FAILURE,
                error=str(exc),
            )
            # R3 E: only AFTER authoritative SI-01 exists may retry processing
            # begin (RR-01.invocation_id FK strict).  RSR stays IN_PROGRESS
            # (NOT terminal FAILED) and the retry workflow begins.
            self._write_rsr(
                execution, state, ResearchStageRecordStage_state.IN_PROGRESS,
                error=str(exc), produced=ctx.produced_output_ids,
            )
            return self._retry_loop(
                invocation, execution, stage, state, 1, manifest_id,
            )
        except Exception as exc:  # noqa: BLE001 — deterministic/unknown
            reason = f"{type(exc).__name__}: {exc}"
            self._persist_si01_actual(
                invocation, status=ServiceInvocationStatus.FAILURE,
                error=reason,
            )
            # CP3 F4: deterministic initial terminal failure -> exactly one
            # RFR-01, committed atomically with the terminal RSR FAILED.
            self._write_rsr(
                execution, state, ResearchStageRecordStage_state.FAILED,
                error=reason, produced=ctx.produced_output_ids,
                rfr=self._ensure_rfr(execution, state, error=reason),
            )
            raise
        else:
            self._persist_si01_actual(
                invocation, status=ServiceInvocationStatus.SUCCESS, error=None,
            )
            self._write_rsr(
                execution, state, ResearchStageRecordStage_state.COMPLETE,
                error=None, produced=ctx.produced_output_ids,
            )
            return RetryOutcome(
                invocation_id=invocation.invocation_id,
                attempt_records=[],
                status=RetryRecordStatus.SUCCEEDED,
                retried=False,
                error=None,
            )

    # -- retry loop ----------------------------------------------------------

    def _retry_loop(
        self,
        invocation: ServiceInvocation,
        execution: ExecutionContext,
        stage: Callable[[StageContext], None],
        state: _ExecState,
        next_retry: int,
        manifest_id: str,
    ) -> RetryOutcome:
        """Retries #next_retry..max_retries (RR-01 attempts)."""
        for attempt_number in range(next_retry, self._policy.max_retries + 1):
            last_attempt = attempt_number == self._policy.max_retries
            ctx = self._build_ctx(execution, state)
            try:
                stage(ctx)
            except RetryableError as exc:
                if not last_attempt:
                    # Budget remains -> stay IN_PROGRESS + record scheduled retry.
                    self._write_rsr(
                        execution, state,
                        ResearchStageRecordStage_state.IN_PROGRESS,
                        error=str(exc), attempt_number=attempt_number,
                        produced=ctx.produced_output_ids,
                    )
                    self._write_attempt_and_manifest(
                        invocation, execution, state, attempt_number,
                        RetryRecordStatus.RETRYING,
                        error=str(exc), manifest_id=manifest_id,
                    )
                    continue
                # Budget exhausted -> terminal FAILED (ESCALATED never used).
                # CP3 F4: retry exhaustion -> exactly one RFR-01, committed
                # atomically with the terminal RSR FAILED (same store).
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.FAILED,
                    error=str(exc), attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                    rfr=self._ensure_rfr(execution, state, error=str(exc)),
                )
                self._write_attempt_and_manifest(
                    invocation, execution, state, attempt_number,
                    RetryRecordStatus.FAILED,
                    error=str(exc), manifest_id=manifest_id,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.FAILED,
                    retried=True,
                    error=str(exc),
                )
            except Exception as exc:  # noqa: BLE001 — deterministic/unknown
                reason = f"{type(exc).__name__}: {exc}"
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.FAILED,
                    error=reason, attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                    rfr=self._ensure_rfr(execution, state, error=reason),
                )
                self._write_attempt_and_manifest(
                    invocation, execution, state, attempt_number,
                    RetryRecordStatus.FAILED,
                    error=reason, manifest_id=manifest_id,
                )
                raise
            else:
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.COMPLETE,
                    error=None, attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                )
                self._write_attempt_and_manifest(
                    invocation, execution, state, attempt_number,
                    RetryRecordStatus.SUCCEEDED,
                    error=None, manifest_id=manifest_id,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=True,
                    error=None,
                )

        raise IntegrityConflict(  # pragma: no cover — logically unreachable
            f"RR-01/{invocation.invocation_id}: unexpected loop exit (fail closed)",
            schema_id="RR-01",
            record_id=invocation.invocation_id,
        )

    # -- store reads (fail closed) -------------------------------------------

    def _rr_ledger(self, invocation_id: str) -> list[RetryRecord]:
        """Immutable retry ledger for an invocation (oldest first)."""
        try:
            all_records = self._store.list_all("RR-01")
        except Exception as exc:  # noqa: BLE001 — propagate, never swallow
            raise type(exc)(
                f"RR-01 retry history unreadable — fail closed: {exc}"
            ) from exc
        attempts = [r for r in all_records if r.invocation_id == invocation_id]
        attempts.sort(key=lambda r: int(r.attempt_number)
                      if str(r.attempt_number).isdigit() else 0)
        return attempts

    def _load_si01(self, invocation_id: str) -> ServiceInvocation | None:
        """Load the AUTHORITATIVE SI-01 by invocation_id, or None.

        CP3 F3 (FD #139 R3): crash/retry recovery MUST read the persisted
        canonical SI-01 fom the store — never trust a caller-supplied
        ``ServiceInvocation`` object whose ``.status`` may be a stale
        request default.  Fail-closed callers treat None as
        'outcome not durably persisted'.
        """
        if not self._store.contains("SI-01", invocation_id):
            return None
        return self._store.load("SI-01", invocation_id)

    def _rsr_history(
        self, execution: ExecutionContext,
    ) -> list[ResearchStageRecord]:
        """RSR-01 records for the EXECUTION IDENTITY, attempt order.

        Scoped to (case_id, stage_name, case_version-from-checkpoint_prefix) —
        a new case_version starts its OWN chain (re-audit §5).
        Fail closed: unreadable stage-state store means the kernel cannot
        establish the authoritative RSR state -> the stage MUST NOT execute.
        """
        try:
            all_records = self._stage_store.list_all("RSR-01")
        except Exception as exc:  # noqa: BLE001 — propagate
            raise type(exc)(
                f"RSR-01 stage-state unreadable — cannot establish checkpoint "
                f"authority, fail closed: {exc}"
            ) from exc
        version = execution.case_version
        recs = [
            r for r in all_records
            if r.case_id == execution.case_id
            and r.stage_name == execution.stage_name
            and _cp_version(r.checkpoint_ref) == version
        ]
        recs.sort(key=lambda r: (r.started_at, r.stage_id))
        return recs

    # -- store writes ---------------------------------------------------------

    def _build_ctx(
        self,
        execution: ExecutionContext,
        state: _ExecState,
        *,
        initial: bool = False,
    ) -> StageContext:
        return StageContext(
            execution=execution,
            execution_id=(
                f"{execution.case_id}|{execution.case_version}|"
                f"{_enum_str(execution.stage_name)}|{state.stage_id}"
            ),
            checkpoint_ref=state.checkpoint_ref,
            previous_output_ids=list(state.previous_outputs),
            produced_output_ids=[],
            # FD #139 R5: REAL epoch-ms of the RSR-01 anchor (started_at).
            # Second-level precision maps to ms ending in 000 (ruling R5).
            anchor_ts_ms=_started_at_to_ms(state.started_at),
        )

    def _write_rsr(
        self,
        execution: ExecutionContext,
        state: _ExecState,
        stage_state: ResearchStageRecordStage_state,
        *,
        error: str | None,
        attempt_number: int | None = None,
        produced: list[str] | None = None,
        rfr: ResearchFailureRecord | None = None,
    ) -> None:
        """Persist a version of the SAME stage_id (append-only, M5.2).

        Outputs = previous + produced by THIS attempt (frozen revision rule:
        restart from last checkpoint preserves previous output).  The
        cumulative outputs carried in ``state.previous_outputs`` are updated
        so the NEXT retry resumes from this authoritative, just-persisted
        state (re-audit §4).  ``completed_at``/``started_at`` are
        FIELD_IMMUTABLE and stable across all versions.

        CP3 F4 (FD #139 R4): when ``rfr`` is supplied (terminal SM-3 FAILED),
        the RSR FAILED record and the RFR-01 record are committed in ONE
        same-store atomic batch (both live in stage_store) — no avoidable
        RSR-FAILED / RFR partial window.
        """
        current_outputs = list(state.previous_outputs) + list(produced or [])
        state.previous_outputs = current_outputs
        if attempt_number is not None:
            state.retry_count = attempt_number
        rec = ResearchStageRecord(
            stage_id=state.stage_id,
            case_id=execution.case_id,
            stage_name=execution.stage_name,
            stage_state=stage_state,
            started_at=state.started_at,       # FIELD_IMMUTABLE: stable
            completed_at=state.completed_at,   # FIELD_IMMUTABLE: stable
            responsible_role="S8",
            checkpoint_ref=state.checkpoint_ref,
            output_ids=current_outputs,
            retry_count=state.retry_count,
            failure_reason=error,
        )
        if rfr is not None:
            # Same-store atomic: terminal RSR FAILED + RFR-01 together.
            self._stage_store.store_batch([rec, rfr])
        else:
            # APPEND_ONLY_STATE -> prior version kept
            self._stage_store.store(rec)
        state.checkpoint_ref = _cp_encode(execution.case_version, state.stage_id)

    def _exec_state_view(self, last: ResearchStageRecord) -> _ExecState:
        """Rebuild the execution-state view from a persisted RSR record.

        Shared by F2 terminal reconciliation and F4 RFR replay so both
        recompute the SAME deterministic identities/anchors as the live
        writer (same stage_id / started_at / checkpoint_ref).
        """
        return _ExecState(
            stage_id=last.stage_id,
            started_at=last.started_at,
            completed_at=last.completed_at or last.started_at,
            checkpoint_ref=last.checkpoint_ref,
            previous_outputs=list(last.output_ids or []),
            retry_count=int(last.retry_count or 0),
        )

    def _reconcile_terminal_provenance(
        self,
        invocation: ServiceInvocation,
        execution: ExecutionContext,
        last: ResearchStageRecord,
        *,
        terminal: ResearchStageRecordStage_state,
        manifest_id: str,
    ) -> None:
        """CP3 F2 (FD #139 R2) — cross-anchor terminal retry reconciliation.

        Invoked BEFORE any terminal replay.  Only applies when retry
        provenance is actually expected: ``last.retry_count > 0``.  A
        terminal RSR with ``retry_count == 0`` is a valid INITIAL terminal
        result and does NOT imply a missing RR.

        Expected provenance for a terminal RSR with ``retry_count = N``:

            RR-01 attempts 1..N, each with the DETERMINISTIC retry identity
            derived from THIS execution (see _retry_identity) — NOT every RR
            under the invocation.  RR records from a sibling stage sharing the
            same invocation_id have different retry identities and are never
            counted / cross-scoped.

        Correction rule (bounded, §R2): only the MECHANICALLY PROVABLE
        missing terminal attempt may be reconstructed — the known
        partial-terminal window where RSR went terminal FIRST and the
        terminal RR/RRM batch then failed.  Exactly attempt N is rebuilt,
        with the SAME deterministic retry_id it would have had live
        (recomputed, not a fresh random UUID — restart-stable).

        If a NON-TERMINAL intermediate attempt is unexpectedly missing, its
        historical outcome cannot be authoritatively derived -> FAIL CLOSED.
        Fictional intermediate history is never synthesized.
        """
        rc = int(last.retry_count or 0)
        if rc <= 0:
            return  # valid initial-terminal execution — no RR required
        ledger = self._rr_ledger(invocation.invocation_id)
        # Execution-scoped view: reconstruct the expected identity for each
        # attempt of THIS execution (same derivation as the live writer).
        state_view = _ExecState(
            stage_id=last.stage_id,
            started_at=last.started_at,
            completed_at=last.completed_at or last.started_at,
            checkpoint_ref=last.checkpoint_ref,
            previous_outputs=list(last.output_ids or []),
            retry_count=rc,
        )
        expected_ids = {
            n: self._retry_identity(execution, state_view, n)
            for n in range(1, rc + 1)
        }
        ledger_ids = {r.retry_id: r for r in ledger}
        present = {n for n, rid in expected_ids.items() if rid in ledger_ids}
        missing = [n for n in range(1, rc + 1) if n not in present]

        # Only the terminal attempt may be missing in a legitimate
        # partial-terminal window.  Anything else = unprovable history.
        if any(n < rc for n in missing):
            raise IntegrityConflict(
                f"RR-01/{invocation.invocation_id}: terminal RSR "
                f"(retry_count={rc}) has UNPROVABLE missing intermediate "
                f"retry history {missing} — cannot fabricate historical "
                f"outcomes (cross-anchor reconcile FAIL CLOSED; M5.2 §7.2)",
                schema_id="RR-01",
                record_id=invocation.invocation_id,
            )
        if rc in present:
            # Provenance already complete -> nothing to reconcile (RRM may
            # still need its summary restored — F6 owns the summary form; F2
            # restores required run provenance without comma-ID logic).
            self._restore_rrm_retry_summary(
                manifest_id, rc,
                terminal_rid=expected_ids[rc],
                terminal_state=terminal,
                invocation_id=invocation.invocation_id,
            )
            return

        # Reconstruct exactly the missing TERMINAL attempt (N) deterministically.
        terminal_status = (
            RetryRecordStatus.SUCCEEDED
            if terminal is ResearchStageRecordStage_state.COMPLETE
            else RetryRecordStatus.FAILED
        )
        if terminal_status is RetryRecordStatus.FAILED:
            error_text = last.failure_reason or "terminal failure (reconciled)"
        else:
            error_text = None
        rec = RetryRecord(
            retry_id=expected_ids[rc],
            invocation_id=invocation.invocation_id,
            attempt_number=str(rc),
            attempted_at=last.completed_at or last.started_at,
            status=terminal_status,
            error=error_text or "none",
            escalated_to=None,
        )
        self._restore_rrm_retry_summary(
            manifest_id, rc,
            terminal_rid=expected_ids[rc],
            terminal_state=terminal,
            invocation_id=invocation.invocation_id,
            reconstructed=[rec],
        )

    def _ensure_rfr(
        self,
        execution: ExecutionContext,
        state: _ExecState,
        *,
        error: str | None,
    ) -> ResearchFailureRecord | None:
        """CP3 F4 (FD #139 R4) — ResearchFailureRecord, exactly once.

        Returns a NEW deterministic RFR-01 for this terminal SM-3 FAILED, or
        None when one ALREADY exists for the same logical terminal failure
        (restart/replay and cross-anchor reconciliation must not duplicate).

        Deterministic failure_id (UUIDv7, corrected F5 derivation):
          seed = execution_id | checkpoint | 'research-failure'
          ts_ms = REAL persisted RSR.started_at epoch-ms.
        Intermediate retry failures (budget remaining) never reach this
        helper — RFR is ONLY for SM-3 terminal FAILED.
        """
        anchor_ms = _started_at_to_ms(state.started_at)
        cp = state.checkpoint_ref or _cp_encode(
            execution.case_version, state.stage_id)
        seed = (
            f"{execution.case_id}|{execution.case_version}|"
            f"{_enum_str(execution.stage_name)}|{state.stage_id}|{cp}|"
            f"research-failure"
        )
        fid = str(deterministic_uuid7(seed, ts_ms=anchor_ms))
        if self._stage_store.contains("RFR-01", fid):
            return None  # already recorded — exactly-once invariant
        reason = error or "terminal stage failure"
        return ResearchFailureRecord(
            failure_id=fid,
            case_id=execution.case_id,
            failure_reason=reason,
            failure_type=ResearchFailureRecordFailure_type.RETRY_LIMIT,
            resolution=ResearchFailureRecordResolution.UNRESOLVED,
            retry_count=state.retry_count or 0,
            stage_name=_enum_str(execution.stage_name),
            error_details=reason,
            failure_timestamp=self._now(),
            recorder="S8",
        )

    def _restore_rrm_retry_summary(
        self,
        manifest_id: str,
        retry_count: int,
        *,
        terminal_rid: str,
        terminal_state: ResearchStageRecordStage_state,
        invocation_id: str | None = None,
        reconstructed: list[RetryRecord] | None = None,
    ) -> None:
        """Restore RRM-01 run provenance (count + terminal failure ref).

        FD #139 R6 owns the final ``retries = count`` summary refactor; this
        F2 helper restores the REQUIRED run provenance WITHOUT introducing any
        new comma-separated retry-ID logic.  When the run summary is still
        using the pre-R6 form, the authoritative count is derived from the
        execution-scoped RR ledger and written as the summary count.
        """
        manifest = self._load_running_manifest(manifest_id)
        recs = reconstructed or []
        if recs:
            # Atomic same-store batch: reconstructed RR + RRM (M5.2 §7.1).
            self._store.store_batch([*recs, manifest])
            # reload authoritative manifest after RR landed
            manifest = self._load_running_manifest(manifest_id)
        # F6 owns the exact count form for the LIVE writer; F2 restores the
        # authoritative count of retry attempts for THIS execution (never
        # comma-separated IDs).  Replay stays a no-op when the summary is
        # already reconciled (no stale overwrite, no write-churn on replay).
        updates: dict = {}
        if str(retry_count) != str(manifest.retries or ""):
            updates["retries"] = str(retry_count)
        if terminal_state is ResearchStageRecordStage_state.FAILED:
            failures = list(manifest.failures or [])
            if terminal_rid not in failures:
                failures.append(terminal_rid)
                updates["failures"] = failures
        if updates:
            enriched = manifest.model_copy(update=updates)
            self._store.store_batch([enriched])

    def _retry_identity(
        self, execution: ExecutionContext, state: _ExecState,
        attempt_number: int,
    ) -> str:
        """DETERMINISTIC RR-01 retry identity for an attempt (CP3 F2).

        Derives the RR retry_id for ONE logical execution + attempt from:

        * execution identity (case_id / case_version / stage_name)
        * stable RSR stage identity (`stage_id`) + checkpoint
          (cp:<case_version>:<stage_id>)
        * attempt number N
        * semantic label ``retry-record``

        The 48-bit timestamp is the REAL persisted RSR-01.started_at
        epoch-ms (FD #139 R5) — never recomputed from wall clock at
        recovery time, so the SAME attempt after restart yields the SAME
        retry_id.  Random bits: corrected deterministic 74-bit SHA-256
        derivation (F5).

        This is the ONLY execution-scoping mechanism on RR-01 (which has no
        stage_name/case_version columns): two stages sharing one invocation
        produce DIFFERENT retry identities, and F2 reconciliation recomputes
        exactly this id to detect missing terminal provenance.
        """
        anchor_ms = _started_at_to_ms(state.started_at)
        cp = state.checkpoint_ref or _cp_encode(
            execution.case_version, state.stage_id)
        seed = (
            f"{execution.case_id}|{execution.case_version}|"
            f"{_enum_str(execution.stage_name)}|{state.stage_id}|{cp}|"
            f"retry-record|{attempt_number}"
        )
        return str(deterministic_uuid7(seed, ts_ms=anchor_ms))

    def _persist_si01_actual(
        self,
        invocation: ServiceInvocation,
        *,
        status: ServiceInvocationStatus,
        error: str | None,
    ) -> None:
        """Persist the authoritative immutable SI-01 with the ACTUAL initial
        outcome (CP3 F3, FD #139 R3).

        The caller-supplied ``ServiceInvocation`` carries only stable request
        identity metadata (invocation_id/case_id/invoked_at/request_type/
        service_id); its ``.status`` is a request default and is NEVER the
        outcome authority.  SI-01 is RECORD_IMMUTABLE — on the initial attempt
        the kernel writes the outcome record once; if SI-01 already exists the
        record is left untouched (RR-01 FK integrity is preserved either way).
        """
        if self._store.contains("SI-01", invocation.invocation_id):
            return  # caller/requester-supplied request record — leave it
        rec = ServiceInvocation(
            invocation_id=invocation.invocation_id,
            case_id=invocation.case_id,
            invoked_at=invocation.invoked_at,
            request_type=invocation.request_type,
            service_id=invocation.service_id,
            status=status,
            completed_at=self._now(),
            error=error,
        )
        self._store.store(rec)

    def _write_attempt_and_manifest(
        self,
        invocation: ServiceInvocation,
        execution: ExecutionContext,
        state: _ExecState,
        attempt_number: int,
        status: RetryRecordStatus,
        *,
        error: str | None,
        manifest_id: str,
    ) -> RetryRecord:
        """Commit the RR-01 + RRM-01 provenance in ONE atomic batch.

        Re-audit §6: the CURRENT authoritative RRM-01 is re-loaded for every
        batch, so prior retry refs are never overwritten by a stale object.
        RRM-01 == RunManifestStore == RR-01 -> store_batch is the M5.2 §7.1
        same-store atomic boundary: all commit or none.
        """
        # CP3 F2 (FD #139 R2): deterministic retry identity — see
        # _retry_identity() for the execution-scoping rationale.
        rid = self._retry_identity(execution, state, attempt_number)
        # CP3 F2 (FD #139 R2): RR retry identity is DETERMINISTIC — derived from
        # the execution identity + stable RSR stage identity/checkpoint +
        # attempt number + semantic label ('retry-record') with the REAL
        # persisted RSR.started_at anchor as the UUIDv7 timestamp.  This is
        # the mechanism that binds an RR record to its logical execution
        # without adding a canonical field to RR-01 (so two stages sharing an
        # invocation are never cross-scoped, and F2 reconciliation recomputes
        # the exact same retry_id after restart).
        rid = self._retry_identity(execution, state, attempt_number)
        rec = RetryRecord(
            retry_id=rid,
            invocation_id=invocation.invocation_id,
            attempt_number=str(attempt_number),
            attempted_at=self._now(),
            status=status,
            error=error or "none",
            escalated_to=None,  # FD #138 §3: never populated in M5.3
        )
        manifest = self._load_running_manifest(manifest_id)  # authoritative NOW
        if status is RetryRecordStatus.RETRYING:
            existing = manifest.retries or ""
            refs = [x.strip() for x in existing.split(",") if x.strip()]
            if rid not in refs:
                refs.append(rid)
            enriched = manifest.model_copy(update={"retries": ",".join(refs)})
        elif status in (RetryRecordStatus.FAILED, RetryRecordStatus.ESCALATED):
            failures = list(manifest.failures or [])
            if rid not in failures:
                failures.append(rid)
            enriched = manifest.model_copy(update={"failures": failures})
        else:  # SUCCEEDED — nothing extra (the RETRYING refs record the lineage)
            enriched = manifest
        self._store.store_batch([rec, enriched])
        return rec

    def _load_running_manifest(self, manifest_id: str) -> RunManifestRecord:
        """Load a RUNNING manifest or fail closed (missing / terminal)."""
        if not self._store.contains("RRM-01", manifest_id):
            raise MissingForeignKey(
                f"RRM-01/{manifest_id}: manifest not found — cannot resolve "
                f"authoritative case_version (fail closed before execution)",
                schema_id="RRM-01",
                record_id=manifest_id,
            )
        manifest = self._store.load("RRM-01", manifest_id)
        run_state = _enum_str(manifest.run_state)
        if run_state in ("COMPLETED", "FAILED"):
            raise ImmutabilityViolation(
                f"RRM-01/{manifest_id}: terminal manifest ({run_state}) cannot "
                f"be the run context — provenance would be immutable (fail "
                f"closed before execution)",
                schema_id="RRM-01",
                record_id=manifest_id,
            )
        return manifest