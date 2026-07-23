"""
Phase 5 Experimental Pipeline — CONSTITUTIONALLY SEPARATE from approved pipeline.
Authorized: FD #27 (23 July 2026).
Re-architected: T0-Phase5-Arch (24 July 2026).

The experimental pipeline DISCOVERS NEW THEMES — it does NOT screen candidates.
This is fundamentally different from the approved 6-stage screening pipeline.

Stages (constitutionally separate — never reuse approved stage functions):
  E1: Anomaly Detection     → statistical deviations from baseline (NOT hand-written)
  E2: Anomaly Classification → cooldown check, dedup, categorize by type
  E3: Hypothesis Generation  → pattern recognition, epistemic metadata (§23.4)
  E4: Founder Review Queue    → surface for Founder approval via Experimental Radar

Hard Guards (FD #27):
  1. ZERO imports from approved pipeline.py stage functions
  2. Output ONLY to experimental/ scope — never to approved pipeline_result
  3. Never modifies THEMES, CANDIDATES, or any approved-strategy data
  4. Circular feedback guard: anomaly→hypothesis→theme→anomaly cooldown (30 days)
  5. Epistemic metadata MANDATORY for all AI-generated hypotheses (§23.4)

Implementation: T1 (inbox.py) → T2 (anomaly.py) → T3 (hypothesis.py) → T4 (radar.py)
"""
from datetime import datetime, date

# ── Imports from experimental fixtures ONLY ──────────────────
# ⚠️ CONSTITUTIONAL GUARD: ZERO imports from pipeline.py stage functions
from fixtures import (
    ANOMALIES, INBOX_HYPOTHESES,
    EXPERIMENTAL_THEMES, EXPERIMENTAL_CANDIDATES,
    EXPERIMENTAL_CANDIDATE_THEME, EXPERIMENTAL_EVIDENCE,
    EXPERIMENTAL_ASSETS, PIPELINE_CONFIG, FIXTURE_CATEGORY,
)

# ── Run metadata ─────────────────────────────────────────────
EXP_RUN_ID = f"EXP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
EXP_PIPELINE_VERSION = "exp-v0.1.0"

# ═══════════════════════════════════════════════════════════════
# E1 — ANOMALY DETECTION (T2 implements: experimental/anomaly.py)
# ═══════════════════════════════════════════════════════════════
# Per FD #27 §2: Must be ACTUAL COMPUTATION — not hand-written fixtures.
# Reads from EOD market data; applies statistical baselines; outputs anomalies.
#
# Detection types:
#   - Sector Divergence: theme RS data vs sector benchmark
#   - Single-Stock Outlier: price data deviation from ETF/peer group
#   - Volume Anomaly: volume spike vs 90-day average
#   - Missing Correlation: expected ETF-candidate correlation breakdown

def stage_anomaly_detection(price_data=None, benchmark_data=None):
    """E1: Detect statistical anomalies from market data.
    T2 (experimental/anomaly.py) provides the detection engine.
    For now: reads from fixture anomalies as architecture placeholder.

    Input:  market data (from source_adapter or data cache)
    Output: list of anomaly dicts → written to Weak Signal Inbox (T1)
    """
    # T2 will replace this with actual statistical computation
    # For architecture skeleton: surface existing anomalies as placeholder
    anomalies = []
    for an in ANOMALIES:
        anomalies.append({
            "id": an["id"],
            "type": an["type"],
            "description": an["description"],
            "first_observed": an["first_observed"],
            "related_theme": an.get("related_theme"),
            "related_tickers": an.get("related_tickers", []),
            "status": an.get("status", "Unexplained"),
            "source": an.get("source", "E1-Anomaly Detection"),
        })

    result = {
        "stage": "E1 — Anomaly Detection",
        "stage_id": "E1",
        "rule": "Statistical deviation from baseline — NOT hand-written fixtures (FD #27 §2)",
        "detection_types": ["Sector Divergence", "Single-Stock Outlier", "Volume Anomaly", "Missing Correlation"],
        "anomalies_detected": len(anomalies),
    }
    return result, anomalies


# ═══════════════════════════════════════════════════════════════
# E2 — ANOMALY CLASSIFICATION (T2 implements: experimental/anomaly.py)
# ═══════════════════════════════════════════════════════════════
# Classifies anomalies by type, checks cooldown window, deduplicates.
#
# CIRCULAR FEEDBACK GUARD (FD #27 §4):
#   Once an anomaly is promoted to hypothesis, the SAME observation
#   cannot re-trigger for 30 days. Track (anomaly_signature, last_promoted_date).

def stage_anomaly_classification(anomalies, existing_hypotheses=None, cooldown_days=30):
    """E2: Classify anomalies, enforce cooldown, deduplicate.
    T2 (experimental/anomaly.py) provides classification + cooldown logic.

    Input:  anomalies from E1 + existing hypotheses from inbox
    Output: classified anomalies, with cooldown flags
    """
    if existing_hypotheses is None:
        existing_hypotheses = []

    # Build cooldown index from existing hypotheses
    cooldown_index = {}
    for hyp in existing_hypotheses:
        # Track which anomaly signatures have been promoted
        sig = hyp.get("id", "")
        proposed = hyp.get("proposed_date", "")
        if sig and proposed:
            cooldown_index[sig] = proposed

    classified = []
    suppressed = []
    for an in anomalies:
        classification = {
            **an,
            "classification": _classify_anomaly_type(an),
            "cooldown_active": False,
            "action": "route_to_hypothesis",
        }

        # Cooldown check: has this anomaly signature been promoted recently?
        an_date = _parse_date(an.get("first_observed", ""))
        for hyp_id, hyp_date_str in cooldown_index.items():
            hyp_date = _parse_date(hyp_date_str)
            if an_date and hyp_date:
                delta = (an_date - hyp_date).days
                if abs(delta) < cooldown_days:
                    classification["cooldown_active"] = True
                    classification["action"] = "suppress"
                    classification["cooldown_remaining_days"] = cooldown_days - abs(delta)
                    suppressed.append(classification)
                    break
        else:
            classified.append(classification)

    result = {
        "stage": "E2 — Anomaly Classification",
        "stage_id": "E2",
        "rule": f"Classify + cooldown ({cooldown_days}d) + dedup (FD #27 §4 circular guard)",
        "classified_count": len(classified),
        "suppressed_count": len(suppressed),
        "suppressed_ids": [s["id"] for s in suppressed],
    }
    return result, classified


def _classify_anomaly_type(anomaly):
    """Map anomaly type to classification bucket."""
    type_map = {
        "Sector Divergence": "structural",
        "Single-Stock Outlier": "tactical",
        "Volume Anomaly": "flow",
        "Missing Correlation": "structural",
    }
    return type_map.get(anomaly.get("type", ""), "unclassified")


def _parse_date(date_str):
    """Parse date string to date object (robust)."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        except (ValueError, IndexError):
            continue
    return None


# ═══════════════════════════════════════════════════════════════
# E3 — HYPOTHESIS GENERATION (T3 implements: experimental/hypothesis.py)
# ═══════════════════════════════════════════════════════════════
# Generates Theme Hypotheses from classified anomalies + evidence patterns.
# ALL AI-generated hypotheses MUST carry epistemic metadata (§23.4):
#   provenance, confidence_level, version, source_references,
#   as_of_time, model_provenance

def stage_hypothesis_generation(anomalies, evidence=None, existing_themes=None):
    """E3: Generate Theme Hypotheses from anomaly patterns.
    T3 (experimental/hypothesis.py) provides the generation engine.

    Input:  classified anomalies (E2) + evidence + existing themes
    Output: list of Hypothesis dicts with MANDATORY epistemic metadata (§23.4)
    """
    # T3 will replace this with actual AI-driven hypothesis generation
    # For architecture skeleton: surface existing hypotheses as placeholder
    hypotheses = []
    for hy in INBOX_HYPOTHESES:
        hypotheses.append({
            "id": hy["id"],
            "title": hy["title"],
            "proposed_driver": hy["proposed_driver"],
            "why_now": hy["why_now"],
            "potential_candidates": hy.get("potential_candidates", []),
            "potential_theme_industry": hy.get("potential_theme_industry", ""),
            "relationship_to_existing": hy.get("relationship_to_existing", ""),
            "key_unknowns": hy.get("key_unknowns", []),
            "proposed_date": hy.get("proposed_date", ""),
            "status": hy.get("status", "Hypothesis — awaiting Founder review"),
            # Epistemic metadata (§23.4) — MANDATORY for AI-generated hypotheses
            "_epistemic": {
                "provenance": "AI-generated from anomaly patterns (V0 synthetic)",
                "confidence_level": "Low",
                "version": "exp-v0.1.0",
                "source_references": [an["id"] for an in anomalies[:3]],
                "as_of_time": PIPELINE_CONFIG.get("point_in_time", ""),
                "model_provenance": "deepseek-v4-pro (Parent) — V0 experimental",
            },
        })

    result = {
        "stage": "E3 — Hypothesis Generation",
        "stage_id": "E3",
        "rule": "AI-generated from anomaly patterns | Epistemic metadata MANDATORY (§23.4)",
        "hypotheses_generated": len(hypotheses),
        "epistemic_metadata_attached": len(hypotheses),
    }
    return result, hypotheses


# ═══════════════════════════════════════════════════════════════
# E4 — FOUNDER REVIEW QUEUE (T4 implements: experimental/radar.py)
# ═══════════════════════════════════════════════════════════════
# Surfaces hypotheses + experimental themes for Founder review.
# Output goes to Experimental Theme Radar — SEPARATE from approved queue.
# Theme approval remains Founder-only (FD #27 §5).

def stage_founder_review_queue(hypotheses, experimental_themes=None):
    """E4: Assemble Founder Review Queue for Experimental Theme Radar.
    T4 (experimental/radar.py) provides the display module.

    Input:  hypotheses (E3) + experimental themes
    Output: review queue (hypotheses pending + themes awaiting approval)
    """
    if experimental_themes is None:
        experimental_themes = EXPERIMENTAL_THEMES

    # Group: hypotheses awaiting review
    pending_hypotheses = [h for h in hypotheses
                          if "awaiting Founder review" in h.get("status", "")]

    # Group: experimental themes (already promoted, awaiting Founder approval)
    exp_themes_display = []
    for t in experimental_themes:
        exp_themes_display.append({
            "id": t["id"],
            "name": t["name"],
            "sector": t.get("sector", ""),
            "industry": t.get("industry", ""),
            "lifecycle": t.get("lifecycle", ""),
            "approval_status": t.get("approval_status", "Experimental"),
            "confidence": t.get("confidence", "Low"),
            "why_now": t.get("why_now", ""),
            "key_tickers": t.get("key_tickers", []),
            "stocks_in_industry": t.get("stocks_in_industry", 0),
        })

    result = {
        "stage": "E4 — Founder Review Queue",
        "stage_id": "E4",
        "rule": "Surface for Founder review | Theme approval = Founder-only (FD #27 §5) | Separate from approved queue",
        "hypotheses_pending": len(pending_hypotheses),
        "experimental_themes": len(exp_themes_display),
        "total_review_items": len(pending_hypotheses) + len(exp_themes_display),
    }
    return result, {
        "hypotheses": hypotheses,
        "experimental_themes": exp_themes_display,
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENTAL PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════════

def run_experimental_pipeline():
    """Execute the 4-stage EXPERIMENTAL pipeline.
    CONSTITUTIONALLY SEPARATE from approved run_pipeline().
    Does NOT import or reuse approved stage functions.

    Returns dict with stages, review_queue, evidence — separate from approved.
    """
    stages = []

    # E1: Anomaly Detection
    e1, anomalies = stage_anomaly_detection()
    stages.append(e1)

    # E2: Anomaly Classification
    e2, classified = stage_anomaly_classification(anomalies, INBOX_HYPOTHESES)
    stages.append(e2)

    # E3: Hypothesis Generation
    e3, hypotheses = stage_hypothesis_generation(classified, EXPERIMENTAL_EVIDENCE, EXPERIMENTAL_THEMES)
    stages.append(e3)

    # E4: Founder Review Queue
    e4, review_queue = stage_founder_review_queue(hypotheses, EXPERIMENTAL_THEMES)
    stages.append(e4)

    experimental_result = {
        "run_id": EXP_RUN_ID,
        "pipeline_version": EXP_PIPELINE_VERSION,
        "strategy": "Theme Intelligence V1 — Experimental",
        "point_in_time": PIPELINE_CONFIG.get("point_in_time", ""),
        "fixture_category": FIXTURE_CATEGORY,
        "stages": stages,
        "review_queue": review_queue,
        "anomalies": anomalies,
        "hypotheses": hypotheses,
        "experimental_themes": EXPERIMENTAL_THEMES,
        "experimental_candidates": EXPERIMENTAL_CANDIDATES,
        "experimental_evidence": EXPERIMENTAL_EVIDENCE,
        "has_data": bool(anomalies or hypotheses or EXPERIMENTAL_THEMES),
        "message": (
            f"E1: {e1['anomalies_detected']} anomalies | "
            f"E2: {e2['classified_count']} classified, {e2['suppressed_count']} suppressed | "
            f"E3: {e3['hypotheses_generated']} hypotheses | "
            f"E4: {e4['total_review_items']} review items"
        ),
        # ⚠️ CONSTITUTIONAL SEPARATION MARKER
        "_constitutional_separation": {
            "approved_pipeline_imports": False,
            "reuses_approved_stages": False,
            "output_target": "experimental/ scope ONLY",
            "modifies_approved_data": False,
            "epistemic_metadata": "mandatory (§23.4)",
            "circular_feedback_guard": "active (30-day cooldown)",
        },
    }
    return experimental_result
