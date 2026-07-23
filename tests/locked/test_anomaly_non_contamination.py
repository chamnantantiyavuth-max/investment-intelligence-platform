"""
Locked Acceptance Test: Anomaly Non-Contamination (T2-L3)
Parent-written · READ-ONLY for subagents
Verifies anomaly detection output does not contaminate approved pipeline.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestAnomalySeparation:
    """Anomaly module must stay within experimental/ scope."""

    def test_anomaly_does_not_import_pipeline(self):
        """experimental/anomaly.py must NOT import from pipeline.py."""
        an_path = os.path.join(AM_V0_DIR, "experimental", "anomaly.py")
        if not os.path.exists(an_path):
            pytest.skip("experimental/anomaly.py not found")

        with open(an_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = [
            "from pipeline import",
            "from pipeline import stage_universe",
            "from pipeline import stage_theme_context",
            "from pipeline import run_pipeline",
        ]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: anomaly.py imports approved pipeline: '{fb}'"
            )

    def test_anomaly_does_not_import_display(self):
        """experimental/anomaly.py must NOT import from display.py."""
        an_path = os.path.join(AM_V0_DIR, "experimental", "anomaly.py")
        if not os.path.exists(an_path):
            pytest.skip("experimental/anomaly.py not found")

        with open(an_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = ["from display import"]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: anomaly.py imports approved display: '{fb}'"
            )

    def test_anomaly_output_goes_to_inbox_not_pipeline(self):
        """Anomaly detection results must be written via inbox API, not to pipeline_result."""
        an_path = os.path.join(AM_V0_DIR, "experimental", "anomaly.py")
        if not os.path.exists(an_path):
            pytest.skip("experimental/anomaly.py not found")

        with open(an_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must write to inbox API
        assert "from experimental.inbox import" in content or "import experimental.inbox" in content, \
            "anomaly.py must import from experimental.inbox to write anomalies"
        assert "add_anomaly" in content, \
            "anomaly.py must call add_anomaly() to write results to Weak Signal Inbox"

        # Must NOT write directly to approved output
        forbidden_writes = [
            'output/pipeline_result.json',
            'output/queue.html',
        ]
        for path in forbidden_writes:
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if path in stripped and any(w in stripped.lower() for w in ["write", "dump", "save", "open(", "json.dump"]):
                    pytest.fail(
                        f"❌ GUARD VIOLATION: anomaly.py writes to approved path: '{path}'\n"
                        f"   Line: {stripped}"
                    )

    def test_anomaly_reads_inbox_via_api(self):
        """Anomaly module reads existing inbox data via inbox API, not directly."""
        an_path = os.path.join(AM_V0_DIR, "experimental", "anomaly.py")
        if not os.path.exists(an_path):
            pytest.skip("experimental/anomaly.py not found")

        with open(an_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Should use inbox API functions
        inbox_api_used = any(fn in content for fn in ["list_anomalies", "list_hypotheses", "add_anomaly"])
        assert inbox_api_used, "anomaly.py must use inbox API (list_anomalies, list_hypotheses, add_anomaly)"

    def test_anomaly_does_not_modify_approved_themes(self):
        """Anomaly module must not mutate THEMES or CANDIDATES."""
        an_path = os.path.join(AM_V0_DIR, "experimental", "anomaly.py")
        if not os.path.exists(an_path):
            pytest.skip("experimental/anomaly.py not found")

        with open(an_path, "r", encoding="utf-8") as f:
            content = f.read()

        mutations = ["THEMES.", "THEMES[", "THEMES =", "CANDIDATES.", "CANDIDATES[", "CANDIDATES ="]
        for pattern in mutations:
            assert pattern not in content, (
                f"❌ GUARD VIOLATION: anomaly.py mutates approved data: '{pattern}'"
            )
