"""Offline reconciliation of the UNH QAD pilot against the committed SEC snapshot."""
from decimal import Decimal

from scripts.qad_pilot.unh_reconcile import _calc_map, reconcile


def _row(result, name, period):
    return _calc_map(result)[(name, period)]


def test_no_unexpected_mismatches():
    result = reconcile()
    assert result["mismatches"] == []
    assert result["ticker"] == "UNH"


def test_fy2025_operating_margin_and_fcf():
    result = reconcile()
    margin = _row(result, "operating_margin_percent", "FY2025")
    fcf = _row(result, "free_cash_flow_millions", "FY2025")
    assert margin["value"] == "4.2"
    assert margin["inputs_millions"] == {"earnings_from_operations": 18964, "revenues": 447567}
    assert fcf["value"] == "16075"
    assert fcf["inputs_millions"] == {"cfo": 19697, "capex": 3622}


def test_interest_coverage_and_net_debt():
    result = reconcile()
    assert _row(result, "interest_coverage", "FY2025")["value"] == "4.74"
    assert _row(result, "interest_coverage", "FY2023")["value"] == "9.97"
    assert _row(result, "net_debt_balance_sheet_millions", "2025-12-31")["value"] == "54024"
    assert _row(result, "net_debt_balance_sheet_millions", "2026-06-30")["value"] == "44743"
    assert _row(result, "net_debt_balance_sheet_millions", "2026-09-30")["value"] == "48486"


def test_debt_note_gap_matches_other_financing_obligations():
    result = reconcile()
    assert _row(result, "debt_note_minus_balance_sheet_lines_millions", "2025-12-31")["value"] == "708"
    assert _row(result, "debt_note_minus_balance_sheet_lines_millions", "2024-12-31")["value"] == "724"


def test_attributable_earnings_identity():
    result = reconcile()
    assert _row(result, "attributable_earnings_identity_millions", "FY2025")["value"] == "12056"
    assert _row(result, "attributable_earnings_identity_millions", "FY2024")["value"] == "14405"
    assert _row(result, "attributable_earnings_identity_millions", "FY2023")["value"] == "22381"


def test_q3_2026_release_ratios_and_xbrl_gap():
    result = reconcile()
    assert _row(result, "operating_margin_percent", "Q3 2026")["value"] == "5.8"
    assert _row(result, "medical_care_ratio_percent", "Q3 2026")["value"] == "88.4"
    assert _row(result, "operating_margin_percent", "Q3 2025")["value"] == "3.8"
    assert _row(result, "operating_margin_percent", "Q1 2025")["value"] == "8.3"
    assert _row(result, "operating_margin_percent", "Q2 2025")["value"] == "4.6"
    assert _row(result, "free_cash_flow_millions", "9M 2026")["value"] == "22666"
    assert _row(result, "implied_quarter_cfo_millions", "Q3 2026")["value"] == "5123"
    names = {row["name"] for row in result["expected_differences"]}
    assert "q3_2026_absent_from_companyfacts" in names


def test_market_quote_drawdown_is_recomputed_not_hardcoded_in_the_module():
    result = reconcile()
    quote = result["market_quote"]
    assert quote["label"] == "MARKET_QUOTE"
    assert Decimal(quote["drawdown_peak_to_trough_percent"]) == Decimal("-61.4")
    assert Decimal(quote["change_peak_to_latest_percent"]) == Decimal("-34.8")
    assert quote["source_url"].startswith("https://query1.finance.yahoo.com/")
