"""Erratum-002 Defect B — FIVE-ANCHOR LIVE-UPDATE DIAGNOSTIC (Commit C).

NOT an acceptance suite.  This is the *diagnostic evidence* committed BEFORE the
production fix, reproducing Defect B on the ACTUAL frozen M5.2 topology.

The real M5.2 topology is FIVE SEPARATE store anchors (not the monolithic
generic ``InMemoryCanonicalRecordStore`` used by ``TestLiveUpdateCarrier``):

    RawSourceArchive      — SRC-01 (content-addressed, admit_source gate)
    EvidenceRegistry      — EV-01 + EAR-01 (admit_evidence gate)
    FinancialFactStore    — FF/NFF/CALC/SCEN (lineage)
    RunManifestStore      — RRM-01 (lifecycle)
    PITContextStore       — PITC-01 (point-in-time context)

``InMemoryEvidenceRegistry`` resolves EVs through the authoritative
RawSourceArchive, but its Transaction ``get_existing`` is ``self._load_raw`` —
the registry's OWN dict only.  A LIVE update's ``EAR-01.update_pit_context_id``
FK points at a ``PITC-01`` that lives in the SEPARATE authoritative
``PITContextStore``.  Against baseline 6d76348, that FK / lookup CANNOT
resolve, so a valid LIVE update through the canonical path fails.

These tests assert the CORRECT five-anchor behaviour:

  A. a valid SRC is admitted through ``RawSourceArchive.admit_source()``
  B. a valid PITC is stored in the separate ``PITContextStore``
  C. a valid EV + EAR LIVE update is submitted through the canonical
     ``EvidenceRegistry.admit_evidence()`` path

They are EXPECTED TO FAIL at baseline 6d76348 — that failing result is the
diagnostic proof.  The production fix (Commit D) makes them pass.
"""
from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import ValidationFailure
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceRecord,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
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
from qad.models.family_i import PITContext


# =====================================================================
# Helpers — build the REAL five-anchor topology
# =====================================================================

def _admit_src(store, source_id: str, raw: bytes) -> SourceRecord:
    """Scenario A — admit a valid SRC-01 through RawSourceArchive.admit_source()."""
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
        update_provenance="five-anchor LIVE update provenance",
        update_pit_context_id=pitc_id,
    )


def _make_pitc(pitc_id: str, created_by: str, case_id: str = "CASE-FA-LIVE") -> PITContext:
    """Scenario B — a valid PITC-01 for the separate PITContextStore."""
    return PITContext(
        pit_context_id=pitc_id,
        as_of_date="2024-06-01",
        mode="LIVE_CASE_UPDATE",
        case_id=case_id,
        created_by=created_by,
    )


def _seed_pitc_store(store: InMemoryPITContextStore, case_id: str) -> None:
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


def _make_evidence_registry(src_archive, pitc_store=None):
    """Wire the EvidenceRegistry to its authoritative anchors.

    Pre-fix constructor accepts only ``source_archive``.  Post-fix it also
    accepts ``pit_context_store`` so ``EAR-01.update_pit_context_id`` can be
    resolved against the authoritative PITContextStore (the same authority
    pattern already used for RawSourceArchive).
    """
    kwargs = {"source_archive": src_archive}
    if pitc_store is not None:
        kwargs["pit_context_store"] = pitc_store
    try:
        return InMemoryEvidenceRegistry(**kwargs)
    except TypeError:
        # Pre-Erratum-002-fix constructor — no pit_context_store kwarg.
        # The authoritative PITContextStore is invisible to the registry's
        # resolver, so a LIVE update's PITC FK cannot resolve.
        return InMemoryEvidenceRegistry(source_archive=src_archive)


# =====================================================================
# Commit C diagnostic tests (EXPECTED TO FAIL at baseline 6d76348)
# =====================================================================

class TestFiveAnchorLiveUpdateDiagnostic:
    """Erratum-002 Defect B — LIVE PITC FK resolution on the five-anchor
    topology.  Expected to fail against baseline 6d76348 (monolithic-store
    tests pass only because they never exercise the real separation)."""

    def test_valid_live_update_resolves_authoritative_pitc(self):
        """Scenarios A + B + C — a valid LIVE update through the canonical
        five-anchor path MUST succeed.

        A: SRC admitted via RawSourceArchive.
        B: PITC stored in the separate authoritative PITContextStore.
        C: EV + EAR (is_update, provenance, update_pit_context_id) submitted
           via EvidenceRegistry.admit_evidence().

        At baseline the registry's resolver cannot see PITC-01 in the
        authoritative PITContextStore → ValidationFailure → this FAILS.
        """
        # A — RawSourceArchive anchor
        src_archive = InMemoryRawSourceArchive()
        _admit_src(src_archive, "SRC-FA-LIVE", b"five-anchor live source bytes")

        # B — PITContextStore anchor (REAL separate store)
        pitc_store = InMemoryPITContextStore()
        _seed_pitc_store(pitc_store, "CASE-FA-LIVE")
        pitc_store.store(_make_pitc("PITC-FA-LIVE", created_by="Research Director"))

        # C — EvidenceRegistry wired to both authoritative anchors
        ev_registry = _make_evidence_registry(src_archive, pitc_store)
        ev = _make_ev("SRC-FA-LIVE", "EV-FA-LIVE")
        ear = _make_live_ear("EV-FA-LIVE", "EAR-FA-LIVE", "PITC-FA-LIVE")

        ch = ev_registry.admit_evidence(ev, ear)
        assert isinstance(ch, str) and len(ch) == 64
        loaded_ear = ev_registry.load("EAR-01", "EAR-FA-LIVE")
        assert loaded_ear.is_update is True
        assert loaded_ear.update_pit_context_id == "PITC-FA-LIVE"

    def test_authorization_requires_exact_research_director_token(self):
        """A ``created_by`` that merely CONTAINS the substring ``Research Director``
        (e.g. ``"Fake Research Director"``) must NOT authorize a LIVE update.

        Frozen SM-12 authorizes the LIVE_CASE_UPDATE carrier ONLY when the
        referenced PITContext's ``created_by`` is the exact canonical role
        token ``"Research Director"``.  Substring matching is unsafe:
        ``"Not Research Director"`` / ``"Research Director impostor"`` /
        ``"Fake Research Director"`` all pass a substring check.

        The PITC is placed where the registry's resolver can see it (its own
        store), so this test isolates the authorization check behaviourally.
        """
        from qad.persistence.reference import InMemoryEvidenceRegistry

        src_archive = InMemoryRawSourceArchive()
        _admit_src(src_archive, "SRC-FA-AUTH", b"five-anchor auth source")

        # Seed the case chain + shadow PITC INTO the registry's own store so
        # the LIVE-caller authorization check is actually reached.
        ev_registry = InMemoryEvidenceRegistry(source_archive=src_archive)
        # (registry is an InMemoryEvidenceRegistry subclass; SM/CR/CASE and
        # PITC pass through super().store() — only EV/EAR/SRC are gated.)
        _seed_pitc_store(ev_registry, "CASE-FA-AUTH")  # type: ignore[arg-type]
        ev_registry.store(
            _make_pitc("PITC-FA-AUTH", "Fake Research Director",
                       case_id="CASE-FA-AUTH")
        )

        ev = _make_ev("SRC-FA-AUTH", "EV-FA-AUTH")
        ear = _make_live_ear("EV-FA-AUTH", "EAR-FA-AUTH", "PITC-FA-AUTH")

        with pytest.raises(
            ValidationFailure,
            match="does not represent Research Director authority",
        ):
            ev_registry.admit_evidence(ev, ear)
