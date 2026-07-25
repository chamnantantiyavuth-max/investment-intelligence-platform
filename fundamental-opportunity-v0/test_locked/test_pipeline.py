"""Locked tests: Full 6-Stage Pipeline (§3)
Spike verification (28 checks) — pipeline test block.
SYNTHETIC FIXTURES — NOT LIVE DATA.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pipeline import run_pipeline
from display import render_full_report


REQUIRED_KEYS = [
    "thesis_summary",
    "thesis_lifecycle",
    "conviction",
    "macro_context",
    "industry_assessment",
    "company_assessment",
    "earnings_trajectory",
    "valuation_context",
    "key_risks",
    "independent_challenge",
    "supporting_evidence",
    "contradicting_evidence",
    "open_questions",
]


# ── 4 Tests as specified in the spike blueprint ──

class TestPipelineOutput:
    """Verify run_pipeline returns correct structure."""

    def test_returns_8_packages(self):
        """Pipeline processes all 8 fixtures."""
        packages = run_pipeline()
        assert len(packages) == 8, f"Expected 8 packages, got {len(packages)}"
        ids = [p["id"] for p in packages]
        expected_ids = ["AAPL", "INTC", "COST", "CRM", "XYZ", "MSFT", "JNJ", "GE"]
        assert ids == expected_ids, (
            f"Package order mismatch.\n  Expected: {expected_ids}\n  Got:      {ids}"
        )

    def test_each_package_has_13_required_keys(self):
        """Every package contains all 13 required sections."""
        packages = run_pipeline()
        for pkg in packages:
            missing = [k for k in REQUIRED_KEYS if k not in pkg]
            assert not missing, (
                f"{pkg['id']}: missing required key(s): {missing}"
            )

    def test_moat_width_is_non_empty(self):
        """Every package has a non-empty string for moat width."""
        packages = run_pipeline()
        for pkg in packages:
            moat = pkg["company_assessment"]["moat"]
            width = moat["width"]
            assert isinstance(width, str), (
                f"{pkg['id']}: moat_width must be str, got {type(width)}"
            )
            assert len(width) > 0, (
                f"{pkg['id']}: moat_width is empty"
            )
            assert width in ("Wide", "Narrow", "None"), (
                f"{pkg['id']}: moat_width '{width}' not in (Wide, Narrow, None)"
            )


class TestPipelineHtmlOutput:
    """Verify HTML output is generated correctly."""

    def test_html_output_created(self):
        """render_full_report returns valid HTML with expected content."""
        packages = run_pipeline()
        html = render_full_report(packages)

        assert isinstance(html, str), f"Expected str, got {type(html)}"
        assert len(html) > 0, "HTML output is empty"

        # Verify key HTML structures
        assert "<!DOCTYPE html>" in html, "Missing DOCTYPE"
        assert "<html" in html, "Missing <html> tag"
        assert "</html>" in html, "Missing </html> tag"
        assert "Research Packages" in html, "Missing page title"

        # Verify each company appears in the HTML
        for pkg in packages:
            assert pkg["name"] in html, (
                f"Company '{pkg['name']}' missing from HTML output"
            )

        # Verify moat assessment renders
        assert "Moat Assessment" in html
        assert "Earnings Quality" in html
        assert "Valuation Context" in html
        assert "Key Risks" in html
        assert "Open Questions" in html
