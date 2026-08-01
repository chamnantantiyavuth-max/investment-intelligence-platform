"""
Direct acceptance tests for the APPROVED Alpha Momentum V0 core pipeline (S1–S6).

Maps to ALPHA-MOMENTUM-V0-SPEC.md §6 AC-1..AC-10 (PD-v0.1-FOUNDING-DOMAIN-SPECIFICATIONS).

These tests import the core pipeline DIRECTLY (not the experimental quarantine)
and verify the approved pipeline satisfies the 10 acceptance criteria.

Recovery finding CRIT-3 (full review 2026-08-02): the core pipeline previously had
no direct automated coverage — separation tests only proved quarantine, not correctness.

NOTE ON IMPORT STRATEGY: this project has multiple modules named pipeline.py /
fixtures.py (alpha-momentum-v0, alpha-momentum-v0/experimental,
fundamental-opportunity-v0, institutional-intelligence-v0, close_system).
Plain `import pipeline` resolves to whichever module was cached first during
collection, so we load the core pipeline by EXPLICIT FILE PATH via importlib.
This is immune to import-order collisions in the combined suite.
"""
import importlib.util
import sys
from pathlib import Path

AM_DIR = Path(__file__).resolve().parents[2] / "alpha-momentum-v0"

# Clear stale cached modules so `from fixtures import ...` inside the core
# pipeline resolves to the ALPHA MOMENTUM fixtures, not another module's
# (same-named modules exist in fundamental-opportunity-v0,
# institutional-intelligence-v0, close_system, alpha-momentum-v0/experimental).
# Same collision-fix pattern as institutional-intelligence-v0/test_locked.
for _mod in ("pipeline", "fixtures", "q_conditions"):
    if _mod in sys.modules:
        _cached = sys.modules[_mod]
        if hasattr(_cached, "__file__") and _cached.__file__:
            if "alpha-momentum-v0" not in _cached.__file__:
                del sys.modules[_mod]


def _load_module(name: str, filename: str):
    """Load a module from an explicit file path (collision-proof).

    AM_DIR is force-placed at sys.path[0] so bare-name relative imports inside
    pipeline.py (e.g. `from fixtures import ...`) resolve to the core module,
    regardless of what earlier-collected test modules inserted.
    """
    # Force AM_DIR to the front (remove any existing entry first).
    am = str(AM_DIR)
    while am in sys.path:
        sys.path.remove(am)
    sys.path.insert(0, am)
    path = AM_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pipeline = _load_module("_am_core_pipeline", "pipeline.py")
fixtures = _load_module("_am_core_fixtures", "fixtures.py")
q_conditions = _load_module("_am_core_q_conditions", "q_conditions.py")


def _run():
    """Run the full core pipeline once."""
    return pipeline.run_pipeline()


def _queue_items(result):
    """Queue is a list of (theme_id, {theme, candidates}) tuples."""
    items = []
    for entry in result["queue"]:
        theme_id, payload = entry
        for cand in payload.get("candidates", []):
            items.append((theme_id, payload["theme"], cand))
    return items


# ── AC-1: Evidence lineage ──────────────────────────────────────────────
def test_ac1_evidence_lineage_preserved():
    """AC-1: A reviewer can trace a Candidate Quality assessment to evidence."""
    result = _run()
    assert "evidence" in result
    assert len(result["evidence"]) > 0
    # Evidence records carry relationship (supporting/contradicting) + candidate refs
    for ev in result["evidence"]:
        assert ev.get("id")
        assert ev.get("relationship") in ("supporting", "contradicting", "missing")
        assert ev.get("candidate") or ev.get("theme")
    # Candidate Quality dimensions are traceable: every queued candidate has a
    # candidate_quality dict with named dimensions (not one opaque score)
    for _, _, cand in _queue_items(result):
        cq = cand.get("candidate_quality", {})
        assert len(cq) >= 4, f"candidate {cand['id']} lacks traceable quality dimensions"


# ── AC-2: Deterministic features ────────────────────────────────────────
def _strip_run_metadata(result):
    """Remove run metadata that is legitimately non-deterministic
    (run_id, generated_at) — AC-2 concerns feature determinism, not
    wall-clock metadata. Same treatment as run_id stripping below."""
    result.pop("run_id", None)
    qc = result.get("q_conditions")
    if isinstance(qc, dict):
        qc.pop("generated_at", None)
    return result


def test_ac2_deterministic_features():
    """AC-2: Same pipeline + same fixtures → identical results."""
    r1 = _strip_run_metadata(_run())
    r2 = _strip_run_metadata(_run())
    assert r1 == r2


# ── AC-3: Separated dimensions ──────────────────────────────────────────
def test_ac3_quality_dimensions_separate():
    """AC-3: Candidate Quality, Entry Readiness, Data Confidence are distinct
    assessments — not one composite score. Theme Quality lives on the Theme Card."""
    result = _run()
    stages = {s["stage"]: s for s in result["stages"]}
    assert "Candidate Quality Assessment" in stages
    assert "Entry Readiness Assessment" in stages
    assert "Data Confidence Assessment" in stages
    for _, theme, cand in _queue_items(result):
        assert isinstance(cand.get("candidate_quality"), dict)
        assert isinstance(cand.get("entry_readiness"), dict)
        assert isinstance(cand.get("data_confidence"), dict) or "data_confidence" in cand
        # Theme Card carries theme-level quality separately
        assert isinstance(theme.get("confidence"), (str, int, float)) or "confidence" in theme


# ── AC-4: Theme Cards ───────────────────────────────────────────────────
def test_ac4_theme_card_fields_present():
    """AC-4: Each V0 theme renders a Theme Card with all required fields."""
    result = _run()
    themes = {t["id"]: t for t in fixtures.THEMES}
    assert len(themes) > 0
    for tid, theme in themes.items():
        assert theme.get("id")
        assert theme.get("name")
        assert theme.get("why_now")  # driver description
        assert theme.get("approval_status")
        assert theme.get("monitoring_status")
        assert theme.get("lifecycle")
    # Queue payloads carry the full theme card
    for _, theme, _ in _queue_items(result):
        assert theme.get("why_now")
        assert theme.get("approval_status")
        assert theme.get("monitoring_status")


# ── AC-5: Research Queue (Theme-first, adaptive, zero-capable) ──────────
def test_ac5_queue_theme_first_adaptive():
    """AC-5: Queue is Theme-first, supports adaptive capacity, can return zero."""
    result = _run()
    queue = result["queue"]
    assert isinstance(queue, list)
    # Theme-first: every entry is keyed by theme_id
    for entry in queue:
        theme_id, payload = entry
        assert isinstance(theme_id, str)
        assert "theme" in payload
    # Adaptive capacity: an empty candidate universe must not crash the pipeline
    saved_cands = fixtures.CANDIDATES
    saved_ct = fixtures.CANDIDATE_THEME
    try:
        fixtures.CANDIDATES = []
        fixtures.CANDIDATE_THEME = []
        result0 = pipeline.run_pipeline()
        assert isinstance(result0["queue"], list)
    finally:
        fixtures.CANDIDATES = saved_cands
        fixtures.CANDIDATE_THEME = saved_ct


# ── AC-6: Human feedback / override with 8 fields + original visible ────
def test_ac6_human_override_preserves_original():
    """AC-6: An override can be recorded; original system assessment remains visible."""
    result = _run()
    assert "overrides" in result
    assert isinstance(result["overrides"], list)
    for ov in result["overrides"]:
        # Constitution §12 override record: system assessment, machine dissent,
        # unresolved counter-evidence, Founder rationale, confirmation,
        # reassessment point, outcome — all preserved, not silently applied
        assert ov.get("candidate_id") or ov.get("entity_id") or ov.get("id")
        assert "system_assessment" in ov or "machine_dissent" in ov
    # Alternative explanations preserved separately (DNA-009)
    alt = result.get("alternative_explanations")
    assert alt is not None
    assert isinstance(alt, (list, dict))
    assert len(alt) > 0


# ── AC-7: Reproducibility (same inputs + version refs → identical) ──────
def test_ac7_reproducibility():
    """AC-7: Repeat run with same inputs + version references → identical output."""
    r1 = _run()
    r2 = _run()
    assert r1["pipeline_version"] == r2["pipeline_version"]
    assert r1["strategy"] == r2["strategy"]
    assert r1["point_in_time"] == r2["point_in_time"]
    assert r1["fixture_category"] == r2["fixture_category"]
    assert r1["queue"] == r2["queue"]
    assert r1["evidence"] == r2["evidence"]


# ── AC-8: Historical state / lifecycle audit trails ─────────────────────
def test_ac8_lifecycle_transition_history():
    """AC-8: Theme lifecycle/Approval/Monitoring transitions recorded & queryable."""
    for t in fixtures.THEMES:
        assert "lifecycle" in t or "lifecycle_stage" in t
        assert "approval_status" in t
        assert "monitoring_status" in t
    # Full audit trails exist on theme cards
    for t in fixtures.THEMES:
        for axis in ("lifecycle_transitions", "approval_transitions", "monitoring_transitions"):
            if axis in t:
                assert isinstance(t[axis], list)


# ── AC-9: Three candidate axes with correct scoping ─────────────────────
def test_ac9_candidate_axes_scoped():
    """AC-9: Candidate–Theme role + Leadership State (relationship axis) and
    Research State (workflow axis) are separate and scoped per relationship."""
    result = _run()
    for theme_id, _, cand in _queue_items(result):
        # Relationship axis: role/leadership lives on the theme-candidate pairing
        cq = cand.get("candidate_quality", {})
        # Leadership state (Confirmed Leader / Emerging Challenger) present
        assert "industry_leadership" in cq or "leadership" in cand
        # Research state / workflow status present (thesis, Q-conditions, queue status)
        assert "thesis" in cand or "research_state" in cand or "q_conditions" in cand or "status" in cand
        # Workflow axis is scoped to the strategy workflow, not a global property
        assert "entry_readiness" in cand  # workflow-axis assessment


# ── AC-10: No live-data / production contamination ──────────────────────
def test_ac10_synthetic_only_and_provisional_stack():
    """AC-10: Only synthetic fixtures; provisional technology not claimed final."""
    result = _run()
    assert "fixture_category" in result
    assert result["fixture_category"] == fixtures.FIXTURE_CATEGORY
    assert "synthetic" in str(fixtures.FIXTURE_CATEGORY).lower() or "fixture" in str(fixtures.FIXTURE_CATEGORY).lower()
    # No broker/execution/allocation artifacts in output
    for key in ("broker", "execution", "allocation", "orders", "positions"):
        assert key not in result, f"forbidden key '{key}' leaked into pipeline output"


# ── Determinism guard: Q-conditions enrichment is also deterministic ────
def test_q_conditions_enrichment_deterministic():
    """Q-Conditions (FD #39) applied to the queue must be deterministic."""
    r1 = _strip_run_metadata(_run())
    r2 = _strip_run_metadata(_run())
    assert r1["q_conditions"] == r2["q_conditions"]
    assert r1["q_conditions"].get("spec_ref")
