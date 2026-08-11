"""Locked-style tests — Quality & Asymmetry Discovery archetype engine (WP2).

Invariants under test:
  1. Pure module imports without yfinance/numpy (pytest venv 3.11 compatible).
  2. Each archetype returns the documented contract (archetype/name/signals/
     checks/matched_count/proposed/as_of).
  3. Thresholds are marked PROPOSED (FD #53) — no production claim.
  4. Deterministic: same input → same output (no RNG, no time).
  5. Known-case behavior: a clean compounder matches A; a no-growth, high-debt,
     overvalued name matches nothing; a cash-rich special-situation matches D.
  6. Firewall contract: scan_ticker output carries evidence-only firewall.
  7. ROIC math: NOPAT/invested-capital computed correctly on a hand-built case.
  8. FCF conversion uses OCF+capex (negative capex convention).
"""
import pytest

from discovery.quality_asymmetry.archetypes import (
    PROPOSED,
    ARCHETYPE_NAMES,
    archetype_a_durable_compounder,
    archetype_b_long_runway,
    archetype_c_mispriced_quality,
    archetype_d_asymmetric_value,
    run_shadow,
    scan_ticker,
)


def _compounder_fin():
    """5 years of a clean compounder: revenue up, high ROIC, strong FCF, no debt."""
    return {
        "revenue": [100, 120, 150, 180, 220],
        "net_income": [20, 25, 32, 40, 50],
        "operating_income": [25, 32, 40, 50, 62],
        "total_assets": [150, 170, 200, 230, 260],
        "total_equity": [100, 115, 135, 155, 180],
        "total_debt": [0, 0, 0, 0, 0],
        "cash": [30, 35, 40, 45, 50],
        "ocf": [28, 33, 40, 48, 58],
        "capex": [-5, -6, -7, -8, -9],
        "dividends_paid": [-4, -5, -6, -7, -8],
        "buybacks_paid": [0, 0, 0, 0, 0],
        "ebitda": [30, 38, 47, 58, 71],
    }


def test_pure_module_imports_without_yfinance():
    import sys
    assert "yfinance" not in sys.modules
    assert "numpy" not in sys.modules


def test_archetype_contract_shape():
    fin = _compounder_fin()
    for fn in (archetype_a_durable_compounder, archetype_b_long_runway,
               archetype_c_mispriced_quality):
        out = fn(fin, {})
        assert out["archetype"] in ARCHETYPE_NAMES
        assert out["name"] == ARCHETYPE_NAMES[out["archetype"]]
        assert isinstance(out["signals"], dict)
        assert isinstance(out["checks"], dict)
        assert isinstance(out["matched_count"], int)
        assert out["proposed"] is True
        assert "as_of" in out


def test_all_thresholds_proposed():
    # FD #53: no production thresholds — the engine must declare PROPOSED
    assert PROPOSED  # non-empty
    out = scan_ticker("TEST", {"revenue": [1], "net_income": [1],
                               "operating_income": [1], "total_assets": [10],
                               "total_equity": [5], "total_debt": [0],
                               "cash": [1], "ocf": [1], "capex": [0]})
    assert out["proposed"] is True
    for a in out["archetypes"]:
        assert a["proposed"] is True


def test_deterministic():
    fin = _compounder_fin()
    a1 = scan_ticker("X", fin, {"price": 100})
    a2 = scan_ticker("X", fin, {"price": 100})
    assert a1 == a2


def test_compounder_matches_archetype_a():
    out = archetype_a_durable_compounder(_compounder_fin())
    # ROIC latest: NOPAT=62*0.79=48.98; invested=260-50=210 → 23.3%
    assert out["signals"]["roic_latest"] is not None
    assert out["signals"]["roic_latest"] > 0.20
    assert out["checks"]["roic_latest >= A_ROIC_MIN"] is True
    assert out["checks"]["net_debt/ebitda <= A_NET_DEBT_EBITDA_MAX"] is True
    assert out["matched_count"] >= 4


def test_roic_math_hand_computed():
    fin = {
        "operating_income": [100],
        "total_assets": [500],
        "cash": [100],
        "total_debt": [0],
        "total_equity": [200],
    }
    out = archetype_a_durable_compounder(fin)
    # NOPAT = 100 * 0.79 = 79; invested = 500 - 100 = 400; ROIC = 19.75%
    assert out["signals"]["roic_latest"] == pytest.approx(0.1975, abs=1e-9)


def test_bad_business_matches_nothing():
    fin = {
        "revenue": [100, 95, 90, 85, 80],   # shrinking
        "net_income": [10, 8, 5, 2, -3],    # deteriorating
        "operating_income": [12, 10, 7, 3, -1],
        "total_assets": [300, 320, 340, 360, 380],
        "total_equity": [100, 95, 88, 80, 70],
        "total_debt": [120, 140, 160, 180, 200],  # rising debt
        "cash": [10, 8, 6, 4, 2],
        "ocf": [15, 10, 5, 0, -5],
        "capex": [-8, -8, -8, -8, -8],
        "dividends_paid": [-2, -2, -2, -2, -2],
        "buybacks_paid": [0, 0, 0, 0, 0],
        "ebitda": [15, 13, 10, 6, 2],
    }
    market = {"price": 50, "price_52w_high": 100, "pe_ratio": 100, "pb_ratio": 5}
    a = archetype_a_durable_compounder(fin, market)
    b = archetype_b_long_runway(fin, market)
    c = archetype_c_mispriced_quality(fin, market)
    d = archetype_d_asymmetric_value(fin, market, {})
    # A: ROIC negative-ish → fail; B: no growth → fail; C: quality fails; D: no cash
    assert a["matched_count"] <= 1
    assert b["matched_count"] == 0
    assert c["quality_pass"] is False
    assert d["matched_count"] == 0


def test_cash_rich_special_situation_matches_d():
    fin = {
        "revenue": [50, 55, 60, 65, 70],
        "net_income": [5, 5, 6, 6, 7],
        "operating_income": [6, 6, 7, 7, 8],
        "total_assets": [200, 210, 220, 230, 240],
        "total_equity": [150, 155, 160, 165, 170],
        "total_debt": [0, 0, 0, 0, 0],
        "cash": [80, 85, 90, 95, 100],       # huge cash pile
        "ocf": [10, 11, 12, 13, 14],
        "capex": [-3, -3, -3, -3, -3],
        "dividends_paid": [-2, -2, -2, -2, -2],
        "buybacks_paid": [-8, -9, -10, -11, -12],  # heavy buybacks
        "ebitda": [8, 8, 9, 9, 10],
    }
    market = {"pb_ratio": 1.2, "buyback_yield_ttm": 0.06}
    recon = {"special_situation": ["holding_co_discount", "forced_selling"]}
    d = archetype_d_asymmetric_value(fin, market, recon)
    assert d["signals"]["net_cash"] is True
    assert d["checks"]["net cash or low leverage"] is True
    assert d["checks"]["buyback_yield >= D_BUYBACK_YIELD_MIN"] is True
    assert d["checks"]["pb <= D_PB_MAX"] is True
    assert d["checks"]["special situation flagged"] is True
    assert d["matched_count"] == 4


def test_firewall_contract():
    fin = _compounder_fin()
    out = scan_ticker("AAPL", fin, {"price": 200})
    assert "firewall" in out
    assert "evidence only" in out["firewall"]
    assert out["ticker"] == "AAPL"
    assert len(out["archetypes"]) == 4


def test_run_shadow_batch():
    fin = _compounder_fin()
    payloads = {
        "CO1": {"fin": fin, "market": {"price": 100}},
        "CO2": {"fin": fin, "market": {"price": 120}},
    }
    results = run_shadow(payloads)
    assert len(results) == 2
    assert {r["ticker"] for r in results} == {"CO1", "CO2"}
