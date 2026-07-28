"""
experimental/radar.py — Experimental Theme Radar (T4)

Phase 5 Theme Intelligence V1
Authorized: FD #27 (23 July 2026)

Dashboard that surfaces unapproved themes, hypotheses, and anomalies
from the experimental pipeline — constitutionally SEPARATE from the
approved Research Queue. Output goes to output/experimental/radar.html.

DISPLAY REQUIREMENTS:
  - Experimental themes with lifecycle + confidence level
  - Theme Hypotheses pending Founder review
  - Anomalies by type (Sector Divergence, Single-Stock, Volume, Missing Correlation)
  - "Propose Theme" button → triggers hypothesis engine
  - "Promote to Review" → sends to Founder Decision Queue

DESIGN SYSTEM: Claude warm minimalism (same as base.html)
  - Flat, clean, neutral palette
  - No dimensional/gradient/3D effects
  - Warm accent colors: blue (#5b9bd5), green (#6baf6b), amber (#d4a853), red (#d4645c)

HARD GUARDS (FD #27):
  1. ZERO imports from pipeline.py or display.py
  2. Radar reads ONLY from experimental/ data sources
  3. Radar HTML output goes to output/experimental/radar.html — NEVER to output/queue.html
  4. "Experimental Themes OFF" indicator must be visible (default state per FD #27)
  5. Radio button / toggle for "Experimental Themes OFF" is default
"""

import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

# ── Paths — experimental scope ONLY ──────────────────────────
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(MODULE_DIR)
PROJECT_ROOT = os.path.dirname(REPO_ROOT)
TEMPLATE_DIRS = [
    os.path.join(REPO_ROOT, "templates"),             # alpha-momentum-v0/templates (radar.html)
    os.path.join(PROJECT_ROOT, "shared", "templates"),  # shared/templates (base.html)
]
EXPERIMENTAL_OUTPUT_DIR = os.path.join(REPO_ROOT, "output", "experimental")
os.makedirs(EXPERIMENTAL_OUTPUT_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIRS),
    autoescape=select_autoescape(["html"]),
)

# ── Constants ────────────────────────────────────────────────
LIFECYCLE_CLASSES = {
    "Expansion": "expansion",
    "Emerging Leadership": "emerging",
    "Formation": "formation",
    "Crowded / Late": "crowded",
    "Deterioration": "deterioration",
}

ANOMALY_TYPE_COLORS = {
    "Sector Divergence": "#d4a853",
    "Single-Stock Outlier": "#d4645c",
    "Volume Anomaly": "#5b9bd5",
    "Missing Correlation": "#6baf6b",
}

CONFIDENCE_COLORS = {
    "High": "var(--success)",
    "Medium": "var(--warning)",
    "Low": "var(--danger)",
}

DEFAULT_EXPERIMENTAL_THEMES_OFF = True


def render_radar(experimental_result, output_dir=None):
    """Render Experimental Theme Radar HTML.

    Reads from experimental_result (NOT from approved pipeline_result).
    Output to output/experimental/radar.html.
    Constitutionally separate from approved queue.

    Args:
        experimental_result: Dict from run_experimental_pipeline()
        output_dir: Optional output directory (default: output/experimental/)

    Returns:
        str: Absolute path to the rendered radar.html file.

    ⚠️ CONSTITUTIONAL GUARDS:
        - ZERO imports from pipeline.py or display.py
        - Reads ONLY experimental/ data sources
        - Writes ONLY to output/experimental/ scope
        - Never mutates THEMES, CANDIDATES, or approved-strategy data
    """
    if output_dir is None:
        output_dir = EXPERIMENTAL_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    # ── Extract data from experimental_result ONLY ──────────
    anomalies = experimental_result.get("anomalies", [])
    hypotheses = experimental_result.get("hypotheses", [])
    experimental_themes = experimental_result.get("experimental_themes", [])
    review_queue = experimental_result.get("review_queue", {})
    stages = experimental_result.get("stages", [])

    # ── Derived metrics ─────────────────────────────────────
    anomaly_count = len(anomalies)
    hypothesis_count = len(hypotheses)
    experimental_theme_count = len(experimental_themes)

    # Anomaly breakdown by type
    anomaly_types = {}
    for an in anomalies:
        t = an.get("type", "Other")
        anomaly_types[t] = anomaly_types.get(t, 0) + 1

    # Hypotheses pending Founder review
    hypotheses_pending = [
        h for h in hypotheses
        if "awaiting Founder review" in h.get("status", "")
    ]

    # Review queue summary
    review_queue_hypotheses = review_queue.get("hypotheses", hypotheses)
    review_queue_themes = review_queue.get("experimental_themes", experimental_themes)

    # Pipeline stages summary
    pipeline_stages = []
    for s in stages:
        sid = s.get("stage_id", "")
        sname = s.get("stage", "")
        vals = {}
        for k, v in s.items():
            if k not in ("stage", "stage_id", "rule") and isinstance(v, (int, str, list)):
                if isinstance(v, list):
                    vals[k] = f"{len(v)} items"
                else:
                    vals[k] = str(v)
        pipeline_stages.append({
            "id": sid,
            "name": sname,
            "metrics": vals,
            "rule": s.get("rule", ""),
        })

    # ── Render via radar.html template ──────────────────────
    template = env.get_template("radar.html")
    html = template.render(
        # Experimental data
        anomalies=anomalies,
        hypotheses=hypotheses,
        experimental_themes=experimental_themes,
        review_queue=review_queue,
        stages=pipeline_stages,

        # Derived data
        anomaly_count=anomaly_count,
        hypothesis_count=hypothesis_count,
        experimental_theme_count=experimental_theme_count,
        anomaly_types=anomaly_types,
        hypotheses_pending=hypotheses_pending,
        review_queue_hypotheses=review_queue_hypotheses,
        review_queue_themes=review_queue_themes,

        # Constants
        lifecycle_classes=LIFECYCLE_CLASSES,
        anomaly_type_colors=ANOMALY_TYPE_COLORS,
        confidence_colors=CONFIDENCE_COLORS,
        experimental_themes_off=DEFAULT_EXPERIMENTAL_THEMES_OFF,

        # Pipeline metadata
        pipeline_version=experimental_result.get("pipeline_version", ""),
        run_id=experimental_result.get("run_id", ""),
        point_in_time=experimental_result.get("point_in_time", ""),
        fixture_category=experimental_result.get("fixture_category", FIXTURE_CATEGORY),
    )

    # ⚠️ CONSTITUTIONAL GUARD: output/experimental/ scope ONLY
    path = os.path.join(output_dir, "radar.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return os.path.abspath(path)


def export_radar_json(experimental_result, output_dir=None):
    """Export radar data as JSON for external consumption.

    Constitutionally separate — reads ONLY experimental/ data.
    Output to output/experimental/radar.json.
    """
    if output_dir is None:
        output_dir = EXPERIMENTAL_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    radar_data = {
        "experimental_themes_off": DEFAULT_EXPERIMENTAL_THEMES_OFF,
        "anomaly_count": len(experimental_result.get("anomalies", [])),
        "hypothesis_count": len(experimental_result.get("hypotheses", [])),
        "experimental_theme_count": len(experimental_result.get("experimental_themes", [])),
        "anomaly_types": {},
        "generated_at": datetime.now().isoformat(),
    }

    for an in experimental_result.get("anomalies", []):
        t = an.get("type", "Other")
        radar_data["anomaly_types"][t] = radar_data["anomaly_types"].get(t, 0) + 1

    path = os.path.join(output_dir, "radar.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(radar_data, f, indent=2, default=str, ensure_ascii=False)

    return os.path.abspath(path)
