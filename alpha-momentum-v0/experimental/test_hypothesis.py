"""Additional tests for experimental/hypothesis.py — Theme Hypothesis Engine.

Covers edge cases, epistemic metadata validation, pattern analysis,
and experimental theme storage beyond what locked tests verify.
"""
import os
import sys
import pytest
from datetime import datetime, date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestAnalyzeAnomaliesForPatterns:
    """Edge cases for pattern analysis."""

    def test_empty_anomalies_returns_empty_list(self):
        """Empty anomaly list -> empty patterns."""
        from experimental.hypothesis import analyze_anomalies_for_patterns
        assert analyze_anomalies_for_patterns([]) == []

    def test_single_anomaly_creates_theme_cluster(self):
        """Single anomaly with related_theme generates one pattern."""
        from experimental.hypothesis import analyze_anomalies_for_patterns
        anomalies = [
            {"id": "AN-001", "type": "Sector Divergence",
             "description": "Test", "related_theme": "TH-014",
             "related_tickers": ["ISRG", "SYK"]},
        ]
        patterns = analyze_anomalies_for_patterns(anomalies)
        assert len(patterns) >= 1
        for p in patterns:
            assert "anomaly_ids" in p
            assert "description" in p

    def test_multiple_anomalies_same_theme(self):
        """Multiple anomalies sharing a theme -> one theme cluster."""
        from experimental.hypothesis import analyze_anomalies_for_patterns
        anomalies = [
            {"id": "AN-001", "type": "Sector Divergence",
             "related_theme": "TH-014", "related_tickers": ["ISRG"]},
            {"id": "AN-002", "type": "Volume Anomaly",
             "related_theme": "TH-014", "related_tickers": ["SYK"]},
        ]
        patterns = analyze_anomalies_for_patterns(anomalies)
        theme_patterns = [p for p in patterns if p.get("pattern_type") == "theme_cluster"]
        clusters = [p for p in theme_patterns if p.get("common_theme") == "TH-014"]
        assert len(clusters) == 1
        assert "AN-001" in clusters[0]["anomaly_ids"]
        assert "AN-002" in clusters[0]["anomaly_ids"]

    def test_anomalies_no_related_theme(self):
        """Anomalies without related_theme still produce patterns (type cluster)."""
        from experimental.hypothesis import analyze_anomalies_for_patterns
        anomalies = [
            {"id": "AN-001", "type": "Volume Anomaly",
             "description": "Cyber vol spike", "related_tickers": ["CRWD"]},
            {"id": "AN-002", "type": "Volume Anomaly",
             "description": "Cloud vol spike", "related_tickers": ["AMZN"]},
        ]
        patterns = analyze_anomalies_for_patterns(anomalies)
        type_patterns = [p for p in patterns if p.get("pattern_type") == "type_cluster"]
        assert len(type_patterns) >= 1
        assert "Volume Anomaly" in type_patterns[0].get("description", "")


class TestGenerateHypothesisEdgeCases:
    """Edge cases for hypothesis generation."""

    def test_empty_anomalies_returns_none(self):
        """Empty anomaly list -> None."""
        from experimental.hypothesis import generate_hypothesis
        assert generate_hypothesis([], [], []) is None

    def test_generated_hypothesis_has_epistemic(self):
        """Every generated hypothesis must carry _epistemic metadata."""
        from experimental.hypothesis import generate_hypothesis
        hyp = generate_hypothesis(
            [{"id": "AN-X1", "type": "Sector Divergence",
              "description": "Test", "first_observed": "2024-07-24",
              "status": "Unexplained", "source": "EOD"}],
            [],
            [],
        )
        assert hyp is not None
        assert "_epistemic" in hyp
        ep = hyp["_epistemic"]
        assert isinstance(ep, dict)
        for field in ["provenance", "confidence_level", "version",
                       "source_references", "as_of_time", "model_provenance"]:
            assert field in ep, f"Missing epistemic field: {field}"

    def test_hypothesis_id_starts_with_hy(self):
        """Hypothesis ID must start with HY-."""
        from experimental.hypothesis import generate_hypothesis
        hyp = generate_hypothesis(
            [{"id": "AN-ID1", "type": "Sector Divergence",
              "description": "ID test", "first_observed": "2024-07-24",
              "status": "Unexplained", "source": "EOD"}],
            [],
            [],
        )
        assert hyp is not None
        assert hyp["id"].startswith("HY-"), f"ID {hyp['id']} must start with HY-"

    def test_source_references_include_anomaly_ids(self):
        """source_references must reference input anomaly IDs."""
        from experimental.hypothesis import generate_hypothesis
        anomalies = [
            {"id": "AN-SRC-1", "type": "Volume Anomaly",
             "description": "Src test", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
            {"id": "AN-SRC-2", "type": "Missing Correlation",
             "description": "Src test 2", "first_observed": "2024-07-24",
             "status": "Unexplained", "source": "EOD"},
        ]
        hyp = generate_hypothesis(anomalies, [], [])
        assert hyp is not None
        refs = hyp["_epistemic"].get("source_references", [])
        input_ids = {a["id"] for a in anomalies}
        matches = [r for r in refs if r in input_ids]
        assert len(matches) > 0, f"source_references {refs} must include input anomalies {input_ids}"


class TestPromoteToExperimental:
    """Experimental theme promotion edge cases."""

    def test_promote_returns_theme_with_exp_id(self):
        """Promoted theme must have TH-EXP- ID."""
        from experimental.hypothesis import promote_to_experimental
        theme = promote_to_experimental({
            "id": "HY-PTEST", "title": "Promote Test",
            "proposed_driver": "Test", "why_now": "Now",
            "potential_candidates": [], "key_unknowns": [],
            "status": "Hypothesis - awaiting Founder review",
            "proposed_date": "2024-07-24",
        })
        assert theme is not None
        assert theme["id"].startswith("TH-EXP-")

    def test_promote_sets_experimental_status(self):
        """Theme must have approval_status='Experimental'."""
        from experimental.hypothesis import promote_to_experimental
        theme = promote_to_experimental({
            "id": "HY-STAT", "title": "Status Test",
            "proposed_driver": "Test", "why_now": "Now",
            "potential_candidates": [], "key_unknowns": [],
            "status": "Hypothesis - awaiting Founder review",
            "proposed_date": "2024-07-24",
        })
        assert theme.get("approval_status") == "Experimental"

    def test_promote_updates_hypothesis_status(self):
        """Hypothesis status must contain 'Promoted' after promotion."""
        from experimental.hypothesis import promote_to_experimental
        hypothesis = {
            "id": "HY-UPD", "title": "Update Test",
            "proposed_driver": "Test", "why_now": "Now",
            "potential_candidates": [], "key_unknowns": [],
            "status": "Hypothesis - awaiting Founder review",
            "proposed_date": "2024-07-24",
        }
        promote_to_experimental(hypothesis)
        assert "Promoted" in hypothesis.get("status", "")

    def test_promote_stores_in_experimental_themes(self):
        """Theme must be stored in EXPERIMENTAL_THEMES list."""
        from experimental.hypothesis import promote_to_experimental, EXPERIMENTAL_STORE
        count_before = len(EXPERIMENTAL_STORE)
        theme = promote_to_experimental({
            "id": "HY-STOR", "title": "Storage Test",
            "proposed_driver": "Test", "why_now": "Now",
            "potential_candidates": [], "key_unknowns": [],
            "status": "Hypothesis - awaiting Founder review",
            "proposed_date": "2024-07-24",
        })
        assert len(EXPERIMENTAL_STORE) == count_before + 1
        assert EXPERIMENTAL_STORE[-1]["id"] == theme["id"]
