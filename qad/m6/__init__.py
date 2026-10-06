"""QAD M6 — Source Intelligence / Gemini Notebook Engineering (FD #151).

Deterministic M6 core, implemented cluster by cluster behind the frozen QAD
abstractions. M6.1 (archive admission attestation) lives here in ``eligibility``;
later clusters (SEALED snapshot builder, run ledger, provider adapter) follow in
dependency order per FD #151.
"""

from __future__ import annotations

from qad.m6.eligibility import (
    SealedEligibility,
    SRCV_ONLY_CAPTURE_PROOF_INELIGIBLE,
    evaluate_sealed_source_eligibility,
)

__all__ = [
    "SealedEligibility",
    "SRCV_ONLY_CAPTURE_PROOF_INELIGIBLE",
    "evaluate_sealed_source_eligibility",
]
