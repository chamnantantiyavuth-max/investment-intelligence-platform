"""RFC-9562 UUID v7 generator (M5.3 correction round — FD #138 §8).

M4A canonical schemas require ``UUID v7`` for canonical IDs (retry_id,
stage_id, invocation_id, pit_context_id, evidence_id, admission_id,
source_id, manifest_id, ...).  This module is the narrow single authority
for generating and validating RFC-9562 UUID v7 values in M5.3.

Layout (RFC-9562 §5.7), shown in integer-bit terms (bit 127 = MSB):
- bits 127..80 : 48-bit unix_ts_ms
- bits 79..76  : version = 7 (0b0111)
- bits 75..64  : rand_a (12 bits)
- bits 63..62  : variant = 10 (0b10)
- bits 61..0   : rand_b (62 bits)

NOT a canonical schema — a deterministic utility with direct tests.
"""

from __future__ import annotations

import secrets
import time
import uuid

_TS_SHIFT = 80
_VERSION_SHIFT = 76
_VERSION_VALUE = 0x7
_RANDA_SHIFT = 64
_VARIANT_BITS = 0x2 << 62  # 10 binary at bits 63..62
_RANDB_MASK = (1 << 62) - 1
_VARIANT_MASK = 0x3 << 62
_MAX_TS = 1 << 48


def generate_uuid7(ts_ms: int | None = None) -> uuid.UUID:
    """Return an RFC-9562 UUID v7.

    ``ts_ms`` overrides the current time (milliseconds) for deterministic
    tests.  Randomness comes from the OS CSPRNG (``secrets``).
    """
    if ts_ms is None:
        ts_ms = int(time.time() * 1000)
    if ts_ms < 0 or ts_ms >= _MAX_TS:
        raise ValueError(f"ts_ms out of UUID v7 48-bit range: {ts_ms}")

    random74 = secrets.randbits(74)
    rand_a = (random74 >> 62) & 0xFFF      # 12 bits
    rand_b = random74 & _RANDB_MASK        # 62 bits
    value = (
        (ts_ms << _TS_SHIFT)
        | (_VERSION_VALUE << _VERSION_SHIFT)
        | (rand_a << _RANDA_SHIFT)
        | _VARIANT_BITS
        | rand_b
    )
    return uuid.UUID(int=value)


def is_uuid7(value: str | uuid.UUID) -> bool:
    """Return True iff ``value`` is a well-formed RFC-9562 UUID v7."""
    try:
        u = value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    if u.version != 7:
        return False
    return u.int & _VARIANT_MASK == _VARIANT_BITS