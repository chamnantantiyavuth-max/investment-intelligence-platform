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

Process trust boundary (explicit)
---------------------------------
M6.4 CONSUMES, and does not build, the SEALED snapshot. Every request is BOUND to
the authoritative snapshot it was derived from: the envelope keeps the snapshot
reference and re-verifies (a) that the snapshot is internally self-consistent
(M6.0 identity recomputed from its own fields, plus per-source byte/hash/length
integrity) and (b) that every derived field (case_id, case_version, pit_mode,
as_of, input_snapshot_hash, snapshot_id, pit_context_id, corpus) agrees with that
snapshot. So a direct construction cannot inject SEALED authority, even with a
recomputed payload hash. A fully consistent in-process forgery by code that can
already import this package is outside the process trust boundary — capability
isolation is not provided by a plain Python dataclass, exactly as the accepted
M6.2/M6.3 clusters already document.

Trusted proof-verification seam (FD #152)
-----------------------------------------
``SUCCESS`` stays representable and testable here, but a positive
enforcement/isolation CLAIM — and equally a non-empty evidence-reference string —
is NOT proof. ``SUCCESS`` is constructed ONLY after BOTH the closed-corpus
enforcement proof AND the request-isolation proof have been VERIFIED through a
trusted, provider-neutral seam (:class:`DeepResearchProofResolver`): an injected
orchestration dependency that returns a structured :class:`ProofVerification`
bound to the EXACT run (request_id, research_run_id, ledger_id, provider_surface,
input_snapshot_hash, proof reference, proof kind), so a proof obtained for one run
can never authorize another run's ``SUCCESS``. The verified outcome is minted into
a private immutable attestation, so the direct ``DeepResearchResult(...)`` path
cannot authorize ``SUCCESS`` either. The default resolver DENIES (M6.4 ships NO
production-success resolver), so a real ``SUCCESS`` is impossible inside M6.4
alone — that is expected; the test boundary may inject a deterministic stub purely
to exercise the seam. M6.4 defines the INTERFACE only: the real proof-producing /
proof-resolving implementation (Gemini, Notebook transport, browser automation,
provider proof collection) belongs to M6.7/M6.8.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from pydantic import BaseModel

from qad.m6.ledger import (
    DeepResearchRunLedgerStore,
    LedgerError,
    validate_rrm_deep_research_runs,
)
from qad.m6.eligibility import SealedEligibility
from qad.m6.snapshot import (
    PROVIDER_CANNOT_ENFORCE_SEALED_INPUT,
    SEALED_PIT_MODE,
    SealedInputSnapshot,
    _compute_input_snapshot_hash,
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
    "NO_VERIFIED_PROOF_RESOLVER",
    "ResearchContractError",
    "RequestAuthorityViolation",
    "ResearchRequestError",
    "ResearchResultError",
    "ResearchResultStatus",
    "ClosedCorpusEnforcement",
    "IsolationVerification",
    "ProofKind",
    "ProofVerificationRequest",
    "ProofVerification",
    "DeepResearchProofResolver",
    "DEFAULT_PROOF_RESOLVER",
    "ProviderConfiguration",
    "SourceCorpusDescriptor",
    "DeepResearchRequest",
    "SourcePointer",
    "DeepResearchResult",
    "build_deep_research_request",
    "build_deep_research_result",
    "compute_result_sha256",
    "compute_citation_list_sha256",
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

    ``NOT_VERIFIED`` is the default. ``ENFORCED`` is a POSITIVE CLAIM that may
    only be carried once the trusted proof seam (FD #152) has verified the
    closed-corpus enforcement proof for the exact run; ``CANNOT_ENFORCE`` forces
    ``PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`` (fail closed — never a fabricated
    success).
    """

    NOT_VERIFIED = "NOT_VERIFIED"
    ENFORCED = "ENFORCED"
    CANNOT_ENFORCE = "CANNOT_ENFORCE"


class IsolationVerification(str, Enum):
    """Request-isolation proof state carried on a result (M6.0 §11.2 R7).

    ``NOT_VERIFIED`` is the default. ``VERIFIED`` is a POSITIVE CLAIM that may
    only be carried once the trusted proof seam (FD #152) has verified the
    request-isolation proof for the exact run; ``UNVERIFIED`` forces
    ``REQUEST_ISOLATION_UNVERIFIED`` (fail closed).
    """

    NOT_VERIFIED = "NOT_VERIFIED"
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"


# ---------------------------------------------------------------------------
# Trusted proof-verification seam (FD #152) — INTERFACE ONLY, non-canonical
# ---------------------------------------------------------------------------


#: Failure reason the fail-closed default resolver reports: M6.4 ships no
#: production-success resolver, so verification is denied.
NO_VERIFIED_PROOF_RESOLVER = "NO_VERIFIED_PROOF_RESOLVER_CONFIGURED"


class ProofKind(str, Enum):
    """The two independent proofs ``SUCCESS`` requires (M6.0 §5 / §11.2 R7)."""

    CLOSED_CORPUS_ENFORCEMENT = "CLOSED_CORPUS_ENFORCEMENT"
    REQUEST_ISOLATION = "REQUEST_ISOLATION"


@dataclass(frozen=True)
class ProofVerificationRequest:
    """Immutable verification context DERIVED from the authoritative request.

    The resolver is asked to verify ONE proof kind, bound to the EXACT logical
    execution context — so a proof obtained for one run can never authorize
    another run's ``SUCCESS``. The context is built from the bound
    :class:`DeepResearchRequest`, never from duplicated caller strings.
    """

    proof_kind: ProofKind
    request_id: str
    research_run_id: str
    ledger_id: str
    provider_surface: str
    input_snapshot_hash: str
    #: An evidence reference is an IDENTIFIER the resolver must resolve and
    #: verify — it is never proof by itself.
    evidence_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.proof_kind, ProofKind):
            raise ResearchResultError("proof_kind must be a ProofKind")
        for name in (
            "request_id", "research_run_id", "ledger_id", "provider_surface",
            "input_snapshot_hash", "evidence_ref",
        ):
            if not _has_visible_text(getattr(self, name)):
                raise ResearchResultError(f"{name} must be a non-blank string")


@dataclass(frozen=True)
class ProofVerification:
    """Structured immutable verification RESULT — deliberately not a naked bool.

    The outcome, the resolved evidence reference and the bound execution identity
    travel together, so the caller can prove the verification applies to the exact
    run being authorized. NON-CANONICAL: this is not SRC-01 / EV-01 / canonical
    provenance and it adds no canonical schema.
    """

    proof_kind: ProofKind
    verified: bool
    request_id: str
    research_run_id: str
    ledger_id: str
    provider_surface: str
    input_snapshot_hash: str
    evidence_ref: str | None = None
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.proof_kind, ProofKind):
            raise ResearchResultError("proof_kind must be a ProofKind")
        if not isinstance(self.verified, bool):
            raise ResearchResultError("verified must be a bool")
        for name in (
            "request_id", "research_run_id", "ledger_id", "provider_surface",
            "input_snapshot_hash",
        ):
            if not _has_visible_text(getattr(self, name)):
                raise ResearchResultError(f"{name} must be a non-blank string")
        if self.verified:
            if not _has_visible_text(self.evidence_ref):
                raise ResearchResultError(
                    "a verified proof must carry the resolved evidence reference"
                )
            if self.failure_reason is not None:
                raise ResearchResultError(
                    "a verified proof must not carry a failure_reason"
                )
        elif not _has_visible_text(self.failure_reason):
            raise ResearchResultError(
                "an unverified proof requires a non-blank failure_reason "
                "(failures are never a silent blank)"
            )


@runtime_checkable
class DeepResearchProofResolver(Protocol):
    """Trusted, provider-neutral proof-verification seam (M6.4 INTERFACE ONLY).

    The resolver is a trusted ORCHESTRATION DEPENDENCY — not provider-supplied
    free-form data, and never stored on the result. It MUST independently verify
    the proof (never merely test ``bool(evidence_ref)`` / ``evidence_ref is not
    empty``) and MUST echo the exact bound execution identity in its
    :class:`ProofVerification`. The real implementation arrives in M6.7/M6.8.
    """

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        """Verify ONE proof kind for the exact run described by ``context``."""
        ...


class _DenyAllProofResolver:
    """Fail-closed default: NO VERIFIED PROOF -> NO ``SUCCESS``."""

    __slots__ = ()

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        return ProofVerification(
            proof_kind=context.proof_kind,
            verified=False,
            request_id=context.request_id,
            research_run_id=context.research_run_id,
            ledger_id=context.ledger_id,
            provider_surface=context.provider_surface,
            input_snapshot_hash=context.input_snapshot_hash,
            evidence_ref=None,
            failure_reason=NO_VERIFIED_PROOF_RESOLVER,
        )


#: M6.4 ships NO production-success resolver: absent an explicitly injected
#: resolver, verification is DENIED (fail closed).
DEFAULT_PROOF_RESOLVER: DeepResearchProofResolver = _DenyAllProofResolver()


def _make_proof_attestation_seam():
    """Create the guarded verified-proof attestation type and its minter.

    The attestation guard is captured in a CLOSURE — there is deliberately no
    module-level token attribute, so the guarded minting path cannot be reached by
    a name import (``from ... import _ATTESTATION_TOKEN``). Only
    ``_mint_verified_proof_attestation`` — called from the trusted verification
    path — can produce an attestation.

    BOUNDED MECHANISM — NOT a security guarantee. Pure Python cannot make an
    object resistant to arbitrary same-process introspection, ``object.__new__``,
    ``object.__setattr__`` or monkeypatching of module internals, and M6.4 does NOT
    claim cryptographic or process capability isolation. The accepted M6.2/M6.3
    IN-PROCESS trust boundary stands unchanged (FD #152 §7): this mechanism closes
    the ordinary library-API construction paths, while hostile in-process code
    remains outside the trust boundary. Consumers therefore re-check a SUCCESS
    result at the consumption boundary (``assert_proof_verified``), which is what
    catches an artifact that never came through this path.
    """
    guard = object()

    class _VerifiedProofAttestation:
        """Private immutable capability minted ONLY by the trusted verification path.

        A ``SUCCESS`` result must carry one, and it must bind that result's exact
        identity. The type is private and its constructor is guard-protected, so
        the direct ``DeepResearchResult(...)`` path cannot fabricate a ``SUCCESS``.
        """

        __slots__ = (
            "request_id",
            "research_run_id",
            "ledger_id",
            "provider_surface",
            "input_snapshot_hash",
            "closed_corpus_evidence_ref",
            "isolation_evidence_ref",
            "result_sha256",
            "citation_list_sha256",
        )

        def __init__(
            self,
            *,
            _guard: object,
            request_id: str,
            research_run_id: str,
            ledger_id: str,
            provider_surface: str,
            input_snapshot_hash: str,
            closed_corpus_evidence_ref: str,
            isolation_evidence_ref: str,
            result_sha256: str,
            citation_list_sha256: str,
        ) -> None:
            if _guard is not guard:
                raise ResearchResultError(
                    "a verified-proof attestation may only be created by the M6.4 "
                    "trusted proof-verification path"
                )
            object.__setattr__(self, "request_id", request_id)
            object.__setattr__(self, "research_run_id", research_run_id)
            object.__setattr__(self, "ledger_id", ledger_id)
            object.__setattr__(self, "provider_surface", provider_surface)
            object.__setattr__(
                self, "input_snapshot_hash", input_snapshot_hash
            )
            object.__setattr__(
                self, "closed_corpus_evidence_ref", closed_corpus_evidence_ref
            )
            object.__setattr__(
                self, "isolation_evidence_ref", isolation_evidence_ref
            )
            object.__setattr__(self, "result_sha256", result_sha256)
            object.__setattr__(self, "citation_list_sha256", citation_list_sha256)

        def __setattr__(self, name: str, value: Any) -> None:
            raise AttributeError("a verified-proof attestation is immutable")

        def __delattr__(self, name: str) -> None:
            raise AttributeError("a verified-proof attestation is immutable")

    def _mint_verified_proof_attestation(
        *,
        request_id: str,
        research_run_id: str,
        ledger_id: str,
        provider_surface: str,
        input_snapshot_hash: str,
        closed_corpus_evidence_ref: str,
        isolation_evidence_ref: str,
        result_sha256: str,
        citation_list_sha256: str,
    ) -> _VerifiedProofAttestation:
        """Mint the capability.

        Closure-scoped on purpose: it is NOT bound as a module attribute, so it
        cannot be imported or called by name. The only module-visible object that
        can reach it is ``_verify_success_proofs`` below, which requires the
        authoritative request AND a resolver that verifies BOTH proofs for the
        exact run.
        """
        return _VerifiedProofAttestation(
            _guard=guard,
            request_id=request_id,
            research_run_id=research_run_id,
            ledger_id=ledger_id,
            provider_surface=provider_surface,
            input_snapshot_hash=input_snapshot_hash,
            closed_corpus_evidence_ref=closed_corpus_evidence_ref,
            isolation_evidence_ref=isolation_evidence_ref,
            result_sha256=result_sha256,
            citation_list_sha256=citation_list_sha256,
        )

    def _verify_success_proofs(
        *,
        request: "DeepResearchRequest",
        proof_resolver: "DeepResearchProofResolver | None",
        corpus_evidence_ref: str | None,
        isolation_evidence_ref: str | None,
        result_sha256: str,
        citation_list_sha256: str,
    ) -> _VerifiedProofAttestation:
        """Run the trusted seam for BOTH proofs and mint the attestation.

        Fail-closed: a missing/blank evidence reference, a missing resolver (the
        default DENIES), a resolver that verifies only one proof, or a verification
        that is not bound to the exact run all refuse ``SUCCESS``. This is the ONLY
        path that reaches the closure-scoped minter.
        """
        if not _has_visible_text(corpus_evidence_ref):
            raise ResearchResultError(
                "SUCCESS requires a non-blank closed_corpus_evidence_ref — an "
                "identifier the trusted resolver must resolve and verify (a string "
                "is not proof)"
            )
        if not _has_visible_text(isolation_evidence_ref):
            raise ResearchResultError(
                "SUCCESS requires a non-blank isolation_evidence_ref — an identifier "
                "the trusted resolver must resolve and verify (a string is not proof)"
            )
        resolver = DEFAULT_PROOF_RESOLVER if proof_resolver is None else proof_resolver
        if not callable(getattr(resolver, "verify_proof", None)):
            raise ResearchResultError(
                "proof_resolver must implement verify_proof(context) -> ProofVerification"
            )
        contexts = (
            _proof_context_from_request(
                request, ProofKind.CLOSED_CORPUS_ENFORCEMENT, corpus_evidence_ref
            ),
            _proof_context_from_request(
                request, ProofKind.REQUEST_ISOLATION, isolation_evidence_ref
            ),
        )
        resolved_refs: list[str] = []
        for context in contexts:
            verification = _invoke_proof_resolver(resolver, context)
            mismatch = _verification_binding_mismatch(context, verification)
            if mismatch is not None:
                raise ResearchResultError(
                    "SUCCESS refused: the resolver returned a proof that is not bound "
                    f"to the exact run being authorized "
                    f"({context.proof_kind.value} — {mismatch})"
                )
            if verification.verified is not True:
                raise ResearchResultError(
                    f"SUCCESS refused: the trusted proof resolver did not verify "
                    f"{context.proof_kind.value} ({verification.failure_reason})"
                )
            resolved_refs.append(verification.evidence_ref)  # type: ignore[arg-type]
        return _mint_verified_proof_attestation(
            request_id=request.request_id,
            research_run_id=request.research_run_id,
            ledger_id=request.ledger_id,
            provider_surface=request.provider.provider_surface,
            input_snapshot_hash=request.input_snapshot_hash,
            closed_corpus_evidence_ref=resolved_refs[0],
            isolation_evidence_ref=resolved_refs[1],
            result_sha256=result_sha256,
            citation_list_sha256=citation_list_sha256,
        )

    return _VerifiedProofAttestation, _verify_success_proofs


# Only the private attestation TYPE and the full verification entry point are
# module-visible. The minting callable stays inside the closure — there is no
# module-level mint function a caller could invoke with bare identity strings.
(
    _VerifiedProofAttestation,
    _verify_success_proofs,
) = _make_proof_attestation_seam()


#: The fields a verified-proof attestation must bind to the result. Round 16
#: (reviewer finding): the validated digests are bound TOO, so replacing the
#: result bytes AND the matching result_sha256 after construction is detected at
#: the consumption boundary (the attested digest no longer matches).
_ATTESTED_IDENTITY_FIELDS = (
    "request_id", "research_run_id", "ledger_id", "provider_surface",
    "input_snapshot_hash", "closed_corpus_evidence_ref", "isolation_evidence_ref",
    "result_sha256", "citation_list_sha256",
)


def _attestation_mismatch(
    attestation: _VerifiedProofAttestation, result: "DeepResearchResult"
) -> str | None:
    """Return the first identity field the attestation does not bind, else None."""
    for name in _ATTESTED_IDENTITY_FIELDS:
        if getattr(attestation, name) != getattr(result, name):
            return (
                f"{name}: result carries {getattr(result, name)!r} but the verified "
                f"proof binds {getattr(attestation, name)!r}"
            )
    return None


def _proof_context_from_request(
    request: "DeepResearchRequest", proof_kind: ProofKind, evidence_ref: str
) -> ProofVerificationRequest:
    """Build the immutable verification context from the authoritative request."""
    return ProofVerificationRequest(
        proof_kind=proof_kind,
        request_id=request.request_id,
        research_run_id=request.research_run_id,
        ledger_id=request.ledger_id,
        provider_surface=request.provider.provider_surface,
        input_snapshot_hash=request.input_snapshot_hash,
        evidence_ref=evidence_ref,
    )


def _verification_binding_mismatch(
    context: ProofVerificationRequest, verification: ProofVerification
) -> str | None:
    """Return the first field where the returned proof is not bound, else None.

    This is what blocks proof replay: a verification produced for Request A (or
    for a different proof kind / ledger / snapshot) does not match the context of
    the run currently being authorized.
    """
    for name in (
        "proof_kind", "request_id", "research_run_id", "ledger_id",
        "provider_surface", "input_snapshot_hash", "evidence_ref",
    ):
        if getattr(verification, name) != getattr(context, name):
            return (
                f"{name}: verification says {getattr(verification, name)!r}, the run "
                f"requires {getattr(context, name)!r}"
            )
    return None


def _invoke_proof_resolver(
    resolver: DeepResearchProofResolver, context: ProofVerificationRequest
) -> ProofVerification:
    """Call the resolver; any failure or non-ProofVerification return fails closed."""
    try:
        verification = resolver.verify_proof(context)
    except ResearchContractError:
        raise
    except Exception as exc:  # noqa: BLE001 — a failing resolver must fail closed
        raise ResearchResultError(
            f"the proof resolver raised {type(exc).__name__} while verifying "
            f"{context.proof_kind.value}; SUCCESS refused (fail closed)"
        ) from exc
    if not isinstance(verification, ProofVerification):
        raise ResearchResultError(
            "the proof resolver must return a ProofVerification (a bare bool or any "
            "other object is not proof)"
        )
    return verification


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

    def __post_init__(self) -> None:
        if not _has_visible_text(self.provider_surface):
            raise ResearchRequestError("provider_surface must be a non-blank string")
        if self.capability != S10_CAPABILITY:
            raise ResearchRequestError(
                f"provider configuration capability must be {S10_CAPABILITY!r}"
            )
        if self.closed_corpus_required is not True:
            raise ResearchRequestError("provider closed_corpus_required must be True")
        if self.request_isolation_required is not True:
            raise ResearchRequestError("provider request_isolation_required must be True")
        if self.timeout_seconds is not None and (
            not isinstance(self.timeout_seconds, int)
            or isinstance(self.timeout_seconds, bool)
            or self.timeout_seconds <= 0
        ):
            raise ResearchRequestError(
                "timeout_seconds must be a positive integer or None"
            )


@dataclass(frozen=True)
class SourceCorpusDescriptor:
    """The exact approved corpus for the request (SEALED: the M6.2 snapshot corpus)."""

    source_ids: tuple[str, ...]
    exact_blob_hashes: tuple[tuple[str, str], ...]
    corpus_hash: str
    closed_corpus_required: bool

    def __post_init__(self) -> None:
        # Normalize to immutable tuples so a caller-supplied list cannot mutate
        # the corpus (and silently invalidate corpus_hash) after construction.
        object.__setattr__(self, "source_ids", tuple(self.source_ids))
        object.__setattr__(
            self, "exact_blob_hashes",
            tuple((str(s), str(h)) for s, h in self.exact_blob_hashes),
        )

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
    #: The authoritative SEALED snapshot this request was derived from. Bound at
    #: construction so a request with SEALED authority cannot be produced by
    #: direct construction (the fields must agree with this snapshot).
    authority_snapshot: "SealedInputSnapshot | None" = field(
        default=None, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        # Normalize BEFORE validating: a caller-supplied list must not be able to
        # mutate the reference set (and stale request_payload_hash) afterwards.
        object.__setattr__(
            self, "authorized_prior_evidence_refs",
            tuple(self.authorized_prior_evidence_refs),
        )
        # ---- authority binding ------------------------------------------
        snapshot = self.authority_snapshot
        if not isinstance(snapshot, SealedInputSnapshot):
            raise ResearchRequestError(
                "a SEALED request must be bound to an authoritative "
                "SealedInputSnapshot (build it with build_deep_research_request)"
            )
        _verify_snapshot_consistency(snapshot)
        for bound_name, declared in (
            ("case_id", self.case_id),
            ("case_version", self.case_version),
            ("pit_mode", self.pit_mode),
            ("as_of", self.as_of),
            ("input_snapshot_hash", self.input_snapshot_hash),
            ("snapshot_id", self.snapshot_id),
            ("pit_context_id", self.pit_context_id),
        ):
            if getattr(snapshot, bound_name) != declared:
                raise ResearchRequestError(
                    f"{bound_name} disagrees with the bound authoritative snapshot"
                )
        bound_hashes = tuple(
            (s.source_id, s.raw_blob_sha256) for s in snapshot.ordered_sources
        )
        if bound_hashes != self.corpus.exact_blob_hashes:
            raise ResearchRequestError(
                "the request corpus disagrees with the bound authoritative snapshot"
            )
        for name in (
            "request_id", "research_run_id", "ledger_id", "rrm_manifest_id",
            "case_id", "case_version", "evidence_gap_id", "research_question",
            "pit_context_id", "pit_mode", "as_of", "input_snapshot_hash",
            "snapshot_id", "request_payload_hash",
        ):
            value = getattr(self, name)
            if not _has_visible_text(value):
                raise ResearchRequestError(f"{name} must be a non-blank string")
        if self.capability != S10_CAPABILITY:
            raise ResearchRequestError(
                f"unsupported capability {self.capability!r}; M6.4 exposes {S10_CAPABILITY!r}"
            )
        if self.pit_mode != SEALED_PIT_MODE:
            raise ResearchRequestError(f"request pit_mode must be {SEALED_PIT_MODE!r}")
        if self.snapshot_id != self.input_snapshot_hash:
            raise ResearchRequestError(
                "snapshot_id must equal the deterministic input_snapshot_hash"
            )
        if self.corpus.closed_corpus_required is not True:
            raise ResearchRequestError("a SEALED request corpus must require a closed corpus")
        if self.request_isolation_required is not True:
            raise ResearchRequestError("a SEALED request must require request isolation")
        if self.provider.closed_corpus_required is not True:
            raise ResearchRequestError("provider configuration must require a closed corpus")
        if self.provider.request_isolation_required is not True:
            raise ResearchRequestError("provider configuration must require request isolation")
        if self.provider.capability != S10_CAPABILITY:
            raise ResearchRequestError("provider configuration capability must be S10")
        if self.corpus.source_ids != tuple(s for s, _ in self.corpus.exact_blob_hashes):
            raise ResearchRequestError(
                "corpus source ids disagree with the exact blob-hash ordering"
            )
        seen_refs: set[str] = set()
        for ref in self.authorized_prior_evidence_refs:
            if not _has_visible_text(ref):
                raise ResearchRequestError(
                    "authorized_prior_evidence_refs entries must be non-blank strings"
                )
            if ref in seen_refs:
                raise ResearchRequestError(
                    f"duplicate authorized prior-evidence reference {ref!r}; the "
                    "reference set must be unique"
                )
            seen_refs.add(ref)
        expected_corpus_hash = _deterministic_hash(_CorpusIdentity(
            sources=[
                _CorpusSource(source_id=s, exact_blob_hash=h)
                for s, h in self.corpus.exact_blob_hashes
            ]
        ))
        if self.corpus.corpus_hash != expected_corpus_hash:
            raise ResearchRequestError("corpus_hash does not match the declared corpus")
        expected_payload_hash = _deterministic_hash(_RequestPayloadIdentity(
            research_question=self.research_question,
            case_id=self.case_id,
            case_version=self.case_version,
            evidence_gap_id=self.evidence_gap_id,
            input_snapshot_hash=self.input_snapshot_hash,
            pit_mode=self.pit_mode,
            as_of=self.as_of,
            capability=self.capability,
            closed_corpus_required=self.corpus.closed_corpus_required,
            request_isolation_required=self.request_isolation_required,
            authorized_prior_evidence_refs=sorted(self.authorized_prior_evidence_refs),
        ))
        if self.request_payload_hash != expected_payload_hash:
            raise ResearchRequestError(
                "request_payload_hash does not match the semantic request payload"
            )

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
    """Private deterministic hash payload (NOT a canonical M4A schema).

    Covers the logical semantic request only: the research question, the
    snapshot-derived authority fields, and the semantic request options. It
    deliberately excludes volatile identity (request UUID, orchestration ids),
    the provider surface, timeouts, wall clock and object identity.
    """

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
    authorized_prior_evidence_refs: list[str]


def _verify_snapshot_consistency(snapshot: SealedInputSnapshot) -> None:
    """Recompute the M6.0 snapshot identity from the snapshot's own fields.

    M6.4 consumes — but does not build — the snapshot. This bounded check makes
    an internally INCONSISTENT snapshot (forged/corrupted case, sources, AS_OF or
    hash) fail closed using the accepted M6.2 identity definition, without
    introducing a second PIT authority. A fully consistent in-process forgery is
    outside the process trust boundary (documented in the module docstring).
    """
    try:
        recomputed = _compute_input_snapshot_hash(
            case_id=snapshot.case_id,
            case_version=snapshot.case_version,
            pit_mode=snapshot.pit_mode,
            as_of=snapshot.as_of,
            ordered=tuple(snapshot.ordered_sources),
        )
    except Exception as exc:  # noqa: BLE001 — unverifiable authority fails closed
        raise RequestAuthorityViolation(
            f"SEALED snapshot identity could not be verified: {type(exc).__name__}"
        ) from exc
    if recomputed != snapshot.input_snapshot_hash:
        raise RequestAuthorityViolation(
            "SEALED snapshot identity is not self-consistent: recomputed "
            f"{recomputed} != declared {snapshot.input_snapshot_hash}"
        )
    if snapshot.snapshot_id != snapshot.input_snapshot_hash:
        raise RequestAuthorityViolation(
            "SEALED snapshot id does not equal its deterministic identity hash"
        )
    if snapshot.closed_corpus_required is not True:
        raise RequestAuthorityViolation(
            "the SEALED snapshot must require a closed corpus"
        )
    # Byte-level integrity: the captured bytes must match the declared blob hash
    # and length for every sealed source (the identity hash alone would not catch
    # a byte swap that preserved the recorded hash).
    for src in snapshot.ordered_sources:
        blob = src.raw_bytes
        if not isinstance(blob, (bytes, bytearray)):
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} does not carry exact bytes"
            )
        if hashlib.sha256(bytes(blob)).hexdigest() != src.raw_blob_sha256:
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} bytes do not match the declared "
                "blob SHA-256"
            )
        if len(blob) != src.raw_byte_length:
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} byte length does not match the "
                "declared length"
            )
        # M6.2 source binding (rules F/H): the source's content hash and the raw
        # blob SHA-256 are the same authority and must agree. The identity hash is
        # computed from the blob hash, so a tampered content_hash alone would
        # otherwise slip through as an internally inconsistent SEALED snapshot.
        if src.source_content_hash != src.raw_blob_sha256:
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} content hash does not match its "
                "raw blob SHA-256"
            )

    # M6.2 structural invariants the authority path must re-check: a snapshot is
    # only authoritative if it is internally consistent with its own build rules.
    if snapshot.source_count != len(snapshot.ordered_sources):
        raise RequestAuthorityViolation(
            "SEALED snapshot source_count does not match its ordered sources"
        )
    ordered_ids = [s.source_id for s in snapshot.ordered_sources]
    if ordered_ids != sorted(ordered_ids):
        raise RequestAuthorityViolation(
            "SEALED snapshot sources are not in canonical (sorted) order"
        )
    if len(set(ordered_ids)) != len(ordered_ids):
        raise RequestAuthorityViolation(
            "SEALED snapshot contains duplicate source ids"
        )
    try:
        as_of_date = dt.date.fromisoformat(snapshot.as_of)
    except (TypeError, ValueError):
        raise RequestAuthorityViolation("SEALED snapshot AS_OF is not an ISO date")
    for src in snapshot.ordered_sources:
        if src.eligibility_verdict != SealedEligibility.ELIGIBLE.value:
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} is not ELIGIBLE "
                f"({src.eligibility_verdict!r})"
            )
        try:
            admitted = dt.datetime.fromisoformat(src.archive_admitted_at)
        except (TypeError, ValueError):
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} admission timestamp is not ISO-8601"
            )
        if admitted.date() > as_of_date:
            raise RequestAuthorityViolation(
                f"SEALED source {src.source_id!r} was admitted after AS_OF"
            )


def _deterministic_hash(payload: BaseModel) -> str:
    return compute_canonical_hash(payload)


def _require_non_empty(value: Any, name: str, error: type[ResearchContractError]) -> str:
    if not _has_visible_text(value):
        raise error(f"{name} must be a non-blank string")
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
    _verify_snapshot_consistency(snapshot)
    if snapshot.pit_mode != SEALED_PIT_MODE:
        raise RequestAuthorityViolation(
            f"snapshot PIT mode {snapshot.pit_mode!r} is not {SEALED_PIT_MODE!r}"
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
    seen_refs: set[str] = set()
    for ref in prior_refs:
        if not _has_visible_text(ref):
            raise ResearchRequestError(
                "authorized_prior_evidence_refs entries must be non-blank strings"
            )
        if ref in seen_refs:
            raise ResearchRequestError(
                f"duplicate authorized prior-evidence reference {ref!r}; the "
                "reference set must be unique"
            )
        seen_refs.add(ref)

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
            # Order-insensitive: the authorized prior-evidence reference set is
            # semantically a set, so a different ordering must not change identity.
            authorized_prior_evidence_refs=sorted(prior_refs),
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
        authority_snapshot=snapshot,
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

    def __post_init__(self) -> None:
        if not isinstance(self.index, int) or isinstance(self.index, bool) or self.index < 0:
            raise ResearchResultError(
                "a source pointer index must be a non-negative integer"
            )
        if not _has_visible_text(self.reference):
            raise ResearchResultError("a source pointer requires a non-blank reference")
        if self.title is not None and not _has_visible_text(self.title):
            raise ResearchResultError(
                "a source pointer title must be a non-blank string or None"
            )


def compute_citation_list_sha256(source_pointers: Sequence["SourcePointer"]) -> str:
    """Deterministic digest over the provider citation / source-pointer list.

    M6.0 §3 defines the result hash as SHA-256 over the exact retrieved report
    bytes **plus** a citation/source-list hash. ``result_sha256`` remains the
    exact report-byte digest; this is the companion digest, computed over the
    canonical ordering of the pointers (operational, NON-CANONICAL — it confers
    no evidence status on the pointers).
    """
    identity = _CitationIdentity(
        citations=[
            _CitationRef(index=int(p.index), reference=str(p.reference),
                         title=p.title if p.title is None else str(p.title))
            for p in source_pointers
        ]
    )
    return _deterministic_hash(identity)


class _CitationRef(BaseModel):
    index: int
    reference: str
    title: str | None = None


class _CitationIdentity(BaseModel):
    citations: list[_CitationRef]


def _validate_result_invariants(
    status: "ResearchResultStatus",
    result_bytes: bytes | None,
    result_sha256: str | None,
    failure_detail: str | None,
    corpus_enum: "ClosedCorpusEnforcement",
    isolation_enum: "IsolationVerification",
    source_pointers: Sequence["SourcePointer"],
    corpus_evidence_ref: str | None,
    isolation_evidence_ref: str | None,
) -> None:
    """The M6.4 result invariants — enforced on EVERY construction path."""
    # negative fail-closed states must carry their matching status
    if corpus_enum is ClosedCorpusEnforcement.CANNOT_ENFORCE and (
        status is not ResearchResultStatus.PROVIDER_CANNOT_ENFORCE_SEALED_INPUT
    ):
        raise ResearchResultError(
            "a provider that cannot enforce the closed corpus must fail closed "
            "with PROVIDER_CANNOT_ENFORCE_SEALED_INPUT (never a fabricated success)"
        )
    if isolation_enum is IsolationVerification.UNVERIFIED and (
        status is not ResearchResultStatus.REQUEST_ISOLATION_UNVERIFIED
    ):
        raise ResearchResultError(
            "an unverified request-isolation state must fail closed with "
            "REQUEST_ISOLATION_UNVERIFIED"
        )
    # a POSITIVE claim requires an explicit, non-empty evidence reference —
    # a bare caller assertion is not proof.
    if corpus_enum is ClosedCorpusEnforcement.ENFORCED and not _has_visible_text(
        corpus_evidence_ref
    ):
        raise ResearchResultError(
            "closed-corpus ENFORCED requires a non-blank closed_corpus_evidence_ref"
        )
    if isolation_enum is IsolationVerification.VERIFIED and not _has_visible_text(
        isolation_evidence_ref
    ):
        raise ResearchResultError(
            "isolation VERIFIED requires a non-blank isolation_evidence_ref"
        )
    # M6.0 §5 / §11.2 R7: a PASS requires POSITIVE proof of closed-corpus
    # enforcement and request isolation; otherwise the run must fail closed.
    if status.is_success:
        if corpus_enum is not ClosedCorpusEnforcement.ENFORCED:
            raise ResearchResultError(
                "SUCCESS requires proven closed-corpus enforcement (ENFORCED with an "
                "evidence reference); otherwise fail closed with "
                "PROVIDER_CANNOT_ENFORCE_SEALED_INPUT"
            )
        if isolation_enum is not IsolationVerification.VERIFIED:
            raise ResearchResultError(
                "SUCCESS requires proven request isolation (VERIFIED with an evidence "
                "reference) per M6.0 R7; otherwise fail closed with "
                "REQUEST_ISOLATION_UNVERIFIED"
            )

    if status.is_success:
        if result_bytes is None or len(bytes(result_bytes)) == 0:
            raise ResearchResultError(
                "SUCCESS requires non-empty result content (a blank provider "
                "result must be represented as a typed failure)"
            )
        if len(bytes(result_bytes).strip()) == 0 or _is_blank_text_bytes(bytes(result_bytes)):
            raise ResearchResultError(
                "SUCCESS requires non-blank result content (blank / whitespace-only "
                "provider output, including Unicode whitespace, must be represented "
                "as a typed failure)"
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
    else:
        if not _has_visible_text(failure_detail):
            raise ResearchResultError(
                "a non-SUCCESS result requires a documented failure_detail "
                "(failures are never a silent blank)"
            )
        if result_bytes is None and result_sha256 is not None:
            raise ResearchResultError(
                "a hash must never be recorded for absent result output"
            )
        if result_bytes is not None and result_sha256 is not None:
            actual = compute_result_sha256(bytes(result_bytes))
            if actual != result_sha256:
                raise ResearchResultError(
                    f"result_sha256 mismatch: recorded {result_sha256}, actual {actual}"
                )

    for ptr in source_pointers:
        if not isinstance(ptr, SourcePointer):
            raise ResearchResultError("source_pointers must contain SourcePointer values")
        if not _has_visible_text(ptr.reference):
            raise ResearchResultError("a source pointer requires a non-blank reference")


@dataclass(frozen=True)
class DeepResearchResult:
    """Immutable logical Deep Research result (NON-CANONICAL, fail-closed).

    The envelope carries no field that could upgrade it to canonical evidence:
    canonical admission is M6.6 plus the existing Evidence Admission Gate.

    Invariants are enforced at construction (``__post_init__``), so a directly
    constructed instance cannot be invalid either — prefer
    :func:`build_deep_research_result` for friendly error messages.
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
    #: Companion digest over the citation/source-pointer list (M6.0 §3); derived
    #: from ``source_pointers`` and validated — a caller-supplied value that
    #: disagrees is rejected.
    citation_list_sha256: str | None = None
    #: Opaque references to the positive enforcement/isolation evidence. Required
    #: (non-empty) before ENFORCED / VERIFIED may be claimed, and therefore before
    #: SUCCESS. These are IDENTIFIERS — the trusted proof seam (FD #152) resolves
    #: and verifies them; M6.4 never treats the string itself as proof.
    closed_corpus_evidence_ref: str | None = None
    isolation_evidence_ref: str | None = None
    #: The deterministic SEALED input-snapshot identity this result is bound to.
    #: Set from the authoritative request for a SUCCESS result, where it must also
    #: agree with the verified-proof attestation; optional for non-SUCCESS results.
    input_snapshot_hash: str | None = None
    #: Private immutable verified-proof capability (FD #152) — minted ONLY by the
    #: trusted verification path in ``build_deep_research_result``. A SUCCESS result
    #: must carry one bound to its own identity, which is why a directly constructed
    #: ``DeepResearchResult(...)`` can never authorize SUCCESS. Never a public field.
    _proof_attestation: "_VerifiedProofAttestation | None" = field(
        default=None, repr=False, compare=False
    )

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """The result envelope is FINAL — subclassing would reopen the FD #152 bypass.

        A subclass could otherwise override ``__post_init__`` (skipping the SUCCESS
        proof gate) and be constructed as a SUCCESS without any trusted
        verification. Refusing subclasses closes that construction path.
        """
        raise ResearchResultError(
            "DeepResearchResult is final and cannot be subclassed — a subclass could "
            "bypass the FD #152 trusted proof-verification gate"
        )

    def __post_init__(self) -> None:
        # Immutable pointer collection: a caller-supplied list must not be able to
        # mutate the preserved source pointers after validation.
        object.__setattr__(self, "source_pointers", tuple(self.source_pointers))
        # Immutable provider metadata: keys/values must be strings (the declared
        # Mapping[str, str]) and the copy is wrapped in an immutable proxy, so
        # neither the caller's mapping nor a mutable value can change the result.
        if self.provider_reported_metadata is not None:
            if not isinstance(self.provider_reported_metadata, Mapping):
                raise ResearchResultError(
                    "provider_reported_metadata must be a mapping of str to str"
                )
            metadata: dict[str, str] = {}
            for key, value in self.provider_reported_metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ResearchResultError(
                        "provider_reported_metadata keys and values must be strings"
                    )
                metadata[key] = value
            object.__setattr__(
                self, "provider_reported_metadata", MappingProxyType(metadata)
            )
        for name in ("request_id", "research_run_id", "ledger_id", "provider_surface"):
            value = getattr(self, name)
            if not _has_visible_text(value):
                raise ResearchResultError(f"{name} must be a non-blank string")
        if not isinstance(self.status, ResearchResultStatus):
            raise ResearchResultError(
                "status must be a ResearchResultStatus (use build_deep_research_result)"
            )
        if not isinstance(self.closed_corpus_enforcement, ClosedCorpusEnforcement):
            raise ResearchResultError(
                "closed_corpus_enforcement must be a ClosedCorpusEnforcement"
            )
        if not isinstance(self.isolation_verification, IsolationVerification):
            raise ResearchResultError(
                "isolation_verification must be an IsolationVerification"
            )
        if self.result_bytes is not None and not isinstance(self.result_bytes, bytes):
            raise ResearchResultError("result_bytes must be bytes or None")
        # Citation/source-list companion digest (M6.0 §3): derived and verified.
        # Derived BEFORE the proof gate below because the attestation binds this
        # digest (round-16 reviewer finding).
        expected_citation = compute_citation_list_sha256(self.source_pointers)
        if self.citation_list_sha256 is None:
            object.__setattr__(self, "citation_list_sha256", expected_citation)
        elif self.citation_list_sha256 != expected_citation:
            raise ResearchResultError(
                "citation_list_sha256 does not match the source-pointer list"
            )
        # ---- trusted proof-verification seam (FD #152) --------------------
        # SUCCESS is only constructible through the trusted verification path:
        # it must carry a private attestation, and that attestation must bind the
        # exact identity of THIS result — including the validated result-byte and
        # citation-list digests. A direct construction carries none, so it can never
        # fabricate a SUCCESS from bare enum claims + invented references.
        if self.status.is_success:
            attestation = self._proof_attestation
            if not isinstance(attestation, _VerifiedProofAttestation):
                raise ResearchResultError(
                    "SUCCESS requires a verified-proof attestation produced by the "
                    "trusted proof-verification path — build the result with "
                    "build_deep_research_result(request=..., proof_resolver=...); a "
                    "directly constructed result cannot authorize SUCCESS"
                )
            mismatch = _attestation_mismatch(attestation, self)
            if mismatch is not None:
                raise ResearchResultError(
                    "SUCCESS refused: the verified-proof attestation does not bind "
                    f"this result ({mismatch})"
                )
        _validate_result_invariants(
            self.status, self.result_bytes, self.result_sha256, self.failure_detail,
            self.closed_corpus_enforcement, self.isolation_verification, self.source_pointers,
            self.closed_corpus_evidence_ref, self.isolation_evidence_ref,
        )

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

    def assert_proof_verified(self) -> "DeepResearchResult":
        """Consumption-boundary revalidation of a ``SUCCESS`` result (FD #152).

        EVERY consumer of a SUCCESS result must call this before acting on it. It
        re-derives the checks instead of trusting construction-time validation, so
        it also catches a result object that never came through the trusted
        verification path:

        * a SUCCESS with no verified-proof attestation (e.g. produced by
          ``object.__new__``, which skips ``__post_init__`` entirely);
        * an attestation that does not bind this result's exact identity;
        * result bytes that no longer match ``result_sha256`` (post-construction
          replacement — e.g. ``object.__setattr__``, which a frozen dataclass does
          NOT prevent);
        * a citation-list digest that no longer matches the source pointers.

        Raises :class:`ResearchResultError` when any check fails. This is the
        bounded in-process control, NOT a process/cryptographic boundary: hostile
        same-process code is outside the accepted M6.2/M6.3 trust boundary, which
        is why this re-check — not the frozen dataclass — is what consumers rely on.
        """
        if not self.status.is_success:
            raise ResearchResultError(
                "assert_proof_verified applies only to a SUCCESS result"
            )
        # getattr: an object created via ``object.__new__`` never ran __post_init__
        # and may not carry this slot at all — that is exactly the case to refuse.
        attestation = getattr(self, "_proof_attestation", None)
        if not isinstance(attestation, _VerifiedProofAttestation):
            raise ResearchResultError(
                "SUCCESS refused at the consumption boundary: the result carries no "
                "verified-proof attestation (it was not produced by the trusted "
                "proof-verification path)"
            )
        mismatch = _attestation_mismatch(attestation, self)
        if mismatch is not None:
            raise ResearchResultError(
                "SUCCESS refused at the consumption boundary: the verified-proof "
                f"attestation does not bind this result ({mismatch})"
            )
        if not isinstance(self.result_bytes, bytes) or not self.result_bytes:
            raise ResearchResultError(
                "SUCCESS refused at the consumption boundary: result bytes are absent"
            )
        if self.result_sha256 != compute_result_sha256(self.result_bytes):
            raise ResearchResultError(
                "SUCCESS refused at the consumption boundary: result bytes no longer "
                "match result_sha256 (the result was mutated after construction)"
            )
        if self.citation_list_sha256 != compute_citation_list_sha256(self.source_pointers):
            raise ResearchResultError(
                "SUCCESS refused at the consumption boundary: the citation-list "
                "digest no longer matches the source pointers"
            )
        return self


def compute_result_sha256(result_bytes: bytes) -> str:
    """SHA-256 over the EXACT bytes that are stored/passed onward."""
    if not isinstance(result_bytes, (bytes, bytearray)):
        raise ResearchResultError("result bytes must be bytes")
    return hashlib.sha256(bytes(result_bytes)).hexdigest()


#: Unicode general categories that render as nothing: separators (Z*), format
#: (Cf — includes the LRM/RLM marks, BOM, zero-width joiners/non-joiners) and
#: control (Cc). Detecting by CATEGORY rather than a hand-listed character set
#: means every invisible character is covered, not just enumerated ones.
_INVISIBLE_CATEGORIES = ("Cf", "Cc", "Cs", "Zs", "Zl", "Zp")

#: Individual codepoints that render as nothing but are neither whitespace nor in
#: an invisible general category (they are e.g. Lo/So/Mn): fillers and other
#: blank glyphs. Enumerated explicitly because Unicode category alone would call
#: them "visible".
_INVISIBLE_CODEPOINTS = frozenset({
    0x00AD,  # SOFT HYPHEN
    0x034F,  # COMBINING GRAPHEME JOINER
    0x115F,  # HANGUL CHOSEONG FILLER
    0x1160,  # HANGUL JUNGSEONG FILLER
    0x17B4,  # KHMER VOWEL INHERENT AQ
    0x17B5,  # KHMER VOWEL INHERENT AA
    0x180E,  # MONGOLIAN VOWEL SEPARATOR
    0x2800,  # BRAILLE PATTERN BLANK
    0x3164,  # HANGUL FILLER
    0xFFA0,  # HALFWIDTH HANGUL FILLER
})

#: Codepoint RANGES that render as nothing (variation selectors, invisible
#: operators, tag characters, interlinear annotation).
_INVISIBLE_RANGES = (
    (0xFE00, 0xFE0F),    # variation selectors
    (0xE0100, 0xE01EF),  # variation selectors supplement
    (0x2060, 0x206F),    # invisible operators / deprecated format controls
    (0xFFF9, 0xFFFB),    # interlinear annotation
)


#: Nonspacing/enclosing combining marks (Mn/Me) require a BASE character to render
#: onto. A string made only of such marks has no visible content — this is the
#: general rule that covers the Mongolian free variation selectors U+180B–U+180F
#: and every other mark, rather than enumerating them one by one.
_MARK_CATEGORIES = ("Mn", "Me")


def _char_is_invisible(ch: str) -> bool:
    """True when a single character renders as nothing on its own."""
    if ch.isspace() or unicodedata.category(ch) in _INVISIBLE_CATEGORIES:
        return True
    cp = ord(ch)
    if cp in _INVISIBLE_CODEPOINTS:
        return True
    return any(low <= cp <= high for low, high in _INVISIBLE_RANGES)


def _is_blank_text(text: str) -> bool:
    """True when ``text`` has no visible content.

    A character contributes nothing when it is whitespace, an invisible category,
    an enumerated blank glyph, in a blank range, or a combining mark (Mn/Me) that
    has no preceding base character to attach to.
    """
    have_base = False
    for ch in text:
        if _char_is_invisible(ch):
            continue
        if unicodedata.category(ch) in _MARK_CATEGORIES and not have_base:
            continue
        have_base = True
    return not have_base


def _is_blank_text_bytes(raw: bytes) -> bool:
    """True when ``raw`` decodes as text whose visible content is empty.

    Every decoded character must be Unicode whitespace or belong to an invisible
    general category (Cf/Cc/Zs/Zl/Zp) — so interleaved and unlisted invisible
    characters (e.g. U+200E LEFT-TO-RIGHT MARK) are blank too. Bytes that do NOT
    decode as UTF-8 are treated as real (binary) payload, not blank text.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return _is_blank_text(text)


def _has_visible_text(value: Any) -> bool:
    """True iff ``value`` is a string carrying at least one visible character.

    Invisible-only strings (spaces, LRM/RLM, BOM, zero-width, controls) are NOT
    acceptable for a contractually non-empty text field. A surrogate codepoint
    (category Cs) is never valid text — not even embedded next to visible
    characters — so any string containing one is rejected.
    """
    if not isinstance(value, str):
        return False
    if any(unicodedata.category(ch) == "Cs" for ch in value):
        return False
    return not _is_blank_text(value)


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
    closed_corpus_evidence_ref: str | None = None,
    isolation_evidence_ref: str | None = None,
    citation_list_sha256: str | None = None,
    request: "DeepResearchRequest | None" = None,
    proof_resolver: "DeepResearchProofResolver | None" = None,
) -> DeepResearchResult:
    """Build an immutable result envelope from provider output.

    SUCCESS is refused for blank output, and a hash is never fabricated for
    absent output. Failures must carry a documented ``failure_detail``.

    FD #152 — a SUCCESS additionally requires the authoritative bound
    ``request`` and a trusted ``proof_resolver`` that independently verifies BOTH
    the closed-corpus enforcement and the request-isolation proof for that exact
    run; a bare ENFORCED/VERIFIED claim plus a non-empty evidence-reference string
    is never enough. With no resolver injected the default DENIES, so SUCCESS is
    refused (fail closed). An invalid SUCCESS is rejected, never coerced.
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

    pointers = tuple(source_pointers)

    # ---- trusted proof-verification seam (FD #152) -------------------------
    input_snapshot_hash: str | None = None
    attestation: _VerifiedProofAttestation | None = None
    if status_enum.is_success:
        # SUCCESS is bound to the authoritative request (never to duplicated
        # caller strings) and must be verified through the trusted seam. An
        # invalid SUCCESS construction is REJECTED — it is never silently coerced
        # into another status.
        if not isinstance(request, DeepResearchRequest):
            raise ResearchResultError(
                "SUCCESS requires the authoritative bound DeepResearchRequest "
                "(build_deep_research_result(request=..., proof_resolver=...)); "
                "duplicated caller strings are not request authority"
            )
        for name, supplied, bound in (
            ("request_id", request_id, request.request_id),
            ("research_run_id", research_run_id, request.research_run_id),
            ("ledger_id", ledger_id, request.ledger_id),
            ("provider_surface", provider_surface, request.provider.provider_surface),
        ):
            if not _has_visible_text(supplied):
                raise ResearchResultError(f"{name} must be a non-blank string")
            if supplied != bound:
                raise ResearchResultError(
                    f"SUCCESS refused: {name} {supplied!r} disagrees with the bound "
                    f"authoritative request ({bound!r})"
                )
        if corpus_enum is not ClosedCorpusEnforcement.ENFORCED:
            raise ResearchResultError(
                "SUCCESS requires the positive closed-corpus enforcement CLAIM "
                "(ENFORCED); a claim alone is never enough — it must also be "
                "verified by the trusted proof resolver"
            )
        if isolation_enum is not IsolationVerification.VERIFIED:
            raise ResearchResultError(
                "SUCCESS requires the positive request-isolation CLAIM (VERIFIED); "
                "a claim alone is never enough — it must also be verified by the "
                "trusted proof resolver"
            )
        # The validated digests are bound INTO the attestation (round-16 reviewer
        # finding), so a post-construction byte/digest replacement is detected at
        # the consumption boundary. Derive them from the actual payload/pointers —
        # never from caller-asserted strings.
        if result_bytes is None:
            raise ResearchResultError(
                "SUCCESS requires non-empty result content"
            )
        payload = bytes(result_bytes)
        validated_result_sha256 = compute_result_sha256(payload)
        if result_sha256 is not None and result_sha256 != validated_result_sha256:
            raise ResearchResultError(
                "SUCCESS refused: result_sha256 does not match the supplied result bytes"
            )
        validated_citation_sha256 = compute_citation_list_sha256(pointers)
        if (
            citation_list_sha256 is not None
            and citation_list_sha256 != validated_citation_sha256
        ):
            raise ResearchResultError(
                "SUCCESS refused: citation_list_sha256 does not match the "
                "source-pointer list"
            )
        attestation = _verify_success_proofs(
            request=request,
            proof_resolver=proof_resolver,
            corpus_evidence_ref=closed_corpus_evidence_ref,
            isolation_evidence_ref=isolation_evidence_ref,
            result_sha256=validated_result_sha256,
            citation_list_sha256=validated_citation_sha256,
        )
        input_snapshot_hash = request.input_snapshot_hash

    # Every M6.4 result invariant is enforced by DeepResearchResult.__post_init__,
    # which runs on ALL construction paths — a directly constructed instance
    # cannot be invalid, and (FD #152) cannot be a SUCCESS without the verified
    # proof attestation minted above.
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
        closed_corpus_evidence_ref=closed_corpus_evidence_ref,
        isolation_evidence_ref=isolation_evidence_ref,
        input_snapshot_hash=input_snapshot_hash,
        _proof_attestation=attestation,
        citation_list_sha256=citation_list_sha256,
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
