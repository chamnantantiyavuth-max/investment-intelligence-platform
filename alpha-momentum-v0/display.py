"""
Alpha Momentum V0 — HTML Display Layer
Renders Theme Cards, Research Queue, and Candidate Detail using Jinja2.
Per THEME-CARD-AND-HUMAN-REVIEW-FLOW.md and FIXTURE-AND-ACCEPTANCE-SCENARIOS.md.

V0.3: Experimental themes + weak signal inbox.
"""
import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))

LIFECYCLE_CLASSES = {
    "Expansion": "expansion",
    "Emerging Leadership": "emerging",
    "Formation": "formation",
    "Crowded / Late": "crowded",
    "Deterioration": "deterioration",
}

LEADERSHIP_CLASSES = {
    "Confirmed Leader": "leader",
    "Emerging Challenger": "challenger",
    "Former Leader": "former",
    "Deteriorating Member": "deteriorating",
}


def _cq_short(cq: dict) -> str:
    g1 = cq.get("Group 1 — Trend & Participation", {})
    rs = g1.get("Relative Strength", "N/A")
    g2 = cq.get("Group 2 — Tradeability & Growth", {})
    f = g2.get("Fundamentals", "N/A")
    return f"{f} / {rs}"


def _er_short(er: dict) -> str:
    g1 = er.get("Group 1 — Pattern Quality", {})
    ps = g1.get("Price Structure", "N/A")
    g2 = er.get("Group 2 — Entry Timing", {})
    bp = g2.get("Breakout Proximity", "N/A")
    return f"{ps} / {bp}"


def _enrich_candidates(candidates_raw, overrides_set):
    enriched = []
    for c in candidates_raw:
        ct = c.get("_ct_relationship", {})
        enriched.append({
            "ticker": c["ticker"],
            "primary_role": ct.get("primary_role", ""),
            "secondary_roles": ct.get("secondary_roles", []),
            "leadership_state": ct.get("leadership_state", ""),
            "cq_short": _cq_short(c.get("_cq_display", {})),
            "er_short": _er_short(c.get("_er_display", {})),
            "dc_warning": c.get("_dc_warning", "✅"),
            "research_state": c.get("research_state", ""),
            "override": c["id"] in overrides_set,
        })
    return enriched


# ── Theme Cards ──

def render_theme_cards(pipeline_result, output_dir=None, is_experimental=False):
    """Render individual Theme Card HTML files per theme using Jinja2 template.
    If is_experimental=True, renders cards for experimental themes."""
    if output_dir is None:
        base = os.path.join(OUTPUT_DIR, "theme_cards")
        if is_experimental:
            base = os.path.join(OUTPUT_DIR, "theme_cards_experimental")
        output_dir = base
    os.makedirs(output_dir, exist_ok=True)

    if is_experimental:
        exp = pipeline_result.get("experimental", {})
        if not exp.get("has_data"):
            return []
        queue = exp["queue"]
        evidence_list = exp.get("evidence", [])
        overrides_list = []
        alt_explanations = {}
    else:
        queue = pipeline_result["queue"]
        evidence_list = pipeline_result.get("evidence", [])
        overrides_list = pipeline_result.get("overrides", [])
        alt_explanations = pipeline_result.get("alternative_explanations", {})

    evidence = {ev["id"]: ev for ev in evidence_list}
    overrides_set = {ov["candidate_id"] for ov in overrides_list}
    template = env.get_template("theme_card.html")
    files = []

    for tid, tdata in queue:
        theme = tdata["theme"]
        theme_evidence = [ev for ev in evidence.values() if ev.get("theme") == tid]
        supporting = [ev for ev in theme_evidence if ev.get("relationship") == "supporting"]
        contradicting = [ev for ev in theme_evidence if ev.get("relationship") == "contradicting"]
        missing = [ev for ev in theme_evidence if ev.get("relationship") == "missing"]
        candidates_display = _enrich_candidates(tdata["candidates"], overrides_set)

        html = template.render(
            theme=theme,
            candidates=candidates_display,
            supporting_evidence=supporting,
            contradicting_evidence=contradicting,
            missing_evidence=missing,
            alternative=alt_explanations.get(tid),
            lifecycle_classes=LIFECYCLE_CLASSES,
            leadership_classes=LEADERSHIP_CLASSES,
            pipeline_version=pipeline_result["pipeline_version"],
            run_id=pipeline_result["run_id"],
            point_in_time=pipeline_result["point_in_time"],
            fixture_category=FIXTURE_CATEGORY,
            is_experimental=is_experimental,
        )

        filename = f"theme_{tid}.html"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        files.append(path)

    return files


# ── Research Queue ──

def render_queue(pipeline_result, output_dir=None):
    """Render the Research Queue HTML using Jinja2 template."""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    queue = pipeline_result["queue"]
    stages = pipeline_result.get("stages", [])
    overrides_set = {ov["candidate_id"] for ov in pipeline_result.get("overrides", [])}
    experimental = pipeline_result.get("experimental", {})

    queue_display = []
    for tid, tdata in queue:
        candidates_display = _enrich_candidates(tdata["candidates"], overrides_set)
        queue_display.append((tid, {"theme": tdata["theme"], "candidates": candidates_display}))

    total_candidates = sum(len(td["candidates"]) for _, td in queue_display)
    empty_theme_count = sum(1 for _, td in queue_display if len(td["candidates"]) == 0)

    exp_queue_display = []
    exp_total = 0
    exp_empty = 0
    if experimental.get("has_data"):
        for tid, tdata in experimental["queue"]:
            candidates_display = _enrich_candidates(tdata["candidates"], set())
            exp_queue_display.append((tid, {"theme": tdata["theme"], "candidates": candidates_display}))
        exp_total = sum(len(td["candidates"]) for _, td in exp_queue_display)
        exp_empty = sum(1 for _, td in exp_queue_display if len(td["candidates"]) == 0)

    template = env.get_template("queue.html")
    html = template.render(
        queue=queue_display,
        theme_count=len(queue),
        total_candidates=total_candidates,
        empty_theme_count=empty_theme_count,
        stages=stages,
        experimental_queue=exp_queue_display,
        experimental_has_data=experimental.get("has_data", False),
        experimental_total=exp_total,
        experimental_empty=exp_empty,
        lifecycle_classes=LIFECYCLE_CLASSES,
        leadership_classes=LEADERSHIP_CLASSES,
        pipeline_version=pipeline_result["pipeline_version"],
        run_id=pipeline_result["run_id"],
        point_in_time=pipeline_result["point_in_time"],
        fixture_category=FIXTURE_CATEGORY,
    )

    path = os.path.join(output_dir, "queue.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ── Weak Signal Inbox ──

def render_inbox(pipeline_result, output_dir=None):
    """Render the Weak Signal Inbox HTML using Jinja2 template."""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    anomalies = pipeline_result.get("inbox_anomalies", [])
    hypotheses = pipeline_result.get("inbox_hypotheses", [])

    template = env.get_template("inbox.html")
    html = template.render(
        anomalies=anomalies,
        hypotheses=hypotheses,
        pipeline_version=pipeline_result["pipeline_version"],
        run_id=pipeline_result["run_id"],
        point_in_time=pipeline_result["point_in_time"],
        fixture_category=FIXTURE_CATEGORY,
    )

    path = os.path.join(output_dir, "inbox.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ── Render All ──

def render_all(pipeline_result):
    """Render all outputs: queue + theme cards (approved + experimental) + inbox + JSON."""
    queue_path = render_queue(pipeline_result)
    card_paths = render_theme_cards(pipeline_result)
    exp_card_paths = render_theme_cards(pipeline_result, is_experimental=True)
    inbox_path = render_inbox(pipeline_result)

    json_path = os.path.join(OUTPUT_DIR, "pipeline_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_result, f, indent=2, default=str, ensure_ascii=False)

    return {
        "queue": queue_path,
        "theme_cards": card_paths,
        "experimental_theme_cards": exp_card_paths,
        "inbox": inbox_path,
        "json": json_path,
    }
