"""
Close System Product Radar V0 — HTML Display Layer
Renders Product Radar table and Synthesis Cards using Jinja2.
Per CLOSE-SYSTEM-PRODUCT-RADAR.md §5.2 (Synthesis Template).
"""
import os, json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))

CONVICTION_CLASSES = {"High": "high", "Moderate": "moderate", "Low": "low"}
LAYER_LABELS = {
    "L1_macro": "1. Macro Economics",
    "L2_policy": "2. Government Policy",
    "L3_cost": "3. Cost Structure",
    "L4_supply_demand": "4. Supply/Demand",
    "L5_hidden": "5. Hidden Signals",
}

CSS = """
:root {
    --bg: #f5f6f8; --card-bg: #fff; --sidebar: #0f1117;
    --text: #1a1a2e; --muted: #6b7280;
    --positive: #10b981; --negative: #ec4899; --warning: #f59e0b;
    --border: #e5e7eb; --radius: 12px;
    --high: #10b981; --moderate: #f59e0b; --low: #6b7280;
    --max: #8b5cf6;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); }
.container { max-width: 1200px; margin: 0 auto; padding: 32px 24px; }
.header { margin-bottom: 32px; }
.header h1 { font-size: 28px; font-weight: 700; }
.header .meta { color: var(--muted); font-size: 13px; margin-top: 4px; }

/* ── Radar Table ── */
.radar-table { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--card-bg); border-radius: var(--radius); box-shadow: 0 1px 3px rgba(0,0,0,.06); overflow: hidden; }
.radar-table th { background: var(--sidebar); color: #fff; padding: 12px 16px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; text-align: left; }
.radar-table td { padding: 14px 16px; border-bottom: 1px solid var(--border); font-size: 14px; vertical-align: top; }
.radar-table tr:last-child td { border-bottom: none; }
.radar-table .ticker { font-weight: 700; font-size: 15px; }
.radar-table .name { color: var(--muted); font-size: 13px; }
.radar-table .price { font-weight: 600; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .03em; }
.badge-pass { background: #d1fae5; color: #065f46; }
.badge-fail { background: #fce7f3; color: #9d174d; }
.badge-high { background: #d1fae5; color: #065f46; }
.badge-moderate { background: #fef3c7; color: #92400e; }
.badge-low { background: #e5e7eb; color: #374151; }
.badge-max { background: #ede9fe; color: #5b21b6; }
.badge-none { background: #fee2e2; color: #991b1b; }

.discount-depth { font-weight: 600; }
.discount-depth.Maximum { color: var(--max); }
.discount-depth.Strong { color: var(--negative); }
.discount-depth.Moderate { color: var(--warning); }
.discount-depth.None { color: var(--low); }

.rec { font-weight: 600; font-size: 13px; }
.rec.Present { color: #065f46; }
.rec.Deep { color: #92400e; }
.rec.Add { color: #1e40af; }
.rec.Monitor { color: #6b7280; }

/* ── Section Cards ── */
.section { margin-top: 40px; }
.section-title { font-size: 20px; font-weight: 700; margin-bottom: 16px; }
.card { background: var(--card-bg); border-radius: var(--radius); box-shadow: 0 1px 3px rgba(0,0,0,.06); padding: 28px; margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.card-ticker { font-size: 22px; font-weight: 800; }
.card-name { font-size: 14px; color: var(--muted); }
.card-meta { text-align: right; font-size: 13px; color: var(--muted); }
.card-meta .conviction { font-size: 16px; font-weight: 700; }
.card-meta .conviction.High { color: var(--high); }
.card-meta .conviction.Moderate { color: var(--moderate); }
.card-meta .conviction.Low { color: var(--low); }

.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card-section h4 { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); margin-bottom: 8px; }
.card-section p, .card-section li { font-size: 14px; line-height: 1.6; }
.card-section ul { padding-left: 18px; }

/* ── Layer Table ── */
.layer-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 16px; }
.layer-table th { text-align: left; padding: 8px 12px; background: #f9fafb; font-weight: 600; color: var(--muted); border-bottom: 2px solid var(--border); }
.layer-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
.layer-table .signal-supporting { color: var(--positive); font-weight: 600; }
.layer-table .signal-neutral { color: var(--muted); }
.layer-table .signal-contradicting { color: var(--negative); font-weight: 600; }

/* ── Recommendation Banner ── */
.rec-banner { margin-top: 20px; padding: 16px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.rec-banner.Present { background: #d1fae5; color: #065f46; }
.rec-banner.Deep { background: #fef3c7; color: #92400e; }
.rec-banner.Add { background: #dbeafe; color: #1e40af; }
.rec-banner.Monitor { background: #f3f4f6; color: #6b7280; }
.rec-banner.Ineligible { background: #fee2e2; color: #991b1b; }

.summary-stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; margin-bottom: 32px; }
.stat-box { background: var(--card-bg); border-radius: var(--radius); padding: 16px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
.stat-box .stat-num { font-size: 28px; font-weight: 800; }
.stat-box .stat-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; margin-top: 4px; }
"""


def _build_layer_table(layers):
    """Build HTML rows for the 5-layer synthesis table."""
    html = ""
    for key, label in LAYER_LABELS.items():
        ldata = layers.get(key, {})
        signal = ldata.get("signal", "neutral")
        note = ldata.get("note", "")
        cls = f"signal-{signal}"
        emoji = {"supporting": "▲", "neutral": "—", "contradicting": "▼"}.get(signal, "—")
        html += f'<tr><td>{label}</td><td class="{cls}">{emoji} {signal.title()}</td><td>{note}</td></tr>\n'
    return html


def render_all(pipeline_result):
    """Render radar table HTML + individual synthesis cards + JSON."""
    products = pipeline_result.get("synthesized", [])
    radar = pipeline_result.get("radar", {})
    stages = pipeline_result.get("stages", [])

    # ── Radar Table ──
    table_rows = ""
    for p in products:
        rec = p["recommendation"]
        rec_cls = rec.split(" ")[0] if " " in rec else rec.split(" — ")[0] if " — " in rec else rec
        depth = p.get("discount_depth", "None")

        p1_cls = "badge-pass" if p.get("p1_pass") else "badge-fail"
        p2_cls = "badge-pass" if p.get("p2_pass") else "badge-fail"
        p3_cls = "badge-pass" if p.get("p3_pass") else "badge-fail"
        conv_cls = f"badge-{p['conviction'].lower()}"
        depth_cls = f"discount-depth {depth}" if depth != "None" else "discount-depth None"

        layer_dots = ""
        for i in range(p["layers_aligned"]):
            layer_dots += '<span style="color:var(--positive);font-weight:700;">●</span>'
        for i in range(p["layers_contradicting"]):
            layer_dots += '<span style="color:var(--negative);font-weight:700;">●</span>'
        for i in range(5 - p["layers_aligned"] - p["layers_contradicting"]):
            layer_dots += '<span style="color:var(--border);">●</span>'

        table_rows += f"""<tr>
            <td><span class="ticker">{p['ticker']}</span><br><span class="name">{p['name']}</span></td>
            <td>{p['category']}</td>
            <td class="price">${p.get('current_price', '—')}</td>
            <td><span class="{p1_cls}">{'✓' if p.get('p1_pass') else '✗'}</span> <span class="{p2_cls}">{'✓' if p.get('p2_pass') else '✗'}</span> <span class="{p3_cls}">{'✓' if p.get('p3_pass') else '✗'}</span></td>
            <td><span class="{depth_cls}">{depth}</span></td>
            <td>{layer_dots} <span class="badge {conv_cls}">{p['conviction']}</span></td>
            <td><span class="rec {rec_cls}">{rec}</span></td>
        </tr>"""

    # ── Summary Stats ──
    s6 = stages[-1] if stages else {}
    stats_html = f"""
    <div class="summary-stats">
        <div class="stat-box"><div class="stat-num">{s6.get('total_products', 0)}</div><div class="stat-label">Total Products</div></div>
        <div class="stat-box"><div class="stat-num" style="color:var(--positive)">{s6.get('eligible_for_radar', 0)}</div><div class="stat-label">Eligible</div></div>
        <div class="stat-box"><div class="stat-num" style="color:var(--high)">{s6.get('present_to_founder', 0)}</div><div class="stat-label">Present to Founder</div></div>
        <div class="stat-box"><div class="stat-num" style="color:var(--warning)">{s6.get('deep_research', 0)}</div><div class="stat-label">Deep Research</div></div>
        <div class="stat-box"><div class="stat-num" style="color:#1e40af">{s6.get('radar_watchlist', 0)}</div><div class="stat-label">Radar Watchlist</div></div>
        <div class="stat-box"><div class="stat-num" style="color:var(--muted)">{s6.get('monitor', 0)}</div><div class="stat-label">Monitor / Wait</div></div>
    </div>"""

    # ── Synthesis Cards ──
    cards_html = ""
    for p in products:
        rec_cls = p["recommendation"].split(" ")[0]
        if p["recommendation"] == "Monitor — Wait for Better Price":
            rec_cls = "Monitor"
        elif "Ineligible" in p["status"]:
            rec_cls = "Ineligible"

        layers_html = _build_layer_table(p.get("layers", {}))
        risks_html = "".join(f"<li>{r}</li>" for r in p.get("key_risks", []))

        # Discount detail
        dd = p.get("discount_detail", {})
        discount_items = ""
        for k, v in dd.items():
            if k not in ("signal",):
                discount_items += f"<li><strong>{k.replace('_', ' ').title()}:</strong> {v}</li>"

        # Demand detail
        dm = p.get("demand_detail", {})
        demand_items = ""
        for k, v in dm.items():
            demand_items += f"<li><strong>{k.replace('_', ' ').title()}:</strong> {v}</li>"

        cards_html += f"""<div class="card">
        <div class="card-header">
            <div>
                <div class="card-ticker">{p['ticker']} <span style="font-size:14px;color:var(--muted);">— {p['name']}</span></div>
                <div style="margin-top:4px;">
                    <span class="badge badge-{p['conviction'].lower()}">{p['conviction']} Conviction</span>
                    <span class="badge" style="margin-left:6px;">{p['category']}</span>
                    <span class="badge" style="margin-left:6px;">{p['status']}</span>
                </div>
            </div>
            <div class="card-meta">
                <div class="conviction {p['conviction']}">{p['layers_aligned']}/5 Layers Aligned</div>
                <div>${p.get('current_price', '—')} {p.get('currency', 'USD')}</div>
            </div>
        </div>

        <div class="card-grid">
            <div class="card-section">
                <h4>🎯 Discount Assessment (P2)</h4>
                <p><strong>Type:</strong> {p.get('discount_type', 'N/A')} · <strong>Depth:</strong> <span class="{depth_cls}">{p.get('discount_depth', 'N/A')}</span></p>
                {f'<p><strong>Target Entry:</strong> {p.get("target_discount_entry")}</p>' if p.get("target_discount_entry") else ''}
                <ul>{discount_items}</ul>
            </div>
            <div class="card-section">
                <h4>📊 Demand Assessment (P3)</h4>
                <p><strong>Type:</strong> {p.get('demand_type', 'N/A')}</p>
                <ul>{demand_items}</ul>
            </div>
        </div>

        <h4 style="margin-top:20px;">🔬 5-Layer Cross-Synthesis</h4>
        <table class="layer-table">
            <tr><th>Layer</th><th>Signal</th><th>Evidence</th></tr>
            {layers_html}
        </table>

        <h4 style="margin-top:20px;">⚠️ Key Risks</h4>
        <ul>{risks_html}</ul>

        <div class="rec-banner {rec_cls}">{p['recommendation']}: {p.get('recommendation_rationale', '')}</div>
        <div style="margin-top:8px;font-size:12px;color:var(--muted);">P1: {p.get('p1_rationale', '')[:200]}...</div>
    </div>"""

    # ── Full HTML page ──
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Close System Product Radar — {pipeline_result['run_id']}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎯 Close System Product Radar</h1>
        <div class="meta">
            Run: {pipeline_result['run_id']} · Pipeline: {pipeline_result['pipeline_version']} ·
            Point-in-Time: {pipeline_result['point_in_time']} · {FIXTURE_CATEGORY}
        </div>
    </div>

    {stats_html}

    <div class="section">
        <div class="section-title">📋 Product Radar</div>
        <table class="radar-table">
            <tr><th>Product</th><th>Category</th><th>Price</th><th>P1 P2 P3</th><th>Discount</th><th>Layers (5)</th><th>Recommendation</th></tr>
            {table_rows}
        </table>
    </div>

    <div class="section">
        <div class="section-title">🔍 Synthesis Cards</div>
        {cards_html}
    </div>

    <div style="text-align:center;padding:40px 0;color:var(--muted);font-size:12px;">
        Close System Product Radar V0 · {pipeline_result['run_id']} · Spec: {pipeline_result['spec_ref']}<br>
        NOT LIVE DATA — SYNTHETIC FIXTURES FOR V0 TESTING ONLY · No broker/execution/capital allocation
    </div>
</div>
</body>
</html>"""

    # ── Write outputs ──
    html_path = os.path.join(OUTPUT_DIR, "radar.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    json_path = os.path.join(OUTPUT_DIR, "pipeline_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_result, f, indent=2, default=str)

    return {
        "radar": html_path,
        "json": json_path,
    }
