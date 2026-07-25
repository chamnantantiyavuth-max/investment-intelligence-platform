"""Locked tests: Value Trap Detector (§3.6.2)
Spike verification (28 checks) — value trap test block.
SYNTHETIC FIXTURES — NOT LIVE DATA.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fixtures import FIXTURES
from moat import classify_moat
from value_trap import is_unusually_cheap, run_value_trap_check


# ── Helpers ──

def _by_id(fixtures, tid: str) -> dict:
    for f in fixtures:
        if f["id"] == tid:
            return f
    raise KeyError(f"Fixture {tid} not found")


# ── 8 Tests as specified in the spike blueprint ──

class TestValueTrapVerdicts:
    """Verify value trap verdicts for known fixtures."""

    def test_intc_is_definite_trap(self):
        """INTC: score 0/5 → DEFINITE_TRAP.
        All 5 questions fail: declining revenue, sector headwind, moat narrowing,
        low credibility, and problems explain the cheapness.
        """
        company = _by_id(FIXTURES, "INTC")
        moat = classify_moat(company)
        vt = run_value_trap_check(company, moat)
        assert vt["triggered"] is True
        assert vt["score"] == 0
        assert vt["verdict"] == "DEFINITE_TRAP"

    def test_crm_is_not_a_trap(self):
        """CRM: score 4/5 → NOT_A_TRAP.
        Only Q2 fails (sector headwind in tech). Earnings growing, moat intact,
        credible management, no structural problems.
        """
        company = _by_id(FIXTURES, "CRM")
        moat = classify_moat(company)
        vt = run_value_trap_check(company, moat)
        assert vt["triggered"] is True
        assert vt["score"] == 4
        assert vt["verdict"] == "NOT_A_TRAP"

    def test_xyz_is_trap(self):
        """XYZ: score 1/5 → TRAP.
        Only Q2 passes (sector neutral). Earnings declining, no moat, low
        credibility, problems explain the cheapness.
        """
        company = _by_id(FIXTURES, "XYZ")
        moat = classify_moat(company)
        vt = run_value_trap_check(company, moat)
        assert vt["triggered"] is True
        assert vt["score"] == 1
        assert vt["verdict"] == "TRAP"

    def test_ge_is_suspect(self):
        """GE: score 2/5 → SUSPECT.
        Q1 + Q2 pass (earnings growing, industrials neutral). Moat narrowing
        (Q3 fail), management MEDIUM (Q4 fail), problems exist (Q5 fail).
        """
        company = _by_id(FIXTURES, "GE")
        moat = classify_moat(company)
        vt = run_value_trap_check(company, moat)
        assert vt["triggered"] is True
        assert vt["score"] == 2
        assert vt["verdict"] == "SUSPECT"


class TestIsUnusuallyCheap:
    """is_unusually_cheap: P/E < 70% of 5Y average."""

    def test_threshold_detection(self):
        """INTC (14.0 < 22.0*0.70=15.4) → True; AAPL (31.2 < 28.5*0.70=19.95) → False."""
        assert is_unusually_cheap(_by_id(FIXTURES, "INTC")) is True
        assert is_unusually_cheap(_by_id(FIXTURES, "AAPL")) is False

    def test_division_by_zero_guard(self):
        """When pe_ttm or pe_5y_avg is 0, return False without dividing."""
        company_zero_pe = _by_id(FIXTURES, "INTC").copy()
        company_zero_pe["pe_ttm"] = 0
        assert is_unusually_cheap(company_zero_pe) is False

        company_zero_5y = _by_id(FIXTURES, "INTC").copy()
        company_zero_5y["pe_5y_avg"] = 0
        assert is_unusually_cheap(company_zero_5y) is False


class TestValueTrapQuestions:
    """Verify individual Q1-Q5 pass/fail for INTC (all fail)."""

    def test_intc_all_questions_fail(self):
        """INTC: Q1 (earnings), Q2 (industry), Q3 (moat), Q4 (mgmt), Q5 (reason) all fail."""
        company = _by_id(FIXTURES, "INTC")
        moat = classify_moat(company)
        vt = run_value_trap_check(company, moat)
        questions = vt["questions"]

        assert len(questions) == 5
        # Q1: revenue_growth_3y = -0.08 < 0.03 → FAIL
        assert questions[0]["pass"] is False, "Q1 should fail: declining revenue"
        # Q2: tech sector has 'headwind' in implication → FAIL
        assert questions[1]["pass"] is False, "Q2 should fail: sector headwind"
        # Q3: trend='Narrowing' not in ('Stable', 'Widening') → FAIL
        assert questions[2]["pass"] is False, "Q3 should fail: moat narrowing"
        # Q4: credibility='LOW' → FAIL
        assert questions[3]["pass"] is False, "Q4 should fail: low credibility"
        # Q5: 4/4 problems → fail_count 4 >= 2 → FAIL
        assert questions[4]["pass"] is False, "Q5 should fail: problems exist"

        # Verify question texts
        assert questions[0]["number"] == 1
        assert "Earnings" in questions[0]["question"]
        assert questions[4]["number"] == 5
        assert "GOOD reason" in questions[4]["question"]


class TestValueTrapScoring:
    """Scoring 0-5 maps to correct verdict."""

    def test_verdict_mapping(self):
        """Verify mapping for scores 0, 1, 2, 3, 4, 5."""
        # Map each fixture's score to expected verdict
        checks = [
            ("INTC", 0, "DEFINITE_TRAP"),
            ("XYZ", 1, "TRAP"),
            ("GE", 2, "SUSPECT"),
            ("CRM", 4, "NOT_A_TRAP"),
        ]
        for tid, expected_score, expected_verdict in checks:
            company = _by_id(FIXTURES, tid)
            moat = classify_moat(company)
            vt = run_value_trap_check(company, moat)
            assert vt["score"] == expected_score, (
                f"{tid}: expected score {expected_score}, got {vt['score']}"
            )
            assert vt["verdict"] == expected_verdict, (
                f"{tid}: expected verdict {expected_verdict}, got {vt['verdict']}"
            )
