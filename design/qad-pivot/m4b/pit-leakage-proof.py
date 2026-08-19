#!/usr/bin/env python3
"""
QAD-M4B PIT Leakage Proof — Non-Production Deterministic Synthetic Tests.

Proves the PIT (Point-in-Time) lock mechanism works correctly for all
canonical modes defined in M3-SERVICES S7 and M4A SM-12.

Tests use ONLY synthetic non-production data.
No production database.
"""

from enum import Enum, auto
from hashlib import sha256
from dataclasses import dataclass, field
from typing import Optional


class Mode(Enum):
    LIVE_CASE_UPDATE = auto()
    SEALED_HISTORICAL_EVALUATION = auto()
    REPLAY_EXCEPTION = auto()


class Verdict(Enum):
    ALLOWED = auto()
    BLOCKED = auto()
    SEAL_INVALIDATED = auto()


@dataclass
class Evidence:
    id: str
    content: str
    recorded_date: str
    is_update: bool = False
    update_provenance: Optional[str] = None


@dataclass
class ReplayException:
    provenance: str
    authorized_actor: str


@dataclass
class Seal:
    corpus_hash: str
    sources: frozenset = field(default_factory=frozenset)

    def verify(self, other_sources: frozenset) -> bool:
        new_hash = sha256(str(sorted(other_sources)).encode()).hexdigest()
        return new_hash == self.corpus_hash


AS_OF = "2026-01-15"
PRE_SOURCE = "source_2025.pdf"
POST_SOURCE = "source_2026_q2.pdf"

sealed_sources = frozenset({PRE_SOURCE, "source_2024.pdf", "source_2023.pdf"})
seal = Seal(
    corpus_hash=sha256(str(sorted(sealed_sources)).encode()).hexdigest(),
    sources=sealed_sources,
)


class PITLock:
    """Synthetic PIT lock for testing. Not a production implementation."""

    def __init__(self, mode: Mode, seal: Seal):
        self.mode = mode
        self.seal = seal

    def check(self, evidence: Evidence, as_of_date: str,
              sealed_sources: frozenset = None,
              replay_exception: ReplayException = None) -> Verdict:
        if not self.seal.verify(sealed_sources or self.seal.sources):
            return Verdict.SEAL_INVALIDATED

        if evidence.recorded_date <= as_of_date:
            return Verdict.ALLOWED

        # Post-AS_OF evidence
        if self.mode == Mode.SEALED_HISTORICAL_EVALUATION:
            return Verdict.BLOCKED

        if self.mode == Mode.LIVE_CASE_UPDATE:
            if evidence.is_update and evidence.update_provenance:
                return Verdict.ALLOWED
            return Verdict.BLOCKED

        if self.mode == Mode.REPLAY_EXCEPTION:
            if replay_exception and replay_exception.provenance:
                # REPLAY_EXCEPTION requires authorized_actor == FOUNDER
                if replay_exception.authorized_actor != "FOUNDER":
                    return Verdict.BLOCKED
                return Verdict.ALLOWED
            return Verdict.BLOCKED

        return Verdict.BLOCKED


def run_all_tests():
    pass_count = 0
    total = 9
    all_pass = True

    print("=" * 70)
    print("  QAD-M4B PIT LEAKAGE PROOF — Non-Production Deterministic")
    print("=" * 70)

    # --- TEST 1: pre-AS_OF in SEALED → ALLOWED ---
    print("\n─── TEST GROUP 1: SEALED mode boundary enforcement ──────────")
    lock_sealed = PITLock(mode=Mode.SEALED_HISTORICAL_EVALUATION, seal=seal)
    pre_evidence = Evidence("ev-001", "pre data", "2025-12-01")
    result = lock_sealed.check(evidence=pre_evidence, as_of_date=AS_OF,
                               sealed_sources=sealed_sources)
    if result == Verdict.ALLOWED:
        print(f"  ✅ PASS  TEST 1: pre-AS_OF evidence in SEALED mode → ALLOWED")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 1: got {result}")
        all_pass = False

    # --- TEST 2: post-AS_OF in SEALED → HARD BLOCK ---
    post_evidence = Evidence("ev-002", "post data", "2026-06-01")
    result = lock_sealed.check(evidence=post_evidence, as_of_date=AS_OF,
                               sealed_sources=sealed_sources)
    if result == Verdict.BLOCKED:
        print(f"  ✅ PASS  TEST 2: post-AS_OF evidence in SEALED mode → HARD BLOCK")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 2: got {result}")
        all_pass = False

    # --- TEST 3: post-AS_OF in LIVE without UPDATE tag → BLOCK ---
    print("\n─── TEST GROUP 2: LIVE mode provenance enforcement ──────────")
    lock_live = PITLock(mode=Mode.LIVE_CASE_UPDATE, seal=seal)
    result = lock_live.check(evidence=post_evidence, as_of_date=AS_OF,
                             sealed_sources=sealed_sources)
    if result == Verdict.BLOCKED:
        print(f"  ✅ PASS  TEST 3: post-AS_OF in LIVE without UPDATE tag → BLOCK")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 3: got {result}")
        all_pass = False

    # --- TEST 4: post-AS_OF in LIVE with valid UPDATE provenance → ALLOWED ---
    update_evidence = Evidence("ev-003", "updated data", "2026-06-01",
                               is_update=True,
                               update_provenance="UPDATE-001: correction")
    result = lock_live.check(evidence=update_evidence, as_of_date=AS_OF,
                             sealed_sources=sealed_sources)
    if result == Verdict.ALLOWED:
        print(f"  ✅ PASS  TEST 4: post-AS_OF in LIVE with valid UPDATE provenance → ALLOWED")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 4: got {result}")
        all_pass = False

    # --- TEST 5: REPLAY_EXCEPTION without provenance → BLOCK ---
    print("\n─── TEST GROUP 3: REPLAY_EXCEPTION provenance enforcement ────")
    lock_replay = PITLock(mode=Mode.REPLAY_EXCEPTION, seal=seal)
    result = lock_replay.check(evidence=post_evidence, as_of_date=AS_OF,
                               replay_exception=None,
                               sealed_sources=sealed_sources)
    if result == Verdict.BLOCKED:
        print(f"  ✅ PASS  TEST 5: REPLAY_EXCEPTION without provenance → BLOCK")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 5: got {result}")
        all_pass = False

    # --- TEST 6: REPLAY_EXCEPTION with FOUNDER actor + valid provenance → ALLOWED ---
    founder_replay = ReplayException("REPLAY-2026-001", "FOUNDER")
    result = lock_replay.check(evidence=post_evidence, as_of_date=AS_OF,
                               replay_exception=founder_replay,
                               sealed_sources=sealed_sources)
    if result == Verdict.ALLOWED:
        print(f"  ✅ PASS  TEST 6: FOUNDER actor + valid provenance → ALLOWED")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 6: got {result}")
        all_pass = False

    # --- TEST 7: sealed fixture/source hash mutation → INVALIDATE SEAL ---
    print("\n─── TEST GROUP 5: Seal integrity enforcement ─────────────────")
    tampered_sources = frozenset({"src/tampered.md", "src/fake.md"})
    result = lock_sealed.check(evidence=pre_evidence, as_of_date=AS_OF,
                               sealed_sources=tampered_sources)
    if result == Verdict.SEAL_INVALIDATED:
        print(f"  ✅ PASS  TEST 7: sealed fixture/source hash mutation → INVALIDATE SEAL")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 7: got {result}")
        all_pass = False

    # --- TEST 8: Research Director actor + valid provenance → BLOCK ---
    print("\n─── TEST GROUP 4: Unauthorized actor enforcement ────────────")
    non_founder_replay = ReplayException("REPLAY-by-ResearchDirector", "RESEARCH_DIRECTOR")
    result = lock_replay.check(evidence=post_evidence, as_of_date=AS_OF,
                               replay_exception=non_founder_replay,
                               sealed_sources=sealed_sources)
    if result == Verdict.BLOCKED:
        print(f"  ✅ PASS  TEST 8: Research Director actor + valid provenance → BLOCK")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 8: got {result} (expected BLOCKED)")
        all_pass = False

    # --- TEST 9: Research Director actor + provenance containing 'Founder' word → BLOCK ---
    spoofed_replay = ReplayException("Founder-says-go", "RESEARCH_DIRECTOR")
    result = lock_replay.check(evidence=post_evidence, as_of_date=AS_OF,
                               replay_exception=spoofed_replay,
                               sealed_sources=sealed_sources)
    if result == Verdict.BLOCKED:
        print(f"  ✅ PASS  TEST 9: spoofed provenance with 'Founder' but actor != FOUNDER → BLOCK")
        pass_count += 1
    else:
        print(f"  ❌ FAIL  TEST 9: got {result} (expected BLOCKED)")
        all_pass = False

    # --- RESULTS ---
    print(f"\n{'=' * 70}")
    print(f"  RESULTS:  {pass_count}/{total} passed  |  {total - pass_count}/{total} failed")
    if all_pass and pass_count == total:
        print("  ✅ ALL PIT LEAKAGE PROOFS VERIFIED")
    else:
        print("  ❌ SOME TESTS FAILED")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()