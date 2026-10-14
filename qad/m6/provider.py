"""QAD M6.7 — PROVIDER ADAPTER CONTRACT (non-canonical, operational).

FD #151 places provider execution in M6.7 (Provider Adapter + Mock Transport) behind the
already-frozen M6.4/M6.5 contracts. This module defines ONLY the provider-neutral adapter
boundary:

* no transport detail ever appears on a canonical or M6.4 domain contract (FD #148 §R-2:
  "do not hardwire consumer UI/browser hacks into canonical domain contracts");
* the adapter receives an already-built immutable :class:`DeepResearchRequest` and returns a
  bounded :class:`ProviderOutcome` — it never mutates the ledger, never classifies retry
  policy and never mints a proof;
* the protocol carries NO credential parameter (credentials are an M6.8 adapter-internal
  concern and may never reach the repo, logs, artifacts or the ledger).

M6.7 ships a deterministic MOCK transport only (Founder decisions R3/R4). No Gemini
Notebook integration, no browser/CDP automation, no network, no live provider call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from qad.m6.ledger import REQUIRED_TELEMETRY_METRICS, TelemetryStatus
from qad.m6.research_contract import (
    DeepResearchRequest,
    DeepResearchResult,
    ProviderConfiguration,
)

#: The M6.7 mock provider surface / transport identity (recorded per run on the ledger).
MOCK_PROVIDER_SURFACE = "gemini_notebook_mock"
MOCK_TRANSPORT_TYPE = "MOCK_DETERMINISTIC_TRANSPORT"

#: Truthful telemetry reason for the mock surface: it exposes no model/token/cost data.
MOCK_PROVIDER_NOT_EXPOSED_REASON = "NOT_EXPOSED_BY_MOCK_PROVIDER"

#: Bounded failure codes (never free-form). M6.0 §8 vocabulary where one exists.
FAILURE_SCRIPTED_TRANSPORT = "MOCK_SCRIPTED_TRANSPORT_FAILURE"
FAILURE_PROVIDER_SHAPE = "MOCK_PROVIDER_RESPONSE_SHAPE_CHANGED"
FAILURE_SEALED_BYTES_NOT_ADMITTED = "MOCK_SEALED_BYTES_NOT_ADMITTED"
FAILURE_SEALED_BYTE_MISMATCH = "MOCK_SEALED_BYTE_HASH_MISMATCH"
FAILURE_SEALED_ATTESTATION = "MOCK_SEALED_SOURCE_NOT_ATTESTED"
FAILURE_PROOF_NOT_VERIFIED = "MOCK_PROOF_NOT_VERIFIED"
FAILURE_CANNOT_ENFORCE_CLOSED_CORPUS = "PROVIDER_CANNOT_ENFORCE_SEALED_INPUT"


class ProviderAdapterError(Exception):
    """The provider adapter contract was violated."""


class ProviderOutcomeKind(str, Enum):
    """Bounded adapter outcome vocabulary (M6.0 §8 aligned)."""

    RESULT = "RESULT"
    TRANSPORT_FAILURE = "TRANSPORT_FAILURE"
    PIT_BLOCK = "PIT_BLOCK"
    PROVIDER_CAPABILITY_INSUFFICIENT = "PROVIDER_CAPABILITY_INSUFFICIENT"
    PROOF_NOT_VERIFIED = "PROOF_NOT_VERIFIED"


@dataclass(frozen=True)
class TransportEvidence:
    """What the adapter actually did — NON-CANONICAL operational evidence.

    Deliberately separate from every domain contract: transport detail stays behind the
    adapter boundary (FD #148 §R-2) and is never promoted into SRC-01 / EV-01 / the
    canonical provenance chain.
    """

    transport_type: str
    provider_surface: str
    attempt_number: int
    sent_source_ids: tuple[str, ...] = ()
    sent_blob_hashes: tuple[tuple[str, str], ...] = ()
    corpus_hash: str = ""
    sealed_bytes_verified: bool = False
    network_used: bool = False
    notes: str = ""

    def __post_init__(self) -> None:
        for name in ("transport_type", "provider_surface", "corpus_hash"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ProviderAdapterError(
                    f"transport evidence requires a non-blank {name}"
                )
        if not isinstance(self.attempt_number, int) or isinstance(
            self.attempt_number, bool
        ) or self.attempt_number < 1:
            raise ProviderAdapterError(
                "transport evidence requires a positive integer attempt_number"
            )
        object.__setattr__(self, "sent_source_ids", tuple(self.sent_source_ids))
        object.__setattr__(
            self,
            "sent_blob_hashes",
            tuple((str(s), str(h)) for s, h in self.sent_blob_hashes),
        )
        if not isinstance(self.sealed_bytes_verified, bool):
            raise ProviderAdapterError("sealed_bytes_verified must be a bool")
        if not isinstance(self.network_used, bool):
            raise ProviderAdapterError("network_used must be a bool")


@dataclass(frozen=True)
class ProviderOutcome:
    """A bounded adapter outcome: exactly one result envelope OR one bounded failure."""

    kind: ProviderOutcomeKind
    provider_surface: str
    attempt_number: int
    result: DeepResearchResult | None = None
    failure_code: str | None = None
    diagnostic: str = ""
    transport_evidence: TransportEvidence | None = None
    telemetry: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ProviderOutcomeKind):
            raise ProviderAdapterError("kind must be a ProviderOutcomeKind")
        if not isinstance(self.provider_surface, str) or not self.provider_surface.strip():
            raise ProviderAdapterError("provider_surface must be a non-blank string")
        if not isinstance(self.attempt_number, int) or isinstance(
            self.attempt_number, bool
        ) or self.attempt_number < 1:
            raise ProviderAdapterError("attempt_number must be a positive integer")
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))
        if self.kind is ProviderOutcomeKind.RESULT:
            if self.result is None:
                raise ProviderAdapterError("a RESULT outcome must carry the result")
            if self.failure_code is not None:
                raise ProviderAdapterError("a RESULT outcome must not carry a failure_code")
        else:
            if not isinstance(self.failure_code, str) or not self.failure_code.strip():
                raise ProviderAdapterError(
                    "a failure outcome requires a non-blank bounded failure_code"
                )

    @property
    def is_success(self) -> bool:
        """True only for a SUCCESS result envelope (never for a failure outcome)."""
        return (
            self.kind is ProviderOutcomeKind.RESULT
            and self.result is not None
            and self.result.is_success
        )


def not_exposed_provider_telemetry(
    reason: str = MOCK_PROVIDER_NOT_EXPOSED_REASON,
) -> dict[str, Any]:
    """A truthful NOT_EXPOSED telemetry record with an explicit reason (M6.0 §2).

    Never zero-as-unknown and never estimated: the mock surface exposes no model identity,
    token usage, cost or provider-reported model version, so each REQUIRED metric is
    recorded as NOT_EXPOSED with the reason.
    """
    if not isinstance(reason, str) or not reason.strip():
        raise ProviderAdapterError("a NOT_EXPOSED reason must be non-blank")
    return {
        metric: {
            "status": TelemetryStatus.NOT_EXPOSED.value,
            "value": None,
            "reason": reason,
        }
        for metric in REQUIRED_TELEMETRY_METRICS
    }


@runtime_checkable
class DeepResearchProvider(Protocol):
    """Provider-neutral adapter interface (interface only — no transport detail)."""

    surface: str
    transport_type: str

    def capability(self) -> ProviderConfiguration:
        """The provider-neutral capability declaration (M6.4 type, unchanged)."""
        ...

    def execute(
        self,
        request: DeepResearchRequest,
        *,
        proof_resolver: Any = None,
        attempt_number: int = 1,
    ) -> ProviderOutcome:
        """Execute ONE attempt and return a bounded outcome.

        ``proof_resolver`` is the TRUSTED orchestration dependency (FD #152); it is never
        provider-supplied data. ``attempt_number`` selects the deterministic scripted
        behaviour for deterministic tests.
        """
        ...
