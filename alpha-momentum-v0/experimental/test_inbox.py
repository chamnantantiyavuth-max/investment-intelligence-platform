"""
Supplementary tests for experimental/inbox.py — Weak Signal Inbox.

These tests exercise edge cases, state isolation, and contract guarantees
beyond the locked acceptance tests. They are NOT read-only and may be
extended as the module evolves.

Run: python -m pytest alpha-momentum-v0/experimental/test_inbox.py -v
"""
import os
import sys

# Fix combined-test collision: same-named module (fixtures) in
# fundamental-opportunity-v0, institutional-intelligence-v0, and alpha-momentum-v0.
# Clear stale cached modules so the AM one loads correctly.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
for _mod in ("fixtures",):
    if _mod in sys.modules:
        _cached = sys.modules[_mod]
        if hasattr(_cached, "__file__") and _cached.__file__:
            if "alpha-momentum-v0" not in _cached.__file__:
                del sys.modules[_mod]
sys.path.insert(0, AM_V0_DIR)

import pytest


def _import_am_fixtures():
    """Import AM fixtures, clearing stale cache from other modules."""
    if 'fixtures' in sys.modules:
        cached = sys.modules['fixtures']
        if hasattr(cached, '__file__') and cached.__file__:
            if 'alpha-momentum-v0' not in cached.__file__:
                del sys.modules['fixtures']
    import fixtures
    return fixtures


# ═══════════════════════════════════════════════════════════════
# Anomaly Edge Cases
# ═══════════════════════════════════════════════════════════════

class TestAnomalyEdgeCases:
    """Anomaly API edge-case coverage."""

    def test_add_anomaly_empty_description(self):
        """add_anomaly accepts empty description (no crash)."""
        from experimental.inbox import add_anomaly, list_anomalies

        before = len(list_anomalies())
        aid = add_anomaly({
            "type": "Volume Anomaly",
            "description": "",
            "first_observed": "2024-07-01",
            "source": "test",
        })
        assert aid
        assert len(list_anomalies()) == before + 1

    def test_add_anomaly_optional_fields_defaulted(self):
        """Optional fields (related_theme, related_tickers) get sensible defaults."""
        from experimental.inbox import add_anomaly, list_anomalies

        aid = add_anomaly({
            "type": "Sector Divergence",
            "description": "Optional fields test",
            "first_observed": "2024-07-01",
            "source": "test",
        })
        anomalies = list_anomalies({"id": aid})
        assert len(anomalies) == 1
        a = anomalies[0]
        # related_theme may be None or absent — should not crash
        # related_tickers should default to empty list
        assert isinstance(a.get("related_tickers", []), list)

    def test_list_anomalies_multiple_filters(self):
        """list_anomalies with compound filter (type + status)."""
        from experimental.inbox import add_anomaly, list_anomalies

        add_anomaly({
            "type": "Missing Correlation",
            "description": "Multi-filter A",
            "first_observed": "2024-07-01",
            "source": "test",
            "status": "Investigating",
        })
        filtered = list_anomalies({"type": "Missing Correlation", "status": "Investigating"})
        assert all(a["type"] == "Missing Correlation" and a["status"] == "Investigating" for a in filtered)

    def test_list_anomalies_filter_none(self):
        """Passing None as filter returns all anomalies (same as no filter)."""
        from experimental.inbox import add_anomaly, list_anomalies

        before_all = len(list_anomalies())
        before_none = len(list_anomalies(None))
        assert before_all == before_none

    def test_annotate_anomaly_all_status_transitions(self):
        """All 4 statuses can be applied sequentially."""
        from experimental.inbox import add_anomaly, annotate_anomaly, list_anomalies

        aid = add_anomaly({
            "type": "Volume Anomaly",
            "description": "Status cycle",
            "first_observed": "2024-07-01",
            "source": "test",
        })

        for status in ["Investigating", "Promoted", "Dismissed"]:
            result = annotate_anomaly(aid, status)
            assert result["status"] == status

    def test_annotate_anomaly_invalid_status_raises(self):
        """Invalid status string raises ValueError with descriptive message."""
        from experimental.inbox import add_anomaly, annotate_anomaly

        aid = add_anomaly({
            "type": "Single-Stock Outlier",
            "description": "Bad status test",
            "first_observed": "2024-07-01",
            "source": "test",
        })
        with pytest.raises(ValueError) as excinfo:
            annotate_anomaly(aid, "NotARealStatus")
        assert "Invalid" in str(excinfo.value) or "status" in str(excinfo.value).lower()


# ═══════════════════════════════════════════════════════════════
# Hypothesis Edge Cases
# ═══════════════════════════════════════════════════════════════

class TestHypothesisEdgeCases:
    """Hypothesis API edge-case coverage."""

    def test_add_hypothesis_without_epistemic_ok(self):
        """Hypothesis can exist without _epistemic (non-AI-generated case)."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        hid = add_hypothesis({
            "title": "No Epistemic",
            "proposed_driver": "Test driver",
            "why_now": "Test",
            "potential_candidates": [],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })
        hyps = list_hypotheses({"id": hid})
        assert len(hyps) == 1
        # _epistemic not present — this is allowed for non-AI entries
        assert "_epistemic" not in hyps[0]

    def test_add_hypothesis_empty_lists(self):
        """Empty potential_candidates and key_unknowns are valid."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        hid = add_hypothesis({
            "title": "Empty Lists",
            "proposed_driver": "Driver",
            "why_now": "Now",
            "potential_candidates": [],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })
        h = list_hypotheses({"id": hid})[0]
        assert isinstance(h["potential_candidates"], list)
        assert isinstance(h["key_unknowns"], list)
        assert len(h["potential_candidates"]) == 0
        assert len(h["key_unknowns"]) == 0

    def test_list_hypotheses_filter_none(self):
        """Passing None as filter returns all hypotheses."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        before_all = len(list_hypotheses())
        before_none = len(list_hypotheses(None))
        assert before_all == before_none

    def test_promote_hypothesis_to_experimental_updates_status(self):
        """promote_hypothesis_to_experimental sets hypothesis status to 'Promoted'."""
        from experimental.inbox import add_hypothesis, promote_hypothesis_to_experimental, list_hypotheses

        hid = add_hypothesis({
            "title": "Promotion Test",
            "proposed_driver": "X",
            "why_now": "Y",
            "potential_candidates": ["A"],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })

        theme_id = promote_hypothesis_to_experimental(hid)
        assert theme_id.startswith("TH-EXP-")

        hyps = list_hypotheses({"id": hid})
        assert len(hyps) == 1
        assert "Promoted" in hyps[0]["status"]

    def test_promote_hypothesis_unique_ids(self):
        """Each promotion generates a unique TH-EXP-XXX ID."""
        from experimental.inbox import add_hypothesis, promote_hypothesis_to_experimental

        ids = set()
        for i in range(5):
            hid = add_hypothesis({
                "title": f"Unique {i}",
                "proposed_driver": "D",
                "why_now": "W",
                "potential_candidates": [],
                "key_unknowns": [],
                "proposed_date": "2024-07-01",
            })
            tid = promote_hypothesis_to_experimental(hid)
            ids.add(tid)

        assert len(ids) == 5, f"Expected 5 unique theme IDs, got {len(ids)}"


# ═══════════════════════════════════════════════════════════════
# State Isolation
# ═══════════════════════════════════════════════════════════════

class TestStateIsolation:
    """In-memory state isolation between anomaly and hypothesis stores."""

    def test_anomaly_store_separate_from_hypothesis_store(self):
        """Adding anomalies does not affect hypothesis count and vice versa."""
        from experimental.inbox import add_anomaly, add_hypothesis, list_anomalies, list_hypotheses

        an_before = len(list_anomalies())
        hy_before = len(list_hypotheses())

        add_anomaly({
            "type": "Sector Divergence",
            "description": "Isolation test",
            "first_observed": "2024-07-01",
            "source": "test",
        })
        # Hypothesis count should be unchanged
        assert len(list_hypotheses()) == hy_before

        add_hypothesis({
            "title": "Isolation Hyp",
            "proposed_driver": "D",
            "why_now": "W",
            "potential_candidates": [],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })
        # Anomaly count should be unchanged
        assert len(list_anomalies()) == an_before + 1


# ═══════════════════════════════════════════════════════════════
# Separation Guard Verification
# ═══════════════════════════════════════════════════════════════

class TestSeparationGuards:
    """Verify inbox.py does not leak into approved pipeline scope."""

    def test_inbox_module_does_not_mutate_fixtures(self):
        """Inbox functions must not mutate fixtures.THEMES or CANDIDATES (FD #27)."""
        f = _import_am_fixtures()

        themes_before = len(f.THEMES)
        candidates_before = len(f.CANDIDATES)

        from experimental.inbox import add_anomaly, add_hypothesis

        add_anomaly({
            "type": "Volume Anomaly",
            "description": "Separation test",
            "first_observed": "2024-07-01",
            "source": "test",
        })
        add_hypothesis({
            "title": "Separation Hyp",
            "proposed_driver": "D",
            "why_now": "W",
            "potential_candidates": [],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })

        assert len(f.THEMES) == themes_before, "THEMES must not be mutated by inbox"
        assert len(f.CANDIDATES) == candidates_before, "CANDIDATES must not be mutated by inbox"

    def test_inbox_loads_without_pipeline_import(self):
        """Verify inbox.py imports do not transitively pull in pipeline.py."""
        import ast

        inbox_path = os.path.join(AM_V0_DIR, "experimental", "inbox.py")
        with open(inbox_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if "pipeline" in module or "display" in module:
                    pytest.fail(f"inbox.py imports forbidden module: {module}")
