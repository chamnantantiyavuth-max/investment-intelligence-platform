"""M5.3 S8 — Retry Kernel (CORRECTION ROUND — FD #138).

Corrected implementation per the Founder decisions recorded in FD #138:

- Retry budget: **INITIAL execution + max 3 retries = max 4 stage executions**.
  The initial execution is NOT retry #1 and is NOT an RR-01 (a clean first-run
  success creates ZERO RR-01 records).
- SI-01 = initial service invocation (frozen purpose). RR-01 = retry attempts
  for a failed operation (M4A RR-01 purpose).
- ESCALATED is REMOVED from M5.3: retry #3 fails -> FAILED always.
  ``escalated_to`` is never populated by this kernel.
- Execution identity = (case_id, authoritative case_version, stage_name),
  resolved from the authoritative RRM-01 (case_version) BEFORE executing.
- Checkpoint replay uses the frozen RSR-01 (ResearchStageRecord) as stage/state
  authority: resume from RSR-01.checkpoint_ref, preserve RSR-01.output_ids[].
  NEVER ``len(RR records) + 1``.
- Retry-history read failure is FAIL CLOSED (typed error propagates; the word
  "no retry history" is never inferred from a store failure).
- RR-01 + RRM-01 provenance update commit through ONE same-store atomic batch
  (RunManifestStore.store_batch). The manifest is preflighted (exists, RUNNING)
  BEFORE the stage executes. Missing/terminal manifest -> fail before execution.
- retry_id / stage_id are RFC-9562 UUID v7 (``qad.ids.generate_uuid7``).

Noncanonical only: ``ExecutionContext`` / ``StageContext`` / ``RetryOutcome`` /
``RetryPolicy`` are service-layer types, not canonical schemas (GO §5 permits a
bounded noncanonical execution-context / idempotency interface).
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
    """Noncanonical logical execution identity (FD #138 §4).

    case_version is resolved from the authoritative RRM-01 run context.
    """

    case_id: str
    case_version: str
    stage_name: ResearchStageRecordStage_name


@dataclass
class StageContext:
    """Noncanonical context handed to the stage callback.

    The stage receives enough deterministic context to resume from the
    authoritative checkpoint and avoid replaying already-completed output
    (GO §5): the execution identity, the checkpoint_ref of the last recorded
    RSR-01, the previously preserved output_ids, and a buffer the stage
    appends its own output ids to.
    """

    execution: ExecutionContext
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


# Terminal RR-01 statuses — the group is done once one appears.
_TERMINAL = {
    RetryRecordStatus.SUCCEEDED,
    RetryRecordStatus.FAILED,
}

_CP_PREFIX = "cp"  # checkpoint ref encoding: "cp:<case_version>:<stage_id>"


def _enum_str(value: Any) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _cp_encode(case_version: str, stage_id: str) -> str:
    return f"{_CP_PREFIX}:{case_version}:{stage_id}"


class RetryKernel:
    """Bounded deterministic retry controller (M3-SERVICES S8, FD #138).

    ``store`` is the authoritative RunManifestStore (SI-01 / RR-01 / RRM-01);
    ``stage_store`` is the canonical store that owns RSR-01 (the checkpoint /
    stage-state authority).  Both are existing canonical protocol surfaces —
    no new schema.
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

        FD #138 lifecycle:
            initial execution (SI-01)           — NOT an RR-01
            retry #1..max_retries (RR-01)       — retry attempts only

        Preflight (BEFORE the stage runs):
            1. SI-01 must exist (RR-01.invocation_id FK).
            2. RRM-01 must exist and be RUNNING (case_version authority).
            3. Execution identity (case_id, case_version, stage_name) resolved.
            4. RSR-01 + RR-01 history readable — otherwise fail closed.

        Raises:
            MissingForeignKey: invocation or manifest not present.
            ImmutabilityViolation: manifest is terminal (COMPLETED/FAILED).
            RuntimeError/typed store errors: retry history or RSR state
                unreadable (fail closed — never treated as 'no history').
            <original non-retryable error>: deterministic/unknown failure —
                recorded honestly (RSR FAILED; RR-01 FAILED when on a retry),
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

        # -- Execution identity ---------------------------------------------
        execution = ExecutionContext(
            case_id=invocation.case_id,
            case_version=case_version,
            stage_name=stage_name,
        )

        # -- Checkpoint replay (RSR-01 authority, version-aware) -------------
        rsr_records = self._rsr_history(invocation.case_id, stage_name)
        if rsr_records:
            last = rsr_records[-1]
            if (
                _enum_str(last.stage_state) == "COMPLETE"
                and last.checkpoint_ref
                and last.checkpoint_ref.count(":") >= 2
                and last.checkpoint_ref.split(":")[1] == case_version
            ):
                # Same execution + same case version -> replay. Stage NOT
                # re-run; zero new canonical records.
                rr = self._rr_history(invocation.invocation_id)
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=rr,
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=any(
                        r.status is RetryRecordStatus.RETRYING for r in rr),
                    error=None,
                )

        # -- Retry accounting (fail closed on unreadable history) ------------
        rr = self._rr_history(invocation.invocation_id)
        retries_used = len(rr)
        if retries_used > self._policy.max_retries:
            raise IntegrityConflict(
                f"RR-01/{invocation.invocation_id}: {retries_used} retry "
                f"records exceed policy max {self._policy.max_retries} without "
                f"a terminal RSR COMPLETE — corrupted attempt log, fail closed",
                schema_id="RR-01",
                record_id=invocation.invocation_id,
            )
        if retries_used > 0:
            # A prior retry run exists (initial already FAILED or retries
            # started) — this is a resume.  If the retry log is already
            # terminal (FAILED), replay it — do NOT re-execute.
            if rr and rr[-1].status is RetryRecordStatus.FAILED:
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=rr,
                    status=RetryRecordStatus.FAILED,
                    retried=True,
                    error=rr[-1].error,
                )
            if rr and rr[-1].status is RetryRecordStatus.SUCCEEDED:
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=rr,
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=True,
                    error=None,
                )

        last_rsr = rsr_records[-1] if rsr_records else None
        checkpoint_ref = last_rsr.checkpoint_ref if last_rsr else None
        preserved_outputs = list(last_rsr.output_ids or []) if last_rsr else []

        # -- Attempt loop ----------------------------------------------------
        next_retry = retries_used + 1  # RR-01 attempt numbering is retry-only

        # INITIAL execution (SI-01; NOT an RR-01) — only when no retries yet.
        if retries_used == 0:
            ctx = StageContext(
                execution=execution,
                checkpoint_ref=checkpoint_ref,
                previous_output_ids=preserved_outputs,
            )
            try:
                stage(ctx)
            except RetryableError as exc:
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.FAILED,
                    error=str(exc), retry_count=0,
                )
                # fall through to retry loop
            except Exception as exc:
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.FAILED,
                    error=f"{type(exc).__name__}: {exc}", retry_count=0,
                )
                raise
            else:
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.COMPLETE,
                    error=None, retry_count=0,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=[],
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=False,
                    error=None,
                )

        # RETRIES #1..max_retries (RR-01 attempts)
        for attempt_number in range(next_retry, self._policy.max_retries + 1):
            ctx = StageContext(
                execution=execution,
                checkpoint_ref=checkpoint_ref,
                previous_output_ids=preserved_outputs,
            )
            last = attempt_number == self._policy.max_retries
            try:
                stage(ctx)
            except RetryableError as exc:
                status = (
                    RetryRecordStatus.RETRYING
                    if not last
                    else RetryRecordStatus.FAILED  # FD #138: always FAILED
                )
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.FAILED,
                    error=str(exc), retry_count=attempt_number,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, status, error=str(exc),
                    manifest=manifest,
                )
                if last:
                    return RetryOutcome(
                        invocation_id=invocation.invocation_id,
                        attempt_records=self._rr_history(
                            invocation.invocation_id),
                        status=RetryRecordStatus.FAILED,
                        retried=True,
                        error=str(exc),
                    )
                continue
            except Exception as exc:
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    retry_count=attempt_number,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, RetryRecordStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    manifest=manifest,
                )
                raise
            else:
                self._write_rsr(
                    execution, ctx, ResearchStageRecordStage_state.COMPLETE,
                    error=None, retry_count=attempt_number,
                )
                self._write_attempt_and_manifest(
                    invocation, attempt_number, RetryRecordStatus.SUCCEEDED,
                    error=None, manifest=manifest,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._rr_history(
                        invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=attempt_number > 0,
                    error=None,
                )

        raise IntegrityConflict(  # pragma: no cover — logically unreachable
            f"RR-01/{invocation.invocation_id}: unexpected loop exit (fail closed)",
            schema_id="RR-01",
            record_id=invocation.invocation_id,
        )

    # -- internal: store reads (fail closed) --------------------------------

    def _rr_history(self, invocation_id: str) -> list[RetryRecord]:
        """Immutable retry log for an invocation, oldest first.

        Fail closed: an unreadable retry log is NEVER 'no retry history' —
        typed/deterministic store errors propagate and the caller must not
        execute the stage.
        """
        try:
            all_records = self._store.list_all("RR-01")
        except Exception as exc:  # noqa: BLE001 — propagate, never swallow
            raise type(exc)(
                f"RR-01 retry history unreadable — fail closed: {exc}"
            ) from exc
        attempts = [
            r for r in all_records if r.invocation_id == invocation_id
        ]
        attempts.sort(
            key=lambda r: int(r.attempt_number)
            if str(r.attempt_number).isdigit()
            else 0
        )
        return attempts

    def _rsr_history(
        self,
        case_id: str,
        stage_name: ResearchStageRecordStage_name,
    ) -> list[ResearchStageRecord]:
        """RSR-01 records for (case_id, stage_name), attempt order.

        Fail closed: an unreadable stage-state store means the kernel cannot
        establish the authoritative RSR state -> the stage MUST NOT execute.
        """
        try:
            all_records = self._stage_store.list_all("RSR-01")
        except Exception as exc:  # noqa: BLE001 — propagate, never swallow
            raise type(exc)(
                f"RSR-01 stage-state unreadable — cannot establish checkpoint "
                f"authority, fail closed: {exc}"
            ) from exc
        recs = [
            r for r in all_records
            if r.case_id == case_id and r.stage_name == stage_name
        ]
        recs.sort(key=lambda r: (r.started_at, r.stage_id))
        return recs

    # -- internal: store writes ---------------------------------------------

    def _write_rsr(
        self,
        execution: ExecutionContext,
        ctx: StageContext,
        stage_state: ResearchStageRecordStage_state,
        *,
        error: str | None,
        retry_count: int,
    ) -> str:
        """Write ONE immutable RSR-01 for this attempt (append-only lineage).

        output_ids = previously preserved outputs + outputs produced by THIS
        attempt (frozen revision rule: restart from last checkpoint preserves
        previous output).  checkpoint_ref = cp:<case_version>:<stage_id>.
        """
        stage_id = self._uuid()
        outputs = list(ctx.previous_output_ids) + list(ctx.produced_output_ids)
        rec = ResearchStageRecord(
            stage_id=stage_id,
            case_id=execution.case_id,
            stage_name=execution.stage_name,
            stage_state=stage_state,
            started_at=self._now(),
            completed_at=self._now(),
            responsible_role="S8",
            checkpoint_ref=_cp_encode(execution.case_version, stage_id),
            output_ids=outputs,
            retry_count=retry_count,
            failure_reason=error,
        )
        self._stage_store.store(rec)
        ctx.checkpoint_ref = rec.checkpoint_ref
        ctx.previous_output_ids = outputs
        return stage_id

    def _write_attempt_and_manifest(
        self,
        invocation: ServiceInvocation,
        attempt_number: int,
        status: RetryRecordStatus,
        *,
        error: str | None,
        manifest: RunManifestRecord,
    ) -> RetryRecord:
        """Commit the RR-01 and its RRM-01 provenance in ONE atomic batch.

        Both schemas belong to the same RunManifestStore authority (M5.2
        §12.2).  ``store_batch`` is the M5.2 §7.1 same-store atomic boundary:
        all records commit or none — no partial canonical state.  Terminal
        (FAILED) retries attach to ``failures``; scheduled retries attach to
        ``retries``; SUCCEEDED attaches nothing (the RETRYING refs already
        record the retry lineage).
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
        enriched = manifest
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
        self._store.store_batch([rec, enriched])
        return rec

    def _load_running_manifest(self, manifest_id: str) -> RunManifestRecord:
        """Load a RUNNING manifest or fail closed (missing / terminal).

        Called BEFORE any stage execution (FD #138 §7 preflight).
        """
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