"""
Close System Product Radar V0 — Pipeline (6 Stages)
Per CLOSE-SYSTEM-PRODUCT-RADAR.md (PD-v0.1, FD #39, 25 July 2026)

Pipeline filters products through P1-P3 eligibility gates,
synthesizes 5-layer intelligence into conviction, and
assembles a prioritized product radar for Founder review.

All stages are deterministic — same input → same output.
No automated scoring, no broker/execution/capital allocation.
"""
from fixtures import PRODUCTS, PIPELINE_CONFIG
from datetime import datetime

RUN_ID = f"CS-V0-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
PIPELINE_VERSION = PIPELINE_CONFIG["pipeline_version"]

RECOMMENDATION_RANK = {
    "Present to Founder": 1,
    "Deep Research": 2,
    "Add to Radar Watchlist": 3,
    "Monitor — Wait for Better Price": 4,
    "Ineligible": 5,
}


# ═══════════════════════════════════════════════════════════
# STAGE 1 — Universe Definition
# ═══════════════════════════════════════════════════════════

def stage_universe(products):
    """Select all products in the Close System radar scope."""
    selected = [p for p in products]  # V0: all products pass universe
    return {
        "stage_id": "S1",
        "stage": "Universe Definition",
        "total_products": len(products),
        "selected_count": len(selected),
    }, selected


# ═══════════════════════════════════════════════════════════
# STAGE 2 — P1: Cannot Go to Zero
# ═══════════════════════════════════════════════════════════

def stage_p1_eligibility(products):
    """Filter: product must satisfy Criterion P1 (cannot go to zero by nature)."""
    eligible = []
    ineligible = []
    for p in products:
        if p.get("p1_eligible", False):
            eligible.append(p)
        else:
            ineligible.append({
                "id": p["id"],
                "ticker": p["ticker"],
                "name": p["name"],
                "reason": p.get("p1_rationale", "Fails P1 — cannot guarantee non-zero value by structure."),
                "status": "P1 FAIL",
            })
    return {
        "stage_id": "S2",
        "stage": "P1 — Cannot Go to Zero",
        "input_count": len(products),
        "passed_count": len(eligible),
        "rejected_count": len(ineligible),
        "rejected": ineligible,
    }, eligible


# ═══════════════════════════════════════════════════════════
# STAGE 3 — P2: Discount Pricing
# ═══════════════════════════════════════════════════════════

def stage_p2_discount(products):
    """Assess: is the product at a discount driven by fear/cycle/policy — not impairment?"""
    results = []
    for p in products:
        entry = {
            "id": p["id"],
            "ticker": p["ticker"],
            "name": p["name"],
            "category": p.get("category", ""),
            "current_price": p.get("current_price"),
            "discount": p.get("p2_discount", False),
            "discount_type": p.get("discount_type", ""),
            "discount_depth": p.get("discount_depth", "None"),
            "discount_detail": p.get("discount_detail", {}),
        }
        if p.get("target_discount_entry"):
            entry["target_discount_entry"] = p["target_discount_entry"]
        results.append(entry)

    at_discount = [r for r in results if r["discount"]]
    return {
        "stage_id": "S3",
        "stage": "P2 — Discount Pricing",
        "input_count": len(products),
        "at_discount": len(at_discount),
        "not_at_discount": len(results) - len(at_discount),
        "discount_breakdown": {
            "Maximum": len([r for r in results if r["discount_depth"] == "Maximum"]),
            "Strong": len([r for r in results if r["discount_depth"] == "Strong"]),
            "Moderate": len([r for r in results if r["discount_depth"] == "Moderate"]),
            "None": len([r for r in results if r["discount_depth"] == "None"]),
        },
    }, results


# ═══════════════════════════════════════════════════════════
# STAGE 4 — P3: Structural Demand
# ═══════════════════════════════════════════════════════════

def stage_p3_demand(products):
    """Assess: is demand structural (industrial, inelastic, infrastructure) — not speculation?"""
    results = []
    for p in products:
        results.append({
            "id": p["id"],
            "ticker": p["ticker"],
            "demand": p.get("p3_demand", False),
            "demand_type": p.get("demand_type", ""),
            "demand_detail": p.get("demand_detail", {}),
        })

    with_demand = [r for r in results if r["demand"]]
    return {
        "stage_id": "S4",
        "stage": "P3 — Structural Demand",
        "input_count": len(products),
        "with_structural_demand": len(with_demand),
        "demand_types": list(set(r["demand_type"] for r in results if r["demand_type"])),
    }, results


# ═══════════════════════════════════════════════════════════
# STAGE 5 — Cross-Layer Synthesis
# ═══════════════════════════════════════════════════════════

def stage_synthesis(products, p2_results, p3_results):
    """Synthesize 5-layer intelligence into conviction and recommendation."""
    p2_map = {r["id"]: r for r in p2_results}
    p3_map = {r["id"]: r for r in p3_results}

    synthesized = []
    for p in products:
        pid = p["id"]
        layers = p.get("layers", {})
        aligned = p.get("layers_aligned", 0)
        contradicting = p.get("layers_contradicting", 0)
        conviction = p.get("conviction", "Low")

        # Determine eligibility status
        p1_pass = p.get("p1_eligible", False)
        p2_pass = p2_map.get(pid, {}).get("discount", False)
        p3_pass = p3_map.get(pid, {}).get("demand", False)
        all_eligible = p1_pass and p2_pass and p3_pass

        if not p1_pass:
            status = "Ineligible (P1)"
        elif not p2_pass:
            status = "Ineligible (P2 — not at discount)"
        elif not p3_pass:
            status = "Ineligible (P3 — no structural demand)"
        else:
            status = "Eligible"

        entry = {
            "id": pid,
            "ticker": p["ticker"],
            "name": p["name"],
            "category": p.get("category", ""),
            "current_price": p.get("current_price"),
            "currency": p.get("currency", "USD"),

            # Eligibility
            "eligible": all_eligible,
            "status": status,
            "p1_pass": p1_pass,
            "p2_pass": p2_pass,
            "p3_pass": p3_pass,

            # Discount
            "discount_type": p2_map.get(pid, {}).get("discount_type", ""),
            "discount_depth": p2_map.get(pid, {}).get("discount_depth", "None"),
            "target_discount_entry": p2_map.get(pid, {}).get("target_discount_entry"),

            # Demand
            "demand_type": p.get("demand_type", ""),

            # Layers
            "layers": layers,
            "layers_aligned": aligned,
            "layers_contradicting": contradicting,
            "conviction": conviction,

            # Risk & Recommendation
            "key_risks": p.get("key_risks", []),
            "recommendation": p.get("recommendation", ""),
            "recommendation_rationale": p.get("recommendation_rationale", ""),

            # Detail (for synthesis cards)
            "discount_detail": p.get("discount_detail", {}),
            "demand_detail": p.get("demand_detail", {}),
            "p1_rationale": p.get("p1_rationale", ""),
        }
        synthesized.append(entry)

    # Sort: eligible first by conviction, then by recommendation rank
    conviction_order = {"High": 0, "Moderate": 1, "Low": 2}
    synthesized.sort(key=lambda s: (
        0 if s["eligible"] else 1,
        conviction_order.get(s["conviction"], 9),
        RECOMMENDATION_RANK.get(s["recommendation"], 9),
    ))

    return {
        "stage_id": "S5",
        "stage": "Cross-Layer Synthesis",
        "input_count": len(products),
        "eligible_count": len([s for s in synthesized if s["eligible"]]),
        "ineligible_count": len([s for s in synthesized if not s["eligible"]]),
        "conviction_breakdown": {
            "High": len([s for s in synthesized if s["conviction"] == "High"]),
            "Moderate": len([s for s in synthesized if s["conviction"] == "Moderate"]),
            "Low": len([s for s in synthesized if s["conviction"] == "Low"]),
        },
    }, synthesized


# ═══════════════════════════════════════════════════════════
# STAGE 6 — Radar Assembly
# ═══════════════════════════════════════════════════════════

def stage_radar(synthesized):
    """Assemble the prioritized product radar for Founder review."""
    radar = {
        "present_to_founder": [s for s in synthesized if s["recommendation"] == "Present to Founder"],
        "deep_research": [s for s in synthesized if s["recommendation"] == "Deep Research"],
        "radar_watchlist": [s for s in synthesized if s["recommendation"] == "Add to Radar Watchlist"],
        "monitor": [s for s in synthesized if s["recommendation"] == "Monitor — Wait for Better Price"],
        "ineligible": [s for s in synthesized if "Ineligible" in s["status"]],
    }

    return {
        "stage_id": "S6",
        "stage": "Radar Assembly",
        "total_products": len(synthesized),
        "eligible_for_radar": len([s for s in synthesized if s["eligible"]]),
        "present_to_founder": len(radar["present_to_founder"]),
        "deep_research": len(radar["deep_research"]),
        "radar_watchlist": len(radar["radar_watchlist"]),
        "monitor": len(radar["monitor"]),
        "ineligible": len(radar["ineligible"]),
    }, radar


# ═══════════════════════════════════════════════════════════
# PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════

def run_pipeline():
    """Execute all 6 stages and return complete pipeline result."""
    stages = []

    s1, universe = stage_universe(PRODUCTS)
    stages.append(s1)

    s2, p1_eligible = stage_p1_eligibility(universe)
    stages.append(s2)

    s3, p2_results = stage_p2_discount(p1_eligible)
    stages.append(s3)

    s4, p3_results = stage_p3_demand(p1_eligible)
    stages.append(s4)

    s5, synthesized = stage_synthesis(p1_eligible, p2_results, p3_results)
    stages.append(s5)

    s6, radar = stage_radar(synthesized)
    stages.append(s6)

    pipeline_result = {
        "run_id": RUN_ID,
        "pipeline_version": PIPELINE_VERSION,
        "pipeline_name": PIPELINE_CONFIG["name"],
        "strategy": PIPELINE_CONFIG["strategy"],
        "spec_ref": PIPELINE_CONFIG["spec_ref"],
        "point_in_time": datetime.now().isoformat(),
        "fixture_category": "SYNTHETIC — FOR V0 TESTING ONLY",
        "stages": stages,
        "synthesized": synthesized,
        "radar": radar,
    }
    return pipeline_result
