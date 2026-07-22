"""
Alpha Momentum V0 — HTML Display Layer
Renders Theme Cards, Research Queue, and Candidate Detail using Jinja2.
Per THEME-CARD-AND-HUMAN-REVIEW-FLOW.md and FIXTURE-AND-ACCEPTANCE-SCENARIOS.md.
"""
import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fixtures import FIXTURE_CATEGORY

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))


def _lifecycle_class(lifecycle: str) -> str:
    return {"Expansion": "expansion", "Emerging Leadership": "emerging",
            "Formation": "formation", "Crowded / Late": "crowded",
            "Deterioration": "deterioration"}.get(lifecycle, "")


def _leadership_class(state: str) -> str:
    return {"Confirmed Leader": "leader", "Emerging Challenger": "challenger",
            "Former Leader": "former", "Deteriorating Member": "deteriorating"}.get(state, "")


def _cq_short(cq: dict) -> str:
    """Short CQ label for table display."""
    g1 = cq.get("Group 1 — Trend & Participation", {})
    rs = g1.get("Relative Strength", "N/A")
    g2 = cq.get("Group 2 — Tradeability & Growth", {})
    f = g2.get("Fundamentals", "N/A")
    return f"{f[:8]} / {rs[:8]}"


def _er_short(er: dict) -> str:
    """Short ER label for table display."""
    g1 = er.get("Group 1 — Pattern Quality", {})
    ps = g1.get("Price Structure", "N/A")
    g2 = er.get("Group 2 — Entry Timing", {})
    bp = g2.get("Breakout Proximity", "N/A")
    return f"{ps[:10]} / {bp[:6]}"


def render_theme_cards(pipeline_result, output_dir=None):
    """Render individual Theme Card HTML files per theme."""
    if output_dir is None:
        output_dir = os.path.join(OUTPUT_DIR, "theme_cards")
    os.makedirs(output_dir, exist_ok=True)
    
    queue = pipeline_result["queue"]
    evidence = {ev["id"]: ev for ev in pipeline_result["evidence"]}
    overrides = {ov["candidate_id"]: ov for ov in pipeline_result["overrides"]}
    files = []

    for tid, tdata in queue:
        theme = tdata["theme"]
        candidates_raw = tdata["candidates"]

        # Group evidence by theme
        theme_evidence = [ev for ev in evidence.values() if ev.get("theme") == tid]
        supporting = [ev for ev in theme_evidence if ev["relationship"] == "supporting"]
        contradicting = [ev for ev in theme_evidence if ev["relationship"] == "contradicting"]
        missing = [ev for ev in theme_evidence if ev["relationship"] == "missing"]

        # Enrich candidates for template
        candidates_display = []
        for c in candidates_raw:
            ct = c.get("_ct_relationship", {})
            candidates_display.append({
                "ticker": c["ticker"],
                "primary_role": ct.get("primary_role", ""),
                "secondary_roles": ct.get("secondary_roles", []),
                "leadership_state": ct.get("leadership_state", ""),
                "leadership_class": _leadership_class(ct.get("leadership_state", "")),
                "cq_short": _cq_short(c.get("_cq_display", {})),
                "er_short": _er_short(c.get("_er_display", {})),
                "dc_warning": c.get("_dc_warning", "✅"),
                "research_state": c.get("research_state", ""),
                "override": c["id"] in overrides,
            })

        template = env.get_template("theme_card.html")
        html = template.render(
            theme=theme,
            candidates=candidates_display,
            supporting_evidence=supporting,
            contradicting_evidence=contradicting,
            missing_evidence=missing,
            alternative=pipeline_result.get("alternative_explanations", {}).get(tid),
            lifecycle_class=_lifecycle_class(theme.get("lifecycle", "")),
            pipeline_version=pipeline_result["pipeline_version"],
            run_id=pipeline_result["run_id"],
            point_in_time=pipeline_result["point_in_time"],
            fixture_category=FIXTURE_CATEGORY,
        )

        filename = f"theme_{tid}.html"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        files.append(path)

    return files


def render_queue(pipeline_result, output_dir=None):
    """Render the Research Queue HTML."""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    queue = pipeline_result["queue"]
    stages = pipeline_result["stages"]
    total = sum(len(td["candidates"]) for _, td in queue)
    empty_themes = [tid for tid, td in queue if len(td["candidates"]) == 0]

    lines = ["<!DOCTYPE html>", '<html lang="en"><head><meta charset="UTF-8">',
             '<title>Research Queue | Alpha Momentum V0</title>',
             '<style>',
             '*{margin:0;padding:0;box-sizing:border-box}',
             'body{font-family:Inter,system-ui,sans-serif;background:#0d1117;color:#c9d1d9;padding:2rem;font-size:13px}',
             '.not-live{background:#da3633;color:#fff;text-align:center;padding:6px 12px;font-weight:700;font-size:11px;border-radius:4px;margin-bottom:1.5rem}',
             'h1{font-size:22px;color:#58a6ff;margin-bottom:0.5rem}',
             '.summary{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}',
             '.metric{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px 16px;text-align:center;min-width:100px}',
             '.metric .num{font-size:24px;font-weight:700}',
             '.metric .lbl{font-size:10px;text-transform:uppercase;color:#8b949e;margin-top:4px}',
             '.expansion{color:#3fb950}.emerging{color:#d29922}.formation{color:#58a6ff}.crowded{color:#f0883e}.deterioration{color:#da3633}',
             '.queue-item{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:1rem;margin-bottom:1rem}',
             '.queue-item h2{font-size:15px;margin-bottom:4px}',
             '.queue-item .meta{font-size:11px;color:#8b949e;margin-bottom:8px}',
             'table{width:100%;border-collapse:collapse;font-size:12px}',
             'th{text-align:left;padding:6px 8px;background:#21262d;color:#8b949e;font-weight:600;text-transform:uppercase;font-size:10px}',
             'td{padding:6px 8px;border-bottom:1px solid #21262d}',
             'tr:hover td{background:#1c2128}',
             '.badge{display:inline-block;padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600}',
             '.badge-leader{background:#1f3a2e;color:#3fb950}.badge-challenger{background:#2b2a1a;color:#d29922}',
             '.badge-former{background:#3a1f1f;color:#da3633}',
             '.override-badge{background:#da3633;color:#fff;padding:1px 5px;border-radius:6px;font-size:9px;font-weight:700;margin-left:4px}',
             '.empty-state{text-align:center;padding:2rem;color:#8b949e;font-style:italic}',
             '.empty-theme{opacity:0.5}',
             '.stages{margin-top:2rem;padding-top:1rem;border-top:1px solid #30363d}',
             '.stages h3{font-size:13px;color:#8b949e;margin-bottom:8px}',
             '.stage-row{display:flex;justify-content:space-between;padding:4px 0;font-size:11px;border-bottom:1px solid #21262d}',
             '.audit{margin-top:1.5rem;font-size:10px;color:#484f58}',
             '</style></head><body>',
             f'<div class="not-live">⚠️ NOT LIVE DATA — FOR V0 TESTING ONLY — {FIXTURE_CATEGORY}</div>',
             '<h1>📊 Research Queue — Alpha Momentum V0</h1>']

    if total == 0:
        lines.append(f'<div class="empty-state">No candidates meet current quality thresholds across any monitored theme.</div>')
        lines.append(f'<p style="text-align:center;color:#8b949e;font-size:12px;">{len(queue)} themes monitored</p>')
    else:
        lines.append('<div class="summary">')
        lines.append(f'<div class="metric"><div class="num" style="color:#58a6ff;">{len(queue)}</div><div class="lbl">Themes</div></div>')
        lines.append(f'<div class="metric"><div class="num" style="color:#3fb950;">{total}</div><div class="lbl">Candidates</div></div>')
        lines.append(f'<div class="metric"><div class="num" style="color:#d29922;">{len(empty_themes)}</div><div class="lbl">Empty Themes</div></div>')
        lines.append('</div>')

        for tid, tdata in queue:
            theme = tdata["theme"]
            lc = _lifecycle_class(theme.get("lifecycle", ""))
            has_candidates = len(tdata["candidates"]) > 0
            empty_class = ' empty-theme' if not has_candidates else ''
            lines.append(f'<div class="queue-item{empty_class}">')
            lines.append(f'<h2><span class="{lc}">●</span> {theme["name"]} <span style="font-size:11px;color:#8b949e;">({theme["sector"]} → {theme["industry"]})</span></h2>')
            lines.append(f'<div class="meta">{theme["lifecycle"]} · {theme["confidence"]} confidence · {len(tdata["candidates"])} candidates · <a href="theme_cards/theme_{tid}.html" style="color:#58a6ff;">Full Theme Card →</a></div>')

            if has_candidates:
                lines.append('<table><thead><tr><th>Ticker</th><th>Role</th><th>Leadership</th><th>CQ</th><th>ER</th><th>DC</th><th>Research</th></tr></thead><tbody>')
                for c in tdata["candidates"]:
                    ct = c.get("_ct_relationship", {})
                    ls = ct.get("leadership_state", "")
                    ovr = ' <span class="override-badge">OVERRIDE</span>' if c["id"] in {ov["candidate_id"] for ov in pipeline_result.get("overrides", [])} else ''
                    lines.append(f'<tr><td><strong style="color:#58a6ff;">{c["ticker"]}</strong>{ovr}</td>')
                    lines.append(f'<td>{ct.get("primary_role","")}</td>')
                    lines.append(f'<td><span class="badge badge-{_leadership_class(ls)}">{ls}</span></td>')
                    lines.append(f'<td>{_cq_short(c.get("_cq_display",{}))}</td>')
                    lines.append(f'<td>{_er_short(c.get("_er_display",{}))}</td>')
                    lines.append(f'<td>{c.get("_dc_warning","✅")}</td>')
                    lines.append(f'<td>{c.get("research_state","")}</td></tr>')
                lines.append('</tbody></table>')
            else:
                lines.append('<div class="empty-state">No qualified candidates — theme is monitored but no actionable setups at this time.</div>')
            lines.append('</div>')

    # Pipeline stages summary
    lines.append('<div class="stages"><h3>Pipeline Stages</h3>')
    for s in stages:
        val = s.get("output_count", s.get("passed_count", s.get("dimensions_assessed", s.get("total_candidates", "—"))))
        lines.append(f'<div class="stage-row"><span>{s["stage_id"]}: {s["stage"]}</span><span style="color:#8b949e;">{val}</span></div>')
    lines.append('</div>')

    lines.append(f'<div class="audit">Pipeline: {pipeline_result["pipeline_version"]} · Run: {pipeline_result["run_id"]} · Point-in-Time: {pipeline_result["point_in_time"]} · {FIXTURE_CATEGORY}</div>')
    lines.append('</body></html>')

    path = os.path.join(output_dir, "queue.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def render_all(pipeline_result):
    """Render all outputs: queue + theme cards + JSON export."""
    queue_path = render_queue(pipeline_result)
    card_paths = render_theme_cards(pipeline_result)

    # JSON export for reproducibility verification (AC-2, AC-7)
    json_path = os.path.join(OUTPUT_DIR, "pipeline_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_result, f, indent=2, default=str, ensure_ascii=False)

    return {
        "queue": queue_path,
        "theme_cards": card_paths,
        "json": json_path,
    }
