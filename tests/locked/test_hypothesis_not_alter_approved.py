"""
Locked Acceptance Test: Hypothesis Non-Alteration (T3-L3)
Parent-written · READ-ONLY for subagents
Verifies hypothesis engine does NOT modify approved data (THEMES, CANDIDATES, pipeline).
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestHypothesisSeparation:
    """Hypothesis engine must stay within experimental/ scope."""

    def test_hypothesis_does_not_import_pipeline(self):
        """experimental/hypothesis.py must NOT import from pipeline.py."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = [
            "from pipeline import",
            "from pipeline import stage_universe",
            "from pipeline import stage_theme_context",
            "from pipeline import run_pipeline",
        ]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: hypothesis.py imports approved pipeline: '{fb}'"
            )

    def test_hypothesis_does_not_import_display(self):
        """experimental/hypothesis.py must NOT import from display.py."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = ["from display import"]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: hypothesis.py imports approved display: '{fb}'"
            )

    def test_hypothesis_uses_inbox_api(self):
        """Hypothesis engine must read anomalies from inbox and write hypotheses to inbox."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must use inbox for input
        assert "list_anomalies" in content or "add_hypothesis" in content, \
            "hypothesis.py must use inbox API (list_anomalies, add_hypothesis)"

    def test_hypothesis_does_not_mutate_approved_themes(self):
        """Hypothesis engine must NOT mutate THEMES or CANDIDATES."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        mutations = ["THEMES.append", "THEMES.extend", "THEMES[", "THEMES =",
                      "CANDIDATES.append", "CANDIDATES[", "CANDIDATES ="]
        for pattern in mutations:
            assert pattern not in content, (
                f"❌ GUARD VIOLATION: hypothesis.py mutates approved data: '{pattern}'"
            )

    def test_hypothesis_creates_experimental_themes_not_approved(self):
        """promote_to_experimental() must create themes in EXPERIMENTAL_THEMES,
        not in approved THEMES."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must create experimental themes with TH-EXP- prefix
        assert "TH-EXP-" in content, \
            "hypothesis.py must create themes with TH-EXP- prefix (experimental scope)"

    def test_hypothesis_uses_separate_pipeline_stages(self):
        """Hypothesis engine must use CONSTITUTIONALLY SEPARATE stages,
        NOT stage_universe/stage_theme_context from approved pipeline."""
        hyp_path = os.path.join(AM_V0_DIR, "experimental", "hypothesis.py")
        if not os.path.exists(hyp_path):
            pytest.skip("experimental/hypothesis.py not found")

        with open(hyp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must NOT reference any approved stage function names
        approved_stages = [
            "stage_universe", "stage_theme_context", "stage_candidate_quality",
            "stage_entry_readiness", "stage_data_confidence", "stage_queue",
        ]
        for stage_fn in approved_stages:
            assert stage_fn not in content, (
                f"❌ GUARD VIOLATION: hypothesis.py references approved stage: '{stage_fn}'\n"
                f"   FD #27 Guard #1: Must use constitutionally separate pipeline stages"
            )
