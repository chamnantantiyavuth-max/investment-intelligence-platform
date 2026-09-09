"""M5.3 S7 — PIT Runtime Enforcement (CORRECTION ROUND — FD #138).

Corrected implementation per the Founder decisions recorded in FD #138:

- **Public surface is ID-based:** ``adjudicate(evidence_id, pitc_id)`` resolves
  the authoritative PITC-01 / EV-01 / EAR-01 from the canonical stores itself.
  Caller-supplied authority OBJECTS are never accepted (no forged PITContext /
  EAR can authorize).  The object-level adjudicator is PRIVATE
  (``_adjudicate_object``) and is only reached through store-resolved records.
- **Source-time PIT (FD #138 §11):** ``effective_pit_time = MAX(EV-01.as_of,
  authoritative_source_available_at)`` where the source-availability time is:
    SEALED_HISTORICAL_EVALUATION -> SRC-01.publication_date REQUIRED;
        missing publication_date -> PIT BLOCK (source not SEALED-eligible,
        retrieval_date is NEVER substituted).
    LIVE_CASE_UPDATE / REPLAY_EXCEPTION -> publication_date if present, else
        SRC-01.retrieval_date (conservative machine-readable availability
        evidence).
  Source metadata unresolvable or timestamp uninterpretable -> **FAIL CLOSED**
  (deterministic PITBlockError; never a silent allow/empty).
- **Store failure fails closed (FD #138 §10):** EvidenceRegistry / PITC /
  source-archive read failures raise typed deterministic errors — an
  infrastructure failure is NEVER a legitimate empty evidence set, and
  'record not found' is differentiated from 'authority unavailable'.
- **EV canonical-hash tamper check = defense-in-depth** (FD #138 §12):
  relabeled 'canonical evidence-record integrity / tamper detection' with
  reason ``record_integrity`` — NOT the M4B TEST-7 sealed-corpus proof.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
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

_KNOWN_MODES = {
    "LIVE_CASE_UPDATE",
    "SEALED_HISTORICAL_EVALUATION",
    "REPLAY_EXCEPTION",
}


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
    excluded; ``blocked_count`` = seal/record-integrity-invalidated records.
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
        Authoritative RawSourceArchive (SRC-01) — used for source-time PIT
        (publication_date / retrieval_date).  Previously injected-but-unused;
        now a first-class temporal input (FD #138 §11).
    rd_role_token:
        Exact canonical Research Director token (frozen SM-12).
    founder_role_token:
        Exact canonical FOUNDER token required for REPLAY_EXCEPTION.

    Raises
    ------
    PITBlockError:
        Deterministic PIT/infrastructure block: forbidden evidence, PITC
        unavailable, source metadata unresolvable/uninterpretable, or a
        canonical store read failure (fail closed — never a silent empty).
    KeyError:
        ``adjudicate``/``access`` for an evidence id that does not exist
        (differentiated from 'authority unavailable').
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

    # -- public API (ID-based — FD #138 §9) ---------------------------------

    def adjudicate(self, evidence_id: str, pitc_id: str) -> PITVerdict:
        """Deterministic PIT verdict for one evidence record in a context.

        Resolves the authoritative EV-01 / PITC-01 / EAR-01 from the canonical
        stores itself.  Callers NEVER supply PITContext / EAR objects.
        """
        pitc = self._load_pitc(pitc_id)
        evidence = self._load_evidence(evidence_id)
        ear = self._resolve_ear(evidence_id)
        return self._adjudicate_object(evidence, pitc, ear)

    def query(self, pitc_id: str) -> PITQueryResult:
        """PIT-aware collection query over EV-01 (minimum §11.3-disciplined).

        A store-read failure raises (fail closed) — never a silent empty.
        In LIVE_CASE_UPDATE mode the AUTHORITATIVE EAR-01 carrier is resolved
        for every EV so a valid post-AS_OF update appears in the collection
        exactly as it does via ``access()``/``adjudicate()`` (re-audit §1).
        """
        pitc = self._load_pitc(pitc_id)
        try:
            candidates = self._evidence_registry.list_all("EV-01")
        except Exception as exc:  # noqa: BLE001 — authority unavailable
            raise PITBlockError(
                f"Evidence store unavailable — cannot establish PIT-valid "
                f"evidence, fail closed: {exc}",
                schema_id="EV-01",
                verdict="BLOCKED",
                reason="evidence_store_unavailable",
            ) from exc

        mode = self._mode_str(pitc)
        ear_by_evidence: dict[str, EvidenceAdmissionRecord] = {}
        if mode == "LIVE_CASE_UPDATE":
            # Batch-resolve the authoritative EAR carriers (Erratum-002 chain).
            try:
                ears = self._evidence_registry.list_all("EAR-01")
            except Exception as exc:  # noqa: BLE001 — authority unavailable
                raise PITBlockError(
                    f"EAR-01 unreadable — cannot resolve the authoritative "
                    f"LIVE carriers, fail closed: {exc}",
                    schema_id="EAR-01",
                    verdict="BLOCKED",
                    reason="evidence_store_unavailable",
                ) from exc
            for ear in ears:
                ear_by_evidence.setdefault(ear.evidence_id, ear)

        allowed: list[EvidenceRecord] = []
        excluded = 0
        blocked = 0
        for rec in candidates:
            ear = ear_by_evidence.get(rec.evidence_id)
            verdict = self._adjudicate_object(rec, pitc, ear)
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
        evidence = self._load_evidence(evidence_id)
        ear = self._resolve_ear(evidence_id)
        verdict = self._adjudicate_object(evidence, pitc, ear)
        if verdict is PITVerdict.ALLOWED:
            return evidence
        reason = (
            "record_integrity"
            if verdict is PITVerdict.SEAL_INVALIDATED
            else self._block_reason(evidence, pitc)
        )
        raise PITBlockError(
            f"PIT block: EV-01/{evidence_id} forbidden under PITC {pitc_id} "
            f"({verdict.value})",
            schema_id="EV-01",
            record_id=evidence_id,
            verdict=verdict.value,
            reason=reason,
        )

    # -- private object-level adjudicator (store-resolved inputs only) ------

    def _adjudicate_object(
        self,
        evidence: EvidenceRecord,
        pitc: PITContext,
        ear: EvidenceAdmissionRecord | None,
    ) -> PITVerdict:
        """Deterministic nine-case PIT semantics with source-time enforcement.

        Private: the caller MUST have resolved ``evidence``/``pitc`` from the
        authoritative stores.  Public entry points only reach this method
        through store resolution (never with caller-supplied objects).
        """
        # Defense-in-depth: canonical EV record integrity / tamper detection
        # (FD #138 §12 — NOT the M4B TEST-7 sealed-corpus proof).
        if not self._verify_integrity(evidence):
            return PITVerdict.SEAL_INVALIDATED

        mode = self._mode_str(pitc)
        if mode not in _KNOWN_MODES:
            return PITVerdict.BLOCKED  # unknown mode -> fail closed

        # Source-time PIT (FD #138 §11).
        source_available = self._source_available_at(evidence, pitc)
        if source_available is None:
            # SEALED + missing publication_date -> PIT BLOCK (not eligible).
            return PITVerdict.BLOCKED

        effective = self._max_date(evidence.as_of, source_available)
        if effective <= self._parse_date(
            pitc.as_of_date,
            where="PITC.as_of_date",
            reason="pit_asof_uninterpretable",
        ):
            # Pre-AS_OF (by BOTH evidence time and source availability time)
            # is PIT-valid in every mode — no future information leak.
            return PITVerdict.ALLOWED

        # Post-effective — mode-specific rules.
        if mode == "SEALED_HISTORICAL_EVALUATION":
            # Hard block.  No override.
            return PITVerdict.BLOCKED

        if mode == "LIVE_CASE_UPDATE":
            # Post-AS_OF permitted ONLY through the Erratum-002 machine-readable
            # carrier, resolved against the AUTHORITATIVE stores.
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
            if (
                pitc.created_by == self._founder_role_token
                and bool(pitc.exception_reason)
            ):
                return PITVerdict.ALLOWED
            return PITVerdict.BLOCKED

        return PITVerdict.BLOCKED  # pragma: no cover — guarded above

    # -- internal helpers (public-contract only) ----------------------------

    def _load_pitc(self, pitc_id: str) -> PITContext:
        """Resolve the AUTHORITATIVE PITC record (fail closed)."""
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

    def _load_evidence(self, evidence_id: str) -> EvidenceRecord:
        """Resolve the AUTHORITATIVE EV record.

        KeyError = the record genuinely does not exist (differs from
        'authority unavailable' which raises PITBlockError/typed errors).
        """
        return self._evidence_registry.load("EV-01", evidence_id)

    def _source_available_at(
        self, evidence: EvidenceRecord, pitc: PITContext
    ) -> date | None:
        """Authoritative source availability time (FD #138 §11).

        Returns a date, or None for the SEALED-missing-publication_date
        BLOCK case.  Raises PITBlockError (FAIL CLOSED) when the source
        metadata cannot be resolved or its timestamp is uninterpretable.
        """
        mode = self._mode_str(pitc)
        if self._source_archive is None:
            raise PITBlockError(
                f"EV-01/{evidence.evidence_id}: source archive unavailable — "
                f"cannot resolve authoritative source time (fail closed)",
                schema_id="EV-01",
                record_id=evidence.evidence_id,
                verdict="BLOCKED",
                reason="source_unavailable",
            )
        try:
            src = self._source_archive.load("SRC-01", evidence.source_id)
        except KeyError as exc:
            raise PITBlockError(
                f"EV-01/{evidence.evidence_id}: SRC-01/{evidence.source_id} "
                f"not in the authoritative archive (fail closed)",
                schema_id="EV-01",
                record_id=evidence.evidence_id,
                verdict="BLOCKED",
                reason="source_unavailable",
            ) from exc
        except Exception as exc:  # noqa: BLE001 — authority unavailable
            raise PITBlockError(
                f"EV-01/{evidence.evidence_id}: source archive read failed "
                f"(fail closed): {exc}",
                schema_id="EV-01",
                record_id=evidence.evidence_id,
                verdict="BLOCKED",
                reason="source_unavailable",
            ) from exc

        pub = getattr(src, "publication_date", None)
        if mode == "SEALED_HISTORICAL_EVALUATION":
            if not pub:
                # M4B Seal Contract requires publication date for every SEALED
                # source; retrieval_date is NEVER substituted (Founder rule).
                return None
            return self._parse_date(
                pub,
                where=f"SRC-01/{evidence.source_id}.publication_date",
                reason="source_timestamp_uninterpretable",
            )
        # LIVE / REPLAY: publication_date if present, else retrieval_date.
        raw = pub if pub else getattr(src, "retrieval_date", None)
        if not raw:
            raise PITBlockError(
                f"EV-01/{evidence.evidence_id}: SRC-01/{evidence.source_id} "
                f"has neither publication_date nor retrieval_date — cannot "
                f"establish availability time (fail closed)",
                schema_id="EV-01",
                record_id=evidence.evidence_id,
                verdict="BLOCKED",
                reason="source_unavailable",
            )
        return self._parse_date(
            raw,
            where=f"SRC-01/{evidence.source_id}",
            reason="source_timestamp_uninterpretable",
        )

    def _verify_integrity(self, rec: EvidenceRecord) -> bool:
        """Defense-in-depth: canonical EV record integrity / tamper detection.

        A record whose stored canonical hash disagrees with the canonical
        serialisation of its current content is SEAL_INVALIDATED — whatever
        forced it (tamper, corruption) it must not satisfy PIT.  This is NOT
        the M4B TEST-7 sealed-CORPUS proof (which lives at the fixture-sealing
        pre-production gate — FD #138 §12).
        """
        try:
            stored = self._evidence_registry.get_canonical_hash(
                "EV-01", rec.evidence_id
            )
        except KeyError as exc:
            raise PITBlockError(
                f"EV-01/{rec.evidence_id}: stored canonical hash unavailable — "
                f"cannot verify record integrity, fail closed",
                schema_id="EV-01",
                record_id=rec.evidence_id,
                verdict="BLOCKED",
                reason="record_unverifiable",
            ) from exc
        try:
            return stored == compute_canonical_hash(rec)
        except Exception as exc:  # noqa: BLE001 — cannot verify
            raise PITBlockError(
                f"EV-01/{rec.evidence_id}: canonical hash computation failed "
                f"— cannot verify record integrity, fail closed: {exc}",
                schema_id="EV-01",
                record_id=rec.evidence_id,
                verdict="BLOCKED",
                reason="record_unverifiable",
            ) from exc

    def _resolve_ear(
        self, evidence_id: str,
    ) -> EvidenceAdmissionRecord | None:
        """Resolve the admission record for an evidence id (authoritative scan).

        Fail closed: an EvidenceRegistry read failure raises — it is never
        converted into 'no carrier'.  Absence (None) is legitimate when the
        registry was readable; adjudication then fails closed per mode.
        """
        if self._evidence_registry is None:
            raise PITBlockError(
                f"EV-01/{evidence_id}: EvidenceRegistry unavailable (fail closed)",
                schema_id="EAR-01",
                verdict="BLOCKED",
                reason="evidence_store_unavailable",
            )
        try:
            ears = self._evidence_registry.list_all("EAR-01")
        except Exception as exc:  # noqa: BLE001 — authority unavailable
            raise PITBlockError(
                f"EAR-01 unreadable — cannot resolve the authoritative "
                f"admission carrier, fail closed: {exc}",
                schema_id="EAR-01",
                verdict="BLOCKED",
                reason="evidence_store_unavailable",
            ) from exc
        for ear in ears:
            if ear.evidence_id == evidence_id:
                return ear
        return None

    @staticmethod
    def _max_date(a: str, b: date) -> date:
        """MAX(EV.as_of, source availability) with deterministic parsing.

        Raises PITBlockError when either timestamp is uninterpretable
        (FAIL CLOSED — FD #138 §11).
        """
        return max(
            PITEnforcementService._parse_date(
                a, where="EV-01.as_of", reason="evidence_timestamp_uninterpretable"
            ),
            b,
        )

    @staticmethod
    def _parse_date(value: str, *, where: str, reason: str) -> date:
        """Parse an ISO-ish date string deterministically or fail closed."""
        if value is None:
            raise PITBlockError(
                f"{where}: missing timestamp — cannot evaluate PIT (fail closed)",
                verdict="BLOCKED",
                reason=reason,
            )
        text = str(value).strip()
        if "T" in text:
            text = text.split("T", 1)[0]
        try:
            return date.fromisoformat(text)
        except ValueError as exc:
            raise PITBlockError(
                f"{where}: uninterpretable timestamp {value!r} — "
                f"cannot evaluate PIT (fail closed)",
                verdict="BLOCKED",
                reason=reason,
            ) from exc

    @staticmethod
    def _mode_str(pitc: PITContext) -> str:
        mode = pitc.mode
        return mode.value if hasattr(mode, "value") else str(mode)

    def _block_reason(self, rec: EvidenceRecord, pitc: PITContext) -> str:
        mode = self._mode_str(pitc)
        if mode == "SEALED_HISTORICAL_EVALUATION":
            return f"post_as_of_in_sealed_context (as_of={rec.as_of})"
        if mode == "LIVE_CASE_UPDATE":
            return "live_update_without_valid_erratum002_carrier"
        if mode == "REPLAY_EXCEPTION":
            return "replay_without_exact_founder_authority_or_reason"
        return f"unknown_pit_mode:{mode}"