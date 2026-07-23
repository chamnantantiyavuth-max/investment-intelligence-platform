"""
Locked Acceptance Test: Inbox Data Model (T1-L1)
Parent-written · READ-ONLY for subagents
Verifies Anomaly + Hypothesis data schemas per T1 contract.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestAnomalySchema:
    """Every anomaly record must have all required fields with valid types."""

    REQUIRED_FIELDS = {
        "id": str,
        "type": str,
        "description": str,
        "first_observed": str,
        "status": str,
        "source": str,
    }
    VALID_TYPES = {"Sector Divergence", "Single-Stock Outlier", "Volume Anomaly", "Missing Correlation"}
    VALID_STATUSES = {"Unexplained", "Investigating", "Promoted", "Dismissed"}

    def test_anomaly_has_required_fields(self):
        """add_anomaly() must produce records with all required fields."""
        from experimental.inbox import add_anomaly

        aid = add_anomaly({
            "type": "Sector Divergence",
            "description": "Test anomaly — sector RS divergence",
            "first_observed": "2024-07-01",
            "source": "EOD market data",
        })
        assert isinstance(aid, str), f"add_anomaly must return string ID, got {type(aid)}"

        anomalies = self._get_all_anomalies()
        created = next((a for a in anomalies if a.get("id") == aid), None)
        assert created is not None, f"Created anomaly {aid} not found in list"

        for field, expected_type in self.REQUIRED_FIELDS.items():
            assert field in created, f"Missing required field: {field}"
            assert isinstance(created[field], expected_type), \
                f"Field {field}: expected {expected_type.__name__}, got {type(created[field]).__name__}"

    def test_anomaly_type_must_be_valid(self):
        """Anomaly type must be one of the 4 defined types."""
        from experimental.inbox import add_anomaly

        for valid_type in self.VALID_TYPES:
            aid = add_anomaly({
                "type": valid_type,
                "description": f"Test {valid_type}",
                "first_observed": "2024-07-01",
                "source": "test",
            })
            assert aid, f"add_anomaly failed for valid type: {valid_type}"

        # Invalid type should raise
        with pytest.raises(ValueError, match="Invalid anomaly type"):
            add_anomaly({
                "type": "Invalid Type XYZ",
                "description": "Bad",
                "first_observed": "2024-07-01",
                "source": "test",
            })

    def test_anomaly_status_must_be_valid(self):
        """Anomaly status must be one of: Unexplained, Investigating, Promoted, Dismissed."""
        from experimental.inbox import add_anomaly, annotate_anomaly

        aid = add_anomaly({
            "type": "Volume Anomaly",
            "description": "Test status transitions",
            "first_observed": "2024-07-01",
            "source": "test",
        })

        for status in self.VALID_STATUSES:
            result = annotate_anomaly(aid, status)
            assert result is not None

        with pytest.raises(ValueError, match="Invalid status"):
            annotate_anomaly(aid, "Bad Status")

    def _get_all_anomalies(self):
        from experimental.inbox import list_anomalies
        return list_anomalies()


class TestHypothesisSchema:
    """Every hypothesis must have required fields + epistemic metadata (§23.4)."""

    REQUIRED_FIELDS = {
        "id": str,
        "title": str,
        "proposed_driver": str,
        "why_now": str,
        "potential_candidates": list,
        "key_unknowns": list,
        "status": str,
        "proposed_date": str,
    }
    # Epistemic metadata (§23.4) — mandatory for all AI-generated hypotheses
    EPISTEMIC_FIELDS = [
        "provenance", "confidence_level", "version",
        "source_references", "as_of_time", "model_provenance",
    ]

    def test_hypothesis_has_required_fields(self):
        """add_hypothesis() must produce records with all required fields."""
        from experimental.inbox import add_hypothesis

        hid = add_hypothesis({
            "title": "Test Hypothesis",
            "proposed_driver": "Test driver",
            "why_now": "Test urgency",
            "potential_candidates": ["AAPL", "MSFT"],
            "key_unknowns": ["Unknown factor A"],
            "proposed_date": "2024-07-01",
        })
        assert isinstance(hid, str), f"add_hypothesis must return string ID, got {type(hid)}"

        hypotheses = self._get_all_hypotheses()
        created = next((h for h in hypotheses if h.get("id") == hid), None)
        assert created is not None, f"Created hypothesis {hid} not found"

        for field, expected_type in self.REQUIRED_FIELDS.items():
            assert field in created, f"Missing required field: {field}"
            assert isinstance(created[field], expected_type), \
                f"Field {field}: expected {expected_type.__name__}, got {type(created[field]).__name__}"

    def test_hypothesis_has_epistemic_metadata(self):
        """All AI-generated hypotheses MUST carry epistemic metadata (§23.4)."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        hid = add_hypothesis({
            "title": "Epistemic Test",
            "proposed_driver": "Test",
            "why_now": "Test",
            "potential_candidates": ["TEST"],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
            "_epistemic": {
                "provenance": "AI-generated from anomaly patterns",
                "confidence_level": "Low",
                "version": "v0.1.0",
                "source_references": ["AN-001"],
                "as_of_time": "2024-07-01",
                "model_provenance": "deepseek-v4-pro (Parent)",
            },
        })

        hypotheses = list_hypotheses()
        created = next(h for h in hypotheses if h["id"] == hid)
        ep = created.get("_epistemic", {})

        for field in self.EPISTEMIC_FIELDS:
            assert field in ep, (
                f"❌ GUARD VIOLATION: Hypothesis {hid} missing _epistemic.{field}\n"
                f"   §23.4: All AI-generated hypotheses MUST carry epistemic metadata"
            )

    def test_hypothesis_status_must_be_valid(self):
        """Hypothesis status transitions must be valid."""
        from experimental.inbox import add_hypothesis, list_hypotheses

        hid = add_hypothesis({
            "title": "Status Test",
            "proposed_driver": "Test",
            "why_now": "Test",
            "potential_candidates": [],
            "key_unknowns": [],
            "proposed_date": "2024-07-01",
        })

        hypotheses = list_hypotheses()
        created = next(h for h in hypotheses if h["id"] == hid)
        status = created.get("status", "")
        valid = {"Hypothesis — awaiting Founder review", "Under Review", "Promoted", "Rejected"}
        assert status in valid, f"Invalid hypothesis status: {status}"

    def _get_all_hypotheses(self):
        from experimental.inbox import list_hypotheses
        return list_hypotheses()
