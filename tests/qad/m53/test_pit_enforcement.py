"""M5.3 S7 — PIT Runtime Enforcement contract tests (CORRECTION ROUND — FD #138).

Encodes the Founder decisions from FD #138:
- Public PIT surface is ID-based: service resolves authoritative PITC/EV/EAR from
  canonical stores; caller-supplied authority OBJECTS are NOT accepted (no
  forged object can authorize).
- Source-time PIT: effective_pit_time = MAX(EV-01.as_of, authoritative source
  availability time). SEALED requires SRC-01.publication_date (missing => PIT
  BLOCK); LIVE/REPLAY fall back to retrieval_date when publication_date absent.
  Unresolvable/uninterpretable source metadata => FAIL CLOSED (typed error).
- Store failure => fail closed (typed error), never a silent empty result.
- EV canonical-hash check = defense-in-depth 'record integrity / tamper
  detection', NOT the M4B TEST-7 corpus-seal proof.
"""
from __future__ import annotations

import hashlib

import pytest

from qad.m53.pit_enforcement import PITEnforcementService, PITVerdict
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceRecord,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_i import PITContext
from qad.persistence import PITBlockError
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
    _Record,
)

AS_OF = "2026-01-15"
PRE_DATE = "2025-12-01"      # <= AS_OF
POST_DATE = "2026-06-01"     # >  AS_OF
PUB_PRE = "2025-12-01"       # source published pre-AS_OF
PUB_POST = "2026-02-15"      # source published post-AS_OF (future-leak case)
RETRIEVAL_POST = "2026-02-10"  # retrieval after AS_OF (conservative LIVE/REPLAY)


def _u7(n: int) -> str:
    return f"00000000-0000-7000-8000-{n:012x}"


# =====================================================================
# Topology helpers (five-anchor; same pattern as the Erratum-002 suites)
# =====================================================================

def _admit_src(store, source_id: str, raw: bytes, *,
               publication_date: str | None = PUB_PRE,
               retrieval_date: str = "2025-11-01") -> SourceRecord:
    ch = hashlib.sha256(raw).hexdigest()
    src = SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/m53/{source_id}",
        content_hash=ch,
        retrieval_date=retrieval_date,
        publication_date=publication_date,
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


def _make_ear(evidence_id: str, admission_id: str, *,
              is_update: bool = False,
              pitc_id: str | None = None) -> EvidenceAdmissionRecord:
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


def _make_pitc(pitc_id: str, created_by: str, case_id: str, *,
               mode: str = "SEALED_HISTORICAL_EVALUATION",
               as_of_date: str = AS_OF,
               exception_reason: str | None = None) -> PITContext:
    return PITContext(
        pit_context_id=pitc_id,
        as_of_date=as_of_date,
        mode=mode,
        case_id=case_id,
        created_by=created_by,
        exception_reason=exception_reason,
    )


def _seed_pitc_store(store, case_id: str) -> None:
    from qad.models import CandidateRecord, CaseRecord, SecurityMaster
    from qad.models.family_a import (
        CandidateRecordEntry_route,
        CandidateRecordSelection_state,
        CaseRecordCase_state,
        SecurityMasterSecurity_type,
        SecurityMasterStatus,
    )
    sm = SecurityMaster(
        entity_id=_u7(0x900), cik="0000998877", exchange="NYSE",
        name="M53 Corp", primary_ticker="M53X",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id=_u7(0x910), entity_id=sm.entity_id,
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


def _seed(src_archive, pitc_store, ev_registry, *,
          sid=_u7(1), case="CASE-M53-001", publication_date=PUB_PRE,
          retrieval_date="2025-11-01"):
    _admit_src(src_archive, sid, b"m53 source bytes",
               publication_date=publication_date,
               retrieval_date=retrieval_date)
    _seed_pitc_store(pitc_store, case)
    return sid, case


# =====================================================================
# Mode-boundary tests (frozen nine-case preserved, ID-based surface)
# =====================================================================

class TestSealedMode:
    def test_sealed_pre_asof_allowed(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(2), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(3)))
        pitc = _make_pitc(_u7(4), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.ALLOWED

    def test_sealed_post_asof_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(5), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(6)))
        pitc = _make_pitc(_u7(7), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED

    def test_sealed_missing_publication_date_is_blocked(self):
        """FD #138 §11: SEALED requires SRC-01.publication_date.
        Missing => PIT BLOCK (source not eligible), even pre-AS_OF evidence."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=None,
                          retrieval_date="2025-11-01")
        ev = _make_ev(sid, _u7(8), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(9)))
        pitc = _make_pitc(_u7(10), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED

    def test_backdated_ev_with_post_asof_source_publication_blocked(self):
        """FD #138 §11 future-leak: financial period pre-AS_OF (EV.as_of =
        2025-12-31) but the filing was published 2026-02-15 (post-AS_OF).
        effective_pit_time = MAX(EV.as_of, publication_date) => blocked."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST,
                          retrieval_date="2025-11-01")
        ev = _make_ev(sid, _u7(11), "2025-12-31")  # pre-AS_OF-looking period
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(12)))
        pitc = _make_pitc(_u7(13), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED


class TestLiveMode:
    def test_live_post_asof_without_carrier_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(14), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(15)))
        pitc = _make_pitc(_u7(16), "Research Director", case,
                          mode="LIVE_CASE_UPDATE")
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED

    def test_live_post_asof_with_valid_carrier_allowed(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(17), POST_DATE)
        pitc = _make_pitc(_u7(18), "Research Director", case,
                          mode="LIVE_CASE_UPDATE")
        pitc_store.store(pitc)
        ear = _make_ear(ev.evidence_id, _u7(19), is_update=True,
                        pitc_id=pitc.pit_context_id)
        ev_reg.admit_evidence(ev, ear)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.ALLOWED

    def test_live_carrier_chained_to_wrong_pitc_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(20), POST_DATE)
        other = _make_pitc(_u7(21), "Research Director", case,
                           mode="LIVE_CASE_UPDATE")
        pitc_store.store(other)
        ear = _make_ear(ev.evidence_id, _u7(22), is_update=True,
                        pitc_id=other.pit_context_id)
        ev_reg.admit_evidence(ev, ear)
        # adjudicate under a DIFFERENT (authoritative) PITC than the carrier chain
        ctx = _make_pitc(_u7(23), "Research Director", case,
                         mode="LIVE_CASE_UPDATE")
        pitc_store.store(ctx)
        assert svc.adjudicate(ev.evidence_id, ctx.pit_context_id) is PITVerdict.BLOCKED

    def test_live_missing_publication_date_uses_retrieval_date(self):
        """FD #138 §11: LIVE with no publication_date uses retrieval_date as
        conservative availability evidence. A source retrieved after AS_OF
        with no carrier => post-AS_OF => blocked (no leak)."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=None,
                          retrieval_date=RETRIEVAL_POST)
        ev = _make_ev(sid, _u7(24), "2025-12-31")
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(25)))
        pitc = _make_pitc(_u7(26), "Research Director", case,
                          mode="LIVE_CASE_UPDATE")
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED


class TestReplayMode:
    def test_replay_with_founder_and_reason_allowed(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(27), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(28)))
        pitc = _make_pitc(_u7(29), "FOUNDER", case,
                          mode="REPLAY_EXCEPTION", exception_reason="replay")
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.ALLOWED

    def test_replay_without_reason_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(30), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(31)))
        pitc = _make_pitc(_u7(32), "FOUNDER", case, mode="REPLAY_EXCEPTION")
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED

    def test_replay_unauthorized_actor_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(33), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(34)))
        pitc = _make_pitc(_u7(35), "Research Director", case,
                          mode="REPLAY_EXCEPTION", exception_reason="replay")
        pitc_store.store(pitc)
        assert svc.adjudicate(ev.evidence_id, pitc.pit_context_id) is PITVerdict.BLOCKED


# =====================================================================
# FD #138 §9 — public surface is ID-based (no caller-supplied objects)
# =====================================================================

class TestPublicAuthorityBoundary:
    def test_public_adjudicate_accepts_only_ids(self):
        """A caller-supplied PITContext/EAR object must NOT be accepted by the
        public surface — the service resolves authority from stores itself."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(36), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(37)))
        pitc = _make_pitc(_u7(38), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        # Forged object with fully valid-looking fields — must not be usable.
        forged = _make_pitc(_u7(39), "FOUNDER", case,
                            mode="REPLAY_EXCEPTION", exception_reason="x")
        # Signature check: adjudicate raises TypeError for object args.
        with pytest.raises(TypeError):
            svc.adjudicate(ev, forged)  # type: ignore[arg-type]

    def test_public_adjudicate_has_no_ear_parameter(self):
        """No caller-supplied EAR — LIVE carrier is always resolved from the
        authoritative EvidenceRegistry."""
        import inspect
        sig = inspect.signature(
            PITEnforcementService.adjudicate)
        assert "ear" not in sig.parameters
        assert "pitc" not in sig.parameters  # only IDs allowed

    def test_forged_ear_in_store_cannot_authorize(self):
        """A forged EAR whose carrier chain points at a NONEXISTENT
        authoritative PITC is REJECTED AT ADMISSION (Erratum-002 authority
        isolation): the canonical admission gate refuses the FK, so no such
        forged carrier can ever exist in the registry."""
        from qad.persistence.errors import TransactionFailure
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(40), POST_DATE)
        # EAR chained to a PITC that was NEVER stored authoritatively.
        ear = _make_ear(ev.evidence_id, _u7(41), is_update=True,
                        pitc_id=_u7(0xBAD))
        with pytest.raises(TransactionFailure):
            ev_reg.admit_evidence(ev, ear)
        # Nothing was admitted.
        assert len(ev_reg.list_all("EV-01")) == 0


# =====================================================================
# FD #138 §10 — store failures fail closed (never silent empty)
# =====================================================================

class TestFailClosed:
    def test_evidence_registry_failure_blocks_never_empty(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        pitc = _make_pitc(_u7(43), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)

        def boom(*a, **k):
            raise RuntimeError("EvidenceRegistry down")

        ev_reg.list_all = boom
        with pytest.raises(PITBlockError):
            svc.query(pitc.pit_context_id)

    def test_pitc_missing_fails_closed(self):
        src, pitc_store, ev_reg, svc = _topology()
        with pytest.raises(PITBlockError):
            svc.query(_u7(0x44))
        with pytest.raises(PITBlockError):
            svc.access(_u7(0x45), _u7(0x46))

    def test_source_metadata_unresolvable_fails_closed(self):
        """FD #138 §11: source record cannot be resolved => FAIL CLOSED
        (typed error), never treated as 'pre-AS_OF, allowed'."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        # Admit evidence whose source was then removed from the archive.
        ev = _make_ev(sid, _u7(47), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(48)))
        svc._source_archive = None  # simulate archive unavailable
        pitc = _make_pitc(_u7(49), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        with pytest.raises(PITBlockError):
            svc.adjudicate(ev.evidence_id, pitc.pit_context_id)

    def test_uninterpretable_timestamp_fails_closed(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date="not-a-date")
        ev = _make_ev(sid, _u7(50), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(51)))
        pitc = _make_pitc(_u7(52), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        with pytest.raises(PITBlockError):
            svc.adjudicate(ev.evidence_id, pitc.pit_context_id)


# =====================================================================
# Defense-in-depth — EV record integrity (NOT M4B corpus seal)
# =====================================================================

class TestRecordIntegrityDefenseInDepth:
    def test_tampered_evidence_record_invalidated(self):
        """Canonical EV record hash mismatch => SEAL_INVALIDATED. Label: record
        integrity / tamper detection — NOT the M4B TEST-7 corpus-seal proof."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(53), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(54)))
        pitc = _make_pitc(_u7(55), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)

        forged = ev.model_copy(update={"content": "tampered content"})
        ev_reg._data["EV-01"][ev.evidence_id] = _Record(
            instance=forged, canonical_hash="0" * 64,
        )
        verdict = svc.adjudicate(ev.evidence_id, pitc.pit_context_id)
        assert verdict is PITVerdict.SEAL_INVALIDATED

    def test_integrity_error_reason_says_record_integrity(self):
        """The reason string labels the check as record-integrity, not corpus
        seal (founder relabel requirement)."""
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(56), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(57)))
        pitc = _make_pitc(_u7(58), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        forged = ev.model_copy(update={"content": "tampered"})
        ev_reg._data["EV-01"][ev.evidence_id] = _Record(
            instance=forged, canonical_hash="0" * 64,
        )
        with pytest.raises(PITBlockError) as exc:
            svc.access(ev.evidence_id, pitc.pit_context_id)
        assert "record_integrity" in exc.value.reason


# =====================================================================
# Minimum PIT-aware query substrate
# =====================================================================

class TestQuerySubstrate:
    def test_collection_query_filters_invalid_evidence(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        pre = _make_ev(sid, _u7(59), PRE_DATE)
        post = _make_ev(sid, _u7(60), POST_DATE)
        ev_reg.admit_evidence(pre, _make_ear(pre.evidence_id, _u7(61)))
        ev_reg.admit_evidence(post, _make_ear(post.evidence_id, _u7(62)))
        pitc = _make_pitc(_u7(63), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        res = svc.query(pitc.pit_context_id)
        ids = {r.evidence_id for r in res.records}
        assert pre.evidence_id in ids
        assert post.evidence_id not in ids
        assert res.excluded_count == 1  # post-AS_OF evidence excluded

    def test_explicit_forbidden_access_returns_pit_block(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg, publication_date=PUB_POST)
        ev = _make_ev(sid, _u7(64), POST_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(65)))
        pitc = _make_pitc(_u7(66), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        with pytest.raises(PITBlockError):
            svc.access(ev.evidence_id, pitc.pit_context_id)

    def test_query_count_tamper_as_blocked(self):
        src, pitc_store, ev_reg, svc = _topology()
        sid, case = _seed(src, pitc_store, ev_reg)
        ev = _make_ev(sid, _u7(67), PRE_DATE)
        ev_reg.admit_evidence(ev, _make_ear(ev.evidence_id, _u7(68)))
        pitc = _make_pitc(_u7(69), "Evidence Intelligence Lead", case)
        pitc_store.store(pitc)
        forged = ev.model_copy(update={"content": "tampered"})
        ev_reg._data["EV-01"][ev.evidence_id] = _Record(
            instance=forged, canonical_hash="0" * 64,
        )
        res = svc.query(pitc.pit_context_id)
        assert res.records == []
        assert res.blocked_count == 1