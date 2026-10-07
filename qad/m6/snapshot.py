"""M6.2 — SEALED Input Snapshot Builder / PIT boundary (FD #150 design / FD #151 impl).

Builds an immutable, reproducible provider-input snapshot from **authoritative**
inputs only:

  * the authoritative PIT context (``PITC-01`` resolved from ``PITContextStore``
    by ``pit_context_id`` — never a caller-supplied AS_OF / mode / case_id), and
  * the authoritative RawSourceArchive records (canonical SRC-01 + exact stored
    raw bytes + ``ArchiveAdmissionAttestation`` — never caller-supplied bytes,
    hashes, attestations, or timestamps).

Core invariant
--------------
``SEALED input is constructed ONLY from exact archive-attested raw bytes that
were admitted at or before AS_OF.``

This cluster contains **no** provider transport, no web retrieval, and no Gemini
Notebook call. It defines — but does not fake — the downstream closed-corpus
contract (``closed_corpus_required``).

The structures here are M6 request-boundary structures. They are **NOT** new
M4A canonical schemas: nothing here is registered in the canonical schema set,
and the private hash-payload models below exist only to reuse the accepted
deterministic serialiser (``qad.persistence.serialization``).

See: design/qad-pivot/m6/QAD-M6.0-DESIGN-GATE-RECONCILIATION.md (11-condition
SEALED rule), FD #150, FD #151.
"""

from __future__ import annotations

import datetime as dt
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel

from qad.m6.eligibility import SealedEligibility, evaluate_sealed_source_eligibility
from qad.persistence.attestation import utc_now
from qad.persistence.errors import AttestationNotFound
from qad.persistence.serialization import compute_canonical_hash

#: The only PITC-01 mode accepted by the SEALED builder.
SEALED_PIT_MODE = "SEALED_HISTORICAL_EVALUATION"

#: Downstream contract marker: provider adapters MUST NOT augment SEALED input
#: (web search, provider-native discovery, prior Notebook corpora/chats, hidden
#: persistent workspace sources). A provider that cannot prove this fails closed
#: with ``PROVIDER_CANNOT_ENFORCE_SEALED_INPUT`` (M6.7/M6.8).
PROVIDER_CANNOT_ENFORCE_SEALED_INPUT = "PROVIDER_CANNOT_ENFORCE_SEALED_INPUT"


class SnapshotFailureCode(str, Enum):
    """Deterministic typed outcomes for SEALED snapshot construction."""

    UNAVAILABLE_FOR_SEALED_PIT = "UNAVAILABLE_FOR_SEALED_PIT"
    PIT_CONTEXT_NOT_FOUND = "PIT_CONTEXT_NOT_FOUND"
    PIT_CONTEXT_UNAVAILABLE = "PIT_CONTEXT_UNAVAILABLE"
    PIT_MODE_NOT_SEALED = "PIT_MODE_NOT_SEALED"
    ARCHIVE_UNAVAILABLE = "ARCHIVE_UNAVAILABLE"
    SOURCE_NOT_FOUND = "SOURCE_NOT_FOUND"
    LEGACY_UNATTESTED_SRC01 = "LEGACY_UNATTESTED_SRC01"
    SRCV_ONLY_CAPTURE_PROOF = "SRCV_ONLY_CAPTURE_PROOF"
    ATTESTATION_INTEGRITY_FAILURE = "ATTESTATION_INTEGRITY_FAILURE"
    SOURCE_ADMITTED_AFTER_AS_OF = "SOURCE_ADMITTED_AFTER_AS_OF"
    SOURCE_PUBLICATION_DATE_MISSING = "SOURCE_PUBLICATION_DATE_MISSING"
    SOURCE_PUBLISHED_AFTER_AS_OF = "SOURCE_PUBLISHED_AFTER_AS_OF"
    RAW_BLOB_UNAVAILABLE = "RAW_BLOB_UNAVAILABLE"
    DUPLICATE_SOURCE_ID = "DUPLICATE_SOURCE_ID"
    SNAPSHOT_BUILD_FAILED = "SNAPSHOT_BUILD_FAILED"


class SnapshotBuildError(Exception):
    """Deterministic snapshot-build failure.

    ``code`` is the aggregate outcome; ``verdicts`` maps every REQUESTED source
    id to its per-source failure code (``None`` = eligible). A non-empty verdict
    map with any non-None value means the whole snapshot was refused — M6 v1 is
    strict: no silent partial corpus.
    """

    def __init__(self, code: SnapshotFailureCode, message: str,
                 verdicts: dict[str, SnapshotFailureCode | None] | None = None,
                 *, reason_code: SnapshotFailureCode | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.reason_code = reason_code or code
        self.verdicts: dict[str, SnapshotFailureCode | None] = dict(verdicts or {})


@dataclass(frozen=True)
class SealedSourceSnapshot:
    """Immutable verified provenance + exact bytes for ONE sealed source."""

    source_id: str
    source_content_hash: str
    raw_blob_sha256: str
    raw_byte_length: int
    archive_attestation_id: str
    archive_admitted_at: str
    raw_bytes: bytes                      # exact archive-loaded, hash-verified bytes
    eligibility_verdict: str = SealedEligibility.ELIGIBLE.value


@dataclass(frozen=True)
class SealedInputSnapshot:
    """Immutable SEALED provider-input snapshot (canonical order, deterministic identity)."""

    snapshot_id: str                      # == input_snapshot_hash (deterministic identity)
    case_id: str
    case_version: str
    pit_context_id: str
    pit_mode: str
    as_of: str
    ordered_sources: tuple[SealedSourceSnapshot, ...]
    source_count: int
    input_snapshot_hash: str
    closed_corpus_required: bool = True
    created_at: str | None = None         # operational metadata — NOT part of identity


# ---------------------------------------------------------------------------
# PRIVATE hash-payload models (not canonical M4A schemas; serialiser input only)
# ---------------------------------------------------------------------------

class _OrderedSourceRef(BaseModel):
    # M6.0 identity uses the exact hash of admitted bytes, not source metadata.
    source_id: str
    exact_blob_hash: str


class _SealedInputSnapshotIdentity(BaseModel):
    case_id: str
    case_version: str
    pit_mode: str
    as_of: str
    sources: list[_OrderedSourceRef]


def input_snapshot_identity_payload(
    *, case_id: str, case_version: str, pit_mode: str,
    as_of: str, ordered: tuple[SealedSourceSnapshot, ...],
) -> dict[str, Any]:
    """The exact deterministic identity contract approved by M6.0.

    PIT context id remains snapshot provenance, not identity. Attestation ids,
    source metadata hashes, and operational metadata are also excluded.
    """
    return {
        "case_id": case_id,
        "case_version": case_version,
        "pit_mode": pit_mode,
        "as_of": as_of,
        "sources": [
            {
                "source_id": s.source_id,
                "exact_blob_hash": s.raw_blob_sha256,
            }
            for s in ordered
        ],
    }


def _compute_input_snapshot_hash(
    *, case_id: str, case_version: str, pit_mode: str,
    as_of: str, ordered: tuple[SealedSourceSnapshot, ...],
) -> str:
    payload = input_snapshot_identity_payload(
        case_id=case_id, case_version=case_version, pit_mode=pit_mode,
        as_of=as_of, ordered=ordered,
    )
    # reuse the accepted deterministic canonical serializer
    return compute_canonical_hash(_SealedInputSnapshotIdentity(
        case_id=payload["case_id"],
        case_version=payload["case_version"],
        pit_mode=payload["pit_mode"],
        as_of=payload["as_of"],
        sources=[_OrderedSourceRef(**s) for s in payload["sources"]],
    ))


# ---------------------------------------------------------------------------
# Per-source resolution (archive is the ONLY authority)
# ---------------------------------------------------------------------------

_INTEGRITY = SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE


def _sealed_source_time_check(src, as_of: dt.date) -> SnapshotFailureCode | None:
    """S7 SEALED source-time rule (upstream guard; S7 itself remains authoritative).

    SEALED requires SRC-01.publication_date and it must be <= AS_OF. Missing or
    uninterpretable metadata fails closed (M6 design §9; S7 FD #138).
    """
    pub = getattr(src, "publication_date", None)
    if not pub:
        return SnapshotFailureCode.SOURCE_PUBLICATION_DATE_MISSING
    # Mirror S7's parser (qad/m53/pit_enforcement.py _parse_date): an ISO datetime
    # form (``2025-11-20T09:00:00``) reduces to its date part; anything
    # uninterpretable fails closed.
    text = str(pub).strip()
    if "T" in text:
        text = text.split("T", 1)[0]
    try:
        pub_date = dt.date.fromisoformat(text)
    except ValueError:
        return SnapshotFailureCode.SOURCE_PUBLICATION_DATE_MISSING
    if pub_date > as_of:
        return SnapshotFailureCode.SOURCE_PUBLISHED_AFTER_AS_OF
    return None


def _classify_unattested(archive, source_id: str, as_of: dt.date) -> SnapshotFailureCode:
    """Classify a source with no archive attestation (fail closed)."""
    verdict = evaluate_sealed_source_eligibility(archive, source_id, as_of)
    if verdict is SealedEligibility.SOURCE_NOT_FOUND:
        return SnapshotFailureCode.SOURCE_NOT_FOUND
    if verdict is SealedEligibility.SRCV_ONLY_CAPTURE_PROOF:
        return SnapshotFailureCode.SRCV_ONLY_CAPTURE_PROOF
    return SnapshotFailureCode.LEGACY_UNATTESTED_SRC01


def _resolve_source(
    archive, as_of: dt.date, source_id: str,
) -> tuple[SealedSourceSnapshot | None, SnapshotFailureCode | None]:
    """Resolve ONE source from archive truth and apply the FD #150 A–K rule.

    Returns ``(snapshot, None)`` when eligible, else ``(None, failure_code)``.
    Caller-supplied objects/bytes/hashes/attestations/timestamps are never
    accepted — only the ``source_id`` crosses this boundary.
    """
    # C — archive attestation exists
    try:
        att = archive.get_admission_attestation(source_id)
    except AttestationNotFound:
        return None, _classify_unattested(archive, source_id, as_of)
    except Exception:  # noqa: BLE001 — adapter cannot provide authority
        return None, SnapshotFailureCode.ARCHIVE_UNAVAILABLE

    # A — canonical SRC-01 exists
    try:
        src = archive.load("SRC-01", source_id)
    except KeyError:
        return None, SnapshotFailureCode.SOURCE_NOT_FOUND
    except Exception:  # noqa: BLE001 — archive cannot provide canonical source
        return None, SnapshotFailureCode.ARCHIVE_UNAVAILABLE

    # S7 SEALED source-time guard (publication_date required + pre-AS_OF)
    st = _sealed_source_time_check(src, as_of)
    if st is not None:
        return None, st

    # B — raw blob exists
    try:
        blob = bytes(archive.load_raw_blob(source_id))
    except KeyError:
        return None, SnapshotFailureCode.RAW_BLOB_UNAVAILABLE
    except Exception:  # noqa: BLE001 — archive cannot provide exact bytes
        return None, SnapshotFailureCode.ARCHIVE_UNAVAILABLE

    # K — re-verify bindings NOW (construction time), not from an earlier result
    try:
        verified = archive.verify_admission_attestation(source_id)
    except AttestationNotFound:
        return None, _INTEGRITY
    except Exception:  # noqa: BLE001 — archive cannot verify authority
        return None, SnapshotFailureCode.ARCHIVE_UNAVAILABLE
    if not verified:
        return None, _INTEGRITY

    # E,H — identity + hash binding (explicit, independent of the archive helper)
    if att.source_id != source_id or att.source_id != src.source_id:
        return None, _INTEGRITY
    if att.source_ref != f"SRC-01:{source_id}":
        return None, _INTEGRITY
    # F
    if att.source_content_hash != src.content_hash:
        return None, _INTEGRITY
    # G
    if hashlib.sha256(blob).hexdigest() != att.raw_blob_sha256:
        return None, _INTEGRITY
    # H
    if att.raw_blob_sha256 != src.content_hash:
        return None, _INTEGRITY
    # I
    if len(blob) != att.raw_byte_length:
        return None, _INTEGRITY

    # D — admitted_at <= AS_OF
    try:
        admitted_at = dt.datetime.fromisoformat(att.admitted_at)
    except (TypeError, ValueError):
        return None, _INTEGRITY
    if admitted_at.date() > as_of:
        return None, SnapshotFailureCode.SOURCE_ADMITTED_AFTER_AS_OF

    # J — the snapshot carries exactly the verified bytes object
    return SealedSourceSnapshot(
        source_id=source_id,
        source_content_hash=src.content_hash,
        raw_blob_sha256=att.raw_blob_sha256,
        raw_byte_length=len(blob),
        archive_attestation_id=att.attestation_id,
        archive_admitted_at=att.admitted_at,
        raw_bytes=blob,
        eligibility_verdict=SealedEligibility.ELIGIBLE.value,
    ), None


def _fail(source_id: str, why: str,
          reason_code: SnapshotFailureCode = _INTEGRITY) -> None:
    raise SnapshotBuildError(
        SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT,
        f"{source_id}: {why}",
        {source_id: reason_code},
        reason_code=reason_code,
    )


def _finalization_revalidation(archive, as_of: dt.date,
                               ordered: tuple[SealedSourceSnapshot, ...]) -> None:
    """K — RELOAD and revalidate every archive binding immediately before finalisation.

    Re-reads the archive (attestation, SRC-01, raw blob) rather than trusting values
    captured earlier, and confirms the captured bytes are byte-identical to the
    archive's current stored bytes.
    """
    for s in ordered:
        try:
            att = archive.get_admission_attestation(s.source_id)
        except AttestationNotFound:
            _fail(s.source_id, "archive attestation missing at finalisation", _INTEGRITY)
        except Exception:
            _fail(s.source_id, "archive attestation unavailable at finalisation",
                  SnapshotFailureCode.ARCHIVE_UNAVAILABLE)
        try:
            src = archive.load("SRC-01", s.source_id)
        except KeyError:
            _fail(s.source_id, "canonical SRC-01 missing at finalisation",
                  SnapshotFailureCode.SOURCE_NOT_FOUND)
        except Exception:
            _fail(s.source_id, "canonical SRC-01 unavailable at finalisation",
                  SnapshotFailureCode.ARCHIVE_UNAVAILABLE)
        try:
            blob = bytes(archive.load_raw_blob(s.source_id))
        except KeyError:
            _fail(s.source_id, "raw blob missing at finalisation",
                  SnapshotFailureCode.RAW_BLOB_UNAVAILABLE)
        except Exception:
            _fail(s.source_id, "raw blob unavailable at finalisation",
                  SnapshotFailureCode.ARCHIVE_UNAVAILABLE)
        try:
            verified = archive.verify_admission_attestation(s.source_id)
        except AttestationNotFound:
            _fail(s.source_id, "archive attestation missing at finalisation", _INTEGRITY)
        except Exception:
            _fail(s.source_id, "archive verification unavailable at finalisation",
                  SnapshotFailureCode.ARCHIVE_UNAVAILABLE)
        if not verified:
            _fail(s.source_id, "archive verification failed at finalisation", _INTEGRITY)
        # R1-1: bind the RELOADED SRC-01 to the finalised source, and bind the
        # reloaded attestation to the provenance captured in the snapshot so a
        # superseded/replaced attestation cannot silently pass finalisation.
        if getattr(src, "source_id", None) != s.source_id:
            _fail(s.source_id, "reloaded SRC-01 identity mismatch at finalisation")
        if src.content_hash != s.source_content_hash:
            _fail(s.source_id, "reloaded SRC-01 content hash mismatch at finalisation")
        if att.attestation_id != s.archive_attestation_id:
            _fail(s.source_id, "attestation replaced/superseded at finalisation")
        if att.admitted_at != s.archive_admitted_at:
            _fail(s.source_id, "attestation admission time changed at finalisation")
        st = _sealed_source_time_check(src, as_of)
        if st is not None:
            _fail(s.source_id, f"SEALED source-time check failed at finalisation ({st.value})", st)
        if att.source_id != s.source_id or att.source_ref != f"SRC-01:{s.source_id}":
            _fail(s.source_id, "attestation source identity broken at finalisation")
        if att.source_content_hash != src.content_hash:
            _fail(s.source_id, "attestation/content-hash binding broken at finalisation")
        if att.raw_blob_sha256 != src.content_hash:
            _fail(s.source_id, "raw-blob-hash/content-hash binding broken at finalisation")
        if len(blob) != att.raw_byte_length:
            _fail(s.source_id, "attested byte length mismatch at finalisation")
        try:
            admitted = dt.datetime.fromisoformat(att.admitted_at)
        except (TypeError, ValueError):
            _fail(s.source_id, "admission timestamp unreadable at finalisation", _INTEGRITY)
        if admitted.date() > as_of:
            _fail(s.source_id, "source admitted after AS_OF at finalisation",
                  SnapshotFailureCode.SOURCE_ADMITTED_AFTER_AS_OF)
        if blob != s.raw_bytes:
            _fail(s.source_id, "captured bytes differ from archive bytes at finalisation")
        if hashlib.sha256(s.raw_bytes).hexdigest() != s.raw_blob_sha256:
            _fail(s.source_id, "bytes changed between verification and finalisation")
        if len(s.raw_bytes) != s.raw_byte_length:
            _fail(s.source_id, "byte length changed at finalisation")


# ---------------------------------------------------------------------------
# Public builder
# ---------------------------------------------------------------------------

def build_sealed_input_snapshot(
    *,
    pit_context_store,
    archive,
    pit_context_id: str,
    case_version: str,
    source_ids: list[str] | tuple[str, ...],
    clock: Callable[[], dt.datetime] | None = None,
) -> SealedInputSnapshot:
    """Build the immutable SEALED provider-input snapshot (fail closed).

    Authority:
      * PIT context — resolved from ``pit_context_store`` by ``pit_context_id``
        (``PITC-01``); caller-supplied as_of / mode / case_id are never used.
      * Sources — resolved from ``archive`` by ``source_id`` only.

    Raises:
      SnapshotBuildError: PIT missing/unreadable/non-SEALED, duplicate ids, or any
        requested source failing an FD #150 condition (strict: the WHOLE snapshot
        is refused — never a silent partial corpus).
    """
    # ---- PIT authority -------------------------------------------------
    try:
        pitc = pit_context_store.load("PITC-01", pit_context_id)
    except KeyError:
        raise SnapshotBuildError(
            SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT,
            f"PITC-01/{pit_context_id}: not found",
            reason_code=SnapshotFailureCode.PIT_CONTEXT_NOT_FOUND,
        ) from None
    except Exception as exc:  # noqa: BLE001 — unreadable store fails closed
        raise SnapshotBuildError(
            SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT,
            f"PITC-01/{pit_context_id}: unavailable ({type(exc).__name__})",
            reason_code=SnapshotFailureCode.PIT_CONTEXT_UNAVAILABLE,
        ) from exc

    mode = str(getattr(pitc, "mode", None) and getattr(pitc.mode, "value", pitc.mode))
    if mode != SEALED_PIT_MODE:
        raise SnapshotBuildError(
            SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT,
            f"PITC-01/{pit_context_id}: mode={mode} is not {SEALED_PIT_MODE}",
            reason_code=SnapshotFailureCode.PIT_MODE_NOT_SEALED,
        )

    case_id = pitc.case_id
    try:
        as_of = dt.date.fromisoformat(pitc.as_of_date)
    except (TypeError, ValueError) as exc:
        raise SnapshotBuildError(
            SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT,
            f"PITC-01/{pit_context_id}: invalid AS_OF date",
            reason_code=SnapshotFailureCode.PIT_CONTEXT_UNAVAILABLE,
        ) from exc

    # ---- duplicate policy (reject caller error, never silently dedupe) --
    requested = list(source_ids)
    if len(set(requested)) != len(requested):
        dupes = sorted({s for s in requested if requested.count(s) > 1})
        raise SnapshotBuildError(
            SnapshotFailureCode.DUPLICATE_SOURCE_ID,
            f"duplicate requested source ids: {dupes}",
            {s: SnapshotFailureCode.DUPLICATE_SOURCE_ID for s in dupes},
        )

    # ---- canonical deterministic ordering (order-invariant hash) --------
    ordered_ids = sorted(requested)

    verdicts: dict[str, SnapshotFailureCode | None] = {}
    resolved: list[SealedSourceSnapshot] = []
    internal_failure: Exception | None = None
    for sid in ordered_ids:
        try:
            snap, code = _resolve_source(archive, as_of, sid)
        except Exception as exc:  # noqa: BLE001 — preserve unexpected implementation failures
            snap, code = None, SnapshotFailureCode.SNAPSHOT_BUILD_FAILED
            if internal_failure is None:
                internal_failure = exc
        verdicts[sid] = code
        if code is None and snap is not None:
            resolved.append(snap)

    if any(v is not None for v in verdicts.values()):
        internal_failed = any(
            verdict is SnapshotFailureCode.SNAPSHOT_BUILD_FAILED
            for verdict in verdicts.values()
        )
        outcome = (
            SnapshotFailureCode.SNAPSHOT_BUILD_FAILED
            if internal_failed else SnapshotFailureCode.UNAVAILABLE_FOR_SEALED_PIT
        )
        raise SnapshotBuildError(
            outcome,
            f"SEALED snapshot {('implementation failed' if internal_failed else 'unavailable')}: "
            f"{sum(1 for v in verdicts.values() if v)} of {len(ordered_ids)} "
            f"requested sources failed",
            verdicts,
        ) from internal_failure

    ordered = tuple(resolved)
    try:
        _finalization_revalidation(archive, as_of, ordered)
    except SnapshotBuildError:
        raise
    except Exception as exc:  # noqa: BLE001 — unexpected finalization implementation failure
        raise SnapshotBuildError(
            SnapshotFailureCode.SNAPSHOT_BUILD_FAILED,
            f"SEALED snapshot implementation failed during finalization ({type(exc).__name__})",
        ) from exc

    as_of_str = as_of.isoformat()
    try:
        snap_hash = _compute_input_snapshot_hash(
            case_id=case_id, case_version=case_version,
            pit_mode=mode, as_of=as_of_str, ordered=ordered,
        )
        created_at = (clock or utc_now)()
        return SealedInputSnapshot(
            snapshot_id=snap_hash,
            case_id=case_id,
            case_version=case_version,
            pit_context_id=pit_context_id,
            pit_mode=mode,
            as_of=as_of_str,
            ordered_sources=ordered,
            source_count=len(ordered),
            input_snapshot_hash=snap_hash,
            closed_corpus_required=True,
            created_at=created_at.isoformat() if isinstance(created_at, dt.datetime) else str(created_at),
        )
    except Exception as exc:  # noqa: BLE001 — serializer/constructor failures are internal
        raise SnapshotBuildError(
            SnapshotFailureCode.SNAPSHOT_BUILD_FAILED,
            f"SEALED snapshot implementation failed during identity construction ({type(exc).__name__})",
        ) from exc
