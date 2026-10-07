"""M6.4 — Research Request/Result Adapter Contract (S10-facing, NON-CANONICAL).

Authority: FD #151 (M6 implementation order) · FD #148–150 · M6.0 design-gate
reconciliation (``design/qad-pivot/m6/QAD-M6.0-DESIGN-GATE-RECONCILIATION.md``)
· M3 S10 *Notebook / Deep Research Interface*
(``design/qad-pivot/QAD-M3-SERVICE-CONTRACTS.md`` §S10) · accepted M6.1 archive
attestation · accepted M6.2 SEALED snapshot builder · accepted M6.3
``DeepResearchRunLedgerStore``.

What this cluster is
--------------------
The IIP-facing LOGICAL request/result boundary for a Deep Research call. It
defines immutable envelopes and their validation rules. It performs **no**
provider work: no Gemini Notebook, no browser/Google transport, no retry or
fallback orchestration, no live source discovery, no canonical evidence
admission, no production activation, no network I/O of any kind.

S10 truth preserved
-------------------
* inputs = research question + approved source corpus + prior evidence (where
  contractually allowed) + provider configuration;
* outputs = synthesis + source pointers, **NON-CANONICAL** — they must be
  validated against the original source before any canonical admission;
* persistent state = ``Stateless (per-request)`` from IIP's perspective, i.e.
  REQUEST-ISOLATED RECONSTRUCTION (FD #148 R-4): the request must never inherit
  an accumulated Notebook chat, a previous Deep Research report, a hidden
  Notebook source corpus, or a previous request workspace;
* failure = documented, never a silent blank.

SEALED authority
----------------
For a SEALED request the authoritative ``case_id``, ``case_version``, PIT mode,
``as_of``, source corpus and ``input_snapshot_hash`` all derive from the
accepted M6.2 :class:`~qad.m6.snapshot.SealedInputSnapshot`. Caller-supplied
claims are accepted only as an assertion that must AGREE with the snapshot;
any disagreement fails closed. M6.4 introduces **no** second PIT authority.

Hash policy
-----------
``request_payload_hash`` is deterministic over the logical semantic payload
(never wall-clock, never a random UUID, never object identity, never a
filesystem path). It is NOT a retry/idempotency mechanism — the idempotency key,
attempt numbering and duplicate-run suppression belong to M6.5.

``result_sha256`` is computed over the exact result bytes that are stored or
passed onward. Hash absence is represented by ``None``; a hash is never
fabricated for absent output.

Boundary: nothing here is a canonical M4A schema; nothing here may upgrade a
result to canonical evidence. Canonical admission is M6.6 plus the existing
Evidence Admission Gate.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

from pydantic import BaseModel

from qad.m6.ledger import (
    DeepResearchRunLedgerStore,
    LedgerError,
    validate_rrm_deep_research_runs,
)
from qad.m6.snapshot import (
    PROVIDER_CANNOT_ENFORCE_SEALED_INPUT,
    SEALED_PIT_MODE,
    SealedInputSnapshot,
)
from qad.persistence.serialization import compute_canonical_hash

#: The only S10-facing capability this contract exposes.
S10_CAPABILITY = "S10"

#: M6.0 §11.2 / R7 — positive clean-context proof is required; otherwise the run
#: fails closed with this state (``REQUEST_ISOLATION_UNVERIFIED``).
REQUEST_ISOLATION_UNVERIFIED = "REQUEST_ISOLATION_UNVERIFIED"

__all__ = [
    "S10_CAPABILITY",
    "REQUEST_ISOLATION_UNVERIFIED",
    "PROVIDER_CANNOT_ENFORCE_SEALED_INPUT",
    "ResearchContractError",
    "RequestAuthorityViolation",
    "ResearchRequestError",
    "ResearchResultError",
    "ResearchResultStatus",
    "ClosedCorpusEnforcement",
    "IsolationVerification",
    "ProviderConfiguration",
    "SourceCorpusDescriptor",
    "DeepResearchRequest",
    "SourcePointer",
    "DeepResearchResult",
    "build_deep_research_request",
    "build_deep_research_result",
    "compute_result_sha256",
    "result_matches_hash",
    "validate_ledger_linkage",
    "validate_rrm_deep_research_runs",
]


# ---------------------------------------------------------------------------
# Typed errors
# ---------------------------------------------------------------------------


class ResearchContractError(Exception):
    """Base class for deterministic M6.4 request/result contract failures."""


class RequestAuthorityViolation(ResearchContractError):
    """A caller claim disagreed with the authoritative SEALED snapshot."""


class ResearchRequestError(ResearchContractError):
    """The request envelope itself failed a contract rule."""


class ResearchResultError(ResearchContractError):
    """The result envelope failed a contract rule (e.g. blank SUCCESS)."""


# ---------------------------------------------------------------------------
# Vocabulary (reuses the accepted M6 failure-state vocabulary)
# ---------------------------------------------------------------------------


class ResearchResultStatus(str, Enum):
    """Result states (M6.0 §8 / §10 / §11.2, S10 failure behavior)."""

    SUCCESS = "SUCCESS"
    RESEARCH_UNAVAILABLE = "RESEARCH_UNAVAILABLE"
    TRANSPORT_FAILURE = "TRANSPORT_FAILURE"
    PIT_BLOCK = "PIT_BLOCK"
    INCOMPLETE = "INCOMPLETE"
    PROVIDER_CANNOT_ENFORCE_SEALED_INPUT = "PROVIDER_CANNOT_ENFORCE_SEALED_INPUT"
    REQUEST_ISOLATION_UNVERIFIED = "REQUEST_ISOLATION_UNVERIFIED"

    @property
    def is_success(self) -> bool:
        return self is ResearchResultStatus.SUCCESS


class ClosedCorpusEnforcement(str, Enum):
    """Closed-corpus enforcement evidence carried on a result.

    M6.4 never claims enforcement: the default is ``NOT_VERIFIED``. ``ENFORCED``
    is reserved for a later cluster's real evidence; ``CANNOT_ENFORCE`` forces
    ``PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`` (fail closed — never a fabricated
    success).
    """

    NOT_VERIFIED = "NOT_VERIFIED"
    ENFORCED = "ENFORCED"
    CANNOT_ENFORCE = "CANNOT_ENFORCE"


class IsolationVerification(str, Enum):
    """Request-isolation proof state carried on a result (M6.0 §11.2 R7)."""

    NOT_VERIFIED = "NOT_VERIFIED"
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"


# ---------------------------------------------------------------------------
# Request envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProviderConfiguration:
    """Provider-neutral configuration sufficient for a later provider adapter.

    Deliberately free of transport detail: no Chrome selectors, no Notebook
    URLs, no debugging ports, no cookies, no credentials, no navigation.
    """

    provider_surface: str
    capability: str = S10_CAPABILITY
    closed_corpus_required: bool = True
    request_isolation_required: bool = True
    timeout_seconds: int | None = None


@dataclass(frozen=True)
class SourceCorpusDescriptor:
    """The exact approved corpus for the request (SEALED: the M6.2 snapshot corpus)."""

    source_ids: tuple[str, ...]
    exact_blob_hashes: tuple[tuple[str, str], ...]
    corpus_hash: str
    closed_corpus_required: bool

    @property
    def source_count(self) -> int:
        return len(self.source_ids)


@dataclass(frozen=True)
class DeepResearchRequest:
    """Immutable logical Deep Research request (operational, NON-CANONICAL).

    Every identity/authority field is derived from the authoritative
    :class:`SealedInputSnapshot`; the caller supplies only the research question,
    the evidence-gap identity, orchestration references, provider selection and
    the authorized prior-evidence references.
    """

    request_id: str
    research_run_id: str
    ledger_id: str
    rrm_manifest_id: str
    case_id: str
    case_version: str
    evidence_gap_id: str
    research_question: str
    pit_context_id: str
    pit_mode: str
    as_of: str
    input_snapshot_hash: str
    snapshot_id: str
    corpus: SourceCorpusDescriptor
    provider: ProviderConfiguration
    request_isolation_required: bool
    authorized_prior_evidence_refs: tuple[str, ...]
    request_payload_hash: str
    capability: str = S10_CAPABILITY

    @property
    def non_canonical(self) -> bool:
        """Always True: a request envelope is operational, never canonical."""
        return True

    @property
    def closed_corpus_required(self) -> bool:
        return self.corpus.closed_corpus_required

    @property
    def source_ids(self) -> tuple[str, ...]:
        return self.corpus.source_ids


class _RequestPayloadIdentity(BaseModel):
    """Private deterministic hash payload (NOT a canonical M4A schema)."""

    research_question: str
    case_id: str
    case_version: str
    evidence_gap_id: str
    input_snapshot_hash: str
    pit_mode: str
    as_of: str
    capability: str
    closed_corpus_required: bool
    request_isolation_required: bool


def _deterministic_hash(payload: BaseModel) -> str:
    return compute_canonical_hash(payload)


def _require_non_empty(value: Any, name: str, error: type[ResearchContractError]) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error(f"{name} must be a non-empty string")
    return value


def _check_claim(name: str, claimed: Any, authoritative: Any) -> None:
    """Fail closed when a caller claim disagrees with the snapshot authority."""
    if claimed is None:
        return
    if claimed != authoritative:
        raise RequestAuthorityViolation(
            f"{name} claim {claimed!r} disagrees with the authoritative SEALED "
            f"snapshot value {authoritative!r}"
        )


def build_deep_research_request(
    *,
    snapshot: SealedInputSnapshot,
    request_id: str,
    research_run_id: str,
    ledger_id: str,
    rrm_manifest_id: str,
    evidence_gap_id: str,
    research_question: str,
    provider_surface: str,
    capability: str = S10_CAPABILITY,
    authorized_prior_evidence_refs: Sequence[str] = (),
    timeout_seconds: int | None = None,
    claimed_case_id: str | None = None,
    claimed_case_version: str | None = None,
    claimed_pit_mode: str | None = None,
    claimed_as_of: str | None = None,
    claimed_input_snapshot_hash: str | None = None,
    claimed_source_ids: Sequence[str] | None = None,
    claimed_closed_corpus_required: bool | None = None,
) -> DeepResearchRequest:
    """Build the immutable logical request from the authoritative snapshot.

    The snapshot supplies ``case_id``, ``case_version``, PIT mode, ``as_of``,
    the source corpus and ``input_snapshot_hash``. Optional ``claimed_*``
    arguments are assertions only — any disagreement raises
    :class:`RequestAuthorityViolation` (fail closed).
    """
    if not isinstance(snapshot, SealedInputSnapshot):
        raise RequestAuthorityViolation(
            "a SEALED request requires an authoritative SealedInputSnapshot"
        )
    if snapshot.pit_mode != SEALED_PIT_MODE:
        raise RequestAuthorityViolation(
            f"snapshot PIT mode {snapshot.pit_mode!r} is not {SEALED_PIT_MODE!r}"
        )
    if not snapshot.closed_corpus_required:
        raise RequestAuthorityViolation(
            "the SEALED snapshot must require a closed corpus"
        )

    _require_non_empty(request_id, "request_id", ResearchRequestError)
    _require_non_empty(research_run_id, "research_run_id", ResearchRequestError)
    _require_non_empty(ledger_id, "ledger_id", ResearchRequestError)
    _require_non_empty(rrm_manifest_id, "rrm_manifest_id", ResearchRequestError)
    _require_non_empty(evidence_gap_id, "evidence_gap_id", ResearchRequestError)
    _require_non_empty(research_question, "research_question", ResearchRequestError)
    _require_non_empty(provider_surface, "provider_surface", ResearchRequestError)
    if capability != S10_CAPABILITY:
        raise ResearchRequestError(
            f"unsupported capability {capability!r}; M6.4 exposes {S10_CAPABILITY!r} only"
        )

    # ---- authority: caller claims may only AGREE with the snapshot ----------
    _check_claim("case_id", claimed_case_id, snapshot.case_id)
    _check_claim("case_version", claimed_case_version, snapshot.case_version)
    _check_claim("pit_mode", claimed_pit_mode, snapshot.pit_mode)
    _check_claim("as_of", claimed_as_of, snapshot.as_of)
    _check_claim("input_snapshot_hash", claimed_input_snapshot_hash,
                 snapshot.input_snapshot_hash)
    _check_claim("closed_corpus_required", claimed_closed_corpus_required, True)

    ordered = tuple(snapshot.ordered_sources)
    snapshot_source_ids = tuple(s.source_id for s in ordered)

    if claimed_source_ids is not None:
        claimed = tuple(claimed_source_ids)
        if tuple(sorted(claimed)) != tuple(sorted(snapshot_source_ids)) or len(
            set(claimed)
        ) != len(claimed):
            raise RequestAuthorityViolation(
                "claimed source corpus disagrees with the authoritative snapshot corpus"
            )

    # ---- corpus derived from the snapshot only ------------------------------
    exact_blob_hashes = tuple((s.source_id, s.raw_blob_sha256) for s in ordered)
    corpus_identity = _CorpusIdentity(
        sources=[
            _CorpusSource(source_id=sid, exact_blob_hash=h)
            for sid, h in exact_blob_hashes
        ]
    )
    corpus = SourceCorpusDescriptor(
        source_ids=snapshot_source_ids,
        exact_blob_hashes=exact_blob_hashes,
        corpus_hash=_deterministic_hash(corpus_identity),
        closed_corpus_required=True,
    )

    prior_refs = tuple(authorized_prior_evidence_refs)
    for ref in prior_refs:
        if not isinstance(ref, str) or not ref.strip():
            raise ResearchRequestError(
                "authorized_prior_evidence_refs entries must be non-empty strings"
            )

    payload_hash = _deterministic_hash(
        _RequestPayloadIdentity(
            research_question=research_question,
            case_id=snapshot.case_id,
            case_version=snapshot.case_version,
            evidence_gap_id=evidence_gap_id,
            input_snapshot_hash=snapshot.input_snapshot_hash,
            pit_mode=snapshot.pit_mode,
            as_of=snapshot.as_of,
            capability=S10_CAPABILITY,
            closed_corpus_required=True,
            request_isolation_required=True,
        )
    )

    return DeepResearchRequest(
        request_id=request_id,
        research_run_id=research_run_id,
        ledger_id=ledger_id,
        rrm_manifest_id=rrm_manifest_id,
        case_id=snapshot.case_id,
        case_version=snapshot.case_version,
        evidence_gap_id=evidence_gap_id,
        research_question=research_question,
        pit_context_id=snapshot.pit_context_id,
        pit_mode=snapshot.pit_mode,
        as_of=snapshot.as_of,
        input_snapshot_hash=snapshot.input_snapshot_hash,
        snapshot_id=snapshot.snapshot_id,
        corpus=corpus,
        provider=ProviderConfiguration(
            provider_surface=provider_surface,
            capability=S10_CAPABILITY,
            closed_corpus_required=True,
            request_isolation_required=True,
            timeout_seconds=timeout_seconds,
        ),
        request_isolation_required=True,
        authorized_prior_evidence_refs=prior_refs,
        request_payload_hash=payload_hash,
        capability=S10_CAPABILITY,
    )


class _CorpusSource(BaseModel):
    source_id: str
    exact_blob_hash: str


class _CorpusIdentity(BaseModel):
    sources: list[_CorpusSource]


# ---------------------------------------------------------------------------
# Result envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourcePointer:
    """A provider citation / DISCOVERED SOURCE REFERENCE — never canonical evidence."""

    index: int
    reference: str
    title: str | None = None


@dataclass(frozen=True)
class DeepResearchResult:
    """Immutable logical Deep Research result (NON-CANONICAL, fail-closed).

    The envelope carries no field that could upgrade it to canonical evidence:
    canonical admission is M6.6 plus the existing Evidence Admission Gate.
    """

    request_id: str
    research_run_id: str
    ledger_id: str
    status: ResearchResultStatus
    provider_surface: str
    result_bytes: bytes | None = None
    result_artifact_ref: str | None = None
    result_sha256: str | None = None
    synthesis_ref: str | None = None
    source_pointers: tuple[SourcePointer, ...] = ()
    completed_at: str | None = None
    provider_reported_metadata: Mapping[str, str] | None = None
    failure_detail: str | None = None
    closed_corpus_enforcement: ClosedCorpusEnforcement = ClosedCorpusEnforcement.NOT_VERIFIED
    isolation_verification: IsolationVerification = IsolationVerification.NOT_VERIFIED

    @property
    def non_canonical(self) -> bool:
        """Always True — a Deep Research result is never canonical evidence."""
        return True

    @property
    def is_success(self) -> bool:
        return self.status.is_success

    @property
    def source_pointer_count(self) -> int:
        return len(self.source_pointers)


def compute_result_sha256(result_bytes: bytes) -> str:
    """SHA-256 over the EXACT bytes that are stored/passed onward."""
    if not isinstance(result_bytes, (bytes, bytearray)):
        raise ResearchResultError("result bytes must be bytes")
    return hashlib.sha256(bytes(result_bytes)).hexdigest()


def result_matches_hash(result: DeepResearchResult) -> bool:
    """True iff the stored bytes hash to the recorded ``result_sha256``."""
    if result.result_bytes is None or result.result_sha256 is None:
        return False
    return compute_result_sha256(result.result_bytes) == result.result_sha256


def build_deep_research_result(
    *,
    request_id: str,
    research_run_id: str,
    ledger_id: str,
    status: str | ResearchResultStatus,
    provider_surface: str,
    result_bytes: bytes | None = None,
    result_artifact_ref: str | None = None,
    result_sha256: str | None = None,
    synthesis_ref: str | None = None,
    source_pointers: Sequence[SourcePointer] = (),
    completed_at: str | None = None,
    provider_reported_metadata: Mapping[str, str] | None = None,
    failure_detail: str | None = None,
    closed_corpus_enforcement: str | ClosedCorpusEnforcement = (
        ClosedCorpusEnforcement.NOT_VERIFIED
    ),
    isolation_verification: str | IsolationVerification = (
        IsolationVerification.NOT_VERIFIED
    ),
) -> DeepResearchResult:
    """Build an immutable result envelope from provider output.

    SUCCESS is refused for blank output, and a hash is never fabricated for
    absent output. Failures must carry a documented ``failure_detail``.
    """
    try:
        status_enum = ResearchResultStatus(status)
    except ValueError:
        raise ResearchResultError(f"unknown result status {status!r}") from None

    try:
        corpus_enum = ClosedCorpusEnforcement(closed_corpus_enforcement)
    except ValueError:
        raise ResearchResultError(
            f"unknown closed-corpus enforcement state {closed_corpus_enforcement!r}"
        ) from None

    try:
        isolation_enum = IsolationVerification(isolation_verification)
    except ValueError:
        raise ResearchResultError(
            f"unknown isolation verification state {isolation_verification!r}"
        ) from None

    _require_non_empty(request_id, "request_id", ResearchResultError)
    _require_non_empty(research_run_id, "research_run_id", ResearchResultError)
    _require_non_empty(ledger_id, "ledger_id", ResearchResultError)
    _require_non_empty(provider_surface, "provider_surface", ResearchResultError)

    # ---- fail-closed enforcement states cannot masquerade as SUCCESS -------
    if corpus_enum is ClosedCorpusEnforcement.CANNOT_ENFORCE and (
        status_enum is not ResearchResultStatus.PROVIDER_CANNOT_ENFORCE_SEALED_INPUT
    ):
        raise ResearchResultError(
            "a provider that cannot enforce the closed corpus must fail closed "
            "with PROVIDER_CANNOT_ENFORCE_SEALED_INPUT (never a fabricated success)"
        )
    if isolation_enum is IsolationVerification.UNVERIFIED and (
        status_enum is not ResearchResultStatus.REQUEST_ISOLATION_UNVERIFIED
    ):
        raise ResearchResultError(
            "an unverified request-isolation state must fail closed with "
            "REQUEST_ISOLATION_UNVERIFIED"
        )

    if status_enum.is_success:
        if result_bytes is None or len(bytes(result_bytes)) == 0:
            raise ResearchResultError(
                "SUCCESS requires non-empty result content (a blank provider "
                "result must be represented as a typed failure)"
            )
        if not result_sha256:
            raise ResearchResultError("SUCCESS requires the exact result_sha256")
        actual = compute_result_sha256(bytes(result_bytes))
        if actual != result_sha256:
            raise ResearchResultError(
                f"result_sha256 mismatch: recorded {result_sha256}, actual {actual}"
            )
        if failure_detail:
            raise ResearchResultError("SUCCESS must not carry failure_detail")
        if isolation_enum is IsolationVerification.UNVERIFIED:
            raise ResearchResultError(
                "SUCCESS with unverified request isolation is refused"
            )
    else:
        if not failure_detail or not str(failure_detail).strip():
            raise ResearchResultError(
                "a non-SUCCESS result requires a documented failure_detail "
                "(failures are never a silent blank)"
            )
        if result_bytes is None and result_sha256 is not None:
            raise ResearchResultError(
                "a hash must never be recorded for absent result output"
            )
        if result_bytes is not None:
            actual = compute_result_sha256(bytes(result_bytes))
            if result_sha256 is not None and actual != result_sha256:
                raise ResearchResultError(
                    f"result_sha256 mismatch: recorded {result_sha256}, actual {actual}"
                )

    pointers = tuple(source_pointers)
    for ptr in pointers:
        if not isinstance(ptr, SourcePointer):
            raise ResearchResultError("source_pointers must contain SourcePointer values")
        if not isinstance(ptr.reference, str) or not ptr.reference.strip():
            raise ResearchResultError("a source pointer requires a non-empty reference")

    return DeepResearchResult(
        request_id=request_id,
        research_run_id=research_run_id,
        ledger_id=ledger_id,
        status=status_enum,
        provider_surface=provider_surface,
        result_bytes=None if result_bytes is None else bytes(result_bytes),
        result_artifact_ref=result_artifact_ref,
        result_sha256=result_sha256,
        synthesis_ref=synthesis_ref,
        source_pointers=pointers,
        completed_at=completed_at,
        provider_reported_metadata=dict(provider_reported_metadata or {}),
        failure_detail=failure_detail,
        closed_corpus_enforcement=corpus_enum,
        isolation_verification=isolation_enum,
    )


# ---------------------------------------------------------------------------
# Linkage (bounded — no ledger/RRM redesign, no orchestration)
# ---------------------------------------------------------------------------


def validate_ledger_linkage(
    ledger_store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    research_run_id: str,
) -> None:
    """Require the request/result ``ledger_id`` to resolve to the ledger record.

    Bounded integration with the accepted M6.3 ledger: no redesign, no second
    provenance store, and the ledger is never turned into a provider transport.
    """
    try:
        record = ledger_store.load_run(ledger_id)
    except LedgerError as exc:
        raise ResearchContractError(
            f"ledger_id {ledger_id!r} does not resolve to a ledger record: {exc}"
        ) from exc
    if record.research_run_id != research_run_id:
        raise ResearchContractError(
            f"ledger {ledger_id!r} belongs to research_run_id "
            f"{record.research_run_id!r}, not {research_run_id!r}"
        )
