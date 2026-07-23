"""
experimental/inbox.py — Weak Signal Inbox

Phase 5 Theme Intelligence V1 (T1)
Authorized: FD #27 (23 July 2026)

In-memory storage + CRUD API for anomalies and theme hypotheses.
Constitutionally separate from the approved pipeline (ALPHA GUARD #1, #4).

Hard guards enforced:
  1. ZERO imports from pipeline.py or display.py
  2. Data stored ONLY in experimental/ scope (in-memory, V0-suitable)
  3. Epistemic metadata REQUIRED on all AI-generated hypotheses (§23.4)
  4. NEVER modifies fixtures.THEMES or fixtures.CANDIDATES
"""

import uuid
from datetime import datetime, date

# ──────────────────────────────────────────────
# In-memory storage (experimental scope only)
# ──────────────────────────────────────────────
_anomalies = []
_hypotheses = []
_anomaly_counter = 0
_hypothesis_counter = 0
_theme_counter = 0

# ──────────────────────────────────────────────
# Valid domain values
# ──────────────────────────────────────────────
VALID_ANOMALY_TYPES = {
    "Sector Divergence",
    "Single-Stock Outlier",
    "Volume Anomaly",
    "Missing Correlation",
}
VALID_ANOMALY_STATUSES = {
    "Unexplained",
    "Investigating",
    "Promoted",
    "Dismissed",
}
VALID_HYPOTHESIS_STATUSES = {
    "Hypothesis — awaiting Founder review",
    "Under Review",
    "Promoted",
    "Rejected",
}

# ──────────────────────────────────────────────
# Helper: generate sequential IDs
# ──────────────────────────────────────────────
def _next_anomaly_id():
    """Generate monotonic anomaly ID: AN-001, AN-002, ..."""
    global _anomaly_counter
    _anomaly_counter += 1
    return f"AN-{_anomaly_counter:03d}"

def _next_hypothesis_id():
    """Generate monotonic hypothesis ID: HY-001, HY-002, ..."""
    global _hypothesis_counter
    _hypothesis_counter += 1
    return f"HY-{_hypothesis_counter:03d}"

def _next_theme_id():
    """Generate monotonic experimental theme ID: TH-EXP-001, ..."""
    global _theme_counter
    _theme_counter += 1
    return f"TH-EXP-{_theme_counter:03d}"


# ═══════════════════════════════════════════════
# ANOMALY API
# ═══════════════════════════════════════════════

def add_anomaly(data: dict) -> str:
    """
    Add a new anomaly to the Weak Signal Inbox.

    Required fields: type, description, first_observed, source
    Optional fields: related_theme, related_tickers
    Returns: anomaly_id (str)

    Raises ValueError if type is not one of the 4 valid types.
    """
    anomaly_type = data.get("type", "")
    if anomaly_type not in VALID_ANOMALY_TYPES:
        raise ValueError(
            f"Invalid anomaly type: '{anomaly_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ANOMALY_TYPES))}"
        )

    anomaly = {
        "id": _next_anomaly_id(),
        "type": anomaly_type,
        "description": data.get("description", ""),
        "first_observed": data.get("first_observed", ""),
        "related_theme": data.get("related_theme"),
        "related_tickers": data.get("related_tickers", []),
        "status": data.get("status", "Unexplained"),
        "source": data.get("source", ""),
    }

    # Validate initial status if explicitly provided
    if "status" in data and data["status"] not in VALID_ANOMALY_STATUSES:
        raise ValueError(
            f"Invalid anomaly status: '{data['status']}'. "
            f"Must be one of: {', '.join(sorted(VALID_ANOMALY_STATUSES))}"
        )

    _anomalies.append(anomaly)
    return anomaly["id"]


def list_anomalies(filter: dict = None) -> list:
    """
    List all anomalies, optionally filtered by key-value pairs.

    Examples:
        list_anomalies()                          # all anomalies
        list_anomalies({"type": "Volume Anomaly"}) # by type
        list_anomalies({"status": "Unexplained"})  # by status
    """
    if not filter:
        return list(_anomalies)

    result = []
    for anomaly in _anomalies:
        match = True
        for key, value in filter.items():
            if key not in anomaly or anomaly[key] != value:
                match = False
                break
        if match:
            result.append(anomaly)

    return result


def annotate_anomaly(id: str, status: str) -> dict:
    """
    Update the status of an existing anomaly.

    Args:
        id: Anomaly ID (e.g., "AN-001")
        status: New status (must be one of the 4 valid statuses)

    Returns:
        The updated anomaly dict.

    Raises:
        KeyError if the anomaly ID is not found.
        ValueError if the status is not valid.
    """
    if status not in VALID_ANOMALY_STATUSES:
        raise ValueError(
            f"Invalid status: '{status}'. "
            f"Must be one of: {', '.join(sorted(VALID_ANOMALY_STATUSES))}"
        )

    for anomaly in _anomalies:
        if anomaly["id"] == id:
            anomaly["status"] = status
            return anomaly

    raise KeyError(f"Anomaly '{id}' not found")


# ═══════════════════════════════════════════════
# HYPOTHESIS API
# ═══════════════════════════════════════════════

def add_hypothesis(data: dict) -> str:
    """
    Add a new theme hypothesis to the Weak Signal Inbox.

    Required fields: title, proposed_driver, why_now,
                     potential_candidates, key_unknowns, proposed_date
    Optional: status (default: "Hypothesis — awaiting Founder review"),
              _epistemic (AI-generated hypotheses MUST carry this — §23.4)

    Returns: hypothesis_id (str)
    """
    hypothesis = {
        "id": _next_hypothesis_id(),
        "title": data.get("title", ""),
        "proposed_driver": data.get("proposed_driver", ""),
        "why_now": data.get("why_now", ""),
        "potential_candidates": data.get("potential_candidates", []),
        "key_unknowns": data.get("key_unknowns", []),
        "status": data.get("status", "Hypothesis — awaiting Founder review"),
        "proposed_date": data.get("proposed_date", ""),
    }

    # Store epistemic metadata if provided (mandatory for AI-generated — §23.4)
    if "_epistemic" in data:
        hypothesis["_epistemic"] = data["_epistemic"]

    _hypotheses.append(hypothesis)
    return hypothesis["id"]


def list_hypotheses(filter: dict = None) -> list:
    """
    List all hypotheses, optionally filtered by key-value pairs.

    Examples:
        list_hypotheses()                                           # all
        list_hypotheses({"status": "Hypothesis — awaiting Founder review"})
    """
    if not filter:
        return list(_hypotheses)

    result = []
    for hypothesis in _hypotheses:
        match = True
        for key, value in filter.items():
            if key not in hypothesis or hypothesis[key] != value:
                match = False
                break
        if match:
            result.append(hypothesis)

    return result


def promote_hypothesis_to_experimental(id: str) -> str:
    """
    Promote a hypothesis to an experimental theme.

    Generates a TH-EXP-XXX theme ID and updates the hypothesis status to "Promoted".

    Args:
        id: Hypothesis ID (e.g., "HY-001")

    Returns:
        theme_id (str, e.g., "TH-EXP-001")

    Raises:
        KeyError if the hypothesis ID is not found.
    """
    hypothesis = None
    for h in _hypotheses:
        if h["id"] == id:
            hypothesis = h
            break

    if hypothesis is None:
        raise KeyError(f"Hypothesis '{id}' not found")

    theme_id = _next_theme_id()
    hypothesis["status"] = "Promoted"

    return theme_id
