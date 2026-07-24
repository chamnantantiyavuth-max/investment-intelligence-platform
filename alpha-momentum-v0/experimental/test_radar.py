"""
Supplementary tests for experimental/radar.py — Experimental Theme Radar (T4).

Verifies template rendering, data integrity, constitutional separation,
and output isolation. Complements the locked acceptance tests.

Run: python -m pytest alpha-momentum-v0/experimental/test_radar.py -v
"""

import os
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)

import pytest


class TestRadarRenderOutput:
    """Verify radar rendering produces correct output."""

    def test_render_radar_returns_path(self):
        """render_radar returns a string path to HTML file."""
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(result, output_dir=tmpdir)
            assert isinstance(path, str)
            assert path.endswith("radar.html")
            assert os.path.exists(path)

    def test_render_radar_output_contains_expected_content(self):
        """Rendered HTML contains key radar elements."""
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(result, output_dir=tmpdir)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            # Must contain Experimental Themes OFF indicator
            assert "Experimental Themes OFF" in html

            # Must reference experimental data
            assert "Experimental Theme Radar" in html

            # Must contain anomaly data if anomalies exist
            if result.get("anomalies"):
                assert "Anomalies" in html

            # Must contain hypotheses if they exist
            if result.get("hypotheses"):
                assert "Hypotheses" in html

    def test_render_radar_default_output_dir(self):
        """Default output dir is output/experimental/."""
        from experimental.radar import render_radar, EXPERIMENTAL_OUTPUT_DIR
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        path = render_radar(result)
        assert EXPERIMENTAL_OUTPUT_DIR in path
        assert "radar.html" in path

        # Clean up
        if os.path.exists(path):
            os.remove(path)


class TestRadarDataIntegrity:
    """Verify radar does not corrupt or alter data."""

    def test_render_radar_does_not_mutate_input(self):
        """render_radar must not modify the input experimental_result dict."""
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        original = str(result)

        with tempfile.TemporaryDirectory() as tmpdir:
            render_radar(result, output_dir=tmpdir)

        # Result dict should be unchanged
        assert str(result) == original, "render_radar mutated input dict"

    def test_render_radar_handles_empty_data(self):
        """render_radar handles empty experimental result gracefully."""
        from experimental.radar import render_radar

        empty_result = {
            "run_id": "EXP-TEST",
            "pipeline_version": "exp-test",
            "point_in_time": "2024-07-01",
            "fixture_category": "TEST",
            "anomalies": [],
            "hypotheses": [],
            "experimental_themes": [],
            "review_queue": {},
            "stages": [],
            "has_data": False,
            "message": "No experimental data",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(empty_result, output_dir=tmpdir)
            assert os.path.exists(path)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            assert "Experimental Themes OFF" in html

    def test_render_radar_with_partial_data(self):
        """Renders with anomalies only, no hypotheses or themes."""
        from experimental.radar import render_radar

        partial_result = {
            "run_id": "EXP-PARTIAL",
            "pipeline_version": "exp-test",
            "point_in_time": "2024-07-01",
            "fixture_category": "TEST",
            "anomalies": [
                {
                    "id": "AN-TEST-001",
                    "type": "Sector Divergence",
                    "description": "Test anomaly",
                    "first_observed": "2024-07-01",
                    "status": "Unexplained",
                    "source": "test",
                    "related_tickers": ["AAPL"],
                }
            ],
            "hypotheses": [],
            "experimental_themes": [],
            "review_queue": {},
            "stages": [],
            "has_data": True,
            "message": "Partial data",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(partial_result, output_dir=tmpdir)
            assert os.path.exists(path)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            assert "AN-TEST-001" in html
            assert "Sector Divergence" in html


class TestRadarOffByDefault:
    """Verify Experimental Themes OFF is properly indicated (FD #27)."""

    def test_off_indicator_in_html(self):
        """Rendered HTML contains OFF indicator."""
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(result, output_dir=tmpdir)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            assert "OFF" in html and "Experimental" in html

    @pytest.mark.parametrize("indicator", [
        "Experimental Themes OFF",
        "experimental themes off",
    ])
    def test_off_indicator_case_insensitive(self, indicator):
        """OFF indicator is visible regardless of casing."""
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = render_radar(result, output_dir=tmpdir)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            found = indicator.lower() in html.lower()
            assert found, f"Expected '{indicator}' in radar HTML"


class TestRadarConstitutionalSeparation:
    """Verify constitutional separation from approved pipeline/output."""

    def test_radar_does_not_import_pipeline(self):
        """radar.py must NOT import from pipeline.py."""
        import ast

        radar_path = os.path.join(AM_V0_DIR, "experimental", "radar.py")
        with open(radar_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                # Only forbid root-level pipeline.py and display.py imports
                if module in ("pipeline", "display"):
                    pytest.fail(
                        f"radar.py imports forbidden module: {module}"
                )

    def test_radar_writes_to_experimental_output(self):
        """Rendered file goes to experimental output dir, not approved queue."""
        from experimental.radar import render_radar, EXPERIMENTAL_OUTPUT_DIR
        from experimental.pipeline import run_experimental_pipeline

        result = run_experimental_pipeline()
        path = render_radar(result)
        assert "output" in path and "experimental" in path
        assert "radar.html" in path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    def test_radar_does_not_mutate_fixtures(self):
        """Radar functions must not mutate fixtures.THEMES or CANDIDATES."""
        import fixtures as f
        from experimental.radar import render_radar
        from experimental.pipeline import run_experimental_pipeline

        themes_before = len(f.THEMES)
        candidates_before = len(f.CANDIDATES)

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            render_radar(result, output_dir=tmpdir)

        assert len(f.THEMES) == themes_before, "THEMES must not be mutated by radar"
        assert len(f.CANDIDATES) == candidates_before, "CANDIDATES must not be mutated by radar"


class TestRadarTemplate:
    """Verify the radar.html template exists and is well-formed."""

    def test_radar_template_exists(self):
        """templates/radar.html must exist."""
        template_path = os.path.join(AM_V0_DIR, "templates", "radar.html")
        assert os.path.exists(template_path), "templates/radar.html not found"

    def test_radar_template_extends_base(self):
        """radar.html must extend base.html."""
        template_path = os.path.join(AM_V0_DIR, "templates", "radar.html")
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert '{% extends "base.html" %}' in content, \
            "radar.html must extend base.html"


class TestRadarExportJSON:
    """Verify radar JSON export."""

    def test_export_radar_json(self):
        """export_radar_json creates valid JSON."""
        from experimental.radar import export_radar_json
        from experimental.pipeline import run_experimental_pipeline
        import json

        result = run_experimental_pipeline()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_radar_json(result, output_dir=tmpdir)
            assert os.path.exists(path)
            assert path.endswith("radar.json")

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "experimental_themes_off" in data
            assert data["experimental_themes_off"] is True
            assert "anomaly_count" in data
            assert "hypothesis_count" in data

    def test_export_radar_json_empty(self):
        """export_radar_json handles empty results."""
        from experimental.radar import export_radar_json
        import json

        empty = {
            "anomalies": [],
            "hypotheses": [],
            "experimental_themes": [],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_radar_json(empty, output_dir=tmpdir)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["anomaly_count"] == 0
            assert data["hypothesis_count"] == 0
