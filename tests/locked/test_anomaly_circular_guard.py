"""
Locked Acceptance Test: Anomaly Circular Feedback Guard (T2-L2)
Parent-written · READ-ONLY for subagents
Verifies cooldown mechanism prevents anomaly→hypothesis→theme→anomaly loops.
Per FD #27 §4: Circular feedback guard requires cooldown/staleness.
"""
import os, sys, pytest
from datetime import date, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AM_V0_DIR = os.path.join(REPO_ROOT, "alpha-momentum-v0")
sys.path.insert(0, AM_V0_DIR)


class TestCircularFeedbackCooldown:
    """Anomaly promoted to hypothesis must not re-trigger within cooldown window."""

    def test_suppress_anomaly_within_cooldown(self):
        """Anomaly observed within 30 days of promotion → suppressed."""
        from experimental.anomaly import check_cooldown

        today = date(2024, 7, 1)
        last_promoted = today - timedelta(days=5)

        result = check_cooldown("AN-001", last_promoted, today, cooldown_days=30)
        assert result["suppress"] is True, \
            f"Should suppress (delta=5d < 30d cooldown), got suppress={result['suppress']}"
        assert result["cooldown_remaining_days"] == 25

    def test_allow_anomaly_after_cooldown(self):
        """Anomaly observed AFTER cooldown window → allowed."""
        from experimental.anomaly import check_cooldown

        today = date(2024, 8, 15)
        last_promoted = date(2024, 7, 1)

        result = check_cooldown("AN-001", last_promoted, today, cooldown_days=30)
        assert result["suppress"] is False, \
            f"Should allow (delta=45d > 30d cooldown), got suppress={result['suppress']}"

    def test_no_prior_promotion_allows_anomaly(self):
        """Anomaly with no prior promotion → always allowed."""
        from experimental.anomaly import check_cooldown

        result = check_cooldown("AN-NEW", None, date(2024, 7, 1), cooldown_days=30)
        assert result["suppress"] is False, \
            "Anomaly with no prior promotion should not be suppressed"

    def test_different_anomaly_not_suppressed(self):
        """Cooldown is per-anomaly-signature — different anomaly ID not affected."""
        from experimental.anomaly import check_cooldown

        today = date(2024, 7, 5)
        promoted = date(2024, 7, 1)  # AN-001 promoted 4 days ago

        # AN-001 should be suppressed
        r1 = check_cooldown("AN-001", promoted, today, cooldown_days=30)
        assert r1["suppress"] is True

        # AN-002 should NOT be suppressed (different signature)
        r2 = check_cooldown("AN-002", None, today, cooldown_days=30)
        assert r2["suppress"] is False, \
            "Different anomaly signature should not be affected by AN-001 cooldown"

    def test_cooldown_window_configurable(self):
        """Cooldown days should be configurable."""
        from experimental.anomaly import check_cooldown

        today = date(2024, 7, 10)
        promoted = date(2024, 7, 1)  # 9 days ago

        # 30-day cooldown: should suppress
        r30 = check_cooldown("AN-001", promoted, today, cooldown_days=30)
        assert r30["suppress"] is True

        # 7-day cooldown: should allow
        r7 = check_cooldown("AN-001", promoted, today, cooldown_days=7)
        assert r7["suppress"] is False


class TestCooldownTracking:
    """Cooldown state must persist across anomaly detection cycles."""

    def test_promotion_updates_cooldown_state(self):
        """After promoting anomaly to hypothesis, cooldown state is recorded."""
        from experimental.anomaly import record_promotion, check_cooldown

        today = date(2024, 7, 1)
        record_promotion("AN-TEST", today)
        result = check_cooldown("AN-TEST", today, date(2024, 7, 5), cooldown_days=30)
        assert result["suppress"] is True, \
            "After record_promotion, anomaly within 30d should be suppressed"

    def test_cooldown_state_persists_across_calls(self):
        """Promotion tracking should survive between function calls."""
        from experimental.anomaly import record_promotion, check_cooldown, clear_promotion_tracking
        # Clean start
        clear_promotion_tracking()

        today = date(2024, 7, 1)
        record_promotion("AN-PERSIST", today)

        # Multiple calls should all see the cooldown
        for _ in range(3):
            r = check_cooldown("AN-PERSIST", today, date(2024, 7, 5), cooldown_days=30)
            assert r["suppress"] is True, "Cooldown state not persisting across calls"

        clear_promotion_tracking()
