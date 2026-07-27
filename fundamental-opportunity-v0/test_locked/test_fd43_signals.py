"""
Locked acceptance tests — Profit Rate Trend & Narrative Gap (FD #43)
Per project-workflow v3.0: locked tests = spec-as-code, immutable by subagents.
"""
import pytest
from value_trap import run_profit_rate_trend
from narrative_gap import run_narrative_gap, compute_fair_value


# ── Profit Rate Trend (Q0 Value Trap pre-check) ──


class TestProfitRateTrend:
    """Q0: ROIC trend analysis — Growth Trap detection."""

    def test_no_decline_stable(self):
        """ROIC stable with growth → NO_DECLINE, not triggered."""
        company = {
            "roic_current": 0.25,
            "roic_5y": 0.25,
            "revenue_growth_3y": 0.10,
            "invested_capital": 50,
        }
        result = run_profit_rate_trend(company)
        assert result["verdict"] == "NO_DECLINE"
        assert result["triggered"] is False

    def test_growth_trap_triggered(self):
        """ROIC dropped 30% from 5Y avg + revenue growing → GROWTH_TRAP."""
        company = {
            "roic_current": 0.14,    # was 0.20
            "roic_5y": 0.20,          # 30% decline
            "revenue_growth_3y": 0.08,  # growing
            "invested_capital": 100,
        }
        result = run_profit_rate_trend(company)
        assert result["verdict"] == "GROWTH_TRAP"
        assert result["triggered"] is True
        assert result["decline_pct"] == pytest.approx(0.30, abs=0.01)

    def test_decline_but_revenue_shrinking(self):
        """ROIC declined but revenue negative → NOT triggered (not a growth trap)."""
        company = {
            "roic_current": 0.10,
            "roic_5y": 0.20,          # 50% decline
            "revenue_growth_3y": -0.05,  # shrinking
            "invested_capital": 80,
        }
        result = run_profit_rate_trend(company)
        # Should NOT trigger — revenue isn't growing, so it's not a "growth trap"
        assert result["triggered"] is False

    def test_moderate_decline(self):
        """ROIC declined 15% with growth → MODERATE_DECLINE, not triggered."""
        company = {
            "roic_current": 0.17,
            "roic_5y": 0.20,          # 15% decline
            "revenue_growth_3y": 0.06,
            "invested_capital": 60,
        }
        result = run_profit_rate_trend(company)
        assert result["verdict"] == "MODERATE_DECLINE"
        assert result["triggered"] is False  # not >=20%

    def test_roic_improving(self):
        """ROIC improving vs 5Y → NO_DECLINE."""
        company = {
            "roic_current": 0.30,
            "roic_5y": 0.22,
            "revenue_growth_3y": 0.12,
            "invested_capital": 150,
        }
        result = run_profit_rate_trend(company)
        assert result["verdict"] == "NO_DECLINE"
        assert result["triggered"] is False
        assert result["decline_pct"] < 0  # negative = improving

    def test_insufficient_data(self):
        """Missing ROIC data → not triggered."""
        company = {"roic_current": 0, "roic_5y": 0, "revenue_growth_3y": 0.10}
        result = run_profit_rate_trend(company)
        assert result["triggered"] is False
        assert "Insufficient" in result.get("reason", "")


# ── Narrative vs Reality Gap ──


class TestNarrativeGap:
    """Narrative Gap: market cap vs fair value divergence."""

    def test_fair_value_computation(self):
        """Fair value = 20% bull + 60% base + 20% bear."""
        company = {
            "market_cap": 100,
            "current_price": 10,
            "scenario_bull": 15,
            "scenario_base": 10,
            "scenario_bear": 5,
        }
        fv = compute_fair_value(company)
        # weighted price = 15*0.2 + 10*0.6 + 5*0.2 = 3+6+1 = 10
        # implied shares = 100/10 = 10
        # fair value = 10 * 10 = 100
        assert fv == 100.0

    def test_fair_priced(self):
        """Gap ratio ~1.0 → FAIR."""
        company = {
            "name": "TestCo",
            "market_cap": 200,
            "current_price": 20,
            "scenario_bull": 25,
            "scenario_base": 20,
            "scenario_bear": 15,
        }
        result = run_narrative_gap(company)
        assert result["verdict"] == "FAIR"
        assert result["triggered"] is False
        assert result["gap_ratio"] == pytest.approx(1.0, abs=0.1)

    def test_bubble_risk(self):
        """Market cap > 2x fair value → BUBBLE_RISK."""
        company = {
            "name": "BubbleCo",
            "market_cap": 500,
            "current_price": 100,
            "scenario_bull": 60,
            "scenario_base": 25,
            "scenario_bear": 10,
        }
        result = run_narrative_gap(company)
        assert result["verdict"] == "BUBBLE_RISK"
        assert result["triggered"] is True
        assert result["gap_ratio"] > 2.0

    def test_undervalued(self):
        """Market cap < 0.5x fair value → UNDERVALUED."""
        company = {
            "name": "HiddenGem",
            "market_cap": 50,
            "current_price": 5,
            "scenario_bull": 25,
            "scenario_base": 15,
            "scenario_bear": 8,
        }
        result = run_narrative_gap(company)
        assert result["verdict"] == "UNDERVALUED"
        assert result["triggered"] is True
        assert result["gap_ratio"] < 0.5

    def test_elevated(self):
        """Gap ratio 1.5-2.0 → ELEVATED."""
        company = {
            "name": "StretchedCo",
            "market_cap": 300,
            "current_price": 30,
            "scenario_bull": 20,
            "scenario_base": 15,
            "scenario_bear": 10,
        }
        result = run_narrative_gap(company)
        assert result["verdict"] == "ELEVATED"

    def test_insufficient_data(self):
        """Missing scenario data → INSUFFICIENT_DATA."""
        company = {"name": "NoData", "market_cap": 100, "current_price": 0}
        result = run_narrative_gap(company)
        assert result["verdict"] == "INSUFFICIENT_DATA"


# ── Integration: pipeline includes both signals ──


class TestPipelineIntegration:
    """Verify both FD #43 signals appear in pipeline output."""

    def test_every_package_has_profit_rate_trend(self):
        """All 8 fixture companies produce profit_rate_trend in valuation_context."""
        from pipeline import run_pipeline
        packages = run_pipeline()
        assert len(packages) == 8
        for pkg in packages:
            prt = pkg["valuation_context"]["profit_rate_trend"]
            assert "verdict" in prt
            assert "decline_pct" in prt
            assert "roic_current" in prt

    def test_every_package_has_narrative_gap(self):
        """All 8 fixture companies produce narrative_gap in valuation_context."""
        from pipeline import run_pipeline
        packages = run_pipeline()
        for pkg in packages:
            ng = pkg["valuation_context"]["narrative_gap"]
            assert "verdict" in ng
            assert "gap_ratio" in ng

    def test_intel_is_not_growth_trap_despite_roic_decline(self):
        """INTC: ROIC dropped 75% but revenue is NEGATIVE → NOT a growth trap."""
        from pipeline import run_pipeline
        packages = run_pipeline()
        intc = [p for p in packages if p["id"] == "INTC"][0]
        prt = intc["valuation_context"]["profit_rate_trend"]
        # ROIC dropped massively but revenue is shrinking
        assert prt["triggered"] is False
        assert prt["decline_pct"] > 0.50  # massive decline confirmed

    def test_costco_narrative_gap_elevated(self):
        """COST: P/E 42 vs industry 14.5 → narrative gap should be elevated."""
        from pipeline import run_pipeline
        packages = run_pipeline()
        cost = [p for p in packages if p["id"] == "COST"][0]
        ng = cost["valuation_context"]["narrative_gap"]
        # COST trades at premium — current price near base scenario
        # Gap should be >= 0.9 (close to fair value)
        assert ng["gap_ratio"] >= 0.9
