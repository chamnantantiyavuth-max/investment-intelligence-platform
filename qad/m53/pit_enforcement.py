"""M5.3 S7 — PIT Runtime Enforcement (reference implementation).

Deterministic, fail-closed point-in-time enforcement over canonical
evidence, using the frozen M4B nine-case PIT semantics (QAD-M4B
``pit-leakage-proof.py``, accepted) mapped to the canonical five-anchor
topology.

Authorities (frozen):
- M4A PITC-01 ``mode``: LIVE_CASE_UPDATE / SEALED_HISTORICAL_EVALUATION /
  REPLAY_EXCEPTION.
- M5.2 §11.1: query-time filtering (exclude ``as_of > query_time``),
  SEALED hard block, evaluation-harness replay exceptions.
- Erratum-002 / FD #137: LIVE carrier = ``EAR-01.is_update`` +
  ``update_provenance`` + ``update_pit_context_id`` -> authoritative PITC-01;
  PITC authorizing an update must have ``created_by`` == exact canonical
  Research Director token (SM-12). No free-text inference.
- QAD-M4B pit-leakage-proof: REPLAY requires exact FOUNDER actor; a
  canonical-hash tamper invalidates the seal.

REFERENCES / NON-PRODUCTION: dict-backed in-memory stores; all cross-store
resolution uses PUBLIC protocols (``load``/``contains``/``list_all``/
``get_canonical_hash``) — never private in-memory internals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from qad.models.family_b import EvidenceAdmissionRecord, EvidenceRecord
from qad.models.family_i import PITContext
from qad.persistence import (
    EvidenceRegistry,
    PITBlockError,
    PITContextStore,
    RawSourceArchive,
    compute_canonical_hash,
)


class PITVerdict(Enum):
    """Deterministic PIT adjudication outcome (mirrors M4B proof)."""

    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    SEAL_INVALIDATED = "SEAL_INVALIDATED"


@dataclass(frozen=True)
class PITQueryResult:
    """PIT-filtered collection query result.

    ``records`` contains ONLY PIT-valid evidence — forbidden evidence never
    leaks into the returned context.  ``excluded_count`` = post-AS_OF
    excluded; ``blocked_count`` = seal-integrity-invalidated records.
    """

    records: list[EvidenceRecord] = field(default_factory=list)
    excluded_count: int = 0
    blocked_count: int = 0


class PITEnforcementService:
    """PIT lock service built on the canonical five-anchor topology.

    Parameters
    ----------
    pitc_store:
        Authoritative PITContextStore (PITC-01).  FAIL CLOSED when the
        store or the referenced context is unavailable.
    evidence_registry:
        Authoritative EvidenceRegistry (EV-01 / EAR-01).
    source_archive:
        Authoritative RawSourceArchive (SRC-01) — held for topology
        completeness; the LIVE carrier chain is resolved through the
        registry + PITContextStore (Erratum-002 authority pattern).
    rd_role_token:
        Exact canonical Research Director token (frozen SM-12).  Substring
        matches are NEVER accepted.
    founder_role_token:
        Exact canonical FOUNDER token required for REPLAY_EXCEPTION
        (frozen M4B proof).  Substring matches are NEVER accepted.

    Raises
    ------
    PITBlockError:
        ``access()`` for forbidden evidence (deterministic; never a silent
        empty result).  ``query()``/``access()`` when the PIT context is
        unavailable (fail closed).
    """

    def __init__(
        self,
        *,
        pitc_store: PITContextStore,
        evidence_registry: EvidenceRegistry,
        source_archive: RawSourceArchive,
        rd_role_token: str = "Research Director",
        founder_role_token: str = "FOUNDER",
    ) -> None:
        self._pitc_store = pitc_store
        self._evidence_registry = evidence_registry
        self._source_archive = source_archive
        self._rd_role_token = rd_role_token
        self._founder_role_token = founder_role_token

    # -- public API ---------------------------------------------------------

    def adjudicate(
        self,
        evidence: EvidenceRecord,
        pitc: PITContext,
        ear: EvidenceAdmissionRecord | None = None,
    ) -> PITVerdict:
        """Deterministic PIT verdict for one evidence record in a context.

        If ``ear`` is omitted for a LIVE context it is resolved from the
        authoritative EvidenceRegistry (EAR-01 scan by ``evidence_id``).
        """
        if not self._verify_integrity(evidence):
            return PITVerdict.SEAL_INVALIDATED

        # Pre-AS_OF evidence is PIT-valid in every mode.
        if evidence.as_of <= pitc.as_of_date:
            return PITVerdict.ALLOWED

        # Post-AS_OF evidence — mode-specific.
        mode = self._mode_str(pitc)

        if mode == "SEALED_HISTORICAL_EVALUATION":
            # Hard block.  No override.
            return PITVerdict.BLOCKED

        if mode == "LIVE_CASE_UPDATE":
            # Post-AS_OF permitted ONLY through the Erratum-002 machine-readable
            # carrier, resolved against the AUTHORITATIVE PITContextStore.
            if ear is None:
                ear = self._resolve_ear(evidence.evidence_id)
            if (
                ear is not None
                and ear.is_update is True
                and bool(ear.update_provenance)
                and ear.update_pit_context_id == pitc.pit_context_id
                and pitc.created_by == self._rd_role_token
            ):
                return PITVerdict.ALLOWED
            return PITVerdict.BLOCKED

        if mode == "REPLAY_EXCEPTION":
            # Requires exact FOUNDER actor + explicit exception reason.
            if (
                pitc.created_by == self._founder_role_token
                and bool(pitc.exception_reason)
            ):
                return PITVerdict.ALLOWED
            return PITVerdict.BLOCKED

        # Unknown mode — fail closed.
        return PITVerdict.BLOCKED

    def query(self, pitc_id: str) -> PITQueryResult:
        """PIT-aware collection query over EV-01 (minimum §11.3-disciplined).

        Returns only PIT-valid evidence; forbidden evidence is counted in
        ``excluded_count`` (post-AS_OF) / ``blocked_count`` (seal-invalid).
        """
        pitc = self._load_pitc(pitc_id)
        allowed: list[EvidenceRecord] = []
        excluded = 0
        blocked = 0
        try:
            candidates = self._evidence_registry.list_all("EV-01")
        except Exception:
            candidates = []
        for rec in candidates:
            verdict = self.adjudicate(rec, pitc)
            if verdict is PITVerdict.ALLOWED:
                allowed.append(rec)
            elif verdict is PITVerdict.BLOCKED:
                excluded += 1
            else:  # SEAL_INVALIDATED
                blocked += 1
        return PITQueryResult(
            records=allowed, excluded_count=excluded, blocked_count=blocked,
        )

    def access(self, evidence_id: str, pitc_id: str) -> EvidenceRecord:
        """Explicit access to a single evidence record under a PIT context.

        Forbidden evidence raises ``PITBlockError`` — the consumer NEVER
        receives a silent empty result pretending the record does not exist.
        """
        pitc = self._load_pitc(pitc_id)
        try:
            rec = self._evidence_registry.load("EV-01", evidence_id)
        except KeyError:
            raise KeyError(f"EV-01/{evidence_id}: not found") from None
        verdict = self.adjudicate(rec, pitc)
        if verdict is PITVerdict.ALLOWED:
            return rec
        raise PITBlockError(
            f"PIT block: EV-01/{evidence_id} forbidden under PITC {pitc_id} "
            f"({verdict.value})",
            schema_id="EV-01",
            record_id=evidence_id,
            verdict=verdict.value,
            reason=self._block_reason(rec, pitc),
        )

    # -- internal helpers (public-contract only) ----------------------------

    def _load_pitc(self, pitc_id: str) -> PITContext:
        if self._pitc_store is None or not self._pitc_store.contains(
            "PITC-01", pitc_id
        ):
            raise PITBlockError(
                f"PIT context unavailable: PITC-01/{pitc_id} (fail closed)",
                schema_id="PITC-01",
                record_id=pitc_id,
                verdict="BLOCKED",
                reason="pit_context_unavailable",
            )
        return self._pitc_store.load("PITC-01", pitc_id)

    def _verify_integrity(self, rec: EvidenceRecord) -> bool:
        """Canonical-hash tamper check (M4B proof TEST 7 semantics).

        A sealed record whose stored canonical hash disagrees with the
        canonical serialisation of its current content is SEAL_INVALIDATED —
        whatever forced it (tamper, corruption) it must not satisfy PIT.
        """
        try:
            stored = self._evidence_registry.get_canonical_hash(
                "EV-01", rec.evidence_id
            )
        except KeyError:
            return False
        try:
            return stored == compute_canonical_hash(rec)
        except Exception:
            return False

    def _resolve_ear(
        self, evidence_id: str,
    ) -> EvidenceAdmissionRecord | None:
        """Resolve the admission record for an evidence id (authoritative scan).

        EAR-01.evidence_id == EV.evidence_id.  Returns None when absent —
        the adjudication then FAILS CLOSED (no carrier -> BLOCKED).
        """
        if self._evidence_registry is None:
            return None
        try:
            ears = self._evidence_registry.list_all("EAR-01")
        except Exception:
            return None
        for ear in ears:
            if ear.evidence_id == evidence_id:
                return ear
        return None

    def _block_reason(self, rec: EvidenceRecord, pitc: PITContext) -> str:
        mode = self._mode_str(pitc)
        if mode == "SEALED_HISTORICAL_EVALUATION":
            return f"post_as_of_in_sealed_context (as_of={rec.as_of})"
        if mode == "LIVE_CASE_UPDATE":
            return "live_update_without_valid_erratum002_carrier"
        if mode == "REPLAY_EXCEPTION":
            return "replay_without_exact_founder_authority_or_reason"
        return f"unknown_pit_mode:{mode}"

    @staticmethod
    def _mode_str(pitc: PITContext) -> str:
        mode = pitc.mode
        return mode.value if hasattr(mode, "value") else str(mode)