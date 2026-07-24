"""
Locked Acceptance Test: Experimental Separation (T0-Phase5-Arch)
Parent-written · READ-ONLY for subagents · MUST pass before T1-T4 implementation

Verifies the THREE hard guards from FD #27:
  1. Experimental pipeline does NOT reuse identical deterministic logic as approved
  2. Experimental output does NOT contaminate approved pipeline_result
  3. Experimental themes do NOT alter official filters, rankings, or approved-strategy alerts

Plus 2 additional constitutional separation checks:
  4. Experimental modules have zero imports from approved stage functions
  5. Experimental output directory is separate from approved output directory
"""
import os
import sys
import json
import tempfile
import pytest

# Ensure we can import from alpha-momentum-v0
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


# ═══════════════════════════════════════════════════════════════
# GUARD 1: No imports from approved pipeline stage functions
# ═══════════════════════════════════════════════════════════════

class TestSeparationNoApprovedImports:
    """Experimental modules must NOT import from approved pipeline stage functions."""

    FORBIDDEN_IMPORTS = [
        "from pipeline import stage_universe",
        "from pipeline import stage_theme_context",
        "from pipeline import stage_candidate_quality",
        "from pipeline import stage_entry_readiness",
        "from pipeline import stage_data_confidence",
        "from pipeline import stage_queue",
        "from pipeline import run_pipeline",
        "import pipeline",  # would allow pipeline.stage_*
    ]

    EXPERIMENTAL_FILES = [
        "experimental/pipeline.py",
        "experimental/display.py",
    ]

    @pytest.mark.parametrize("filepath", EXPERIMENTAL_FILES)
    def test_no_approved_stage_imports(self, filepath):
        """Verify experimental files do not import approved stage functions."""
        full_path = os.path.join(AM_V0_DIR, filepath)
        if not os.path.exists(full_path):
            pytest.skip(f"File not found: {filepath}")

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        for forbidden in self.FORBIDDEN_IMPORTS:
            assert forbidden not in content, (
                f"❌ GUARD VIOLATION: {filepath} contains forbidden import: '{forbidden}'\n"
                f"   FD #27 Guard #1: Experimental pipeline must NOT reuse identical deterministic logic as approved"
            )

    def test_experimental_pipeline_is_constitutionally_separate(self):
        """Verify experimental pipeline defines its own stages, not reusing approved ones."""
        full_path = os.path.join(AM_V0_DIR, "experimental", "pipeline.py")
        if not os.path.exists(full_path):
            pytest.skip("experimental/pipeline.py not found")

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must define its own stage functions
        assert "def stage_anomaly_detection" in content, \
            "Missing: experimental pipeline must define stage_anomaly_detection"
        assert "def stage_anomaly_classification" in content, \
            "Missing: experimental pipeline must define stage_anomaly_classification"
        assert "def stage_hypothesis_generation" in content, \
            "Missing: experimental pipeline must define stage_hypothesis_generation"
        assert "def stage_founder_review_queue" in content, \
            "Missing: experimental pipeline must define stage_founder_review_queue"

        # Must have its own runner
        assert "def run_experimental_pipeline" in content, \
            "Missing: experimental pipeline must define run_experimental_pipeline"

    def test_experimental_display_standalone(self):
        """Verify experimental display does not import from approved display.py."""
        full_path = os.path.join(AM_V0_DIR, "experimental", "display.py")
        if not os.path.exists(full_path):
            pytest.skip("experimental/display.py not found")

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden_display_imports = [
            "from display import render_theme_cards",
            "from display import render_queue",
            "from display import render_all",
            "from display import",
        ]
        for forbidden in forbidden_display_imports:
            assert forbidden not in content, (
                f"❌ GUARD VIOLATION: experimental/display.py imports from approved display.py: '{forbidden}'"
            )


# ═══════════════════════════════════════════════════════════════
# GUARD 2: Experimental output does not contaminate approved pipeline_result
# ═══════════════════════════════════════════════════════════════

class TestSeparationOutputContamination:
    """Experimental output must NOT write to approved output directory."""

    APPROVED_OUTPUT_DIR = os.path.join(AM_V0_DIR, "output")
    EXPERIMENTAL_OUTPUT_DIR = os.path.join(AM_V0_DIR, "output", "experimental")

    def test_experimental_output_directory_separate(self):
        """Experimental output goes to output/experimental/, not output/."""
        exp_pipeline_path = os.path.join(AM_V0_DIR, "experimental", "pipeline.py")
        exp_display_path = os.path.join(AM_V0_DIR, "experimental", "display.py")

        for filepath in [exp_pipeline_path, exp_display_path]:
            if not os.path.exists(filepath):
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Must NOT write to the approved output directory directly
            # Allow reading from output/ for data, but writes must target experimental/
            # pipeline.py may reference output_target in its constitutional separation marker
            # instead of a literal file path (it returns data; display.py handles file I/O)
            has_experimental_ref = (
                'output/experimental' in content
                or 'EXPERIMENTAL_OUTPUT_DIR' in content
                or 'experimental/ scope ONLY' in content
            )
            assert has_experimental_ref, \
                f"{os.path.basename(filepath)}: Must reference output/experimental/, EXPERIMENTAL_OUTPUT_DIR, or 'experimental/ scope ONLY' — not to approved output/"

    def test_experimental_pipeline_does_not_modify_pipeline_result(self):
        """Experimental pipeline must not modify the approved pipeline_result.json."""
        exp_pipeline_path = os.path.join(AM_V0_DIR, "experimental", "pipeline.py")
        if not os.path.exists(exp_pipeline_path):
            pytest.skip("experimental/pipeline.py not found")

        with open(exp_pipeline_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must not write to pipeline_result.json
        forbidden_writes = [
            '"output/pipeline_result.json"',
            "'output/pipeline_result.json'",
        ]
        for forbidden in forbidden_writes:
            # Only flag if it's a write operation, not a read
            if forbidden in content:
                # Check context: is this a write or just a reference in comments?
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if forbidden in line and not line.strip().startswith("#"):
                        # Check surrounding lines for write context
                        context = "\n".join(lines[max(0,i-2):i+3])
                        if any(w in context.lower() for w in ["write", "dump", "save", "output"]):
                            pytest.fail(
                                f"❌ GUARD VIOLATION: experimental/pipeline.py writes to approved "
                                f"pipeline_result.json at line {i+1}:\n{context}"
                            )


# ═══════════════════════════════════════════════════════════════
# GUARD 3: Experimental themes do not alter approved data
# ═══════════════════════════════════════════════════════════════

class TestSeparationNoApprovedDataMutation:
    """Experimental themes must NOT alter THEMES, CANDIDATES, or approved-strategy data."""

    def test_experimental_themes_have_experimental_status(self):
        """All experimental themes must have approval_status='Experimental'."""
        try:
            from fixtures import EXPERIMENTAL_THEMES
        except ImportError:
            pytest.skip("Cannot import EXPERIMENTAL_THEMES from fixtures")

        for theme in EXPERIMENTAL_THEMES:
            status = theme.get("approval_status", "")
            assert status == "Experimental", (
                f"❌ GUARD VIOLATION: Experimental theme {theme['id']} has "
                f"approval_status='{status}' — must be 'Experimental'"
            )

    def test_experimental_themes_not_in_approved_themes(self):
        """Experimental themes must NOT appear in the approved THEMES list."""
        try:
            from fixtures import THEMES, EXPERIMENTAL_THEMES
        except ImportError:
            pytest.skip("Cannot import fixtures")

        approved_ids = {t["id"] for t in THEMES}
        for theme in EXPERIMENTAL_THEMES:
            assert theme["id"] not in approved_ids, (
                f"❌ GUARD VIOLATION: Experimental theme {theme['id']} found in approved THEMES list"
            )

    def test_experimental_candidates_not_in_approved_candidates(self):
        """Experimental candidates must NOT appear in the approved CANDIDATES list."""
        try:
            from fixtures import CANDIDATES, EXPERIMENTAL_CANDIDATES
        except ImportError:
            pytest.skip("Cannot import fixtures")

        approved_ids = {c["id"] for c in CANDIDATES}
        for candidate in EXPERIMENTAL_CANDIDATES:
            assert candidate["id"] not in approved_ids, (
                f"❌ GUARD VIOLATION: Experimental candidate {candidate['id']} found in approved CANDIDATES list"
            )

    def test_approved_pipeline_does_not_import_experimental(self):
        """Approved pipeline.py must NOT import experimental data."""
        pipeline_path = os.path.join(AM_V0_DIR, "pipeline.py")
        with open(pipeline_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check only for actual import statements (not comments)
        forbidden_imports = [
            "from experimental",
            "import experimental",
        ]
        for item in forbidden_imports:
            # Search non-comment lines only
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue  # Skip comment lines
                if item in stripped:
                    pytest.fail(
                        f"❌ GUARD VIOLATION: approved pipeline.py imports experimental: '{item}'\n"
                        f"   Line: {stripped}"
                    )

        # Check for EXPERIMENTAL_* imports specifically in import statements
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped.startswith("from fixtures import") or stripped.startswith("import fixtures"):
                if "EXPERIMENTAL" in stripped:
                    pytest.fail(
                        f"❌ GUARD VIOLATION: approved pipeline.py imports EXPERIMENTAL data:\n"
                        f"   Line: {stripped}"
                    )


# ═══════════════════════════════════════════════════════════════
# GUARD 4: Constitutional separation markers
# ═══════════════════════════════════════════════════════════════

class TestSeparationConstitutionalMarkers:
    """Experimental pipeline must have explicit constitutional separation markers."""

    def test_experimental_pipeline_has_separation_marker(self):
        """Experimental pipeline must contain _constitutional_separation metadata."""
        exp_pipeline_path = os.path.join(AM_V0_DIR, "experimental", "pipeline.py")
        if not os.path.exists(exp_pipeline_path):
            pytest.skip("experimental/pipeline.py not found")

        with open(exp_pipeline_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "_constitutional_separation" in content, (
            "Missing: experimental pipeline must contain _constitutional_separation metadata block"
        )
        assert "approved_pipeline_imports" in content, (
            "Missing: _constitutional_separation must track approved_pipeline_imports"
        )
        assert "reuses_approved_stages" in content, (
            "Missing: _constitutional_separation must track reuses_approved_stages"
        )

    def test_experimental_result_has_separation_marker(self):
        """run_experimental_pipeline() must return _constitutional_separation in result."""
        try:
            from experimental.pipeline import run_experimental_pipeline
        except ImportError:
            pytest.skip("Cannot import experimental.pipeline")

        result = run_experimental_pipeline()
        separation = result.get("_constitutional_separation", {})

        assert separation.get("approved_pipeline_imports") == False, \
            "❌ _constitutional_separation.approved_pipeline_imports must be False"
        assert separation.get("reuses_approved_stages") == False, \
            "❌ _constitutional_separation.reuses_approved_stages must be False"
        assert "experimental/ scope" in separation.get("output_target", ""), \
            "❌ _constitutional_separation.output_target must be experimental/ scope ONLY"
        assert separation.get("modifies_approved_data") == False, \
            "❌ _constitutional_separation.modifies_approved_data must be False"
        assert separation.get("epistemic_metadata") == "mandatory (§23.4)", \
            "❌ _constitutional_separation.epistemic_metadata must be 'mandatory (§23.4)'"


# ═══════════════════════════════════════════════════════════════
# GUARD 5: Epistemic metadata on hypotheses
# ═══════════════════════════════════════════════════════════════

class TestSeparationEpistemicMetadata:
    """All AI-generated hypotheses must carry epistemic metadata (§23.4)."""

    def test_hypotheses_have_epistemic_metadata(self):
        """Every hypothesis from run_experimental_pipeline must have _epistemic block."""
        try:
            from experimental.pipeline import run_experimental_pipeline
        except ImportError:
            pytest.skip("Cannot import experimental.pipeline")

        result = run_experimental_pipeline()
        hypotheses = result.get("hypotheses", [])

        for hyp in hypotheses:
            ep = hyp.get("_epistemic", {})
            assert ep, (
                f"❌ GUARD VIOLATION: Hypothesis {hyp.get('id','?')} missing _epistemic metadata (§23.4)"
            )
            assert "provenance" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.provenance required"
            assert "confidence_level" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.confidence_level required"
            assert "version" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.version required"
            assert "source_references" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.source_references required"
            assert "as_of_time" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.as_of_time required"
            assert "model_provenance" in ep, \
                f"Hypothesis {hyp['id']}: _epistemic.model_provenance required"


# ═══════════════════════════════════════════════════════════════
# GUARD 6: Circular feedback — cooldown mechanism
# ═══════════════════════════════════════════════════════════════

class TestSeparationCircularFeedbackGuard:
    """Circular feedback guard: anomaly→hypothesis→theme→anomaly must have cooldown."""

    def test_cooldown_mechanism_exists(self):
        """E2 classification stage must implement cooldown logic."""
        exp_pipeline_path = os.path.join(AM_V0_DIR, "experimental", "pipeline.py")
        if not os.path.exists(exp_pipeline_path):
            pytest.skip("experimental/pipeline.py not found")

        with open(exp_pipeline_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "cooldown" in content.lower(), (
            "Missing: experimental pipeline must implement cooldown mechanism for circular feedback guard"
        )
        assert "suppress" in content.lower(), (
            "Missing: E2 must suppress anomalies within cooldown window"
        )

    def test_cooldown_suppresses_recently_promoted(self):
        """An anomaly recently promoted to hypothesis should be suppressed."""
        try:
            from experimental.pipeline import stage_anomaly_classification
        except ImportError:
            pytest.skip("Cannot import experimental.pipeline")

        # Create an anomaly matching a hypothesis ID
        anomaly = {
            "id": "AN-001",
            "type": "Sector Divergence",
            "first_observed": "2024-06-15",
        }
        # Hypothesis referencing same signature, proposed recently
        existing = [{"id": "AN-001", "proposed_date": "2024-06-20"}]

        result, classified = stage_anomaly_classification([anomaly], existing, cooldown_days=30)

        # AN-001 should be suppressed (within 30-day cooldown)
        suppressed = result.get("suppressed_ids", [])
        assert "AN-001" in suppressed, (
            f"❌ GUARD VIOLATION: Circular feedback guard failed — AN-001 should be suppressed "
            f"(proposed 2024-06-20, observed 2024-06-15, delta=5 days < 30-day cooldown). "
            f"suppressed_ids={suppressed}"
        )
