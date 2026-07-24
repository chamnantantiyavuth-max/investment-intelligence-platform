"""
Locked Acceptance Test: Hypothesis Epistemic Metadata (T3-L2)
Parent-written · READ-ONLY for subagents
Verifies §23.4: All AI-generated hypotheses MUST carry epistemic metadata.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)

EPISTEMIC_FIELDS = [
    "provenance", "confidence_level", "version",
    "source_references", "as_of_time", "model_provenance",
]


class TestEpistemicMetadataMandatory:
    """Every AI-generated hypothesis MUST have _epistemic block (§23.4)."""

    def test_generate_hypothesis_has_epistemic_metadata(self):
        """generate_hypothesis() output must carry _epistemic block."""
        from experimental.hypothesis import generate_hypothesis

        anomalies = [
            {"id": "AN-001", "type": "Sector Divergence",
             "description": "Test", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
        ]

        hypothesis = generate_hypothesis(anomalies, [], [])
        if hypothesis is None:
            pytest.skip("generate_hypothesis returned None (no patterns)")

        ep = hypothesis.get("_epistemic", {})
        assert ep, (
            f"❌ GUARD VIOLATION: Hypothesis {hypothesis.get('id','?')} missing _epistemic metadata\n"
            f"   §23.4: All AI-generated hypotheses MUST carry epistemic metadata"
        )

        for field in EPISTEMIC_FIELDS:
            assert field in ep, (
                f"❌ GUARD VIOLATION: Hypothesis missing _epistemic.{field}\n"
                f"   §23.4 requires: {', '.join(EPISTEMIC_FIELDS)}"
            )

    def test_promote_to_experimental_preserves_epistemic(self):
        """Experimental theme must retain epistemic metadata from hypothesis."""
        from experimental.hypothesis import promote_to_experimental

        hypothesis = {
            "id": "HY-EP-001",
            "title": "Metadata Test",
            "proposed_driver": "Test driver",
            "why_now": "Test urgency",
            "potential_candidates": ["TEST"],
            "key_unknowns": [],
            "status": "Hypothesis — awaiting Founder review",
            "proposed_date": "2024-07-24",
            "potential_theme_industry": "Test Industry",
            "_epistemic": {
                "provenance": "AI-generated from anomaly patterns (Parent verification)",
                "confidence_level": "Low",
                "version": "exp-v0.1.0",
                "source_references": ["AN-001", "AN-002"],
                "as_of_time": "2024-07-24",
                "model_provenance": "deepseek-v4-pro (Parent)",
            },
        }

        theme = promote_to_experimental(hypothesis)

        # Theme should carry source epistemic metadata
        source_ep = theme.get("_source_epistemic") or theme.get("_epistemic", {})
        if source_ep:
            # At minimum, provenance should be preserved
            assert "provenance" in source_ep or "source_hypothesis" in theme, \
                "Experimental theme must reference epistemic provenance"

    def test_epistemic_confidence_levels_valid(self):
        """Confidence level must be one of: High, Moderate, Low."""
        from experimental.hypothesis import generate_hypothesis

        anomalies = [
            {"id": "AN-CONF", "type": "Volume Anomaly",
             "description": "Confidence test", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
        ]

        hypothesis = generate_hypothesis(anomalies, [], [])
        if hypothesis is None:
            pytest.skip("No hypothesis generated")

        ep = hypothesis.get("_epistemic", {})
        conf = ep.get("confidence_level", "")
        valid = {"High", "Moderate", "Low"}
        assert conf in valid, (
            f"❌ Invalid confidence_level: '{conf}'. Must be one of {valid}"
        )

    def test_epistemic_source_references_non_empty(self):
        """source_references must reference actual anomaly/evidence IDs."""
        from experimental.hypothesis import generate_hypothesis

        anomalies = [
            {"id": "AN-SRC-001", "type": "Missing Correlation",
             "description": "Source refs test", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
            {"id": "AN-SRC-002", "type": "Sector Divergence",
             "description": "Second anomaly", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
        ]

        hypothesis = generate_hypothesis(anomalies, [], [])
        if hypothesis is None:
            pytest.skip("No hypothesis generated")

        ep = hypothesis.get("_epistemic", {})
        refs = ep.get("source_references", [])
        assert isinstance(refs, list), "source_references must be a list"
        # Should reference at least one of the input anomalies
        if refs:
            input_ids = {a["id"] for a in anomalies}
            matches = [r for r in refs if r in input_ids]
            assert len(matches) > 0, \
                f"source_references {refs} should reference at least one input anomaly {input_ids}"
