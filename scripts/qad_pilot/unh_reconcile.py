#!/usr/bin/env python3
"""Offline reconciliation for the UNH QAD research pilot.

Reads the committed SEC companyfacts subset and the filing-text anchors.
No network access. Recomputes operating margin, free cash flow, balance-sheet
net debt, interest coverage, and the medical care ratio, then compares those
results with the figures printed in the filings.

Free cash flow here means cash from operations minus purchases of property,
equipment and capitalized software. It does not subtract acquisitions,
dividends, or the Change Healthcare care-provider loans.

Net debt (balance sheet) means short-term borrowings and current maturities
plus long-term debt less current maturities, minus cash. That sum differs from
the debt-note total by the other financing obligations disclosed in the note.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "research" / "qad_pilot" / "unh"
SUBSET_PATH = DATA_DIR / "sec_companyfacts_subset.json"
ANCHORS_PATH = DATA_DIR / "filing_anchors.json"
QUOTES_PATH = DATA_DIR / "market_quotes.json"

MILLION = 1_000_000


def _d(value: int | str | Decimal) -> Decimal:
    return Decimal(str(value))


def _pct_1(numerator: int, denominator: int) -> Decimal:
    return (_d(numerator) / _d(denominator) * Decimal(100)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )


def _ratio_2(numerator: int, denominator: int) -> Decimal:
    return (_d(numerator) / _d(denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _key(concept: str, start: str | None, end: str) -> tuple:
    return (concept, start, end)


def _index_facts(subset: dict) -> dict[tuple, dict]:
    indexed: dict[tuple, dict] = {}
    for fact in subset["facts"]:
        key = _key(fact["concept"], fact.get("start"), fact["end"])
        if key in indexed:
            raise ValueError(f"duplicate fact in subset: {key}")
        indexed[key] = fact
    return indexed


def _millions(fact: dict) -> int:
    if fact["val"] % MILLION != 0:
        raise ValueError(f"{fact['concept']} {fact['end']} is not a whole number of millions")
    return fact["val"] // MILLION


def reconcile(
    subset_path: Path = SUBSET_PATH,
    anchors_path: Path = ANCHORS_PATH,
    quotes_path: Path = QUOTES_PATH,
) -> dict:
    """Return calculations, expected differences, and unexpected mismatches."""
    subset = _load(subset_path)
    anchors = _load(anchors_path)
    quotes = _load(quotes_path)
    facts = _index_facts(subset)
    mismatches: list[str] = []

    if len(anchors["xbrl_anchors"]) != len(subset["facts"]):
        mismatches.append(
            f"anchor count {len(anchors['xbrl_anchors'])} != subset facts {len(subset['facts'])}"
        )

    for anchor in anchors["xbrl_anchors"]:
        key = _key(anchor["concept"], anchor.get("start"), anchor["end"])
        fact = facts.get(key)
        if fact is None:
            mismatches.append(f"anchor missing from subset: {key}")
            continue
        if fact["val"] != anchor["millions"] * MILLION:
            mismatches.append(
                f"XBRL/filing mismatch {key}: xbrl={fact['val']} filing_millions={anchor['millions']}"
            )
        if fact["accn"] != anchor["accn"] or fact["filed"] != anchor["filed"]:
            mismatches.append(f"provenance mismatch {key}")

    def fact_m(concept: str, end: str, start: str | None) -> int:
        fact = facts[_key(concept, start, end)]
        return _millions(fact)

    calculations: list[dict] = []

    def add_calc(name: str, period: str, value: str, formula: str, label: str, inputs: dict) -> None:
        calculations.append(
            {
                "name": name,
                "period": period,
                "value": value,
                "formula": formula,
                "label": label,
                "inputs_millions": inputs,
            }
        )

    # Operating margin, MCR, FCF, coverage for the three fiscal years in the 10-K.
    for year, start, end in (
        (2023, "2023-01-01", "2023-12-31"),
        (2024, "2024-01-01", "2024-12-31"),
        (2025, "2025-01-01", "2025-12-31"),
    ):
        revenue = fact_m("Revenues", end, start)
        efo = fact_m("OperatingIncomeLoss", end, start)
        cfo = fact_m("NetCashProvidedByUsedInOperatingActivities", end, start)
        capex = fact_m("PaymentsToAcquirePropertyPlantAndEquipment", end, start)
        interest = fact_m("InterestExpense", end, start)
        premiums = fact_m("PremiumsEarnedNet", end, start)
        medical = fact_m("PolicyholderBenefitsAndClaimsIncurredNet", end, start)
        profit = fact_m("ProfitLoss", end, start)
        nci = fact_m("NetIncomeLossAttributableToNoncontrollingInterest", end, start)
        attributable = fact_m("NetIncomeLoss", end, start)
        period = f"FY{year}"
        add_calc(
            "operating_margin_percent",
            period,
            str(_pct_1(efo, revenue)),
            "OperatingIncomeLoss / Revenues",
            "INFERRED",
            {"earnings_from_operations": efo, "revenues": revenue},
        )
        add_calc(
            "free_cash_flow_millions",
            period,
            str(cfo - capex),
            "CFO - purchases of property, equipment and capitalized software",
            "INFERRED",
            {"cfo": cfo, "capex": capex},
        )
        add_calc(
            "interest_coverage",
            period,
            str(_ratio_2(efo, interest)),
            "OperatingIncomeLoss / InterestExpense",
            "INFERRED",
            {"earnings_from_operations": efo, "interest_expense": interest},
        )
        add_calc(
            "medical_care_ratio_percent",
            period,
            str(_pct_1(medical, premiums)),
            "medical costs / premium revenue",
            "INFERRED",
            {"medical_costs": medical, "premiums": premiums},
        )
        if profit - nci != attributable:
            mismatches.append(
                f"FY{year} ProfitLoss - NCI != NetIncomeLoss ({profit} - {nci} != {attributable})"
            )
        add_calc(
            "attributable_earnings_identity_millions",
            period,
            str(profit - nci),
            "ProfitLoss - NetIncomeLossAttributableToNoncontrollingInterest",
            "INFERRED",
            {"profit_loss": profit, "nci": nci, "net_income_loss_xbrl": attributable},
        )

    for row in anchors["reported_ratios_percent"]:
        if row["name"] == "operating_margin":
            got = _pct_1(
                fact_m("OperatingIncomeLoss", row["end"], row["start"]),
                fact_m("Revenues", row["end"], row["start"]),
            )
        elif row["name"] == "medical_care_ratio":
            got = _pct_1(
                fact_m("PolicyholderBenefitsAndClaimsIncurredNet", row["end"], row["start"]),
                fact_m("PremiumsEarnedNet", row["end"], row["start"]),
            )
        else:
            mismatches.append(f"unknown reported ratio {row['name']}")
            continue
        if got != Decimal(row["reported"]):
            mismatches.append(
                f"{row['name']} {row['end']} recomputed {got} != reported {row['reported']}"
            )

    # Balance-sheet net debt and the debt-note gap.
    expected_gap = {row["end"]: row["millions"] for row in anchors["other_financing_obligations_millions"]}
    for end in ("2024-12-31", "2025-12-31"):
        cash = fact_m("CashAndCashEquivalentsAtCarryingValue", end, None)
        short = fact_m("DebtCurrent", end, None)
        long = fact_m("LongTermDebtNoncurrent", end, None)
        combined = fact_m("DebtLongtermAndShorttermCombinedAmount", end, None)
        net_debt = short + long - cash
        gap = short + long - combined
        add_calc(
            "net_debt_balance_sheet_millions",
            end,
            str(net_debt),
            "DebtCurrent + LongTermDebtNoncurrent - cash",
            "INFERRED",
            {"short_term_and_current": short, "long_term_debt": long, "cash": cash},
        )
        add_calc(
            "debt_note_minus_balance_sheet_lines_millions",
            end,
            str(gap),
            "(DebtCurrent + LongTermDebtNoncurrent) - DebtLongtermAndShorttermCombinedAmount",
            "INFERRED",
            {"balance_sheet_debt": short + long, "debt_note_total": combined},
        )
        if gap != expected_gap[end]:
            mismatches.append(
                f"debt gap at {end} is {gap}, debt note other financing obligations {expected_gap[end]}"
            )

    # Q2 and six-month 2026 from the 10-Q.
    q_rev = fact_m("Revenues", "2026-06-30", "2026-04-01")
    q_efo = fact_m("OperatingIncomeLoss", "2026-06-30", "2026-04-01")
    q_int = fact_m("InterestExpense", "2026-06-30", "2026-04-01")
    add_calc(
        "operating_margin_percent",
        "Q2 2026",
        str(_pct_1(q_efo, q_rev)),
        "OperatingIncomeLoss / Revenues",
        "INFERRED",
        {"earnings_from_operations": q_efo, "revenues": q_rev},
    )
    add_calc(
        "interest_coverage",
        "Q2 2026",
        str(_ratio_2(q_efo, q_int)),
        "OperatingIncomeLoss / InterestExpense",
        "INFERRED",
        {"earnings_from_operations": q_efo, "interest_expense": q_int},
    )
    h_rev = fact_m("Revenues", "2026-06-30", "2026-01-01")
    h_efo = fact_m("OperatingIncomeLoss", "2026-06-30", "2026-01-01")
    h_int = fact_m("InterestExpense", "2026-06-30", "2026-01-01")
    h_cfo = fact_m("NetCashProvidedByUsedInOperatingActivities", "2026-06-30", "2026-01-01")
    h_capex = fact_m("PaymentsToAcquirePropertyPlantAndEquipment", "2026-06-30", "2026-01-01")
    add_calc(
        "operating_margin_percent",
        "6M 2026",
        str(_pct_1(h_efo, h_rev)),
        "OperatingIncomeLoss / Revenues",
        "INFERRED",
        {"earnings_from_operations": h_efo, "revenues": h_rev},
    )
    add_calc(
        "free_cash_flow_millions",
        "6M 2026",
        str(h_cfo - h_capex),
        "CFO - purchases of property, equipment and capitalized software",
        "INFERRED",
        {"cfo": h_cfo, "capex": h_capex},
    )
    add_calc(
        "interest_coverage",
        "6M 2026",
        str(_ratio_2(h_efo, h_int)),
        "OperatingIncomeLoss / InterestExpense",
        "INFERRED",
        {"earnings_from_operations": h_efo, "interest_expense": h_int},
    )
    cash_q2 = fact_m("CashAndCashEquivalentsAtCarryingValue", "2026-06-30", None)
    st_q2 = fact_m("DebtCurrent", "2026-06-30", None)
    lt_q2 = fact_m("LongTermDebtNoncurrent", "2026-06-30", None)
    add_calc(
        "net_debt_balance_sheet_millions",
        "2026-06-30",
        str(st_q2 + lt_q2 - cash_q2),
        "DebtCurrent + LongTermDebtNoncurrent - cash",
        "INFERRED",
        {"short_term_and_current": st_q2, "long_term_debt": lt_q2, "cash": cash_q2},
    )

    # Q1 2025 still had an operating margin near the pre-dislocation band.
    # Q2 2025 is where the quarterly margin broke. Both are in the cached subset.
    for label, end, start in (
        ("Q1 2025", "2025-03-31", "2025-01-01"),
        ("Q2 2025", "2025-06-30", "2025-04-01"),
    ):
        q_rev_y = fact_m("Revenues", end, start)
        q_efo_y = fact_m("OperatingIncomeLoss", end, start)
        add_calc(
            "operating_margin_percent",
            label,
            str(_pct_1(q_efo_y, q_rev_y)),
            "OperatingIncomeLoss / Revenues",
            "INFERRED",
            {"earnings_from_operations": q_efo_y, "revenues": q_rev_y},
        )
    # Q3 2025 operating margin from the 10-Q (medical costs for that quarter are not in the subset).
    add_calc(
        "operating_margin_percent",
        "Q3 2025",
        str(
            _pct_1(
                fact_m("OperatingIncomeLoss", "2025-09-30", "2025-07-01"),
                fact_m("Revenues", "2025-09-30", "2025-07-01"),
            )
        ),
        "OperatingIncomeLoss / Revenues",
        "INFERRED",
        {
            "earnings_from_operations": fact_m("OperatingIncomeLoss", "2025-09-30", "2025-07-01"),
            "revenues": fact_m("Revenues", "2025-09-30", "2025-07-01"),
        },
    )

    release = anchors["earnings_release_q3_2026_not_in_companyfacts"]
    if release["in_companyfacts_as_of_retrieval"] is not False:
        mismatches.append("Q3 2026 was expected to be absent from companyfacts")
    if any(fact["end"] == "2026-09-30" for fact in subset["facts"]):
        mismatches.append("subset unexpectedly contains a 2026-09-30 fact")
    fig = release["figures_millions"]
    # Prior-year column of the earnings release must match the Q3 2025 10-Q XBRL.
    if fig["revenues_q3_2025"] != fact_m("Revenues", "2025-09-30", "2025-07-01"):
        mismatches.append("Q3 2025 revenue in the Oct 2026 release != Q3 2025 10-Q XBRL")
    if fig["earnings_from_operations_q3_2025"] != fact_m("OperatingIncomeLoss", "2025-09-30", "2025-07-01"):
        mismatches.append("Q3 2025 operating earnings in the Oct 2026 release != Q3 2025 10-Q XBRL")
    # Comparative debt lines in the release must match the FY2025 10-K.
    if fig["short_term_borrowings_and_current_maturities_2025_12_31_comparative"] != fact_m(
        "DebtCurrent", "2025-12-31", None
    ):
        mismatches.append("earnings-release comparative short-term debt != FY2025 10-K")
    if fig["long_term_debt_less_current_2025_12_31_comparative"] != fact_m(
        "LongTermDebtNoncurrent", "2025-12-31", None
    ):
        mismatches.append("earnings-release comparative long-term debt != FY2025 10-K")

    q3_margin = _pct_1(fig["earnings_from_operations_q3_2026"], fig["revenues_q3_2026"])
    q3_2025_margin = _pct_1(
        fact_m("OperatingIncomeLoss", "2025-09-30", "2025-07-01"),
        fact_m("Revenues", "2025-09-30", "2025-07-01"),
    )
    q3_mcr = _pct_1(fig["medical_costs_q3_2026"], fig["premiums_q3_2026"])
    q3_2025_mcr = _pct_1(fig["medical_costs_q3_2025"], fig["premiums_q3_2025"])
    ratios = release["reported_ratios_percent"]
    if q3_margin != Decimal(ratios["operating_margin_q3_2026_earnings_by_business_table"]):
        mismatches.append(f"Q3 2026 operating margin {q3_margin} != release table")
    if q3_2025_margin != Decimal(ratios["operating_margin_q3_2025_earnings_by_business_table"]):
        mismatches.append(f"Q3 2025 operating margin {q3_2025_margin} != release table")
    if q3_mcr != Decimal(ratios["medical_care_ratio_q3_2026"]):
        mismatches.append(f"Q3 2026 MCR {q3_mcr} != release")
    if q3_2025_mcr != Decimal(ratios["medical_care_ratio_q3_2025"]):
        mismatches.append(f"Q3 2025 MCR {q3_2025_mcr} != release")
    segment_checks = (
        ("unitedhealthcare_earnings_from_operations_q3_2026", "unitedhealthcare_revenues_q3_2026", "3.3"),
        ("optum_earnings_from_operations_q3_2026", "optum_revenues_q3_2026", "5.6"),
        ("optum_health_earnings_from_operations_q3_2026", "optum_health_revenues_q3_2026", "3.2"),
        ("optum_health_earnings_from_operations_q3_2025", "optum_health_revenues_q3_2025", "0.2"),
    )
    for numer_key, denom_key, reported in segment_checks:
        got = _pct_1(fig[numer_key], fig[denom_key])
        if got != Decimal(reported):
            mismatches.append(f"{numer_key} margin {got} != release {reported}")
    add_calc(
        "operating_margin_percent",
        "Q3 2026",
        str(q3_margin),
        "earnings from operations / total revenues, earnings release",
        "INFERRED",
        {
            "earnings_from_operations": fig["earnings_from_operations_q3_2026"],
            "revenues": fig["revenues_q3_2026"],
        },
    )
    add_calc(
        "medical_care_ratio_percent",
        "Q3 2026",
        str(q3_mcr),
        "medical costs / premiums, earnings release",
        "INFERRED",
        {"medical_costs": fig["medical_costs_q3_2026"], "premiums": fig["premiums_q3_2026"]},
    )
    fcf_9m = fig["cfo_9m_2026"] - fig["capex_ppe_and_software_9m_2026"]
    add_calc(
        "free_cash_flow_millions",
        "9M 2026",
        str(fcf_9m),
        "9M CFO - 9M purchases of property, equipment and capitalized software, earnings release",
        "INFERRED",
        {"cfo": fig["cfo_9m_2026"], "capex": fig["capex_ppe_and_software_9m_2026"]},
    )
    implied_q3_cfo = fig["cfo_9m_2026"] - h_cfo
    add_calc(
        "implied_quarter_cfo_millions",
        "Q3 2026",
        str(implied_q3_cfo),
        "9M earnings-release CFO - 6M XBRL CFO",
        "INFERRED",
        {"cfo_9m_release": fig["cfo_9m_2026"], "cfo_6m_xbrl": h_cfo},
    )
    net_debt_q3 = (
        fig["short_term_borrowings_and_current_maturities_2026_09_30"]
        + fig["long_term_debt_less_current_2026_09_30"]
        - fig["cash_2026_09_30"]
    )
    add_calc(
        "net_debt_balance_sheet_millions",
        "2026-09-30",
        str(net_debt_q3),
        "short-term borrowings and current maturities + long-term debt less current - cash, earnings release",
        "INFERRED",
        {
            "short_term_and_current": fig["short_term_borrowings_and_current_maturities_2026_09_30"],
            "long_term_debt": fig["long_term_debt_less_current_2026_09_30"],
            "cash": fig["cash_2026_09_30"],
        },
    )

    points = {p["role"]: p for p in quotes["points"]}
    peak = Decimal(str(points["2024_weekly_high_in_series"]["close"]))
    trough = Decimal(str(points["trough_after_that_high"]["close"]))
    last = Decimal(str(points["latest_weekly_bar_at_retrieval"]["close"]))
    drawdown = ((trough / peak) - 1) * 100
    from_peak = ((last / peak) - 1) * 100
    market = {
        "label": "MARKET_QUOTE",
        "peak_close": str(peak),
        "trough_close": str(trough),
        "latest_close": str(last),
        "drawdown_peak_to_trough_percent": str(drawdown.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
        "change_peak_to_latest_percent": str(from_peak.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
        "source_url": quotes["source_url"],
        "retrieved_at_utc": quotes["retrieved_at_utc"],
    }

    return {
        "issuer": subset["issuer"],
        "ticker": subset["ticker"],
        "cik": subset["cik"],
        "companyfacts_retrieved_at_utc": subset["retrieved_at_utc"],
        "companyfacts_url": subset["source_url"],
        "calculations": calculations,
        "expected_differences": [
            {
                "name": "balance_sheet_debt_vs_debt_note",
                "explanation": (
                    "DebtCurrent + LongTermDebtNoncurrent exceeds "
                    "DebtLongtermAndShorttermCombinedAmount by the other financing "
                    "obligations disclosed in the FY2025 10-K debt note."
                ),
                "amounts_millions": expected_gap,
            },
            {
                "name": "xbrl_netincomeloss_is_attributable",
                "explanation": (
                    "us-gaap NetIncomeLoss matches net earnings attributable to "
                    "UnitedHealth Group common shareholders. Consolidated net earnings "
                    "are us-gaap ProfitLoss. ProfitLoss minus NCI equals NetIncomeLoss."
                ),
            },
            {
                "name": "q3_2026_absent_from_companyfacts",
                "explanation": release["reason"],
            },
        ],
        "market_quote": market,
        "mismatches": mismatches,
    }


def _calc_map(result: dict) -> dict[tuple, dict]:
    return {(row["name"], row["period"]): row for row in result["calculations"]}


def main(argv: list[str] | None = None) -> int:
    result = reconcile()
    payload = {
        "ticker": result["ticker"],
        "mismatches": result["mismatches"],
        "calculations": result["calculations"],
        "market_quote": result["market_quote"],
        "expected_differences": [row["name"] for row in result["expected_differences"]],
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not result["mismatches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
