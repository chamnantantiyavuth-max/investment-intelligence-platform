"""
Locked Acceptance Test: Inbox Separation (T1-L3)
Parent-written · READ-ONLY for subagents
Verifies inbox module does not leak into approved pipeline scope.
"""
import os, sys, pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestInboxSeparation:
    """Inbox module must stay within experimental/ scope."""

    def test_inbox_does_not_import_pipeline(self):
        """experimental/inbox.py must NOT import from pipeline.py."""
        inbox_path = os.path.join(AM_V0_DIR, "experimental", "inbox.py")
        if not os.path.exists(inbox_path):
            pytest.skip("experimental/inbox.py not found")

        with open(inbox_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = [
            "from pipeline import",
            "from pipeline import stage_universe",
            "from pipeline import stage_theme_context",
            "from pipeline import stage_candidate_quality",
            "from pipeline import stage_entry_readiness",
            "from pipeline import stage_data_confidence",
            "from pipeline import stage_queue",
        ]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: inbox.py imports approved pipeline: '{fb}'"
            )

    def test_inbox_does_not_import_display(self):
        """experimental/inbox.py must NOT import from display.py."""
        inbox_path = os.path.join(AM_V0_DIR, "experimental", "inbox.py")
        if not os.path.exists(inbox_path):
            pytest.skip("experimental/inbox.py not found")

        with open(inbox_path, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden = ["from display import", "from display import render_queue"]
        for fb in forbidden:
            assert fb not in content, (
                f"❌ GUARD VIOLATION: inbox.py imports approved display: '{fb}'"
            )

    def test_inbox_writes_to_experimental_scope_only(self):
        """Inbox data must be stored in experimental/ scope, not in approved output."""
        inbox_path = os.path.join(AM_V0_DIR, "experimental", "inbox.py")
        if not os.path.exists(inbox_path):
            pytest.skip("experimental/inbox.py not found")

        with open(inbox_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must not write to the approved output directory
        forbidden_paths = [
            'output/pipeline_result.json',
            'output/queue.html',
            'output/theme_cards',
        ]
        for path in forbidden_paths:
            if path in content:
                # Check context: is this a write or just a comment?
                for line in content.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        continue
                    if path in stripped and any(w in stripped for w in ["write", "dump", "save", "open"]):
                        pytest.fail(
                            f"❌ GUARD VIOLATION: inbox.py writes to approved path: '{path}'\n"
                            f"   Line: {stripped}"
                        )

    def test_inbox_does_not_modify_approved_themes(self):
        """Inbox must not modify fixtures.THEMES or fixtures.CANDIDATES."""
        inbox_path = os.path.join(AM_V0_DIR, "experimental", "inbox.py")
        if not os.path.exists(inbox_path):
            pytest.skip("experimental/inbox.py not found")

        with open(inbox_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Inbox may read THEMES for reference, but must not assign/mutate
        mutation_patterns = [
            "THEMES.append", "THEMES.extend", "THEMES.insert",
            "THEMES[", "THEMES =",
            "CANDIDATES.append", "CANDIDATES.extend", "CANDIDATES.insert",
            "CANDIDATES[", "CANDIDATES =",
        ]
        for pattern in mutation_patterns:
            assert pattern not in content, (
                f"❌ GUARD VIOLATION: inbox.py mutates approved data: '{pattern}'\n"
                f"   FD #27 Guard #3: Experimental themes must NOT alter official data"
            )
