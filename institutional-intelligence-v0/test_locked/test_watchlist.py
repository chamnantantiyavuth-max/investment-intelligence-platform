"""Locked tests: Institutional Intelligence V0 — Watchlist
FD #42 · Phase 10
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from watchlist import (
    WATCHLIST, CATEGORIES, get_fund, get_funds_by_category, get_all_ciks, summary,
)


class TestWatchlistIntegrity:
    """Watchlist data is complete and well-formed."""

    def test_all_five_categories_present(self):
        cats = set(f["category"] for f in WATCHLIST)
        for c in CATEGORIES:
            assert c in cats, f"Category '{c}' missing from watchlist"

    def test_every_fund_has_required_fields(self):
        required = ["name", "cik", "manager", "category", "style", "aum_b"]
        for f in WATCHLIST:
            for field in required:
                assert field in f, f"Fund {f.get('name','?')} missing field '{field}'"
                assert f[field] is not None, f"Fund {f['name']} has None for '{field}'"

    def test_cik_format(self):
        for f in WATCHLIST:
            assert f["cik"].startswith("000"), f"CIK {f['cik']} doesn't start with 000"
            assert len(f["cik"]) == 10, f"CIK {f['cik']} not 10 chars"

    def test_aum_positive(self):
        for f in WATCHLIST:
            assert f["aum_b"] > 0, f"Fund {f['name']} has AUM <= 0"

    def test_no_duplicate_ciks(self):
        ciks = [f["cik"] for f in WATCHLIST]
        assert len(ciks) == len(set(ciks)), f"Duplicate CIKs found: {len(ciks)} vs {len(set(ciks))}"

    def test_all_categories_in_valid_list(self):
        for f in WATCHLIST:
            assert f["category"] in CATEGORIES, f"Invalid category '{f['category']}' for {f['name']}"


class TestWatchlistLookup:
    """Lookup functions work correctly."""

    def test_get_fund_by_name(self):
        f = get_fund(name="Berkshire Hathaway")
        assert f is not None
        assert f["cik"] == "0001067983"

    def test_get_fund_by_cik(self):
        f = get_fund(cik="0001649339")
        assert f is not None
        assert f["name"] == "Scion Asset Management"

    def test_get_fund_not_found(self):
        assert get_fund(name="Nonexistent Fund") is None
        assert get_fund(cik="0000000000") is None

    def test_get_funds_by_category(self):
        legendary = get_funds_by_category("Legendary")
        assert len(legendary) >= 10
        for f in legendary:
            assert f["category"] == "Legendary"

    def test_get_all_ciks(self):
        ciks = get_all_ciks()
        assert len(ciks) == len(WATCHLIST)
        assert all(isinstance(c, str) for c in ciks)


class TestWatchlistSummary:
    """Summary function works."""

    def test_summary_returns_string(self):
        s = summary()
        assert isinstance(s, str)
        assert "Legendary" in s
        assert "TOTAL:" in s

    def test_summary_includes_all_categories(self):
        s = summary()
        for cat in CATEGORIES:
            assert cat in s, f"Category '{cat}' missing from summary"
