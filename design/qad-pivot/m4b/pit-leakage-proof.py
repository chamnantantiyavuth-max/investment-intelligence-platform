#!/usr/bin/env python3
"""
QAD-M4B PIT Leakage Proof — Non-production deterministic test suite.

Proves the Point-in-Time sealed evaluation protocol (M3-SERVICES S7)
correctly enforces AS_OF temporal boundaries, provenance rules,
replay-exception governance, and seal integrity.

7 tests using ONLY synthetic non-production data.  No production database.

Usage:
    python pit-leakage-proof.py
    python pit-leakage-proof.py -v   (verbose per-test detail)
"""

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum, auto
from typing import Optional

# ---------------------------------------------------------------------------
# Synthetic PIT domain model (non-production)
# ---------------------------------------------------------------------------


class Mode(Enum):
    SEALED = auto()
    LIVE = auto()


class Verdict(Enum):
    ALLOWED = "ALLOWED"
    BLOCK = "BLOCK"
    INVALIDATE_SEAL = "INVALIDATE SEAL"


@dataclass(frozen=True)
class Evidence:
    """A synthetic evidence item with an explicit timestamp and optional provenance."""
    id: str
    content: str
    recorded_date: date      # when this evidence was created/published


@dataclass(frozen=True)
class FixtureSeal:
    """Hash-locked seal bound to an AS_OF_DATE."""
    fixture_id: str
    as_of_date: date
    # Deterministic hash of the sealed evidence set + fixture metadata
    _sealed_hash: Optional[str] = None

    @staticmethod
    def _compute_hash(fixture_id: str, as_of_date: date,
                      evidence_sources: tuple) -> str:
        raw = f"{fixture_id}|{as_of_date.isoformat()}|{json.dumps(sorted(evidence_sources), sort_keys=True)}"
        return hashlib.sha256(raw.encode()).hexdigest()

    @classmethod
    def create(cls, fixture_id: str, as_of_date: date,
               evidence_sources: tuple[str, ...]):
        h = cls._compute_hash(fixture_id, as_of_date, evidence_sources)
        return cls(fixture_id=fixture_id, as_of_date=as_of_date,
                   _sealed_hash=h)

    def verify_integrity(self, evidence_sources: tuple[str, ...]) -> bool:
        """Returns True if the seal hash still matches the source set."""
        if self._sealed_hash is None:
            return False
        expected = self._compute_hash(self.fixture_id, self.as_of_date,
                                      evidence_sources)
        return self._sealed_hash == expected


@dataclass
class Provenance:
    """Provenance metadata carried with an UPDATE operation."""
    update_type: str         # e.g. "factual_correction", "new_disclosure"
    source: str              # verifiable source identifier
    timestamp: date
    justification: str       # why this update was necessary


class PITLock:
    """
    Simulates the M3-SERVICES S7 PIT lock mechanism.

    In SEALED mode:
      - Pre-AS_OF evidence → ALLOWED
      - Post-AS_OF evidence → HARD BLOCK (no exceptions)

    In LIVE mode:
      - Pre-AS_OF evidence → ALLOWED
      - Post-AS_OF evidence WITHOUT UPDATE provenance → BLOCK
      - Post-AS_OF evidence WITH valid UPDATE provenance → ALLOWED

    REPLAY_EXCEPTION handling:
      - Without explicit provenance → BLOCK
      - With explicit provenance → ALLOWED

    Seal integrity:
      - Mutated fixture/source hash → INVALIDATE SEAL
    """

    def __init__(self, mode: Mode, seal: Optional[FixtureSeal] = None):
        self.mode = mode
        self.seal = seal

    def check(self, evidence: Evidence,
              as_of_date: date,
              provenance: Optional[Provenance] = None,
              is_replay_exception: bool = False,
              sealed_sources: Optional[tuple[str, ...]] = None) -> Verdict:
        """
        Evaluate whether `evidence` passes the PIT lock.

        Parameters
        ----------
        evidence : Evidence
            The synthetic evidence item under test.
        as_of_date : date
            The fixture's hard cutoff date.
        provenance : Provenance or None
            If set, carries UPDATE provenance metadata.
        is_replay_exception : bool
            If True, this query is tagged as a REPLAY_EXCEPTION.
        sealed_sources : tuple[str, ...] or None
            The original sealed source identifiers (for integrity check).
        """
        # --- Seal integrity check -------------------------------------------
        if self.seal is not None and sealed_sources is not None:
            if not self.seal.verify_integrity(sealed_sources):
                return Verdict.INVALIDATE_SEAL

        is_post_as_of = evidence.recorded_date > as_of_date

        # --- REPLAY_EXCEPTION path ------------------------------------------
        if is_replay_exception:
            if provenance is None or not provenance.source:
                return Verdict.BLOCK
            return Verdict.ALLOWED

        # --- SEALED mode ----------------------------------------------------
        if self.mode == Mode.SEALED:
            if is_post_as_of:
                return Verdict.BLOCK    # HARD BLOCK — no exceptions in SEALED
            return Verdict.ALLOWED

        # --- LIVE mode ------------------------------------------------------
        if self.mode == Mode.LIVE:
            if is_post_as_of:
                if provenance is not None and provenance.source:
                    return Verdict.ALLOWED
                return Verdict.BLOCK
            return Verdict.ALLOWED

        return Verdict.BLOCK  # safety fallback

# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------


class PITLeakageProof:
    """Runs the 7 deterministic PIT leakage tests."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0

    def _assert(self, condition: bool, test_num: int, label: str,
                detail: str = ""):
        if condition:
            self.passed += 1
            status = "✅ PASS"
        else:
            self.failed += 1
            status = "❌ FAIL"
        msg = f"  {status}  TEST {test_num}: {label}"
        if self.verbose and detail:
            msg += f"\n           {detail}"
        print(msg)

    def run_all(self):
        print("=" * 62)
        print("  QAD-M4B PIT LEAKAGE PROOF — Non-Production Deterministic")
        print("=" * 62)
        print()

        # --- Synthetic fixture data -----------------------------------------
        AS_OF = date(2023, 6, 1)

        pre_evidence = Evidence(
            id="EVD-PRE-001",
            content="Pre-AS_OF quarterly earnings report (Q1 2023)",
            recorded_date=date(2023, 5, 15),
        )
        post_evidence = Evidence(
            id="EVD-POST-002",
            content="Post-AS_OF unexpected earnings beat (Q2 2023)",
            recorded_date=date(2023, 8, 10),
        )
        # A second post-AS_OF item for the update-provenance test
        post_evidence_update = Evidence(
            id="EVD-POST-003",
            content="Post-AS_OF regulatory filing correction",
            recorded_date=date(2023, 9, 1),
        )

        sealed_sources = (
            "src/sbux/fy2022-10k.md",
            "src/sbux/fy2023-q1.md",
            "src/sbux/industry-coffee-consumption.md",
        )
        seal = FixtureSeal.create(
            fixture_id="FIX-2026-001",
            as_of_date=AS_OF,
            evidence_sources=sealed_sources,
        )

        # --- TEST 1 ----------------------------------------------------------
        print("─── TEST GROUP 1: SEALED mode boundary enforcement ──────────")
        lock_sealed = PITLock(mode=Mode.SEALED, seal=seal)
        result = lock_sealed.check(
            evidence=pre_evidence, as_of_date=AS_OF,
            sealed_sources=sealed_sources)
        self._assert(
            result == Verdict.ALLOWED, 1,
            "pre-AS_OF evidence in SEALED mode → ALLOWED",
            f"result={result.value}  as_of={AS_OF}  recorded={pre_evidence.recorded_date}")

        # --- TEST 2 ----------------------------------------------------------
        result = lock_sealed.check(
            evidence=post_evidence, as_of_date=AS_OF,
            sealed_sources=sealed_sources)
        self._assert(
            result == Verdict.BLOCK, 2,
            "post-AS_OF evidence in SEALED mode → HARD BLOCK",
            f"result={result.value}  as_of={AS_OF}  recorded={post_evidence.recorded_date}")

        # --- TEST 3 ----------------------------------------------------------
        print("\n─── TEST GROUP 2: LIVE mode provenance enforcement ──────────")
        lock_live = PITLock(mode=Mode.LIVE)
        result = lock_live.check(
            evidence=post_evidence, as_of_date=AS_OF,
            provenance=None)
        self._assert(
            result == Verdict.BLOCK, 3,
            "post-AS_OF evidence in LIVE mode without UPDATE tag → BLOCK",
            f"result={result.value}  provenance=None")

        # --- TEST 4 ----------------------------------------------------------
        provenance = Provenance(
            update_type="factual_correction",
            source="sec/edgar/2023-08-15/8k-exhibit99.1",
            timestamp=date(2023, 9, 1),
            justification="Corrected revenue recognition disclosure received post-AS_OF"
        )
        result = lock_live.check(
            evidence=post_evidence_update, as_of_date=AS_OF,
            provenance=provenance)
        self._assert(
            result == Verdict.ALLOWED, 4,
            "post-AS_OF evidence in LIVE mode with valid UPDATE provenance → ALLOWED",
            f"result={result.value}  provenance.source={provenance.source}")

        # --- TEST 5 ----------------------------------------------------------
        print("\n─── TEST GROUP 3: REPLAY_EXCEPTION provenance enforcement ────")
        result = lock_sealed.check(
            evidence=post_evidence, as_of_date=AS_OF,
            is_replay_exception=True, provenance=None,
            sealed_sources=sealed_sources)
        self._assert(
            result == Verdict.BLOCK, 5,
            "REPLAY_EXCEPTION without exception provenance → BLOCK",
            f"result={result.value}  is_replay_exception=True  provenance=None")

        # --- TEST 6 ----------------------------------------------------------
        replay_prov = Provenance(
            update_type="replay_exception",
            source="operator/FD-142/override-2023-08-12",
            timestamp=date(2023, 8, 12),
            justification="Founder-authorized replay for calibration validation"
        )
        result = lock_sealed.check(
            evidence=post_evidence, as_of_date=AS_OF,
            is_replay_exception=True, provenance=replay_prov,
            sealed_sources=sealed_sources)
        self._assert(
            result == Verdict.ALLOWED, 6,
            "REPLAY_EXCEPTION with explicit provenance → ALLOWED",
            f"result={result.value}  provenance.source={replay_prov.source}")

        # --- TEST 7 ----------------------------------------------------------
        print("\n─── TEST GROUP 4: Seal integrity enforcement ─────────────────")
        tampered_sources = (
            "src/sbux/fy2022-10k.md",
            "src/sbux/fy2023-q1.md",
            "src/sbux/industry-coffee-consumption.md",
            "src/sbux/leaked-q2-2023.md",  # <-- injected post-seal
        )
        result = lock_sealed.check(
            evidence=pre_evidence, as_of_date=AS_OF,
            sealed_sources=tampered_sources)
        self._assert(
            result == Verdict.INVALIDATE_SEAL, 7,
            "sealed fixture/source hash mutation → INVALIDATE SEAL",
            f"result={result.value}  original_sources_count={len(sealed_sources)}  tampered_count={len(tampered_sources)}")

        # --- Summary ---------------------------------------------------------
        print()
        print("=" * 62)
        total = self.passed + self.failed
        print(f"  RESULTS:  {self.passed}/{total} passed  |  "
              f"{self.failed}/{total} failed")
        if self.failed == 0:
            print("  ✅ ALL PIT LEAKAGE PROOFS VERIFIED")
        else:
            print("  ❌ LEAKAGE PROOF FAILURES DETECTED")
        print("=" * 62)
        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="QAD-M4B PIT Leakage Proof — deterministic synthetic tests")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show per-test detail")
    args = parser.parse_args()

    suite = PITLeakageProof(verbose=args.verbose)
    success = suite.run_all()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()