"""Locked tests: Institutional Intelligence V0 — Pipeline
End-to-end smoke tests. Synthetic fixtures only.
FD #42 · Phase 10
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline import (
    run_pipeline,
    query_signals_by_ticker,
    query_signals_by_fund,
    query_top_conviction,
    _previous_quarter,
)
from fixtures import FIXTURES


class TestPipelineOutput:
    """Pipeline produces correct structure."""

    def test_returns_result_with_signals_and_summary(self):
        result = run_pipeline()
        assert "signals" in result
        assert "summary" in result
        assert "meta" in result

    def test_signals_non_empty(self):
        result = run_pipeline()
        assert len(result["signals"]) > 0

    def test_each_signal_has_required_keys(self):
        result = run_pipeline()
        required = [
            "filer_name", "filer_cik", "filer_category", "ticker",
            "filing_quarter", "report_date", "pct_of_portfolio",
            "conviction", "conviction_rationale", "action", "action_detail",
            "change_pct", "signal_score", "value_usd",
        ]
        for s in result["signals"]:
            for k in required:
                assert k in s, f"Signal missing key: {k}"

    def test_signals_sorted_by_score_desc(self):
        result = run_pipeline()
        scores = [s["signal_score"] for s in result["signals"]]
        assert scores == sorted(scores, reverse=True), "Signals not sorted by score descending"

    def test_summary_has_stats(self):
        result = run_pipeline()
        s = result["summary"]
        assert s["total_funds_tracked"] > 0
        assert s["total_signals"] > 0
        assert s["total_filings"] > 0
        assert "fund_stats" in s
        assert "ticker_stats" in s

    def test_meta_has_latency_note(self):
        result = run_pipeline()
        assert "latency_note" in result["meta"]
        assert "45-day" in result["meta"]["latency_note"]


class TestPipelineQueries:
    """Query functions filter correctly."""

    def test_query_by_ticker(self):
        result = run_pipeline()
        aapl_signals = query_signals_by_ticker("AAPL", result["signals"])
        assert len(aapl_signals) > 0
        for s in aapl_signals:
            assert s["ticker"] == "AAPL"

    def test_query_by_ticker_case_insensitive(self):
        result = run_pipeline()
        aapl = query_signals_by_ticker("aapl", result["signals"])
        msft = query_signals_by_ticker("MSFT", result["signals"])
        assert len(aapl) > 0
        assert len(msft) > 0

    def test_query_by_fund(self):
        result = run_pipeline()
        brk = query_signals_by_fund("0001067983", result["signals"])
        assert len(brk) > 0
        for s in brk:
            assert s["filer_cik"] == "0001067983"

    def test_query_top_conviction(self):
        result = run_pipeline()
        high = query_top_conviction(result["signals"], "High")
        for s in high:
            assert s["conviction"] in ("Maximum", "High")

    def test_query_top_conviction_maximum(self):
        result = run_pipeline()
        max_sigs = query_top_conviction(result["signals"], "Maximum")
        for s in max_sigs:
            assert s["conviction"] == "Maximum"


class TestPreviousQuarter:
    """Quarter arithmetic helper."""

    def test_q1_to_prev(self):
        assert _previous_quarter("2026Q1") == "2025Q4"

    def test_q2_to_prev(self):
        assert _previous_quarter("2026Q2") == "2026Q1"

    def test_q4_to_prev(self):
        assert _previous_quarter("2026Q4") == "2026Q3"


class TestEmptyPipeline:
    """Empty input returns gracefully."""

    def test_empty_input_returns_empty(self):
        result = run_pipeline(filings=[])
        assert result["signals"] == []
        assert result["meta"]["error"] == "No data"
