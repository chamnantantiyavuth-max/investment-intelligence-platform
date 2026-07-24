"""
Locked Acceptance Test: Hypothesis Promotion (T3-L1)
Parent-written · READ-ONLY for subagents
Verifies hypothesis generation engine produces well-formed output + promotion path.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestHypothesisGeneration:
    """Hypothesis engine must produce well-formed hypotheses from anomaly patterns."""

    def test_generate_hypothesis_from_anomalies(self):
        """generate_hypothesis(anomalies, evidence, existing_themes) → Hypothesis dict."""
        from experimental.hypothesis import generate_hypothesis

        anomalies = [
            {"id": "AN-001", "type": "Sector Divergence", "description": "Healthcare RS surge",
             "first_observed": "2024-07-01", "status": "Unexplained", "source": "EOD",
             "related_theme": "TH-014", "related_tickers": ["ISRG", "SYK"]},
        ]
        evidence = [
            {"id": "EV-007", "type": "Observed Fact", "content": "MDT Q4 revenue +5.2% YoY",
             "relationship": "supporting", "theme": "TH-014"},
        ]
        existing_themes = [
            {"id": "TH-014", "name": "Medical Devices", "sector": "Healthcare"},
        ]

        hypothesis = generate_hypothesis(anomalies, evidence, existing_themes)

        # Must have required fields
        required = ["id", "title", "proposed_driver", "why_now", "potential_candidates",
                     "key_unknowns", "status", "proposed_date"]
        for field in required:
            assert field in hypothesis, f"Missing required field: {field}"

        # ID must start with HY-
        assert hypothesis["id"].startswith("HY-"), \
            f"Hypothesis ID must start with HY-, got {hypothesis['id']}"

        # Status must indicate awaiting review
        assert "awaiting Founder review" in hypothesis["status"] or "Hypothesis" in hypothesis["status"], \
            f"Invalid status: {hypothesis['status']}"

    def test_analyze_anomalies_for_patterns(self):
        """analyze_anomalies_for_patterns(anomalies) → list of pattern candidates."""
        from experimental.hypothesis import analyze_anomalies_for_patterns

        anomalies = [
            {"id": "AN-001", "type": "Sector Divergence", "description": "Healthcare RS surge",
             "related_theme": "TH-014", "related_tickers": ["ISRG", "SYK"]},
            {"id": "AN-003", "type": "Volume Anomaly", "description": "Cyber vol spike",
             "related_theme": "TH-030", "related_tickers": ["CRWD", "PANW"]},
        ]

        patterns = analyze_anomalies_for_patterns(anomalies)
        assert isinstance(patterns, list), f"Expected list, got {type(patterns).__name__}"

        # Each pattern should identify grouping
        for p in patterns:
            assert "anomaly_ids" in p or "description" in p, \
                "Each pattern must have anomaly_ids or description"

    def test_promote_to_experimental_creates_theme(self):
        """promote_to_experimental(hypothesis_id) → ExperimentalTheme with TH-EXP- ID."""
        from experimental.hypothesis import promote_to_experimental

        hypothesis = {
            "id": "HY-TEST-001",
            "title": "Test Theme Hypothesis",
            "proposed_driver": "Test structural driver",
            "why_now": "Immediate catalyst",
            "potential_candidates": ["AAPL", "MSFT"],
            "key_unknowns": ["Unknown X"],
            "status": "Hypothesis — awaiting Founder review",
            "proposed_date": "2024-07-24",
            "potential_theme_industry": "Test Industry",
        }

        theme = promote_to_experimental(hypothesis)

        assert theme is not None, "promote_to_experimental must return a theme dict"
        assert "id" in theme
        assert theme["id"].startswith("TH-EXP-"), \
            f"Experimental theme ID must start with TH-EXP-, got {theme['id']}"
        assert theme.get("approval_status") == "Experimental", \
            f"Must have approval_status='Experimental', got {theme.get('approval_status')}"
        assert theme.get("name") == hypothesis["title"], \
            "Theme name should match hypothesis title"

    def test_promote_updates_hypothesis_status(self):
        """After promotion, hypothesis status should reflect promoted state."""
        from experimental.hypothesis import promote_to_experimental

        hypothesis = {
            "id": "HY-PROMO-002",
            "title": "Promotable",
            "proposed_driver": "Test",
            "why_now": "Test",
            "potential_candidates": [],
            "key_unknowns": [],
            "status": "Hypothesis — awaiting Founder review",
            "proposed_date": "2024-07-24",
            "potential_theme_industry": "Test",
        }

        promote_to_experimental(hypothesis)

        # Hypothesis status should have changed
        assert "Promoted" in hypothesis.get("status", ""), \
            f"Expected status to contain 'Promoted', got {hypothesis.get('status')}"

    def test_empty_anomalies_returns_empty_hypothesis(self):
        """Empty anomaly list → generate_hypothesis returns None or empty."""
        from experimental.hypothesis import generate_hypothesis

        result = generate_hypothesis([], [], [])
        # Should return None or a hypothesis indicating no patterns found
        if result is not None:
            # If it returns a dict, it should indicate no discovery
            assert result.get("status") is not None
