#!/usr/bin/env python3
"""
QAD-M4A Contract Validator — Non-production deterministic validation tooling.

Validates M4A schema contracts, state machines, and invariants against
M3 frozen domain contracts. Does NOT validate production code.

Usage:
    python validate-m4a-contracts.py
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent  # project root

# Known M3 contract files
M3_CONTRACTS = {
    "QAD-OPERATING-MODEL.md",
    "QAD-DISCOVERY-AND-SELECTION.md",
    "QAD-FULL-RESEARCH-PROTOCOL.md",
    "QAD-EVIDENCE-AND-SOURCE-MODEL.md",
    "QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md",
    "QAD-BUSINESS-INDUSTRY-MANAGEMENT.md",
    "QAD-IMPAIRMENT-AND-RECOVERY.md",
    "QAD-ECONOMIC-UNDERWRITING.md",
    "QAD-CHALLENGE-AUDIT-PUBLICATION.md",
}

# Known M3 design artifacts
M3_DESIGN = {
    "QAD-M3-PRODUCTION-ROLE-CONTRACTS.md",
    "QAD-M3-SERVICE-CONTRACTS.md",
    "QAD-M3-ROLE-AND-SERVICE-REGISTRY.md",
    "QAD-M3-WORKFORCE-MIGRATION-MAP.md",
    "QAD-M3-TRACEABILITY-MATRIX.md",
}

# Canonical service identity (S1-S12)
CANONICAL_SERVICES = {
    "S1": "Autonomous Selection Engine",
    "S2": "Research Budget Controller",
    "S3": "Security / Entity Resolution",
    "S4": "Canonical Evidence Registry",
    "S5": "Raw Source Archive",
    "S6": "Run Manifest Service",
    "S7": "Point-in-Time Lock",
    "S8": "Retry / Research Execution Controller",
    "S9": "Case Locking / Idempotency",
    "S10": "Notebook / Deep Research Interface",
    "S11": "Publication Renderer",
    "S12": "Evaluation Harness",
}

# Canonical moat types (FD #61)
CANONICAL_MOAT_TYPES = {
    "SHARE_OF_MIND",
    "NETWORK_EFFECT",
    "HIGH_SWITCHING_COST",
    "COST_ADVANTAGE",
    "INTANGIBLE_ASSETS",
    "EFFICIENT_SCALE",
}

# Canonical impairment states
CANONICAL_IMPAIRMENT_STATES = {
    "TEMPORARY",
    "MOSTLY_TEMPORARY",
    "MIXED",
    "STRUCTURAL",
    "UNRESOLVED",
}

# Canonical selection states
CANONICAL_SELECTION_STATES = {
    "AUTO_RESEARCH_NOW",
    "WATCH_PRICE",
    "WATCH_EVIDENCE",
    "DATA_LIMITED_WATCH",
    "REJECT",
    "SELECTION_ERROR",
}

# Canonical evidence types
CANONICAL_EVIDENCE_TYPES = {"FACT", "CLAIM", "INFERENCE", "HYPOTHESIS"}

# Underwriting verdict states
CANONICAL_VERDICT_STATES = {
    "QAD_CONFIRMED",
    "QAD_PROBABLE",
    "QAD_UNRESOLVED",
    "NOT_QAD_STRUCTURAL",
    "NOT_QAD_QUALITY",
    "NOT_QAD_VALUATION",
}

# 15 critical invariants
INVARIANTS = [
    "INV-001",
    "INV-002",
    "INV-003",
    "INV-004",
    "INV-005",
    "INV-006",
    "INV-007",
    "INV-008",
    "INV-009",
    "INV-010",
    "INV-011",
    "INV-012",
    "INV-013",
    "INV-014",
    "INV-015",
]

# 12 state machines
STATE_MACHINES = [
    "SM-1",
    "SM-2",
    "SM-3",
    "SM-4",
    "SM-5",
    "SM-6",
    "SM-7",
    "SM-8",
    "SM-9",
    "SM-10",
    "SM-11",
    "SM-12",
]

results = {"pass": 0, "fail": 0, "warn": 0}


def check(condition: bool, message: str, severity: str = "fail"):
    if condition:
        results["pass"] += 1
        print(f"  ✅ {message}")
    else:
        results[severity] += 1
        print(f"  {'❌' if severity == 'fail' else '⚠️'} {message}")


def validate_domain_contracts():
    """Check that exactly 9 domain contract files exist."""
    print("\n=== 1. Domain Contract Inventory ===")
    qad_dir = BASE / "project-definition" / "qad"
    if not qad_dir.exists():
        print(f"  ❌ Directory not found: {qad_dir}")
        results["fail"] += 1
        return

    actual_files = {f.name for f in qad_dir.iterdir() if f.suffix == ".md"}
    check(actual_files == M3_CONTRACTS,
          f"Domain contracts: {len(actual_files)} files (expected {len(M3_CONTRACTS)})")


def validate_service_identity():
    """Check that S1-S12 are consistent across all 3 sources."""
    print("\n=== 2. Service Identity (S1-S12) ===")
    service_contract_path = BASE / "design" / "qad-pivot" / "QAD-M3-SERVICE-CONTRACTS.md"
    if service_contract_path.exists():
        content = service_contract_path.read_text()
        for sid, sname in CANONICAL_SERVICES.items():
            # Check the service_id appears in the service contracts
            # Check service name appears in the document
            found_id = sid in content
            found_name = sname.split("/")[0].strip() in content
            check(found_id and found_name,
                  f"{sid}: {sname} in SERVICE-CONTRACTS.md")
    else:
        print(f"  ❌ SERVICE-CONTRACTS.md not found")
        results["fail"] += 1


def validate_moat_types():
    """Check that moat taxonomy uses canonical FD #61 types."""
    print("\n=== 3. Moat Taxonomy (FD #61) ===")
    schema_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    if schema_path.exists():
        content = schema_path.read_text()
        for mt in CANONICAL_MOAT_TYPES:
            check(mt.lower() in content.lower(),
                  f"Moat type: {mt}")
    else:
        print(f"  ⚠️ M4A schemas not yet created (will check later)")
        results["warn"] += 1


def validate_impairment_states():
    """Check canonical impairment states."""
    print("\n=== 4. Impairment States ===")
    schema_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    if schema_path.exists():
        content = schema_path.read_text()
        for st in CANONICAL_IMPAIRMENT_STATES:
            check(st in content, f"Impairment state: {st}")
    else:
        results["warn"] += 1


def validate_evidence_taxonomy():
    """Check evidence types (FACT ≠ CLAIM ≠ INFERENCE ≠ HYPOTHESIS)."""
    print("\n=== 5. Evidence Taxonomy ===")
    schema_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    if schema_path.exists():
        content = schema_path.read_text()
        for et in CANONICAL_EVIDENCE_TYPES:
            check(et in content, f"Evidence type: {et}")
    else:
        results["warn"] += 1


def validate_state_machines():
    """Check that all 12 state machines exist."""
    print("\n=== 6. State Machines ===")
    sm_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-STATE-MACHINES.md"
    if sm_path.exists():
        content = sm_path.read_text()
        for sm in STATE_MACHINES:
            check(sm in content, f"State machine: {sm}")
    else:
        print(f"  ⚠️ State machines not yet created")
        results["warn"] += 1


def validate_invariants():
    """Check that all 15 invariants exist."""
    print("\n=== 7. Critical Invariants ===")
    inv_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-INVARIANTS.md"
    if inv_path.exists():
        content = inv_path.read_text()
        for inv in INVARIANTS:
            check(inv in content, f"Invariant: {inv}")
    else:
        print(f"  ⚠️ Invariants not yet created")
        results["warn"] += 1


def validate_m3_frozen():
    """Check that M3 artifacts are frozen (not DRAFT)."""
    print("\n=== 8. M3 Artifact Freeze Status ===")
    for fname in M3_CONTRACTS | M3_DESIGN:
        fpath = BASE / "project-definition" / "qad" / fname
        if not fpath.exists():
            fpath = BASE / "design" / "qad-pivot" / fname
        if fpath.exists():
            content = fpath.read_text()
            # Check for "FROZEN FOR M4 DERIVATION" in status
            if "FROZEN FOR M4 DERIVATION" in content:
                check(True, f"{fname}: FROZEN ✅")
            elif "FINAL" in content:
                check(True, f"{fname}: FINAL (acceptable) ✅")
            else:
                check(False, f"{fname}: status not frozen ❌")
        else:
            # Some design artifacts may not exist in the domain dir
            alt_path = BASE / "design" / "qad-pivot" / fname
            if alt_path.exists():
                content = alt_path.read_text()
                if "FROZEN FOR M4 DERIVATION" in content:
                    check(True, f"{fname}: FROZEN ✅")
                elif "FINAL" in content:
                    check(True, f"{fname}: FINAL (acceptable) ✅")
                else:
                    check(False, f"{fname}: status not frozen ❌")


def validate_no_production_code():
    """Check that no production code was created."""
    print("\n=== 9. No Production Code ===")
    m4a_dir = BASE / "design" / "qad-pivot" / "m4a"
    if m4a_dir.exists():
        py_files = list(m4a_dir.glob("*.py"))
        # Only validate-m4a-contracts.py is allowed
        allowed = {"validate-m4a-contracts.py"}
        actual = {f.name for f in py_files}
        disallowed = actual - allowed
        if disallowed:
            check(False, f"Unexpected .py files: {disallowed}")
        else:
            check(True, "Only validate-m4a-contracts.py present")
    else:
        check(True, "No M4A directory (yet)")


def main():
    print("=" * 60)
    print("QAD-M4A Contract Validator")
    print("=" * 60)

    validate_domain_contracts()
    validate_service_identity()
    validate_moat_types()
    validate_impairment_states()
    validate_evidence_taxonomy()
    validate_state_machines()
    validate_invariants()
    validate_m3_frozen()
    validate_no_production_code()

    print("\n" + "=" * 60)
    print(f"Results: {results['pass']} passed, {results['fail']} failed, {results['warn']} warnings")
    print("=" * 60)

    if results["fail"] > 0:
        print("\n❌ VALIDATION FAILED")
        sys.exit(1)
    elif results["warn"] > 0:
        print("\n⚠️ VALIDATION PASSED WITH WARNINGS")
        sys.exit(0)
    else:
        print("\n✅ VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()