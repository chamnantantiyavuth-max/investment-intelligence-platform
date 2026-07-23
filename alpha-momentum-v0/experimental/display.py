"""
Phase 5 Experimental Display — CONSTITUTIONALLY SEPARATE from approved display.
Authorized: FD #27 (23 July 2026).
Re-architected: T0-Phase5-Arch (24 July 2026).

Renders Weak Signal Inbox + Experimental Theme Radar.
ZERO imports from approved display.py render functions.
Output goes to output/experimental/ — NEVER to approved output/.
"""
import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

# ── Paths — experimental scope ONLY ──────────────────────────
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
EXPERIMENTAL_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "experimental")
os.makedirs(EXPERIMENTAL_OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))

# ── Constants ────────────────────────────────────────────────
LIFECYCLE_CLASSES = {
    "Expansion": "expansion",
    "Emerging Leadership": "emerging",
    "Formation": "formation",
    "Crowded / Late": "crowded",
    "Deterioration": "deterioration",
}


# ═══════════════════════════════════════════════════════════════
# WEAK SIGNAL INBOX RENDERING
# ═══════════════════════════════════════════════════════════════

def render_inbox(experimental_result, output_dir=None):
    """Render Weak Signal Inbox HTML.
    Reads from experimental_result (NOT from approved pipeline_result).
    Output to output/experimental/inbox.html.

    ⚠️ CONSTITUTIONAL GUARD: Does NOT import from display.py
    """
    if output_dir is None:
        output_dir = EXPERIMENTAL_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    anomalies = experimental_result.get("anomalies", [])
    hypotheses = experimental_result.get("hypotheses", [])

    template = env.get_template("inbox.html")
    html = template.render(
        anomalies=anomalies,
        hypotheses=hypotheses,
        pipeline_version=experimental_result.get("pipeline_version", ""),
        run_id=experimental_result.get("run_id", ""),
        point_in_time=experimental_result.get("point_in_time", ""),
        fixture_category=experimental_result.get("fixture_category", FIXTURE_CATEGORY),
    )

    path = os.path.join(output_dir, "inbox.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════════════════
# EXPERIMENTAL THEME CARDS
# ═══════════════════════════════════════════════════════════════

def render_theme_cards_experimental(experimental_result, output_dir=None):
    """Render experimental Theme Card HTML files.
    Reads from experimental_result (NOT from approved pipeline_result).
    Output to output/experimental/theme_cards_experimental/.

    ⚠️ CONSTITUTIONAL GUARD: Does NOT import render_theme_cards from display.py
    """
    if output_dir is None:
        output_dir = os.path.join(EXPERIMENTAL_OUTPUT_DIR, "theme_cards_experimental")
    os.makedirs(output_dir, exist_ok=True)

    experimental_themes = experimental_result.get("experimental_themes", [])
    experimental_evidence = experimental_result.get("experimental_evidence", [])
    experimental_candidates = experimental_result.get("experimental_candidates", [])

    if not experimental_themes:
        return []

    # Build evidence index
    evidence_by_theme = {}
    for ev in experimental_evidence:
        tid = ev.get("theme", "")
        if tid not in evidence_by_theme:
            evidence_by_theme[tid] = {"supporting": [], "contradicting": [], "missing": []}
        rel = ev.get("relationship", "")
        if rel in ("supporting", "contradicting", "missing"):
            evidence_by_theme[tid][rel].append(ev)

    template = env.get_template("theme_card.html")
    files = []

    for theme in experimental_themes:
        tid = theme["id"]
        ev = evidence_by_theme.get(tid, {"supporting": [], "contradicting": [], "missing": []})

        html = template.render(
            theme=theme,
            candidates=[c for c in experimental_candidates if c.get("ticker") in theme.get("key_tickers", [])],
            supporting_evidence=ev["supporting"],
            contradicting_evidence=ev["contradicting"],
            missing_evidence=ev["missing"],
            alternative=None,
            lifecycle_classes=LIFECYCLE_CLASSES,
            leadership_classes={},
            pipeline_version=experimental_result.get("pipeline_version", ""),
            run_id=experimental_result.get("run_id", ""),
            point_in_time=experimental_result.get("point_in_time", ""),
            fixture_category=FIXTURE_CATEGORY,
            is_experimental=True,
        )

        filename = f"theme_{tid}.html"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        files.append(path)

    return files


# ═══════════════════════════════════════════════════════════════
# EXPERIMENTAL THEME RADAR (T4 will replace with full implementation)
# ═══════════════════════════════════════════════════════════════

def render_radar(experimental_result, output_dir=None):
    """Render Experimental Theme Radar HTML.
    T4 (experimental/radar.py) will provide the full dashboard.
    For T0 architecture: renders a minimal radar page.

    Output to output/experimental/radar.html.
    ⚠️ CONSTITUTIONAL GUARD: Does NOT import from display.py
    """
    if output_dir is None:
        output_dir = EXPERIMENTAL_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    anomalies = experimental_result.get("anomalies", [])
    hypotheses = experimental_result.get("hypotheses", [])
    experimental_themes = experimental_result.get("experimental_themes", [])
    review_queue = experimental_result.get("review_queue", {})
    stages = experimental_result.get("stages", [])

    # Count by type
    anomaly_types = {}
    for an in anomalies:
        t = an.get("type", "Other")
        anomaly_types[t] = anomaly_types.get(t, 0) + 1

    # Check if radar template exists; if not, generate inline
    radar_template_path = os.path.join(TEMPLATE_DIR, "radar.html")
    if os.path.exists(radar_template_path):
        template = env.get_template("radar.html")
    else:
        # Use inline minimal rendering (T4 will create proper template)
        html = _render_radar_inline(
            anomalies=anomalies,
            hypotheses=hypotheses,
            experimental_themes=experimental_themes,
            anomaly_types=anomaly_types,
            stages=stages,
            result=experimental_result,
        )

    path = os.path.join(output_dir, "radar.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def _render_radar_inline(anomalies, hypotheses, experimental_themes, anomaly_types,
                         stages, result):
    """Minimal inline radar rendering — replaced by proper template in T4."""
    base_template = env.get_template("base.html")

    # Build radar content block
    radar_html = f"""<div class="page">
  <div class="page-header">
    <h1>📡 Experimental Theme Radar</h1>
    <div class="subtitle">Unapproved themes, hypotheses, and anomalies — separate from approved Research Queue</div>
  </div>

  <div style="padding: 0.75rem 1rem; background: var(--accent-light); border-radius: var(--radius-sm); margin-bottom: 2rem; font-size: 13px; color: var(--text-secondary);">
    ⚠️ <strong>Experimental Themes OFF</strong> is the default. Nothing here affects the official Research Queue. Theme approval remains Founder-only. Epistemic metadata (§23.4) attached to all AI-generated hypotheses.
  </div>

  <!-- Pipeline Stages Summary -->
  <div class="section">
    <h2>🔄 Experimental Pipeline</h2>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;">
"""
    for s in stages:
        sid = s.get("stage_id", "")
        name = s.get("stage", "")
        vals = []
        for k, v in s.items():
            if k not in ("stage", "stage_id", "rule") and isinstance(v, (int, str)):
                vals.append(f"{k}: {v}")
        radar_html += f"""      <div style="background:var(--bg-page);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.75rem 1rem;flex:1;min-width:200px;">
        <strong style="font-size:12px;">{sid}: {name}</strong>
        <div style="font-size:11px;color:var(--text-tertiary);margin-top:4px;">{'; '.join(vals[:3])}</div>
      </div>
"""

    radar_html += f"""    </div>
  </div>

  <!-- Anomalies by Type -->
  <div class="section">
    <h2>🔍 Anomalies ({len(anomalies)} detected)</h2>
"""
    for atype, count in anomaly_types.items():
        radar_html += f"""    <span class="badge" style="margin-right:4px;">{atype}: {count}</span>"""

    radar_html += """
    <div style="display:flex;flex-direction:column;gap:0.75rem;margin-top:1rem;">
"""
    for an in anomalies:
        radar_html += f"""      <div style="background:var(--bg-page);border:1px solid var(--border);border-left:3px solid var(--warning);border-radius:var(--radius-sm);padding:0.75rem 1rem;">
        <div><strong style="font-size:13px;">{an['id']}</strong> <span class="badge" style="background:var(--warning-bg);color:var(--warning);">{an.get('type','')}</span> <span class="badge" style="background:var(--danger-bg);color:var(--danger);">{an.get('status','')}</span></div>
        <p style="font-size:12px;color:var(--text-secondary);margin-top:4px;">{an.get('description','')[:200]}...</p>
      </div>
"""
    radar_html += """    </div>
  </div>

  <!-- Hypotheses -->
  <div class="section">
    <h2>💡 Theme Hypotheses ({hypotheses_count} pending review)</h2>
"""
    radar_html = radar_html.replace("{hypotheses_count}", str(len(hypotheses)))

    for hy in hypotheses:
        ep = hy.get("_epistemic", {})
        radar_html += f"""    <div style="background:var(--bg-page);border:1px solid var(--border);border-left:3px solid var(--info);border-radius:var(--radius-sm);padding:1rem;margin-bottom:0.75rem;">
      <div><strong style="font-size:14px;">{hy['id']}: {hy.get('title','')}</strong> <span class="badge" style="background:var(--info-bg);color:var(--info);">{hy.get('status','')}</span></div>
      <p style="font-size:12px;color:var(--text-secondary);margin-top:4px;">{hy.get('proposed_driver','')[:200]}...</p>
      <div style="font-size:10px;color:var(--text-tertiary);margin-top:8px;">📋 Epistemic: {ep.get('provenance','')} | Confidence: {ep.get('confidence_level','')} | v{ep.get('version','')}</div>
    </div>
"""

    radar_html += """  </div>

  <!-- Experimental Themes -->
  <div class="section">
    <h2>🧪 Experimental Themes ({exp_count})</h2>
"""
    radar_html = radar_html.replace("{exp_count}", str(len(experimental_themes)))

    for t in experimental_themes:
        radar_html += f"""    <div style="background:var(--bg-page);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:var(--radius-sm);padding:1rem;margin-bottom:0.75rem;">
      <div><strong style="font-size:14px;">{t['id']}: {t.get('name','')}</strong> <span class="badge" style="background:var(--accent-light);color:var(--accent);">{t.get('approval_status','')}</span></div>
      <p style="font-size:12px;color:var(--text-secondary);margin-top:4px;">{t.get('why_now','')[:200]}...</p>
      <div style="font-size:11px;margin-top:4px;">Sector: {t.get('sector','')} | Industry: {t.get('industry','')} | Confidence: {t.get('confidence','')}</div>
    </div>
"""

    radar_html += """  </div>

  <!-- Navigation -->
  <div style="text-align:center;margin-top:2rem;">
    <a href="../queue.html" style="font-size:13px;">← Back to Approved Research Queue</a>
    &nbsp;·&nbsp;
    <a href="inbox.html" style="font-size:13px;">📡 Weak Signal Inbox →</a>
  </div>
</div>"""

    # Wrap in base template
    page_html = f"""{{% extends "base.html" %}}
{{% block title %}}Experimental Theme Radar | Alpha Momentum V0{{% endblock %}}
{{% block content %}}
{radar_html}
{{% endblock %}}"""

    # Use the same approach: render through base.html with precomputed content
    # Since we can't easily inject raw HTML into Jinja2 extends, render base with our content
    from jinja2 import Template
    base_content = env.get_template("base.html")
    # Workaround: render radar as standalone HTML with base styling inline
    return _render_standalone(radar_html, result, "Experimental Theme Radar")


def _render_standalone(content_html, result, title):
    """Render a standalone HTML page with base template styling applied."""
    base_template = env.get_template("base.html")
    # Read base.html to extract styles
    base_path = os.path.join(TEMPLATE_DIR, "base.html")
    with open(base_path, "r", encoding="utf-8") as f:
        base_source = f.read()

    # Use Jinja2 to render base with our content injected
    # Create a simple template that includes base content
    template_source = base_source.replace(
        "{% block content %}{% endblock %}",
        "{% block content %}" + content_html + "{% endblock %}"
    )
    template_source = template_source.replace(
        "{% block title %}{% endblock %}",
        "{% block title %}" + title + " | Alpha Momentum V0{% endblock %}"
    )
    from jinja2 import Template as Jinja2Template
    tpl = Jinja2Template(template_source)
    return tpl.render(
        pipeline_version=result.get("pipeline_version", ""),
        run_id=result.get("run_id", ""),
        point_in_time=result.get("point_in_time", ""),
        fixture_category=result.get("fixture_category", FIXTURE_CATEGORY),
    )


# ═══════════════════════════════════════════════════════════════
# RENDER ALL — Experimental
# ═══════════════════════════════════════════════════════════════

def render_all_experimental(experimental_result):
    """Render all experimental outputs: inbox + radar + theme cards + JSON.
    ⚠️ CONSTITUTIONAL GUARD: ZERO imports from approved display.py
    Output to output/experimental/ — NEVER to approved output/
    """
    if not experimental_result or not experimental_result.get("has_data"):
        return {"message": "No experimental data to render"}

    inbox_path = render_inbox(experimental_result)
    radar_path = render_radar(experimental_result)
    card_paths = render_theme_cards_experimental(experimental_result)

    # Save experimental pipeline result JSON
    json_path = os.path.join(EXPERIMENTAL_OUTPUT_DIR, "experimental_pipeline_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(experimental_result, f, indent=2, default=str, ensure_ascii=False)

    return {
        "inbox": inbox_path,
        "radar": radar_path,
        "theme_cards_experimental": card_paths,
        "json": json_path,
    }
