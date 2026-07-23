"""
⚠️ QUARANTINED — Phase 5 Experimental Display
Moved from display.py per WF-Phase 2R Architecture Review (23 Jul 2026).
Do NOT import this module from approved display code.
"""
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "experimental")
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))

# ── Experimental Theme Cards ──

def render_theme_cards_experimental(pipeline_result, output_dir=None):
    """Render experimental Theme Card HTML files. ⚠️ QUARANTINED."""
    if output_dir is None:
        base = os.path.join(OUTPUT_DIR, "theme_cards_experimental")
        output_dir = base
    os.makedirs(output_dir, exist_ok=True)
    # (simplified — delegates to main render_theme_cards with is_experimental=True)
    from display import render_theme_cards
    return render_theme_cards(pipeline_result, output_dir=output_dir, is_experimental=True)

# ── Weak Signal Inbox ──

def render_inbox(anomalies, hypotheses, pipeline_version, run_id, point_in_time, fixture_category, output_dir=None):
    """Render Weak Signal Inbox HTML. ⚠️ QUARANTINED."""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    template = env.get_template("inbox.html")
    html = template.render(
        anomalies=anomalies,
        hypotheses=hypotheses,
        pipeline_version=pipeline_version,
        run_id=run_id,
        point_in_time=point_in_time,
        fixture_category=fixture_category,
    )

    path = os.path.join(output_dir, "inbox.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path
