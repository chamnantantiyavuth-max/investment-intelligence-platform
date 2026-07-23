"""
⚠️ QUARANTINED — Phase 5 Experimental Pipeline
Moved from pipeline.py per WF-Phase 2R Architecture Review (23 Jul 2026).
Do NOT import this module from approved pipeline code.
"""
from fixtures import (
    ANOMALIES, INBOX_HYPOTHESES,
    EXPERIMENTAL_THEMES, EXPERIMENTAL_CANDIDATES,
    EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_EVIDENCE,
    EXPERIMENTAL_ASSETS,
)
from pipeline import (
    stage_universe, stage_theme_context, stage_candidate_quality,
    stage_entry_readiness, stage_data_confidence, stage_queue,
)


def run_experimental_pipeline():
    """Run the pipeline for Experimental themes only. Reuses same stage logic.
    ⚠️ This function is QUARANTINED — do NOT call from approved pipeline.

    Returns dict with stages, queue, evidence — separate from main pipeline."""
    if not EXPERIMENTAL_THEMES:
        return {"stages": [], "queue": [], "evidence": [], "has_data": False, "message": "No experimental themes defined"}

    theme_map = {t["id"]: t for t in EXPERIMENTAL_THEMES}
    stages = []
    candidates = {}

    s1, candidates = stage_universe(EXPERIMENTAL_ASSETS, EXPERIMENTAL_CANDIDATES)
    stages.append(s1)

    s2, candidates = stage_theme_context(candidates, EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_THEMES)
    stages.append(s2)

    s3, candidates = stage_candidate_quality(candidates)
    stages.append(s3)

    s4, candidates = stage_entry_readiness(candidates)
    stages.append(s4)

    s5, candidates = stage_data_confidence(candidates)
    stages.append(s5)

    s6, queue = stage_queue(candidates, EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_THEMES, theme_map)
    stages.append(s6)

    return {
        "stages": stages,
        "queue": queue,
        "evidence": EXPERIMENTAL_EVIDENCE,
        "has_data": True,
        "message": f"{len(EXPERIMENTAL_THEMES)} themes, {len(EXPERIMENTAL_CANDIDATES)} candidates",
    }
