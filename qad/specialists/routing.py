"""Research Director router.

Reads the case's Research Charter and H1–H5, ranks the Evidence Gap Map
with the §6 EIV bands, and emits bounded charters plus task packets.
It does not execute the investigations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from qad.ids import deterministic_uuid7
from qad.models.family_b import (
    EvidenceGap,
    EvidenceGapOperational_status,
    HypothesisRecord,
    HypothesisRecordHypothesis_label,
    HypothesisRecordPlausibility,
)
from qad.models.family_c import (
    HypothesisSet,
    InvestigatorCharter,
    InvestigatorCharterExpected_information_value,
    InvestigatorCharterInvestigator_type,
    ResearchCharter,
    ResearchCharterCharter_state,
)
from qad.specialists.budget import (
    CASE_BUDGET_CEILING,
    DEFAULT_CHARTER_BUDGET,
    Budget,
    assert_within_charter_ceiling,
)
from qad.specialists.catalog import get_specialist, load_catalog
from qad.specialists.contract import LIMITATIONS, RESULT_CONTRACT_ID, RESULT_FIELDS, TASK_PACKET_ID
from qad.specialists.scoring import RankedGap, natural_selection, rank_gaps
from qad.specialists.stages import transition_stage
from research.qad_pilot.unh.case_slice import ANCHOR_TS_MS, AS_OF_DATE, OPENED_AT

STOP_RULE = (
    "EVIDENCE_SUFFICIENT or BUDGET_EXHAUSTED or "
    "COUNTER_EVIDENCE_FOUND or TIME_EXPIRED"
)

# Protocol §2 definitions applied to the UNH pilot. Director-drafted.
# Not a Founder approval and not a new hypothesis taxonomy.
UNH_HYPOTHESES: tuple[dict[str, str], ...] = (
    {
        "label": "H1",
        "statement": (
            "H1 Temporary impairment: UnitedHealth is a quality business whose "
            "2025 operating-margin break is a temporary headwind with a likely recovery. "
            "Director-drafted from QAD-FULL-RESEARCH-PROTOCOL.md §2. Not Founder-approved."
        ),
        "falsification_criteria": (
            "Falsified if UnitedHealth is not a high-quality business, or the margin "
            "break is not a temporary headwind with a likely recovery."
        ),
    },
    {
        "label": "H2",
        "statement": (
            "H2 Structural deterioration: the business model or the industry funding "
            "of UnitedHealth is permanently damaged, rather than delayed. "
            "Director-drafted from QAD-FULL-RESEARCH-PROTOCOL.md §2. Not Founder-approved."
        ),
        "falsification_criteria": (
            "Falsified if neither the business model nor the industry is permanently damaged."
        ),
    },
    {
        "label": "H3",
        "statement": (
            "H3 Mixed: some UnitedHealth economics are genuinely impaired and others "
            "remain intact, and the net direction is unclear. "
            "Director-drafted from QAD-FULL-RESEARCH-PROTOCOL.md §2. Not Founder-approved."
        ),
        "falsification_criteria": (
            "Falsified if the damage is not mixed, or the net direction is clear."
        ),
    },
    {
        "label": "H4",
        "statement": (
            "H4 Quality assumption wrong: UnitedHealth was never a high-quality business, "
            "so the quality premise of the case fails. "
            "Director-drafted from QAD-FULL-RESEARCH-PROTOCOL.md §2. Not Founder-approved."
        ),
        "falsification_criteria": (
            "Falsified if the quality premise holds and it was a high-quality business."
        ),
    },
    {
        "label": "H5",
        "statement": (
            "H5 Valuation already fair: the impairment may be real, but the market price "
            "already reflects it, so there is no asymmetry. "
            "Director-drafted from QAD-FULL-RESEARCH-PROTOCOL.md §2. Not Founder-approved."
        ),
        "falsification_criteria": (
            "Falsified if a real impairment is not already reflected in the price, "
            "so asymmetry remains, or if there is no real impairment."
        ),
    },
)


def _uid(seed: str, ts_ms: int) -> str:
    return str(deterministic_uuid7(seed, ts_ms=ts_ms))


def _enum(value: object) -> str:
    return getattr(value, "value", value)  # type: ignore[return-value]


@dataclass
class IssuedCharter:
    gap_id: str
    specialist_id: str
    display_name: str
    canonical_role: str
    investigator_type: str | None
    investigator_charter_id: str | None
    falsifiable_question: str
    question: str
    eiv: str
    budget: str
    why: str
    override: bool
    charter_record: dict
    task_packet: dict


@dataclass
class RouteResult:
    case_id: str
    natural: list[dict]
    selected: list[IssuedCharter]
    override: dict
    charter_id: str
    hypothesis_ids: list[str]
    limitations: tuple[str, ...] = field(default_factory=lambda: LIMITATIONS)


def _existing_charter(registry, case_id: str):
    rows = [row for row in registry.list_all("RC-01") if row.case_id == case_id]
    return rows[0] if rows else None


def ensure_hypotheses(registry, case_id: str, ts_ms: int) -> list[str]:
    """Store H1–H5 when the case has none. Wording is the protocol applied to UNH."""
    existing = {
        _enum(row.hypothesis_label): row
        for row in registry.list_all("HYP-01")
        if row.case_id == case_id
    }
    if len(existing) == 5:
        return [existing[label] .hypothesis_id for label in ("H1", "H2", "H3", "H4", "H5")]
    ids: list[str] = []
    for spec in UNH_HYPOTHESES:
        hypothesis_id = _uid(f"hyp:{case_id}:{spec['label']}", ts_ms)
        ids.append(hypothesis_id)
        registry.store(
            HypothesisRecord(
                case_id=case_id,
                falsification_criteria=spec["falsification_criteria"],
                hypothesis_id=hypothesis_id,
                hypothesis_label=HypothesisRecordHypothesis_label(spec["label"]),
                initial_plausibility=HypothesisRecordPlausibility.UNCLEAR,
                originator="Research Director",
                statement=spec["statement"],
                created_at=OPENED_AT,
                current_plausibility=HypothesisRecordPlausibility.UNCLEAR,
                status_history=[
                    f"{OPENED_AT} Director-drafted UNCLEAR. Not Founder-approved. "
                    "MANUAL/FOUNDER_DIRECTED pilot."
                ],
            )
        )
    return ids


def ensure_research_charter(
    registry,
    case_id: str,
    hypothesis_ids: list[str],
    key_questions: list[str],
    ts_ms: int,
) -> str:
    existing = _existing_charter(registry, case_id)
    if existing is not None:
        return existing.charter_id
    charter_id = _uid(f"rc:{case_id}", ts_ms)
    registry.store(
        ResearchCharter(
            budget_estimate=CASE_BUDGET_CEILING.as_charter_string(),
            case_id=case_id,
            charter_id=charter_id,
            charter_state=ResearchCharterCharter_state.DRAFT,
            director="Research Director",
            evidence_lead_validation=(
                "NOT_VALIDATED. Evidence Intelligence Lead has not validated this "
                "Director draft. MANUAL/FOUNDER_DIRECTED pilot. Not Founder-approved."
            ),
            evidence_scope=(
                "Desk research on public filings and government data for the selected "
                "evidence gaps. No interviews, surveys, or site visits."
            ),
            hypothesis_ids=hypothesis_ids,
            key_questions=key_questions,
            created_at=OPENED_AT,
            material_blind_spots=[
                "Charter is DRAFT. Budget Controller has not approved an RB-01.",
                "H1–H5 are Director-drafted, not Founder-approved.",
                "MANUAL_PILOT is not a canonical entry_route. Entry route remains FOUNDER_DIRECTED.",
            ],
            source_plan="Public L1, L3, L4, L5, L6, L7 sources named on each charter. L8, L9, and L10 are out of scope.",
            timeline=f"Case as-of {AS_OF_DATE}. Proposed caps only.",
        )
    )
    registry.store(
        HypothesisSet(
            case_id=case_id,
            charter_id=charter_id,
            hypothesis_ids=hypothesis_ids,
            hypothesis_set_id=_uid(f"hs:{case_id}", ts_ms),
            created_at=OPENED_AT,
            creator="Research Director",
        )
    )
    return charter_id


def _draft_gap(registry, case_id: str, spec: dict, ts_ms: int) -> EvidenceGap:
    gap_id = _uid(f"gap:{case_id}:{spec['specialist_id']}", ts_ms)
    if registry.contains("EG-01", gap_id):
        return registry.load("EG-01", gap_id)
    gap = EvidenceGap(
        gap_id=gap_id,
        case_id=case_id,
        created_by="Research Director",
        importance=spec["importance"],
        operational_status=EvidenceGapOperational_status.UNRESOLVED,
        question=spec["question"],
        resolvability_class=spec["resolvability_class"],
        created_at=OPENED_AT,
        falsifiable_question=spec["falsifiable_question"],
    )
    registry.store(gap)
    return gap


def _best_for(ranked: list[RankedGap], specialist_id: str, used: set[str]) -> RankedGap | None:
    for item in ranked:
        if item.specialist_id == specialist_id and item.gap_id not in used:
            return item
    return None


def _why(item: RankedGap, override: bool) -> str:
    base = (
        f"EIV {item.eiv} from importance {item.importance} and "
        f"resolvability {item.resolvability_class} "
        "(QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md §6)"
    )
    if override:
        return base + ". Selected by the documented Founder-priority override."
    return base + ". Selected by deterministic EIV order."


def _charter_question(item: RankedGap) -> str:
    """Use a real falsifier. UNH gap notes are status text, not the question."""
    note = (item.falsifiable_question or "").strip()
    if note and not note.startswith(("No IC-01", "The ", "Those ")):
        return note
    return item.question


def _packet(
    *,
    case_id: str,
    item: RankedGap,
    specialist: dict,
    charter_id: str | None,
    budget: Budget,
    falsifiable: str,
) -> dict:
    gap_id = item.gap_id
    return {
        "packet_version": TASK_PACKET_ID,
        "case_id": case_id,
        "gap_id": gap_id,
        "specialist_id": specialist["specialist_id"],
        "display_name": specialist["display_name"],
        "canonical_role": specialist["canonical_role"],
        "investigator_type": specialist.get("investigator_type"),
        "investigator_charter_id": charter_id,
        "desk_research_only": True,
        "falsifiable_question": falsifiable,
        "gap_note": item.falsifiable_question,
        "question": item.question,
        "allowed_source_classes": list(specialist["allowed_source_classes"]),
        "budget": {
            "max_tool_calls": budget.max_tool_calls,
            "max_sources": budget.max_sources,
            "max_minutes": budget.max_minutes,
            "charter_string": budget.as_charter_string(),
            "approved_by_budget_controller": False,
        },
        "stop_rule": STOP_RULE,
        "forbidden_actions": list(specialist["forbidden_actions"]),
        "domain_instructions": specialist["domain_instructions"],
        "protocol_citation": specialist["protocol_citation"],
        "preferred_sources": list(specialist["preferred_sources"]),
        "result_path": f"research/qad-cases/{case_id}/results/{gap_id}.json",
        "summary_path": f"research/qad-cases/{case_id}/results/{gap_id}.md",
        "summary_language": "th",
        "result_contract": {
            "id": RESULT_CONTRACT_ID,
            "fields": list(RESULT_FIELDS),
            "usage_fields": ["tool_calls", "sources", "minutes"],
            "source_provenance_fields": [
                "url",
                "retrieval_timestamp",
                "source_date",
                "publisher",
            ],
            "dispositions": [
                "ANSWERED",
                "NOT_ANSWERED",
                "PARTIALLY_ANSWERED",
                "UNRESOLVED",
            ],
        },
        "independence": (
            "Execute as a separate agent from Structural Red Team, Independent "
            "Research Auditor, Chief Underwriter, and Founder for this case."
        ),
    }


def _issue_one(
    registry,
    case_id: str,
    item: RankedGap,
    specialist: dict,
    budget: Budget,
    ts_ms: int,
    override: bool,
) -> IssuedCharter:
    investigator_type = specialist.get("investigator_type")
    falsifiable = _charter_question(item)
    charter_payload: dict
    charter_model_id: str | None = None
    if investigator_type:
        charter_model_id = _uid(f"ic:{case_id}:{item.gap_id}:{specialist['specialist_id']}", ts_ms)
        record = InvestigatorCharter(
            allowed_source_classes=list(specialist["allowed_source_classes"]),
            budget=budget.as_charter_string(),
            falsifiable_question=falsifiable,
            gap_id=item.gap_id,
            investigator_charter_id=charter_model_id,
            investigator_type=InvestigatorCharterInvestigator_type(investigator_type),
            stop_rule=STOP_RULE,
            authorizing_role="Research Director",
            created_at=OPENED_AT,
            expected_information_value=InvestigatorCharterExpected_information_value(item.eiv),
            geography="United States",
            independence_check=(
                "Executor must be a separate agent from Structural Red Team, "
                "Independent Research Auditor, Chief Underwriter, and Founder. "
                "Research Director authorized the charter and does not execute it."
            ),
            population_represented=(
                "Public-record population named in the falsifiable question. "
                "Not a surveyed population."
            ),
            sampling_limitations=(
                "Desk research only. Public documents. No interviews, surveys, or site visits."
            ),
            time_window=f"FY2023 through case as-of {AS_OF_DATE}, plus public documents already dated inside that window.",
        )
        registry.store(record)
        charter_payload = record.model_dump(mode="json")
        charter_payload["record_kind"] = "IC-01"
    else:
        charter_payload = {
            "record_kind": "DESK_ASSIGNMENT",
            "schema_id": None,
            "reason": (
                "IC-01.investigator_type has no value for this core desk. "
                "Canonical role is unchanged. This object is not a new schema."
            ),
            "gap_id": item.gap_id,
            "specialist_id": specialist["specialist_id"],
            "canonical_role": specialist["canonical_role"],
            "falsifiable_question": falsifiable,
            "allowed_source_classes": list(specialist["allowed_source_classes"]),
            "budget": budget.as_charter_string(),
            "stop_rule": STOP_RULE,
            "authorizing_role": "Research Director",
            "desk_research_only": True,
            "expected_information_value": item.eiv,
            "geography": "United States",
            "sampling_limitations": (
                "Desk research only. Public documents. No interviews, surveys, or site visits."
            ),
            "time_window": f"FY2023 through case as-of {AS_OF_DATE}.",
        }
    packet = _packet(
        case_id=case_id,
        item=item,
        specialist=specialist,
        charter_id=charter_model_id,
        budget=budget,
        falsifiable=falsifiable,
    )
    return IssuedCharter(
        gap_id=item.gap_id,
        specialist_id=specialist["specialist_id"],
        display_name=specialist["display_name"],
        canonical_role=specialist["canonical_role"],
        investigator_type=investigator_type,
        investigator_charter_id=charter_model_id,
        falsifiable_question=falsifiable,
        question=item.question,
        eiv=item.eiv,
        budget=budget.as_charter_string(),
        why=_why(item, override),
        override=override,
        charter_record=charter_payload,
        task_packet=packet,
    )


def _ranked_public(item: RankedGap) -> dict:
    return {
        "gap_id": item.gap_id,
        "specialist_id": item.specialist_id,
        "eiv": item.eiv,
        "importance": item.importance,
        "resolvability_class": item.resolvability_class,
        "question": item.question,
    }


def route_case(
    bundle,
    *,
    max_n: int = 3,
    founder_priority: dict | None = None,
    charter_budget: Budget | None = None,
    ts_ms: int = ANCHOR_TS_MS,
) -> RouteResult:
    """Select up to ``max_n`` specialists and store their charter records."""
    if max_n < 1:
        raise ValueError("max_n must be at least 1")
    budget = charter_budget or DEFAULT_CHARTER_BUDGET
    assert_within_charter_ceiling(budget)
    if budget.times(max_n).exceeds(CASE_BUDGET_CEILING):
        raise ValueError(
            f"{max_n} charters at {budget} exceed the case ceiling {CASE_BUDGET_CEILING}"
        )
    load_catalog()
    registry = bundle.registry
    case_id = bundle.case_id
    case = registry.load("CASE-01", case_id)
    if case.research_director != "Research Director":
        raise RuntimeError("CaseRecord.research_director is not Research Director")

    ranked = rank_gaps(
        [row for row in registry.list_all("EG-01") if row.case_id == case_id]
    )
    natural = natural_selection(ranked, max_n)
    requested = list((founder_priority or {}).get("priority") or [])
    override_applied = False
    override_reason = ""
    chosen_pairs: list[tuple[RankedGap, bool]] = []
    if requested:
        natural_ids = [item.specialist_id for item in natural]
        if natural_ids != requested:
            override_applied = True
            absent = [
                specialist_id
                for specialist_id in requested
                if all(item.specialist_id != specialist_id for item in ranked)
            ]
            override_reason = (
                "Natural EIV order selected "
                + ", ".join(natural_ids)
                + ". Founder priority differs. "
                + (
                    "No stored gap classifies to: " + ", ".join(absent) + ". "
                    if absent
                    else ""
                )
                + "The override does not change EIV bands. "
                "It replaces the natural third slot where the requested dimension is absent "
                "or ranks below the cutoff."
            )
        used: set[str] = set()
        for specialist_id in requested[:max_n]:
            match = _best_for(ranked, specialist_id, used)
            drafted = False
            if match is None:
                spec = _draft_spec(founder_priority or {}, specialist_id)
                if spec is None:
                    raise KeyError(
                        f"no stored gap for {specialist_id} and no director-drafted question"
                    )
                gap = _draft_gap(registry, case_id, spec, ts_ms)
                ranked = rank_gaps(
                    [row for row in registry.list_all("EG-01") if row.case_id == case_id]
                )
                match = next(item for item in ranked if item.gap_id == gap.gap_id)
                # The draft is explicitly for this specialist even if keywords differ.
                match = RankedGap(
                    gap_id=match.gap_id,
                    specialist_id=specialist_id,
                    eiv=match.eiv,
                    importance=match.importance,
                    resolvability_class=match.resolvability_class,
                    question=match.question,
                    falsifiable_question=match.falsifiable_question,
                    operational_status=match.operational_status,
                )
                drafted = True
            used.add(match.gap_id)
            chosen_pairs.append((match, override_applied or drafted))
    else:
        chosen_pairs = [(item, False) for item in natural]

    hypothesis_ids = ensure_hypotheses(registry, case_id, ts_ms)
    selected: list[IssuedCharter] = []
    for item, flagged in chosen_pairs:
        specialist = get_specialist(item.specialist_id or "")
        selected.append(
            _issue_one(
                registry,
                case_id,
                item,
                specialist,
                budget,
                ts_ms,
                flagged,
            )
        )
    charter_id = ensure_research_charter(
        registry,
        case_id,
        hypothesis_ids,
        [item.falsifiable_question for item in selected],
        ts_ms,
    )
    transition_stage(
        registry,
        case_id,
        "CHARTER",
        "IN_PROGRESS",
        "RC-01 DRAFT stored. Not VALIDATED and not BUDGET_APPROVED, so CHARTER is not COMPLETE.",
        [charter_id, *hypothesis_ids],
    )
    transition_stage(
        registry,
        case_id,
        "SCUTTLEBUTT",
        "IN_PROGRESS",
        "Desk-research charters issued. SCUTTLEBUTT is not COMPLETE: "
        "QAD-MODERN-SCUTTLEBUTT-PROTOCOL.md §1 says scuttlebutt is not desk research.",
        [item.investigator_charter_id or item.gap_id for item in selected],
    )
    return RouteResult(
        case_id=case_id,
        natural=[_ranked_public(item) for item in natural],
        selected=selected,
        override={
            "applied": override_applied,
            "reason": override_reason,
            "requested": requested,
            "founder_approved": False,
            "label": (founder_priority or {}).get("label", ""),
        },
        charter_id=charter_id,
        hypothesis_ids=hypothesis_ids,
    )


def _draft_spec(founder_priority: dict, specialist_id: str) -> dict | None:
    for spec in founder_priority.get("draft_gaps") or []:
        if spec.get("specialist_id") == specialist_id:
            return spec
    return None


def write_artifacts(result: RouteResult, out_dir: Path, registry) -> list[Path]:
    """Write charter records and task packets. No personal data."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def dump(name: str, payload) -> Path:
        path = out_dir / name
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(path)
        return path

    case_id = result.case_id
    hypotheses = [
        registry.load("HYP-01", hypothesis_id).model_dump(mode="json")
        for hypothesis_id in result.hypothesis_ids
    ]
    dump("hypotheses.json", hypotheses)
    dump(
        "research-charter.json",
        registry.load("RC-01", result.charter_id).model_dump(mode="json"),
    )
    hypothesis_sets = [
        row.model_dump(mode="json")
        for row in registry.list_all("HS-01")
        if row.case_id == case_id
    ]
    dump("hypothesis-set.json", hypothesis_sets)
    draft_gaps = [
        row.model_dump(mode="json")
        for row in registry.list_all("EG-01")
        if row.case_id == case_id and str(row.gap_id) not in _original_gap_ids()
    ]
    dump("draft-gaps.json", draft_gaps)
    for item in result.selected:
        dump(f"{item.gap_id}.charter.json", item.charter_record)
        dump(f"{item.gap_id}.task.json", item.task_packet)
    dump(
        "route-manifest.json",
        {
            "case_id": case_id,
            "charter_id": result.charter_id,
            "charter_state": "DRAFT",
            "label": "MANUAL/FOUNDER_DIRECTED pilot",
            "founder_approved": False,
            "natural_selection": result.natural,
            "override": result.override,
            "selected": [
                {
                    "gap_id": item.gap_id,
                    "specialist_id": item.specialist_id,
                    "display_name": item.display_name,
                    "canonical_role": item.canonical_role,
                    "investigator_type": item.investigator_type,
                    "investigator_charter_id": item.investigator_charter_id,
                    "question": item.question,
                    "falsifiable_question": item.falsifiable_question,
                    "eiv": item.eiv,
                    "budget": item.budget,
                    "why": item.why,
                    "override": item.override,
                    "charter_file": f"{item.gap_id}.charter.json",
                    "task_file": f"{item.gap_id}.task.json",
                }
                for item in result.selected
            ],
            "limitations": list(result.limitations),
        },
    )
    return written


def _original_gap_ids() -> set[str]:
    from research.qad_pilot.unh.case_slice import CASE_ID

    seeds = (
        "q3-10q-absent",
        "reserve-bridge",
        "outlook-path-2025",
        "skeptic-cache-gap",
        "scuttlebutt-unopened",
    )
    return {_uid(f"gap:{seed}", ANCHOR_TS_MS) for seed in seeds} | {CASE_ID}


def reload_case_records(bundle, out_dir: Path) -> None:
    """Load routed charter records into a freshly built case bundle."""
    registry = bundle.registry
    for row in json.loads((out_dir / "draft-gaps.json").read_text(encoding="utf-8")):
        if not registry.contains("EG-01", row["gap_id"]):
            registry.store(EvidenceGap(**row))
    for row in json.loads((out_dir / "hypotheses.json").read_text(encoding="utf-8")):
        if not registry.contains("HYP-01", row["hypothesis_id"]):
            registry.store(HypothesisRecord(**row))
    charter = json.loads((out_dir / "research-charter.json").read_text(encoding="utf-8"))
    if not registry.contains("RC-01", charter["charter_id"]):
        registry.store(ResearchCharter(**charter))
    for row in json.loads((out_dir / "hypothesis-set.json").read_text(encoding="utf-8")):
        if not registry.contains("HS-01", row["hypothesis_set_id"]):
            registry.store(HypothesisSet(**row))
    for path in sorted(out_dir.glob("*.charter.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("record_kind") != "IC-01":
            continue
        payload = {key: value for key, value in payload.items() if key != "record_kind"}
        if not registry.contains("IC-01", payload["investigator_charter_id"]):
            registry.store(InvestigatorCharter(**payload))
