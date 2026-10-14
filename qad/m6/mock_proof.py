"""QAD M6.7 — TRUSTED MOCK PROOF RESOLVER (explicit test-boundary injection only).

Founder decision R1: a deterministic MOCK proof resolver may be injected through an
explicit test-only seam, while the M6.4 deny-all ``DEFAULT_PROOF_RESOLVER`` remains the
authoritative production default (absent injection, ``SUCCESS`` still fails closed).

This resolver is NOT a production resolver and does NOT claim to be a Gemini proof
resolver. It independently verifies evidence recorded by the deterministic M6.7 mock
harness:

* it never treats a non-empty evidence reference as proof;
* it never echoes provider-supplied identity fields and returns ``verified=True``;
* it resolves the reference to the harness's recorded OBSERVATIONS and then re-checks the
  actual property (closed-corpus inventory / request isolation) plus the exact six-field
  execution binding (request_id, research_run_id, ledger_id, provider_surface,
  input_snapshot_hash, proof_kind);
* any missing, inconsistent, unbound or unproven case returns ``verified=False`` with a
  bounded failure reason (fail closed).
"""

from __future__ import annotations

from qad.m6.mock_transport import MOCK_EVIDENCE_PRODUCER, MockEvidenceStore
from qad.m6.research_contract import (
    ProofKind,
    ProofVerification,
    ProofVerificationRequest,
)

#: Marker: this resolver is a test-only dependency, never a production resolver.
MOCK_PROOF_RESOLVER_IS_TEST_ONLY = True
MOCK_PROOF_RESOLVER_PRODUCER = "M6.7_MOCK_PROOF_RESOLVER"

REASON_NO_EVIDENCE = "NO_MOCK_EXECUTION_EVIDENCE"
REASON_INCONSISTENT_REF = "EVIDENCE_REFERENCE_NOT_SELF_CONSISTENT"
REASON_NOT_HARNESS_PRODUCED = "EVIDENCE_NOT_PRODUCED_BY_THE_MOCK_HARNESS"
REASON_BINDING = "BINDING_MISMATCH"
REASON_CLOSED_CORPUS = "CLOSED_CORPUS_ENFORCEMENT_NOT_PROVEN"
REASON_SEALED_BYTES = "SEALED_BYTES_NOT_VERIFIED"
REASON_ISOLATION = "REQUEST_ISOLATION_NOT_PROVEN"
REASON_UNKNOWN_KIND = "UNKNOWN_PROOF_KIND"

_BOUND_FIELDS = (
    "request_id",
    "research_run_id",
    "ledger_id",
    "provider_surface",
    "input_snapshot_hash",
)


class MockProofResolver:
    """Deterministic mock proof resolver (test-boundary injection only)."""

    __slots__ = ("_evidence",)

    def __init__(self, evidence_store: MockEvidenceStore) -> None:
        if not isinstance(evidence_store, MockEvidenceStore):
            raise TypeError(
                "MockProofResolver requires the mock harness's MockEvidenceStore"
            )
        self._evidence = evidence_store

    @property
    def evidence_store(self) -> MockEvidenceStore:
        return self._evidence

    @staticmethod
    def _unverified(context: ProofVerificationRequest, reason: str) -> ProofVerification:
        return ProofVerification(
            proof_kind=context.proof_kind,
            verified=False,
            request_id=context.request_id,
            research_run_id=context.research_run_id,
            ledger_id=context.ledger_id,
            provider_surface=context.provider_surface,
            input_snapshot_hash=context.input_snapshot_hash,
            evidence_ref=None,
            failure_reason=reason,
        )

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        """Verify ONE proof kind for the exact run described by ``context``."""
        record = self._evidence.resolve(context.evidence_ref)
        if record is None:
            # A non-empty reference string is NOT proof: nothing was recorded for it.
            return self._unverified(context, REASON_NO_EVIDENCE)
        if record.evidence_ref != record.recompute_ref():
            # The record was edited after the harness wrote it.
            return self._unverified(context, REASON_INCONSISTENT_REF)
        if record.producer != MOCK_EVIDENCE_PRODUCER:
            return self._unverified(context, REASON_NOT_HARNESS_PRODUCED)

        for field in _BOUND_FIELDS:
            if getattr(record, field) != getattr(context, field):
                return self._unverified(context, REASON_BINDING + ":" + field)
        if record.proof_kind is not context.proof_kind:
            return self._unverified(context, REASON_BINDING + ":proof_kind")

        # The property is re-checked from the RECORDED OBSERVATIONS — never echoed.
        if context.proof_kind is ProofKind.CLOSED_CORPUS_ENFORCEMENT:
            if not record.sealed_bytes_verified:
                return self._unverified(context, REASON_SEALED_BYTES)
            if not record.inventory_is_closed:
                return self._unverified(context, REASON_CLOSED_CORPUS)
        elif context.proof_kind is ProofKind.REQUEST_ISOLATION:
            if not record.context_is_isolated:
                return self._unverified(context, REASON_ISOLATION)
        else:
            return self._unverified(context, REASON_UNKNOWN_KIND)

        return ProofVerification(
            proof_kind=context.proof_kind,
            verified=True,
            request_id=context.request_id,
            research_run_id=context.research_run_id,
            ledger_id=context.ledger_id,
            provider_surface=context.provider_surface,
            input_snapshot_hash=context.input_snapshot_hash,
            evidence_ref=context.evidence_ref,
            failure_reason=None,
        )
