"""M6 SEALED source eligibility — M6.1 (FD #150).

Minimal evaluator over the archive admission attestation, used by the mandatory
combined backdating fixture. The full SEALED snapshot builder (deterministic
``input_snapshot_hash``, per-source verdict set, provider-input enforcement) is
the M6.2 cluster.

Trusted SEALED rule (FD #150 §6, M6 v1):
  A canonical SRC-01 must exist, its raw blob must exist, a valid archive
  admission attestation must exist, ``attestation.admitted_at <= AS_OF``, and the
  attestation ↔ SRC-01 ↔ raw-blob bindings must be intact. Any failure →
  ``UNAVAILABLE_FOR_SEALED_PIT`` (fail closed).
"""

from __future__ import annotations

import datetime as dt
from enum import Enum

from qad.persistence.errors import AttestationNotFound

#: FD #149/#150 — SRCV-01 alone is never sufficient evidence of exact-version
#: byte capture; ``SRCV_ONLY_CAPTURE_PROOF`` is not eligible for M6 v1 SEALED.
SRCV_ONLY_CAPTURE_PROOF_INELIGIBLE = True


class SealedEligibility(str, Enum):
    """SEALED/replay input eligibility verdict for one candidate source."""

    ELIGIBLE = "ELIGIBLE"
    UNAVAILABLE_FOR_SEALED_PIT = "UNAVAILABLE_FOR_SEALED_PIT"
    LEGACY_UNATTESTED_SRC01 = "LEGACY_UNATTESTED_SRC01"
    SRCV_ONLY_CAPTURE_PROOF = "SRCV_ONLY_CAPTURE_PROOF"
    SOURCE_NOT_FOUND = "SOURCE_NOT_FOUND"


def _has_version_records(archive, source_id: str) -> bool:
    """True if the archive holds SRCV-01 version evidence for this source.

    SRCV-01 alone is never sufficient byte-capture proof for M6 v1 SEALED
    (M5.2 §10.4 does not bind SRCV-01.content_hash to exact version bytes).
    """
    # IMPORTANT (M6.1 review R2): only ACTUAL SRCV-01 records count. The
    # RawSourceArchive store_version()/list_versions() API manages SRC-01
    # version *snapshots* and is NOT SRCV-01 evidence (M5.2 §10.4 / boundary
    # contract). Inferring SRCV-only from list_versions would misclassify.
    data = getattr(archive, "_data", None)
    if isinstance(data, dict):
        for rec in data.get("SRCV-01", {}).values():
            inst = getattr(rec, "instance", rec)
            if getattr(inst, "source_id", None) == source_id:
                return True
    return False


def evaluate_sealed_source_eligibility(
    archive, source_id: str, as_of: dt.date,
) -> SealedEligibility:
    """Evaluate whether one source is eligible as SEALED/replay input.

    ``archive`` is a RawSourceArchive (authoritative). All data is re-loaded
    from the archive itself — caller-supplied source bytes are never consulted.
    """
    if not archive.contains("SRC-01", source_id):
        return SealedEligibility.SOURCE_NOT_FOUND

    try:
        attestation = archive.get_admission_attestation(source_id)
    except AttestationNotFound:
        # No archive attestation: either a pre-attestation legacy record, or a
        # caller relying on SRCV-01 version records as the capture proof
        # (FD #149/#150: SRCV_ONLY_CAPTURE_PROOF is NOT M6 v1 SEALED-eligible).
        if _has_version_records(archive, source_id):
            return SealedEligibility.SRCV_ONLY_CAPTURE_PROOF
        return SealedEligibility.LEGACY_UNATTESTED_SRC01

    # Re-verify attestation ↔ SRC-01 ↔ raw-blob bindings from archive state.
    if not archive.verify_admission_attestation(source_id):
        return SealedEligibility.UNAVAILABLE_FOR_SEALED_PIT

    admitted_at = dt.datetime.fromisoformat(attestation.admitted_at)
    if admitted_at.date() > as_of:
        return SealedEligibility.UNAVAILABLE_FOR_SEALED_PIT

    return SealedEligibility.ELIGIBLE
