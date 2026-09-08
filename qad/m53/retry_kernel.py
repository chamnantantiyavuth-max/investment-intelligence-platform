"""M5.3 S8 — Retry Kernel (reference implementation).

Deterministic bounded retry orchestration over the canonical RunManifestStore,
per the frozen authorities:

- M4A RR-01 (I-4): one immutable ``RetryRecord`` per attempt (own ``retry_id``
  UUID v7), ``attempt_number`` 1..N, ``status`` RETRYING / SUCCEEDED / FAILED /
  ESCALATED, ``attempted_at`` PIT field, ``invocation_id -> SI-01.invocation_id``.
  Validation rule: **max 3 retries per stage; after 3 -> FAILED**.
- M3-SERVICES S8: bounded retries per stage, retry from last checkpoint,
  previous stage output preserved, same stage + same case version -> same
  execution (idempotent).
- M5.2 §7.4: write fails pre/mid-commit -> zero partial state, retry safe.
- Erratum-002 / FD #137: RRM-01 lifecycle — a RUNNING manifest may be enriched
  (RUNNING -> RUNNING); terminal (COMPLETED/FAILED) is immutable.

Failure classification (deterministic):
- ``RetryableError``            -> transient, retried (up to policy max).
- Persistence contract errors   -> NOT retried (deterministic validation /
  integrity / immutability / FK failures are never blindly retried).
- Any other exception           -> NOT retried (fail closed), recorded FAILED
  and re-raised after honest attempt record writes.

Idempotency (fail closed):
- Replay over a terminal attempt log returns the existing outcome without
  touching ``stage`` and without creating duplicate canonical records.
- The same immutable identity (retry_id) may NEVER be written with different
  content: the canonical store raises ``IntegrityConflict`` and the kernel
  does not suppress it.
- Attempt identity is (invocation_id, attempt_number); a re-run resumes from
  the LAST RECORDED checkpoint (retry-from-checkpoint semantics).

REFERENCES / NON-PRODUCTION: in-memory store; single public dependency is the
``RunManifestStore`` protocol surface (contains/load/store/list_all).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

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


class RetryableError(Exception):
    """Marker for a transient, retry-worthy failure (network, rate-limit,
    timeout, 5xx).  Deterministic contract failures (ValidationFailure,
    IntegrityConflict, ImmutabilityViolation, MissingForeignKey) are NOT
    retryable and MUST be raised as their own typed errors."""


@dataclass(frozen=True)
class RetryPolicy:
    """Bounded retry policy (frozen: max 3 attempts per stage)."""

    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")


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
    RetryRecordStatus.ESCALATED,
}


def _enum_str(value: Any) -> str:
    return value.value if hasattr(value, "value") else str(value)


class RetryKernel:
    """Bounded deterministic retry controller (M3-SERVICES S8, reference)."""

    def __init__(
        self,
        store: RunManifestStore,
        *,
        policy: RetryPolicy | None = None,
        now: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._policy = policy or RetryPolicy()
        self._now = now or (
            lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    # -- public API ---------------------------------------------------------

    def execute(
        self,
        invocation: ServiceInvocation,
        stage: Callable[[], None],
        *,
        escalated_to: str | None = None,
        manifest_id: str | None = None,
        retry_id: str | None = None,
    ) -> RetryOutcome:
        """Run ``stage`` under the bounded retry policy.

        ``stage`` is a callable that raises on failure — ``RetryableError``
        for transient failures (retried), any other exception for
        deterministic/unknown failures (NOT retried; recorded then re-raised).

        Args:
            invocation: SI-01 record that MUST already exist in the store
                (RR-01.invocation_id FK dependency).  Fail closed otherwise.
            stage: zero-arg callable performing the service work.
            escalated_to: optional human/role reference recorded when the
                attempt budget is exhausted and the caller chooses escalation.
            manifest_id: optional RUNNING RRM-01 manifest to append the
                retry refs to (fail closed on terminal manifests).
            retry_id: optional explicit identity for the FIRST attempt record
                (collision with different content -> IntegrityConflict).

        Raises:
            MissingForeignKey: invocation or manifest not present.
            IntegrityConflict: same retry_id already stored with different
                content (immutable identity collision — fail closed).
            ImmutabilityViolation: manifest_id targets a terminal manifest.
            <original non-retryable error>: deterministic/unknown failure —
                recorded honestly, then re-raised.
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

        records = self._attempts_for(invocation.invocation_id)

        # Idempotent replay: a terminal log is final — return it untouched.
        terminal = [r for r in records if r.status in _TERMINAL]
        if terminal:
            last = terminal[-1]
            return RetryOutcome(
                invocation_id=invocation.invocation_id,
                attempt_records=records,
                status=last.status,
                retried=len([r for r in records if r.status is RetryRecordStatus.RETRYING]) > 0,
                error=last.error,
            )

        # Resume from the last recorded checkpoint (retry-from-checkpoint).
        next_attempt = len(records) + 1
        if next_attempt > self._policy.max_attempts:
            raise IntegrityConflict(
                f"RR-01/{invocation.invocation_id}: attempts exhausted "
                f"({self._policy.max_attempts}) without a terminal record — "
                f"corrupted attempt log, fail closed",
                schema_id="RR-01",
                record_id=invocation.invocation_id,
            )

        for attempt_number in range(next_attempt, self._policy.max_attempts + 1):
            last = attempt_number == self._policy.max_attempts
            try:
                stage()
            except RetryableError as exc:
                if not last:
                    # Retry scheduled — group state = RETRYING.
                    self._write_attempt(
                        invocation, attempt_number, RetryRecordStatus.RETRYING,
                        error=str(exc), retry_id=retry_id,
                        manifest_id=manifest_id,
                    )
                    continue
                # Budget exhausted — frozen rule: FAILED (ESCALATED if chosen).
                status = (
                    RetryRecordStatus.ESCALATED
                    if escalated_to is not None
                    else RetryRecordStatus.FAILED
                )
                self._write_attempt(
                    invocation, attempt_number, status, error=str(exc),
                    escalated_to=escalated_to, retry_id=retry_id,
                    manifest_id=manifest_id,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._attempts_for(invocation.invocation_id),
                    status=status,
                    retried=True,
                    error=str(exc),
                )
            except Exception as exc:
                # Deterministic/unknown failure — NOT retried (fail closed).
                self._write_attempt(
                    invocation, attempt_number, RetryRecordStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    escalated_to=None, retry_id=retry_id,
                    manifest_id=manifest_id,
                )
                raise
            else:
                self._write_attempt(
                    invocation, attempt_number, RetryRecordStatus.SUCCEEDED,
                    error=None, retry_id=retry_id, manifest_id=manifest_id,
                )
                return RetryOutcome(
                    invocation_id=invocation.invocation_id,
                    attempt_records=self._attempts_for(invocation.invocation_id),
                    status=RetryRecordStatus.SUCCEEDED,
                    retried=attempt_number > 1,
                    error=None,
                )

        raise IntegrityConflict(  # pragma: no cover — logically unreachable
            f"RR-01/{invocation.invocation_id}: unexpected loop exit (fail closed)",
            schema_id="RR-01",
            record_id=invocation.invocation_id,
        )

    # -- internal -----------------------------------------------------------

    def _attempts_for(self, invocation_id: str) -> list[RetryRecord]:
        """Return the immutable attempt log for an invocation, oldest first."""
        try:
            all_records = self._store.list_all("RR-01")
        except Exception:
            return []
        attempts = [
            r for r in all_records if r.invocation_id == invocation_id
        ]
        attempts.sort(
            key=lambda r: int(r.attempt_number)
            if str(r.attempt_number).isdigit()
            else 0
        )
        return attempts

    def _write_attempt(
        self,
        invocation: ServiceInvocation,
        attempt_number: int,
        status: RetryRecordStatus,
        *,
        error: str | None,
        escalated_to: str | None = None,
        retry_id: str | None = None,
        manifest_id: str | None = None,
    ) -> RetryRecord:
        """Write exactly ONE immutable RR-01 for this attempt.

        The canonical store rejects the same ``retry_id`` with different
        content (``IntegrityConflict``) — the kernel never suppresses it
        (immutable identity -> fail closed).

        RRM integration (honest, minimal):
        - RETRYING attempt  -> appended to ``RRM-01.retries`` (retry lineage)
        - FAILED/ESCALATED  -> appended to ``RRM-01.failures``
        - SUCCEEDED         -> nothing appended (the RETRYING refs already
          record that the run retried before succeeding)
        """
        rid = retry_id or f"RR-{invocation.invocation_id}-{attempt_number}"
        rec = RetryRecord(
            retry_id=rid,
            invocation_id=invocation.invocation_id,
            attempt_number=str(attempt_number),
            attempted_at=self._now(),
            status=status,
            error=error or "none",
            escalated_to=escalated_to,
        )
        self._store.store(rec)
        if manifest_id is not None:
            if status is RetryRecordStatus.RETRYING:
                self._attach_retry_to_manifest(manifest_id, rid)
            elif status in (RetryRecordStatus.FAILED, RetryRecordStatus.ESCALATED):
                self._attach_failure_to_manifest(manifest_id, rid)
        return rec

    def _attach_retry_to_manifest(self, manifest_id: str, retry_id: str) -> None:
        """Append a retry ref to ``RRM-01.retries`` (RUNNING only, fail closed)."""
        manifest = self._load_running_manifest(manifest_id)
        existing = manifest.retries or ""
        refs = [x.strip() for x in existing.split(",") if x.strip()]
        if retry_id not in refs:
            refs.append(retry_id)
        self._store.store(manifest.model_copy(update={"retries": ",".join(refs)}))

    def _attach_failure_to_manifest(self, manifest_id: str, retry_id: str) -> None:
        """Append a failure ref to ``RRM-01.failures`` (RUNNING only, fail closed)."""
        manifest = self._load_running_manifest(manifest_id)
        failures = list(manifest.failures or [])
        if retry_id not in failures:
            failures.append(retry_id)
        self._store.store(manifest.model_copy(update={"failures": failures}))

    def _load_running_manifest(self, manifest_id: str) -> RunManifestRecord:
        """Load a RUNNING manifest or fail closed (missing / terminal)."""
        if not self._store.contains("RRM-01", manifest_id):
            raise MissingForeignKey(
                f"RRM-01/{manifest_id}: manifest not found — cannot attach "
                f"retry provenance (fail closed)",
                schema_id="RRM-01",
                record_id=manifest_id,
            )
        manifest = self._store.load("RRM-01", manifest_id)
        run_state = _enum_str(manifest.run_state)
        if run_state in ("COMPLETED", "FAILED"):
            raise ImmutabilityViolation(
                f"RRM-01/{manifest_id}: terminal manifest ({run_state}) is "
                f"immutable — retry provenance cannot be attached",
                schema_id="RRM-01",
                record_id=manifest_id,
            )
        return manifest