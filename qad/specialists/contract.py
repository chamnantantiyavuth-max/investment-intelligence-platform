"""Result and task packet contract for external specialist agents.

This is not a canonical schema. Claims become canonical only through
``InMemoryRawSourceArchive.admit_source`` and
``InMemoryEvidenceRegistry.admit_evidence``.
"""

from __future__ import annotations

RESULT_CONTRACT_ID = "qad.specialists.result.v1"
TASK_PACKET_ID = "qad.specialists.task.v1"

# Fields an executing agent must write. ``investigator_charter_id`` is null
# only for a desk assignment that has no IC-01 investigator_type.
RESULT_FIELDS: tuple[str, ...] = (
    "contract",
    "case_id",
    "gap_id",
    "investigator_charter_id",
    "specialist_id",
    "actor_id",
    "canonical_role",
    "desk_research_only",
    "disposition",
    "falsifiable_question",
    "stop_rule_triggered",
    "usage",
    "sampling_limitations",
    "claims",
    "findings",
)

USAGE_FIELDS: tuple[str, ...] = ("tool_calls", "sources", "minutes")

CLAIM_FIELDS: tuple[str, ...] = ("statement", "evidence_type", "source")

# Provenance required before a claim may be admitted. A missing field is
# quarantined and cannot become FactRecord VERIFIED.
SOURCE_PROVENANCE_FIELDS: tuple[str, ...] = (
    "url",
    "retrieval_timestamp",
    "source_date",
    "publisher",
)

SOURCE_FIELDS: tuple[str, ...] = SOURCE_PROVENANCE_FIELDS + (
    "source_tier",
    "title",
    "quotation",
)

# IR-01 has no UNRESOLVED disposition. The token is recorded on the gap
# journal and in IR-01.findings. The IR-01 enum used is NOT_ANSWERED.
SPECIALIST_DISPOSITIONS: frozenset[str] = frozenset(
    {"ANSWERED", "NOT_ANSWERED", "PARTIALLY_ANSWERED", "UNRESOLVED"}
)

IR_DISPOSITION_FOR_SPECIALIST: dict[str, str] = {
    "ANSWERED": "ANSWERED",
    "NOT_ANSWERED": "NOT_ANSWERED",
    "PARTIALLY_ANSWERED": "PARTIALLY_ANSWERED",
    "UNRESOLVED": "NOT_ANSWERED",
}

LIMITATIONS: tuple[str, ...] = (
    "Tool-call, source, and time budgets of an external Grok Cloud agent are "
    "self-reported on the result file. Ingest enforces those reported numbers "
    "against the charter cap. It does not meter the agent's actual calls.",
    "Independence is by separate agent execution plus the same-actor ledger. "
    "It is not cryptographic and not an operating-system identity check.",
    "EG-01 is RECORD_IMMUTABLE in the generated descriptor, including "
    "operational_status and investigator_charter_id. A status rewrite is "
    "rejected. Disposition is recorded on IR-01 when an IC-01 exists, and in "
    "the ingest journal. The stored gap stays at its current status.",
    "Desk-research-only work cannot move SCUTTLEBUTT to COMPLETE. "
    "QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md §1: scuttlebutt is not desk research. "
    "The stage may be IN_PROGRESS or INCOMPLETE.",
    "No RB-01 is written. The Research Budget Controller has not approved the "
    "caps. RC-01 stays DRAFT. The Evidence Intelligence Lead has not validated "
    "the charter. The Research Director does not self-authorize the budget.",
    "H1–H5 for this pilot are Director-drafted from "
    "QAD-FULL-RESEARCH-PROTOCOL.md §2 applied to UNH. They are not "
    "Founder-approved. MANUAL_PILOT is not a canonical entry_route. The case "
    "entry route remains FOUNDER_DIRECTED.",
    "Provenance checks require a URL, retrieval timestamp, source date, and "
    "publisher. A local snapshot is not a receipt. A hand-inserted SRC-01 is "
    "not a receipt. A FACT stays UNVERIFIED unless the passage is in an "
    "S5/M6 receipt minted by an independent HTTP fetch, and the statement's "
    "numbers, negation, direction words, and detectable actors match that "
    "passage. That match is lexical inclusion, not semantic entailment. A "
    "generic RC-01 does not override a mismatch. A sign-off counts only when "
    "it is bound to this case, gap, claim, source, and passage hash. "
    "A case or report read does not fetch. It replays a receipt file written "
    "by the explicit verify command. That file is not a hand-inserted SRC-01.",
    "qad.m53.retry_kernel meters canonical stage retries (initial plus 3). "
    "It is not used to retry an external specialist. Those runs are outside "
    "this process, and a self-reported failure is not a kernel retry.",
    "Management & Capital Allocation has no IC-01 investigator_type. That "
    "charter is a desk assignment bound to the gap. It is not a new schema. "
    "Its claims still enter through the existing admission boundary.",
)
