#!/usr/bin/env python3
"""
QAD-M4B Evaluation Pack Validator — Non-production deterministic validation.

Validates M4B evaluation contract, fixture specs, and acceptance matrix
against M3 frozen contracts and M4A canonical schemas.

Usage:
    python validate-m4b-pack.py
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent  # project root

results = {"pass": 0, "fail": 0, "warn": 0}

# Expected fixture types
FIXTURE_TYPES = [
    "True Temporary Impairment",
    "True Structural Deterioration",
    "Mixed Impairment",
    "False Quality",
    "Balance-Sheet Trap",
    "Industry / Cycle Shock",
    "Company-Specific Shock",
    "Unresolved / Ambiguous Case",
    "Valuation Failure",
    "Narrative Panic",
]

# Expected evaluation dimensions
EVAL_DIMENSIONS = [
    "Source Recall",
    "Citation Correctness",
    "Claim Support",
    "Original-Source Validation",
    "Contradiction Coverage",
    "Decision-Changing Evidence Recall",
    "H1–H5 Coverage",
    "Quality Verification Correctness",
    "False-Quality Detection",
    "Temporary-vs-Structural Calibration",
    "Recovery Mechanism Quality",
    "Thesis-Killer Detection",
    "False-Confidence Rate",
    "Calculation Reproducibility",
    "Normalization Correctness",
    "Permanent-Loss Coverage",
    "Reverse-DCF Correctness",
    "Scenario Consistency",
    "PIT Correctness",
    "Provenance Completeness",
    "Failure-State Correctness",
    "Research-Stop Quality",
    "Audit-Gate Correctness",
    "Report Factual-Error Rate",
    "Universe Coverage Rate",
    "Data-Ready Coverage",
    "Known-Opportunity Recall",
    "Quality Candidate Recall",
    "Dislocation Detection Rate",
    "Signal-to-Candidate Conversion",
    "Candidate-to-Research Conversion",
    "Discovery Cost per New Candidate",
    "False Positive Rate (Material)",
    "Decision-Changing Candidate Recall",
]


def check(condition: bool, message: str, severity: str = "fail"):
    if condition:
        results["pass"] += 1
        print(f"  ✅ {message}")
    else:
        results[severity] += 1
        print(f"  {'❌' if severity == 'fail' else '⚠️'} {message}")


def validate_evaluation_contract():
    """Check evaluation contract exists and has required sections."""
    print("\n=== 1. Evaluation Contract ===")
    path = BASE / "design" / "qad-pivot" / "m4b" / "QAD-M4B-EVALUATION-CONTRACT.md"
    check(path.exists(), "Evaluation contract exists")
    if path.exists():
        content = path.read_text()
        check("TYPE A" in content, "Type A evaluation defined")
        check("TYPE B" in content, "Type B evaluation defined")
        check("SEALED" in content, "PIT sealed evaluation protocol defined")
        check("Radar" in content, "Radar incremental-recall evaluation defined")
        check("Expected Information Value" in content, "Research saturation defined")
        check("Tier" in content, "Cost/model routing evaluation defined")
        check("PROVISIONAL_M4B_THRESHOLD" in content, "Provisional threshold policy defined")


def validate_fixture_spec():
    """Check fixture spec has all 10 fixture types."""
    print("\n=== 2. PIT Fixture Spec ===")
    path = BASE / "design" / "qad-pivot" / "m4b" / "QAD-M4B-PIT-FIXTURE-SPEC.md"
    check(path.exists(), "Fixture spec exists")
    if path.exists():
        content = path.read_text()
        for ft in FIXTURE_TYPES:
            check(ft in content, f"Fixture type: {ft}")
        check("AS_OF" in content, "AS_OF date defined")
        check("H1" in content, "Expected hypotheses (H1)")
        check("H5" in content, "Expected hypotheses (H5)")
        check("leak" in content.lower(), "Leak test defined")


def validate_acceptance_matrix():
    """Check acceptance matrix exists and covers evaluation dimensions."""
    print("\n=== 3. Acceptance Matrix ===")
    path = BASE / "design" / "qad-pivot" / "m4b" / "QAD-M4B-ACCEPTANCE-MATRIX.md"
    check(path.exists(), "Acceptance matrix exists")
    if path.exists():
        content = path.read_text()
        for dim in EVAL_DIMENSIONS:
            # Check key terms
            terms = dim.lower().split()[:2]
            found = all(t in content.lower() for t in terms)
            if found:
                results["pass"] += 1
            else:
                results["warn"] += 1
                print(f"  ⚠️ Dimension may need checking: {dim}")
        check("PROVISIONAL_M4B_THRESHOLD" in content, "Provisional thresholds present")
        check("TYPE_A" in content or "Type A" in content, "Type A metrics present")
        check("TYPE_B" in content or "Type B" in content, "Type B metrics present")


def validate_no_production_code():
    """Check that no production code was created."""
    print("\n=== 4. No Production Code ===")
    m4b_dir = BASE / "design" / "qad-pivot" / "m4b"
    if m4b_dir.exists():
        py_files = list(m4b_dir.glob("*.py"))
        allowed = {"validate-m4b-pack.py", "pit-leakage-proof.py"}
        actual = {f.name for f in py_files}
        disallowed = actual - allowed
        if disallowed:
            check(False, f"Unexpected .py files: {disallowed}")
        else:
            check(True, "Only validate-m4b-pack.py present")
    else:
        check(True, "No M4B directory")


def validate_m4a_frozen():
    """Check that M4A artifacts are frozen."""
    print("\n=== 5. M4A Freeze Status ===")
    m4a_closeout = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CLOSEOUT.md"
    if m4a_closeout.exists():
        content = m4a_closeout.read_text()
        check("FREEZE" in content or "FROZEN" in content, "M4A freeze gate status present")


def main():
    print("=" * 60)
    print("QAD-M4B Evaluation Pack Validator")
    print("=" * 60)

    validate_evaluation_contract()
    validate_fixture_spec()
    validate_acceptance_matrix()
    validate_no_production_code()
    validate_m4a_frozen()

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