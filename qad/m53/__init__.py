"""M5.3 — QAD runtime infrastructure (reference implementation).

Bounded scope per Founder GO (8 Sep 2026, OPTION A):

- S7  — PIT Runtime Enforcement (``pit_enforcement``)
- S8  — Retry Kernel + RRM integration (``retry_kernel``)
- Minimum PIT-aware query substrate — ONLY what S7 requires:
  ``PITEnforcementService.query()`` (EV-01 collection, PIT-filtered) and
  ``PITEnforcementService.access()`` (explicit single-record access).

NOT included (M5.2 §11.3, explicitly deferred): full Query API, filter DSL,
sort/paginate framework, cross-store joins, full-text search, time-series
queries, graph traversal, ORM/DB abstraction, production adapter selection.

All implementations are REFERENCE / NON-PRODUCTION — in-memory stores, public
interfaces only (no private in-memory internals are depended upon).
"""
from __future__ import annotations

# Re-export errors surfaced by M5.3 services
from qad.persistence import PITBlockError

from qad.m53.pit_enforcement import PITEnforcementService, PITQueryResult, PITVerdict
from qad.m53.retry_kernel import (
    ExecutionContext,
    RetryKernel,
    RetryOutcome,
    RetryPolicy,
    RetryableError,
    StageContext,
)

__all__ = [
    "PITBlockError",
    "PITEnforcementService",
    "PITQueryResult",
    "PITVerdict",
    "ExecutionContext",
    "RetryableError",
    "RetryKernel",
    "RetryOutcome",
    "RetryPolicy",
    "StageContext",
]