"""Locked tests: Earnings Quality Dimension (§3.5.1)
Spike verification (28 checks) — earnings quality test block.
SYNTHETIC FIXTURES — NOT LIVE DATA.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fixtures import FIXTURES
from earnings_quality import assess_earnings_quality


# ── Helpers ──

def _by_id(fixtures, tid: str) -> dict:
    for f in fixtures:
        if f["id"] == tid:
            return f
    raise KeyError(f"Fixture {tid} not found")


# ── 6 Tests as specified in the spike blueprint ──

class TestEarningsQualityCosmetic:
    """COSMETIC detection: revenue LOW + buyback ≥2% + one_time items."""

    def test_xyz_is_cosmetic(self):
        """XYZ: revenue LOW + buyback 4.0% + one_time items → COSMETIC."""
        eq = assess_earnings_quality(_by_id(FIXTURES, "XYZ"))
        assert eq["rating"] == "COSMETIC", (
            f"Expected COSMETIC, got {eq['rating']}"
        )
        assert eq["conviction_impact"] == "Red flag — investigate before acting on numbers"
        assert eq["revenue_quality"] == "LOW"
        assert eq["share_buyback_impact_pct"] >= 2.0
        assert eq["one_time_items"] is True


class TestEarningsQualityHigh:
    """HIGH detection: all signals positive, organic beat."""

    def test_aaple_is_high(self):
        """AAPL: HIGH revenue/margin, strong FCF, no one-time, raised guidance."""
        eq = assess_earnings_quality(_by_id(FIXTURES, "AAPL"))
        assert eq["rating"] == "HIGH", f"Expected HIGH, got {eq['rating']}"

    def test_msft_is_high(self):
        """MSFT: HIGH revenue/margin, strong FCF, no one-time, raised guidance."""
        eq = assess_earnings_quality(_by_id(FIXTURES, "MSFT"))
        assert eq["rating"] == "HIGH", f"Expected HIGH, got {eq['rating']}"


class TestEarningsQualityLow:
    """LOW detection: declining revenue, low margins, weak FCF."""

    def test_intc_is_low(self):
        """INTC: revenue LOW + FCF conversion -0.30 < 0.5 → LOW."""
        eq = assess_earnings_quality(_by_id(FIXTURES, "INTC"))
        assert eq["rating"] == "LOW", f"Expected LOW, got {eq['rating']}"


class TestEarningsQualityMedium:
    """MEDIUM detection: mixed signals fall through to default."""

    def test_crm_is_medium(self):
        """CRM: revenue MEDIUM (not HIGH), mixed signals → MEDIUM."""
        eq = assess_earnings_quality(_by_id(FIXTURES, "CRM"))
        assert eq["rating"] == "MEDIUM", f"Expected MEDIUM, got {eq['rating']}"


class TestEarningsQualityConvictionImpact:
    """conviction_impact must match rating for all fixtures."""

    IMPACT_MAP = {
        "HIGH": "Strengthens thesis",
        "MEDIUM": "Neutral — wait for next quarter",
        "LOW": "Weakens thesis",
        "COSMETIC": "Red flag — investigate before acting on numbers",
    }

    def test_conviction_impact_matches_rating(self):
        """Every fixture's conviction_impact correctly reflects its rating."""
        for fixture in FIXTURES:
            eq = assess_earnings_quality(fixture)
            expected_impact = self.IMPACT_MAP.get(eq["rating"])
            assert eq["conviction_impact"] == expected_impact, (
                f"{fixture['id']}: rating={eq['rating']}, "
                f"expected impact='{expected_impact}', "
                f"got='{eq['conviction_impact']}'"
            )
