"""QAD M6.7 - DETERMINISTIC MOCK TRANSPORT (non-canonical, offline).

FD #151 M6.7 provider execution, Founder decisions R3/R4/R5:

* MOCK ONLY - no Gemini Notebook, no browser/CDP, no network, no credentials. This module
  imports no egress library, and the acceptance suite proves the whole path runs with
  ``socket`` disabled.
* The transport is DETERMINISTIC: outcomes are scripted per attempt, SEALED bytes are
  reloaded from the authoritative archive (never caller-supplied), and the evidence it
  produces is reproducible.
* The transport produces INDEPENDENTLY CHECKABLE EXECUTION EVIDENCE for the two FD #149/
  #152 proof properties (closed-corpus enforcement and request isolation). Evidence is
  written through a module-private guard so an ordinary caller cannot fabricate it, and the
  mock proof resolver re-derives the evidence reference and re-checks the observed facts.

The transport NEVER mutates the ledger, never classifies retry policy, never chooses an
attempt number and never mints a proof.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from qad.m6.provider import (
    FAILURE_CANNOT_ENFORCE_CLOSED_CORPUS,
    FAILURE_PROOF_NOT_VERIFIED,
    FAILURE_SCRIPTED_TRANSPORT,
    FAILURE_SEALED_BYTES_NOT_ADMITTED,
    FAILURE_SEALED_BYTE_MISMATCH,
    FAILURE_SEALED_ATTESTATION,
    MOCK_PROVIDER_SURFACE,
    MOCK_TRANSPORT_TYPE,
    ProviderAdapterError,
    ProviderOutcome,
    ProviderOutcomeKind,
    TransportEvidence,
    not_exposed_provider_telemetry,
)
from qad.m6.research_contract import (
    ClosedCorpusEnforcement,
    IsolationVerification,
    ProofKind,
    ProviderConfiguration,
    ResearchResultError,
    ResearchResultStatus,
    SourcePointer,
    build_deep_research_result,
)

#: Provenance marker for evidence minted by this deterministic harness.
MOCK_EVIDENCE_PRODUCER = "M6.7_MOCK_TRANSPORT"

#: Deterministic citation references for mock-discovered sources.
MOCK_SOURCE_REFERENCE_PREFIX = "mock://source/"

#: Module-private guard. Only this module can write execution evidence.
_EVIDENCE_GUARD = object()


def compute_mock_evidence_ref(
    proof_kind,
    request_id,
    research_run_id,
    ledger_id,
    provider_surface,
    input_snapshot_hash,
    approved_source_ids,
    approved_corpus_hash,
    observed_source_ids,
    observed_corpus_hash,
    extraneous_source_ids,
    sealed_bytes_verified,
    isolation_probe_performed,
    foreign_canary_tokens,
    attempt_number,
    producer,
):
    """Deterministic digest over the FULL observed fact set.

    Because the reference digests what was OBSERVED (not a caller-supplied string), a
    fabricated or edited evidence record no longer matches its own reference.
    """
    payload = json.dumps(
        {
            "proof_kind": proof_kind.value,
            "request_id": request_id,
            "research_run_id": research_run_id,
            "ledger_id": ledger_id,
            "provider_surface": provider_surface,
            "input_snapshot_hash": input_snapshot_hash,
            "approved_source_ids": list(approved_source_ids),
            "approved_corpus_hash": approved_corpus_hash,
            "observed_source_ids": list(observed_source_ids),
            "observed_corpus_hash": observed_corpus_hash,
            "extraneous_source_ids": list(extraneous_source_ids),
            "sealed_bytes_verified": bool(sealed_bytes_verified),
            "isolation_probe_performed": bool(isolation_probe_performed),
            "foreign_canary_tokens": list(foreign_canary_tokens),
            "attempt_number": attempt_number,
            "producer": producer,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "MOCK-EVID-" + hashlib.sha256(payload).hexdigest()[:24]


@dataclass(frozen=True)
class MockExecutionEvidence:
    """Independently checkable execution evidence for ONE proof kind of ONE run."""

    evidence_ref: str
    proof_kind: ProofKind
    request_id: str
    research_run_id: str
    ledger_id: str
    provider_surface: str
    input_snapshot_hash: str
    approved_source_ids: tuple
    approved_corpus_hash: str
    observed_source_ids: tuple
    observed_corpus_hash: str
    extraneous_source_ids: tuple
    sealed_bytes_verified: bool
    isolation_probe_performed: bool
    foreign_canary_tokens: tuple
    attempt_number: int
    producer: str = MOCK_EVIDENCE_PRODUCER

    def __post_init__(self):
        if not isinstance(self.proof_kind, ProofKind):
            raise ProviderAdapterError("evidence proof_kind must be a ProofKind")
        for name in (
            "evidence_ref", "request_id", "research_run_id", "ledger_id",
            "provider_surface", "input_snapshot_hash", "approved_corpus_hash",
            "observed_corpus_hash", "producer",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ProviderAdapterError(
                    "execution evidence requires a non-blank " + name)
        for name in ("approved_source_ids", "observed_source_ids",
                     "extraneous_source_ids", "foreign_canary_tokens"):
            object.__setattr__(self, name, tuple(getattr(self, name)))
        if not isinstance(self.attempt_number, int) or isinstance(
                self.attempt_number, bool) or self.attempt_number < 1:
            raise ProviderAdapterError("evidence attempt_number must be positive")
        for name in ("sealed_bytes_verified", "isolation_probe_performed"):
            if not isinstance(getattr(self, name), bool):
                raise ProviderAdapterError(name + " must be a bool")

    @property
    def inventory_is_closed(self):
        """The provider-visible inventory was EXACTLY the approved corpus."""
        return (
            self.observed_source_ids == self.approved_source_ids
            and self.observed_corpus_hash == self.approved_corpus_hash
            and not self.extraneous_source_ids
        )

    @property
    def context_is_isolated(self):
        """The request context carried no foreign (previous-run) material."""
        return self.isolation_probe_performed and not self.foreign_canary_tokens

    def recompute_ref(self):
        return compute_mock_evidence_ref(
            proof_kind=self.proof_kind,
            request_id=self.request_id,
            research_run_id=self.research_run_id,
            ledger_id=self.ledger_id,
            provider_surface=self.provider_surface,
            input_snapshot_hash=self.input_snapshot_hash,
            approved_source_ids=self.approved_source_ids,
            approved_corpus_hash=self.approved_corpus_hash,
            observed_source_ids=self.observed_source_ids,
            observed_corpus_hash=self.observed_corpus_hash,
            extraneous_source_ids=self.extraneous_source_ids,
            sealed_bytes_verified=self.sealed_bytes_verified,
            isolation_probe_performed=self.isolation_probe_performed,
            foreign_canary_tokens=self.foreign_canary_tokens,
            attempt_number=self.attempt_number,
            producer=self.producer,
        )


class MockEvidenceStore:
    """Append-only evidence log. WRITABLE ONLY by the mock harness.

    The write path requires a module-private guard, so an ordinary caller cannot inject a
    fabricated evidence record (bounded mechanism - hostile same-process introspection of
    the guard is outside the accepted trust boundary, as recorded for FD #152).
    """

    __slots__ = ("_records",)

    def __init__(self):
        self._records = {}

    def _record(self, evidence, *, token):
        if token is not _EVIDENCE_GUARD:
            raise ProviderAdapterError(
                "mock execution evidence may only be written by the M6.7 mock harness")
        if evidence.evidence_ref != evidence.recompute_ref():
            raise ProviderAdapterError(
                "mock execution evidence reference is not self-consistent with the "
                "recorded observations")
        existing = self._records.get(evidence.evidence_ref)
        if existing is not None:
            # Deterministic re-execution of the SAME attempt observes the SAME facts, so
            # the identical record is re-minted; that is idempotent, not a rewrite. A
            # DIFFERENT record under an existing reference is a contradiction.
            if existing != evidence:
                raise ProviderAdapterError(
                    "mock execution evidence is immutable; the reference exists with "
                    "different recorded observations")
            return
        self._records[evidence.evidence_ref] = evidence

    def resolve(self, evidence_ref):
        return self._records.get(evidence_ref)

    def refs(self):
        return tuple(self._records)

    def _last(self, kind):
        for ref in reversed(list(self._records)):
            record = self._records[ref]
            if record.proof_kind is kind:
                return record
        return None

    def foreign_canary_tokens(self):
        """Foreign (previous-run) material observed by the LAST isolation probe."""
        record = self._last(ProofKind.REQUEST_ISOLATION)
        return () if record is None else record.foreign_canary_tokens

    def observed_source_ids(self):
        """The provider-visible inventory of the LAST isolation probe."""
        record = self._last(ProofKind.REQUEST_ISOLATION)
        return () if record is None else record.observed_source_ids



@dataclass(frozen=True)
class MockTransportScript:
    """Deterministic per-attempt script (1-based attempt numbers)."""

    attempt_outcomes: tuple = ()
    extraneous_citations: tuple = ()
    withhold_closed_corpus_evidence: bool = False
    withhold_isolation_evidence: bool = False
    forced_evidence_refs: object = None
    byte_tampering: bool = False
    cannot_enforce_closed_corpus: bool = False

    def __post_init__(self):
        allowed = ("RESULT", "TRANSPORT_FAILURE")
        for number, kind in self.attempt_outcomes:
            if not isinstance(number, int) or isinstance(number, bool) or number < 1:
                raise ProviderAdapterError(
                    "a scripted attempt number must be a positive integer")
            if kind not in allowed:
                raise ProviderAdapterError(
                    "unknown scripted outcome " + repr(kind)
                    + "; allowed: " + repr(sorted(allowed)))
        if self.forced_evidence_refs is not None:
            object.__setattr__(
                self, "forced_evidence_refs", tuple(self.forced_evidence_refs))

    def outcome_for(self, attempt_number):
        for number, kind in self.attempt_outcomes:
            if number == attempt_number:
                return kind
        return "RESULT"


class DeterministicMockTransport:
    """Deterministic, offline, provider-neutral mock transport (M6.7)."""

    def __init__(
        self,
        *,
        archive=None,
        evidence_store=None,
        script=None,
        surface=MOCK_PROVIDER_SURFACE,
        reuse_context=False,
        result_bytes=b"deterministic mock synthesis [1][2]",
        synthesis_ref="mock://synthesis/1",
        transport_type=MOCK_TRANSPORT_TYPE,
        timeout_seconds=None,
    ):
        self.surface = surface
        self.transport_type = transport_type
        self.result_bytes = bytes(result_bytes)
        self.synthesis_ref = synthesis_ref
        self._archive = archive
        self.evidence_store = (
            evidence_store if evidence_store is not None else MockEvidenceStore())
        self._script = script if script is not None else MockTransportScript()
        self._reuse_context = bool(reuse_context)
        self._context = set()
        self._timeout = timeout_seconds

    def capability(self):
        return ProviderConfiguration(
            provider_surface=self.surface, timeout_seconds=self._timeout)

    def _fail(self, kind, code, diagnostic, attempt_number, evidence=None):
        return ProviderOutcome(
            kind=kind,
            provider_surface=self.surface,
            attempt_number=attempt_number,
            failure_code=code,
            diagnostic=diagnostic,
            transport_evidence=evidence,
            telemetry=not_exposed_provider_telemetry(),
            evidence_refs=(),
        )

    def _mint_evidence(self, request, kind, attempt_number, approved, observed,
                       extraneous, sealed_ok):
        facts = dict(
            proof_kind=kind,
            request_id=request.request_id,
            research_run_id=request.research_run_id,
            ledger_id=request.ledger_id,
            provider_surface=self.surface,
            input_snapshot_hash=request.input_snapshot_hash,
            approved_source_ids=tuple(approved),
            approved_corpus_hash=request.corpus.corpus_hash,
            observed_source_ids=tuple(observed),
            observed_corpus_hash=request.corpus.corpus_hash,
            extraneous_source_ids=tuple(extraneous),
            sealed_bytes_verified=bool(sealed_ok),
            isolation_probe_performed=True,
            foreign_canary_tokens=tuple(extraneous),
            attempt_number=attempt_number,
            producer=MOCK_EVIDENCE_PRODUCER,
        )
        ref = compute_mock_evidence_ref(**facts)
        evidence = MockExecutionEvidence(evidence_ref=ref, **facts)
        self.evidence_store._record(evidence, token=_EVIDENCE_GUARD)
        return evidence

    def _claim_ref(self, request, kind, attempt_number):
        """A plausible but UNBACKED evidence reference (adversarial fixture)."""
        payload = "|".join((
            kind.value, request.request_id, request.research_run_id,
            request.ledger_id, self.surface, request.input_snapshot_hash,
            str(attempt_number),
        )).encode("utf-8")
        return "MOCK-CLAIM-" + hashlib.sha256(payload).hexdigest()[:24]

    def execute(self, request, *, proof_resolver=None, attempt_number=1):
        if self._script.cannot_enforce_closed_corpus:
            return self._fail(
                ProviderOutcomeKind.PROVIDER_CAPABILITY_INSUFFICIENT,
                FAILURE_CANNOT_ENFORCE_CLOSED_CORPUS,
                "the configured mock surface cannot enforce a closed corpus",
                attempt_number,
            )
        if self._script.outcome_for(attempt_number) == "TRANSPORT_FAILURE":
            return self._fail(
                ProviderOutcomeKind.TRANSPORT_FAILURE,
                FAILURE_SCRIPTED_TRANSPORT,
                "scripted deterministic transport failure",
                attempt_number,
            )

        corpus_ids = tuple(str(s) for s in request.corpus.source_ids)
        declared = dict(request.corpus.exact_blob_hashes)

        # Request-isolated reconstruction is the default (FD #148 R-4). A deliberately
        # REUSED harness accumulates the previous request's corpus, giving the isolation
        # canary something real to detect.
        if self._reuse_context:
            self._context = set(self._context) | set(corpus_ids)
        else:
            self._context = set(corpus_ids)
        # The provider's own reported source inventory (its usable context PLUS any
        # citation it returns) must be a subset of the approved corpus: a citation
        # outside the approved corpus is a closed-corpus violation, and it is recorded
        # in the evidence so the resolver refuses it instead of it passing unnoticed.
        observed = tuple(sorted(
            set(self._context) | set(self._script.extraneous_citations)))
        extraneous = tuple(sorted(set(observed) - set(corpus_ids)))

        if self._archive is None:
            return self._fail(
                ProviderOutcomeKind.PIT_BLOCK, FAILURE_SEALED_BYTES_NOT_ADMITTED,
                "a SEALED request requires the authoritative archive to reload bytes",
                attempt_number,
            )

        sent_hashes = []
        for sid in corpus_ids:
            try:
                attestation = self._archive.get_admission_attestation(sid)
                blob = self._archive.load_raw_blob(sid)
            except Exception:
                return self._fail(
                    ProviderOutcomeKind.PIT_BLOCK, FAILURE_SEALED_ATTESTATION,
                    "source " + repr(sid)
                    + " has no archive admission attestation / blob",
                    attempt_number,
                )
            if self._script.byte_tampering:
                blob = bytes(blob) + b"!"
            digest = hashlib.sha256(blob).hexdigest()
            attested = getattr(attestation, "raw_blob_sha256", None)
            if digest != declared.get(sid) or attested != digest:
                return self._fail(
                    ProviderOutcomeKind.PIT_BLOCK, FAILURE_SEALED_BYTE_MISMATCH,
                    "source " + repr(sid)
                    + ": supplied bytes do not match the attested blob",
                    attempt_number,
                )
            sent_hashes.append((sid, digest))

        evidence = TransportEvidence(
            transport_type=self.transport_type,
            provider_surface=self.surface,
            attempt_number=attempt_number,
            sent_source_ids=tuple(sorted(corpus_ids)),
            sent_blob_hashes=tuple(sent_hashes),
            corpus_hash=request.corpus.corpus_hash,
            sealed_bytes_verified=True,
            network_used=False,
            notes="deterministic offline mock transport",
        )

        closed = self._mint_evidence(
            request, ProofKind.CLOSED_CORPUS_ENFORCEMENT, attempt_number,
            corpus_ids, observed, extraneous, True)
        isolation = self._mint_evidence(
            request, ProofKind.REQUEST_ISOLATION, attempt_number,
            corpus_ids, observed, extraneous, True)
        if self._script.withhold_closed_corpus_evidence:
            corpus_ref = self._claim_ref(
                request, ProofKind.CLOSED_CORPUS_ENFORCEMENT, attempt_number)
        else:
            corpus_ref = closed.evidence_ref
        if self._script.withhold_isolation_evidence:
            isolation_ref = self._claim_ref(
                request, ProofKind.REQUEST_ISOLATION, attempt_number)
        else:
            isolation_ref = isolation.evidence_ref
        if self._script.forced_evidence_refs is not None:
            forced = tuple(self._script.forced_evidence_refs)
            if len(forced) > 0:
                corpus_ref = forced[0]
            if len(forced) > 1:
                isolation_ref = forced[1]

        pointers = []
        for index, sid in enumerate(corpus_ids):
            pointers.append(SourcePointer(
                index=index, reference=MOCK_SOURCE_REFERENCE_PREFIX + sid))
        base = len(corpus_ids)
        for extra_index, sid in enumerate(self._script.extraneous_citations):
            pointers.append(SourcePointer(
                index=base + extra_index,
                reference=MOCK_SOURCE_REFERENCE_PREFIX + sid))
        pointers = tuple(pointers)

        try:
            result = build_deep_research_result(
                request_id=request.request_id,
                research_run_id=request.research_run_id,
                ledger_id=request.ledger_id,
                status=ResearchResultStatus.SUCCESS,
                provider_surface=self.surface,
                result_bytes=self.result_bytes,
                result_sha256=hashlib.sha256(self.result_bytes).hexdigest(),
                result_artifact_ref=self.synthesis_ref,
                source_pointers=pointers,
                closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                isolation_verification=IsolationVerification.VERIFIED,
                closed_corpus_evidence_ref=corpus_ref,
                isolation_evidence_ref=isolation_ref,
                request=request,
                proof_resolver=proof_resolver,
            )
        except ResearchResultError as exc:
            return self._fail(
                ProviderOutcomeKind.PROOF_NOT_VERIFIED, FAILURE_PROOF_NOT_VERIFIED,
                str(exc)[:300], attempt_number, evidence)

        return ProviderOutcome(
            kind=ProviderOutcomeKind.RESULT,
            provider_surface=self.surface,
            attempt_number=attempt_number,
            result=result,
            transport_evidence=evidence,
            telemetry=not_exposed_provider_telemetry(),
            evidence_refs=(corpus_ref, isolation_ref),
        )
