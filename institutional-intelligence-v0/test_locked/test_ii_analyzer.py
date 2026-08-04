"""Locked tests: Institutional Intelligence V0 — Analyzer
Concentration → Conviction, Action Detection, Signal Scoring.
FD #42 · Phase 10
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from analyzer import (
    concentration_to_conviction,
    detect_action,
    CONVICTION_THRESHOLDS,
)


class TestConcentrationToConviction:
    """Concentration % → Conviction level mapping."""

    def test_maximum_conviction(self):
        r = concentration_to_conviction(44.8)
        assert r["level"] == "Maximum"

    def test_high_conviction(self):
        r = concentration_to_conviction(13.5)
        assert r["level"] == "High"

    def test_moderate_conviction(self):
        r = concentration_to_conviction(7.2)
        assert r["level"] == "Moderate"

    def test_low_conviction(self):
        r = concentration_to_conviction(3.0)
        assert r["level"] == "Low"

    def test_minimal_conviction(self):
        r = concentration_to_conviction(0.5)
        assert r["level"] == "Minimal"

    def test_zero_conviction(self):
        r = concentration_to_conviction(0.0)
        assert r["level"] == "Minimal"

    def test_boundary_exactly_20(self):
        r = concentration_to_conviction(20.0)
        assert r["level"] == "Maximum"

    def test_boundary_exactly_10(self):
        r = concentration_to_conviction(10.0)
        assert r["level"] == "High"

    def test_returns_rationale(self):
        r = concentration_to_conviction(25.0)
        assert isinstance(r["rationale"], str)
        assert len(r["rationale"]) > 10

    def test_all_thresholds_have_rationale(self):
        for threshold, level, rationale in CONVICTION_THRESHOLDS:
            assert isinstance(level, str) and len(level) > 0
            assert isinstance(rationale, str) and len(rationale) > 10


class TestActionDetection:
    """Detect ADD/REDUCE/NEW/EXIT/MAINTAIN/BASELINE from quarter-over-quarter changes."""

    def test_new_position(self):
        r = detect_action(5.0, None, is_baseline=False)
        assert r["action"] == "NEW"

    def test_baseline(self):
        r = detect_action(10.0, None, is_baseline=True)
        assert r["action"] == "BASELINE"

    def test_add_significant(self):
        r = detect_action(15.0, 5.0)  # +200%
        assert r["action"] == "ADD"

    def test_add_moderate(self):
        r = detect_action(12.0, 10.0)  # +20%
        assert r["action"] == "ADD"

    def test_reduce_significant(self):
        r = detect_action(2.0, 10.0)  # -80%
        assert r["action"] == "REDUCE"

    def test_reduce_moderate(self):
        r = detect_action(8.0, 10.0)  # -20%
        assert r["action"] == "REDUCE"

    def test_maintain(self):
        r = detect_action(10.0, 10.0)  # 0% change
        assert r["action"] == "MAINTAIN"

    def test_maintain_small_change(self):
        r = detect_action(10.5, 10.0)  # +5%
        assert r["action"] == "MAINTAIN"

    def test_exit(self):
        r = detect_action(0.0, 5.0)
        assert r["action"] == "EXIT"

    def test_returns_change_pct(self):
        r = detect_action(12.0, 10.0)
        assert "change_pct" in r
        assert r["change_pct"] > 0

    def test_returns_detail(self):
        r = detect_action(5.0, None)
        assert isinstance(r["detail"], str) and len(r["detail"]) > 10


class TestSignalScoring:
    """FD #53: signal_score (0-100) removed — no spec basis. Class retained as
    a guard that the unapproved function is GONE and signals carry only
    approved fields (conviction/action per FD #42)."""

    def test_score_signal_function_removed(self):
        import analyzer as a
        assert not hasattr(a, "score_signal"), "score_signal must not exist (FD #53)"
        assert not hasattr(a, "signal_score"), "signal_score must not exist (FD #53)"
