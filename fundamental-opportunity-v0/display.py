"""
HTML Display Renderer — 13-Section Research Package
Reuses shared design tokens from alpha-momentum-v0 base.html pattern.

SYNTHETIC FIXTURES — NOT LIVE DATA.
"""

import json
import os
from datetime import datetime


def render_research_package(pkg: dict) -> str:
    """Render a single Research Package as an HTML card."""
    c = pkg  # shorthand
    moat = c["company_assessment"]["moat"]
    eq = c["earnings_trajectory"]
    val = c["valuation_context"]
    conv = c["conviction"]

    # ── Moat type badges ──
    moat_badges = "".join(
        f'<span class="moat-type {t["strength"].lower()}">{t["type"]} ({t["strength"]})</span>'
        for t in moat["types"]
    ) if moat["types"] else '<span class="moat-type none">No Moat</span>'

    # ── Value Trap section ──
    vt_html = ""
    if val.get("unusually_cheap") and val["value_trap"].get("triggered"):
        vt = val["value_trap"]
        vt_html = f"""
        <div class="section value-trap">
            <h3>⚠️ Value Trap Detector — Flagged as Unusually Cheap</h3>
            <div class="vt-score vt-{vt['verdict'].lower()}">
                Score: {vt['score']}/5 — {vt['action']}
            </div>
            <div class="vt-questions">
                {"".join(f'<div class="vt-q {"pass" if q["pass"] else "fail"}">{q["icon"]} Q{q["number"]}: {q["detail"]}</div>' for q in vt["questions"])}
            </div>
        </div>"""

    # ── Independent Challenge ──
    challenge_items = "".join(f"<li>{ch}</li>" for ch in c["independent_challenge"])

    # ── Conviction bar ──
    conv_pct = {"Maximum": 100, "High": 75, "Moderate": 50, "Low": 25}.get(conv["level"], 50)

    return f"""
    <div class="research-package" id="pkg-{c['id']}">
        <div class="rp-header">
            <h2>{c['name']} <span class="ticker">({c['id']})</span></h2>
            <div class="rp-meta">
                <span class="lifecycle badge">{c['thesis_lifecycle']}</span>
                <span class="conviction badge conv-{conv['level'].lower()}">Conviction: {conv['level']}</span>
            </div>
        </div>

        <div class="conviction-bar">
            <div class="conv-fill" style="width:{conv_pct}%"></div>
        </div>
        <p class="conv-rationale">{conv['rationale']}</p>

        <!-- §1: Thesis Summary -->
        <div class="section">
            <h3>📋 Thesis Summary</h3>
            <p>{c['thesis_summary']}</p>
        </div>

        <!-- §6: Company Assessment — Moat -->
        <div class="section moat-section">
            <h3>🏰 Moat Assessment</h3>
            <div class="moat-grid">
                <div class="moat-dim">
                    <span class="dim-label">Width</span>
                    <span class="dim-value width-{moat['width'].lower()}">{moat['width']}</span>
                </div>
                <div class="moat-dim">
                    <span class="dim-label">Depth</span>
                    <span class="dim-value depth-{moat['depth'].lower()}">{moat['depth']}</span>
                </div>
                <div class="moat-dim">
                    <span class="dim-label">Trend</span>
                    <span class="dim-value trend-{moat['trend'].lower()}">{moat['trend']}</span>
                </div>
            </div>
            <div class="moat-badges">{moat_badges}</div>
            <p class="moat-narrative">{c['company_assessment']['moat_narrative']}</p>
        </div>

        {vt_html}

        <!-- §7: Earnings Trajectory -->
        <div class="section earnings-section">
            <h3>📊 Earnings Quality</h3>
            <div class="eq-rating eq-{eq['rating'].lower()}">Quality: {eq['rating']}</div>
            <p>{eq['narrative']}</p>
            <div class="eq-details">
                <span>Surprise: {eq['surprise_direction']} ({eq['surprise_magnitude_pct']:+.1f}%)</span>
                <span>Revenue Quality: {eq['revenue_quality']}</span>
                <span>Margin Quality: {eq['margin_quality']}</span>
                <span>FCF Conversion: {eq['fcf_conversion']:.2f}x</span>
                <span>Guidance: {eq['guidance_direction']}</span>
            </div>
        </div>

        <!-- §8: Valuation Context -->
        <div class="section valuation-section">
            <h3>💰 Valuation Context</h3>
            <table class="val-table">
                <tr><td>P/E (TTM)</td><td>{val['pe_ttm']:.1f}x</td><td>vs 5Y: {val['pe_5y_avg']:.1f}x</td></tr>
                <tr><td>EV/EBITDA</td><td>{val['ev_ebitda']:.1f}x</td><td>vs Industry: {val['ev_ebitda_industry']:.1f}x</td></tr>
                <tr><td>FCF Yield</td><td>{val['fcf_yield']:.1%}</td><td></td></tr>
                <tr><td>Bull / Base / Bear</td><td colspan="2">${val['scenario_bull']} / ${val['scenario_base']} / ${val['scenario_bear']} (Current: ${val['current_price']})</td></tr>
            </table>
        </div>

        <!-- §10: Independent Challenge -->
        <div class="section challenge-section">
            <h3>⚔️ Independent Challenge</h3>
            <ul>{challenge_items}</ul>
        </div>

        <!-- §11-12: Evidence -->
        <div class="section evidence-section">
            <h3>📎 Evidence</h3>
            <div class="evidence-grid">
                <div class="evidence-col supporting">
                    <h4>✅ Supporting</h4>
                    {"".join(f'<div class="ev-item">{e}</div>' for e in c['supporting_evidence'])}
                </div>
                <div class="evidence-col contradicting">
                    <h4>❌ Contradicting</h4>
                    {"".join(f'<div class="ev-item">{e}</div>' for e in c['contradicting_evidence'])}
                </div>
            </div>
        </div>

        <!-- §9: Key Risks -->
        <div class="section risks-section">
            <h3>⚠️ Key Risks</h3>
            <ul>{"".join(f'<li>{r}</li>' for r in c['key_risks'])}</ul>
        </div>

        <!-- §13: Open Questions -->
        <div class="section questions-section">
            <h3>❓ Open Questions</h3>
            <ul>{"".join(f'<li>{q}</li>' for q in c['open_questions'])}</ul>
        </div>
    </div>"""


def render_full_report(packages: list[dict], json_path: str = None, source: str = "SYNTHETIC") -> str:
    """Render all Research Packages as a complete HTML page.

    Args:
        packages: List of Research Package dicts from pipeline.
        json_path: Optional path to save JSON output.
        source: Data source label — "SYNTHETIC" or "REAL EOD".
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    is_real = source == "REAL EOD"
    watermark_text = "REAL EOD — YAHOO FINANCE" if is_real else "SYNTHETIC — NOT LIVE DATA"
    version_label = "Phase 9 · FD #41" if is_real else "Phase 8 Spike · FD #40"
    disclaimer_text = (
        "REAL EOD DATA — YAHOO FINANCE. FOR V0 DEVELOPMENT ONLY. NOT INVESTMENT ADVICE.<br>"
        if is_real else
        "SYNTHETIC FIXTURES — FOR V0 TESTING ONLY. NOT LIVE DATA. NOT INVESTMENT ADVICE.<br>"
    )

    # Save JSON
    if json_path:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w") as f:
            json.dump(packages, f, indent=2, default=str)

    cards = "\n".join(render_research_package(pkg) for pkg in packages)

    # Summary stats
    wide_moats = sum(1 for p in packages if p["company_assessment"]["moat"]["width"] == "Wide")
    traps = sum(1 for p in packages
                if p["valuation_context"].get("value_trap", {}).get("verdict") in ("TRAP", "DEFINITE_TRAP", "SUSPECT"))
    cheap_quality = sum(1 for p in packages
                        if p["valuation_context"].get("value_trap", {}).get("verdict") == "NOT_A_TRAP")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fundamental & Opportunity — Research Packages</title>
<style>
    /* ── IIP Design Tokens ── */
    :root {{
        --bg: #f5f6f8;
        --card: #ffffff;
        --text: #1a1a2e;
        --muted: #6b7280;
        --mint: #10b981;
        --pink: #ec4899;
        --amber: #f59e0b;
        --blue: #3b82f6;
        --purple: #8b5cf6;
        --radius: 12px;
        --sidebar: #0f1117;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: var(--bg);
        color: var(--text);
        font-size: 14px;
        line-height: 1.6;
    }}
    .report-header {{
        background: var(--sidebar);
        color: #fff;
        padding: 24px 32px;
    }}
    .report-header h1 {{ font-size: 20px; font-weight: 700; }}
    .report-header .meta {{ font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px; }}
    .summary-bar {{
        display: flex;
        gap: 16px;
        padding: 16px 32px;
        background: #fff;
        border-bottom: 1px solid #e5e7eb;
    }}
    .summary-stat {{
        text-align: center;
        min-width: 100px;
    }}
    .summary-stat .stat-value {{ font-size: 24px; font-weight: 700; }}
    .summary-stat .stat-label {{ font-size: 11px; text-transform: uppercase; color: var(--muted); }}
    .stat-mint {{ color: var(--mint); }}
    .stat-pink {{ color: var(--pink); }}
    .stat-amber {{ color: var(--amber); }}

    .packages {{ padding: 24px 32px; display: flex; flex-direction: column; gap: 24px; }}
    .research-package {{
        background: var(--card);
        border-radius: var(--radius);
        padding: 28px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .rp-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }}
    .rp-header h2 {{ font-size: 18px; font-weight: 700; }}
    .ticker {{ color: var(--muted); font-weight: 500; font-size: 14px; }}
    .rp-meta {{ display: flex; gap: 8px; }}
    .badge {{
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }}
    .lifecycle {{ background: #dbeafe; color: #1e40af; }}
    .conviction {{ background: #d1fae5; color: #065f46; }}
    .conv-low {{ background: #fee2e2; color: #991b1b; }}
    .conv-moderate {{ background: #fef3c7; color: #92400e; }}

    .conviction-bar {{
        height: 6px;
        background: #e5e7eb;
        border-radius: 3px;
        margin-bottom: 8px;
    }}
    .conv-fill {{
        height: 100%;
        background: linear-gradient(90deg, var(--pink), var(--amber), var(--mint));
        border-radius: 3px;
    }}
    .conv-rationale {{ font-size: 12px; color: var(--muted); margin-bottom: 20px; }}

    .section {{ margin-bottom: 20px; }}
    .section h3 {{ font-size: 14px; font-weight: 600; margin-bottom: 8px; color: var(--text); }}
    .section p {{ font-size: 13px; color: var(--text); }}

    /* Moat */
    .moat-grid {{ display: flex; gap: 16px; margin-bottom: 12px; }}
    .moat-dim {{ text-align: center; }}
    .dim-label {{ display: block; font-size: 10px; text-transform: uppercase; color: var(--muted); }}
    .dim-value {{ display: block; font-size: 18px; font-weight: 700; }}
    .width-wide {{ color: var(--mint); }}
    .width-narrow {{ color: var(--amber); }}
    .width-none {{ color: var(--pink); }}
    .depth-deep {{ color: var(--mint); }}
    .depth-moderate {{ color: var(--amber); }}
    .depth-shallow {{ color: var(--pink); }}
    .trend-widening {{ color: var(--mint); }}
    .trend-stable {{ color: var(--blue); }}
    .trend-narrowing {{ color: var(--pink); }}

    .moat-badges {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }}
    .moat-type {{
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }}
    .moat-type.strong {{ background: #d1fae5; color: #065f46; }}
    .moat-type.moderate {{ background: #fef3c7; color: #92400e; }}
    .moat-type.weak {{ background: #fee2e2; color: #991b1b; }}
    .moat-type.none {{ background: #f3f4f6; color: var(--muted); }}

    /* Value Trap */
    .value-trap {{ background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; }}
    .vt-score {{ font-weight: 700; font-size: 14px; margin-bottom: 8px; }}
    .vt-not_a_trap {{ color: var(--mint); }}
    .vt-mixed {{ color: var(--amber); }}
    .vt-suspect, .vt-trap, .vt-definite_trap {{ color: var(--pink); }}
    .vt-questions {{ display: flex; flex-direction: column; gap: 4px; }}
    .vt-q {{ font-size: 12px; padding: 2px 0; }}
    .vt-q.pass {{ color: var(--mint); }}
    .vt-q.fail {{ color: var(--pink); }}

    /* Earnings */
    .eq-rating {{ font-weight: 700; font-size: 16px; margin-bottom: 4px; }}
    .eq-high {{ color: var(--mint); }}
    .eq-medium {{ color: var(--amber); }}
    .eq-low {{ color: var(--pink); }}
    .eq-cosmetic {{ color: var(--pink); text-decoration: line-through; }}
    .eq-details {{ display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px; color: var(--muted); margin-top: 8px; }}

    /* Valuation Table */
    .val-table {{ width: 100%; font-size: 13px; border-collapse: collapse; }}
    .val-table td {{ padding: 4px 12px 4px 0; }}
    .val-table td:first-child {{ font-weight: 600; color: var(--muted); width: 120px; }}

    /* Challenge & Risks */
    .challenge-section ul, .risks-section ul, .questions-section ul {{
        padding-left: 18px;
        font-size: 13px;
    }}
    .challenge-section li {{ color: var(--pink); }}
    .risks-section li {{ color: var(--amber); }}

    /* Evidence */
    .evidence-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .evidence-col h4 {{ font-size: 12px; text-transform: uppercase; margin-bottom: 6px; }}
    .supporting h4 {{ color: var(--mint); }}
    .contradicting h4 {{ color: var(--pink); }}
    .ev-item {{ font-size: 12px; color: var(--muted); padding: 2px 0; }}

    .disclaimer {{
        text-align: center;
        padding: 24px;
        font-size: 11px;
        color: var(--muted);
        border-top: 1px solid #e5e7eb;
        margin-top: 24px;
    }}

    .watermark {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 72px;
        font-weight: 900;
        color: rgba(0,0,0,0.03);
        pointer-events: none;
        z-index: 0;
    }}
</style>
</head>
<body>
<div class="watermark">{watermark_text}</div>

<div class="report-header">
    <h1>Fundamental & Opportunity Intelligence — Research Packages</h1>
    <div class="meta">Pipeline v0.2.0 · {now} · {version_label}</div>
</div>

<div class="summary-bar">
    <div class="summary-stat">
        <div class="stat-value">{len(packages)}</div>
        <div class="stat-label">Companies</div>
    </div>
    <div class="summary-stat">
        <div class="stat-value stat-mint">{wide_moats}</div>
        <div class="stat-label">Wide Moat</div>
    </div>
    <div class="summary-stat">
        <div class="stat-value stat-mint">{cheap_quality}</div>
        <div class="stat-label">Cheap & Quality</div>
    </div>
    <div class="summary-stat">
        <div class="stat-value stat-pink">{traps}</div>
        <div class="stat-label">Value Traps</div>
    </div>
</div>

<div class="packages">
    {cards}
</div>

<div class="disclaimer">
    {disclaimer_text}
    Fundamental & Opportunity Intelligence v0.2 · {version_label}
</div>

</body>
</html>"""


def render_cheap_quality_watchlist(packages: list[dict]) -> str:
    """Render the 'Cheap & Quality' watchlist as a separate summary card."""
    # Filter companies that passed Value Trap check
    cq = [p for p in packages
          if p["valuation_context"].get("value_trap", {}).get("verdict") == "NOT_A_TRAP"]

    if not cq:
        return "<p>No companies currently in 'Cheap & Quality' watchlist.</p>"

    rows = ""
    for p in cq:
        moat = p["company_assessment"]["moat"]
        val = p["valuation_context"]
        rows += f"""
        <tr>
            <td><strong>{p['name']}</strong> ({p['id']})</td>
            <td>{moat['width']} / {moat['depth']}</td>
            <td>P/E: {val['pe_ttm']:.1f}x vs 5Y: {val['pe_5y_avg']:.1f}x</td>
            <td>{p['conviction']['level']}</td>
        </tr>"""

    return f"""
    <div class="section">
        <h3>🟢 Cheap & Quality Watchlist</h3>
        <p class="muted">Companies that are unusually cheap vs own history AND passed Value Trap detection.</p>
        <table class="val-table">
            <thead><tr>
                <th>Company</th><th>Moat</th><th>Valuation</th><th>Conviction</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""
