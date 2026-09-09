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

from qad.ids import generate_uuid7
from qad.models.family_c import (
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import (
    RetryRecord,
    RetryRecordStatus,
    RunManifestRecord,
    ServiceInvocation,
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
    """

    execution: ExecutionContext
    execution_id: str
    checkpoint_ref: str | None = None
    previous_output_ids: list[str] = field(default_factory=list)
    produced_output_ids: list[str] = field(default_factory=list)


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
        if not self._store.contains("SI-01", invocation.invocation_id):
            raise MissingForeignKey(
                f"SI-01/{invocation.invocation_id}: invocation not found — "
                f"RR-01.invocation_id FK requires it (fail closed)",
                schema_id="RR-01",
                field="invocation_id",
                target_schema="SI-01",
                target_ids=[invocation.invocation_id],
            )

        # -- Manifest preflight (BEFORE any stage execution / any write) ----
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
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=last.retry_count > 0,
                    error=None,
                )
            if _enum_str(last.stage_state) == "FAILED":
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_ledger(invocation.invocation_id),
                    status=RetryRecordStatus.FAILED,
                    retried=True,
                    error=last.failure_reason,
                )
            # IN_PROGRESS -> resume mid-flight (initial already executed).
            state = _ExecState(
                stage_id=last.stage_id,
                started_at=last.started_at,
                completed_at=last.completed_at or last.started_at,
                checkpoint_ref=last.checkpoint_ref or _cp_encode(case_version, last.stage_id),
                previous_outputs=list(last.output_ids or []),
                retry_count=last.retry_count or 0,
            )
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

        # -- INITIAL execution (NOT an RR-01) --------------------------------
        state = _ExecState(
            stage_id=self._uuid(),
            started_at=self._now(),
            completed_at=self._now(),  # FIELD_IMMUTABLE: captured once, stable
            checkpoint_ref="",  # set below with the true stage_id encoding
            previous_outputs=[],
            retry_count=0,
        )
        state.checkpoint_ref = _cp_encode(case_version, state.stage_id)
        ctx = self._build_ctx(execution, state, initial=True)
        try:
            stage(ctx)
        except RetryableError as exc:
            # Initial failed retryably -> IN_PROGRESS (NOT terminal FAILED) and
            # the retry workflow begins (re-audit §3, SM-3).
            self._write_rsr(
                execution, state, ResearchStageRecordStage_state.IN_PROGRESS,
                error=str(exc), produced=ctx.produced_output_ids,
            )
            return self._retry_loop(
                invocation, execution, stage, state, 1, manifest_id,
            )
        except Exception as exc:  # noqa: BLE001 — deterministic/unknown
            self._write_rsr(
                execution, state, ResearchStageRecordStage_state.FAILED,
                error=f"{type(exc).__name__}: {exc}",
                produced=ctx.produced_output_ids,
            )
            raise
        else:
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
                        invocation, attempt_number, RetryRecordStatus.RETRYING,
                        error=str(exc), manifest_id=manifest_id,
                    )
                    continue
                # Budget exhausted -> terminal FAILED (ESCALATED never used).
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.FAILED,
                    error=str(exc), attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, RetryRecordStatus.FAILED,
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
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, RetryRecordStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    manifest_id=manifest_id,
                )
                raise
            else:
                self._write_rsr(
                    execution, state, ResearchStageRecordStage_state.COMPLETE,
                    error=None, attempt_number=attempt_number,
                    produced=ctx.produced_output_ids,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, RetryRecordStatus.SUCCEEDED,
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
    ) -> None:
        """Persist a version of the SAME stage_id (append-only, M5.2).

        Outputs = previous + produced by THIS attempt (frozen revision rule:
        restart from last checkpoint preserves previous output).  The
        cumulative outputs carried in ``state.previous_outputs`` are updated
        so the NEXT retry resumes from this authoritative, just-persisted
        state (re-audit §4).  ``completed_at``/``started_at`` are
        FIELD_IMMUTABLE and stable across all versions.
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
        self._stage_store.store(rec)  # APPEND_ONLY_STATE -> prior version kept
        state.checkpoint_ref = _cp_encode(execution.case_version, state.stage_id)

    def _write_attempt_and_manifest(
        self,
        invocation: ServiceInvocation,
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
        rid = self._uuid()
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