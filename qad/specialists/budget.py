"""Proposed per-charter budget bounds.

M3-05 §3 requires a budget on every investigation charter. M3-05 §6 says
the Research Director does not self-authorize unlimited investigation, and
exhaustion is INCOMPLETE rather than a weakened gate. The numbers below are
the router’s proposed cap for an external desk-research packet. They are not
an RB-01 approval and not an investment threshold.

``qad.m53.retry_kernel.RetryPolicy.max_retries`` is the canonical stage
retry budget (initial + 3). It meters RSR-01 execution inside this process.
It does not meter an external agent’s tool calls, so it is not called here.
"""

from __future__ import annotations

from dataclasses import dataclass

from qad.m53.retry_kernel import RetryPolicy


# Cited so the stage-retry budget stays the kernel’s, not a second copy.
STAGE_RETRY_BUDGET = RetryPolicy().max_retries


class BudgetBoundError(Exception):
    """A charter or a self-reported usage is outside the proposed cap."""


@dataclass(frozen=True)
class Budget:
    max_tool_calls: int
    max_sources: int
    max_minutes: int

    def as_charter_string(self) -> str:
        return (
            f"max_tool_calls={self.max_tool_calls};"
            f"max_sources={self.max_sources};"
            f"max_minutes={self.max_minutes}"
        )

    def exceeds(self, ceiling: Budget) -> bool:
        return (
            self.max_tool_calls > ceiling.max_tool_calls
            or self.max_sources > ceiling.max_sources
            or self.max_minutes > ceiling.max_minutes
        )

    def times(self, count: int) -> Budget:
        return Budget(
            self.max_tool_calls * count,
            self.max_sources * count,
            self.max_minutes * count,
        )


# Per charter, and the case sum of the charters this router may emit.
# 3 x the default equals the case ceiling, so a fourth equal charter cannot.
DEFAULT_CHARTER_BUDGET = Budget(max_tool_calls=8, max_sources=6, max_minutes=90)
PER_CHARTER_CEILING = Budget(max_tool_calls=12, max_sources=8, max_minutes=120)
CASE_BUDGET_CEILING = Budget(max_tool_calls=24, max_sources=18, max_minutes=270)


def parse_budget(text: str) -> Budget:
    parts: dict[str, int] = {}
    for piece in text.split(";"):
        key, _, raw = piece.partition("=")
        if key not in {"max_tool_calls", "max_sources", "max_minutes"}:
            raise BudgetBoundError(f"unknown budget field {key!r}")
        parts[key] = int(raw)
    missing = {"max_tool_calls", "max_sources", "max_minutes"} - parts.keys()
    if missing:
        raise BudgetBoundError(f"budget missing {sorted(missing)}")
    return Budget(
        max_tool_calls=parts["max_tool_calls"],
        max_sources=parts["max_sources"],
        max_minutes=parts["max_minutes"],
    )


def assert_within_charter_ceiling(budget: Budget) -> None:
    if budget.exceeds(PER_CHARTER_CEILING):
        raise BudgetBoundError(
            f"charter budget {budget} exceeds per-charter ceiling "
            f"{PER_CHARTER_CEILING}"
        )
    if min(budget.max_tool_calls, budget.max_sources, budget.max_minutes) < 1:
        raise BudgetBoundError("charter budget components must be at least 1")


def assert_usage_within(usage: dict, budget: Budget) -> None:
    """Enforce self-reported usage. This does not observe the agent."""
    try:
        reported = Budget(
            max_tool_calls=int(usage["tool_calls"]),
            max_sources=int(usage["sources"]),
            max_minutes=int(usage["minutes"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise BudgetBoundError(f"usage is not a complete budget report: {usage!r}") from exc
    if reported.exceeds(budget):
        raise BudgetBoundError(
            f"self-reported usage {reported} exceeds charter budget {budget}"
        )
