"""M5.3 S7 — PIT Runtime Enforcement contract tests (direct, not regression).

Proves the frozen nine-case PIT semantics on the canonical five-anchor
topology, plus the minimum PIT-aware query substrate (collection filtering
and explicit-access PIT block).  All evidence is admitted THROUGH the
canonical admission path (RawSourceArchive.admit_source -> EvidenceRegistry
.admit_evidence) — no store(EV-01)/store(EAR-01) bypass.
"""
from __future__ import annotations

import hashlib

import pytest

from qad.m53.pit_enforcement import PITEnforcementService, PITVerdict
from qad.persistence import PITBlockError
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
    _Record,
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

AS_OF = "2026-01-15"
PRE_DATE = "2025-12-01"     # <= AS_OF
POST_DATE = "2026-06-01"    # >  AS_OF


# =====================================================================
# Topology helpers (five-anchor; same pattern as the Erratum-002 suites)
# =====================================================================

def _admit_src(store, source_id: str, raw: bytes) -> SourceRecord:
    ch = hashlib.sha256(raw).hexdigest()
    src = SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/m53/{source_id}",
        content_hash=ch,
        retrieval_date="2025-11-01",
    )
    store.admit_source(src, raw)
    return src


def _make_ev(source_id: str, evidence_id: str, as_of: str) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        source_id=source_id,
        evidence_type="FACT",
        validation_status="RAW",
        content=f"evidence {evidence_id} @ {as_of}",
        admitting_role="Evidence Intelligence Lead",
        as_of=as_of,
        extractor="v1",
        source_tier="T1",
    )


def _make_ear(
    evidence_id: str,
    admission_id: str,
    *,
    is_update: bool = False,
    pitc_id: str | None = None,
) -> EvidenceAdmissionRecord:
    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        evidence_id=evidence_id,
        admitting_role="Evidence Intelligence Lead",
        admission_timestamp="2025-11-02T12:00:00",
        admission_method="DIRECT_SOURCE",
        validation_method="SOURCE_CROSS_REFERENCE",
        source_tier_check="T1",
        is_update=is_update,
        update_provenance="m53-live-carrier update" if is_update else None,
        update_pit_context_id=pitc_id if is_update else None,
    )


def _make_pitc(
    pitc_id: str,
    created_by: str,
    case_id: str,
    *,
    mode: str = "SEALED_HISTORICAL_EVALUATION",
    as_of_date: str = AS_OF,
    exception_reason: str | None = None,
) -> PITContext:
    return PITContext(
        pit_context_id=pitc_id,
        as_of_date=as_of_date,
        mode=mode,
        case_id=case_id,
        created_by=created_by,
        exception_reason=exception_reason,
    )


def _seed_pitc_store(store, case_id: str) -> None:
    sm = SecurityMaster(
        entity_id="E-M53-001", cik="0000998877", exchange="NYSE",
        name="M53 Corp", primary_ticker="M53X",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id="CAND-M53-001", entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2025-10-01T00:00:00", evidence_freshness="2025-11-01",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
        signal_ids=[],
    )
    store.store(cand)
    case = CaseRecord(
        case_id=case_id, entity_id=sm.entity_id,
        candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN,
        as_of_date=AS_OF, opened_at="2025-10-02T08:00:00",
        research_director="Research Director",
    )
    store.store(case)


def _topology():
    src_archive = InMemoryRawSourceArchive()
    pitc_store = InMemoryPITContextStore()
    ev_registry = InMemoryEvidenceRegistry(
        source_archive=src_archive, pit_context_store=pitc_store
    )
    service = PITEnforcementService(
        pitc_store=pitc_store,
        evidence_registry=ev_registry,
        source_archive=src_archive,
    )
    return src_archive, pitc_store, ev_registry, service


def _seed_case_and_src(src_archive, pitc_store, sid="SRC-M53-001",
                       case="CASE-M53-001"):
    _admit_src(src_archive, sid, b"m53 source bytes")
    _seed_pitc_store(pitc_store, case)
    return sid, case


# =====================================================================
# Mode-boundary tests (frozen nine-case)
# =====================================================================

class TestSealedMode:
    def test_sealed_pre_asof_allowed(self):
        """TEST 1 — pre-AS_OF evidence in SEALED mode -> ALLOWED."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-PRE", PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-PRE", "EAR-M53-PRE"))
        pitc = pitc_store.store(
            _make_pitc("PITC-M53-SEAL", "Evidence Intelligence Lead", case)
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-SEAL")
        assert svc.adjudicate(ev, ctx) is PITVerdict.ALLOWED

    def test_sealed_post_asof_blocked(self):
        """TEST 2 — post-AS_OF evidence in SEALED mode -> HARD BLOCK."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-POST", POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-POST", "EAR-M53-POST"))
        pitc_store.store(
            _make_pitc("PITC-M53-SEAL", "Evidence Intelligence Lead", case)
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-SEAL")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED

    def test_tampered_sealed_evidence_invalidated(self):
        """TEST 7 — canonical-hash tamper on a sealed record -> SEAL_INVALIDATED."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-TAMPER", PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-TAMPER", "EAR-M53-TAMPER"))
        pitc_store.store(
            _make_pitc("PITC-M53-SEAL", "Evidence Intelligence Lead", case)
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-SEAL")

        # Tamper: replace the stored record with a MODIFIED copy whose
        # recorded canonical hash no longer matches its content.
        forged = _make_ev(sid, "EV-M53-TAMPER", PRE_DATE)
        forged = forged.model_copy(update={"content": "tampered content"})
        ev_reg._data["EV-01"]["EV-M53-TAMPER"] = _Record(
            instance=forged, canonical_hash="0" * 64,
        )

        assert svc.adjudicate(forged, ctx) is PITVerdict.SEAL_INVALIDATED


class TestLiveMode:
    def test_live_post_asof_without_carrier_blocked(self):
        """TEST 3 — post-AS_OF in LIVE without update carrier -> BLOCK."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-LIVE1", POST_DATE)
        # admission WITHOUT is_update carrier
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-LIVE1", "EAR-M53-LIVE1"))
        pitc_store.store(
            _make_pitc("PITC-M53-LIVE", "Research Director", case,
                       mode="LIVE_CASE_UPDATE")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-LIVE")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED

    def test_live_post_asof_with_valid_carrier_allowed(self):
        """TEST 4 — post-AS_OF in LIVE with valid Erratum-002 carrier -> ALLOWED."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        pitc_store.store(
            _make_pitc("PITC-M53-LIVE2", "Research Director", case,
                       mode="LIVE_CASE_UPDATE")
        )
        ev = _make_ev(sid, "EV-M53-LIVE2", POST_DATE)
        ear = _make_ear("EV-M53-LIVE2", "EAR-M53-LIVE2",
                        is_update=True, pitc_id="PITC-M53-LIVE2")
        ev_reg.admit_evidence(ev, ear)
        ctx = pitc_store.load("PITC-01", "PITC-M53-LIVE2")
        assert svc.adjudicate(ev, ctx) is PITVerdict.ALLOWED

    def test_live_carrier_chained_to_wrong_pitc_blocked(self):
        """A LIVE carrier pointing at a DIFFERENT PITC must not satisfy the
        adjudication against this context (authority chain is exact)."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        # The update is authorized under PITC-M53-OTHER (its own LIVE context).
        pitc_store.store(
            _make_pitc("PITC-M53-OTHER", "Research Director", case,
                       mode="LIVE_CASE_UPDATE")
        )
        ev = _make_ev(sid, "EV-M53-LIVE3", POST_DATE)
        ear = _make_ear("EV-M53-LIVE3", "EAR-M53-LIVE3",
                        is_update=True, pitc_id="PITC-M53-OTHER")
        ev_reg.admit_evidence(ev, ear)
        # Adjudicate against a DIFFERENT LIVE context (PITC-M53-LIVE3): the
        # authorized chain does not transfer to another context.
        pitc_store.store(
            _make_pitc("PITC-M53-LIVE3", "Research Director", case,
                       mode="LIVE_CASE_UPDATE")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-LIVE3")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED

    def test_live_carrier_requires_exact_rd_token(self):
        """A LIVE PITC created by a spoofed/other actor must not authorize
        the update (exact canonical token, SM-12 / Erratum-002).

        The admission gate already rejects a spoofed carrier at WRITE time
        (fail closed).  Here we additionally prove the QUERY-TIME adjudicator
        resists it: the adversarial EAR is injected directly into the
        registry (tamper simulation) and the service must STILL block.
        """
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        # LIVE PITC whose created_by CONTAINS the words but is not exact.
        pitc_store.store(
            _make_pitc("PITC-M53-LIVE4", "Fake Research Director", case,
                       mode="LIVE_CASE_UPDATE")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-LIVE4")
        ev = _make_ev(sid, "EV-M53-LIVE4", POST_DATE)
        ear = _make_ear("EV-M53-LIVE4", "EAR-M53-LIVE4",
                        is_update=True, pitc_id="PITC-M53-LIVE4")
        # Adversarial injection (bypasses the write gate deliberately).
        from qad.persistence.reference import _Record
        from qad.persistence.serialization import compute_canonical_hash
        ev_reg._data.setdefault("EV-01", {})["EV-M53-LIVE4"] = _Record(
            instance=ev, canonical_hash=compute_canonical_hash(ev))
        ev_reg._data.setdefault("EAR-01", {})["EAR-M53-LIVE4"] = _Record(
            instance=ear, canonical_hash=compute_canonical_hash(ear))
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED


class TestReplayMode:
    def test_replay_without_provenance_blocked(self):
        """TEST 5 — REPLAY_EXCEPTION without exception reason -> BLOCK."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-REP1", POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-REP1", "EAR-M53-REP1"))
        pitc_store.store(
            _make_pitc("PITC-M53-REP1", "FOUNDER", case,
                       mode="REPLAY_EXCEPTION", exception_reason=None)
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-REP1")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED

    def test_replay_with_founder_allowed(self):
        """TEST 6 — exact FOUNDER actor + exception reason -> ALLOWED."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-REP2", POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-REP2", "EAR-M53-REP2"))
        pitc_store.store(
            _make_pitc("PITC-M53-REP2", "FOUNDER", case,
                       mode="REPLAY_EXCEPTION",
                       exception_reason="evaluation replay")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-REP2")
        assert svc.adjudicate(ev, ctx) is PITVerdict.ALLOWED

    def test_replay_unauthorized_actor_blocked(self):
        """TEST 8 — Research Director actor (not FOUNDER) -> BLOCK."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-REP3", POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-REP3", "EAR-M53-REP3"))
        pitc_store.store(
            _make_pitc("PITC-M53-REP3", "Research Director", case,
                       mode="REPLAY_EXCEPTION",
                       exception_reason="replay by RD")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-REP3")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED

    def test_replay_spoofed_authority_blocked(self):
        """TEST 9 — spoofed text containing 'Founder' but != exact token -> BLOCK."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        ev = _make_ev(sid, "EV-M53-REP4", POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear("EV-M53-REP4", "EAR-M53-REP4"))
        pitc_store.store(
            _make_pitc("PITC-M53-REP4", "Founder Admin", case,
                       mode="REPLAY_EXCEPTION",
                       exception_reason="replay by Founder Admin")
        )
        ctx = pitc_store.load("PITC-01", "PITC-M53-REP4")
        assert svc.adjudicate(ev, ctx) is PITVerdict.BLOCKED


# =====================================================================
# Minimum PIT-aware query substrate
# =====================================================================

class TestPitAwareQuerySubstrate:
    def _sealed_context_with_mixed_evidence(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed_case_and_src(src, pitc_store)
        pre = _make_ev(sid, "EV-M53-PREQ", PRE_DATE)
        post = _make_ev(sid, "EV-M53-POSTQ", POST_DATE)
        ev_reg.admit_evidence(pre, _make_ear("EV-M53-PREQ", "EAR-M53-PREQ"))
        ev_reg.admit_evidence(post, _make_ear("EV-M53-POSTQ", "EAR-M53-POSTQ"))
        pitc_store.store(
            _make_pitc("PITC-M53-Q", "Evidence Intelligence Lead", case)
        )
        return ev_reg, svc, pre, post

    def test_collection_query_filters_invalid_evidence(self):
        """TEST 10 — collection query excludes post-AS_OF in SEALED mode."""
        ev_reg, svc, pre, post = self._sealed_context_with_mixed_evidence()
        result = svc.query("PITC-M53-Q")
        ids = {r.evidence_id for r in result.records}
        assert pre.evidence_id in ids
        assert post.evidence_id not in ids
        assert result.excluded_count == 1
        assert result.blocked_count == 0

    def test_explicit_forbidden_access_returns_pit_block(self):
        """TEST 11 — explicit access to forbidden evidence -> PITBlockError
        (deterministic contract error, NOT a silent empty result)."""
        ev_reg, svc, pre, post = self._sealed_context_with_mixed_evidence()
        # allowed access works
        assert svc.access("EV-M53-PREQ", "PITC-M53-Q").evidence_id == "EV-M53-PREQ"
        # forbidden access raises a deterministic PIT block
        with pytest.raises(PITBlockError) as exc:
            svc.access("EV-M53-POSTQ", "PITC-M53-Q")
        assert exc.value.verdict == "BLOCKED"
        assert "post_as_of_in_sealed_context" in exc.value.reason
        assert exc.value.schema_id == "EV-01"
        assert exc.value.record_id == "EV-M53-POSTQ"

    def test_no_forbidden_leakage_into_returned_context(self):
        """TEST 12 — returned context contains ONLY PIT-valid evidence;
        tamper-invalidated records are counted, never returned."""
        ev_reg, svc, pre, post = self._sealed_context_with_mixed_evidence()

        # Tamper the POST record's stored canonical hash (seal corruption).
        forged = post.model_copy(update={"content": "forged content"})
        ev_reg._data["EV-01"]["EV-M53-POSTQ"] = _Record(
            instance=forged, canonical_hash="0" * 64,
        )

        result = svc.query("PITC-M53-Q")
        ids = {r.evidence_id for r in result.records}
        assert pre.evidence_id in ids
        assert "EV-M53-POSTQ" not in ids          # never leaks
        assert result.blocked_count == 1           # seal-invalidated, counted
        # Might also be excluded_count 0 because tamper is decided first.
        assert result.excluded_count == 0

    def test_query_fails_closed_when_pitc_unavailable(self):
        """Missing authoritative PIT context -> PITBlockError (fail closed)."""
        src, pitc_store, ev_reg, svc = _topology()
        with pytest.raises(PITBlockError):
            svc.query("PITC-NO-SUCH")
        with pytest.raises(PITBlockError):
            svc.access("EV-M53-PREQ", "PITC-NO-SUCH")