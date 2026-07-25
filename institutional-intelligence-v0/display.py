"""
Institutional Intelligence V0 — Display Renderer
HTML + JSON output. Reuses IIP design tokens.

FD #42 · Phase 10 · 26 July 2026
"""

import json
import os
from datetime import datetime


def render_html(result: dict) -> str:
    """Render Institutional Intelligence results as HTML page."""
    signals = result.get("signals", [])
    summary = result.get("summary", {})
    meta = result.get("meta", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Top signals table
    top_rows = ""
    for s in signals[:20]:
        action_cls = s["action"].lower()
        conv_cls = s["conviction"].lower()
        score_clr = "#065f46" if s["signal_score"] >= 60 else ("#92400e" if s["signal_score"] >= 35 else "#991b1b")
        top_rows += f"""
        <tr>
            <td><strong>{s['filer_name']}</strong></td>
            <td><span class="badge cat-{s.get('filer_category','unknown').lower().replace(' ','-')}">{s.get('filer_category','?')}</span></td>
            <td><strong>{s['ticker']}</strong></td>
            <td>{s['pct_of_portfolio']:.1f}%</td>
            <td><span class="conviction {conv_cls}">{s['conviction']}</span></td>
            <td><span class="action {action_cls}">{s['action']}</span></td>
            <td><span class="score" style="color:{score_clr}">{s['signal_score']}</span></td>
        </tr>"""

    # Ticker aggregate stats
    ticker_rows = ""
    ts = summary.get("ticker_stats", {})
    for ticker in sorted(ts.keys()):
        t = ts[ticker]
        ticker_rows += f"""
        <tr>
            <td><strong>{ticker}</strong></td>
            <td>{t['total_funds']}</td>
            <td>{t['buying_funds']}</td>
            <td>{t['selling_funds']}</td>
            <td><span class="conviction {t['aggregate_conviction'].lower()}">{t['aggregate_conviction']}</span></td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Institutional Intelligence — Phase 10</title>
<style>
    :root {{
        --bg: #f5f6f8; --card: #ffffff; --text: #1f2937; --muted: #6b7280;
        --mint: #059669; --pink: #dc2626; --amber: #d97706; --blue: #2563eb;
        --sidebar: #0f1117;
    }}
    body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); margin: 0; padding: 24px; color: var(--text); }}
    .header {{ margin-bottom: 24px; }}
    .header h1 {{ font-size: 24px; margin: 0 0 4px; }}
    .header .meta {{ font-size: 12px; color: var(--muted); }}
    .summary-bar {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .stat {{ background: var(--card); border-radius: 8px; padding: 16px 24px; min-width: 120px; }}
    .stat .value {{ font-size: 28px; font-weight: 700; }}
    .stat .label {{ font-size: 11px; text-transform: uppercase; color: var(--muted); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 8px; overflow: hidden; margin-bottom: 24px; }}
    th, td {{ padding: 10px 14px; text-align: left; font-size: 13px; border-bottom: 1px solid #f3f4f6; }}
    th {{ font-size: 11px; text-transform: uppercase; color: var(--muted); background: #f9fafb; }}
    .conviction {{ font-weight: 700; }}
    .conviction.maximum {{ color: var(--mint); }}
    .conviction.high {{ color: var(--mint); }}
    .conviction.moderate {{ color: var(--amber); }}
    .conviction.low {{ color: var(--pink); }}
    .conviction.minimal {{ color: var(--muted); }}
    .action {{ font-weight: 600; font-size: 11px; padding: 2px 8px; border-radius: 4px; }}
    .action.new, .action.add {{ background: #d1fae5; color: #065f46; }}
    .action.maintain {{ background: #e5e7eb; color: #374151; }}
    .action.reduce, .action.exit {{ background: #fee2e2; color: #991b1b; }}
    .badge {{ font-size: 10px; padding: 2px 6px; border-radius: 4px; }}
    .badge.cat-legendary {{ background:#fef3c7; color:#92400e; }}
    .badge.cat-tiger-cub {{ background:#dbeafe; color:#1e40af; }}
    .badge.cat-major-fund {{ background:#e5e7eb; color:#374151; }}
    .badge.cat-activist {{ background:#fce7f3; color:#9d174d; }}
    .badge.cat-specialist {{ background:#d1fae5; color:#065f46; }}
    .score {{ font-weight: 700; }}
    .disclaimer {{ font-size: 11px; color: var(--muted); text-align: center; margin-top: 32px; padding: 16px; border-top: 1px solid #e5e7eb; }}
    .watermark {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-30deg); font-size: 72px; font-weight: 900; color: rgba(0,0,0,0.03); pointer-events: none; z-index: 0; }}
</style>
</head>
<body>
<div class="watermark">{meta.get('data_source', 'SYNTHETIC')}</div>

<div class="header">
    <h1>🏛️ Institutional Intelligence</h1>
    <div class="meta">Pipeline v0.1.0 · {now} · Phase 10 · FD #42 · {meta.get('data_source', 'SYNTHETIC')}</div>
</div>

<div class="summary-bar">
    <div class="stat"><div class="value">{summary.get('total_funds_tracked', 0)}</div><div class="label">Funds Tracked</div></div>
    <div class="stat"><div class="value">{summary.get('total_signals', 0)}</div><div class="label">Signals</div></div>
    <div class="stat"><div class="value">{summary.get('total_filings', 0)}</div><div class="label">13F Filings</div></div>
</div>

<h2>🔝 Top Signals</h2>
<table>
    <thead><tr>
        <th>Fund</th><th>Category</th><th>Ticker</th><th>% of Portfolio</th><th>Conviction</th><th>Action</th><th>Score</th>
    </tr></thead>
    <tbody>{top_rows}</tbody>
</table>

<h2>📊 Ticker Aggregate</h2>
<table>
    <thead><tr>
        <th>Ticker</th><th>Funds Holding</th><th>Buying</th><th>Selling</th><th>Agg Conviction</th>
    </tr></thead>
    <tbody>{ticker_rows}</tbody>
</table>

<div class="disclaimer">
    SYNTHETIC 13F FIXTURES — FOR V0 TESTING ONLY. NOT LIVE DATA. NOT INVESTMENT ADVICE.<br>
    Institutional Intelligence v0.1 · FD #42 · Phase 10<br>
    13F data has ~45-day lag. Concentration is a proxy for conviction — not a guarantee of future performance.
</div>
</body>
</html>"""


def save_json(result: dict, path: str):
    """Save pipeline result as JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str, ensure_ascii=False)


def render_report(result: dict, json_path: str = None) -> str:
    """Full report: save JSON + return HTML."""
    if json_path:
        save_json(result, json_path)
    return render_html(result)
