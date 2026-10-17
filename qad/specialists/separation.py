"""Same-actor separation of duties.

Source: design/qad-pivot/QAD-M3-ROLE-AND-SERVICE-REGISTRY.md §4
(Separation of Duties Matrix) and §6 (Role Compatibility), including §7
independence domains where they decide whether one actor may hold both roles.

§4 rows marked ALLOWED describe workflow (Red Team output reaches the
Underwriter; the editor does not create the thesis). They are not permission
for one actor to hold both roles on the same case. §7 keeps domains A–E
separate. A specialist who executed on a case cannot also be Structural Red
Team, Independent Research Auditor, or Chief Underwriter for that case.
"""

from __future__ import annotations

from dataclasses import dataclass


RESEARCH_DIRECTOR = "Research Director"
EVIDENCE_INTELLIGENCE = "Evidence Intelligence Lead"
CORE_DESK = "Core Desk Researcher"
BUSINESS_INDUSTRY = "Business & Industry Analyst"
FINANCIAL_MANAGEMENT = "Financial & Management Analyst"
IMPAIRMENT = "Impairment Diagnosis Specialist"
VALUATION = "Valuation & Expectations Specialist"
CHIEF_UNDERWRITER = "Chief Underwriter"
RED_TEAM = "Structural Red Team"
AUDITOR = "Independent Research Auditor"
EDITOR = "Thai Long-Form Research Editor"
STEWARD = "Thesis / Knowledge Steward"
SCOUT = "Discovery & Dislocation Scout"
ELASTIC = "Elastic Investigator"
FOUNDER = "Founder"
PORTFOLIO_MANAGER = "Portfolio Manager"
SELECTION_ENGINE = "Selection Engine"

ANALYTICAL_ROLES: frozenset[str] = frozenset(
    {
        CORE_DESK,
        BUSINESS_INDUSTRY,
        FINANCIAL_MANAGEMENT,
        IMPAIRMENT,
        VALUATION,
        ELASTIC,
    }
)

# Roles a specialist execution must not also hold on the same case.
INDEPENDENCE_ROLES: frozenset[str] = frozenset(
    {RED_TEAM, AUDITOR, CHIEF_UNDERWRITER, FOUNDER}
)

# Unordered pairs. One actor, one case.
FORBIDDEN_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({RESEARCH_DIRECTOR, AUDITOR}),
        frozenset({RESEARCH_DIRECTOR, RED_TEAM}),
        frozenset({EVIDENCE_INTELLIGENCE, AUDITOR}),
        frozenset({BUSINESS_INDUSTRY, CHIEF_UNDERWRITER}),
        frozenset({FINANCIAL_MANAGEMENT, CHIEF_UNDERWRITER}),
        frozenset({IMPAIRMENT, CHIEF_UNDERWRITER}),
        frozenset({VALUATION, CHIEF_UNDERWRITER}),
        frozenset({CORE_DESK, CHIEF_UNDERWRITER}),
        frozenset({ELASTIC, CHIEF_UNDERWRITER}),
        frozenset({SCOUT, SELECTION_ENGINE}),
        frozenset({SELECTION_ENGINE, CHIEF_UNDERWRITER}),
        frozenset({SELECTION_ENGINE, RESEARCH_DIRECTOR}),
        frozenset({CHIEF_UNDERWRITER, PORTFOLIO_MANAGER}),
        frozenset({RED_TEAM, AUDITOR}),
        frozenset({RED_TEAM, CHIEF_UNDERWRITER}),
        frozenset({AUDITOR, CHIEF_UNDERWRITER}),
        frozenset({FOUNDER, RESEARCH_DIRECTOR}),
        frozenset({FOUNDER, RED_TEAM}),
        frozenset({FOUNDER, AUDITOR}),
        frozenset({FOUNDER, CHIEF_UNDERWRITER}),
        frozenset({EDITOR, RESEARCH_DIRECTOR}),
        frozenset({EDITOR, CHIEF_UNDERWRITER}),
    }
)


class SeparationViolation(Exception):
    """The same actor would hold incompatible roles on one case."""

    def __init__(self, message: str, *, actor_id: str, roles: list[str]) -> None:
        self.actor_id = actor_id
        self.roles = roles
        super().__init__(message)


@dataclass(frozen=True)
class SeparationDecision:
    allowed: bool
    actor_id: str
    roles: tuple[str, ...]
    conflict: str
    citation: str = (
        "design/qad-pivot/QAD-M3-ROLE-AND-SERVICE-REGISTRY.md §§4, 6, 7"
    )


def check_roles(actor_id: str, roles: list[str]) -> SeparationDecision:
    """Return whether one actor may hold all of ``roles`` on one case."""
    unique = tuple(dict.fromkeys(roles))
    analytical = [role for role in unique if role in ANALYTICAL_ROLES]
    blocked = [role for role in unique if role in INDEPENDENCE_ROLES]
    if analytical and blocked:
        return SeparationDecision(
            allowed=False,
            actor_id=actor_id,
            roles=unique,
            conflict=(
                f"specialist execution {analytical[0]} cannot also be "
                f"{blocked[0]} on the same case"
            ),
        )
    for index, left in enumerate(unique):
        for right in unique[index + 1 :]:
            if frozenset({left, right}) in FORBIDDEN_PAIRS:
                return SeparationDecision(
                    allowed=False,
                    actor_id=actor_id,
                    roles=unique,
                    conflict=f"{left} × {right} is forbidden for one actor",
                )
    return SeparationDecision(
        allowed=True,
        actor_id=actor_id,
        roles=unique,
        conflict="",
    )


def check_assignment(
    existing: list[tuple[str, str]],
    actor_id: str,
    role: str,
) -> SeparationDecision:
    """Check ``role`` against roles this actor already holds on the case."""
    held = [prior for actor, prior in existing if actor == actor_id]
    return check_roles(actor_id, [*held, role])


def require_assignment(
    existing: list[tuple[str, str]],
    actor_id: str,
    role: str,
) -> SeparationDecision:
    decision = check_assignment(existing, actor_id, role)
    if not decision.allowed:
        raise SeparationViolation(
            decision.conflict,
            actor_id=actor_id,
            roles=list(decision.roles),
        )
    return decision
