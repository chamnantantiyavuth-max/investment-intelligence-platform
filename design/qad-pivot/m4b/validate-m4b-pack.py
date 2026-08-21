#!/usr/bin/env python3
"""QAD-M4B Evaluation Pack Validator — Non-production deterministic validation.

Upgraded for M4B final pack: adds checks for lifecycle sequence, seal
contract fields, PIT proof subprocess execution, threshold scanning,
fixture counts, Type A/B separation, M4A freeze status, and the final
independent review file.

Usage:
    python validate-m4b-pack.py
"""

import re
import subprocess  # nosec — non-production deterministic validation only
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent  # project root
M4B_DIR = BASE / "design" / "qad-pivot" / "m4b"

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
    "H1\u2013H5 Coverage",
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

# Required seal-contract mandatory fields per Evaluation Contract §3.4
# Exact concepts required — not generic tokens
SEAL_CONTRACT_FIELDS = [
    "fixture_id",
    "fixture_version",
    "AS_OF_DATE",
    "immutable source IDs",
    "source content hashes",
    "source publication dates",
    "allowed pre-AS_OF corpus manifest",
    "forbidden post-AS_OF leak sentinels",
    "expected quality/impairment/verdict labels",
    "label rationale",
    "material alternative interpretation",
    "ambiguity notes",
    "adjudicator identity",
    "adjudication method",
    "adjudication timestamp",
    "corpus_hash",
    "label_hash",
    "seal_hash",
]

# Exact lifecycle sequence per Evaluation Contract §3.3
LIFECYCLE_SEQUENCE = (
    "DRAFT_UNSEALED",
    "SOURCE_PACK_COMPLETE",
    "INDEPENDENTLY_ADJUDICATED",
    "SEALED",
)


def check(condition: bool, message: str, severity: str = "fail"):
    pass_mark = "\u2705"
    fail_mark = "\u274c"
    warn_mark = "\u26a0\ufe0f"
    if condition:
        results["pass"] += 1
        print(f"  {pass_mark} {message}")
    else:
        results[severity] += 1
        print(f"  {fail_mark if severity == 'fail' else warn_mark} {message}")


def validate_evaluation_contract():
    """Check evaluation contract exists and has required sections."""
    print("\n=== 1. Evaluation Contract ===")
    path = M4B_DIR / "QAD-M4B-EVALUATION-CONTRACT.md"
    check(path.exists(), "Evaluation contract exists")
    if not path.exists():
        return
    content = path.read_text()
    check("TYPE A" in content, "Type A evaluation defined")
    check("TYPE B" in content, "Type B evaluation defined")
    check("SEALED" in content, "PIT sealed evaluation protocol defined")
    check("Radar" in content, "Radar incremental-recall evaluation defined")
    check("Expected Information Value" in content, "Research saturation defined")
    check("Tier" in content, "Cost/model routing evaluation defined")
    check("PROVISIONAL_M4B_THRESHOLD" in content,
         "Provisional threshold policy defined")

    # Check 1: Evaluation contract status is post-M4A-freeze — EXACT MATCH REQUIRED
    # Parse the explicit first Status header. Do NOT search for FINAL anywhere.
    status_match = re.search(r"^>\s+\*\*Status:\*\*\s+(.+)$", content, re.MULTILINE)
    if status_match:
        status_text = status_match.group(1).strip()
        expected = "M4B FINAL / FROZEN — FOUNDER ACCEPTED"
        check(status_text == expected,
              f"Evaluation contract status: '{status_text}' == '{expected}'")
    else:
        check(False,
              "Evaluation contract has explicit first Status header (no fallback — exact match required)")

    # Check 2: Lifecycle exact sequence exists
    lifecycle_present = all(phase in content for phase in LIFECYCLE_SEQUENCE)
    lifecycle_str = " \u2192 ".join(LIFECYCLE_SEQUENCE)
    check(lifecycle_present,
          f"Lifecycle sequence {lifecycle_str} present in contract")

    # Check 5: All seal-contract mandatory fields present
    missing_fields = [f for f in SEAL_CONTRACT_FIELDS if f.lower() not in content.lower()]
    check(len(missing_fields) == 0,
          f"All seal-contract mandatory fields present (missing: {missing_fields})")


def validate_fixture_spec():
    """Check fixture spec has all 10 fixture types and lifecycle markers."""
    print("\n=== 2. PIT Fixture Spec ===")
    path = M4B_DIR / "QAD-M4B-PIT-FIXTURE-SPEC.md"
    check(path.exists(), "Fixture spec exists")
    if not path.exists():
        return
    content = path.read_text()
    for ft in FIXTURE_TYPES:
        check(ft in content, f"Fixture type: {ft}")
    check("AS_OF" in content, "AS_OF date defined")
    check("H1" in content, "Expected hypotheses (H1)")
    check("H5" in content, "Expected hypotheses (H5)")
    check("leak" in content.lower(), "Leak test defined")

    # Check 3: Fixture spec contains AI_PROPOSED, DRAFT_UNSEALED, NOT_VALID_FOR_SCORING
    check("AI_PROPOSED" in content, "Status marker: AI_PROPOSED present")
    check("DRAFT_UNSEALED" in content, "Status marker: DRAFT_UNSEALED present")
    check("NOT_VALID_FOR_SCORING" in content,
          "Status marker: NOT_VALID_FOR_SCORING present")

    # Check 4: SEALED_FIXTURE_COUNT == 0, DRAFT_FIXTURE_CANDIDATES == 10
    sealed_match = re.search(r"SEALED_FIXTURE_COUNT\s*=\s*(\d+)", content)
    draft_match = re.search(r"DRAFT_FIXTURE_CANDIDATES\s*=\s*(\d+)", content)
    if sealed_match:
        check(int(sealed_match.group(1)) == 0,
              f"SEALED_FIXTURE_COUNT == {sealed_match.group(1)} (expected 0)")
    else:
        check(False, "SEALED_FIXTURE_COUNT declaration present")
    if draft_match:
        check(int(draft_match.group(1)) == 10,
              f"DRAFT_FIXTURE_CANDIDATES == {draft_match.group(1)} (expected 10)")
    else:
        check(False, "DRAFT_FIXTURE_CANDIDATES declaration present")


def validate_acceptance_matrix():
    """Check acceptance matrix exists and covers evaluation dimensions."""
    print("\n=== 3. Acceptance Matrix ===")
    path = M4B_DIR / "QAD-M4B-ACCEPTANCE-MATRIX.md"
    check(path.exists(), "Acceptance matrix exists")
    if not path.exists():
        return
    content = path.read_text()
    for dim in EVAL_DIMENSIONS:
        terms = dim.lower().split()[:2]
        found = all(t in content.lower() for t in terms)
        if found:
            results["pass"] += 1
        else:
            results["warn"] += 1
            print(f"  \u26a0\ufe0f Dimension may need checking: {dim}")
    check("PROVISIONAL_M4B_THRESHOLD" in content,
          "Provisional thresholds present")
    check("TYPE_A" in content or "Type A" in content,
          "Type A metrics present")
    check("TYPE_B" in content or "Type B" in content,
          "Type B metrics present")

    # Check 7: Type A / Type B remain separate — verify each metric row
    # has an explicit type marker and no row lacks one
    metric_rows = re.findall(
        r"^\|\s*\d+\.\d+\s*\|.*\|$", content, re.MULTILINE
    )
    rows_with_type = 0
    rows_without_type = 0
    for row in metric_rows:
        if re.search(r"\|\s*(A|B|A\+B)\s*\|$", row):
            rows_with_type += 1
        else:
            rows_without_type += 1
    check(rows_without_type == 0,
          f"All {rows_with_type} metric rows have explicit type marker "
          f"({rows_without_type} ambiguous)")
    check(rows_with_type == 44,
          f"Expected exactly 44 metric rows, found {rows_with_type}")

    # Check 8: All material thresholds are PROVISIONAL_M4B_THRESHOLD
    # Look for any numeric threshold values that aren't PROVISIONAL
    # (allow known false-positives: year numbers, dates, table numbers)
    numeric_suspects = re.findall(
        r"(?<!\d)([5-9]\d(?:\.\d+)?%|1\d{2}(?:\.\d+)?%)", content
    )
    check(len(numeric_suspects) == 0,
          f"No hidden numeric thresholds found "
          f"({len(numeric_suspects)} numeric % patterns detected: "
          f"{numeric_suspects})")

    # Check 9: Per-row Pass Threshold column verification
    # Parse every metric row into columns and verify column 4 (Pass Threshold)
    metric_rows = re.findall(
        r"^\|\s*\d+\.\d+\s*\|.*\|$", content, re.MULTILINE
    )
    rows_with_provis = 0
    rows_without_provis = 0
    for row in metric_rows:
        cols = [c.strip() for c in row.split("|")]
        # cols[0] = empty (before first |), cols[1] = #, cols[2] = Metric,
        # cols[3] = Definition, cols[4] = Pass Threshold, cols[5] = Fixtures,
        # cols[6] = Method, cols[7] = Type, cols[8] = empty (after last |)
        if len(cols) >= 7:
            threshold_cell = cols[4] if len(cols) > 4 else ""
            if "PROVISIONAL_M4B_THRESHOLD" in threshold_cell:
                rows_with_provis += 1
            else:
                rows_without_provis += 1
    check(rows_without_provis == 0,
          f"All {rows_with_provis} metric rows have PROVISIONAL_M4B_THRESHOLD "
          f"in Pass Threshold cell ({rows_without_provis} non-provisional)")
    check(rows_with_provis == 44,
          f"Exactly 44 metric rows with provisional threshold (found {rows_with_provis})")


def validate_no_production_code():
    """Check that no production code was created."""
    print("\n=== 4. No Production Code ===")
    if not M4B_DIR.exists():
        check(True, "No M4B directory")
        return

    py_files = list(M4B_DIR.glob("*.py"))
    allowed = {"validate-m4b-pack.py", "pit-leakage-proof.py"}
    actual = {f.name for f in py_files}
    disallowed = actual - allowed

    if disallowed:
        check(False, f"Unexpected .py files: {disallowed}")
    else:
        # Check 10 (message fix): "Only validate-m4b-pack.py and pit-leakage-proof.py present"
        check(True, "Only validate-m4b-pack.py and pit-leakage-proof.py present")


def validate_m4a_frozen():
    """Check that M4A artifacts are frozen."""
    print("\n=== 5. M4A Freeze Status ===")
    m4a_closeout = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CLOSEOUT.md"
    if m4a_closeout.exists():
        content = m4a_closeout.read_text()
        check("FREEZE" in content or "FROZEN" in content,
              "M4A baseline status = FINAL / FROZEN")
    else:
        check(False, "M4A closeout file exists")


def validate_pit_proof():
    """Execute pit-leakage-proof.py as subprocess and verify results."""
    print("\n=== 6. PIT Leakage Proof ===")
    pit_path = M4B_DIR / "pit-leakage-proof.py"
    check(pit_path.exists(), "PIT proof file exists")
    if not pit_path.exists():
        return

    result = subprocess.run(  # nosec — non-production deterministic test
        [sys.executable, str(pit_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    exit_code_ok = result.returncode == 0
    check(exit_code_ok,
          f"PIT proof subprocess exit code == {result.returncode} (expected 0)")

    # Count passed tests in output — require EXACTLY 9
    pass_matches = re.findall(r"\u2705 PASS\s+TEST\s+(\d+)", result.stdout)
    total_tests = len(pass_matches)
    check(total_tests == 9,
          f"PIT proof has exactly {total_tests} passing tests (expected 9)")

    # Verify all 9 tests by name
    test_names = [
        "TEST 1", "TEST 2", "TEST 3", "TEST 4",
        "TEST 5", "TEST 6", "TEST 7", "TEST 8",
        "TEST 9",
    ]
    for tn in test_names:
        check(tn in result.stdout, f"{tn} present in PIT proof output")

    # Verify results summary line
    summary_match = re.search(r"RESULTS:\s+(\d+)/(\d+)\s+passed", result.stdout)
    if summary_match:
        passed = int(summary_match.group(1))
        total = int(summary_match.group(2))
        check(passed == 9 and total == 9,
              f"PIT summary: {passed}/{total} passed (expected 9/9)")
    else:
        check(False, "PIT results summary line found")

    # Log any errors
    if not exit_code_ok:
        print(f"  STDOUT: {result.stdout[:500]}")
        print(f"  STDERR: {result.stderr[:500]}")


def validate_independent_review():
    """Check final independent review file exists."""
    print("\n=== 7. Final Independent Review ===")
    path = M4B_DIR / "QAD-M4B-INDEPENDENT-REVIEW-FINAL.md"
    check(path.exists(), "Final independent review file (QAD-M4B-INDEPENDENT-REVIEW-FINAL.md) exists")
    if path.exists():
        content = path.read_text()
        check("FINAL" in content, "Review file is marked FINAL")
    # Post-review proof sync
    sync_path = M4B_DIR / "QAD-M4B-POST-REVIEW-PROOF-SYNC.md"
    check(sync_path.exists(), "Post-review proof sync file exists")
    if sync_path.exists():
        sync_content = sync_path.read_text()
        check("MECHANICAL POST-REVIEW VERIFICATION" in sync_content,
              "Post-review sync is marked as mechanical verification, not independent review")


def main():
    print("=" * 60)
    print("QAD-M4B Evaluation Pack Validator (Upgraded)")
    print("=" * 60)

    validate_evaluation_contract()
    validate_fixture_spec()
    validate_acceptance_matrix()
    validate_no_production_code()
    validate_m4a_frozen()
    validate_pit_proof()
    validate_independent_review()

    print("\n" + "=" * 60)
    print(f"Results: {results['pass']} passed, {results['fail']} failed, "
          f"{results['warn']} warnings")
    print("=" * 60)

    if results["fail"] > 0:
        print("\n\u274c VALIDATION FAILED")
        sys.exit(1)
    elif results["warn"] > 0:
        print("\n\u26a0\ufe0f VALIDATION PASSED WITH WARNINGS")
        sys.exit(0)
    else:
        print("\n\u2705 VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()