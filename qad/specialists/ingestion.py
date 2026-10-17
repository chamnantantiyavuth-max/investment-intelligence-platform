"""Ingest a specialist result through the existing admission boundary.

A claim with a URL, retrieval timestamp, source date, and publisher may reach
FACT-01 VERIFIED only when two separate checks both pass.

1. The cited passage occurs in bytes already bound to an S5/M6 original-source
   verification receipt, or to a trusted archived source identity: source id,
   sha256 of the stored bytes, retrieval/observation time, and a retriever
   that is not the submitting specialist and not this ingest loader. A local
   snapshot (``.bin`` + ``.url``, ``manifest.json``, or an explicit mapping)
   is not that receipt.
2. For a FACT, the statement's numeric values and core proposition are
   contained in that passage. A paraphrase that does not match stays
   UNVERIFIED unless an Evidence Lead sign-off is already recorded on RC-01.

Quarantine is the S4 / scuttlebutt quality-gate word for "not admitted". It
is not a new canonical status. The fact status used on that path is the
existing FactRecord value UNVERIFIED.

UNRESOLVED is not an IR-01 disposition. The report stores NOT_ANSWERED and
the findings record specialist_disposition=UNRESOLVED. The gap journal
records UNRESOLVED. EG-01 itself is left unchanged when the descriptor
rejects a status rewrite.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
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
    OriginalSourceVerification,
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
_INGEST_LOADER = "qad.specialists.ingest"
_M6_RETRIEVER = "qad.m6.source_bridge"
_SIGNED_CHARTER_STATES = frozenset(
    {"VALIDATED", "BUDGET_APPROVED", "ACTIVE", "COMPLETED"}
)
_STOPWORDS = frozenset(
    """
    a an the of and or to in on for with by from that this these those is are
    was were be been being as at it its than then into over per
    """.split()
)
_NUMBER_RE = re.compile(
    r"(?<![\d.])(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(\s*(?:%|percent|pct\.?))?",
    re.IGNORECASE,
)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")

UNTRUSTED_SNAPSHOT_REASON = (
    "local snapshot is not bound to an S5/M6 original-source verification receipt "
    "or a trusted archived source identity"
)
STATEMENT_UNSUPPORTED_REASON = (
    "FACT statement numeric values or core proposition were not found in the cited "
    "passage; no Evidence Lead sign-off is recorded"
)


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


def _numeric_marks(text: str) -> list[tuple[Decimal, bool]]:
    marks: list[tuple[Decimal, bool]] = []
    for match in _NUMBER_RE.finditer(text or ""):
        whole = match.group(1).replace(",", "")
        frac = match.group(2)
        token = f"{whole}.{frac}" if frac is not None else whole
        try:
            value = Decimal(token)
        except InvalidOperation:
            continue
        marks.append((value, bool(match.group(3))))
    return marks


def _proposition_words(text: str) -> list[str]:
    return [
        word.lower()
        for word in _WORD_RE.findall(text or "")
        if len(word) >= 3 and word.lower() not in _STOPWORDS
    ]


def statement_supported_by_passage(statement: str, passage: str) -> bool:
    """True when the statement's numbers and core words occur in the passage.

    ``24.8`` does not match ``2.48``. Percent and bare numbers are different
    marks. This is not a paraphrase judgment.
    """
    statement_numbers = _numeric_marks(statement)
    remaining = _numeric_marks(passage)
    for mark in statement_numbers:
        if mark not in remaining:
            return False
        remaining.remove(mark)
    words = _proposition_words(statement)
    if not statement_numbers and not words:
        return False
    passage_words = set(_proposition_words(passage))
    return all(word in passage_words for word in words)


def _blocked_retrievers(*identities: str) -> set[str]:
    blocked = {_INGEST_LOADER}
    for item in identities:
        text = str(item or "").strip()
        if text:
            blocked.add(text)
    return blocked


def _hash_checked_blob(archive, source_id: str) -> bytes | None:
    try:
        if not archive.verify_admission_attestation(source_id):
            return None
        raw = archive.load_raw_blob(source_id)
        stored_hash = archive.get_raw_blob_hash(source_id)
        row = archive.load("SRC-01", source_id)
    except Exception:
        return None
    if not isinstance(raw, bytes) or not raw:
        return None
    digest = hashlib.sha256(raw).hexdigest()
    if stored_hash != digest or getattr(row, "content_hash", None) != digest:
        return None
    return raw


def _trusted_archived_source(archive, url: str, quotation: str, blocked: set[str]):
    """Existing SRC-01 whose identity is independent of the submitting specialist."""
    try:
        rows = list(archive.list_all("SRC-01"))
    except Exception:
        return None
    fallback = None
    for row in rows:
        if getattr(row, "url_or_identifier", None) != url:
            continue
        source_id = str(getattr(row, "source_id", "") or "").strip()
        retriever = str(getattr(row, "retriever", "") or "").strip()
        observed = str(getattr(row, "retrieval_date", "") or "").strip()
        if not source_id or not retriever or not observed or retriever in blocked:
            continue
        raw = _hash_checked_blob(archive, source_id)
        if raw is None:
            continue
        if passage_occurs_in_independent_bytes(quotation, raw):
            return row, raw
        if fallback is None:
            fallback = (row, raw)
    return fallback


def _matching_receipt(verifications, url: str, quotation: str):
    """Minted M6 receipt whose bytes contain the passage and name this URL."""
    for verification in verifications or ():
        if not isinstance(verification, OriginalSourceVerification):
            continue
        if not verification.is_verified_verdict_for(source_id=verification.source_id or ""):
            continue
        location = str(verification.location or "").strip()
        observed = str(verification.retrieval_date or "").strip()
        raw = verification.raw_bytes
        if location != url or not verification.source_id or not observed:
            continue
        if not isinstance(raw, bytes) or not raw or not verification.content_hash:
            continue
        if hashlib.sha256(raw).hexdigest() != verification.content_hash:
            continue
        if passage_occurs_in_independent_bytes(quotation, raw):
            return verification
    return None


def _local_snapshot_bytes(
    url: str,
    *,
    independent_snapshots: dict[str, bytes] | None,
    snapshot_dir: Path | None,
) -> bytes | None:
    if independent_snapshots and url in independent_snapshots:
        raw = independent_snapshots[url]
        if isinstance(raw, bytes) and raw:
            return raw
    loaded = load_url_snapshots(snapshot_dir).get(url)
    if loaded:
        return loaded
    return None


def evidence_lead_signoff_recorded(registry, specialist_actor: str) -> bool:
    """True only for an RC-01 Evidence Lead sign-off already in the registry.

    A specialist result cannot record this. DRAFT and NOT_VALIDATED charters
    do not count.
    """
    try:
        rows = list(registry.list_all("RC-01"))
    except Exception:
        return False
    actor = str(specialist_actor or "").strip()
    for row in rows:
        lead = str(getattr(row, "evidence_lead", None) or "").strip()
        validation = str(getattr(row, "evidence_lead_validation", None) or "").strip()
        state = _enum(getattr(row, "charter_state", ""))
        if state not in _SIGNED_CHARTER_STATES:
            continue
        if not lead or lead == actor:
            continue
        if not validation or validation.upper().startswith("NOT_VALIDATED"):
            continue
        return True
    return False


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
    source_verifications=None,
) -> dict:
    """Admit one claim, or return a quarantine/preserved reason.

    The specialist ``quotation`` is the passage to find. It is never archived
    as the original document and its hash is never the verification proof.
    A local snapshot that contains the passage is still not a receipt.
    """
    source = claim["source"]
    quotation = str(source["quotation"])
    url = str(source["url"])
    statement = str(claim["statement"])
    actor = str(result["actor_id"])
    blocked = _blocked_retrievers(actor, str(result.get("specialist_id") or ""), str(result.get("canonical_role") or ""))
    archive = bundle.archive
    registry = bundle.registry
    local = _local_snapshot_bytes(
        url,
        independent_snapshots=independent_snapshots,
        snapshot_dir=snapshot_dir,
    )
    trusted = _trusted_archived_source(archive, url, quotation, blocked)
    receipt = None if trusted and passage_occurs_in_independent_bytes(quotation, trusted[1]) else _matching_receipt(
        source_verifications, url, quotation
    )
    if receipt is not None and archive.contains("SRC-01", receipt.source_id):
        stored = _hash_checked_blob(archive, receipt.source_id)
        row = archive.load("SRC-01", receipt.source_id)
        retriever = str(getattr(row, "retriever", "") or "").strip()
        same_bytes = stored == receipt.raw_bytes
        same_url = getattr(row, "url_or_identifier", None) == url
        if not same_bytes or not same_url or (retriever and retriever in blocked):
            receipt = None
    trusted_bytes = None
    if trusted is not None and passage_occurs_in_independent_bytes(quotation, trusted[1]):
        trusted_bytes = trusted[1]
    elif receipt is not None:
        trusted_bytes = receipt.raw_bytes
    if not passage_occurs_in_independent_bytes(quotation, trusted_bytes):
        if passage_occurs_in_independent_bytes(quotation, local):
            reason = UNTRUSTED_SNAPSHOT_REASON
        else:
            reason = PASSAGE_ABSENT_REASON
        return {
            "status": "QUARANTINED",
            "verification_status": "UNVERIFIED",
            "reason": reason,
        }
    assert trusted_bytes is not None
    if claim["evidence_type"] == "FACT" and not statement_supported_by_passage(statement, quotation):
        if not evidence_lead_signoff_recorded(registry, actor):
            return {
                "status": "QUARANTINED",
                "verification_status": "UNVERIFIED",
                "reason": STATEMENT_UNSUPPORTED_REASON,
            }
    digest = hashlib.sha256(trusted_bytes).hexdigest()
    passage_digest = hashlib.sha256(quotation.encode("utf-8")).hexdigest()
    seed = f"{result['gap_id']}:{index}:{digest}:{passage_digest}"
    evidence_id = str(deterministic_uuid7(f"ev:{seed}", ts_ms=ts_ms))
    tier = str(source["source_tier"])
    if trusted is not None and passage_occurs_in_independent_bytes(quotation, trusted[1]):
        source_id = trusted[0].source_id
    elif receipt is not None and archive.contains("SRC-01", receipt.source_id):
        source_id = receipt.source_id
    elif receipt is not None:
        source_id = receipt.source_id
        try:
            archive.admit_source(
                SourceRecord(
                    content_hash=receipt.content_hash,
                    retrieval_date=str(receipt.retrieval_date),
                    source_id=source_id,
                    source_tier=SourceRecordSource_tier(receipt.source_tier),
                    source_type=SourceRecordSource_type(receipt.source_type),
                    url_or_identifier=url,
                    publication_date=receipt.publication_date,
                    retrieval_method="M6 original-source verification receipt",
                    retriever=_M6_RETRIEVER,
                    title=(receipt.title or statement)[:240],
                ),
                receipt.raw_bytes,
            )
        except (ValueError, TypeError):
            return {
                "status": "QUARANTINED",
                "verification_status": "UNVERIFIED",
                "reason": UNTRUSTED_SNAPSHOT_REASON,
            }
    else:
        return {
            "status": "QUARANTINED",
            "verification_status": "UNVERIFIED",
            "reason": UNTRUSTED_SNAPSHOT_REASON,
        }
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
        validation_method=(
            "cited passage found in an S5/M6 receipt or trusted archived source, "
            "and the FACT statement matches that passage or an Evidence Lead sign-off is recorded"
        ),
    )
    admission = EvidenceAdmissionRecord(
        admission_id=str(deterministic_uuid7(f"ear:{seed}", ts_ms=ts_ms)),
        admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
        admission_timestamp=str(source["retrieval_timestamp"]),
        admitting_role="Evidence Intelligence Lead",
        evidence_id=evidence_id,
        source_tier_check=tier,
        validation_method=(
            "cited passage found in an S5/M6 receipt or trusted archived source, "
            "and the FACT statement matches that passage or an Evidence Lead sign-off is recorded"
        ),
        source_as_of=str(source["source_date"])[:10],
        validation_notes=(
            "Passage located in a pre-existing trusted source identity or minted "
            "M6 receipt. A local snapshot was not the receipt. The specialist "
            "quotation hash was not the source hash."
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
    source_verifications=None,
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
            source_verifications=source_verifications,
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
