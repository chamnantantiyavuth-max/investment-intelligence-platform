"""M6.6 — Noncanonical Source Discovery + Admission Bridge (FD #151).

Bounded provider-neutral bridge from NONCANONICAL discovered source references
(provider citations / source pointers) to durable candidate registration,
independent original-source verification, selective canonical admission, and
durable candidate dispositions.

Core doctrine (M6.0 §5/§7/§9, FD #148–#154):

* A provider report / citation / synthesis / source pointer is a DISCOVERY HINT.
  It is NEVER canonical evidence and never verifies itself.
* Provider-authored claims (including ``original_source_verified=true``) are NOT
  verification authority. Trusted verification is an injected orchestration
  dependency whose DEFAULT state DENIES (fail closed).
* No blind Import All. Every discovered candidate receives exactly ONE durable
  disposition through the accepted M6.3 ledger.
* PIT authority is unchanged: SEALED/replay eligibility is decided by the
  existing archive-admission-attestation rule; a newly discovered current source
  can never be injected into a closed SEALED corpus.
* Canonical admission happens ONLY through the existing authoritative boundaries
  (``RawSourceArchive.admit_source`` / ``EvidenceRegistry.admit_evidence``).
  ``store()`` / direct canonical writes are never used as a bypass.

This module performs NO provider execution: no Gemini, no Notebook transport, no
browser/CDP automation, no network, no credentials. Original-source bytes are
supplied through approved authority boundaries (deterministic fixtures/archives).

**This module never writes a Deep Research SUCCESS.** It does not call
``append_attempt(outcome=SUCCESS)``, ``terminalize(terminal_status=SUCCESS)`` or
``finalize_success_attempt_atomic(...)``. ``M6_RAW_SUCCESS_API_GATE`` (FD #154)
remains OPEN and is neither closed, weakened, bypassed nor reinterpreted here.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, Sequence

from qad.m6.ledger import (
    CandidateDisposition,
    DeepResearchRunLedgerStore,
    LedgerIdentityConflict,
    LedgerTerminalError,
    LedgerValidationError,
    RunRecord,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.persistence.errors import IntegrityConflict

#: PIT modes (string values mirror ``PITContextMode``; compared as strings so the
#: bridge never invents a second PIT vocabulary).
_SEALED = "SEALED_HISTORICAL_EVALUATION"
_REPLAY_EXCEPTION = "REPLAY_EXCEPTION"
_LIVE = "LIVE_CASE_UPDATE"

#: Truthful candidate statuses BEFORE disposition is decided.
VERIFICATION_STATUS_PENDING = "PENDING"
PIT_ELIGIBILITY_UNKNOWN = "UNKNOWN"

#: The exact canonical TRUE representation required by the authoritative
#: EvidenceRegistry AI-method gate (Founder Decision, 26 Aug 2026).
ORIGINAL_SOURCE_VERIFIED_TRUE = "true"

#: Documented reason codes (truthful, auditable).
REASON_NO_VERIFIER = "NO_TRUSTED_ORIGINAL_SOURCE_VERIFIER_CONFIGURED"
REASON_SOURCE_NOT_FOUND = "ORIGINAL_SOURCE_DOCUMENT_NOT_AVAILABLE"
REASON_SOURCE_MISMATCH = "ORIGINAL_SOURCE_MISMATCH"
REASON_INSUFFICIENT_PROOF = "ORIGINAL_SOURCE_PROOF_INSUFFICIENT"
REASON_SEALED_NOT_ELIGIBLE = "NOT_ELIGIBLE_FOR_SEALED_PIT"
REASON_REPLAY_EXCEPTION_BOUNDARY = "REPLAY_EXCEPTION_AUTHORIZATION_BOUNDARY_REQUIRED"
REASON_ADMITTED = "ORIGINAL_SOURCE_VERIFIED_AND_ADMITTED"
REASON_REUSED = "ORIGINAL_SOURCE_ALREADY_ADMITTED_AND_ELIGIBLE"
REASON_IDENTITY_CONFLICT = "SOURCE_IDENTITY_CONFLICT"

#: Exact canonical FOUNDER authorization role required for REPLAY_EXCEPTION
#: (mirrors the accepted runtime token in ``PITEnforcementService``).
FOUNDER_ROLE_TOKEN = "FOUNDER"


class SourceBridgeError(Exception):
    """Base class for M6.6 bridge errors."""


class CandidateIdentityConflict(SourceBridgeError):
    """A re-registered candidate id resolved to a DIFFERENT pointer identity.

    Candidate identity is deterministic, so this indicates corruption or a
    hostile/replayed identifier — never a silent overwrite.
    """


class SourceFailureKind(str, Enum):
    """Why independent original-source verification did not succeed.

    Deterministic disposition mapping (documented, no caller policy):
      NOT_FOUND          -> UNAVAILABLE
      MISMATCH           -> REJECTED
      INSUFFICIENT_PROOF -> DEFERRED
    """

    NOT_FOUND = "NOT_FOUND"
    MISMATCH = "MISMATCH"
    INSUFFICIENT_PROOF = "INSUFFICIENT_PROOF"


# ---------------------------------------------------------------------------
# Noncanonical input boundary
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DiscoveredSourceReference:
    """A NONCANONICAL discovered source reference (citation / source pointer).

    Deliberately minimal: a citation index plus an external reference string.
    ``provider_claim_original_source_verified`` records what the provider CLAIMED;
    it is never trusted as verification authority.
    """

    index: int
    reference: str
    title: str | None = None
    provider_claim_original_source_verified: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.index, int) or isinstance(self.index, bool) or self.index < 0:
            raise SourceBridgeError(
                "a discovered source reference requires a non-negative integer index"
            )
        if not isinstance(self.reference, str) or not self.reference.strip():
            raise SourceBridgeError("a discovered source reference requires a non-blank reference")


def coerce_discovered_reference(pointer: Any) -> DiscoveredSourceReference:
    """Coerce an M6.4 ``SourcePointer`` (or compatible object) into the bridge input.

    Only the DISCOVERY fields are read — an M6.4 source pointer confers no
    evidence status.
    """
    if isinstance(pointer, DiscoveredSourceReference):
        return pointer
    index = getattr(pointer, "index", None)
    reference = getattr(pointer, "reference", None)
    if reference is None:
        raise SourceBridgeError(
            "the bridge input must expose .index and .reference (e.g. an M6.4 SourcePointer)"
        )
    return DiscoveredSourceReference(
        index=index,
        reference=reference,
        title=getattr(pointer, "title", None),
    )


# ---------------------------------------------------------------------------
# Stable candidate identity
# ---------------------------------------------------------------------------


def compute_source_candidate_id(
    *, ledger_id: str, pointer_index: int, reference: str,
) -> str:
    """Deterministic, durably repeatable candidate identity within the exact run.

    Inputs: the exact logical run, the citation index and the external reference.

    The identity MUST NOT depend on wall clock, random UUID, process/object
    identity, filesystem path, provider surface, attempt number or verification
    outcome. Re-processing the same discovered reference therefore resolves to the
    SAME candidate (no silent duplicate), while a DIFFERENT citation index remains
    a DISTINCT candidate even when it points at the same underlying document.
    """
    if not isinstance(ledger_id, str) or not ledger_id.strip():
        raise SourceBridgeError("compute_source_candidate_id requires a non-blank ledger_id")
    if not isinstance(pointer_index, int) or isinstance(pointer_index, bool) or pointer_index < 0:
        raise SourceBridgeError("compute_source_candidate_id requires a non-negative index")
    if not isinstance(reference, str) or not reference.strip():
        raise SourceBridgeError("compute_source_candidate_id requires a non-blank reference")
    identity = {
        "ledger_id": ledger_id,
        "pointer_index": pointer_index,
        "reference": " ".join(reference.split()),
    }
    digest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"SC-{digest[:24]}"


# ---------------------------------------------------------------------------
# Original-source verification seam (trusted orchestration dependency)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceVerificationRequest:
    """Exact execution context bound into independent verification (no replay)."""

    ledger_id: str
    research_run_id: str
    request_id: str
    source_candidate_id: str
    pointer_index: int
    reference: str
    claimed_title: str | None = None
    provider_claim_original_source_verified: str | None = None


@dataclass(frozen=True)
class SourceVerificationCandidate:
    """What a verifier RETURNS — an UNTRUSTED candidate verdict (permissive DTO).

    Deliberately NOT proof: anyone (including a provider-shaped caller) can construct
    one, so it confers no authority. The bridge converts a candidate into the trusted
    :class:`OriginalSourceVerification` ONLY through its module-internal minting path,
    bound to the exact request.
    """

    verified: bool
    reason: str
    failure_kind: SourceFailureKind | None = None
    source_id: str | None = None
    source_tier: str | None = None
    source_type: str | None = None
    content_hash: str | None = None
    raw_bytes: bytes | None = None
    location: str | None = None
    publication_date: str | None = None
    retrieval_date: str | None = None
    title: str | None = None
    mismatches: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise SourceBridgeError("a source verification candidate requires a non-blank reason")
        if not self.verified:
            return
        for name, value in (
            ("source_id", self.source_id),
            ("source_tier", self.source_tier),
            ("source_type", self.source_type),
            ("content_hash", self.content_hash),
            ("retrieval_date", self.retrieval_date),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SourceBridgeError(f"a verified candidate requires a non-blank {name}")
        if not isinstance(self.raw_bytes, bytes) or not self.raw_bytes:
            raise SourceBridgeError("a verified candidate requires the exact original bytes")
        if self.mismatches:
            raise SourceBridgeError("a verified candidate cannot carry mismatches")
        if hashlib.sha256(self.raw_bytes).hexdigest() != self.content_hash:
            raise SourceBridgeError("a verified candidate requires content_hash == sha256(raw_bytes)")


#: Module-private minting token. A TRUSTED verdict exists only when the module-internal
#: minting path attached this token; a plain caller cannot obtain a trusted verdict by
#: construction (FD #152 principle: direct construction cannot bypass verification).
#: Hostile same-process introspection of the token is OUTSIDE the accepted trust
#: boundary (FD #152, Founder-fixed).
_MINT_TOKEN = object()


@dataclass(frozen=True)
class OriginalSourceVerification:
    """TRUSTED, immutable verdict — mintable ONLY by the bridge's verification path.

    Direct construction is REFUSED. A verdict is minted inside
    :func:`verify_and_admit_source` and is BOUND to the exact (ledger run, candidate)
    it was produced for, so a verdict minted for one candidate can never authorize
    another (no cross-candidate / cross-run replay).
    """

    verified: bool
    reason: str
    failure_kind: SourceFailureKind | None = None
    source_id: str | None = None
    source_tier: str | None = None
    source_type: str | None = None
    content_hash: str | None = None
    raw_bytes: bytes | None = None
    location: str | None = None
    publication_date: str | None = None
    retrieval_date: str | None = None
    title: str | None = None
    mismatches: tuple[str, ...] = ()
    _minted: object | None = field(default=None, repr=False, compare=False)
    bound_ledger_id: str | None = field(default=None, repr=False, compare=False)
    bound_source_candidate_id: str | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._minted is not _MINT_TOKEN:
            raise SourceBridgeError(
                "an original-source verdict cannot be constructed directly; it is minted "
                "only by the trusted verification path (FD #152 principle)"
            )
        if not (self.bound_ledger_id and self.bound_source_candidate_id):
            raise SourceBridgeError("a verdict must be bound to its exact run and candidate")

    def assert_attested_for(
        self, *, ledger_id: str, source_candidate_id: str, source_id: str | None = None,
    ) -> None:
        """Consumption-boundary re-validation (no replay across candidates/runs)."""
        if self._minted is not _MINT_TOKEN:
            raise SourceBridgeError("verdict is not a minted trusted verdict")
        if (
            self.bound_ledger_id != ledger_id
            or self.bound_source_candidate_id != source_candidate_id
        ):
            raise SourceBridgeError(
                "verdict is not bound to this run/candidate (minted for "
                f"{self.bound_ledger_id!r}/{self.bound_source_candidate_id!r})"
            )
        if source_id is not None and self.verified and self.source_id != source_id:
            raise SourceBridgeError(
                f"verdict source_id {self.source_id!r} does not match {source_id!r}"
            )

    def is_verified_verdict_for(self, *, source_id: str) -> bool:
        """True ONLY for a MINTED VERIFIED verdict for exactly this source.

        This gates the HONEST construction of the canonical
        ``original_source_verified`` truth value. The authoritative RUN/CANDIDATE
        binding is additionally enforced at the evidence-admission boundary via
        :meth:`authorizes_evidence_for`.
        """
        return bool(
            self._minted is _MINT_TOKEN
            and self.verified
            and not self.mismatches
            and self.source_id == source_id
        )

    def authorizes_evidence_for(
        self, *, ledger_id: str, source_candidate_id: str, source_id: str,
    ) -> bool:
        """FULL consumption-boundary check: minted + verified + exact run/candidate/source.

        A verdict minted for run A / candidate A can never authorize evidence for run B
        / candidate B, even when both cite the same underlying source.
        """
        return bool(
            self.is_verified_verdict_for(source_id=source_id)
            and self.bound_ledger_id == ledger_id
            and self.bound_source_candidate_id == source_candidate_id
        )


class OriginalSourceVerifier(Protocol):
    """Provider-neutral trusted verification dependency (interface/Protocol only).

    The default state DENIES. A verifier must independently establish the original
    document's identity, location, exact bytes and hash, tier and (where relevant)
    the claim/extract location — provider synthesis alone is never sufficient.
    It returns an UNTRUSTED :class:`SourceVerificationCandidate`; only the module can
    turn a candidate into a trusted verdict.
    """

    def verify(self, request: SourceVerificationRequest, /) -> SourceVerificationCandidate:
        ...


class _DenyingOriginalSourceVerifier:
    """Default: NO verified proof -> NO admission (fail closed)."""

    def verify(self, request: SourceVerificationRequest, /) -> SourceVerificationCandidate:
        return SourceVerificationCandidate(
            verified=False,
            reason=REASON_NO_VERIFIER,
            failure_kind=SourceFailureKind.INSUFFICIENT_PROOF,
        )


#: The shipped default verifier: denies verification.
DEFAULT_ORIGINAL_SOURCE_VERIFIER: OriginalSourceVerifier = _DenyingOriginalSourceVerifier()


def _disposition_for_failure(
    verification: OriginalSourceVerification,
) -> CandidateDisposition:
    """Deterministic failure -> disposition mapping (never policy-free guessing)."""
    kind = verification.failure_kind
    if kind is SourceFailureKind.NOT_FOUND:
        return CandidateDisposition.UNAVAILABLE
    if kind is SourceFailureKind.MISMATCH:
        return CandidateDisposition.REJECTED
    return CandidateDisposition.DEFERRED


# ---------------------------------------------------------------------------
# Durable candidate registration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RegisteredCandidate:
    source_candidate_id: str
    pointer_index: int
    reference: str
    already_registered: bool


def register_discovered_candidates(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    references: Sequence[Any],
    discovery_timestamp: str,
) -> tuple[RegisteredCandidate, ...]:
    """Durably register EVERY discovered reference as a run-scoped candidate.

    Registration precedes any admission decision, so a discovered source can never
    silently disappear (M6.0 §7.5: no source may vanish without a disposition).
    Replay is idempotent: the same (run, index, reference) resolves to the same
    candidate id and is not duplicated. A candidate id that resolves to a DIFFERENT
    identity is refused rather than silently overwritten.
    """
    record = store.load_run(ledger_id)
    if record.is_terminal:
        raise LedgerTerminalError(
            f"ledger run {ledger_id!r} is terminal; candidate registration refused"
        )
    if not isinstance(discovery_timestamp, str) or not discovery_timestamp.strip():
        raise SourceBridgeError("registration requires a non-blank discovery_timestamp")

    registered: list[RegisteredCandidate] = []
    for pointer in references:
        ref = coerce_discovered_reference(pointer)
        candidate_id = compute_source_candidate_id(
            ledger_id=ledger_id, pointer_index=ref.index, reference=ref.reference
        )
        existing = {c.source_candidate_id: c for c in record.candidates}.get(candidate_id)
        if existing is not None:
            # Idempotent replay — but NEVER a silent overwrite of a different identity.
            if existing.url_or_identifier != ref.reference:
                raise CandidateIdentityConflict(
                    f"candidate id {candidate_id!r} already resolves to a different "
                    f"reference ({existing.url_or_identifier!r} != {ref.reference!r})"
                )
            registered.append(
                RegisteredCandidate(candidate_id, ref.index, ref.reference, True)
            )
            continue
        try:
            store.register_candidate(
                ledger_id,
                source_candidate_id=candidate_id,
                url_or_identifier=ref.reference,
                discovery_timestamp=discovery_timestamp,
                original_source_verification_status=VERIFICATION_STATUS_PENDING,
                pit_eligibility=PIT_ELIGIBILITY_UNKNOWN,
                fingerprint=f"{_POINTER_INDEX_MARKER}{ref.index}",
            )
        except LedgerIdentityConflict:
            # Lost a race with a concurrent identical registration: re-read and
            # confirm identity instead of blindly trusting the failure.
            after = {c.source_candidate_id: c for c in store.load_run(ledger_id).candidates}
            settled = after.get(candidate_id)
            if settled is None or settled.url_or_identifier != ref.reference:
                raise
        registered.append(RegisteredCandidate(candidate_id, ref.index, ref.reference, False))
    return tuple(registered)


def pending_candidates(record: RunRecord) -> tuple[str, ...]:
    """Candidate ids that still lack a durable disposition (completeness check)."""
    disposed = {d.source_candidate_id for d in record.dispositions}
    return tuple(
        c.source_candidate_id for c in record.candidates
        if c.source_candidate_id not in disposed
    )


# ---------------------------------------------------------------------------
# PIT-aware selective source admission
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceAdmissionOutcome:
    """Truthful outcome of the source-admission stage for ONE candidate."""

    source_candidate_id: str
    disposition: CandidateDisposition
    reason: str
    src01_id: str | None = None
    admitted: bool = False
    reused: bool = False
    attestation_id: str | None = None
    verification: OriginalSourceVerification | None = None


def _source_exists(archive: Any, source_id: str) -> bool:
    try:
        return bool(archive.contains("SRC-01", source_id))
    except Exception:  # pragma: no cover - defensive; archive must be authoritative
        return False


def _stored_bytes_match(archive: Any, source_id: str, content_hash: str) -> bool:
    """True only when the archive's stored bytes hash equals the verified hash.

    The stored blob is the authority; a caller-supplied hash never overwrites it.
    """
    try:
        stored = archive.get_raw_blob_hash(source_id)
    except Exception:  # pragma: no cover - defensive; missing blob is a mismatch
        return False
    if stored is None:
        return False
    if stored == content_hash:
        return True
    try:
        record = archive.load("SRC-01", source_id)
    except Exception:  # pragma: no cover - defensive
        return False
    return getattr(record, "content_hash", None) == content_hash


def _sealed_eligible(archive: Any, source_id: str, as_of: str) -> bool:
    """Reuse the accepted M6.1/FD #150 SEALED rule (no second PIT authority)."""
    from qad.m6.eligibility import SealedEligibility, evaluate_sealed_source_eligibility

    import datetime as _dt

    try:
        as_of_date = _dt.date.fromisoformat(as_of[:10])
    except Exception:
        return False
    verdict = evaluate_sealed_source_eligibility(archive, source_id, as_of_date)
    return verdict is SealedEligibility.ELIGIBLE


def verify_and_admit_source(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    source_candidate_id: str,
    verifier: OriginalSourceVerifier | None = None,
    archive: Any,
    pit_context_store: Any | None = None,
) -> SourceAdmissionOutcome:
    """Independently verify ONE discovered candidate, then selectively admit it.

    Order of gates (all fail closed):

    1. the candidate must be durably registered for this exact run;
    2. independent verification must SUCCEED (default verifier DENIES);
    3. for SEALED / REPLAY_EXCEPTION runs, PIT eligibility is decided by the
       existing archive-attestation rule — a newly discovered current source can
       never be injected into a closed SEALED corpus;
    4. canonical admission happens ONLY via ``RawSourceArchive.admit_source`` with
       the exact verified bytes.

    Already-admitted identical sources are REUSED (no duplicate canonical object).
    """
    record = store.load_run(ledger_id)
    if record.is_terminal:
        raise LedgerTerminalError(
            f"ledger run {ledger_id!r} is terminal; source admission refused"
        )
    candidate = {c.source_candidate_id: c for c in record.candidates}.get(source_candidate_id)
    if candidate is None:
        raise SourceBridgeError(
            f"candidate {source_candidate_id!r} was never registered for run {ledger_id!r}"
        )
    if any(d.source_candidate_id == source_candidate_id for d in record.dispositions):
        raise SourceBridgeError(
            f"candidate {source_candidate_id!r} already has a final disposition"
        )

    resolved = verifier if verifier is not None else DEFAULT_ORIGINAL_SOURCE_VERIFIER
    request = SourceVerificationRequest(
        ledger_id=record.ledger_id,
        research_run_id=record.research_run_id,
        request_id=record.request_id,
        source_candidate_id=source_candidate_id,
        pointer_index=_pointer_index_for(record, source_candidate_id),
        reference=candidate.url_or_identifier,
        claimed_title=None,
        provider_claim_original_source_verified=None,
    )
    candidate_verdict = resolved.verify(request)
    if not isinstance(candidate_verdict, SourceVerificationCandidate):
        raise SourceBridgeError(
            "an original-source verifier must return a SourceVerificationCandidate"
        )

    def _mint(v: SourceVerificationCandidate) -> OriginalSourceVerification:
        """Closure-scoped minter — deliberately NOT module-addressable.

        There is no importable path that mints a trusted verdict from bare caller
        strings, so a trusted verdict can only arise from this verification call.
        """
        return OriginalSourceVerification(
            verified=v.verified, reason=v.reason, failure_kind=v.failure_kind,
            source_id=v.source_id, source_tier=v.source_tier, source_type=v.source_type,
            content_hash=v.content_hash, raw_bytes=v.raw_bytes, location=v.location,
            publication_date=v.publication_date, retrieval_date=v.retrieval_date,
            title=v.title, mismatches=v.mismatches, _minted=_MINT_TOKEN,
            bound_ledger_id=record.ledger_id,
            bound_source_candidate_id=source_candidate_id,
        )

    verification = _mint(candidate_verdict)
    verification.assert_attested_for(
        ledger_id=ledger_id, source_candidate_id=source_candidate_id
    )

    if not verification.verified:
        return SourceAdmissionOutcome(
            source_candidate_id=source_candidate_id,
            disposition=_disposition_for_failure(verification),
            reason=verification.reason,
            verification=verification,
        )

    assert verification.source_id is not None  # enforced by the verification type
    assert verification.content_hash is not None
    assert verification.raw_bytes is not None
    source_id = verification.source_id

    mode = record.pit_mode
    already = _source_exists(archive, source_id)

    # A source that already exists must MATCH the independently verified bytes.
    # Same id + different content is an identity conflict: never a silent reuse and
    # never an overwrite of immutable canonical bytes.
    if already and not _stored_bytes_match(archive, source_id, verification.content_hash):
        return SourceAdmissionOutcome(
            source_candidate_id=source_candidate_id,
            disposition=CandidateDisposition.REJECTED,
            reason=REASON_IDENTITY_CONFLICT,
            src01_id=source_id,
        )

    if mode == _SEALED:
        if not already:
            # A discovered CURRENT source is post-AS_OF by construction: it can
            # never be injected into a closed SEALED corpus.
            return SourceAdmissionOutcome(
                source_candidate_id=source_candidate_id,
                disposition=CandidateDisposition.DEFERRED,
                reason=REASON_SEALED_NOT_ELIGIBLE,
            )
        if not _sealed_eligible(archive, source_id, record.as_of):
            return SourceAdmissionOutcome(
                source_candidate_id=source_candidate_id,
                disposition=CandidateDisposition.UNAVAILABLE,
                reason=REASON_SEALED_NOT_ELIGIBLE,
                src01_id=source_id,
            )
        return SourceAdmissionOutcome(
            source_candidate_id=source_candidate_id,
            disposition=CandidateDisposition.IMPORTED,
            reason=REASON_REUSED,
            src01_id=source_id,
            reused=True,
            verification=verification,
        )

    if mode == _REPLAY_EXCEPTION:
        # The EXISTING explicit authorization/provenance boundary is REQUIRED —
        # verified against the authoritative PITC-01, never invented here. This
        # applies to ALREADY-ADMITTED sources too (round-10 finding 3).
        if not _replay_exception_authorized(record, pit_context_store=pit_context_store):
            return SourceAdmissionOutcome(
                source_candidate_id=source_candidate_id,
                disposition=CandidateDisposition.DEFERRED,
                reason=REASON_REPLAY_EXCEPTION_BOUNDARY,
                verification=verification,
            )
        if already:
            if not _sealed_eligible(archive, source_id, record.as_of):
                return SourceAdmissionOutcome(
                    source_candidate_id=source_candidate_id,
                    disposition=CandidateDisposition.UNAVAILABLE,
                    reason=REASON_SEALED_NOT_ELIGIBLE,
                    src01_id=source_id,
                    verification=verification,
                )
            return SourceAdmissionOutcome(
                source_candidate_id=source_candidate_id,
                disposition=CandidateDisposition.IMPORTED,
                reason=REASON_REUSED,
                src01_id=source_id,
                reused=True,
                verification=verification,
            )
        # authorized replay of a not-yet-admitted source: the exception is what
        # authorizes using the post-AS_OF bytes, so admission proceeds below through
        # the authoritative archive boundary only.

    # LIVE_CASE_UPDATE (and an AUTHORIZED replay of a new source)
    if already:
        return SourceAdmissionOutcome(
            source_candidate_id=source_candidate_id,
            disposition=CandidateDisposition.IMPORTED,
            reason=REASON_REUSED,
            src01_id=source_id,
            reused=True,
            verification=verification,
        )

    source_record = _build_source_record(verification)
    if source_record is None:
        return SourceAdmissionOutcome(
            source_candidate_id=source_candidate_id,
            disposition=CandidateDisposition.REJECTED,
            reason=REASON_SOURCE_MISMATCH,
        )
    try:
        archive.admit_source(source_record, verification.raw_bytes)
    except IntegrityConflict:
        # Same source id, different payload: never overwrite immutable bytes.
        raise
    except Exception:
        raise

    attestation_id: str | None = None
    try:
        attestation = archive.get_admission_attestation(source_id)
        attestation_id = getattr(attestation, "attestation_id", None)
    except Exception:
        attestation_id = None

    return SourceAdmissionOutcome(
        source_candidate_id=source_candidate_id,
        disposition=CandidateDisposition.IMPORTED,
        reason=REASON_ADMITTED,
        src01_id=source_id,
        admitted=True,
        attestation_id=attestation_id,
        verification=verification,
    )


#: Operational marker persisted in the ledger candidate's ``fingerprint`` column so the
#: citation index is recoverable EXACTLY (no arbitrary search bound). Operational,
#: non-canonical metadata on a non-canonical ledger — not a schema change.
_POINTER_INDEX_MARKER = "pointer_index="


def _pointer_index_for(record: RunRecord, source_candidate_id: str) -> int:
    """Recover the citation index exactly as persisted at registration."""
    candidate = {c.source_candidate_id: c for c in record.candidates}.get(
        source_candidate_id
    )
    if candidate is None:
        return 0
    fingerprint = candidate.fingerprint or ""
    if fingerprint.startswith(_POINTER_INDEX_MARKER):
        try:
            return int(fingerprint[len(_POINTER_INDEX_MARKER):])
        except ValueError:
            return 0
    return 0


def _replay_exception_authorized(
    record: RunRecord, *, pit_context_store: Any | None,
) -> bool:
    """Reuse the EXISTING REPLAY_EXCEPTION rule — no second PIT authority.

    Requires the AUTHORITATIVE PITC-01 (resolved by the run's ``pit_context_id``) to be
    in REPLAY_EXCEPTION mode, to carry the Founder authorization role, and to have a
    non-empty ``exception_reason``. Any missing surface or mismatch fails closed — the
    same rule the accepted runtime enforces (``PITEnforcementService``/FD #148).
    """
    if pit_context_store is None:
        return False
    try:
        if not pit_context_store.contains("PITC-01", record.pit_context_id):
            return False
        pitc = pit_context_store.load("PITC-01", record.pit_context_id)
    except Exception:
        return False
    return bool(
        getattr(pitc, "mode", None) == _REPLAY_EXCEPTION
        and getattr(pitc, "created_by", None) == FOUNDER_ROLE_TOKEN
        and bool(getattr(pitc, "exception_reason", None))
    )


def _build_source_record(
    verification: OriginalSourceVerification,
) -> SourceRecord | None:
    """Construct the SRC-01 metadata for a VERIFIED original document.

    A source-tier/source-type that the canonical vocabulary cannot represent is a
    mismatch (REJECTED), not a silent coercion.
    """
    try:
        tier = SourceRecordSource_tier(verification.source_tier)
    except ValueError:
        return None
    try:
        source_type = SourceRecordSource_type(verification.source_type)
    except ValueError:
        return None
    return SourceRecord(
        source_id=verification.source_id,
        content_hash=verification.content_hash,
        retrieval_date=verification.retrieval_date,
        source_tier=tier,
        source_type=source_type,
        url_or_identifier=verification.location or "archive://verified-original",
        title=verification.title,
        publication_date=verification.publication_date,
    )


# ---------------------------------------------------------------------------
# Canonical evidence admission (reuse the existing gate)
# ---------------------------------------------------------------------------


def build_evidence_admission(
    *,
    evidence: EvidenceRecord,
    verification: OriginalSourceVerification,
    admission_id: str,
    admission_timestamp: str,
    admitting_role: str,
    admission_method: EvidenceAdmissionRecordAdmission_method | str,
    validation_method: str,
    contradiction_check: str | None = None,
    pit_verified: str | None = None,
    source_as_of: str | None = None,
) -> EvidenceAdmissionRecord:
    """Build the EAR-01 record, deriving ``original_source_verified`` HONESTLY.

    The authoritative EvidenceRegistry AI-method gate requires the exact lowercase
    string ``"true"`` for AI_EXTRACTION / AI_SYNTHESIS. This helper sets it ONLY
    when independent verification actually SUCCEEDED for THIS evidence's source;
    otherwise it is left unset, so the existing gate rejects the admission
    (fail closed). The value is never synthesized.
    """
    if isinstance(admission_method, EvidenceAdmissionRecordAdmission_method):
        method_value = admission_method.value
    else:
        method_value = str(admission_method)

    # ONLY a minted VERIFIED verdict bound to this exact evidence source can set the
    # canonical truth value; a forged, unverified, candidate-shaped or cross-source
    # verdict never can (fail closed).
    if isinstance(verification, OriginalSourceVerification):
        verified_here = verification.is_verified_verdict_for(source_id=evidence.source_id)
    else:
        verified_here = False
    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        admission_method=EvidenceAdmissionRecordAdmission_method(method_value),
        admission_timestamp=admission_timestamp,
        admitting_role=admitting_role,
        evidence_id=evidence.evidence_id,
        source_tier_check=evidence.source_tier,
        validation_method=validation_method,
        contradiction_check=contradiction_check,
        original_source_verified=(
            ORIGINAL_SOURCE_VERIFIED_TRUE if verified_here else None
        ),
        pit_verified=pit_verified,
        source_as_of=source_as_of or evidence.as_of,
        validation_notes=(
            "original source independently verified by the M6.6 bridge"
            if verified_here
            else "NOT independently verified — AI admission must be rejected"
        ),
    )


def admit_candidate_evidence(
    registry: Any,
    *,
    evidence: EvidenceRecord,
    admission: EvidenceAdmissionRecord,
    ledger_id: str,
    source_candidate_id: str,
    verified_source_id: str,
    verification: OriginalSourceVerification | None = None,
):
    """Admit EV-01 + EAR-01 through the EXISTING authoritative gate only.

    PROOF-BOUND: the bridge re-derives the truth value at this boundary. A caller-authored
    EAR is accepted ONLY when it does not assert verification, or when it asserts the
    canonical ``"true"`` AND the bridge's OWN minted verdict authorizes exactly this
    run + candidate + source. Everything else fails closed BEFORE any canonical write —
    an ordinary caller cannot hand-build a verified EAR, and cannot admit evidence for a
    source that was not the one independently verified and admitted for this candidate.
    """
    if admission.evidence_id != evidence.evidence_id:
        raise SourceBridgeError(
            "EAR-01.evidence_id must equal EV-01.evidence_id "
            f"({admission.evidence_id!r} != {evidence.evidence_id!r})"
        )
    if evidence.source_id != verified_source_id:
        raise SourceBridgeError(
            f"evidence source {evidence.source_id!r} is not the source independently "
            f"verified and admitted for this candidate ({verified_source_id!r})"
        )
    claimed = getattr(admission, "original_source_verified", None)
    if claimed is not None and claimed != ORIGINAL_SOURCE_VERIFIED_TRUE:
        raise SourceBridgeError(
            "EAR-01.original_source_verified must be the canonical "
            f"{ORIGINAL_SOURCE_VERIFIED_TRUE!r} or unset, got {claimed!r}"
        )
    if claimed is not None:
        authorized = bool(
            isinstance(verification, OriginalSourceVerification)
            and verification.authorizes_evidence_for(
                ledger_id=ledger_id,
                source_candidate_id=source_candidate_id,
                source_id=evidence.source_id,
            )
        )
        if not authorized:
            raise SourceBridgeError(
                "an EAR-01 asserting original_source_verified may be admitted ONLY when "
                "the bridge's own verdict verifies exactly this run/candidate/source"
            )
    return registry.admit_evidence(evidence, admission)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateOutcome:
    source_candidate_id: str
    pointer_index: int
    reference: str
    disposition: CandidateDisposition
    reason: str
    src01_id: str | None = None
    evidence_ids: tuple[str, ...] = ()
    ear_ids: tuple[str, ...] = ()
    evidence_admission_error: str | None = None


@dataclass
class BridgeOutcome:
    ledger_id: str
    outcomes: list[CandidateOutcome] = field(default_factory=list)

    @property
    def pending(self) -> tuple[str, ...]:
        return tuple(
            o.source_candidate_id for o in self.outcomes
            if o.disposition is CandidateDisposition.DEFERRED
        )


def process_discovered_sources(
    store: DeepResearchRunLedgerStore,
    *,
    ledger_id: str,
    references: Sequence[Any],
    discovery_timestamp: str,
    archive: Any,
    verifier: OriginalSourceVerifier | None = None,
    registry: Any | None = None,
    evidence_builder: Any | None = None,
    pit_context_store: Any | None = None,
) -> BridgeOutcome:
    """Full bounded pipeline for the run's discovered sources.

    register -> verify -> selectively admit source -> optionally admit evidence
    -> durably dispose. Never terminalizes the run and never writes SUCCESS.

    ``evidence_builder`` (optional) is a callable
    ``(candidate_id, src01_id, verification) -> tuple[EvidenceRecord, EvidenceAdmissionRecord] | None``
    supplied by the caller (deterministic fixtures in tests). When omitted, the
    candidate is disposed IMPORTED with the source admission only, and the
    outcome truthfully reports that no canonical evidence was admitted.
    """
    registered = register_discovered_candidates(
        store, ledger_id=ledger_id, references=references,
        discovery_timestamp=discovery_timestamp,
    )
    # One outcome row per UNIQUE candidate identity: duplicate input is not a duplicate
    # candidate (durable integrity already guarantees one candidate/disposition).
    unique_registered: list[RegisteredCandidate] = []
    _seen_ids: set[str] = set()
    for reg in registered:
        if reg.source_candidate_id in _seen_ids:
            continue
        _seen_ids.add(reg.source_candidate_id)
        unique_registered.append(reg)
    registered = tuple(unique_registered)
    outcome = BridgeOutcome(ledger_id=ledger_id)

    for reg in registered:
        # SAFE RE-ENTRY: a candidate that already holds its ONE final disposition is
        # already settled. Re-processing reports the committed disposition from the
        # durable ledger instead of re-admitting, re-registering or erroring — and
        # never rewrites committed canonical state.
        settled = {
            d.source_candidate_id: d
            for d in store.load_run(ledger_id).dispositions
        }.get(reg.source_candidate_id)
        if settled is not None:
            outcome.outcomes.append(
                CandidateOutcome(
                    source_candidate_id=reg.source_candidate_id,
                    pointer_index=reg.pointer_index,
                    reference=reg.reference,
                    disposition=settled.disposition,
                    reason=settled.reason,
                    src01_id=settled.src01_id,
                    evidence_ids=tuple(settled.evidence_ids),
                    ear_ids=tuple(settled.ear_ids),
                )
            )
            continue

        admission = verify_and_admit_source(
            store, ledger_id=ledger_id, source_candidate_id=reg.source_candidate_id,
            verifier=verifier, archive=archive, pit_context_store=pit_context_store,
        )
        evidence_ids: tuple[str, ...] = ()
        ear_ids: tuple[str, ...] = ()
        evidence_error: str | None = None

        if admission.disposition is CandidateDisposition.IMPORTED and registry is not None \
                and evidence_builder is not None:
            try:
                built = evidence_builder(
                    reg.source_candidate_id, admission.src01_id, admission.verification
                )
                if built is not None:
                    ev, ear = built
                    admit_candidate_evidence(
                        registry, evidence=ev, admission=ear,
                        ledger_id=ledger_id,
                        source_candidate_id=reg.source_candidate_id,
                        verified_source_id=admission.src01_id,
                        verification=admission.verification,
                    )
                    evidence_ids = (ev.evidence_id,)
                    ear_ids = (ear.admission_id,)
            except Exception as exc:  # cross-store boundary: preserve committed state
                evidence_error = f"{type(exc).__name__}: {exc}"

        reason = admission.reason
        if evidence_error is not None:
            # Truthful partial outcome: the SOURCE is imported; canonical evidence
            # was NOT admitted. Never claim otherwise.
            reason = (
                f"{admission.reason}; canonical evidence admission FAILED "
                f"({evidence_error}) — no canonical evidence was admitted"
            )
        elif admission.disposition is CandidateDisposition.IMPORTED \
                and not evidence_ids and registry is not None:
            reason = f"{admission.reason}; no canonical evidence admitted"

        store.dispose_candidate(
            ledger_id,
            reg.source_candidate_id,
            disposition=admission.disposition,
            reason=reason,
            src01_id=admission.src01_id,
            evidence_ids=evidence_ids,
            ear_ids=ear_ids,
        )
        outcome.outcomes.append(
            CandidateOutcome(
                source_candidate_id=reg.source_candidate_id,
                pointer_index=reg.pointer_index,
                reference=reg.reference,
                disposition=admission.disposition,
                reason=reason,
                src01_id=admission.src01_id,
                evidence_ids=evidence_ids,
                ear_ids=ear_ids,
                evidence_admission_error=evidence_error,
            )
        )
    return outcome


__all__ = [
    "BridgeOutcome",
    "CandidateIdentityConflict",
    "CandidateOutcome",
    "DEFAULT_ORIGINAL_SOURCE_VERIFIER",
    "DiscoveredSourceReference",
    "ORIGINAL_SOURCE_VERIFIED_TRUE",
    "OriginalSourceVerification",
    "OriginalSourceVerifier",
    "SourceAdmissionOutcome",
    "SourceBridgeError",
    "SourceFailureKind",
    "SourceVerificationCandidate",
    "SourceVerificationRequest",
    "admit_candidate_evidence",
    "build_evidence_admission",
    "coerce_discovered_reference",
    "compute_source_candidate_id",
    "pending_candidates",
    "process_discovered_sources",
    "register_discovered_candidates",
    "verify_and_admit_source",
]
