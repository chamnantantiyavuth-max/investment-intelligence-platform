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