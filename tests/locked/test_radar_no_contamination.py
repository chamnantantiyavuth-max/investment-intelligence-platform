"""
Locked Acceptance Test: Radar Non-Contamination (T4-L2)
Parent-written · READ-ONLY for subagents
Verifies radar output goes to output/experimental/ — NEVER to approved output.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestRadarNonContamination:
    """Radar output must stay in output/experimental/ scope."""

    def test_radar_writes_to_experimental_output(self):
        """Radar must write to output/experimental/radar.html, not output/queue.html."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must write to experimental output directory
        assert "output/experimental" in content or "EXPERIMENTAL_OUTPUT_DIR" in content or "experimental" in content.lower(), \
            "radar.py must write to output/experimental/ scope"

    def test_radar_does_not_write_to_approved_queue(self):
        """Radar must NOT overwrite output/queue.html."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must NOT write to approved queue path
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "queue.html" in stripped and not "experimental" in stripped:
                if any(w in stripped.lower() for w in ["write", "dump", "save", "open(", "render"]):
                    pytest.fail(
                        f"❌ GUARD VIOLATION: radar.py writes to approved queue.html\n"
                        f"   Line: {stripped}"
                    )

    def test_radar_does_not_modify_approved_templates(self):
        """Radar must NOT modify approved templates (queue.html, base.html as write target)."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        mutations = [
            "templates/queue.html",  # as write target
        ]
        for pattern in mutations:
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if pattern in stripped and any(w in stripped.lower() for w in ["write", "open(", "dump", "save"]):
                    pytest.fail(
                        f"❌ GUARD VIOLATION: radar.py writes to approved template: '{pattern}'\n"
                        f"   Line: {stripped}"
                    )

    def test_radar_does_not_mutate_approved_themes(self):
        """Radar must NOT mutate THEMES or CANDIDATES."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        mutations = ["THEMES.", "THEMES[", "THEMES =", "CANDIDATES.", "CANDIDATES[", "CANDIDATES ="]
        for pattern in mutations:
            assert pattern not in content, (
                f"❌ GUARD VIOLATION: radar.py mutates approved data: '{pattern}'"
            )

    def test_radar_renders_from_experimental_pipeline_result(self):
        """Radar rendering must consume experimental pipeline_result, not approved."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must read from experimental pipeline result
        assert "experimental" in content.lower(), \
            "radar.py must reference experimental data (not approved pipeline_result)"
