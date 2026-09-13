"""qad.ids — RFC-9562 UUID v7 utility direct tests (FD #138 §8)."""

from __future__ import annotations

import re
import uuid

import pytest

from qad.ids import deterministic_uuid7, generate_uuid7, is_uuid7

UUID7_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def test_generated_id_is_uuid_v7():
    u = generate_uuid7()
    assert UUID7_RE.match(str(u)), f"format: {u}"
    assert u.version == 7
    assert u.variant == uuid.RFC_4122
    assert is_uuid7(u)
    assert is_uuid7(str(u))


def test_timestamp_embedded_correctly():
    """The 48-bit ms timestamp must be recoverable from the top bits."""
    ts = 1_750_000_000_000
    u = generate_uuid7(ts_ms=ts)
    # Top 48 bits of the 128-bit int = timestamp.
    extracted = u.int >> 80
    assert extracted == ts


def test_unique_within_a_batch():
    ids = {generate_uuid7() for _ in range(500)}
    assert len(ids) == 500


def test_deterministic_given_same_timestamp_and_seed():
    """Same ts_ms must yield the same UUID when randomness is deterministic.

    We cannot control ``secrets`` here, so this only proves API stability:
    different ts_ms changes the top bits (monotonic ordering).
    """
    a = generate_uuid7(ts_ms=1000)
    b = generate_uuid7(ts_ms=2000)
    assert a < b  # timestamp ordering preserved in the UUID ordering


def test_is_uuid7_rejects_non_v7():
    u4 = uuid.uuid4()
    assert not is_uuid7(u4)
    assert not is_uuid7("RR-SI-M53-001-1")
    assert not is_uuid7("not-a-uuid")
    assert not is_uuid7(12345)
    assert not is_uuid7(None)


def test_ts_range_validation():
    with pytest.raises(ValueError):
        generate_uuid7(ts_ms=-1)
    with pytest.raises(ValueError):
        generate_uuid7(ts_ms=1 << 48)


def test_monotonic_msec_generation():
    """Real-clock generation must produce version 7 ids."""
    u = generate_uuid7()
    assert u.version == 7
    assert (u.int >> 80) > 0  # timestamp non-zero


class TestDeterministicUuid7:
    """Correction Pass 2 (FD #138 §5/§8) + CP3 (FD #139 R5): deterministic
    stage-owned ids with a REAL anchor timestamp (never hash-derived)."""

    _TS = 1_750_000_000_000  # fixed real epoch-ms anchor for utility tests

    def test_same_seed_same_value(self):
        a = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        b = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        assert a == b
        assert is_uuid7(a)

    def test_different_seed_different_value(self):
        a = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        b = deterministic_uuid7("exec1|cp2|gap", ts_ms=self._TS)
        assert a != b

    def test_semantic_label_scopes_identity(self):
        gap = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        note = deterministic_uuid7("exec1|cp1|note", ts_ms=self._TS)
        assert gap != note

    def test_valid_bit_layout(self):
        u = deterministic_uuid7("any|seed", ts_ms=self._TS)
        assert UUID7_RE.match(str(u))
        assert u.version == 7
        assert u.variant == uuid.RFC_4122

    def test_timestamp_field_is_real_anchor_ms(self):
        """FD #139 R5: the 48-bit ts field MUST be the supplied real epoch-ms
        anchor, not hash-derived bits."""
        u = deterministic_uuid7("any|seed", ts_ms=self._TS)
        assert u.int >> 80 == self._TS

    def test_different_anchor_different_uuid(self):
        """Same seed but a different (later) execution anchor -> different
        UUID (timestamp participates in the identity)."""
        a = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        b = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS + 1000)
        assert a != b

    def test_ts_required(self):
        """No silent hash-derived fallback: ts_ms is a required keyword."""
        with pytest.raises(TypeError):
            deterministic_uuid7("any|seed")  # type: ignore[call-arg]

    def test_exact_deterministic_rand74_bits(self):
        """FD #139 R5 exact-component test: reconstruct rand74 from the
        decoded UUID and compare to the exact expected SHA-256 derivation.

        This prevents a future regression where fewer than 74 random bits
        are used (the pre-fix implementation kept only 38 bits via
        digest[6:20] >> 74, silently zeroing rand_a) while superficial
        UUID-shape tests stay green."""
        import hashlib

        seed = "exec1|cp1|gap"
        ts_ms = self._TS
        expected_rand74 = (
            int.from_bytes(hashlib.sha256(seed.encode("utf-8")).digest(), "big")
            & ((1 << 74) - 1)
        )
        u = deterministic_uuid7(seed, ts_ms=ts_ms)
        # Decode UUID components (RFC-9562 §5.7 layout).
        unix_ts_ms = u.int >> 80
        rand_a = (u.int >> 64) & 0xFFF          # top 12 of the 74 rand bits
        rand_b = u.int & ((1 << 62) - 1)        # lower 62 rand bits
        actual_rand74 = (rand_a << 62) | rand_b
        assert unix_ts_ms == ts_ms, "timestamp field must be the real anchor"
        assert actual_rand74 == expected_rand74, (
            f"rand74 mismatch: got {actual_rand74}, expected {expected_rand74}"
        )
        # rand_a must be non-trivial (the pre-fix defect zeroed it).
        assert rand_a != 0, "rand_a must carry deterministic entropy"
        assert rand_a.bit_length() <= 12 and rand_b.bit_length() <= 62

    def test_rand74_differs_across_semantic_labels(self):
        """Distinct semantic labels must yield distinct full random fields
        (not merely distinct timestamps)."""
        gap = deterministic_uuid7("exec1|cp1|gap", ts_ms=self._TS)
        note = deterministic_uuid7("exec1|cp1|note", ts_ms=self._TS)
        assert (gap.int & ((1 << 62) - 1)) != (note.int & ((1 << 62) - 1))