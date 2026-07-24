"""
Phase 6: Learning Loop — Self-Reflection Log
Authorized: FD #28 (24 July 2026)

Generates structured 7-section markdown after every material pipeline run.
Per LEARNING-AND-KNOWLEDGE-LOOP.md + self-reflection-template.md.

AI-generated drafts — Founder-reviewed before becoming official knowledge.

ERP-005 (FD #38): SRL trigger criteria — generate ONLY on material changes,
NOT on routine daily runs or docs-only edits.
"""
import os, json, datetime, re
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS_DIR = os.path.join(REPO_ROOT, "operational", "self-reflection-logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# ── Section Labels ───────────────────────────────────────────
SECTIONS = [
    "Run Context",
    "Thesis Status Changes",
    "Surprises",
    "Mistakes Identified",
    "Lessons",
    "Open Questions",
    "Blind Spots",
]


def _find_prior_logs() -> list:
    """Find previous self-reflection logs, sorted newest first."""
    logs = []
    if not os.path.exists(LOGS_DIR):
        return logs
    for fname in sorted(os.listdir(LOGS_DIR), reverse=True):
        if fname.endswith(".md") and fname != "template.md":
            logs.append(os.path.join(LOGS_DIR, fname))
    return logs


def _extract_thesis_changes(current: dict, prior_log_path: str = None) -> list:
    """Compare current thesis states vs prior run to detect changes.
    Returns list of (candidate_id, ticker, old_status, new_status, evidence_refs)."""
    changes = []
    candidates = []
    for _, tdata in current.get("queue", []):
        for c in tdata.get("candidates", []):
            candidates.append({
                "id": c.get("id", ""),
                "ticker": c.get("ticker", ""),
                "research_state": c.get("research_state", ""),
                "thesis_status": c.get("thesis_status", ""),
            })

    # For V0: detect changes from prior log (simple parsing)
    # If no prior log, mark all as "initial assessment"
    if not prior_log_path:
        for c in candidates:
            changes.append({
                "candidate": c["ticker"],
                "change": "Initial assessment",
                "detail": f"First run — {c['research_state']}, thesis: {c.get('thesis_status','N/A')}",
            })
        return changes

    # TODO Phase 6B: parse prior log for thesis states and compute diffs
    return changes


def _detect_surprises(anomalies: list, hypotheses: list) -> list:
    """Extract surprises from anomalies and hypothesis patterns."""
    surprises = []
    for an in anomalies:
        surprises.append({
            "source": f"Anomaly {an.get('id','')}",
            "type": an.get("type", ""),
            "observation": an.get("description", "")[:200],
        })
    for hy in hypotheses:
        surprises.append({
            "source": f"Hypothesis {hy.get('id','')}",
            "observation": f"New theme proposed: {hy.get('title','')} — {hy.get('proposed_driver','')[:150]}",
        })
    return surprises


def _detect_blind_spots(pipeline_result: dict, gaps: list = None) -> list:
    """Identify themes/candidates/risks present in evidence but absent from Watchlist."""
    blind_spots = []

    # Theme blind spots: empty themes in queue
    for tid, tdata in pipeline_result.get("queue", []):
        if len(tdata.get("candidates", [])) == 0:
            theme = tdata.get("theme", {})
            blind_spots.append({
                "type": "Empty Theme",
                "detail": f"{tid}: {theme.get('name','')} — has evidence but zero candidates in Watchlist",
                "sector": theme.get("sector", ""),
            })

    # Coverage gap blind spots (from gaps.py)
    if gaps:
        for g in gaps:
            blind_spots.append({
                "type": g.get("gap_type", "Unknown"),
                "detail": g.get("description", ""),
                "recommendation": g.get("recommendation", ""),
            })

    return blind_spots


# ═══════════════════════════════════════════════════════════════
# ERP-005 (FD #38): SRL Trigger Criteria
# ═══════════════════════════════════════════════════════════════

def should_generate_srl(pipeline_result: dict, prior_state: dict = None,
                         trigger_context: str = None) -> tuple:
    """Determine if SRL should be generated per ERP-005 trigger criteria.

    Triggers (any one = generate):
      (1) Candidate count changed vs prior state
      (2) Thesis status or conviction level changed
      (3) Founder review session occurred (trigger_context='founder_review')
      (4) Coverage gap was resolved (trigger_context='gap_resolved')

    Suppressed:
      - Routine daily runs with zero changes
      - Docs-only edits (trigger_context='docs_only')

    Returns (should_generate: bool, reason: str).
    """
    # Docs-only edits → suppress
    if trigger_context == "docs_only":
        return False, "ERP-005: docs-only edit — SRL suppressed"

    # Founder review or gap resolution → always generate
    if trigger_context in ("founder_review", "gap_resolved"):
        return True, f"ERP-005 trigger: {trigger_context}"

    # Check for candidate count changes
    current_count = sum(len(td.get("candidates", []))
                        for _, td in pipeline_result.get("queue", []))
    if prior_state:
        prior_count = prior_state.get("candidate_count", -1)
        if prior_count >= 0 and current_count != prior_count:
            return True, (
                f"ERP-005 trigger (1): candidate count changed "
                f"({prior_count} → {current_count})"
            )

        # Check thesis/conviction changes
        prior_theses = prior_state.get("thesis_snapshot", {})
        current_theses = _snapshot_theses(pipeline_result)
        if prior_theses != current_theses:
            changed = []
            for tid, info in current_theses.items():
                prior_info = prior_theses.get(tid, {})
                if prior_info != info:
                    changed.append(tid)
            return True, (
                f"ERP-005 trigger (2): thesis/conviction changed for {changed}"
            )

    # No changes detected → check if this is a routine run
    if trigger_context == "routine_daily":
        return False, "ERP-005: routine daily run with zero changes — SRL suppressed"

    # First run or no prior state → generate (initial baseline)
    return True, "ERP-005: first run or no prior state — generating baseline SRL"


def _snapshot_theses(pipeline_result: dict) -> dict:
    """Take a snapshot of current thesis states for change detection."""
    snapshot = {}
    for _, tdata in pipeline_result.get("queue", []):
        for c in tdata.get("candidates", []):
            tid = c.get("ticker", c.get("id", "?"))
            snapshot[tid] = {
                "thesis_status": c.get("thesis_status", ""),
                "conviction_level": c.get("conviction_level", ""),
            }
    return snapshot


def build_prior_state(pipeline_result: dict) -> dict:
    """Build a prior state dict for the next run to compare against."""
    queue = pipeline_result.get("queue", [])
    return {
        "candidate_count": sum(len(td.get("candidates", [])) for _, td in queue),
        "thesis_snapshot": _snapshot_theses(pipeline_result),
    }


# ═══════════════════════════════════════════════════════════════
# SRL Generator
# ═══════════════════════════════════════════════════════════════

def generate_self_reflection(pipeline_result: dict, exp_result: dict = None,
                              prior_log: str = None, run_id: str = None,
                              trigger_reason: str = None) -> str:
    """Generate a 7-section self-reflection log in markdown.

    Args:
        pipeline_result: Approved pipeline output (from pipeline.run_pipeline())
        exp_result: Experimental pipeline output (optional, from experimental.pipeline)
        prior_log: Path to most recent prior self-reflection log
        run_id: Run identifier (defaults to pipeline_result['run_id'])
        trigger_reason: ERP-005 trigger reason string

    Returns:
        Path to the generated markdown file.
    """
    if run_id is None:
        run_id = pipeline_result.get("run_id", datetime.datetime.now().strftime("AM-V0-%Y%m%d-%H%M%S"))

    pipeline_version = pipeline_result.get("pipeline_version", "v0.1.0")
    point_in_time = pipeline_result.get("point_in_time", str(datetime.date.today()))
    fixture_category = pipeline_result.get("fixture_category", "SYNTHETIC")

    # Gather data
    anomalies = exp_result.get("anomalies", []) if exp_result else []
    hypotheses = exp_result.get("hypotheses", []) if exp_result else []
    thesis_changes = _extract_thesis_changes(pipeline_result, prior_log)
    surprises = _detect_surprises(anomalies, hypotheses)
    blind_spots = _detect_blind_spots(pipeline_result)

    # Theme/candidate stats
    queue = pipeline_result.get("queue", [])
    theme_count = len(queue)
    total_candidates = sum(len(td.get("candidates", [])) for _, td in queue)
    empty_themes = sum(1 for _, td in queue if len(td.get("candidates", [])) == 0)

    # Prior log reference
    prior_ref = os.path.basename(prior_log) if prior_log else "None — first run"

    # ── Build markdown ──
    md = f"""# Self-Reflection Log
**Run:** {run_id}
**Date:** {datetime.date.today().strftime('%Y-%m-%d')}
**Pipeline Version:** {pipeline_version}
**Point-in-Time:** {point_in_time}
**Prior Log:** {prior_ref}
**ERP-005 Trigger:** {trigger_reason or 'Not specified'}

---

## 1. Run Context

- **Pipeline:** {pipeline_version} ({fixture_category})
- **Themes evaluated:** {theme_count} ({theme_count - empty_themes} with candidates, {empty_themes} empty)
- **Candidates assessed:** {total_candidates}
- **Experimental:** {len(anomalies)} anomalies, {len(hypotheses)} hypotheses, {len(exp_result.get('experimental_themes', [])) if exp_result else 0} experimental themes
- **Special conditions:** {"Phase 5 active — experimental pipeline running in parallel" if exp_result else "Standard run"}

## 2. Thesis Status Changes

"""
    if thesis_changes:
        for tc in thesis_changes:
            md += f"- **{tc['candidate']}**: {tc['change']} — {tc['detail']}\n"
    else:
        md += "- No thesis status changes detected in this run.\n"

    md += """
## 3. Surprises

"""
    if surprises:
        for s in surprises:
            md += f"- **[{s['source']}]** {s.get('type','') + ': ' if s.get('type') else ''}{s['observation']}\n"
    else:
        md += "- No surprises detected in this run.\n"

    md += """
## 4. Mistakes Identified

"""
    md += "- _[AI assessment pending — review prior log for contradicted predictions]_\n"

    md += """
## 5. Lessons

"""
    md += "- _[AI assessment pending — extract patterns from thesis changes and surprises]_\n"

    md += """
## 6. Open Questions

"""
    if hypotheses:
        for hy in hypotheses:
            for uk in hy.get("key_unknowns", [])[:3]:
                md += f"- [{hy.get('id','')}] {uk}\n"
    if empty_themes > 0:
        md += f"- {empty_themes} approved themes have zero candidates — is Watchlist coverage adequate?\n"

    md += """
## 7. Blind Spots

"""
    if blind_spots:
        for bs in blind_spots:
            md += f"- **[{bs['type']}]** {bs['detail']}\n"
            if bs.get("recommendation"):
                md += f"  → {bs['recommendation']}\n"
    else:
        md += "- No blind spots identified in this run.\n"

    md += f"""

---

*Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | AI Intelligence Layer (§23) | Draft — not official knowledge until Founder reviews*
"""

    # ── Write to file ──
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{date_str}-run-{run_id.replace(':','-')}.md"
    filepath = os.path.join(LOGS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    return filepath
