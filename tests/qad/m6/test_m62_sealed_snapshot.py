"""M6.2 — SEALED Input Snapshot Builder / PIT boundary — acceptance tests (FD #150 / FD #151).

RED→GREEN suite for the M6.2 cluster. Proves the SEALED provider-input snapshot is
built ONLY from authoritative PIT context + archive-attested exact bytes admitted
at or before AS_OF, deterministically, with no silent partial corpus.

Run:  pytest tests/qad/m6/test_m62_sealed_snapshot.py -q
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib

import pytest

from qad.models.family_b import (
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
    SourceVersion,
)
from qad.models.family_i import PITContext, PITContextMode
from qad.persistence.reference import InMemoryPITContextStore, InMemoryRawSourceArchive
from qad.m6.snapshot import (
    SealedInputSnapshot,
    SnapshotBuildError,
    SnapshotFailureCode,
    build_sealed_input_snapshot,
)


# =====================================================================
# Helpers
# =====================================================================

AS_OF = "2026-01-01"
ADMITTED = "2025-12-15T00:00:00+00:00"


def _src(sid: str, raw: bytes, retrieval_date: str = "2025-12-01") -> SourceRecord:
    return SourceRecord(
        source_id=sid, source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/{sid}",
        content_hash=hashlib.sha256(raw).hexdigest(), retrieval_date=retrieval_date,
    )


def _archive(admitted_at_iso: str = ADMITTED) -> InMemoryRawSourceArchive:
    fixed = dt.datetime.fromisoformat(admitted_at_iso)
    return InMemoryRawSourceArchive(clock=lambda: fixed)


def _seed_case(store, case_id: str) -> None:
    from qad.models import CandidateRecord, CaseRecord, SecurityMaster
    from qad.models.family_a import (
        CandidateRecordEntry_route,
        CandidateRecordSelection_state,
        CaseRecordCase_state,
        SecurityMasterSecurity_type,
        SecurityMasterStatus,
    )
    sm = SecurityMaster(
        entity_id=f"SM-{case_id}", cik="0000998877", exchange="NYSE",
        name="M62 Corp", primary_ticker="M62X",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id=f"CR-{case_id}", entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2025-10-01T00:00:00", evidence_freshness="2025-11-01",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW, signal_ids=[],
    )
    store.store(cand)
    store.store(CaseRecord(
        case_id=case_id, entity_id=sm.entity_id, candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN, as_of_date=AS_OF,
        opened_at="2025-10-02T08:00:00", research_director="Research Director",
    ))


def _pit(store: InMemoryPITContextStore, *, mode=PITContextMode.SEALED_HISTORICAL_EVALUATION,
         as_of: str = AS_OF, case_id: str = "CASE-1", pid: str = "PITC-1") -> str:
    if not store.contains("CASE-01", case_id):
        _seed_case(store, case_id)
    store.store(PITContext(
        pit_context_id=pid, case_id=case_id, as_of_date=as_of,
        mode=mode, created_by="founder",
    ))
    return pid


def _admit(store: InMemoryRawSourceArchive, sid: str, raw: bytes, retrieval_date="2025-12-01"):
    store.admit_source(_src(sid, raw, retrieval_date), raw)


def _build(archive, pit_store, *, source_ids, pit_context_id="PITC-1",
           case_version="v1", clock=None):
    return build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id=pit_context_id,
        case_version=case_version, source_ids=list(source_ids),
        **({"clock": clock} if clock is not None else {}),
    )


# =====================================================================
# 1–4: happy path, order invariance, canonical ordering, duplicates
# =====================================================================

class TestBuildAndOrdering:
    def test_valid_sealed_context_and_eligible_source_builds(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"alpha")
        pid = _pit(p)
        snap = _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert isinstance(snap, SealedInputSnapshot)
        assert snap.source_count == 1
        assert snap.case_id == "CASE-1"
        assert snap.case_version == "v1"
        assert snap.pit_context_id == pid
        assert snap.pit_mode == "SEALED_HISTORICAL_EVALUATION"
        assert snap.as_of == AS_OF
        assert snap.ordered_sources[0].source_id == "S1"
        assert snap.ordered_sources[0].raw_bytes == b"alpha"

    def test_request_order_does_not_change_hash(self):
        a, p = _archive(), InMemoryPITContextStore()
        for sid, raw in (("S3", b"c"), ("S1", b"a"), ("S2", b"b")):
            _admit(a, sid, raw)
        pid = _pit(p)
        h1 = _build(a, p, source_ids=["S1", "S2", "S3"], pit_context_id=pid).input_snapshot_hash
        h2 = _build(a, p, source_ids=["S3", "S1", "S2"], pit_context_id=pid).input_snapshot_hash
        h3 = _build(a, p, source_ids=["S2", "S3", "S1"], pit_context_id=pid).input_snapshot_hash
        assert h1 == h2 == h3

    def test_canonical_source_ordering_deterministic(self):
        a, p = _archive(), InMemoryPITContextStore()
        for sid in ("S3", "S1", "S2"):
            _admit(a, sid, sid.encode())
        pid = _pit(p)
        snap = _build(a, p, source_ids=["S3", "S1", "S2"], pit_context_id=pid)
        assert [s.source_id for s in snap.ordered_sources] == ["S1", "S2", "S3"]

    def test_duplicate_source_ids_rejected(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1", "S1"], pit_context_id=pid)
        assert exc.value.code is SnapshotFailureCode.DUPLICATE_SOURCE_ID


# =====================================================================
# 5–6: PIT authority
# =====================================================================

class TestPITAuthority:
    def test_missing_pit_context_fails_closed(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id="NOPE")
        assert exc.value.code is SnapshotFailureCode.PIT_CONTEXT_NOT_FOUND

    def test_non_sealed_pit_mode_rejected(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p, mode=PITContextMode.LIVE_CASE_UPDATE)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.code is SnapshotFailureCode.PIT_MODE_NOT_SEALED

    def test_unreadable_pit_context_fails_closed(self, monkeypatch):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p)

        def _boom(*_a, **_k):
            raise RuntimeError("store unavailable")

        monkeypatch.setattr(p, "load", _boom)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.code is SnapshotFailureCode.PIT_CONTEXT_UNAVAILABLE


# =====================================================================
# 7–12: per-source FD #150 conditions
# =====================================================================

class TestSourceConditions:
    def test_source_not_found(self):
        a, p = _archive(), InMemoryPITContextStore()
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["MISSING"], pit_context_id=pid)
        assert exc.value.verdicts["MISSING"] is SnapshotFailureCode.SOURCE_NOT_FOUND

    def test_legacy_unattested_src01_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        a._attestations.pop("S1")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.LEGACY_UNATTESTED_SRC01

    def test_srcv_only_capture_proof_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        raw = b"srcv"
        _admit(a, "S1", raw)
        a.store(SourceVersion(
            version_id="S1-V1", source_id="S1", version_number="1",
            retrieval_date="2025-12-01", content_hash=hashlib.sha256(raw).hexdigest(),
        ))
        a._attestations.pop("S1")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.SRCV_ONLY_CAPTURE_PROOF

    def test_admitted_after_as_of_blocked(self):
        a = _archive(admitted_at_iso="2026-02-01T00:00:00+00:00")
        _admit(a, "S1", b"a")
        pid = _pit(p := InMemoryPITContextStore())
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.SOURCE_ADMITTED_AFTER_AS_OF

    def test_corrupted_source_identity_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        a._attestations["S1"] = dataclasses.replace(a._attestations["S1"], source_id="OTHER")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE

    def test_corrupted_raw_blob_hash_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        a._raw_blobs["S1"] = b"tampered different bytes"
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE

    def test_byte_length_mismatch_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        a._attestations["S1"] = dataclasses.replace(a._attestations["S1"], raw_byte_length=999)
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE

    def test_raw_blob_unavailable_blocked(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        a._raw_blobs.pop("S1")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.RAW_BLOB_UNAVAILABLE


# =====================================================================
# 13–15: byte authority, no partial corpus, exact bytes
# =====================================================================

class TestByteAuthority:
    def test_detached_caller_bytes_cannot_override(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"archive truth")
        pid = _pit(p)
        snap = _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert snap.ordered_sources[0].raw_bytes == b"archive truth"
        # the builder's public signature accepts source ids only — no bytes seam
        import inspect
        sig = inspect.signature(build_sealed_input_snapshot)
        assert "raw_bytes" not in sig.parameters
        assert "sources" not in sig.parameters

    def test_mixed_set_with_one_invalid_fails_entirely(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        _admit(a, "S2", b"b")
        a._raw_blobs["S2"] = b"corrupt"
        _admit(a, "S3", b"c")
        pid = _pit(p)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1", "S2", "S3"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is None          # S1 itself is fine
        assert exc.value.verdicts["S2"] is SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE
        assert exc.value.code is SnapshotFailureCode.SNAPSHOT_BUILD_FAILED

    def test_mutable_buffer_cannot_mutate_stored_or_snapshot_bytes(self):
        a, p = _archive(), InMemoryPITContextStore()
        buf = bytearray(b"mutable bytes")
        a.admit_source(SourceRecord(
            source_id="S1", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/S1",
            content_hash=hashlib.sha256(bytes(buf)).hexdigest(),
            retrieval_date="2025-12-01"), buf)
        buf[0:7] = b"MUTATED"           # mutate the caller buffer AFTER admission
        pid = _pit(p)
        snap = _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert isinstance(snap.ordered_sources[0].raw_bytes, bytes)
        assert snap.ordered_sources[0].raw_bytes == b"mutable bytes"
        assert a.load_raw_blob("S1") == b"mutable bytes"

    def test_snapshot_contains_exact_verified_bytes(self):
        a, p = _archive(), InMemoryPITContextStore()
        raw = b"\x00\x01exact\xff"
        _admit(a, "S1", raw)
        pid = _pit(p)
        snap = _build(a, p, source_ids=["S1"], pit_context_id=pid)
        s = snap.ordered_sources[0]
        assert s.raw_bytes == raw
        assert hashlib.sha256(s.raw_bytes).hexdigest() == s.raw_blob_sha256
        assert s.raw_blob_sha256 == s.source_content_hash == a.get_admission_attestation("S1").raw_blob_sha256
        assert s.raw_byte_length == len(raw)
        assert s.archive_attestation_id == a.get_admission_attestation("S1").attestation_id


# =====================================================================
# 16–19: deterministic hash
# =====================================================================

class TestDeterministicHash:
    def _one_source_snapshot(self, a, p, *, as_of=AS_OF, case_version="v1", clock=None):
        pid = _pit(p, as_of=as_of)
        return _build(a, p, source_ids=["S1"], pit_context_id=pid,
                      case_version=case_version, clock=clock)

    def test_hash_excludes_volatile_creation_time(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        t1 = lambda: dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
        t2 = lambda: dt.datetime(2030, 6, 6, tzinfo=dt.timezone.utc)
        s1 = self._one_source_snapshot(a, p, clock=t1)
        s2 = self._one_source_snapshot(a, p, clock=t2)
        assert s1.created_at != s2.created_at          # operational metadata differs
        assert s1.input_snapshot_hash == s2.input_snapshot_hash

    def test_equivalent_inputs_in_separate_archives_same_hash(self):
        """Same semantic inputs captured in two archives must hash identically.

        Attestation ids are random uuid4 — they must NOT be identity inputs.
        """
        p = InMemoryPITContextStore()
        a1 = _archive(); _admit(a1, "S1", b"same")
        a2 = _archive(); _admit(a2, "S1", b"same")
        pid = _pit(p)
        h1 = _build(a1, p, source_ids=["S1"], pit_context_id=pid).input_snapshot_hash
        h2 = _build(a2, p, source_ids=["S1"], pit_context_id=pid).input_snapshot_hash
        assert a1.get_admission_attestation("S1").attestation_id != \
            a2.get_admission_attestation("S1").attestation_id
        assert h1 == h2

    def test_changing_one_raw_byte_changes_hash(self):
        p = InMemoryPITContextStore()
        a1 = _archive(); _admit(a1, "S1", b"original")
        a2 = _archive(); _admit(a2, "S1", b"modified")
        h1 = self._one_source_snapshot(a1, p).input_snapshot_hash
        h2 = self._one_source_snapshot(a2, p).input_snapshot_hash
        assert h1 != h2

    def test_changing_as_of_changes_hash(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        h1 = _build(a, p, source_ids=["S1"], pit_context_id=_pit(p, as_of="2026-01-01", pid="P1")).input_snapshot_hash
        h2 = _build(a, p, source_ids=["S1"], pit_context_id=_pit(p, as_of="2026-01-02", pid="P2")).input_snapshot_hash
        assert h1 != h2

    def test_changing_case_version_changes_hash(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p)
        h1 = _build(a, p, source_ids=["S1"], pit_context_id=pid, case_version="v1").input_snapshot_hash
        h2 = _build(a, p, source_ids=["S1"], pit_context_id=pid, case_version="v2").input_snapshot_hash
        assert h1 != h2


# =====================================================================
# 20–22: closed corpus, backdating, construction-time verification
# =====================================================================

class TestPolicyInvariants:
    def test_closed_corpus_required_always_true(self):
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        snap = _build(a, p, source_ids=["S1"], pit_context_id=_pit(p))
        assert snap.closed_corpus_required is True

    def test_backdated_retrieval_date_cannot_bypass_admitted_at(self):
        """Caller sets retrieval_date 2025-12-01 but archive admitted at 2026-02-01."""
        a = _archive(admitted_at_iso="2026-02-01T00:00:00+00:00")
        _admit(a, "S1", b"a", retrieval_date="2025-12-01")
        pid = _pit(p := InMemoryPITContextStore(), as_of="2026-01-01")
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.SOURCE_ADMITTED_AFTER_AS_OF
        assert dt.date.fromisoformat("2025-12-01") < dt.date.fromisoformat("2026-01-01")

    def test_finalization_revalidates_archive_authority(self, monkeypatch):
        """K must RELOAD/reverify at finalisation, not trust the earlier result."""
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p)
        real = a.verify_admission_attestation
        calls = {"n": 0}

        def flaky(sid):
            calls["n"] += 1
            return real(sid) if calls["n"] == 1 else False

        monkeypatch.setattr(a, "verify_admission_attestation", flaky)
        with pytest.raises(SnapshotBuildError):
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert calls["n"] >= 2          # resolution + finalisation revalidation

    def test_verification_happens_during_construction(self, monkeypatch):
        """A false archive verification at build time must fail the build."""
        a, p = _archive(), InMemoryPITContextStore()
        _admit(a, "S1", b"a")
        pid = _pit(p)
        monkeypatch.setattr(a, "verify_admission_attestation", lambda _sid: False)
        with pytest.raises(SnapshotBuildError) as exc:
            _build(a, p, source_ids=["S1"], pit_context_id=pid)
        assert exc.value.verdicts["S1"] is SnapshotFailureCode.ATTESTATION_INTEGRITY_FAILURE
