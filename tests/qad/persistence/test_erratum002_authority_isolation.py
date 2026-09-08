"""Erratum-002 — PITC AUTHORITY-ISOLATION DIAGNOSTIC (Commit E).

NOT an acceptance suite.  This is the *diagnostic evidence* committed BEFORE
the production fix, reproducing the authority-isolation defect on the REAL
frozen M5.2 five-anchor topology at baseline 089cbe6.

The frozen topology keeps the five stores SEPARATE; ``PITC-01`` belongs to the
authoritative ``PITContextStore`` anchor ONLY.  ``InMemoryEvidenceRegistry``
must never become a shadow PIT authority — but at baseline:

  1. ``_composite_contains`` / ``_composite_get_existing`` consult the
     registry's OWN local state FIRST (``self.contains`` / ``self._load_raw``)
     before the authoritative PITContextStore.
  2. ``InMemoryEvidenceRegistry.store()`` blocks ``EV-01`` / ``EAR-01`` /
     ``SRC-01`` but NOT ``PITC-01`` — so a PITC-01 can be stored locally and
     will be resolved BEFORE the authoritative anchor.

That contradicts the five-anchor authority contract and the code comments
("never a registry-local shadow copy").

These tests assert the CORRECT behaviour and are EXPECTED TO FAIL at baseline:

  A. an authoritative PITC with mode=SEALED_HISTORICAL_EVALUATION PLUS a local
     shadow PITC with the SAME id, mode=LIVE_CASE_UPDATE and created_by
     "Research Director" — a LIVE update referencing that id MUST be decided
     against the AUTHORITATIVE PITC (→ fail).  At baseline the shadow wins and
     the LIVE update incorrectly passes.
  B. ``EvidenceRegistry.store(PITC-01)`` MUST be rejected.  At baseline it
     succeeds.

The production fix (Commit F) makes them pass and adds the full
authority-isolation acceptance matrix.
"""
from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import CanonicalBoundaryViolation, TransactionFailure
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
)
from qad.models import CandidateRecord, CaseRecord, SecurityMaster
from qad.models.family_a import (
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecordCase_state,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceRecord,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_i import PITContext


# =====================================================================
# Helpers — build the REAL five-anchor topology
# =====================================================================

def _admit_src(store, source_id: str, raw: bytes) -> SourceRecord:
    ch = hashlib.sha256(raw).hexdigest()
    src = SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/auth-iso/{source_id}",
        content_hash=ch,
        retrieval_date="2024-06-01",
    )
    store.admit_source(src, raw)
    return src


def _make_ev(source_id: str, evidence_id: str) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        source_id=source_id,
        evidence_type="FACT",
        validation_status="RAW",
        content="authority-isolation evidence",
        admitting_role="Evidence Intelligence Lead",
        as_of="2024-06-01",
        extractor="v1",
        source_tier="T1",
    )


def _make_live_ear(evidence_id: str, admission_id: str, pitc_id: str) -> EvidenceAdmissionRecord:
    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        evidence_id=evidence_id,
        admitting_role="Evidence Intelligence Lead",
        admission_timestamp="2024-06-01T12:00:00",
        admission_method="DIRECT_SOURCE",
        validation_method="SOURCE_CROSS_REFERENCE",
        source_tier_check="T1",
        is_update=True,
        update_provenance="authority-isolation LIVE provenance",
        update_pit_context_id=pitc_id,
    )


def _make_pitc(
    pitc_id: str,
    created_by: str,
    case_id: str = "CASE-ISO-001",
    mode: str = "LIVE_CASE_UPDATE",
) -> PITContext:
    return PITContext(
        pit_context_id=pitc_id,
        as_of_date="2024-06-01",
        mode=mode,
        case_id=case_id,
        created_by=created_by,
    )


def _seed_pitc_store(store, case_id: str) -> None:
    sm = SecurityMaster(
        entity_id="E-ISO-001",
        cik="0000123456",
        exchange="NYSE",
        name="Auth Iso Corp",
        primary_ticker="AUTH",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id="CAND-ISO-001",
        entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2024-06-01T00:00:00",
        evidence_freshness="2024-06-01",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
        signal_ids=[],
    )
    store.store(cand)
    case = CaseRecord(
        case_id=case_id,
        entity_id=sm.entity_id,
        candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN,
        as_of_date="2024-06-01",
        opened_at="2024-06-01T08:00:00",
        research_director="Research Director",
    )
    store.store(case)


def _topology():
    """Wire RawSourceArchive + PITContextStore to a fresh EvidenceRegistry."""
    src_archive = InMemoryRawSourceArchive()
    pitc_store = InMemoryPITContextStore()
    ev_registry = InMemoryEvidenceRegistry(
        source_archive=src_archive, pit_context_store=pitc_store
    )
    return src_archive, pitc_store, ev_registry


# =====================================================================
# Commit E diagnostic tests (EXPECTED TO FAIL at baseline 089cbe6)
# =====================================================================

class TestPitcAuthorityIsolationDiagnostic:
    """Erratum-002 — authority isolation defect proof.

    Expected to fail against baseline 089cbe6 (commit-d detection): the local
    shadow PITC is resolved before the authoritative PITContextStore, so the
    LIVE update incorrectly passes; and registry-local PITC-01 storage is not
    blocked.
    """

    def test_local_shadow_cannot_override_authoritative_pitc(self):
        """Scenario A — authoritative PITC mode=SEALED + local shadow PITC
        with the SAME id, mode=LIVE_CASE_UPDATE, created_by='Research Director'.

        A LIVE update referencing that PITC id MUST be decided against the
        AUTHORITATIVE PITContextStore → FAIL (wrong mode).

        At baseline 089cbe6 the composite resolver consults the registry-local
        shadow FIRST (``self.contains`` / ``self._load_raw``) → the LIVE update
        INCORRECTLY PASSES → this test FAILS (DID NOT RAISE).  This is the
        authority inversion.

        The shadow is inserted directly into the registry's local ``_data`` —
        this is deliberate tamper-simulation of a registry-local PITC record
        existing for any reason (legacy state, other path, tamper).  The
        five-anchor authority contract must resist this: NO registry-local PIT
        shadow may EVER satisfy the FK or the LIVE authorization lookup.
        """
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ISO-001", b"authority-isolation source bytes")
        _seed_pitc_store(pitc_store, "CASE-ISO-001")

        # Authoritative PITContextStore: SEALED_HISTORICAL_EVALUATION
        pitc_store.store(
            _make_pitc("PITC-ISO-001", "Evidence Intelligence Lead",
                       mode="SEALED_HISTORICAL_EVALUATION")
        )

        # Registry-LOCAL shadow PITC (same id) — LIVE + Research Director.
        # Direct _data insertion (tamper simulation): the point is that even
        # when a local PITC record exists, it MUST NOT be consulted.
        from qad.persistence.reference import _Record
        ev_registry._data.setdefault("PITC-01", {})["PITC-ISO-001"] = _Record(
            instance=_make_pitc("PITC-ISO-001", "Research Director",
                                mode="LIVE_CASE_UPDATE"),
            canonical_hash="0" * 64,
        )

        ev = _make_ev("SRC-ISO-001", "EV-ISO-001")
        ear = _make_live_ear("EV-ISO-001", "EAR-ISO-001", "PITC-ISO-001")

        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        # Decided against the AUTHORITATIVE PITC → wrong-mode error
        assert any("LIVE_CASE_UPDATE" in str(e) for e in exc.value.errors)

    def test_evidence_registry_direct_pitc_store_blocked(self):
        """Direct ``EvidenceRegistry.store(PITC-01)`` MUST be rejected
        (CanonicalBoundaryViolation) — PITC belongs to the authoritative
        PITContextStore anchor only.

        At baseline 089cbe6 the registry does NOT block PITC-01 → the store
        SUCCEEDS → this test FAILS (DID NOT RAISE).
        """
        src_archive, _pitc_store, ev_registry = _topology()
        with pytest.raises(CanonicalBoundaryViolation):
            ev_registry.store(
                _make_pitc("PITC-ISO-X", "Research Director")
            )
        # No shadow may be left behind by an attempted bypass
        assert not ev_registry.contains("PITC-01", "PITC-ISO-X")


# =====================================================================
# Commit F — authority-isolation ACCEPTANCE matrix (Erratum-002 / FD #137)
# =====================================================================

class _PublicOnlyPITCStore:
    """REFERENCE / TEST — a PITContextStore that exposes ONLY the public
    Protocol surface (``CanonicalRecordStore`` + PITC extension), and by
    construction has NO ``_load_raw`` private method.

    If the EvidenceRegistry resolver ever reaches for a private reference
    implementation method, this wrapper raises AttributeError — proving the
    resolver stays on the public contract.
    """

    def __init__(self, delegate):
        self._delegate = delegate

    def store(self, instance, /):
        return self._delegate.store(instance)

    def load(self, schema_id, record_id, /):
        return self._delegate.load(schema_id, record_id)

    def load_historical(self, schema_id, record_id, /):
        return self._delegate.load_historical(schema_id, record_id)

    def contains(self, schema_id, record_id, /):
        return self._delegate.contains(schema_id, record_id)

    def list_ids(self, schema_id, /):
        return self._delegate.list_ids(schema_id)

    def list_all(self, schema_id, /):
        return self._delegate.list_all(schema_id)

    def get_canonical_hash(self, schema_id, record_id, /):
        return self._delegate.get_canonical_hash(schema_id, record_id)

    def store_batch(self, instances, /):
        return self._delegate.store_batch(instances)

    def delete(self, schema_id, record_id, /):
        return self._delegate.delete(schema_id, record_id)

    def delete_batch(self, pairs, /):
        return self._delegate.delete_batch(pairs)

    def tombstone(self, schema_id, record_id, reason="", authorizer=""):
        return self._delegate.tombstone(schema_id, record_id, reason, authorizer)

    def is_tombstoned(self, schema_id, record_id, /):
        return self._delegate.is_tombstoned(schema_id, record_id)

    def list_tombstoned_ids(self):
        return self._delegate.list_tombstoned_ids("PITC-01")


def _plant_local_shadow(ev_registry, pitc, record_id=None):
    """Insert a PITC record DIRECTLY into the registry's local ``_data``.

    Deliberate tamper-simulation: proves the authority contract holds even
    when a registry-local PIT record exists for any reason (legacy state,
    other path, tamper).  Does NOT use the (now blocked) store() path.
    """
    from qad.persistence.reference import _Record
    rid = record_id or pitc.pit_context_id
    ev_registry._data.setdefault("PITC-01", {})[rid] = _Record(
        instance=pitc, canonical_hash="0" * 64,
    )


class TestPitcAuthorityIsolationAcceptance:
    """Authority-isolation acceptance matrix — the eight proofs required by
    the Erratum-002 independent audit (Commit F)."""

    def test_authoritative_valid_no_shadow_passes(self):
        """#1 — authoritative PITC valid (LIVE + Research Director), no shadow
        → PASS on the canonical five-anchor admission path."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-001", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-001")
        pitc_store.store(_make_pitc("PITC-ACC-001", "Research Director", case_id="CASE-ACC-001"))

        ev = _make_ev("SRC-ACC-001", "EV-ACC-001")
        ear = _make_live_ear("EV-ACC-001", "EAR-ACC-001", "PITC-ACC-001")
        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64
        assert ev_registry.contains("EAR-01", "EAR-ACC-001")

    def test_authoritative_wrong_mode_beats_local_shadow(self):
        """#2 — authoritative PITC wrong mode (SEALED) + local fake LIVE PITC
        with the SAME id → FAIL based on the AUTHORITATIVE PITC."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-002", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-002")
        pitc_store.store(_make_pitc("PITC-ACC-002", "Evidence Intelligence Lead",
                                    case_id="CASE-ACC-002",
                                    mode="SEALED_HISTORICAL_EVALUATION"))
        _plant_local_shadow(ev_registry,
                            _make_pitc("PITC-ACC-002", "Research Director",
                                       case_id="CASE-ACC-002",
                                       mode="LIVE_CASE_UPDATE"))

        ev = _make_ev("SRC-ACC-002", "EV-ACC-002")
        ear = _make_live_ear("EV-ACC-002", "EAR-ACC-002", "PITC-ACC-002")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any("LIVE_CASE_UPDATE" in str(e) for e in exc.value.errors)
        assert not ev_registry.contains("EV-01", "EV-ACC-002")  # zero partial

    def test_authoritative_unauthorized_beats_local_shadow(self):
        """#3 — authoritative PITC unauthorized created_by + local fake
        Research Director PITC with the SAME id → FAIL based on the
        AUTHORITATIVE PITC."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-003", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-003")
        pitc_store.store(_make_pitc("PITC-ACC-003", "Evidence Intelligence Lead",
                                   case_id="CASE-ACC-003"))
        _plant_local_shadow(ev_registry,
                            _make_pitc("PITC-ACC-003", "Research Director",
                              case_id="CASE-ACC-003"))

        ev = _make_ev("SRC-ACC-003", "EV-ACC-003")
        ear = _make_live_ear("EV-ACC-003", "EAR-ACC-003", "PITC-ACC-003")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any("Research Director" in str(e) for e in exc.value.errors)
        assert not ev_registry.contains("EAR-01", "EAR-ACC-003")

    def test_authoritative_absent_fails_closed_even_with_local_shadow(self):
        """#4 — authoritative PITC ABSENT + local PITC exists → FAIL CLOSED
        (the local shadow must never satisfy the FK)."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-004", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-004")
        _plant_local_shadow(ev_registry,
                            _make_pitc("PITC-ACC-004", "Research Director",
                           case_id="CASE-ACC-004"))

        ev = _make_ev("SRC-ACC-004", "EV-ACC-004")
        ear = _make_live_ear("EV-ACC-004", "EAR-ACC-004", "PITC-ACC-004")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        joined = "\n".join(str(e) for e in exc.value.errors)
        assert "PITC-01" in joined or "update_pit_context_id" in joined
        assert not ev_registry.contains("EV-01", "EV-ACC-004")

    def test_direct_store_blocked(self):
        """#5 — EvidenceRegistry.store(PITC-01) → CanonicalBoundaryViolation."""
        src_archive, _pitc_store, ev_registry = _topology()
        with pytest.raises(CanonicalBoundaryViolation):
            ev_registry.store(_make_pitc("PITC-ACC-005", "Research Director",
                        case_id="CASE-ACC-005"))

    def test_store_batch_blocked(self):
        """#6 — EvidenceRegistry.store_batch([... PITC-01 ...]) → rejected."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-006", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-006")
        pitc = _make_pitc("PITC-ACC-006", "Research Director")
        with pytest.raises(CanonicalBoundaryViolation):
            ev_registry.store_batch([pitc])

    def test_resolver_uses_public_pitc_store_api(self):
        """#7 — the resolver works against a PITContextStore that exposes
        ONLY the public Protocol surface (no ``_load_raw`` private method)."""
        src_archive, pitc_store, _ = _topology()
        _admit_src(src_archive, "SRC-ACC-007", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-007")
        pitc_store.store(_make_pitc("PITC-ACC-007", "Research Director",
                                   case_id="CASE-ACC-007"))

        public_only = _PublicOnlyPITCStore(pitc_store)
        ev_registry = InMemoryEvidenceRegistry(
            source_archive=src_archive, pit_context_store=public_only
        )
        ev = _make_ev("SRC-ACC-007", "EV-ACC-007")
        ear = _make_live_ear("EV-ACC-007", "EAR-ACC-007", "PITC-ACC-007")
        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64  # public-API-only path works

    def test_no_shadow_needed_on_valid_path(self):
        """#8 — a valid canonical admission path works with ZERO registry-local
        PITC; no shadow is created as a side effect."""
        src_archive, pitc_store, ev_registry = _topology()
        _admit_src(src_archive, "SRC-ACC-008", b"acceptance source bytes")
        _seed_pitc_store(pitc_store, "CASE-ACC-008")
        pitc_store.store(_make_pitc("PITC-ACC-008", "Research Director",
                                   case_id="CASE-ACC-008"))

        ev = _make_ev("SRC-ACC-008", "EV-ACC-008")
        ear = _make_live_ear("EV-ACC-008", "EAR-ACC-008", "PITC-ACC-008")
        ev_registry.admit_evidence(ev, ear)

        assert not ev_registry.contains("PITC-01", "PITC-ACC-008")
        assert "PITC-01" not in ev_registry._data  # no shadow ever created