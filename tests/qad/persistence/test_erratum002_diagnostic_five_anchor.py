"""Erratum-002 Defect B — FIVE-ANCHOR LIVE-UPDATE PROOF (Commit C + D).

Started as Commit C *diagnostic evidence*: tests asserting the CORRECT
behaviour on the ACTUAL frozen M5.2 topology, committed BEFORE the production
fix.  They FAILED at baseline 6d76348 — that failing result (Commit C, 05c32a8)
proved two material defects:

  1. Five-anchor FK / lookup cannot resolve.  ``InMemoryEvidenceRegistry``
     resolved FKs only against its own dict + RawSourceArchive, so a LIVE
     update's ``EAR-01.update_pit_context_id`` could not reach a PITC-01 that
     lives in the separate authoritative PITContextStore:
       MissingForeignKey: EAR-01.update_pit_context_id: FK reference
       'PITC-FA-LIVE' not found in PITC-01.pit_context_id
  2. Substring authorization unsafe.  ``"Research Director" in str(created_by)``
     accepted ``"Fake Research Director"`` (test DID NOT RAISE).

Commit D (this file together with the production fix) wires the EvidenceRegistry
admission transaction to the authoritative PITContextStore and requires the
exact canonical role token ``"Research Director"``.  These tests now PASS and
are the five-anchor LIVE-update acceptance proof:

  RawSourceArchive.admit_source  (SRC-01)
  -> PITContextStore.store       (PITC-01, separate authoritative anchor)
  -> EvidenceRegistry.admit_evidence(EV, EAR)   (canonical path, EAR-01)

Real M5.2 five-anchor topology (never the monolithic seeded_store):

    RawSourceArchive      — SRC-01 (content-addressed, admit_source gate)
    EvidenceRegistry      — EV-01 + EAR-01 (admit_evidence gate)
    FinancialFactStore    — FF/NFF/CALC/SCEN (lineage)
    RunManifestStore      — RRM-01 (lifecycle)
    PITContextStore       — PITC-01 (point-in-time context)

No ``store(EAR-01)`` bypass is used as the closure proof — every scenario runs
through the canonical ``admit_evidence()`` path.
"""
from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import TransactionFailure, ValidationFailure
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
)
from qad.models import (
    CandidateRecord,
    CaseRecord,
    SecurityMaster,
)
from qad.models.family_a import (
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecordCase_state,
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
    """A — admit a valid SRC-01 through RawSourceArchive.admit_source()."""
    ch = hashlib.sha256(raw).hexdigest()
    src = SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/five-anchor/{source_id}",
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
        content="five-anchor live evidence",
        admitting_role="Evidence Intelligence Lead",
        as_of="2024-06-01",
        extractor="v1",
        source_tier="T1",
    )


def _make_live_ear(
    evidence_id: str,
    admission_id: str,
    pitc_id: str | None,
    *,
    is_update: bool = True,
    provenance: str = "five-anchor LIVE update provenance",
) -> EvidenceAdmissionRecord:
    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        evidence_id=evidence_id,
        admitting_role="Evidence Intelligence Lead",
        admission_timestamp="2024-06-01T12:00:00",
        admission_method="DIRECT_SOURCE",
        validation_method="SOURCE_CROSS_REFERENCE",
        source_tier_check="T1",
        is_update=is_update,
        update_provenance=provenance,
        update_pit_context_id=pitc_id,
    )


def _make_pitc(
    pitc_id: str,
    created_by: str,
    case_id: str = "CASE-FA-LIVE",
    mode: str = "LIVE_CASE_UPDATE",
) -> PITContext:
    """B — a valid PITC-01 for the separate PITContextStore."""
    return PITContext(
        pit_context_id=pitc_id,
        as_of_date="2024-06-01",
        mode=mode,
        case_id=case_id,
        created_by=created_by,
    )


def _seed_pitc_store(store, case_id: str) -> None:
    """Seed the minimal FK chain PITC-01 depends on (CASE-01 → SM-01, CR-01)."""
    sm = SecurityMaster(
        entity_id="E-FA-LIVE",
        cik="0000123456",
        exchange="NYSE",
        name="Five Anchor Corp",
        primary_ticker="FIVE",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id="CAND-FA-LIVE",
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


def _five_anchor_topology(
    created_by: str = "Research Director",
    *,
    mode: str = "LIVE_CASE_UPDATE",
    source_id: str = "SRC-FA-LIVE",
    pitc_id: str = "PITC-FA-LIVE",
    case_id: str = "CASE-FA-LIVE",
):
    """Build the REAL five-anchor topology and return wired anchors.

    Returns (src_archive, pitc_store, ev_registry, pitc_id, source_id).
    The PITC lives ONLY in the authoritative PITContextStore — never in the
    EvidenceRegistry (no shadow copy on the canonical path).
    """
    src_archive = InMemoryRawSourceArchive()
    _admit_src(src_archive, source_id, b"five-anchor live source bytes")

    pitc_store = InMemoryPITContextStore()
    _seed_pitc_store(pitc_store, case_id)
    pitc_store.store(_make_pitc(pitc_id, created_by, case_id=case_id, mode=mode))

    ev_registry = InMemoryEvidenceRegistry(
        source_archive=src_archive, pit_context_store=pitc_store
    )
    return src_archive, pitc_store, ev_registry, pitc_id, source_id


# =====================================================================
# Five-anchor LIVE-update acceptance proof (Erratum-002 / FD #137)
# =====================================================================

class TestFiveAnchorLiveUpdate:
    """LIVE update through the canonical five-anchor admission path."""

    def test_valid_live_context_passes(self):
        """Valid LIVE context (exact Research Director token) → PASS."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology()
        ev = _make_ev(source_id, "EV-FA-LIVE")
        ear = _make_live_ear("EV-FA-LIVE", "EAR-FA-LIVE", pitc_id)

        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64
        loaded = ev_registry.load("EAR-01", "EAR-FA-LIVE")
        assert loaded.is_update is True
        assert loaded.update_pit_context_id == pitc_id

    def test_cross_anchor_fk_actually_resolves_through_pitc_store(self):
        """The PITC FK is resolved from the AUTHORITATIVE PITContextStore.

        The registry holds NO shadow copy of the PITC; admission succeeds only
        because the composite resolver reaches the separate authoritative store.
        """
        _, pitc_store, ev_registry, pitc_id, source_id = _five_anchor_topology()
        # Prove the PITC exists ONLY in the separate authoritative store
        assert pitc_store.contains("PITC-01", pitc_id) is True
        assert ev_registry.contains("PITC-01", pitc_id) is False  # no shadow

        ev = _make_ev(source_id, "EV-FK-RESOLVE")
        ear = _make_live_ear("EV-FK-RESOLVE", "EAR-FK-RESOLVE", pitc_id)
        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64
        assert ev_registry.contains("EAR-01", "EAR-FK-RESOLVE")

    def test_missing_pit_context_fails(self):
        """LIVE update referencing a NON-EXISTENT PITC → FAIL (FK not found)."""
        _, _, ev_registry, _pitc_id, source_id = _five_anchor_topology()
        ev = _make_ev(source_id, "EV-FA-NO-PITC")
        ear = _make_live_ear("EV-FA-NO-PITC", "EAR-FA-NO-PITC",
                             "PITC-DOES-NOT-EXIST")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        joined = "\n".join(str(e) for e in exc.value.errors)
        assert "update_pit_context_id" in joined or "PITC-01" in joined
        # zero partial state
        assert not ev_registry.contains("EV-01", "EV-FA-NO-PITC")
        assert not ev_registry.contains("EAR-01", "EAR-FA-NO-PITC")

    def test_wrong_mode_fails(self):
        """A SEALED PITC must not authorize a LIVE update → FAIL."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology(
            mode="SEALED_HISTORICAL_EVALUATION"
        )
        ev = _make_ev(source_id, "EV-FA-MODE")
        ear = _make_live_ear("EV-FA-MODE", "EAR-FA-MODE", pitc_id)
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any("LIVE_CASE_UPDATE" in str(e) for e in exc.value.errors)
        assert not ev_registry.contains("EAR-01", "EAR-FA-MODE")

    def test_unauthorized_actor_fails(self):
        """PITC created_by not the Research Director token → FAIL."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology(
            created_by="Evidence Intelligence Lead"
        )
        ev = _make_ev(source_id, "EV-FA-UNAUTH")
        ear = _make_live_ear("EV-FA-UNAUTH", "EAR-FA-UNAUTH", pitc_id)
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any(
            "Research Director" in str(e) for e in exc.value.errors
        )
        assert not ev_registry.contains("EAR-01", "EAR-FA-UNAUTH")

    def test_spoofed_actor_text_fails(self):
        """Substring spoofs must FAIL — created_by must be the exact token.

        Values like "Fake Research Director", "Not Research Director", and
        "Research Director impostor" contain the substring but are NOT the
        canonical role.  They must be rejected (Commit C proved the old
        substring rule accepted them).
        """
        for spoof in ("Fake Research Director", "Not Research Director",
                      "Research Director impostor", "Research Director: test"):
            _, _, ev_registry, pitc_id, source_id = _five_anchor_topology(
                created_by=spoof
            )
            ev = _make_ev(source_id, f"EV-SPOOF-{len(spoof)}")
            ear = _make_live_ear(
                f"EV-SPOOF-{len(spoof)}", f"EAR-SPOOF-{len(spoof)}", pitc_id
            )
            with pytest.raises(TransactionFailure) as exc:
                ev_registry.admit_evidence(ev, ear)
            assert any(
                "does not represent Research Director authority"
                in str(e) for e in exc.value.errors
            )

    def test_missing_provenance_fails(self):
        """is_update=true without update_provenance → FAIL."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology()
        ev = _make_ev(source_id, "EV-FA-NO-PROV")
        ear = _make_live_ear("EV-FA-NO-PROV", "EAR-FA-NO-PROV", pitc_id,
                             provenance="")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any("update_provenance" in str(e) for e in exc.value.errors)
        assert not ev_registry.contains("EAR-01", "EAR-FA-NO-PROV")

    def test_missing_pit_context_id_fails(self):
        """is_update=true without update_pit_context_id → FAIL."""
        _, _, ev_registry, _pitc_id, source_id = _five_anchor_topology()
        ev = _make_ev(source_id, "EV-FA-NO-ID")
        ear = _make_live_ear("EV-FA-NO-ID", "EAR-FA-NO-ID", None)
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any("update_pit_context_id" in str(e) for e in exc.value.errors)
        assert not ev_registry.contains("EAR-01", "EAR-FA-NO-ID")

    def test_fail_closed_without_authoritative_pitc_store(self):
        """LIVE update when the authoritative PITContextStore is UNAVAILABLE
        → FAIL CLOSED (the PITC cannot be resolved — no shadow fallback)."""
        src_archive = InMemoryRawSourceArchive()
        _admit_src(src_archive, "SRC-FA-FC", b"fail-closed source")
        # Registry constructed WITHOUT the authoritative PITContextStore
        ev_registry = InMemoryEvidenceRegistry(source_archive=src_archive)
        ev = _make_ev("SRC-FA-FC", "EV-FA-FC")
        ear = _make_live_ear("EV-FA-FC", "EAR-FA-FC", "PITC-FA-FC")
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        joined = "\n".join(str(e) for e in exc.value.errors)
        assert "PITC-01" in joined or "update_pit_context_id" in joined
        assert not ev_registry.contains("EAR-01", "EAR-FA-FC")


class TestExactResearchDirectorAuthorization:
    """Exact canonical role token — machine-readable LIVE authorization.

    ``created_by == "Research Director"`` (SM-12).  Substring matching is
    forbidden; ``update_provenance`` is human provenance, NEVER authorization.
    """

    def test_exact_token_passes(self):
        """Exact token 'Research Director' is the ONLY accepted authority."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology(
            created_by="Research Director"
        )
        ev = _make_ev(source_id, "EV-EXACT-1")
        ear = _make_live_ear("EV-EXACT-1", "EAR-EXACT-1", pitc_id)
        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64

    @pytest.mark.parametrize(
        "spoof",
        ["Research Director impostor",
         "Researcher Director",
         "Research director",
         "research director",
         "Research Director Extra",
         "The Research Director"],
    )
    def test_substring_and_case_spoofs_fail(self, spoof):
        """Any created_by that merely resembles / contains the token → FAIL."""
        _, _, ev_registry, pitc_id, source_id = _five_anchor_topology(
            created_by=spoof
        )
        ev = _make_ev(source_id, f"EV-CASE-{abs(hash(spoof)) % 100000}")
        ear = _make_live_ear(
            f"EV-CASE-{abs(hash(spoof)) % 100000}",
            f"EAR-CASE-{abs(hash(spoof)) % 100000}", pitc_id,
        )
        with pytest.raises(TransactionFailure) as exc:
            ev_registry.admit_evidence(ev, ear)
        assert any(
            "does not represent Research Director authority"
            in str(e) for e in exc.value.errors
        )