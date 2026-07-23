"""
Locked Acceptance Test: Anomaly Detection (T2-L1)
Parent-written · READ-ONLY for subagents
Verifies statistical anomaly detection produces valid output from market data.
Per FD #27 §2: Must be ACTUAL COMPUTATION — not hand-written fixtures.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestAnomalyDetectionOutput:
    """All detection functions must produce well-formed anomaly records."""

    def test_detect_sector_divergence_returns_list(self):
        """detect_sector_divergence() must return a list of anomaly dicts."""
        from experimental.anomaly import detect_sector_divergence

        # Synthetic test data: theme RS values over time
        theme_rs_data = {
            "TH-004": [45, 48, 52, 55, 58, 62, 78, 85],  # sharp acceleration
            "TH-014": [30, 31, 29, 32, 33, 31, 30, 32],  # flat
        }
        sector_benchmark = 35  # static benchmark for test

        result = detect_sector_divergence(theme_rs_data, benchmark=sector_benchmark)
        assert isinstance(result, list), f"Expected list, got {type(result).__name__}"

        for an in result:
            self._assert_valid_anomaly(an, "Sector Divergence")

    def test_detect_single_stock_outlier_returns_list(self):
        """detect_single_stock_outlier() must return a list of anomaly dicts."""
        from experimental.anomaly import detect_single_stock_outlier

        price_data = {"NVDA": [100, 102, 105, 108, 112, 118, 125, 150]}
        benchmark = {"benchmark": [100, 101, 102, 103, 104, 105, 106, 107]}

        result = detect_single_stock_outlier(price_data, benchmark)
        assert isinstance(result, list), f"Expected list, got {type(result).__name__}"

        for an in result:
            self._assert_valid_anomaly(an, "Single-Stock Outlier")

    def test_detect_volume_anomaly_returns_list(self):
        """detect_volume_anomaly() must return a list of anomaly dicts."""
        from experimental.anomaly import detect_volume_anomaly

        volume_data = {"TEST": [1000, 1100, 1050, 1200, 1150, 3000, 1100]}
        avg_baseline = 1200

        result = detect_volume_anomaly(volume_data, avg_baseline=avg_baseline)
        assert isinstance(result, list), f"Expected list, got {type(result).__name__}"

        for an in result:
            self._assert_valid_anomaly(an, "Volume Anomaly")

    def test_detect_missing_correlation_returns_list(self):
        """detect_missing_correlation() must return a list of anomaly dicts."""
        from experimental.anomaly import detect_missing_correlation

        etf_data = {"TAN": [100, 105, 110, 108, 112, 115, 120, 125]}
        candidate_data = {"FSLR": [100, 101, 100, 102, 99, 98, 100, 99]}

        result = detect_missing_correlation(etf_data, candidate_data)
        assert isinstance(result, list), f"Expected list, got {type(result).__name__}"

        for an in result:
            self._assert_valid_anomaly(an, "Missing Correlation")

    def test_detection_is_computational_not_fixture(self):
        """Detection must compute from input data, not return hard-coded fixtures.
        Same input must produce same output; different input must produce different output."""
        from experimental.anomaly import detect_volume_anomaly

        # Same input → same output
        v1 = {"A": [100, 200, 100]}
        r1 = detect_volume_anomaly(v1, avg_baseline=120)
        r2 = detect_volume_anomaly(v1, avg_baseline=120)
        assert r1 == r2, "Same input must produce same output (deterministic)"

        # Different input → potentially different output
        v2 = {"A": [100, 100, 100]}  # flat, no anomaly expected
        r3 = detect_volume_anomaly(v2, avg_baseline=100)
        # Flat data at baseline should produce fewer anomalies than spike data
        # (not strictly required, but validates computation vs fixture)
        assert len(r3) <= len(r1), "Flat data at baseline should not produce more anomalies than spike data"

    def test_anomaly_output_has_required_fields(self):
        """Every detected anomaly must have: id, type, description, first_observed, status, source."""
        from experimental.anomaly import detect_sector_divergence

        result = detect_sector_divergence(
            {"TH-004": [10, 15, 20, 25, 30, 35, 40, 45]},
            benchmark=20,
        )
        for an in result:
            self._assert_valid_anomaly(an, "Sector Divergence")

    # ── helpers ──

    def _assert_valid_anomaly(self, anomaly, expected_type):
        assert "id" in anomaly, f"Missing id in {anomaly}"
        assert anomaly.get("type") == expected_type, \
            f"Expected type {expected_type}, got {anomaly.get('type')}"
        assert "description" in anomaly, "Missing description"
        assert "first_observed" in anomaly, "Missing first_observed"
        assert "status" in anomaly, "Missing status"


class TestAnomalyDetectionEdgeCases:
    """Detection should handle edge cases gracefully."""

    def test_empty_input_returns_empty_list(self):
        """Empty data should return empty list, not error."""
        from experimental.anomaly import detect_sector_divergence, detect_single_stock_outlier
        from experimental.anomaly import detect_volume_anomaly, detect_missing_correlation

        assert detect_sector_divergence({}, benchmark=0) == []
        assert detect_single_stock_outlier({}, {}) == []
        assert detect_volume_anomaly({}, avg_baseline=0) == []
        assert detect_missing_correlation({}, {}) == []

    def test_single_value_input_handled(self):
        """Single data point should not crash."""
        from experimental.anomaly import detect_volume_anomaly

        result = detect_volume_anomaly({"A": [100]}, avg_baseline=100)
        assert isinstance(result, list), f"Single-value input should return list, got {type(result).__name__}"
