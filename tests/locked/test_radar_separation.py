"""
Locked Acceptance Test: Radar Separation (T4-L1)
Parent-written · READ-ONLY for subagents
Verifies Experimental Theme Radar uses experimental data only, zero approved imports.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestRadarSeparation:
    """Radar must use experimental data sources only."""

    def test_radar_does_not_import_pipeline(self):
        """experimental/radar.py must NOT import from pipeline.py."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = ["from pipeline import", "from pipeline import run_pipeline"]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: radar.py imports approved pipeline: '{fb}'"
            )

    def test_radar_does_not_import_display(self):
        """experimental/radar.py must NOT import from display.py."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = ["from display import render_queue", "from display import render_all",
                      "from display import render_theme_cards"]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: radar.py imports approved display: '{fb}'"
            )

    def test_radar_reads_from_experimental_data(self):
        """Radar must read from experimental/ data sources, not approved pipeline."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must use experimental data sources
        experimental_sources = [
            "experimental_result", "EXPERIMENTAL_THEMES", "anomalies",
            "hypotheses", "review_queue",
        ]
        used = [s for s in experimental_sources if s in content]
        assert len(used) >= 2, (
            f"radar.py must use at least 2 experimental data sources. Found: {used}"
        )

    def test_radar_has_off_by_default_indicator(self):
        """Radar must indicate 'Experimental Themes OFF' is the default (FD #27)."""
        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        if not os.path.exists(radar_path):
            pytest.skip("experimental/radar.py not found")

        with open(radar_path, "r", encoding="utf-8") as f:
            content = f.read()

        # The radar template or code must indicate OFF is default
        off_indicators = ["OFF", "off by default", "experimental themes off", "not active"]
        found = any(ind.lower() in content.lower() for ind in off_indicators)
        # Not strictly required in Python code (could be in HTML template)
        # So this is a soft check
        if not found:
            # Check the HTML template instead
            radar_html = os.path.join(AM_V0_DIR, "templates", "radar.html")
            if os.path.exists(radar_html):
                with open(radar_html, "r", encoding="utf-8") as f2:
                    html_content = f2.read()
                found_html = any(ind.lower() in html_content.lower() for ind in off_indicators)
                assert found_html, \
                    "Radar must indicate Experimental Themes OFF is default (FD #27)"

    def test_radar_template_exists(self):
        """templates/radar.html must exist."""
        radar_html = os.path.join(AM_V0_DIR, "templates", "radar.html")
        assert os.path.exists(radar_html), \
            "templates/radar.html must exist for Experimental Theme Radar rendering"
