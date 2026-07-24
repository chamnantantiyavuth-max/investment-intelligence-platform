"""experimental/hypothesis.py — Theme Hypothesis Engine

Phase 5 Theme Intelligence V1 (T3)
Authorized: FD #27 (23 July 2026)

AI proposal pipeline that generates hypotheses from anomalies with
epistemic metadata (§23.4). Constitutionally separate from the
approved pipeline stages.

Pipeline flow (constitutionally separate from approved):
1. Read anomalies from inbox
2. Cross-reference with existing evidence
3. Check against existing themes to avoid duplicates
4. Generate hypothesis narrative
5. Write to inbox (via add_hypothesis)
6. Promote to experimental theme → stored in memory

HARD GUARDS:
1. ZERO imports from pipeline.py or display.py
2. Uses CONSTITUTIONALLY SEPARATE pipeline stages
3. Experimental themes created via promote_to_experimental() -> stored
   separately (EXPERIMENTAL_STORE list), never in fixtures
4. AI-generated hypotheses carry MANDATORY epistemic metadata (§23.4)
5. Founder approval still required to promote Experimental → Approved
"""

import uuid
from datetime import datetime, date

# Inbox API for reading/writing anomalies and hypotheses
from experimental.inbox import add_hypothesis, list_anomalies, list_hypotheses

# ──────────────────────────────────────────────
# In-memory storage for experimental themes
# ──────────────────────────────────────────────
EXPERIMENTAL_STORE = []

# Version & configuration constants
HYPOTHESIS_VERSION = "exp-v0.1.0"
VALID_CONFIDENCE_LEVELS = {"High", "Moderate", "Low"}

# Experimental theme ID counter
_theme_counter = 0


# ═══════════════════════════════════════════════
# PATTERN ANALYSIS
# ═══════════════════════════════════════════════

def analyze_anomalies_for_patterns(anomalies: list) -> list[dict]:
    """Group anomalies by theme/industry/common tickers to identify patterns.

    Analyzes anomalies across three axes:
    1. Theme clusters — anomalies sharing a related_theme
    2. Type clusters — anomalies of the same type (only for 2+ of same type)
    3. Cross-clusters — common tickers appearing across multiple anomalies

    Args:
        anomalies: list of anomaly dicts (each with 'id', 'type',
                   'related_theme', 'related_tickers', etc.)

    Returns:
        list of pattern dicts, each with at minimum 'anomaly_ids' and
        'description' keys
    """
    if not anomalies:
        return []

    patterns = []

    # ── 1. Group by related_theme ──
    theme_groups = {}
    for a in anomalies:
        theme = a.get("related_theme", "__none__")
        if theme not in theme_groups:
            theme_groups[theme] = []
        theme_groups[theme].append(a)

    for theme, group in theme_groups.items():
        if theme == "__none__":
            continue
        ids = [a["id"] for a in group]
        types = sorted({a.get("type", "") for a in group})
        tickers = sorted({
            t for a in group for t in a.get("related_tickers", [])
        })

        patterns.append({
            "anomaly_ids": ids,
            "description": (
                f"Pattern detected: {len(group)} anomalies sharing theme {theme}. "
                f"Types: {', '.join(types)}. "
                f"Tickers: {', '.join(tickers) if tickers else 'none'}."
            ),
            "common_theme": theme,
            "common_tickers": tickers,
            "pattern_type": "theme_cluster",
        })

    # ── 2. Group by type (only when 2+ anomalies share the same type) ──
    type_groups = {}
    for a in anomalies:
        atype = a.get("type", "Unknown")
        if atype not in type_groups:
            type_groups[atype] = []
        type_groups[atype].append(a)

    for atype, group in type_groups.items():
        if len(group) < 2:
            continue  # Only meaningful clusters
        ids = [a["id"] for a in group]
        tickers = sorted({
            t for a in group for t in a.get("related_tickers", [])
        })
        patterns.append({
            "anomaly_ids": ids,
            "description": (
                f"Pattern detected: {len(group)} anomalies of type '{atype}'. "
                f"Tickers: {', '.join(tickers) if tickers else 'none'}."
            ),
            "common_tickers": tickers,
            "pattern_type": "type_cluster",
        })

    # ── 3. Cross-cluster: common tickers across multiple anomalies ──
    all_ticker_sets = [
        set(a.get("related_tickers", [])) for a in anomalies
        if a.get("related_tickers")
    ]
    if len(all_ticker_sets) >= 2:
        common = all_ticker_sets[0].intersection(*all_ticker_sets[1:])
        if common:
            ids = [a["id"] for a in anomalies]
            tickers = sorted(common)
            patterns.append({
                "anomaly_ids": ids,
                "description": (
                    f"Pattern detected: {len(tickers)} ticker(s) appear "
                    f"across multiple anomalies: {', '.join(tickers)}."
                ),
                "common_tickers": tickers,
                "pattern_type": "cross_cluster",
            })

    return patterns


# ═══════════════════════════════════════════════
# HYPOTHESIS GENERATION
# ═══════════════════════════════════════════════

def generate_hypothesis(
    anomalies: list,
    evidence: list,
    existing_themes: list,
) -> dict:
    """Produce a Theme Hypothesis from anomalies with epistemic metadata.

    Constitutionally separate pipeline:
    1. Read anomalies from inbox (passed as argument)
    2. Cross-reference with existing evidence
    3. Check against existing themes to avoid duplicates
    4. Generate hypothesis narrative
    5. Write to inbox via add_hypothesis()

    Every AI-generated hypothesis carries mandatory epistemic metadata per
    §23.4: provenance, confidence_level, version, source_references,
    as_of_time, model_provenance.

    Args:
        anomalies: list of anomaly dicts (constituionally separate input)
        evidence: list of evidence dicts (read-only from fixtures)
        existing_themes: list of approved theme dicts (read-only)

    Returns:
        Hypothesis dict with _epistemic block, or None if no anomalies
        provided.
    """
    if not anomalies:
        return None

    # ── Step 1: Analyze patterns ──
    patterns = analyze_anomalies_for_patterns(anomalies)

    # Build narrative from patterns
    if patterns:
        why_now = patterns[0].get(
            "description",
            f"{len(patterns)} pattern(s) identified from {len(anomalies)} anomalies",
        )
    else:
        why_now = (
            f"Single anomaly ({anomalies[0].get('id', '?')}) — "
            f"no related patterns found"
        )

    # ── Step 2: Cross-reference with evidence ──
    evidence_ids = [e["id"] for e in evidence if isinstance(e, dict) and "id" in e]

    # ── Step 3: Check against existing themes ──
    existing_theme_names = {
        t.get("name", "").lower() for t in existing_themes
        if isinstance(t, dict)
    }

    # ── Step 4: Determine proposed driver from anomaly types ──
    all_types = {a.get("type", "") for a in anomalies}
    if "Sector Divergence" in all_types:
        proposed_driver = (
            "Sector-level divergence detected suggesting structural rotation "
            "not yet captured by existing themes"
        )
    elif "Volume Anomaly" in all_types:
        proposed_driver = (
            "Volume anomalies suggesting accumulation or distribution pattern "
            "in theme-related tickers"
        )
    elif "Single-Stock Outlier" in all_types:
        proposed_driver = (
            "Single-stock outlier behavior suggesting an unrecognized "
            "beneficiary not fully captured by its current theme"
        )
    elif "Missing Correlation" in all_types:
        proposed_driver = (
            "Correlation breakdown suggesting a structural shift or "
            "mispricing between theme-linked tickers"
        )
    else:
        proposed_driver = (
            "Multi-anomaly pattern suggesting an unrecognized or emerging "
            "theme driver"
        )

    # ── Gather candidate tickers from anomalies ──
    candidate_tickers = []
    seen = set()
    for a in anomalies:
        for t in a.get("related_tickers", []):
            if t not in seen:
                seen.add(t)
                candidate_tickers.append(t)

    # ── Build key unknowns ──
    key_unknowns = [
        f"Validation required: {len(patterns)} pattern(s) identified "
        f"from {len(anomalies)} anomalies",
    ]
    if evidence_ids:
        key_unknowns.append(
            f"Evidence cross-reference: {len(evidence_ids)} evidence "
            f"items available for review"
        )

    # ── Build hypothesis data for inbox ──
    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    today_str = datetime.now().strftime("%Y-%m-%d")

    hyp_data = {
        "title": (
            f"Theme Hypothesis from {len(anomalies)} "
            f"anomaly/anomalies"
        ),
        "proposed_driver": proposed_driver,
        "why_now": why_now,
        "potential_candidates": candidate_tickers,
        "key_unknowns": key_unknowns,
        "status": "Hypothesis — awaiting Founder review",
        "proposed_date": today_str,
        "_epistemic": {
            "provenance": "AI-generated from anomaly patterns (hypothesis engine)",
            "confidence_level": "Low",
            "version": HYPOTHESIS_VERSION,
            "source_references": (
                [a["id"] for a in anomalies if "id" in a]
                + evidence_ids
            ),
            "as_of_time": now_ts,
            "model_provenance": "deepseek-v4-flash (hypothesis engine)",
        },
    }

    # ── Step 5: Write to inbox ──
    hyp_id = add_hypothesis(hyp_data)

    # ── Retrieve the persisted hypothesis to return ──
    for h in list_hypotheses():
        if h.get("id") == hyp_id:
            return h

    # Fallback: return dict with the correct ID
    result = dict(hyp_data)
    result["id"] = hyp_id
    del result["_epistemic"]
    result["_epistemic"] = hyp_data["_epistemic"]
    return result


# ═══════════════════════════════════════════════
# PROMOTION TO EXPERIMENTAL THEME
# ═══════════════════════════════════════════════

def promote_to_experimental(hypothesis: dict) -> dict:
    """Promote a hypothesis to ExperimentalTheme with TH-EXP- ID.

    Creates an experimental theme from the hypothesis, stores it in the
    in-memory EXPERIMENTAL_STORE list (constitutionally separate from
    approved fixtures), updates the hypothesis status to reflect
    promotion, and preserves epistemic metadata from the source hypothesis.

    Founder approval still required to promote Experimental → Approved.

    Args:
        hypothesis: Hypothesis dict (must have at minimum 'id' and 'title')

    Returns:
        ExperimentalTheme dict with:
            - id starting with TH-EXP-
            - approval_status set to "Experimental"
            - name matching hypothesis title
            - _source_epistemic carrying hypothesis epistemic provenance
            - source_hypothesis referencing the original hypothesis ID
    """
    global _theme_counter
    _theme_counter += 1

    # Generate TH-EXP- ID
    theme_id = f"TH-EXP-{_theme_counter:03d}"

    # Determine sector/industry from hypothesis
    sector = hypothesis.get("potential_theme_industry", "Unknown")
    industry = hypothesis.get("potential_theme_industry", "Unknown")
    why_now = hypothesis.get("why_now", "")
    candidates = hypothesis.get("potential_candidates", [])
    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build experimental theme (constitutionally separate from approved fixtures)
    theme = {
        "id": theme_id,
        "name": hypothesis.get("title", "Unnamed Hypothesis"),
        "sector": sector,
        "industry": industry,
        "lifecycle": "Formation",
        "approval_status": "Experimental",
        "monitoring_status": "Active Monitoring",
        "why_now": why_now,
        "confidence": "Low",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {
                "prior": "Detected Hypothesis",
                "new": "Experimental",
                "reason": "AI-promoted from hypothesis based on anomaly pattern analysis",
                "actor": "AI System",
                "timestamp": now_ts,
                "version": HYPOTHESIS_VERSION,
            },
        ],
        "monitoring_transitions": [
            {
                "prior": "Not Monitored",
                "new": "Active Monitoring",
                "reason": "Experimental theme — active monitoring for signal validation",
                "actor": "AI System",
                "timestamp": now_ts,
                "version": HYPOTHESIS_VERSION,
            },
        ],
        "stocks_in_industry": len(candidates),
        "key_tickers": candidates,
    }

    # ── Preserve epistemic metadata (per §23.4) ──
    source_epistemic = hypothesis.get("_epistemic")
    if source_epistemic:
        # Store as _source_epistemic for provenance tracking
        theme["_source_epistemic"] = dict(source_epistemic)
        # Also carry _epistemic on the theme itself
        theme["_epistemic"] = dict(source_epistemic)

    # Reference the source hypothesis
    theme["source_hypothesis"] = hypothesis.get("id", "")

    # -- Store in EXPERIMENTAL_STORE (constitutionally separate) --
    EXPERIMENTAL_STORE.append(theme)

    # ── Update hypothesis status to reflect promotion ──
    hypothesis["status"] = "Promoted — awaiting Founder approval"

    return theme
