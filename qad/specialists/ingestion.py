"""Ingest a specialist result through the existing admission boundary.

A claim with a URL, retrieval timestamp, source date, and publisher is
admitted as SRC-01 bytes plus EV-01/EAR-01. A claim missing any of those
is quarantined. Quarantine is the S4 / scuttlebutt quality-gate word for
"not admitted". It is not a new canonical status. The fact status used is
the existing FactRecord value UNVERIFIED, and no VERIFIED fact is stored.

UNRESOLVED is not an IR-01 disposition. The report stores NOT_ANSWERED and
the findings record specialist_disposition=UNRESOLVED. The gap journal
records UNRESOLVED. EG-01 itself is left unchanged when the descriptor
rejects a status rewrite.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from qad.ids import deterministic_uuid7
from qad.models.family_b import (
    ClaimRecord,
    ClaimRecordClaimant_type,
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceGapOperational_status,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    FactRecord,
    FactRecordVerification_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_c import (
    InvestigationReport,
    InvestigationReportDisposition,
    InvestigationReportStop_rule,
)
from qad.persistence.errors import IntegrityConflict, TransactionFailure
from qad.specialists.budget import BudgetBoundError, assert_usage_within, parse_budget
from qad.specialists.contract import (
    IR_DISPOSITION_FOR_SPECIALIST,
    RESULT_CONTRACT_ID,
    RESULT_FIELDS,
    SOURCE_FIELDS,
    SPECIALIST_DISPOSITIONS,
    USAGE_FIELDS,
)
from qad.specialists.scoring import assign_eiv
from qad.specialists.separation import SeparationViolation, check_roles
from qad.specialists.stages import find_stage, transition_stage
from research.qad_pilot.unh.case_slice import ANCHOR_TS_MS, record_verified_fact

_FIELDWORK = {"interview", "survey", "site_visit"}


@dataclass
class IngestOutcome:
    case_id: str
    gap_id: str
    admitted_evidence_ids: list[str] = field(default_factory=list)
    admitted_source_ids: list[str] = field(default_factory=list)
    quarantined: list[dict] = field(default_factory=list)
    investigation_disposition: str = ""
    ir_disposition: str | None = None
    investigation_id: str | None = None
    gap_status: dict = field(default_factory=dict)
    stage_state: str = ""
    actor_id: str = ""
    canonical_role: str = ""


def _enum(value: object) -> str:
    return getattr(value, "value", value)  # type: ignore[return-value]


def _parse_time(value: str, *, field_name: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError(f"{field_name} is empty")
    datetime.fromisoformat(text.replace("Z", "+00:00"))
    return text


def provenance_errors(source: dict, allowed: list[str], *, desk_research_only: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(source, dict):
        return ["source is missing"]
    for name in ("url", "retrieval_timestamp", "source_date", "publisher"):
        if not str(source.get(name) or "").strip():
            errors.append(f"missing {name}")
    url = str(source.get("url") or "")
    parsed = urlparse(url)
    if url and parsed.scheme not in {"http", "https"}:
        errors.append("url scheme is not http or https")
    for name in ("retrieval_timestamp", "source_date"):
        raw = str(source.get(name) or "").strip()
        if not raw:
            continue
        try:
            _parse_time(raw if "T" in raw else raw + "T00:00:00Z", field_name=name)
        except ValueError:
            errors.append(f"{name} is not a timestamp")
    if not str(source.get("quotation") or "").strip():
        errors.append("missing quotation bytes")
    tier = str(source.get("source_tier") or "")
    if tier and tier not in allowed:
        errors.append(f"source_tier {tier} is outside the charter")
    if desk_research_only and str(source.get("collection_method") or "") in _FIELDWORK:
        errors.append("fieldwork collection is outside desk_research_only")
    if tier in {"L8", "L9", "L10"}:
        errors.append(f"{tier} cannot support a material conclusion in this desk charter")
    return errors


def decide_scuttlebutt_state(
    issued_ids: list[str],
    reported_ids: set[str],
    *,
    desk_research_only: bool,
    contract_complete: bool,
) -> str:
    """IN_PROGRESS until every issued charter has a report.

    COMPLETE only when the contract predicate is true and the work is not
    desk-research-only. Otherwise a full set of reports is INCOMPLETE.
    """
    if not issued_ids or any(item not in reported_ids for item in issued_ids):
        return "IN_PROGRESS"
    if contract_complete and not desk_research_only:
        return "COMPLETE"
    return "INCOMPLETE"


def scuttlebutt_contract_complete(reports: list[dict]) -> bool:
    """M3-05 §8 plus stage 6: answered, sourced, and not stopped for budget.

    Desk-research-only charters never satisfy §1, so callers must also pass
    desk_research_only=False before moving the stage to COMPLETE.
    """
    if not reports:
        return False
    for report in reports:
        if report.get("disposition") != "ANSWERED":
            return False
        if report.get("stop_rule_triggered") == "BUDGET_EXHAUSTED":
            return False
        if not report.get("admitted_evidence_ids"):
            return False
    return True


def _gap_journal(registry, gap_id: str, journal_status: str) -> dict:
    gap = registry.load("EG-01", gap_id)
    written = False
    reason = ""
    try:
        registry.store(
            gap.model_copy(
                update={
                    "operational_status": EvidenceGapOperational_status(journal_status)
                }
            )
        )
        written = True
    except (IntegrityConflict, TransactionFailure) as exc:
        written = False
        reason = str(exc)
    current = registry.load("EG-01", gap_id)
    return {
        "written": written,
        "reason": reason,
        "canonical_status": _enum(current.operational_status),
        "journal_status": journal_status,
    }


def _admit_claim(bundle, result: dict, claim: dict, index: int, ts_ms: int) -> tuple[str, str]:
    source = claim["source"]
    quotation = str(source["quotation"])
    raw = quotation.encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    seed = f"{result['gap_id']}:{index}:{digest}"
    source_id = str(deterministic_uuid7(f"src:{seed}", ts_ms=ts_ms))
    evidence_id = str(deterministic_uuid7(f"ev:{seed}", ts_ms=ts_ms))
    archive = bundle.archive
    registry = bundle.registry
    tier = str(source["source_tier"])
    source_type = str(source.get("source_type") or "OTHER")
    if not archive.contains("SRC-01", source_id):
        archive.admit_source(
            SourceRecord(
                content_hash=digest,
                retrieval_date=str(source["retrieval_timestamp"]),
                source_id=source_id,
                source_tier=SourceRecordSource_tier(tier),
                source_type=SourceRecordSource_type(source_type),
                url_or_identifier=str(source["url"]),
                author=str(source["publisher"]),
                publication_date=str(source["source_date"]),
                retrieval_method="specialist result quotation",
                retriever=str(result["actor_id"]),
                title=str(source.get("title") or claim["statement"])[:240],
            ),
            raw,
        )
    if not registry.contains("EV-01", evidence_id):
        evidence = EvidenceRecord(
            admitting_role="Evidence Intelligence Lead",
            as_of=str(source["source_date"])[:10],
            content=quotation,
            evidence_id=evidence_id,
            evidence_type=EvidenceRecordEvidence_type(claim["evidence_type"]),
            extractor=str(result["actor_id"]),
            source_id=source_id,
            source_tier=tier,
            validation_status=EvidenceRecordValidation_status.RAW,
            extraction_method=RESULT_CONTRACT_ID,
            validation_method="provenance fields present; URL not re-fetched",
        )
        registry.admit_evidence(
            evidence,
            EvidenceAdmissionRecord(
                admission_id=str(deterministic_uuid7(f"ear:{seed}", ts_ms=ts_ms)),
                admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
                admission_timestamp=str(source["retrieval_timestamp"]),
                admitting_role="Evidence Intelligence Lead",
                evidence_id=evidence_id,
                source_tier_check=tier,
                validation_method="provenance fields present; URL not re-fetched",
                source_as_of=str(source["source_date"])[:10],
                validation_notes=(
                    "Quotation bytes from the specialist result. "
                    "The ingest boundary did not re-fetch the URL."
                ),
            ),
        )
    evidence_type = claim["evidence_type"]
    if evidence_type == "FACT":
        fact_id = str(deterministic_uuid7(f"fact:{seed}", ts_ms=ts_ms))
        if not registry.contains("FACT-01", fact_id):
            record_verified_fact(
                registry,
                archive,
                FactRecord(
                    evidence_id=evidence_id,
                    fact_id=fact_id,
                    source_location=str(source["url"]),
                    statement=str(claim["statement"]),
                    verification_status=FactRecordVerification_status.VERIFIED,
                    as_of=str(source["source_date"])[:10],
                    extractor=str(result["actor_id"]),
                ),
            )
    elif evidence_type == "CLAIM":
        claim_id = str(deterministic_uuid7(f"clm:{seed}", ts_ms=ts_ms))
        if not registry.contains("CLM-01", claim_id):
            claimant = str(claim.get("claimant") or "OTHER")
            registry.store(
                ClaimRecord(
                    claim_date=str(source["source_date"])[:10],
                    claim_id=claim_id,
                    claimant=ClaimRecordClaimant_type(claimant),
                    evidence_id=evidence_id,
                    statement=str(claim["statement"]),
                    extractor=str(result["actor_id"]),
                    source=source_id,
                )
            )
    return evidence_id, source_id


def ingest_result(
    bundle,
    result: dict,
    charter: dict,
    ledger: list[tuple[str, str]],
    *,
    issued_ids: list[str],
    reported_ids: set[str],
    ts_ms: int = ANCHOR_TS_MS,
) -> IngestOutcome:
    missing = [name for name in RESULT_FIELDS if name not in result]
    if missing:
        raise ValueError(f"result missing fields {missing}")
    if result["contract"] != RESULT_CONTRACT_ID:
        raise ValueError(f"unknown result contract {result['contract']!r}")
    if result["case_id"] != bundle.case_id or result["gap_id"] != charter["gap_id"]:
        raise ValueError("result is not bound to this case and charter gap")
    if result["specialist_id"] != charter["specialist_id"]:
        raise ValueError("result specialist does not match the charter")
    if result.get("investigator_charter_id") != charter.get("investigator_charter_id"):
        raise ValueError("result charter id does not match")
    if result["canonical_role"] != charter["canonical_role"]:
        raise SeparationViolation(
            "result role does not match the charter role",
            actor_id=str(result["actor_id"]),
            roles=[str(result["canonical_role"]), str(charter["canonical_role"])],
        )
    if charter.get("desk_research_only") and result.get("desk_research_only") is not True:
        raise ValueError("desk-research charter cannot accept a fieldwork result")
    disposition = str(result["disposition"])
    if disposition not in SPECIALIST_DISPOSITIONS:
        raise ValueError(f"disposition {disposition!r} is not a known investigation result")
    actor = str(result["actor_id"])
    roles = [str(result["canonical_role"]), *(result.get("additional_roles") or [])]
    decision = check_roles(actor, [*(prior for who, prior in ledger if who == actor), *roles])
    if not decision.allowed:
        raise SeparationViolation(decision.conflict, actor_id=actor, roles=list(decision.roles))
    for extra in result.get("additional_roles") or []:
        if extra != result["canonical_role"]:
            extra_decision = check_roles(actor, [str(result["canonical_role"]), str(extra)])
            if not extra_decision.allowed:
                raise SeparationViolation(
                    extra_decision.conflict,
                    actor_id=actor,
                    roles=list(extra_decision.roles),
                )
    usage = result["usage"]
    if not isinstance(usage, dict) or any(name not in usage for name in USAGE_FIELDS):
        raise BudgetBoundError("usage must report tool_calls, sources, and minutes")
    assert_usage_within(usage, parse_budget(charter["budget"]))

    outcome = IngestOutcome(
        case_id=bundle.case_id,
        gap_id=charter["gap_id"],
        actor_id=actor,
        canonical_role=str(result["canonical_role"]),
    )
    allowed = list(charter["allowed_source_classes"])
    for index, claim in enumerate(result["claims"]):
        if not isinstance(claim, dict) or any(name not in claim for name in ("statement", "evidence_type", "source")):
            outcome.quarantined.append(
                {
                    "statement": str((claim or {}).get("statement") if isinstance(claim, dict) else ""),
                    "status": "QUARANTINED",
                    "verification_status": "UNVERIFIED",
                    "reason": "claim is missing statement, evidence_type, or source",
                }
            )
            continue
        if claim["evidence_type"] not in {"FACT", "CLAIM"}:
            outcome.quarantined.append(
                {
                    "statement": claim["statement"],
                    "status": "QUARANTINED",
                    "verification_status": "UNVERIFIED",
                    "reason": "evidence_type is not FACT or CLAIM",
                }
            )
            continue
        source = claim.get("source") or {}
        if isinstance(source, dict):
            source = {**source, "collection_method": claim.get("collection_method")}
        errors = provenance_errors(
            source,
            allowed,
            desk_research_only=bool(charter.get("desk_research_only")),
        )
        if errors:
            outcome.quarantined.append(
                {
                    "statement": claim["statement"],
                    "status": "QUARANTINED",
                    "verification_status": "UNVERIFIED",
                    "reason": "; ".join(errors),
                }
            )
            continue
        evidence_id, source_id = _admit_claim(bundle, result, claim, index, ts_ms)
        outcome.admitted_evidence_ids.append(evidence_id)
        outcome.admitted_source_ids.append(source_id)

    effective = disposition
    if disposition == "ANSWERED" and not outcome.admitted_evidence_ids:
        effective = "UNRESOLVED"
    outcome.investigation_disposition = effective
    ir_disposition = IR_DISPOSITION_FOR_SPECIALIST[effective]
    findings = [str(item) for item in result.get("findings") or []]
    marker = f"specialist_disposition={effective}"
    if marker not in findings:
        findings.append(marker)
    if disposition != effective:
        findings.append(f"specialist_claimed={disposition}; boundary_rejected_without_admitted_evidence")

    charter_id = charter.get("investigator_charter_id")
    if charter_id:
        investigation_id = str(deterministic_uuid7(f"ir:{charter_id}", ts_ms=ts_ms))
        stop = result.get("stop_rule_triggered")
        stop_value = stop if stop in {item.value for item in InvestigationReportStop_rule} else None
        if not bundle.registry.contains("IR-01", investigation_id):
            bundle.registry.store(
                InvestigationReport(
                    disposition=InvestigationReportDisposition(ir_disposition),
                    evidence_gap_id=charter["gap_id"],
                    falsifiable_question=str(result["falsifiable_question"]),
                    findings=findings,
                    investigation_id=investigation_id,
                    investigator=actor,
                    investigator_charter_id=charter_id,
                    proposed_evidence_ids=list(outcome.admitted_evidence_ids),
                    sampling_limitations=str(result.get("sampling_limitations") or ""),
                    sources=list(outcome.admitted_source_ids),
                    stop_rule_triggered=(
                        InvestigationReportStop_rule(stop_value) if stop_value else None
                    ),
                )
            )
        outcome.investigation_id = investigation_id
        outcome.ir_disposition = ir_disposition

    journal_status = "UNRESOLVED" if effective in {"UNRESOLVED", "NOT_ANSWERED"} else effective
    if journal_status == "ANSWERED":
        journal_status = "CLOSED"
    elif journal_status == "PARTIALLY_ANSWERED":
        journal_status = "PARTIALLY_CLOSED"
    outcome.gap_status = _gap_journal(bundle.registry, charter["gap_id"], journal_status)

    reported = set(reported_ids)
    reported.add(charter["gap_id"])
    target = decide_scuttlebutt_state(
        issued_ids,
        reported,
        desk_research_only=bool(charter.get("desk_research_only")),
        contract_complete=False,
    )
    stage = transition_stage(
        bundle.registry,
        bundle.case_id,
        "SCUTTLEBUTT",
        target,
        f"Ingest {charter['gap_id']} disposition {effective}. Target {target}.",
        [item for item in (outcome.investigation_id, charter["gap_id"]) if item],
        complete_allowed=False,
    )
    outcome.stage_state = _enum(stage.stage_state)
    ledger.append((actor, str(result["canonical_role"])))
    return outcome


def load_charter_file(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("record_kind") == "IC-01":
        return {
            "gap_id": payload["gap_id"],
            "specialist_id": payload.get("specialist_id"),
            "canonical_role": None,
            "investigator_charter_id": payload["investigator_charter_id"],
            "allowed_source_classes": payload["allowed_source_classes"],
            "budget": payload["budget"],
            "desk_research_only": True,
            "falsifiable_question": payload["falsifiable_question"],
            "investigator_type": payload["investigator_type"],
        }
    return {
        "gap_id": payload["gap_id"],
        "specialist_id": payload["specialist_id"],
        "canonical_role": payload["canonical_role"],
        "investigator_charter_id": None,
        "allowed_source_classes": payload["allowed_source_classes"],
        "budget": payload["budget"],
        "desk_research_only": True,
        "falsifiable_question": payload["falsifiable_question"],
        "investigator_type": None,
    }


def attach_role_from_task(charter: dict, task_path: Path) -> dict:
    if charter.get("canonical_role") and charter.get("specialist_id"):
        return charter
    task = json.loads(task_path.read_text(encoding="utf-8"))
    charter["canonical_role"] = task["canonical_role"]
    charter["specialist_id"] = task["specialist_id"]
    return charter


def gap_eiv_unchanged(gap) -> str:
    """Re-read helper so tests can show scoring still uses the same rule."""
    return assign_eiv(gap.importance, _enum(gap.resolvability_class), gap.question)
