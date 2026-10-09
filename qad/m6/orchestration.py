"""QAD M6.5 — Retry / Telemetry / Idempotency (FD #148 §1/§3, FD #151 M6 sequence).

A DETERMINISTIC orchestration layer over the already-accepted M6.3 Run Ledger
(:mod:`qad.m6.ledger`) and the M6.4 request/result contract
(:mod:`qad.m6.research_contract`). It implements ONLY:

* **idempotency** — one canonical logical-request identity, one logical run;
* **retry policy** — Mode A / Mode B, bounded to THREE attempts, truthful labels;
* **attempt accounting** — retry identity ``(idempotency_key, attempt_number)``;
* **truthful telemetry** — ``EXPOSED`` records the exact value, ``NOT_EXPOSED``
  records ``null`` + a reason; unknown is never encoded as zero.

Scope boundary (FD #151): this module is **NOT a provider adapter**. It performs no
provider execution — no Gemini, no Notebook, no browser/CDP, no network, no
credentials, no live calls. Provider execution is M6.7/M6.8. Everything here is
NON-CANONICAL: it adds no canonical schema (the registry stays at 68) and never
promotes anything to canonical evidence.

Authority:
* FD #148 §1 (R-1) — reconciled S10 retry semantics, Mode A / Mode B;
* FD #148 §3 (R-4) — idempotency key + retry identity + result hash;
* M6.0 design §1/§2/§3/§7/§8 — retry, telemetry truthfulness, ledger, failure states.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from qad.models.family_b import EvidenceGapOperational_status

from qad.m6.ledger import (
    ATTEMPT_NUMBER_MAX,
    ATTEMPT_NUMBER_MIN,
    CONTRACT_TELEMETRY_METRICS,
    REQUIRED_TELEMETRY_METRICS,
    DeepResearchRunLedgerStore,
    LedgerIdentityConflict,
    RetryMode,
    RunRecord,
    TelemetryStatus,
    TerminalStatus,
)
from qad.m6.research_contract import (
    S10_CAPABILITY,
    DeepResearchRequest,
    DeepResearchResult,
)

__all__ = [
    "DEEP_RESEARCH_STAGE",
    "MAX_ATTEMPTS",
    "TELEMETRY_NOT_EXPOSED_REASON",
    "NOT_EXPOSED_BY_PROVIDER",
    "IDEMPOTENCY_FIELDS",
    "OrchestrationError",
    "IdempotencyError",
    "RetryPolicyError",
    "compute_idempotency_key",
    "idempotency_key_for_request",
    "ResolutionOutcome",
    "LogicalRunResolution",
    "resolve_or_create_logical_run",
    "OrchestrationMode",
    "ProviderSet",
    "AttemptPlan",
    "plan_attempt",
    "validate_attempt_plan",
    "AttemptClassification",
    "classify_attempt_outcome",
    "classify_result_status",
    "EvidenceGapTransitionInstruction",
    "RetryDecision",
    "decide_retry",
    "build_telemetry",
    "exposed",
    "not_exposed",
    "not_exposed_telemetry",
    "record_failed_attempt",
    "accept_success_result",
    "terminalize_research_unavailable",
]


# ---------------------------------------------------------------------------
# Bounded constants
# ---------------------------------------------------------------------------

#: M6.0 §3 retry identity — MAXIMUM THREE attempts TOTAL (attempt 4 is impossible).
MAX_ATTEMPTS: int = ATTEMPT_NUMBER_MAX

#: The M6 pipeline stage identity used by the idempotency formula. The Deep
#: Research stage is S10 (FD #148 S10 amendment), so the default is the existing
#: S10 capability identity — no competing stage vocabulary is introduced.
DEEP_RESEARCH_STAGE: str = S10_CAPABILITY

#: The idempotency formula's exact field set, in canonical serialization order
#: (M6.0 §3): ``hash(case_id, case_version, stage, evidence_gap_id,
#: request_payload_hash, input_snapshot_hash)``.
IDEMPOTENCY_FIELDS: tuple[str, ...] = (
    "case_id",
    "case_version",
    "stage",
    "evidence_gap_id",
    "request_payload_hash",
    "input_snapshot_hash",
)

#: Truthful-unavailability reason used when a provider does not expose a metric
#: (M6.0 §2). Never an estimate, never a zero.
TELEMETRY_NOT_EXPOSED_REASON: str = (
    "provider surface does not expose this metric (M6.0 §2 truthful unavailability)"
)

#: Authorized RRM-01 sentinel for an unexposed model identity (M6.0 §2).
NOT_EXPOSED_BY_PROVIDER: str = "NOT_EXPOSED_BY_PROVIDER"

#: Attempt outcomes the authority treats as TRANSIENT (retryable): M6.0 §8 defines
#: ``RESEARCH_UNAVAILABLE`` as "retries exhausted / provider unreachable" and
#: ``TRANSPORT_FAILURE`` as a transport error / navigation ambiguity / UI drift —
#: the classes a bounded retry exists to absorb (§1 Mode B).
RETRYABLE_ATTEMPT_OUTCOMES: frozenset[TerminalStatus] = frozenset(
    {TerminalStatus.TRANSPORT_FAILURE, TerminalStatus.RESEARCH_UNAVAILABLE}
)

#: FAIL-CLOSED attempt outcomes. Retrying these merely because retry capacity
#: exists is forbidden (brief §6): a SEALED PIT defect cannot be repaired by a
#: retry (M6.0 §8 PIT_BLOCK), a budget exhaustion is terminal (M6.0 §8
#: INCOMPLETE), SUCCESS is already terminal, and ``FAILED`` is the conservative
#: fail-closed bucket for anything not positively classified as retryable.
NON_RETRYABLE_ATTEMPT_OUTCOMES: frozenset[TerminalStatus] = frozenset(
    {
        TerminalStatus.SUCCESS,
        TerminalStatus.PIT_BLOCK,
        TerminalStatus.INCOMPLETE,
        TerminalStatus.FAILED,
    }
)

#: M6.4 result statuses that are CONTRACTUALLY FAIL-CLOSED. They must never be
#: retried and never re-labelled (FD #152 / M6.4 §6-§7).
FAIL_CLOSED_RESULT_STATUSES: frozenset[str] = frozenset(
    {"PROVIDER_CANNOT_ENFORCE_SEALED_INPUT", "REQUEST_ISOLATION_UNVERIFIED"}
)

#: M6.4 result statuses that are transient and therefore retryable.
RETRYABLE_RESULT_STATUSES: frozenset[str] = frozenset(
    {"TRANSPORT_FAILURE", "RESEARCH_UNAVAILABLE"}
)


class OrchestrationError(Exception):
    """Base error for the M6.5 deterministic orchestration layer."""


class IdempotencyError(OrchestrationError):
    """A logical-request identity could not be computed or resolved."""


class RetryPolicyError(OrchestrationError):
    """An attempt violates the bounded M6 retry policy."""


# ---------------------------------------------------------------------------
# 1. Idempotency — one canonical logical-request identity (M6.0 §3)
# ---------------------------------------------------------------------------

def _canonical_identity_payload(pairs: tuple[tuple[str, str], ...]) -> bytes:
    """Length-prefixed, order-fixed serialization (deterministic + injective).

    Length-prefixing makes the encoding unambiguous even if a field value contains
    the separator, so distinct inputs can never collide by construction. It uses no
    clock, no UUID/random identity, no process/object identity, no filesystem path,
    no notebook identity, no attempt number and no provider surface.
    """
    parts: list[bytes] = []
    for name, value in pairs:
        raw = value.encode("utf-8")
        parts.append(f"{name}:{len(raw)}:".encode("ascii") + raw)
    return b"\n".join(parts)


def compute_idempotency_key(
    *,
    case_id: str,
    case_version: str,
    evidence_gap_id: str,
    request_payload_hash: str,
    input_snapshot_hash: str,
    stage: str = DEEP_RESEARCH_STAGE,
) -> str:
    """Deterministic canonical idempotency key (M6.0 §3 / FD #148 §3).

    ``hash(case_id, case_version, stage, evidence_gap_id, request_payload_hash,
    input_snapshot_hash)`` — a repeat request with the SAME key is the SAME logical
    request and never a silent second run.
    """
    values = {
        "case_id": case_id,
        "case_version": case_version,
        "stage": stage,
        "evidence_gap_id": evidence_gap_id,
        "request_payload_hash": request_payload_hash,
        "input_snapshot_hash": input_snapshot_hash,
    }
    pairs: list[tuple[str, str]] = []
    for name in IDEMPOTENCY_FIELDS:
        value = values[name]
        if not isinstance(value, str) or not value.strip():
            raise IdempotencyError(
                f"idempotency identity requires a non-blank {name}"
            )
        pairs.append((name, value))
    digest = hashlib.sha256(_canonical_identity_payload(tuple(pairs))).hexdigest()
    return f"idem-{digest}"


def idempotency_key_for_request(
    request: DeepResearchRequest, *, stage: str = DEEP_RESEARCH_STAGE
) -> str:
    """Canonical idempotency key for an M6.4 request (identity taken FROM it)."""
    if not isinstance(request, DeepResearchRequest):
        raise IdempotencyError(
            "idempotency_key_for_request requires a DeepResearchRequest"
        )
    return compute_idempotency_key(
        case_id=request.case_id,
        case_version=request.case_version,
        evidence_gap_id=request.evidence_gap_id,
        request_payload_hash=request.request_payload_hash,
        input_snapshot_hash=request.input_snapshot_hash,
        stage=stage,
    )


class ResolutionOutcome(str, Enum):
    """What resolving an idempotency key produced."""

    CREATED = "CREATED"
    EXISTING_ACTIVE = "EXISTING_ACTIVE"
    EXISTING_TERMINAL = "EXISTING_TERMINAL"


@dataclass(frozen=True)
class LogicalRunResolution:
    """The resolved logical run for an idempotency key (never a duplicate)."""

    outcome: ResolutionOutcome
    idempotency_key: str
    ledger_id: str
    attempts_recorded: int
    next_attempt_number: int | None
    retry_budget_remaining: int
    history_consistent: bool = True
    unfinalized_success: bool = False
    terminal_status: TerminalStatus | None = None
    record: RunRecord | None = field(default=None, repr=False, compare=False)

    @property
    def is_terminal(self) -> bool:
        return self.terminal_status is not None

    @property
    def may_attempt(self) -> bool:
        """True only when a further attempt is permitted by the durable budget."""
        return self.next_attempt_number is not None


def _last_attempt_blocks_retry(record: RunRecord) -> bool:
    """True when the recorded history forbids another attempt (fail closed).

    Two cases block: a persisted SUCCESS attempt (a successful attempt is never
    retried — round-2 finding 4), and a previous attempt whose outcome is not
    RETRYABLE (round-2 finding 3).
    """
    outcomes = [a.outcome for a in record.attempts]
    if any(o == TerminalStatus.SUCCESS.value for o in outcomes):
        return True
    if not outcomes:
        return False
    try:
        return classify_attempt_outcome(outcomes[-1]) is not AttemptClassification.RETRYABLE
    except OrchestrationError:
        return True


def _resolution_from_record(
    outcome: ResolutionOutcome, key: str, record: RunRecord
) -> LogicalRunResolution:
    used = [a.attempt_number for a in record.attempts]
    # The durable attempt history must be the contiguous sequence 1..N (M6.5 §13
    # criterion 34). A gapped history is treated FAIL-CLOSED: no further attempt is
    # permitted, so the resolution can never report a self-contradictory pair such
    # as "no next attempt but two attempts remaining".
    consistent = used == list(range(1, len(used) + 1))
    blocked = _last_attempt_blocks_retry(record)
    next_attempt: int | None
    if record.is_terminal or not consistent or blocked:
        next_attempt = None
    else:
        candidate = len(used) + 1
        next_attempt = candidate if candidate <= MAX_ATTEMPTS else None
    remaining = 0 if next_attempt is None else (MAX_ATTEMPTS - next_attempt + 1)
    return LogicalRunResolution(
        outcome=outcome,
        idempotency_key=key,
        ledger_id=record.ledger_id,
        attempts_recorded=len(used),
        next_attempt_number=next_attempt,
        retry_budget_remaining=remaining,
        history_consistent=consistent,
        unfinalized_success=(
            not record.is_terminal
            and any(a.outcome == TerminalStatus.SUCCESS.value for a in record.attempts)
        ),
        terminal_status=record.terminal_status,
        record=record,
    )


def _classify_or_fail_closed(outcome: Any) -> AttemptClassification:
    """Classification helper: an unknown/absent outcome is fail-closed."""
    try:
        return classify_attempt_outcome(outcome)
    except OrchestrationError:
        return AttemptClassification.NON_RETRYABLE


def _require_all_attempts_retryable(
    record: RunRecord, *, before_number: int | None = None
) -> None:
    """EVERY recorded attempt must be RETRYABLE (M6.5 lifecycle discipline).

    A later retryable outcome must never mask an earlier fail-closed attempt: M6.5
    enforces this on its OWN boundaries (recording, SUCCESS acceptance, exhaustion and
    recovery), independent of what the accepted M6.3 ledger alone permits. The optional
    ``before_number`` restricts the check to attempts preceding a given attempt number
    (used by recovery, whose history legitimately ends in a SUCCESS attempt).
    """
    for attempt in record.attempts:
        if before_number is not None and attempt.attempt_number >= before_number:
            continue
        classification = _classify_or_fail_closed(attempt.outcome)
        if classification is not AttemptClassification.RETRYABLE:
            raise RetryPolicyError(
                f"attempt {attempt.attempt_number} outcome {attempt.outcome!r} is "
                f"{classification.value}; every preceding attempt must be retryable "
                "before M6.5 proceeds (a later retryable outcome cannot mask an earlier "
                "fail-closed attempt)"
            )


def _next_attempt_guard(
    store: DeepResearchRunLedgerStore, ledger_id: str
) -> tuple[RunRecord, int]:
    """The M6.5 recording boundary gate.

    M6.3's ledger deliberately validates only the 1..3 RANGE and duplicate identity;
    lifecycle ORDERING and outcome discipline are owned here by the orchestrator, so
    this does not change the accepted M6.3 ledger semantics. Refused: a terminal run,
    a non-contiguous history, an exhausted budget, a persisted SUCCESS attempt, and a
    retry after a fail-closed (non-retryable) outcome.
    """
    record = store.load_run(ledger_id)
    if record.is_terminal:
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} is already terminal; no further attempt "
            "may be recorded"
        )
    used = [a.attempt_number for a in record.attempts]
    if used != list(range(1, len(used) + 1)):
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} has a non-contiguous attempt history "
            f"{used}; M6.5 requires the contiguous sequence 1..N"
        )
    outcomes = [a.outcome for a in record.attempts]
    if any(o == TerminalStatus.SUCCESS.value for o in outcomes):
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} already has a persisted SUCCESS attempt; a "
            "successful attempt is never retried — finalize it through "
            "accept_success_result (recovery path)"
        )
    _require_all_attempts_retryable(record)
    expected = len(used) + 1
    if expected > MAX_ATTEMPTS:
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} has exhausted the {MAX_ATTEMPTS}-attempt budget"
        )
    return record, expected


def _require_result_run_binding(record: RunRecord, result: DeepResearchResult) -> None:
    """Bind an accepted SUCCESS result to the TARGET ledger run (FD #152 §4/§7).

    M6.4 binds a verified proof to the exact run, so M6.5 must refuse a result whose
    identity belongs to a DIFFERENT logical run — otherwise a proof-verified result
    produced for run A could terminalize run B as SUCCESS (round-3 reviewer finding).
    """
    for name, got, bound in (
        ("request_id", result.request_id, record.request_id),
        ("research_run_id", result.research_run_id, record.research_run_id),
        ("ledger_id", result.ledger_id, record.ledger_id),
        ("input_snapshot_hash", result.input_snapshot_hash, record.input_snapshot_hash),
    ):
        if got != bound:
            raise RetryPolicyError(
                f"SUCCESS refused: the result's {name} {got!r} is not bound to the "
                f"target ledger run {record.ledger_id!r} ({name}={bound!r})"
            )


def _validate_plan_against_record(
    record: RunRecord,
    plan: AttemptPlan,
    provider_set: ProviderSet,
    expected: int,
) -> None:
    """Validate the plan against BOTH the policy and the previous durable attempt."""
    validate_attempt_plan(plan, provider_set)
    if plan.attempt_number != expected:
        raise RetryPolicyError(
            "attempt history must be the contiguous sequence 1..N: expected attempt "
            f"{expected} for ledger run {record.ledger_id!r}, got {plan.attempt_number}"
        )
    if not record.attempts:
        # Attempt 1 must use the deterministic default AND agree with the ledger run's
        # own configured provider surface — otherwise the durable run and its attempt
        # history would disagree about the provider (round-4 reviewer finding).
        if plan.provider_surface != record.provider_surface:
            raise RetryPolicyError(
                "the initial attempt provider must equal the ledger run's configured "
                f"provider surface {record.provider_surface!r}, got "
                f"{plan.provider_surface!r}"
            )
        return
    previous = record.attempts[-1].provider_surface
    # The plan must be the DETERMINISTIC plan for this run — a caller cannot bypass the
    # planner by supplying a different (but individually well-formed) plan.
    expected_plan = plan_attempt(
        provider_set=provider_set,
        attempt_number=expected,
        previous_provider_surface=previous,
    )
    if plan != expected_plan:
        raise RetryPolicyError(
            "the attempt plan must be the deterministic plan for this run "
            f"({expected_plan!r}), got {plan!r}"
        )
    if provider_set.mode is OrchestrationMode.MODE_B:
        if plan.provider_surface != previous:
            raise RetryPolicyError(
                "a Mode B retry must stay on the same provider "
                f"({previous!r}), got {plan.provider_surface!r}"
            )
        return
    if plan.provider_changed:
        if plan.provider_surface == previous:
            raise RetryPolicyError(
                "PROVIDER_FALLBACK requires the provider to ACTUALLY change"
            )
    elif plan.provider_surface != previous:
        raise RetryPolicyError(
            "a SAME_PROVIDER_RETRY must keep the previous provider "
            f"({previous!r}), got {plan.provider_surface!r}"
        )


def resolve_or_create_logical_run(
    store: DeepResearchRunLedgerStore,
    *,
    idempotency_key: str,
    create_run_kwargs: Mapping[str, Any] | None = None,
) -> LogicalRunResolution:
    """Resolve the logical run for ``idempotency_key``, creating it only once.

    * an existing ACTIVE logical run is REUSED — never a second logical run, and
      the durable attempt budget is NEVER reset;
    * an existing TERMINAL logical run resolves its terminal state and is never
      silently re-executed;
    * a concurrent/racing duplicate creation is reconciled by RE-READING the
      existing logical run (the M6.3 UNIQUE constraint is preserved, never
      weakened).
    """
    if not isinstance(store, DeepResearchRunLedgerStore):
        raise IdempotencyError("resolve_or_create_logical_run requires a ledger store")
    existing = store.load_run_by_idempotency_key(idempotency_key)
    if existing is not None:
        return _resolution_from_record(
            ResolutionOutcome.EXISTING_TERMINAL
            if existing.is_terminal
            else ResolutionOutcome.EXISTING_ACTIVE,
            idempotency_key,
            existing,
        )

    if create_run_kwargs is None:
        raise IdempotencyError(
            f"no logical run exists for idempotency_key {idempotency_key!r} and no "
            "create_run_kwargs were supplied"
        )
    kwargs = dict(create_run_kwargs)
    supplied = kwargs.get("idempotency_key")
    if supplied != idempotency_key:
        raise IdempotencyError(
            "create_run_kwargs.idempotency_key must equal the resolved idempotency_key "
            f"({supplied!r} != {idempotency_key!r})"
        )
    try:
        ledger_id = store.create_run(**kwargs)
    except LedgerIdentityConflict:
        # A racing duplicate create lost the race: reconcile by re-reading the
        # existing logical run instead of reporting a second logical run.
        raced = store.load_run_by_idempotency_key(idempotency_key)
        if raced is None:
            raise
        return _resolution_from_record(
            ResolutionOutcome.EXISTING_TERMINAL
            if raced.is_terminal
            else ResolutionOutcome.EXISTING_ACTIVE,
            idempotency_key,
            raced,
        )
    record = store.load_run(ledger_id)
    return _resolution_from_record(ResolutionOutcome.CREATED, idempotency_key, record)


# ---------------------------------------------------------------------------
# 2. Provider set + retry policy (M6.0 §1 Mode A / Mode B)
# ---------------------------------------------------------------------------

class OrchestrationMode(str, Enum):
    """FD #148 §1 reconciled S10 retry modes."""

    MODE_A = "MODE_A"  # >= 2 compliant providers -> different-provider retry allowed
    MODE_B = "MODE_B"  # exactly 1 compliant provider -> SAME-PROVIDER retry only


@dataclass(frozen=True)
class ProviderSet:
    """The EXPLICIT configured compliant provider set (never inferred).

    Only providers named here may ever be used. A single-provider configuration can
    never masquerade as Mode A, and Mode A never invents a second provider.
    """

    compliant_providers: tuple[str, ...]

    def __post_init__(self) -> None:
        raw = self.compliant_providers
        if isinstance(raw, (str, bytes)):
            raise RetryPolicyError(
                "compliant_providers must be a COLLECTION of provider names, not a "
                "single string — a string would be iterated into characters and "
                "silently invent provider surfaces (and could fake Mode A)"
            )
        try:
            providers = tuple(raw)
        except TypeError:
            raise RetryPolicyError(
                "compliant_providers must be an iterable of provider names"
            ) from None
        if not providers:
            raise RetryPolicyError("at least one compliant provider is required")
        for name in providers:
            if not isinstance(name, str) or not name.strip():
                raise RetryPolicyError("provider names must be non-blank strings")
        if len(set(providers)) != len(providers):
            raise RetryPolicyError("compliant provider names must be unique")
        object.__setattr__(self, "compliant_providers", tuple(sorted(providers)))

    @property
    def mode(self) -> OrchestrationMode:
        return (
            OrchestrationMode.MODE_A
            if len(self.compliant_providers) >= 2
            else OrchestrationMode.MODE_B
        )

    @property
    def default_provider(self) -> str:
        """Deterministic first provider (sorted set) — never inferred."""
        return self.compliant_providers[0]

    def provider_for_index(self, index: int) -> str:
        """Deterministic round-robin over the explicit set."""
        return self.compliant_providers[index % len(self.compliant_providers)]


@dataclass(frozen=True)
class AttemptPlan:
    """The truthful plan for ONE attempt (retry identity + provider + label)."""

    attempt_number: int
    retry_mode: RetryMode
    provider_surface: str
    fallback_used: bool
    provider_changed: bool

    @property
    def is_initial_attempt(self) -> bool:
        return self.retry_mode is RetryMode.INITIAL_ATTEMPT


def plan_attempt(
    *,
    provider_set: ProviderSet,
    attempt_number: int,
    previous_provider_surface: str | None = None,
) -> AttemptPlan:
    """Plan attempt ``attempt_number`` under the bounded M6 retry policy.

    * attempt 1 -> ``INITIAL_ATTEMPT`` on the deterministic default provider;
    * Mode B (one compliant provider) -> attempts 2..3 are
      ``SAME_PROVIDER_RETRY`` on the SAME provider, and can never be labelled
      provider fallback (``fallback_used`` stays False);
    * Mode A (>= 2 compliant providers) -> a retry may use a DIFFERENT compliant
      provider; the change is labelled ``PROVIDER_FALLBACK`` with
      ``fallback_used = True``, and only ever selects a provider from the explicit
      configured set;
    * attempt 4 is IMPOSSIBLE and is refused.
    """
    if not isinstance(provider_set, ProviderSet):
        raise RetryPolicyError("plan_attempt requires a ProviderSet")
    if (
        not isinstance(attempt_number, int)
        or isinstance(attempt_number, bool)
        or not (ATTEMPT_NUMBER_MIN <= attempt_number <= MAX_ATTEMPTS)
    ):
        raise RetryPolicyError(
            f"attempt_number must be an integer in {ATTEMPT_NUMBER_MIN}.."
            f"{MAX_ATTEMPTS}; attempt {attempt_number!r} is impossible in M6"
        )

    if attempt_number == ATTEMPT_NUMBER_MIN:
        if previous_provider_surface is not None:
            raise RetryPolicyError(
                "the initial attempt has no previous provider to retry from"
            )
        return AttemptPlan(
            attempt_number=attempt_number,
            retry_mode=RetryMode.INITIAL_ATTEMPT,
            provider_surface=provider_set.default_provider,
            fallback_used=False,
            provider_changed=False,
        )

    if previous_provider_surface is None:
        raise RetryPolicyError(
            f"attempt {attempt_number} is a retry and requires the previous "
            "provider surface"
        )
    if previous_provider_surface not in provider_set.compliant_providers:
        raise RetryPolicyError(
            f"previous provider {previous_provider_surface!r} is not in the explicit "
            "compliant provider set"
        )

    if provider_set.mode is OrchestrationMode.MODE_B:
        # Exactly one compliant provider: same-provider retry ONLY. Never fallback.
        return AttemptPlan(
            attempt_number=attempt_number,
            retry_mode=RetryMode.SAME_PROVIDER_RETRY,
            provider_surface=provider_set.default_provider,
            fallback_used=False,
            provider_changed=False,
        )

    # Mode A: deterministic selection from the explicit set. The provider changes
    # when the round-robin index moves off the current provider — never fabricated.
    current_index = provider_set.compliant_providers.index(previous_provider_surface)
    selected = provider_set.provider_for_index(current_index + 1)
    changed = selected != previous_provider_surface
    return AttemptPlan(
        attempt_number=attempt_number,
        retry_mode=RetryMode.PROVIDER_FALLBACK if changed else RetryMode.SAME_PROVIDER_RETRY,
        provider_surface=selected,
        fallback_used=changed,
        provider_changed=changed,
    )


# ---------------------------------------------------------------------------
# 3. Failure classification + bounded retry decision (M6.0 §8)
# ---------------------------------------------------------------------------

def validate_attempt_plan(plan: AttemptPlan, provider_set: ProviderSet) -> AttemptPlan:
    """Validate an attempt plan's TRUTHFULNESS before it is durably recorded.

    Recording a caller-supplied label is not enough (round-2 reviewer finding): the
    label, the provider membership and the fallback flag must all be mechanically
    consistent with the committed Mode A / Mode B policy, otherwise a durable record
    could claim a provider fallback that never happened or name a provider outside
    the explicit configured set.
    """
    if not isinstance(plan, AttemptPlan):
        raise RetryPolicyError("validate_attempt_plan requires an AttemptPlan")
    if not isinstance(provider_set, ProviderSet):
        raise RetryPolicyError("validate_attempt_plan requires a ProviderSet")
    if (
        not isinstance(plan.attempt_number, int)
        or isinstance(plan.attempt_number, bool)
        or not (ATTEMPT_NUMBER_MIN <= plan.attempt_number <= MAX_ATTEMPTS)
    ):
        raise RetryPolicyError(
            f"attempt_number must be an integer in {ATTEMPT_NUMBER_MIN}.."
            f"{MAX_ATTEMPTS}, got {plan.attempt_number!r}"
        )
    if plan.provider_surface not in provider_set.compliant_providers:
        raise RetryPolicyError(
            f"attempt provider {plan.provider_surface!r} is not in the explicit "
            f"compliant provider set {provider_set.compliant_providers!r}"
        )
    truthful = (
        plan.fallback_used
        == plan.provider_changed
        == (plan.retry_mode is RetryMode.PROVIDER_FALLBACK)
    )
    if not truthful:
        raise RetryPolicyError(
            "attempt labels must be truthful: fallback_used, provider_changed and "
            "PROVIDER_FALLBACK must agree"
        )
    if plan.attempt_number == ATTEMPT_NUMBER_MIN:
        if (
            plan.retry_mode is not RetryMode.INITIAL_ATTEMPT
            or plan.fallback_used
            or plan.provider_changed
        ):
            raise RetryPolicyError(
                "the initial attempt must be INITIAL_ATTEMPT with no fallback"
            )
        if plan.provider_surface != provider_set.default_provider:
            raise RetryPolicyError(
                "the initial attempt must use the deterministic default provider"
            )
        return plan
    if plan.retry_mode is RetryMode.INITIAL_ATTEMPT:
        raise RetryPolicyError("only attempt 1 may be INITIAL_ATTEMPT")
    if provider_set.mode is OrchestrationMode.MODE_B:
        if plan.retry_mode is not RetryMode.SAME_PROVIDER_RETRY:
            raise RetryPolicyError(
                "a one-provider (Mode B) run may only SAME_PROVIDER_RETRY — it can "
                "never be labelled a provider fallback"
            )
        if plan.provider_surface != provider_set.default_provider:
            raise RetryPolicyError(
                "a Mode B retry must stay on the same (only) compliant provider"
            )
    return plan


class AttemptClassification(str, Enum):
    """Whether a terminal attempt outcome may be retried."""

    SUCCESS = "SUCCESS"
    RETRYABLE = "RETRYABLE"
    NON_RETRYABLE = "NON_RETRYABLE"


def classify_attempt_outcome(outcome: str | TerminalStatus) -> AttemptClassification:
    """Mechanically classify a durable attempt outcome (fail-closed default).

    Authority: M6.0 §8. ``TRANSPORT_FAILURE`` / ``RESEARCH_UNAVAILABLE`` are the
    transient classes a bounded retry exists to absorb; ``PIT_BLOCK`` and
    ``INCOMPLETE`` are fail-closed; ``SUCCESS`` is terminal. Anything unclassified
    falls to NON_RETRYABLE — retry is never granted by default.
    """
    try:
        status = TerminalStatus(outcome)
    except ValueError:
        raise OrchestrationError(f"unknown attempt outcome {outcome!r}") from None
    if status is TerminalStatus.SUCCESS:
        return AttemptClassification.SUCCESS
    if status in RETRYABLE_ATTEMPT_OUTCOMES:
        return AttemptClassification.RETRYABLE
    return AttemptClassification.NON_RETRYABLE


def classify_result_status(status: str) -> AttemptClassification:
    """Classify an M6.4 result status, honouring the FAIL-CLOSED contract.

    ``PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`` and ``REQUEST_ISOLATION_UNVERIFIED``
    are contractually fail-closed (FD #152 §6/§7) and are NEVER retried, even when
    retry budget remains.
    """
    value = str(status)
    if value == "SUCCESS":
        return AttemptClassification.SUCCESS
    if value in FAIL_CLOSED_RESULT_STATUSES:
        return AttemptClassification.NON_RETRYABLE
    if value in RETRYABLE_RESULT_STATUSES:
        return AttemptClassification.RETRYABLE
    return AttemptClassification.NON_RETRYABLE


@dataclass(frozen=True)
class EvidenceGapTransitionInstruction:
    """A deterministic EG-01 transition INSTRUCTION — never a write.

    FD #148 §1 / M6.0 §8: retry exhaustion leaves the run
    ``RESEARCH_UNAVAILABLE`` and the linked Evidence Gap in the appropriate
    unresolved state (``DEFERRED``). No canonical EG-01 mutation service exists yet,
    so M6.5 does NOT invent a canonical write API: it emits this instruction and the
    gap stays preserved/unresolved.
    """

    evidence_gap_id: str
    from_status: str
    to_status: str
    reason: str
    schema_id: str = "EG-01"
    authority_ref: str = "FD #148 §1 / M6.0 §8"
    applied: bool = False


@dataclass(frozen=True)
class RetryDecision:
    """The bounded, truthful decision for the attempt that just failed."""

    classification: AttemptClassification
    attempt_number: int
    should_retry: bool
    next_attempt: AttemptPlan | None = None
    terminal_status: TerminalStatus | None = None
    evidence_gap_instruction: EvidenceGapTransitionInstruction | None = None
    evidence_gates_weakened: bool = False

    def __post_init__(self) -> None:
        if self.evidence_gates_weakened:
            raise RetryPolicyError("M6 retry never weakens evidence/quality gates")
        if self.should_retry and self.next_attempt is None:
            raise RetryPolicyError("a retry decision must carry the next attempt plan")
        if self.should_retry and self.terminal_status is not None:
            raise RetryPolicyError("a retry decision cannot also be terminal")
        if not self.should_retry and self.terminal_status is None:
            raise RetryPolicyError(
                "a non-retry decision must resolve a terminal status"
            )


def decide_retry(
    *,
    provider_set: ProviderSet,
    attempt_number: int,
    outcome: str | TerminalStatus,
    previous_provider_surface: str | None,
    evidence_gap_id: str,
    gap_from_status: str = EvidenceGapOperational_status.OPEN.value,
) -> RetryDecision:
    """Decide the next step for the attempt that just failed.

    Fail-closed: a non-retryable / fail-closed outcome is NEVER retried merely
    because budget remains. A retryable failure retries only while the durable
    3-attempt budget allows; exhaustion ends ``RESEARCH_UNAVAILABLE`` and emits the
    EG-01 ``DEFERRED`` instruction without weakening any gate.
    """
    if (
        not isinstance(attempt_number, int)
        or isinstance(attempt_number, bool)
        or not (ATTEMPT_NUMBER_MIN <= attempt_number <= MAX_ATTEMPTS)
    ):
        raise RetryPolicyError(
            "attempt_number must be an integer in "
            f"{ATTEMPT_NUMBER_MIN}..{MAX_ATTEMPTS} (retry identity is "
            f"(idempotency_key, attempt_number)); got {attempt_number!r}"
        )
    classification = classify_attempt_outcome(outcome)

    if classification is AttemptClassification.SUCCESS:
        raise RetryPolicyError(
            "decide_retry applies to a failed attempt; a SUCCESS result must be "
            "accepted through accept_success_result (FD #152 proof gate)"
        )

    if classification is AttemptClassification.NON_RETRYABLE:
        return RetryDecision(
            classification=classification,
            attempt_number=attempt_number,
            should_retry=False,
            terminal_status=TerminalStatus(outcome),
            evidence_gap_instruction=None,
        )

    if attempt_number >= MAX_ATTEMPTS:
        return RetryDecision(
            classification=classification,
            attempt_number=attempt_number,
            should_retry=False,
            terminal_status=TerminalStatus.RESEARCH_UNAVAILABLE,
            evidence_gap_instruction=EvidenceGapTransitionInstruction(
                evidence_gap_id=evidence_gap_id,
                from_status=gap_from_status,
                to_status=EvidenceGapOperational_status.DEFERRED.value,
                reason=(
                    "Deep Research retries exhausted "
                    f"({MAX_ATTEMPTS} attempts); run terminated RESEARCH_UNAVAILABLE"
                ),
            ),
        )

    return RetryDecision(
        classification=classification,
        attempt_number=attempt_number,
        should_retry=True,
        next_attempt=plan_attempt(
            provider_set=provider_set,
            attempt_number=attempt_number + 1,
            previous_provider_surface=previous_provider_surface,
        ),
    )


# ---------------------------------------------------------------------------
# 4. Truthful telemetry normalization (M6.0 §2 / §7.2)
# ---------------------------------------------------------------------------

def exposed(value: Any, *, reason: str | None = None) -> dict[str, Any]:
    """An EXPOSED metric carrying the EXACT provider-exposed value.

    ``0`` / ``False`` are real exposed values and are preserved. This is a claim of
    exposure: never use it for an unknown or estimated value.
    """
    if value is None:
        raise OrchestrationError(
            "an EXPOSED metric requires the exact exposed value; use not_exposed() "
            "when the provider does not expose it"
        )
    return {"status": TelemetryStatus.EXPOSED.value, "value": value, "reason": reason}


def not_exposed(reason: str = TELEMETRY_NOT_EXPOSED_REASON) -> dict[str, Any]:
    """A NOT_EXPOSED metric: ``value`` MUST be ``null`` and the reason is REQUIRED.

    This is the only way to say "unknown" — unknown can therefore never be encoded
    as ``0``.
    """
    if not isinstance(reason, str) or not reason.strip():
        raise OrchestrationError("a NOT_EXPOSED metric requires a non-blank reason")
    return {"status": TelemetryStatus.NOT_EXPOSED.value, "value": None, "reason": reason}


def build_telemetry(
    metrics: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Normalize a closed-set, fully-declared telemetry payload (fail closed).

    Rejects an unknown metric, a missing REQUIRED metric, and any metric whose
    declared shape contradicts its status. The M6.3 ledger re-validates the same
    rules at its durable boundary — this helper never bypasses it.
    """
    if not isinstance(metrics, Mapping):
        raise OrchestrationError("build_telemetry requires a metric mapping")
    unknown = sorted(m for m in metrics if m not in CONTRACT_TELEMETRY_METRICS)
    if unknown:
        raise OrchestrationError(f"non-contract telemetry metric(s): {unknown}")
    missing = [m for m in REQUIRED_TELEMETRY_METRICS if m not in metrics]
    if missing:
        raise OrchestrationError(
            "telemetry must declare a truthful state for every contract metric; "
            f"missing required metric(s): {missing}"
        )
    out: dict[str, dict[str, Any]] = {}
    for name, spec in metrics.items():
        if not isinstance(spec, Mapping):
            raise OrchestrationError(f"telemetry[{name}] must be a mapping")
        raw_status = spec.get("status")
        try:
            status = TelemetryStatus(raw_status)
        except ValueError:
            raise OrchestrationError(
                f"telemetry[{name}].status must be EXPOSED|NOT_EXPOSED, "
                f"got {raw_status!r}"
            ) from None
        value = spec.get("value")
        reason = spec.get("reason")
        if status is TelemetryStatus.EXPOSED:
            if value is None:
                raise OrchestrationError(
                    f"telemetry[{name}] EXPOSED requires an exact value"
                )
            out[name] = {"status": status.value, "value": value, "reason": reason}
        else:
            if value is not None:
                raise OrchestrationError(
                    f"telemetry[{name}] NOT_EXPOSED must carry value=null "
                    "(never zero-as-unknown)"
                )
            if not isinstance(reason, str) or not reason.strip():
                raise OrchestrationError(
                    f"telemetry[{name}] NOT_EXPOSED requires a non-blank reason"
                )
            out[name] = {"status": status.value, "value": None, "reason": reason}
    return out


def not_exposed_telemetry(
    reason: str = TELEMETRY_NOT_EXPOSED_REASON,
) -> dict[str, dict[str, Any]]:
    """The expected truthful state for the consumer Gemini Notebook surface.

    Every contract metric is explicitly ``NOT_EXPOSED`` with a reason — no invented
    model identity, no estimated tokens, no estimated cost. ``total_tokens`` is
    OMITTED (optional) rather than guessed.
    """
    return build_telemetry(
        metrics={name: not_exposed(reason) for name in REQUIRED_TELEMETRY_METRICS}
    )


# ---------------------------------------------------------------------------
# 5. Durable attempt recording + the M6.4 SUCCESS consumption gate
# ---------------------------------------------------------------------------

def record_failed_attempt(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    plan: AttemptPlan,
    provider_set: ProviderSet,
    transport_type: str,
    outcome: str | TerminalStatus,
    error: str | None,
    telemetry: Mapping[str, Any],
    started_at: str | None = None,
    completed_at: str | None = None,
) -> None:
    """Durably append ONE failed attempt from a VALIDATED plan (append-only).

    The attempt identity and its truthful labels come from the plan, which is
    validated against the committed Mode A / Mode B policy AND against the previous
    durable attempt — so a caller can no longer persist a fabricated provider
    fallback label or an unconfigured provider (round-2 reviewer finding).
    """
    if classify_attempt_outcome(outcome) is AttemptClassification.SUCCESS:
        raise OrchestrationError(
            "record_failed_attempt refuses SUCCESS — a successful attempt must go "
            "through accept_success_result (FD #152 proof gate)"
        )
    record, expected = _next_attempt_guard(store, ledger_id)
    _validate_plan_against_record(record, plan, provider_set, expected)
    store.append_attempt(
        ledger_id,
        attempt_number=plan.attempt_number,
        retry_mode=plan.retry_mode,
        provider_surface=plan.provider_surface,
        transport_type=transport_type,
        started_at=started_at,
        completed_at=completed_at,
        outcome=outcome,
        error=error,
        telemetry=telemetry,
    )


def accept_success_result(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    result: DeepResearchResult,
    plan: AttemptPlan,
    provider_set: ProviderSet,
    transport_type: str,
    telemetry: Mapping[str, Any],
    started_at: str | None = None,
    completed_at: str | None = None,
) -> RunRecord:
    """Accept a SUCCESS result and terminalize the run — proof verified FIRST.

    HARD carry-forward condition (FD #152 / M6.4 independent review): the result is
    revalidated with :meth:`DeepResearchResult.assert_proof_verified` BEFORE anything
    is recorded, terminalized or returned. A forged, unverified or
    post-construction-tampered SUCCESS can therefore never terminalize a run as
    SUCCESS. ``status == SUCCESS`` / ``is_success`` alone is NEVER sufficient.

    The attempt label/provider come from a validated :class:`AttemptPlan` (round-2
    reviewer finding). The final SUCCESS attempt and the SUCCESS terminal record (with
    the exact result binding) are written through ONE atomic M6.3 boundary
    (:meth:`DeepResearchRunLedgerStore.finalize_success_attempt_atomic`, FD #153), so a
    partial failure can never leave a SUCCESS attempt without its terminal result
    binding. A pre-amendment ORPHAN SUCCESS attempt (persisted attempt, no terminal
    record) is UNTRUSTED and is REFUSED fail-closed — it is never repaired and never
    given a caller-supplied result hash.

    M6.5 itself produces no provider SUCCESS: it only ACCEPTS a result that the
    trusted M6.4 verification path already produced (provider execution is
    M6.7/M6.8).
    """
    if not isinstance(result, DeepResearchResult):
        raise OrchestrationError("accept_success_result requires a DeepResearchResult")
    # --- the proof gate must run BEFORE any durable or downstream consumption ---
    result.assert_proof_verified()
    if not result.status.is_success:  # defensive: assert_proof_verified guards this
        raise OrchestrationError("accept_success_result requires a SUCCESS result")

    record = store.load_run(ledger_id)
    if record.is_terminal:
        raise RetryPolicyError(f"ledger run {ledger_id!r} is already terminal")
    # FD #152 exact-run binding: the result must belong to THIS target ledger run,
    # otherwise a proof-verified result produced for another run could terminalize
    # this one as SUCCESS (round-3 reviewer finding).
    _require_result_run_binding(record, result)
    if any(a.outcome == TerminalStatus.SUCCESS.value for a in record.attempts):
        # FD #153 §7 — PRE-AMENDMENT ORPHAN SUCCESS STATE. A persisted SUCCESS attempt
        # with NO terminal record is impossible through the atomic SUCCESS-finalization
        # boundary, so it can only be a legacy/foreign inconsistent state. It is
        # UNTRUSTED: FAIL CLOSED rather than attach an arbitrary newly supplied result
        # to it. No migration scheme, no inferred/missing result hash.
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} has a persisted SUCCESS attempt but no terminal "
            "record — a pre-amendment ORPHAN SUCCESS state. Recovery is REFUSED "
            "(fail-closed): a newly supplied result must never be attached to an orphan "
            "SUCCESS attempt"
        )

    _, expected = _next_attempt_guard(store, ledger_id)
    _validate_plan_against_record(record, plan, provider_set, expected)
    if result.provider_surface != plan.provider_surface:
        raise RetryPolicyError(
            "the successful result's provider surface must equal the validated attempt "
            f"plan provider ({result.provider_surface!r} != {plan.provider_surface!r})"
        )
    # FD #153: ONE atomic boundary — the final SUCCESS attempt and the SUCCESS terminal
    # record carrying the exact result binding can never be separated by a partial
    # failure (no `append_attempt(SUCCESS)` + separate `terminalize(SUCCESS)` pair).
    store.finalize_success_attempt_atomic(
        ledger_id,
        attempt_number=plan.attempt_number,
        retry_mode=plan.retry_mode,
        provider_surface=plan.provider_surface,
        transport_type=transport_type,
        result_sha256=result.result_sha256,
        result_artifact_ref=result.result_artifact_ref,
        started_at=started_at,
        completed_at=completed_at,
        telemetry=telemetry,
    )
    return store.load_run(ledger_id)


def terminalize_research_unavailable(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    failure_detail: str,
) -> RunRecord:
    """Terminalize an exhausted logical run as ``RESEARCH_UNAVAILABLE``.

    The linked EG-01 instruction is emitted by :func:`decide_retry`; this function
    performs only the run terminalization the ledger already owns.
    """
    record = store.load_run(ledger_id)
    if record.is_terminal:
        raise RetryPolicyError(f"ledger run {ledger_id!r} is already terminal")
    used = [a.attempt_number for a in record.attempts]
    if used != list(range(1, len(used) + 1)):
        raise RetryPolicyError(
            f"ledger run {ledger_id!r} has a non-contiguous attempt history {used}"
        )
    if len(used) != MAX_ATTEMPTS:
        raise RetryPolicyError(
            "RESEARCH_UNAVAILABLE requires the retry budget to be ACTUALLY exhausted "
            f"({MAX_ATTEMPTS} attempts); ledger run {ledger_id!r} has {len(used)} "
            "attempt(s) — use the appropriate typed failure instead"
        )
    # EVERY attempt must be retryable: an earlier fail-closed outcome (or a SUCCESS)
    # makes "retry exhaustion" the wrong disposition.
    _require_all_attempts_retryable(record)
    store.terminalize(
        ledger_id,
        terminal_status=TerminalStatus.RESEARCH_UNAVAILABLE,
        failure_detail=failure_detail,
    )
    return store.load_run(ledger_id)
