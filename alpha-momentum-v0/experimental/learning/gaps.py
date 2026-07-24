"""
Phase 6: Learning Loop — Coverage Gap Detection
Authorized: FD #28 (24 July 2026)

Scans system state for 4 gap types after every material pipeline run.
Per coverage-gap-template.md + LEARNING-AND-KNOWLEDGE-LOOP.md.

Gaps are surfaced, never silently acted upon. Founder decides disposition.
"""
import os, json, datetime
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GAPS_DIR = os.path.join(REPO_ROOT, "operational", "coverage-gaps")
os.makedirs(GAPS_DIR, exist_ok=True)


def detect_coverage_gaps(pipeline_result: dict, exp_result: dict = None,
                          run_id: str = None) -> list:
    """Detect coverage gaps across 4 types.

    Returns list of gap dicts with: gap_type, severity, description, evidence_refs, recommendation.
    """
    if run_id is None:
        run_id = pipeline_result.get("run_id", "unknown")

    gaps = []

    # ── Type 1: Theme Coverage Gap ──
    # Approved theme with evidence but zero candidates
    queue = pipeline_result.get("queue", [])
    for tid, tdata in queue:
        candidates = tdata.get("candidates", [])
        theme = tdata.get("theme", {})
        if len(candidates) == 0:
            gaps.append({
                "gap_type": "Theme Coverage Gap",
                "severity": "Medium",
                "theme_id": tid,
                "theme_name": theme.get("name", tid),
                "description": f"Theme {tid} ({theme.get('name','')}) has zero candidates in Watchlist despite being Approved and under Active Monitoring.",
                "current_coverage": 0,
                "evidence_strength": _assess_evidence_strength(tid, pipeline_result),
                "recommendation": f"Add at least 1 candidate to {tid} Watchlist or downgrade monitoring to Passive.",
                "evidence_refs": _get_evidence_refs(tid, pipeline_result),
            })

    # ── Type 2: Candidate Blind Spot ──
    # Candidate appearing in anomalies/hypotheses but not in Watchlist
    if exp_result:
        all_tickers_in_watchlist = set()
        for _, tdata in queue:
            for c in tdata.get("candidates", []):
                all_tickers_in_watchlist.add(c.get("ticker", ""))

        # Check anomalies for tickers not in watchlist
        for an in exp_result.get("anomalies", []):
            for t in an.get("related_tickers", []):
                if t not in all_tickers_in_watchlist:
                    gaps.append({
                        "gap_type": "Candidate Blind Spot",
                        "severity": "Low",
                        "ticker": t,
                        "description": f"{t} appears in anomaly {an.get('id','')} ({an.get('type','')}) but is not tracked in any Watchlist.",
                        "appears_in": [an.get("related_theme", "")],
                        "recommendation": f"Evaluate {t} as potential Candidate for {an.get('related_theme','relevant theme')}.",
                        "evidence_refs": [an.get("id", "")],
                    })
                    all_tickers_in_watchlist.add(t)  # prevent duplicates

        # Check hypotheses for tickers not in watchlist
        for hy in exp_result.get("hypotheses", []):
            for t in hy.get("potential_candidates", []):
                if t not in all_tickers_in_watchlist:
                    gaps.append({
                        "gap_type": "Candidate Blind Spot",
                        "severity": "Medium",
                        "ticker": t,
                        "description": f"{t} proposed in hypothesis {hy.get('id','')} ('{hy.get('title','')}') but not tracked in any Watchlist.",
                        "appears_in": [hy.get("id", "")],
                        "recommendation": f"Add {t} to Watchlist if hypothesis '{hy.get('title','')}' advances.",
                        "evidence_refs": [],
                    })
                    all_tickers_in_watchlist.add(t)

    # ── Type 3: Sector Blind Spot ──
    # Sector with improving signals but no theme coverage
    sectors_covered = set()
    for _, tdata in queue:
        theme = tdata.get("theme", {})
        if theme.get("sector"):
            sectors_covered.add(theme["sector"])

    # Check experimental themes for new sectors
    if exp_result:
        for et in exp_result.get("experimental_themes", []):
            sector = et.get("sector", "")
            if sector and sector not in sectors_covered:
                gaps.append({
                    "gap_type": "Sector Blind Spot",
                    "severity": "Low",
                    "sector": sector,
                    "description": f"Sector '{sector}' has an experimental theme ({et.get('id','')}: {et.get('name','')}) but no approved theme coverage.",
                    "recommendation": f"If experimental theme {et.get('id','')} advances, this sector will be covered.",
                    "evidence_refs": [et.get("id", "")],
                })

    # ── Type 4: Risk Blind Spot ──
    # Risk factor in evidence not tracked in any thesis key_risks
    all_tracked_risks = set()
    for _, tdata in queue:
        for c in tdata.get("candidates", []):
            for risk in c.get("key_risks", []):
                all_tracked_risks.add(risk[:80])  # first 80 chars as signature

    evidence = pipeline_result.get("evidence", [])
    contradicting = [ev for ev in evidence if ev.get("relationship") == "contradicting"]
    for ev in contradicting:
        risk_sig = ev.get("content", "")[:80]
        if risk_sig not in all_tracked_risks:
            gaps.append({
                "gap_type": "Risk Blind Spot",
                "severity": "High",
                "description": f"Contradicting evidence ({ev.get('id','')}) not reflected in any candidate's key_risks: {ev.get('content','')[:150]}",
                "affects_theme": ev.get("theme", ""),
                "recommendation": f"Add this risk to key_risks for all candidates in {ev.get('theme','')}.",
                "evidence_refs": [ev.get("id", "")],
            })
            all_tracked_risks.add(risk_sig)

    return gaps


def _assess_evidence_strength(theme_id: str, pipeline_result: dict) -> str:
    """Assess evidence strength for a theme (simple heuristic for V0)."""
    evidence = pipeline_result.get("evidence", [])
    theme_ev = [ev for ev in evidence if ev.get("theme") == theme_id]
    supporting = sum(1 for ev in theme_ev if ev.get("relationship") == "supporting")
    contradicting = sum(1 for ev in theme_ev if ev.get("relationship") == "contradicting")

    if supporting >= 3 and contradicting == 0:
        return "Strong"
    elif supporting >= 2:
        return "Moderate"
    elif supporting >= 1:
        return "Weak"
    else:
        return "No evidence"


def _get_evidence_refs(theme_id: str, pipeline_result: dict) -> list:
    """Get evidence IDs for a theme."""
    evidence = pipeline_result.get("evidence", [])
    return [ev.get("id", "") for ev in evidence if ev.get("theme") == theme_id]


def generate_gap_report(gaps: list, pipeline_result: dict,
                         run_id: str = None) -> str:
    """Generate a coverage gap report in markdown.

    Returns path to the generated file.
    """
    if run_id is None:
        run_id = pipeline_result.get("run_id", "unknown")

    pipeline_version = pipeline_result.get("pipeline_version", "v0.1.0")

    # Count by type
    type_counts = {}
    for g in gaps:
        gt = g.get("gap_type", "Other")
        type_counts[gt] = type_counts.get(gt, 0) + 1

    md = f"""# Coverage Gap Report
**Run:** {run_id}
**Date:** {datetime.date.today().strftime('%Y-%m-%d')}
**Pipeline Version:** {pipeline_version}
**Reviewer:** AI (deepseek-v4-pro — Parent)

---

## Summary

- **Gaps detected:** {len(gaps)}
"""
    for gt, count in type_counts.items():
        md += f"- **{gt}:** {count}\n"

    md += "\n---\n\n## Gap Details\n\n"

    for i, g in enumerate(gaps, 1):
        md += f"### {i}. {g['gap_type']}: {g.get('theme_name', g.get('ticker', g.get('sector', g.get('description','')))[:60])}\n\n"
        md += f"- **Severity:** {g.get('severity','N/A')}\n"
        md += f"- **Description:** {g.get('description','')}\n"
        if g.get("current_coverage") is not None:
            md += f"- **Current Coverage:** {g['current_coverage']} candidates\n"
        if g.get("evidence_strength"):
            md += f"- **Evidence Strength:** {g['evidence_strength']}\n"
        if g.get("appears_in"):
            md += f"- **Appears In:** {', '.join(g['appears_in'])}\n"
        if g.get("affects_theme"):
            md += f"- **Affects:** {g['affects_theme']}\n"
        if g.get("evidence_refs"):
            md += f"- **Evidence References:** {', '.join(g['evidence_refs'])}\n"
        md += f"- **Recommendation:** {g.get('recommendation','N/A')}\n\n"

    md += f"""---

## Founder Decisions Required

"""
    for i, g in enumerate(gaps, 1):
        md += f"- [ ] Gap {i}: {g.get('recommendation','')[:100]}\n"

    if not gaps:
        md += "- No gaps detected — no decisions required.\n"

    md += f"""
## Disposition

- **Next Review:** After next material pipeline run

---

*Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | AI Intelligence Layer (§23) | Gaps are surfaced, never acted upon automatically*
"""

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{date_str}-gap-report-{run_id.replace(':','-')}.md"
    filepath = os.path.join(GAPS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    return filepath
