"""Locked tests: Moat Classification System (§3.4.1)
Spike verification (28 checks) — moat test block.
SYNTHETIC FIXTURES — NOT LIVE DATA.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fixtures import FIXTURES
from moat import (
    classify_moat,
    moat_conviction_cap,
    moat_strength_score,
    moat_narrative,
)


# ── Helpers ──

def _by_id(fixtures, tid: str) -> dict:
    for f in fixtures:
        if f["id"] == tid:
            return f
    raise KeyError(f"Fixture {tid} not found")


# ── 8 Tests as specified in the spike blueprint ──

class TestMoatClassification:
    """Verify classify_moat for known fixtures."""

    def test_aaple_classified_wide(self):
        """AAPL: Wide moat, Deep, Stable."""
        moat = classify_moat(_by_id(FIXTURES, "AAPL"))
        assert moat["width"] == "Wide"
        assert moat["depth"] == "Deep"
        assert moat["trend"] == "Stable"

    def test_intc_classified_narrow(self):
        """INTC: Narrow moat, Shallow, Narrowing."""
        moat = classify_moat(_by_id(FIXTURES, "INTC"))
        assert moat["width"] == "Narrow"
        assert moat["depth"] == "Shallow"
        assert moat["trend"] == "Narrowing"

    def test_xyz_classified_none(self):
        """XYZ: empty moat_types forces None width, Shallow depth."""
        moat = classify_moat(_by_id(FIXTURES, "XYZ"))
        assert moat["width"] == "None"
        assert moat["depth"] == "Shallow"
        assert moat["trend"] == "Narrowing"
        assert moat["total_types"] == 0
        assert moat["active_count"] == 0

    def test_msft_wide_with_three_types(self):
        """MSFT: Wide/Deep/Widening, 3 types, all Strong."""
        moat = classify_moat(_by_id(FIXTURES, "MSFT"))
        assert moat["width"] == "Wide"
        assert moat["depth"] == "Deep"
        assert moat["trend"] == "Widening"
        assert moat["total_types"] == 3
        assert moat["active_count"] == 3

    def test_width_depth_trend_mapped_correctly(self):
        """Verify width/depth/trend fields map correctly for all fixtures."""
        for fixture in FIXTURES:
            moat = classify_moat(fixture)
            # width must be one of the valid values
            assert moat["width"] in ("Wide", "Narrow", "None")
            # depth must be one of the valid values
            assert moat["depth"] in ("Deep", "Moderate", "Shallow")
            # trend must be one of the valid values
            assert moat["trend"] in ("Stable", "Widening", "Narrowing")
            # types_summary should be a string
            assert isinstance(moat["types_summary"], str)


class TestMoatConvictionCap:
    """Conviction cap table: width × depth mapping."""

    def test_conviction_cap_table(self):
        """Wide+Deep=Maximum, Narrow+Shallow=Moderate, None+Shallow=Moderate."""
        aapl_moat = classify_moat(_by_id(FIXTURES, "AAPL"))
        intc_moat = classify_moat(_by_id(FIXTURES, "INTC"))
        xyz_moat = classify_moat(_by_id(FIXTURES, "XYZ"))

        assert moat_conviction_cap(aapl_moat) == "Maximum"
        assert moat_conviction_cap(intc_moat) == "Moderate"
        assert moat_conviction_cap(xyz_moat) == "Moderate"


class TestMoatStrengthScore:
    """moat_strength_score returns 0-100 integer."""

    def test_score_range_0_to_100(self):
        """Score is always an integer in [0, 100] for all fixtures."""
        for fixture in FIXTURES:
            moat = classify_moat(fixture)
            score = moat_strength_score(moat)
            assert isinstance(score, int), f"{fixture['id']}: expected int, got {type(score)}"
            assert 0 <= score <= 100, f"{fixture['id']}: {score} outside [0, 100]"
        # Verify specific values
        assert moat_strength_score(classify_moat(_by_id(FIXTURES, "XYZ"))) == 0
        assert moat_strength_score(classify_moat(_by_id(FIXTURES, "MSFT"))) == 100


class TestMoatNarrative:
    """moat_narrative returns non-empty descriptive string."""

    def test_narrative_is_non_empty_string(self):
        """Every fixture produces a non-empty, descriptive narrative."""
        for fixture in FIXTURES:
            moat = classify_moat(fixture)
            narrative = moat_narrative(moat)
            assert isinstance(narrative, str), f"{fixture['id']}: expected str, got {type(narrative)}"
            assert len(narrative) > 0, f"{fixture['id']}: narrative is empty"
