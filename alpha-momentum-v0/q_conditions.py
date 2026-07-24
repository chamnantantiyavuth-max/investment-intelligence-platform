"""
Alpha Momentum V0 — Q-Conditions (Exit Rules + Watchlist Lifecycle)
Per ONEIL-MINERVINI-RULE-PACK.md §6-7 (FD #39, 25 July 2026)

Q-Conditions = the exit framework: when to sell, reduce, or invalidate.
Watchlist Lifecycle = state machine for candidate progression.

All rules are deterministic advisory signals — never auto-execute.
Capital Command handles actual position management (external).
"""
from datetime import datetime, date
from typing import Optional

# ═══════════════════════════════════════════════════════════
# WATCHLIST LIFECYCLE STATE MACHINE
# ═══════════════════════════════════════════════════════════

LIFECYCLE_STATES = [
    "Discovered",      # Appeared in pipeline for first time
    "Qualified",       # Passed minimum QC thresholds
    "Watchlist",       # Active monitoring, no setup yet
    "Setup Forming",   # VCP/base/pullback developing
    "Ready for Review",# Setup complete, entry trigger defined → SURFACE TO FOUNDER
    "Trigger Observed",# Entry condition met per spec
    "Extended",        # Price too far above entry — risk/reward unfavorable
    "Failed",          # Thesis invalidated or technical breakdown
    "Invalidated",     # Theme/thesis no longer valid
    "Archived",        # Historical record
]

VALID_TRANSITIONS = {
    "Discovered":      ["Qualified"],
    "Qualified":       ["Watchlist", "Failed"],
    "Watchlist":       ["Setup Forming", "Failed", "Invalidated"],
    "Setup Forming":   ["Ready for Review", "Watchlist", "Failed"],
    "Ready for Review":["Trigger Observed", "Watchlist", "Failed", "Invalidated"],
    "Trigger Observed":["Extended", "Failed"],
    "Extended":        ["Watchlist", "Failed"],
    "Failed":          ["Archived", "Watchlist"],  # re-enter if thesis recovers
    "Invalidated":     ["Archived"],
    "Archived":        [],  # terminal state
}


def get_next_states(current_state: str) -> list[str]:
    """Return valid next states from current lifecycle state."""
    return VALID_TRANSITIONS.get(current_state, [])


def is_valid_transition(from_state: str, to_state: str) -> bool:
    """Check if a lifecycle transition is valid."""
    return to_state in VALID_TRANSITIONS.get(from_state, [])


def determine_lifecycle(candidate: dict, pipeline_context: dict = None) -> str:
    """Determine the appropriate lifecycle state for a candidate based on its attributes.

    Rules (per ONEIL-MINERVINI-RULE-PACK.md §7):
    - Stage 2 + positive RS + theme approved → at least Watchlist
    - VCP forming or entry_trigger defined → Setup Forming
    - Entry conditions met → Ready for Review
    - Stage 3/4 → Failed
    - Thesis invalidated → Invalidated
    """
    thesis = candidate.get("thesis_status", "")
    stage = candidate.get("stage", "")
    rs = candidate.get("relative_strength", "")
    entry_trigger = candidate.get("entry_trigger", "")
    current_lifecycle = candidate.get("lifecycle_state", "Discovered")

    # ── Failure states (override everything) ──
    if thesis == "Invalidated":
        return "Invalidated"
    if thesis == "Weakening" and stage in ("Stage 3", "Stage 4"):
        return "Failed"

    # ── Progression logic ──
    if current_lifecycle == "Discovered":
        return "Qualified"  # pipeline surfaced → auto-qualify for initial assessment

    if current_lifecycle == "Qualified":
        if thesis in ("Confirmed", "Strengthening") and rs == "positive":
            return "Watchlist"
        return "Qualified"  # stay

    if current_lifecycle == "Watchlist":
        # Check if a setup is forming
        has_trigger = bool(entry_trigger and (isinstance(entry_trigger, str) and entry_trigger.strip()))
        trigger_waiting = (
            isinstance(entry_trigger, dict)
            and entry_trigger.get("trigger_status") == "Waiting"
        )
        if stage == "Stage 2" and (has_trigger or trigger_waiting):
            return "Setup Forming"
        return "Watchlist"

    if current_lifecycle == "Setup Forming":
        trigger_ready = (
            isinstance(entry_trigger, dict)
            and entry_trigger.get("trigger_status") == "Ready"
        )
        if trigger_ready:
            return "Ready for Review"
        return "Setup Forming"

    if current_lifecycle == "Ready for Review":
        trigger_observed = (
            isinstance(entry_trigger, dict)
            and entry_trigger.get("trigger_status") == "Observed"
        )
        if trigger_observed:
            return "Trigger Observed"
        return "Ready for Review"

    # Default: no change
    return current_lifecycle


# ═══════════════════════════════════════════════════════════
# EXIT CONDITION DETECTION
# ═══════════════════════════════════════════════════════════

def detect_exit_signals(candidate: dict) -> list[dict]:
    """Detect exit signals for a candidate.

    Returns a list of exit signal dicts. Empty list = no exit signal.
    Multiple signals may fire simultaneously.

    Per ONEIL-MINERVINI-RULE-PACK.md §6.
    """
    signals = []
    ticker = candidate.get("ticker", candidate.get("id", "?"))
    thesis = candidate.get("thesis_status", "")
    stage = candidate.get("stage", "")
    conviction = candidate.get("conviction_level", "")

    # ── Thesis Invalidation (Sell Immediately) ──
    if thesis == "Invalidated":
        signals.append({
            "type": "Thesis Invalidation",
            "severity": "CRITICAL",
            "candidate": ticker,
            "message": f"Thesis invalidated for {ticker}. Sell immediately if holding.",
            "action": "exit_full",
            "rule_ref": "ONEIL-MINERVINI-RULE-PACK §6.1",
        })

    if thesis == "Weakening" and stage in ("Stage 3", "Stage 4"):
        signals.append({
            "type": "Thesis Weakening + Stage Deterioration",
            "severity": "HIGH",
            "candidate": ticker,
            "message": f"{ticker}: Thesis weakening ({thesis}) + Stage deterioration ({stage}). Strong sell signal.",
            "action": "exit_or_reduce",
            "rule_ref": "ONEIL-MINERVINI-RULE-PACK §6.1",
        })

    # ── Technical Breakdown ──
    if stage == "Stage 4":
        signals.append({
            "type": "Stage 4 Downtrend",
            "severity": "HIGH",
            "candidate": ticker,
            "message": f"{ticker} is in Stage 4 (Declining). Never enter. Exit if holding.",
            "action": "exit_full",
            "rule_ref": "ONEIL-MINERVINI-RULE-PACK §2.4",
        })

    if stage == "Stage 3" and thesis not in ("Invalidated",):
        signals.append({
            "type": "Stage 3 Distribution Warning",
            "severity": "MEDIUM",
            "candidate": ticker,
            "message": f"{ticker} entering Stage 3 (Topping/Distribution). Monitor closely. Consider reducing.",
            "action": "monitor_closely",
            "rule_ref": "ONEIL-MINERVINI-RULE-PACK §2.3",
        })

    # ── Risk Management (Non-Negotiable) ──
    if conviction == "Low" and thesis != "Invalidated":
        # ERP-004: Low conviction MUST have entry_trigger with measurable conditions
        entry_trigger = candidate.get("entry_trigger", "")
        has_trigger = bool(entry_trigger and (
            (isinstance(entry_trigger, str) and entry_trigger.strip())
            or (isinstance(entry_trigger, dict) and entry_trigger.get("conditions"))
        ))
        if not has_trigger:
            signals.append({
                "type": "ERP-004 Violation — Missing Entry Trigger",
                "severity": "MEDIUM",
                "candidate": ticker,
                "message": f"{ticker}: Low conviction without explicit entry_trigger. Required per ERP-004 (FD #37).",
                "action": "add_entry_trigger",
                "rule_ref": "ERP-004 (FD #37)",
            })

    return signals


# ═══════════════════════════════════════════════════════════
# Q-CONDITIONS REPORT GENERATOR
# ═══════════════════════════════════════════════════════════

def generate_q_conditions_report(queue: list) -> dict:
    """Generate a Q-Conditions report for the entire queue.

    Returns a dict with:
    - lifecycle_summary: counts per lifecycle state
    - exit_signals: list of all exit signals detected
    - actions_required: list of candidates requiring Founder attention
    """
    lifecycle_counts = {s: 0 for s in LIFECYCLE_STATES}
    all_exit_signals = []
    actions_required = []

    for _, tdata in queue:
        for c in tdata.get("candidates", []):
            state = c.get("lifecycle_state", "Discovered")
            lifecycle_counts[state] = lifecycle_counts.get(state, 0) + 1

            # Detect exit signals
            signals = detect_exit_signals(c)
            if signals:
                all_exit_signals.extend(signals)
                for s in signals:
                    if s["severity"] in ("CRITICAL", "HIGH"):
                        actions_required.append({
                            "candidate": c.get("ticker", c.get("id")),
                            "action": s["action"],
                            "reason": s["message"],
                        })

            # Check lifecycle progression
            next_state = determine_lifecycle(c)
            if next_state != state:
                actions_required.append({
                    "candidate": c.get("ticker", c.get("id")),
                    "action": f"lifecycle: {state} → {next_state}",
                    "reason": f"Lifecycle progression recommended based on thesis={c.get('thesis_status')}, stage={c.get('stage')}",
                })

    return {
        "generated_at": datetime.now().isoformat(),
        "spec_ref": "ONEIL-MINERVINI-RULE-PACK.md §6-7",
        "lifecycle_summary": lifecycle_counts,
        "exit_signals": all_exit_signals,
        "exit_signal_count": len(all_exit_signals),
        "critical_count": len([s for s in all_exit_signals if s["severity"] == "CRITICAL"]),
        "high_count": len([s for s in all_exit_signals if s["severity"] == "HIGH"]),
        "medium_count": len([s for s in all_exit_signals if s["severity"] == "MEDIUM"]),
        "actions_required": actions_required,
    }


# ═══════════════════════════════════════════════════════════
# PIPELINE INTEGRATION POINT
# ═══════════════════════════════════════════════════════════

def enrich_queue_with_q_conditions(queue: list) -> list:
    """Enrich each candidate in the queue with lifecycle state + exit signals.

    Called from pipeline.run_pipeline() after Stage 6.
    Mutates queue in place for efficiency.
    """
    for _, tdata in queue:
        for c in tdata.get("candidates", []):
            # Set lifecycle state if not present
            if "lifecycle_state" not in c or not c["lifecycle_state"]:
                c["lifecycle_state"] = determine_lifecycle(c)

            # Attach exit signals
            signals = detect_exit_signals(c)
            c["exit_signals"] = signals
            c["has_exit_signal"] = len(signals) > 0
            c["exit_signal_severity"] = (
                signals[0]["severity"] if signals else "NONE"
            )

            # Valid next states
            c["valid_next_states"] = get_next_states(c["lifecycle_state"])

    return queue
