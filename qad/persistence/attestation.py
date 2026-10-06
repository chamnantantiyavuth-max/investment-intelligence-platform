"""Archive admission attestation — M6.1 (FD #150 design / FD #151 implementation).

Archive-owned, **immutable** admission metadata created by the RawSourceArchive
admission boundary itself. It is **NOT** a canonical M4A investment schema; it is
**NOT** the Research Room state; it is **NOT** the DeepResearchRunLedger. It is
the trusted SEALED capture proof for M6 v1.

Why it exists
-------------
``RawSourceArchive.admit_source`` binds raw bytes to ``SRC-01.content_hash``, but
the caller constructs the ``SRC-01`` instance (including ``retrieval_date``)
*before* admission. ``SRC-01.retrieval_date`` is therefore source/provenance
metadata and MUST NOT be treated as authoritative proof that the exact bytes
existed in the archive at that historical time. The trusted capture time is
``ArchiveAdmissionAttestation.admitted_at``, generated **inside** the archive
boundary from an archive-owned clock.

Deterministic tests may inject the archive clock; production caller paths MUST
NOT be able to supply historical ``admitted_at`` values.

See: design/qad-pivot/m6/QAD-M6.0-DESIGN-GATE-RECONCILIATION.md §5;
design/qad-pivot/m5/QAD-M5.2-PERSISTENCE-BOUNDARY-CONTRACT.md §2.1.1.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import uuid
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

ATTESTATION_FORMAT_VERSION = "1"

#: The only admission path that produces an attestation in M6 v1.
ADMISSION_METHOD_ADMIT_SOURCE = "ADMIT_SOURCE"

#: Legacy SRC-01 records created before attestation support are NOT eligible for
#: M6 v1 SEALED operation (FD #150). Never synthesize an old ``admitted_at``.
LEGACY_UNATTESTED = "LEGACY_UNATTESTED_SRC01"


def utc_now() -> _dt.datetime:
    """Archive-owned default clock: timezone-aware UTC 'now'."""
    return _dt.datetime.now(_dt.timezone.utc)


@runtime_checkable
class ArchiveClock(Protocol):
    """Archive-owned clock provider.

    Production callers cannot inject or supply this; only the archive holds a
    reference. Deterministic tests MAY construct an archive with a fixed clock.
    """

    def __call__(self) -> _dt.datetime:  # pragma: no cover - protocol
        ...


def _iso_utc(ts: _dt.datetime) -> str:
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=_dt.timezone.utc)
    return ts.astimezone(_dt.timezone.utc).isoformat()


@dataclass(frozen=True)
class ArchiveAdmissionAttestation:
    """Immutable archive admission attestation (FD #150).

    Frozen dataclass — deliberately NOT a canonical M4A schema and NOT a
    Pydantic canonical record, so it can never be admitted through the canonical
    stores.
    """

    attestation_id: str
    source_id: str
    source_ref: str                      # canonical SRC-01 reference
    source_content_hash: str             # == SRC-01.content_hash
    raw_blob_sha256: str                 # == sha256(stored raw bytes)
    raw_byte_length: int
    admitted_at: str                     # ISO-8601 UTC, archive-owned
    archive_instance: str
    admission_method: str
    attestation_format_version: str = ATTESTATION_FORMAT_VERSION
    # -- optional ----------------------------------------------------------
    transaction_ref: str | None = None
    storage_backend: str | None = None
    external_time_attestation_ref: str | None = None


def build_attestation(
    *,
    source_id: str,
    source_content_hash: str,
    raw_bytes: bytes,
    admitted_at: _dt.datetime,
    archive_instance: str,
    admission_method: str = ADMISSION_METHOD_ADMIT_SOURCE,
    transaction_ref: str | None = None,
    storage_backend: str | None = None,
    external_time_attestation_ref: str | None = None,
) -> ArchiveAdmissionAttestation:
    """Construct an attestation INSIDE the archive boundary.

    This helper only ever runs within the archive; it deliberately takes no
    caller-facing ``admitted_at`` source other than the archive's own clock.
    """
    return ArchiveAdmissionAttestation(
        attestation_id=str(uuid.uuid4()),
        source_id=source_id,
        source_ref=f"SRC-01:{source_id}",
        source_content_hash=source_content_hash,
        raw_blob_sha256=hashlib.sha256(raw_bytes).hexdigest(),
        raw_byte_length=len(raw_bytes),
        admitted_at=_iso_utc(admitted_at),
        archive_instance=archive_instance,
        admission_method=admission_method,
        transaction_ref=transaction_ref,
        storage_backend=storage_backend,
        external_time_attestation_ref=external_time_attestation_ref,
    )


def verify_attestation_binding(
    *, attestation: ArchiveAdmissionAttestation,
    stored_raw_bytes: bytes, src_content_hash: str,
) -> bool:
    """Recompute the attestation ↔ SRC-01 ↔ raw-blob bindings (FD #150 C–I).

    Returns ``True`` only if every binding is intact. The caller is responsible
    for having re-loaded ``stored_raw_bytes`` and the SRC-01 record from the
    authoritative archive (never from caller-supplied detached bytes).
    """
    if attestation.source_content_hash != src_content_hash:
        return False
    if attestation.raw_blob_sha256 != src_content_hash:
        return False
    if hashlib.sha256(stored_raw_bytes).hexdigest() != attestation.raw_blob_sha256:
        return False
    if len(stored_raw_bytes) != attestation.raw_byte_length:
        return False
    return True
