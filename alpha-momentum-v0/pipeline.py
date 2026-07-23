"""
Alpha Momentum V0 — Pipeline (6 Stages)
Per PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md (DS-501 through DS-513)
All stages are deterministic — same input → same output.
No investment thresholds, weights, or formulas.
"""
from fixtures import (
    THEMES, EVIDENCE, ENTITIES, ASSETS, CANDIDATES,
    CANDIDATE_THEME, HUMAN_OVERRIDES, ALTERNATIVE_EXPLANATIONS,
    ANOMALIES, INBOX_HYPOTHESES,
    EXPERIMENTAL_THEMES, EXPERIMENTAL_CANDIDATES,
    EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_EVIDENCE,
    EXPERIMENTAL_ASSETS,
    PIPELINE_CONFIG, FIXTURE_CATEGORY,
)
from datetime import datetime

# ── Stage 0: Run metadata ─────────────────────────────────
RUN_ID = f"AM-V0-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
PIPELINE_VERSION = PIPELINE_CONFIG["pipeline_version"]

# ═══════════════════════════════════════════════════════════
# STAGE 1 — Universe Definition
# ═══════════════════════════════════════════════════════════
# DS-501: Operational V0 Universe Boundary in Pipeline Context
# DS-309: NYSE + NASDAQ + ADRs, fixture-defined
# DS-310: No additional eligibility criteria

def stage_universe(assets, candidates):
    """Select the controlled V0 universe. Returns all fixture candidates."""
    result = {
        "stage": "Universe Definition",
        "stage_id": "S1",
        "inputs": {"assets_count": len(assets), "candidates_count": len(candidates)},
        "rule": "DS-309: NYSE+NASDAQ+ADRs, fixture-defined",
        "passed": [c["id"] for c in candidates],
        "rejected": [],
        "output_count": len(candidates),
    }
    return result, {c["id"]: c for c in candidates}


# ═══════════════════════════════════════════════════════════
# STAGE 2 — Theme Context / Theme-linked Selection
# ═══════════════════════════════════════════════════════════
# DS-502: Theme Context Stage Behavior — Filter: must have >= 1 Theme

def stage_theme_context(candidates, candidate_theme, themes):
    """Filter: Candidate must have >= 1 Theme relationship."""
    # Build theme lookup
    theme_map = {t["id"]: t for t in themes}
    # Build candidate-theme index
    ct_index = {}
    for ct in candidate_theme:
        cid = ct["candidate_id"]
        if cid not in ct_index:
            ct_index[cid] = []
        ct_index[cid].append(ct)

    passed = {}
    rejected = []
    for cid, cdata in candidates.items():
        if cid in ct_index:
            cdata["_theme_relationships"] = ct_index[cid]
            passed[cid] = cdata
        else:
            rejected.append(cid)

    result = {
        "stage": "Theme Context",
        "stage_id": "S2",
        "rule": "DS-502: Filter — Candidate must have >= 1 Theme relationship",
        "theme_links_found": {cid: [ct["theme_id"] for ct in ct_index.get(cid, [])] for cid in passed},
        "passed_count": len(passed),
        "rejected_count": len(rejected),
        "rejected_ids": rejected,
    }
    return result, passed


# ═══════════════════════════════════════════════════════════
# STAGE 3 — Candidate Quality Assessment
# ═══════════════════════════════════════════════════════════
# DS-503: CQ — Enrichment (adds labels, does not filter)
# DS-301: 5 CQ domains — Fundamentals, Growth, Liquidity, RS, Trend Quality
# DS-304: Output — 2 groups: Trend & Participation, Tradeability & Growth

def stage_candidate_quality(candidates):
    """Enrich each candidate with quality dimension labels."""
    for cid, cdata in candidates.items():
        cq = cdata.get("candidate_quality", {})
        cdata["_cq_display"] = {
            "Group 1 — Trend & Participation": {
                "Relative Strength": cq.get("relative_strength", "N/A"),
                "Trend Quality": cq.get("trend_quality", "N/A"),
                "Accumulation": cq.get("accumulation", "N/A"),
            },
            "Group 2 — Tradeability & Growth": {
                "Fundamentals": cq.get("fundamentals", "N/A"),
                "Growth": cq.get("growth", "N/A"),
                "Liquidity": cq.get("liquidity", "N/A"),
            },
            "Industry Leadership": cq.get("industry_leadership", "N/A"),
        }

    result = {
        "stage": "Candidate Quality Assessment",
        "stage_id": "S3",
        "rule": "DS-503: Enrichment — adds quality labels, no filtering",
        "dimensions_assessed": len(candidates),
    }
    return result, candidates


# ═══════════════════════════════════════════════════════════
# STAGE 4 — Entry Readiness Assessment
# ═══════════════════════════════════════════════════════════
# DS-504: ER — Enrichment (adds labels, does not filter)
# DS-302: 4 ER domains — Base Quality, Volatility Contraction, Extension Risk, Breakout Proximity
# DS-305: Output — 2 groups: Pattern Quality, Entry Timing

def stage_entry_readiness(candidates):
    """Enrich each candidate with entry readiness labels."""
    for cid, cdata in candidates.items():
        er = cdata.get("entry_readiness", {})
        cdata["_er_display"] = {
            "Group 1 — Pattern Quality": {
                "Price Structure": er.get("price_structure", "N/A"),
                "Base Quality": er.get("base_quality", "N/A"),
                "Volatility Contraction": er.get("volatility_contraction", "N/A"),
            },
            "Group 2 — Entry Timing": {
                "Breakout Proximity": er.get("breakout_proximity", "N/A"),
                "Volume Behavior": er.get("volume_behavior", "N/A"),
                "Extension Risk": er.get("extension_risk", "N/A"),
            },
        }

    result = {
        "stage": "Entry Readiness Assessment",
        "stage_id": "S4",
        "rule": "DS-504: Enrichment — adds readiness labels, no filtering",
        "dimensions_assessed": len(candidates),
    }
    return result, candidates


# ═══════════════════════════════════════════════════════════
# STAGE 5 — Data Confidence Assessment
# ═══════════════════════════════════════════════════════════
# DS-505: DC — Warning (flags low confidence, does not filter)
# DS-401 through DS-412: Freshness, Completeness, Reliability, Independence, Conflicts, Missing

def stage_data_confidence(candidates):
    """Flag each candidate with data confidence."""
    for cid, cdata in candidates.items():
        dc = cdata.get("data_confidence", {})
        cdata["_dc_display"] = {
            "Freshness": dc.get("freshness", "N/A"),
            "Completeness": dc.get("completeness", "N/A"),
            "Reliability": dc.get("reliability", "N/A"),
            "Conflicts": dc.get("conflicts", "None"),
            "Missing Data": dc.get("missing_data", "None"),
        }
        # Determine warning level
        issues = 0
        if "Stale" in dc.get("freshness", ""): issues += 1
        if "Incomplete" in dc.get("completeness", ""): issues += 1
        if "conflicts" in dc and dc["conflicts"] != "None": issues += 1
        if issues >= 2:
            cdata["_dc_warning"] = "⚠️ Low Confidence"
        elif issues == 1:
            cdata["_dc_warning"] = "⚠️ Moderate Confidence"
        else:
            cdata["_dc_warning"] = "✅"

    result = {
        "stage": "Data Confidence Assessment",
        "stage_id": "S5",
        "rule": "DS-505: Warning — flags low confidence, does not filter",
        "dimensions_assessed": len(candidates),
    }
    return result, candidates


# ═══════════════════════════════════════════════════════════
# STAGE 6 — Research Queue Assembly
# ═══════════════════════════════════════════════════════════
# DS-506: Theme-first grouping
# DS-507: Unordered — no prioritization (templates inactive)
# DS-508: Show-all — no quality threshold
# DS-509: Empty queue = valid honest output
# HC-01: V0 fixed order: sector → industry
# HC-02: V0 lifecycle-prioritized grouping within theme

LIFECYCLE_ORDER = {"Expansion": 1, "Emerging Leadership": 2, "Formation": 3, "Crowded / Late": 4, "Deterioration": 5}

def stage_queue(candidates, candidate_theme, themes, theme_map):
    """Assemble the Research Queue — Theme-first with V0 ordering. Includes empty themes."""
    # Build candidate-theme index
    ct_by_theme = {}
    for ct in candidate_theme:
        tid = ct["theme_id"]
        if tid not in ct_by_theme:
            ct_by_theme[tid] = []
        ct_by_theme[tid].append(ct)

    # Populate all themes (including empty ones)
    queue_themes = {}
    all_theme_ids = {t["id"] for t in themes}
    for tid in all_theme_ids:
        queue_themes[tid] = {"theme": theme_map.get(tid, {}), "candidates": []}

    # Fill candidates for themes that have them
    for tid, ct_list in ct_by_theme.items():
        for ct in ct_list:
            cid = ct["candidate_id"]
            if cid in candidates:
                cdata = dict(candidates[cid])
                cdata["_ct_relationship"] = ct
                queue_themes[tid]["candidates"].append(cdata)

    # Sort themes: sector → industry (V0 HC-01)
    sorted_themes = sorted(queue_themes.items(), key=lambda x: (
        x[1]["theme"].get("sector", "ZZZ"),
        x[1]["theme"].get("industry", "ZZZ"),
    ))

    # Sort candidates within theme: lifecycle-prioritized (V0 HC-02)
    for tid, tdata in sorted_themes:
        tdata["candidates"].sort(key=lambda c: LIFECYCLE_ORDER.get(
            tdata["theme"].get("lifecycle", "Deterioration"), 5))

    # Count empty themes
    empty_themes = [tid for tid, tdata in sorted_themes if len(tdata["candidates"]) == 0]
    total_candidates = sum(len(td["candidates"]) for _, td in sorted_themes)

    result = {
        "stage": "Research Queue Assembly",
        "stage_id": "S6",
        "rule": "DS-506: Theme-first grouping | DS-507: Unordered | DS-508: Show-all",
        "themes_in_queue": len(sorted_themes),
        "themes_with_candidates": len(sorted_themes) - len(empty_themes),
        "empty_themes": empty_themes,
        "total_candidates": total_candidates,
        "empty_queue": total_candidates == 0,
    }
    return result, sorted_themes


# ═══════════════════════════════════════════════════════════
# PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════

def run_pipeline():
    """Execute all 6 pipeline stages. Returns stage outputs + final queue."""
    theme_map = {t["id"]: t for t in THEMES}
    stages = []
    candidates = {}

    # S1: Universe
    s1, candidates = stage_universe(ASSETS, CANDIDATES)
    stages.append(s1)

    # S2: Theme Context
    s2, candidates = stage_theme_context(candidates, CANDIDATE_THEME, THEMES)
    stages.append(s2)

    # S3: Candidate Quality
    s3, candidates = stage_candidate_quality(candidates)
    stages.append(s3)

    # S4: Entry Readiness
    s4, candidates = stage_entry_readiness(candidates)
    stages.append(s4)

    # S5: Data Confidence
    s5, candidates = stage_data_confidence(candidates)
    stages.append(s5)

    # S6: Queue
    s6, queue = stage_queue(candidates, CANDIDATE_THEME, THEMES, theme_map)
    stages.append(s6)

    pipeline_result = {
        "run_id": RUN_ID,
        "pipeline_version": PIPELINE_VERSION,
        "strategy": PIPELINE_CONFIG["strategy"],
        "point_in_time": PIPELINE_CONFIG["point_in_time"],
        "fixture_category": FIXTURE_CATEGORY,
        "stages": stages,
        "queue": queue,
        "evidence": EVIDENCE,
        "overrides": HUMAN_OVERRIDES,
        "alternative_explanations": ALTERNATIVE_EXPLANATIONS,
        "inbox_anomalies": ANOMALIES,
        "inbox_hypotheses": INBOX_HYPOTHESES,
        "experimental": run_experimental_pipeline(),
    }
    return pipeline_result


def run_experimental_pipeline():
    """Run the pipeline for Experimental themes only. Reuses same stage logic.
    Returns dict with stages, queue, evidence — separate from main pipeline."""
    if not EXPERIMENTAL_THEMES:
        return {"stages": [], "queue": [], "evidence": [], "has_data": False, "message": "No experimental themes defined"}

    theme_map = {t["id"]: t for t in EXPERIMENTAL_THEMES}
    stages = []
    candidates = {}

    # S1: Universe (experimental candidates)
    s1, candidates = stage_universe(EXPERIMENTAL_ASSETS, EXPERIMENTAL_CANDIDATES)
    stages.append(s1)

    # S2: Theme Context
    s2, candidates = stage_theme_context(candidates, EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_THEMES)
    stages.append(s2)

    # S3: Candidate Quality
    s3, candidates = stage_candidate_quality(candidates)
    stages.append(s3)

    # S4: Entry Readiness
    s4, candidates = stage_entry_readiness(candidates)
    stages.append(s4)

    # S5: Data Confidence
    s5, candidates = stage_data_confidence(candidates)
    stages.append(s5)

    # S6: Queue
    s6, queue = stage_queue(candidates, EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_THEMES, theme_map)
    stages.append(s6)

    return {
        "stages": stages,
        "queue": queue,
        "evidence": EXPERIMENTAL_EVIDENCE,
        "has_data": True,
        "message": f"{len(EXPERIMENTAL_THEMES)} themes, {len(EXPERIMENTAL_CANDIDATES)} candidates",
    }
