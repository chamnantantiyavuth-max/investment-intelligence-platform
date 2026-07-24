"""
Close System Product Radar V0 — HTML Display Layer
Renders Product Radar table and Synthesis Cards using Jinja2.
Per CLOSE-SYSTEM-PRODUCT-RADAR.md §5.2 (Synthesis Template).
V1.1: Refactored to use shared unified design system (FD #39, 25 July 2026).
"""
import os, json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
SHARED_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shared", "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader([TEMPLATE_DIR, SHARED_TEMPLATE_DIR]),
    autoescape=select_autoescape(["html"]),
)

LAYER_LABELS = {
    "L1_macro": "1. Macro Economics",
    "L2_policy": "2. Government Policy",
    "L3_cost": "3. Cost Structure",
    "L4_supply_demand": "4. Supply/Demand",
    "L5_hidden": "5. Hidden Signals",
}


def _enrich_products_for_template(products):
    """Prepare product data for Jinja2 template rendering."""
    enriched = []
    for p in products:
        entry = dict(p)  # shallow copy

        # Build layer rows for template iteration
        layers = p.get("layers", {})
        entry["layer_rows"] = []
        for lid, label in LAYER_LABELS.items():
            entry["layer_rows"].append((lid, label, layers.get(lid, {"signal": "neutral", "note": ""})))

        enriched.append(entry)
    return enriched


def render_all(pipeline_result):
    """Render radar table HTML + synthesis cards using Jinja2 template."""
    products = _enrich_products_for_template(pipeline_result.get("synthesized", []))
    radar = pipeline_result.get("radar", {})
    stages = pipeline_result.get("stages", [])
    s6 = stages[-1] if stages else {}

    template = env.get_template("radar.html")
    html = template.render(
        # Page context (shared base)
        run_id=pipeline_result["run_id"],
        pipeline_version=pipeline_result["pipeline_version"],
        pipeline_name="Close System Product Radar V0",
        point_in_time=pipeline_result["point_in_time"],
        fixture_category=FIXTURE_CATEGORY,
        spec_ref=pipeline_result["spec_ref"],

        # Radar data
        products=products,
        total_products=s6.get("total_products", 0),
        eligible=s6.get("eligible_for_radar", 0),
        present_count=s6.get("present_to_founder", 0),
        research_count=s6.get("deep_research", 0),
        watchlist_count=s6.get("radar_watchlist", 0),
        monitor_count=s6.get("monitor", 0),
    )

    html_path = os.path.join(OUTPUT_DIR, "radar.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    json_path = os.path.join(OUTPUT_DIR, "pipeline_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_result, f, indent=2, default=str)

    return {"radar": html_path, "json": json_path}
