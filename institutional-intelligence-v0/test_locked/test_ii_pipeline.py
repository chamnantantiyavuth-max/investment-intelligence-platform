"""Locked tests: Institutional Intelligence V0 — Pipeline
End-to-end smoke tests. Synthetic fixtures only.
FD #42 · Phase 10 + 10.5
"""
import sys, os

# Fix combined-test collision: same-named modules (pipeline, fixtures) in
# fundamental-opportunity-v0 and institutional-intelligence-v0.
# Clear stale cached modules so the institutional one loads correctly.
_ii_dir = os.path.join(os.path.dirname(__file__), "..")
for _mod in ("pipeline", "fixtures"):
    if _mod in sys.modules:
        _cached = sys.modules[_mod]
        if hasattr(_cached, "__file__") and _cached.__file__:
            if "institutional" not in _cached.__file__:
                del sys.modules[_mod]
sys.path.insert(0, _ii_dir)

from pipeline import (
    run_pipeline,
    query_signals_by_ticker,
    query_signals_by_fund,
    query_top_conviction,
    _previous_quarter,
)


class TestPipelineOutput:
    """Pipeline produces correct structure."""

    def test_returns_signals_and_summary(self):
        result = run_pipeline()
        assert "signals" in result
        assert "summary" in result
        assert "meta" in result
        assert result["meta"]["data_source"] == "SYNTHETIC"

    def test_signals_have_required_fields(self):
        result = run_pipeline()
        required = [
            "filer_name", "filer_cik", "ticker", "filing_quarter",
            "pct_of_portfolio", "conviction", "action",
        ]
        for s in result["signals"]:
            for field in required:
                assert field in s, f"Missing {field} in signal"

    def test_conviction_maps_correctly(self):
        result = run_pipeline()
        valid_convictions = {"Maximum", "High", "Moderate", "Low", "Minimal"}
        for s in result["signals"]:
            assert s["conviction"] in valid_convictions


class TestQueryFunctions:
    """Pipeline query helpers work correctly."""

    def test_query_by_ticker(self):
        result = run_pipeline()
        signals = result["signals"]
        filtered = query_signals_by_ticker("NVDA", signals)
        assert len(filtered) > 0
        for s in filtered:
            assert s["ticker"] == "NVDA"

    def test_query_by_fund(self):
        result = run_pipeline()
        signals = result["signals"]
        # Use a CIK from fixtures
        filtered = query_signals_by_fund("0001067983", signals)
        assert len(filtered) > 0
        for s in filtered:
            assert s["filer_cik"] == "0001067983"

    def test_query_top_conviction(self):
        result = run_pipeline()
        signals = result["signals"]
        filtered = query_top_conviction(signals, "High")
        for s in filtered:
            assert s["conviction"] in ("Maximum", "High")


class TestPreviousQuarter:
    """Quarter math."""

    def test_q1_previous_is_q4_prior_year(self):
        assert _previous_quarter("2026Q1") == "2025Q4"

    def test_q2_previous_is_q1(self):
        assert _previous_quarter("2026Q2") == "2026Q1"


class TestPipelineWithRealData:
    """Pipeline handles real 13F data correctly."""

    def test_real_data_source_watermark(self):
        result = run_pipeline(filings=[{
            "filer_cik": "0001067983",
            "filer_name": "Berkshire Hathaway",
            "filing_quarter": "2026Q1",
            "report_date": "2026-03-31",
            "holdings": [
                {"ticker": "AAPL", "pct_of_portfolio": 22.0, "value_usd": 150e9},
                {"ticker": "BAC", "pct_of_portfolio": 10.5, "value_usd": 70e9},
            ],
        }])
        assert result["meta"]["data_source"] == "REAL 13F"
        assert len(result["signals"]) == 2

    def test_real_data_conviction_from_concentration(self):
        result = run_pipeline(filings=[{
            "filer_cik": "0001067983",
            "filer_name": "Test Fund",
            "filing_quarter": "2026Q1",
            "report_date": "2026-03-31",
            "holdings": [
                {"ticker": "MEGA", "pct_of_portfolio": 25.0, "value_usd": 50e9},
            ],
        }])
        assert result["signals"][0]["conviction"] == "Maximum"
