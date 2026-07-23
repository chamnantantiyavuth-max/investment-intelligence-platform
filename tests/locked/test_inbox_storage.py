"""
Locked Acceptance Test: Inbox Storage (T1-L2)
Parent-written · READ-ONLY for subagents
Verifies Weak Signal Inbox API: CRUD + query + promotion.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestInboxAnomalyAPI:
    """Anomaly CRUD operations."""

    def test_add_and_list_anomalies(self):
        """add_anomaly → list_anomalies round-trip."""
        from experimental.inbox import add_anomaly, list_anomalies

        before = len(list_anomalies())
        aid = add_anomaly({
            "type": "Volume Anomaly",
            "description": "Test: unusual volume in TEST",
            "first_observed": "2024-07-01",
            "source": "EOD data",
            "related_tickers": ["TEST"],
        })
        after = len(list_anomalies())
        assert after == before + 1, f"Expected {before + 1} anomalies, got {after}"
        assert aid, "add_anomaly must return non-empty ID"

    def test_list_anomalies_with_filter(self):
        """list_anomalies(filter) returns filtered results."""
        from experimental.inbox import list_anomalies

        all_anomalies = list_anomalies()
        if not all_anomalies:
            pytest.skip("No anomalies to filter")

        # Filter by type
        first_type = all_anomalies[0]["type"]
        filtered = list_anomalies({"type": first_type})
        assert all(a["type"] == first_type for a in filtered), \
            f"Filter type={first_type} returned non-matching anomalies"

        # Filter by status
        filtered = list_anomalies({"status": "Unexplained"})
        assert all(a["status"] == "Unexplained" for a in filtered), \
            "Filter status=Unexplained returned non-matching anomalies"

    def test_annotate_anomaly_updates_status(self):
        """annotate_anomaly(id, status) updates the anomaly status."""
        from experimental.inbox import add_anomaly, annotate_anomaly, list_anomalies

        aid = add_anomaly({
            "type": "Missing Correlation",
            "description": "Test: annotation",
            "first_observed": "2024-07-01",
            "source": "test",
        })

        result = annotate_anomaly(aid, "Investigating")
        assert result is not None

        # Verify the anomaly status changed
        anomalies = list_anomalies()
        updated = next(a for a in anomalies if a["id"] == aid)
        assert updated["status"] == "Investigating", \
            f"Expected status Investigating, got {updated['status']}"

    def test_annotate_nonexistent_anomaly_raises(self):
        """Annotating a non-existent anomaly should raise."""
        from experimental.inbox import annotate_anomaly

        with pytest.raises(KeyError, match="not found"):
            annotate_anomaly("NONEXISTENT-999", "Dismissed")


class TestInboxHypothesisAPI:
    """Hypothesis CRUD + promotion."""

    def test_add_and_list_hypotheses(self):
        """add_hypothesis → list_hypotheses round-trip."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        before = len(list_hypotheses())
        hid = add_hypothesis({
            "title": "Test Theme Hypothesis",
            "proposed_driver": "Test driver",
            "why_now": "Because testing",
            "potential_candidates": ["TEST"],
            "key_unknowns": ["Unknown X"],
            "proposed_date": "2024-07-01",
        })
        after = len(list_hypotheses())
        assert after == before + 1, f"Expected {before + 1} hypotheses, got {after}"
        assert hid, "add_hypothesis must return non-empty ID"

    def test_list_hypotheses_with_filter(self):
        """list_hypotheses(filter) returns filtered results."""
        from experimental.inbox import list_hypotheses

        all_hyps = list_hypotheses()
        if not all_hyps:
            pytest.skip("No hypotheses to filter")

        # Filter by status
        filtered = list_hypotheses({"status": "Hypothesis — awaiting Founder review"})
        assert all("awaiting Founder review" in h["status"] for h in filtered), \
            "Filter returned non-matching hypotheses"

    def test_promote_hypothesis_to_experimental(self):
        """promote_hypothesis_to_experimental(id) → theme_id."""
        from experimental.inbox import add_hypothesis, promote_hypothesis_to_experimental, list_hypotheses

        hid = add_hypothesis({
            "title": "Promotable Hypothesis",
            "proposed_driver": "Clear structural driver",
            "why_now": "Immediate catalyst",
            "potential_candidates": ["AAPL", "MSFT"],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })

        theme_id = promote_hypothesis_to_experimental(hid)
        assert theme_id, "promote must return a theme_id"
        assert theme_id.startswith("TH-EXP-"), \
            f"Experimental theme ID must start with TH-EXP-, got {theme_id}"

        # Hypothesis status should update to Promoted
        hypotheses = list_hypotheses()
        promoted = next(h for h in hypotheses if h["id"] == hid)
        assert "Promoted" in promoted["status"], \
            f"Expected status 'Promoted', got {promoted['status']}"


class TestInboxIdempotency:
    """Inbox operations should be stable across repeated calls."""

    def test_list_anomalies_idempotent(self):
        """list_anomalies() twice returns same count."""
        from experimental.inbox import list_anomalies
        a1 = len(list_anomalies())
        a2 = len(list_anomalies())
        assert a1 == a2, f"list_anomalies not idempotent: {a1} vs {a2}"

    def test_list_hypotheses_idempotent(self):
        """list_hypotheses() twice returns same count."""
        from experimental.inbox import list_hypotheses
        h1 = len(list_hypotheses())
        h2 = len(list_hypotheses())
        assert h1 == h2, f"list_hypotheses not idempotent: {h1} vs {h2}"
