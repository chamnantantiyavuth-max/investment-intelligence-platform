"""Ingest a specialist result through the existing admission boundary.

A claim with a URL, retrieval timestamp, source date, and publisher may be
admitted only when its cited passage occurs in original bytes the ingest
step itself loaded: a snapshot file, an explicit snapshot mapping, or a
hash-checked raw blob already in the archive for that URL. The specialist
quotation and any hash of that quotation are not those bytes.

A passage that is not found is quarantined. Quarantine is the S4 /
scuttlebutt quality-gate word for "not admitted". It is not a new canonical
status. The fact status used on that path is the existing FactRecord value
UNVERIFIED. FACT-01 VERIFIED is stored only after the passage check passes.

UNRESOLVED is not an IR-01 disposition. The report stores NOT_ANSWERED and
the findings record specialist_disposition=UNRESOLVED. The gap journal
records UNRESOLVED. EG-01 itself is left unchanged when the descriptor
rejects a status rewrite.
"""

from __future__ import annotations

import hashlib
import json
import os
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
from qad.m6.source_bridge import (
    PASSAGE_ABSENT_REASON,
    passage_occurs_in_independent_bytes,
)
from qad.persistence.errors import IntegrityConflict, TransactionFailure
from qad.persistence.serialization import compute_canonical_hash
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
    preserved: list[dict] = field(default_factory=list)
    verified_fact_ids: list[str] = field(default_factory=list)
    investigation_disposition: str = ""
    ir_disposition: str | None = None
    investigation_id: str | None = None
    gap_status: dict = field(default_factory=dict)
    stage_state: str = ""
    actor_id: str = ""
    canonical_role: str = ""


def case_directory(case_id: str) -> Path:
    """Directory of committed case files. ``QAD_CASE_ROOT`` overrides the repo path."""
    override = os.environ.get("QAD_CASE_ROOT")
    base = Path(override) if override else Path("research/qad-cases")
    return base / case_id


def load_url_snapshots(snapshot_dir: Path | None) -> dict[str, bytes]:
    """Load snapshot bytes the ingest step reads from disk. No network."""
    if snapshot_dir is None or not snapshot_dir.is_dir():
        return {}
    loaded: dict[str, bytes] = {}
    manifest = snapshot_dir / "manifest.json"
    if manifest.is_file():
        mapping = json.loads(manifest.read_text(encoding="utf-8"))
        for url, name in (mapping.get("urls") or {}).items():
            path = snapshot_dir / str(name)
            if path.is_file():
                loaded[str(url)] = path.read_bytes()
    for path in sorted(snapshot_dir.glob("*.bin")):
        url_file = path.with_suffix(".url")
        if url_file.is_file():
            url = url_file.read_text(encoding="utf-8").strip()
            loaded.setdefault(url, path.read_bytes())
    return loaded


def _archive_bytes_for_url(archive, url: str) -> bytes | None:
    """Hash-checked raw blob already stored for this URL. Not the specialist quote."""
    try:
        rows = archive.list_all("SRC-01")
    except Exception:
        return None
    for row in rows:
        if getattr(row, "url_or_identifier", None) != url:
            continue
        source_id = row.source_id
        try:
            raw = archive.load_raw_blob(source_id)
            stored_hash = archive.get_raw_blob_hash(source_id)
        except Exception:
            continue
        digest = hashlib.sha256(raw).hexdigest()
        if stored_hash != digest or getattr(row, "content_hash", None) != digest:
            continue
        return raw
    return None


def resolve_independent_bytes(
    url: str,
    *,
    archive,
    independent_snapshots: dict[str, bytes] | None,
    snapshot_dir: Path | None,
) -> bytes | None:
    """Bytes the ingest step loaded. The claim's quotation is not consulted."""
    if independent_snapshots and url in independent_snapshots:
        raw = independent_snapshots[url]
        if isinstance(raw, bytes) and raw:
            return raw
    loaded = load_url_snapshots(snapshot_dir).get(url)
    if loaded:
        return loaded
    return _archive_bytes_for_url(archive, url)


def _store_preserving(registry, schema_id: str, record_id: str, record) -> str:
    """Store once. An existing different record is left as it is."""
    if registry.contains(schema_id, record_id):
        existing = registry.load(schema_id, record_id)
        if compute_canonical_hash(existing) == compute_canonical_hash(record):
            return "idempotent"
        return "preserved"
    registry.store(record)
    return "stored"


def _admit_evidence_preserving(registry, evidence, admission) -> str:
    if registry.contains("EV-01", evidence.evidence_id):
        existing = registry.load("EV-01", evidence.evidence_id)
        if compute_canonical_hash(existing) == compute_canonical_hash(evidence):
            return "idempotent"
        return "preserved"
    registry.admit_evidence(evidence, admission)
    return "stored"


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


def _admit_claim(
    bundle,
    result: dict,
    claim: dict,
    index: int,
    ts_ms: int,
    *,
    independent_snapshots: dict[str, bytes] | None,
    snapshot_dir: Path | None,
) -> dict:
    """Admit one claim, or return a quarantine/preserved reason.

    The specialist ``quotation`` is the passage to find. It is never archived
    as the original document and its hash is never the verification proof.
    """
    source = claim["source"]
    quotation = str(source["quotation"])
    url = str(source["url"])
    independent = resolve_independent_bytes(
        url,
        archive=bundle.archive,
        independent_snapshots=independent_snapshots,
        snapshot_dir=snapshot_dir,
    )
    if not passage_occurs_in_independent_bytes(quotation, independent):
        return {
            "status": "QUARANTINED",
            "verification_status": "UNVERIFIED",
            "reason": PASSAGE_ABSENT_REASON,
        }
    assert independent is not None
    digest = hashlib.sha256(independent).hexdigest()
    passage_digest = hashlib.sha256(quotation.encode("utf-8")).hexdigest()
    seed = f"{result['gap_id']}:{index}:{digest}:{passage_digest}"
    source_id = str(deterministic_uuid7(f"independent-src:{url}:{digest}", ts_ms=ts_ms))
    evidence_id = str(deterministic_uuid7(f"ev:{seed}", ts_ms=ts_ms))
    archive = bundle.archive
    registry = bundle.registry
    tier = str(source["source_tier"])
    source_type = str(source.get("source_type") or "OTHER")
    matched = _archive_bytes_for_url(archive, url)
    if matched is not None and matched == independent:
        for row in archive.list_all("SRC-01"):
            if row.url_or_identifier == url and hashlib.sha256(matched).hexdigest() == row.content_hash:
                source_id = row.source_id
                break
    if archive.contains("SRC-01", source_id):
        stored = archive.load_raw_blob(source_id)
        if hashlib.sha256(stored).hexdigest() != digest:
            return {
                "status": "QUARANTINED",
                "verification_status": "UNVERIFIED",
                "reason": (
                    "stored source bytes differ from the independent snapshot; "
                    "not overwritten"
                ),
            }
    else:
        archive.admit_source(
            SourceRecord(
                content_hash=digest,
                retrieval_date=str(source["retrieval_timestamp"]),
                source_id=source_id,
                source_tier=SourceRecordSource_tier(tier),
                source_type=SourceRecordSource_type(source_type),
                url_or_identifier=url,
                author=str(source["publisher"]),
                publication_date=str(source["source_date"]),
                retrieval_method="independent snapshot loaded by ingest",
                retriever="qad.specialists.ingest",
                title=str(source.get("title") or claim["statement"])[:240],
            ),
            independent,
        )
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
        validation_method="cited passage found in independently loaded original source bytes",
    )
    admission = EvidenceAdmissionRecord(
        admission_id=str(deterministic_uuid7(f"ear:{seed}", ts_ms=ts_ms)),
        admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
        admission_timestamp=str(source["retrieval_timestamp"]),
        admitting_role="Evidence Intelligence Lead",
        evidence_id=evidence_id,
        source_tier_check=tier,
        validation_method="cited passage found in independently loaded original source bytes",
        source_as_of=str(source["source_date"])[:10],
        validation_notes=(
            "Passage located in original bytes loaded by the ingest step. "
            "The specialist quotation hash was not the source hash."
        ),
    )
    evidence_state = _admit_evidence_preserving(registry, evidence, admission)
    if evidence_state == "preserved":
        return {
            "status": "PRESERVED",
            "evidence_id": evidence_id,
            "reason": "existing canonical evidence differs; not overwritten",
        }
    verified_fact_id = None
    evidence_type = claim["evidence_type"]
    if evidence_type == "FACT":
        fact_id = str(deterministic_uuid7(f"fact:{seed}", ts_ms=ts_ms))
        fact = FactRecord(
            evidence_id=evidence_id,
            fact_id=fact_id,
            source_location=url,
            statement=str(claim["statement"]),
            verification_status=FactRecordVerification_status.VERIFIED,
            as_of=str(source["source_date"])[:10],
            extractor=str(result["actor_id"]),
        )
        fact_state = "stored"
        if registry.contains("FACT-01", fact_id):
            existing = registry.load("FACT-01", fact_id)
            if compute_canonical_hash(existing) == compute_canonical_hash(fact):
                fact_state = "idempotent"
            else:
                fact_state = "preserved"
        else:
            record_verified_fact(registry, archive, fact)
        if fact_state == "preserved":
            return {
                "status": "PRESERVED",
                "evidence_id": evidence_id,
                "source_id": source_id,
                "reason": "existing FACT-01 differs; adverse record was not overwritten",
            }
        verified_fact_id = fact_id
    elif evidence_type == "CLAIM":
        claim_id = str(deterministic_uuid7(f"clm:{seed}", ts_ms=ts_ms))
        claimant = str(claim.get("claimant") or "OTHER")
        claim_state = _store_preserving(
            registry,
            "CLM-01",
            claim_id,
            ClaimRecord(
                claim_date=str(source["source_date"])[:10],
                claim_id=claim_id,
                claimant=ClaimRecordClaimant_type(claimant),
                evidence_id=evidence_id,
                statement=str(claim["statement"]),
                extractor=str(result["actor_id"]),
                source=source_id,
            ),
        )
        if claim_state == "preserved":
            return {
                "status": "PRESERVED",
                "evidence_id": evidence_id,
                "source_id": source_id,
                "reason": "existing CLM-01 differs; not overwritten",
            }
    return {
        "status": "ADMITTED",
        "evidence_id": evidence_id,
        "source_id": source_id,
        "verified_fact_id": verified_fact_id,
    }


def ingest_result(
    bundle,
    result: dict,
    charter: dict,
    ledger: list[tuple[str, str]],
    *,
    issued_ids: list[str],
    reported_ids: set[str],
    ts_ms: int = ANCHOR_TS_MS,
    independent_snapshots: dict[str, bytes] | None = None,
    snapshot_dir: Path | None = None,
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
    if snapshot_dir is None:
        candidate = case_directory(bundle.case_id) / "snapshots"
        snapshot_dir = candidate if candidate.is_dir() else None
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
        decision = _admit_claim(
            bundle,
            result,
            claim,
            index,
            ts_ms,
            independent_snapshots=independent_snapshots,
            snapshot_dir=snapshot_dir,
        )
        if decision["status"] == "QUARANTINED":
            outcome.quarantined.append(
                {
                    "statement": claim["statement"],
                    "status": "QUARANTINED",
                    "verification_status": "UNVERIFIED",
                    "reason": decision["reason"],
                }
            )
            continue
        if decision["status"] == "PRESERVED":
            outcome.preserved.append(
                {
                    "statement": claim["statement"],
                    "evidence_id": decision.get("evidence_id"),
                    "reason": decision["reason"],
                }
            )
            continue
        outcome.admitted_evidence_ids.append(decision["evidence_id"])
        outcome.admitted_source_ids.append(decision["source_id"])
        if decision.get("verified_fact_id"):
            outcome.verified_fact_ids.append(decision["verified_fact_id"])

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


def replay_committed_ingests(bundle, *, case_dir: Path | None = None) -> list[IngestOutcome]:
    """Replay committed ingest journals into a freshly built case.

    The journal names the gap. The result file is re-admitted under the
    current trust rule. Record identity comes from ``deterministic_uuid7``.
    An existing different canonical record is left in place.
    """
    from qad.specialists.routing import reload_case_records
    from qad.specialists.stages import find_stage, transition_stage

    case_dir = case_dir or case_directory(bundle.case_id)
    journal_dir = case_dir / "ingest"
    charter_dir = case_dir / "charters"
    outcomes: list[IngestOutcome] = []
    if not journal_dir.is_dir() or not charter_dir.is_dir():
        bundle.ingest_replay = _recovery_payload(bundle, outcomes)
        return outcomes
    journal_ids = {path.stem for path in journal_dir.glob("*.json")}
    if not journal_ids:
        bundle.ingest_replay = _recovery_payload(bundle, outcomes)
        return outcomes
    order: list[str] = []
    manifest_path = charter_dir / "route-manifest.json"
    manifest = {}
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        order = [row["gap_id"] for row in manifest.get("selected") or []]
    ordered = [gap_id for gap_id in order if gap_id in journal_ids]
    ordered.extend(sorted(gap_id for gap_id in journal_ids if gap_id not in ordered))
    reload_case_records(bundle, charter_dir)
    stage = find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT")
    if _enum(stage.stage_state) == "NOT_STARTED":
        transition_stage(
            bundle.registry,
            bundle.case_id,
            "SCUTTLEBUTT",
            "IN_PROGRESS",
            "Result ingest reopened SCUTTLEBUTT on a rebuilt case.",
            [],
        )
    issued = [row["gap_id"] for row in manifest.get("selected") or []] or list(ordered)
    reported: set[str] = set()
    ledger: list[tuple[str, str]] = []
    snapshot_dir = case_dir / "snapshots"
    for gap_id in ordered:
        payload = json.loads((case_dir / "results" / f"{gap_id}.json").read_text(encoding="utf-8"))
        charter = attach_role_from_task(
            load_charter_file(charter_dir / f"{gap_id}.charter.json"),
            charter_dir / f"{gap_id}.task.json",
        )
        outcome = ingest_result(
            bundle,
            payload,
            charter,
            ledger,
            issued_ids=issued,
            reported_ids=reported,
            snapshot_dir=snapshot_dir if snapshot_dir.is_dir() else None,
        )
        reported.add(outcome.gap_id)
        outcomes.append(outcome)
    bundle.ingest_replay = _recovery_payload(bundle, outcomes)
    return outcomes


def _recovery_payload(bundle, outcomes: list[IngestOutcome]) -> dict:
    from qad.specialists.stages import find_stage

    accepted: list[dict] = []
    quarantined: list[dict] = []
    preserved: list[dict] = []
    investigations: list[dict] = []
    for outcome in outcomes:
        quarantined.extend(outcome.quarantined)
        preserved.extend(outcome.preserved)
        for evidence_id, source_id in zip(
            outcome.admitted_evidence_ids, outcome.admitted_source_ids
        ):
            evidence = bundle.registry.load("EV-01", evidence_id)
            source = bundle.archive.load("SRC-01", source_id)
            facts = [
                row
                for row in bundle.registry.list_all("FACT-01")
                if row.evidence_id == evidence_id
            ]
            claims = [
                row
                for row in bundle.registry.list_all("CLM-01")
                if row.evidence_id == evidence_id
            ]
            verification = None
            statement = evidence.content
            if facts:
                verification = _enum(facts[0].verification_status)
                statement = facts[0].statement
            elif claims:
                statement = claims[0].statement
            accepted.append(
                {
                    "gap_id": outcome.gap_id,
                    "evidence_id": evidence_id,
                    "source_id": source_id,
                    "evidence_type": _enum(evidence.evidence_type),
                    "validation_status": _enum(evidence.validation_status),
                    "statement": statement,
                    "verification_status": verification,
                    "source_url": source.url_or_identifier,
                    "content_hash": source.content_hash,
                }
            )
        if outcome.investigation_id and bundle.registry.contains("IR-01", outcome.investigation_id):
            report = bundle.registry.load("IR-01", outcome.investigation_id)
            investigations.append(
                {
                    "investigation_id": report.investigation_id,
                    "gap_id": outcome.gap_id,
                    "evidence_gap_id": report.evidence_gap_id,
                    "disposition": _enum(report.disposition),
                }
            )
    try:
        stage_state = _enum(find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT").stage_state)
    except KeyError:
        stage_state = ""
    return {
        "accepted_evidence": accepted,
        "quarantined": quarantined,
        "preserved": preserved,
        "investigations": investigations,
        "scuttlebutt_stage_state": stage_state,
        "verified_fact_count": sum(
            1 for row in accepted if row["verification_status"] == "VERIFIED"
        ),
    }
