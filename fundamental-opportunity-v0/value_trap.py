"""
Value Trap Detector — §3.6.2
Per FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)

5-question check triggered when valuation is "Unusually Cheap" (-2σ below own history).
"""

from fixtures import MACRO_REGIME


def is_unusually_cheap(company: dict) -> bool:
    """§3.6.2: Unusually Cheap = P/E < (5Y avg − 2σ).

    Requires `pe_5y_stddev` in the data. Without σ the trigger cannot be
    asserted (returns False) — no proxy threshold is invented (FD #53,
    audit C-02 code-to-spec)."""
    pe_ttm = company.get("pe_ttm", 0)
    pe_5y = company.get("pe_5y_avg", pe_ttm)
    sd = company.get("pe_5y_stddev")
    if not pe_ttm or not pe_5y or sd is None:
        return False  # insufficient data — honest, no proxy
    return pe_ttm < pe_5y - 2 * sd


def run_profit_rate_trend(company: dict) -> dict:
    """Q0: Check if profit rate (ROIC) is declining despite revenue growth.

    Per FD #43. Empirical signal: ROIC decline vs 5Y average,
    flagged when combined with positive revenue growth (Growth Trap pattern).

    Returns dict with trend analysis. Triggers when ROIC declines >=20% from 5Y avg
    while revenue is still growing (the dangerous combination).
    """
    roic_current = company.get("roic_current", 0)
    roic_5y = company.get("roic_5y", roic_current)
    revenue_growth = company.get("revenue_growth_3y", 0)
    invested_capital = company.get("invested_capital", 0)

    if roic_5y == 0 or roic_current == 0:
        return {"triggered": False, "reason": "Insufficient ROIC data"}

    decline_pct = (roic_5y - roic_current) / roic_5y
    revenue_growing = revenue_growth > 0.03

    triggered = decline_pct >= 0.20 and revenue_growing

    verdict = "NO_DECLINE"
    detail = f"ROIC stable: {roic_current:.1%} vs 5Y avg {roic_5y:.1%}"

    if triggered:
        verdict = "GROWTH_TRAP"
        detail = (
            f"⚠️ Profit Rate Decline: ROIC dropped {decline_pct:.0%} from 5Y avg "
            f"({roic_5y:.1%} → {roic_current:.1%}) despite revenue growing "
            f"{revenue_growth:+.0%} 3Y CAGR. Invested capital: ${invested_capital:.0f}B. "
            f"Classic Growth Trap — adding capacity but earning less on each dollar invested."
        )
    elif decline_pct >= 0.10:
        verdict = "MODERATE_DECLINE"
        detail = (
            f"ROIC declining {decline_pct:.0%} ({roic_5y:.1%} → {roic_current:.1%}). "
            f"Revenue growth: {revenue_growth:+.0%}. Monitor closely."
        )

    return {
        "triggered": triggered,
        "verdict": verdict,
        "roic_current": roic_current,
        "roic_5y": roic_5y,
        "decline_pct": decline_pct,
        "revenue_growth_3y": revenue_growth,
        "invested_capital": invested_capital,
        "detail": detail,
    }


def run_value_trap_check(company: dict, moat_assessment: dict) -> dict:
    """Run the 5-question Value Trap check.

    Returns scored assessment with verdict.
    """
    q1 = _check_earnings_growth(company)
    q2 = _check_industry_health(company)
    q3 = _check_moat_intact(moat_assessment)
    q4 = _check_management(company)
    q5 = _check_cheap_reason(q1, q2, q3, q4)

    questions = [q1, q2, q3, q4, q5]
    score = sum(1 for q in questions if q["pass"])

    verdict_map = {
        5: ("NOT_A_TRAP", "🟢 Genuinely cheap — business intact. Add to 'Cheap & Quality' watchlist."),
        # FD #53 (spec §3.6.2): 3–4 = mixed — deeper research required, NOT not-a-trap
        4: ("MIXED", "🟡 Mixed signals — 4/5 checks pass but not conclusive. Deeper research required."),
        3: ("MIXED", "🟡 Mixed signals — some concerns but not trap-level. Deeper research needed."),
        2: ("SUSPECT", "🔴 Likely value trap — structural problems masked by low multiple. Do not add."),
        1: ("TRAP", "🔴 Likely value trap — structural problems masked by low multiple. Do not add."),
        0: ("DEFINITE_TRAP", "🔴 Definite value trap — cheap for obvious, terminal reasons. Archive."),
    }
    verdict, action = verdict_map.get(score, ("UNKNOWN", "Manual review required."))

    return {
        "triggered": True,
        "score": score,
        "max_score": 5,
        "verdict": verdict,
        "action": action,
        "questions": questions,
        "narrative": _build_trap_narrative(company, score, verdict, action, questions),
    }


def _check_earnings_growth(company: dict) -> dict:
    """Q1: Are earnings still growing?"""
    rev_growth = company.get("revenue_growth_3y", 0)
    eps_surprise = company.get("surprise_magnitude_pct", 0)

    # Pass if revenue growing AND not missing earnings badly
    passes = rev_growth > 0.03 and eps_surprise > -10

    return {
        "number": 1,
        "question": "Earnings still growing?",
        "pass": passes,
        "detail": f"Revenue 3Y CAGR: {rev_growth:+.0%}, Latest EPS surprise: {eps_surprise:+.1f}%",
        "icon": "✅" if passes else "❌",
    }


def _check_industry_health(company: dict) -> dict:
    """Q2: Is the industry growing or declining?"""
    sector = company.get("sector", "Unknown")
    implication = MACRO_REGIME["sector_implications"].get(sector, "Unknown")

    # Pass if sector isn't clearly in decline
    passes = "headwind" not in implication.lower() or "defensive" in implication.lower()

    return {
        "number": 2,
        "question": "Industry growing or declining?",
        "pass": passes,
        "detail": f"Sector: {sector} — {implication}",
        "icon": "✅" if passes else "❌",
    }


def _check_moat_intact(moat: dict) -> dict:
    """Q3: Is the moat intact or eroding?"""
    width = moat.get("width", "None")
    trend = moat.get("trend", "Stable")

    # Pass if moat is Wide or Narrow + Stable/Widening
    passes = width in ("Wide", "Narrow") and trend in ("Stable", "Widening")

    return {
        "number": 3,
        "question": "Moat intact or eroding?",
        "pass": passes,
        "detail": f"Moat: {width} width, trend: {trend}",
        "icon": "✅" if passes else "❌",
    }


def _check_management(company: dict) -> dict:
    """Q4: Is management credible?"""
    credibility = company.get("management_credibility", "UNKNOWN")
    ceo_tenure = company.get("ceo_tenure_years", 0)
    cfo_turnover = company.get("cfo_turnover_3y", 0)

    # Pass if management credible OR new CEO with <1 CFO turnover
    passes = credibility == "HIGH" or (ceo_tenure < 3 and cfo_turnover <= 1)

    return {
        "number": 4,
        "question": "Management credible?",
        "pass": passes,
        "detail": f"Credibility: {credibility}, CEO tenure: {ceo_tenure}y, CFO turnover (3y): {cfo_turnover}",
        "icon": "✅" if passes else "❌",
    }


def _check_cheap_reason(q1, q2, q3, q4) -> dict:
    """Q5: After Q1-Q4 — is it cheap for a GOOD reason?"""
    # "Good reason" = at least 2 of Q1-Q4 fail (structural problems exist)
    fail_count = sum(1 for q in (q1, q2, q3, q4) if not q["pass"])

    # This is inverted: we PASS Q5 when it's NOT cheap for a good reason
    # i.e., the business is fine => genuinely cheap
    passes = fail_count < 2

    return {
        "number": 5,
        "question": "Cheap for a GOOD reason? (i.e., real problems exist)",
        "pass": passes,
        "detail": f"{fail_count}/4 structural problems found — "
                   f"{'Business problems explain the discount → VALUE TRAP' if not passes else 'No major structural issues → genuinely cheap'}",
        "icon": "✅" if passes else "❌",
    }


def _build_trap_narrative(company, score, verdict, action, questions):
    """Generate human-readable value trap narrative."""
    name = company.get("name", company.get("id", "?"))
    pe = company.get("pe_ttm", 0)
    pe_5y = company.get("pe_5y_avg", pe)

    lines = [
        f"**Unusually Cheap Flag:** {name} P/E {pe:.1f}x vs 5Y avg {pe_5y:.1f}x "
        f"(-{(1 - pe/pe_5y)*100:.0f}%)",
        "",
        "**Value Trap Check (5 questions):**",
    ]
    for q in questions:
        lines.append(f"- Q{q['number']}: {q['question']} → {q['icon']} {q['detail']}")

    lines.extend([
        "",
        f"**Verdict:** {verdict} ({score}/5)",
        f"**Action:** {action}",
    ])
    return "\n".join(lines)
