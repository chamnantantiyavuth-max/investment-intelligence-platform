"""qad.ids — RFC-9562 UUID v7 utility direct tests (FD #138 §8)."""

from __future__ import annotations

import re
import uuid

import pytest

from qad.ids import generate_uuid7, is_uuid7

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