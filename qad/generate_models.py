#!/usr/bin/env python3
"""M5.1 — Canonical Schema Code Generator.
Reads QAD-M4A-CANONICAL-SCHEMAS.md and generates Pydantic v2 models.
Groups schemas by canonical family sections (## headers).
Non-production deterministic generation — frozen inputs produce frozen outputs.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
SCHEMAS_MD = BASE.parent / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
OUTPUT = BASE / "models"
OUTPUT.mkdir(parents=True, exist_ok=True)

FAMILY_TITLES = {
    "A": "Identity & Coverage",
    "B": "Evidence & Sources",
    "C": "Research Case & Execution",
    "D": "Business & Industry Quality",
    "E": "Dislocation & Impairment",
    "F": "Financial & Valuation",
    "G": "Challenge, Audit & Governance",
    "H": "Monitoring & Knowledge",
    "I": "System & Infrastructure",
}

TYPE_MAP = {
    "entity_id": "str", "primary_ticker": "str", "cik": "str", "name": "str",
    "exchange": "str", "security_type": "str", "status": "str",
    "isin": "Optional[str]", "sedol": "Optional[str]", "adr_flag": "Optional[bool]",
    "dual_listings": "Optional[list[str]]", "ticker_history": "Optional[list[str]]",
    "corporate_actions": "Optional[list[str]]", "sector": "Optional[str]", "industry": "Optional[str]",
    "inclusion_state": "str", "inclusion_reason": "str", "as_of_date": "str",
    "exclusion_category": "Optional[str]", "exclusion_detail": "Optional[str]",
    "quality_flag": "Optional[bool]", "dislocation_flag": "Optional[bool]", "last_reviewed": "Optional[str]",
    "signal_id": "str", "signal_type": "str", "source_signal": "str", "signal_date": "str",
    "summary": "str", "evidence_ids": "Optional[list[str]]",
    "confidence": "Optional[str]", "resolution_state": "Optional[str]",
    "candidate_id": "str", "candidate_type": "str", "origin_signal_id": "str",
    "decision_rationale": "str", "review_state": "str",
    "case_id": "str", "research_charter_id": "str", "case_status": "str",
    "source_id": "str", "source_type": "str", "retrieval_method": "str",
    "source_url": "str", "content_hash": "str", "publication_date": "str", "access_date": "str",
    "source_version": "Optional[str]",
    "evidence_id": "str", "claim_id": "str", "fact_id": "str",
    "evidence_type": "str", "evidence_status": "str", "evidence_text": "str",
    "extracted_by": "str", "verification_status": "str",
    "inference_id": "str", "inference_type": "str", "inference_text": "str",
    "premise_ids": "Optional[list[str]]",
    "hypothesis_id": "str", "hypothesis_text": "str", "hypothesis_type": "str", "test_status": "str",
    "contradiction_id": "str", "contradiction_type": "str", "contradiction_summary": "str",
    "contradiction_evidence": "Optional[list[str]]",
    "gap_id": "str", "gap_type": "str", "gap_description": "str", "impact": "str",
    "filled_by": "Optional[str]",
    "admission_id": "str", "admission_decision": "str", "admission_rationale": "str",
    "reviewer": "str", "reviewer_role": "str",
    "version_id": "str", "parent_source_id": "str", "change_summary": "str",
    "charter_id": "str", "charter_type": "str", "scope_definition": "str", "start_date": "str",
    "stage_id": "str", "stage_type": "str", "stage_status": "str",
    "started_at": "str", "completed_at": "Optional[str]",
    "investigator_id": "str", "investigator_type": "str",
    "budget_id": "str", "budget_allocated": "float", "budget_consumed": "float", "budget_unit": "str",
    "failure_id": "str", "failure_stage": "str", "failure_mode": "str", "failure_detail": "str",
    "hypothesis_set_id": "str", "hypotheses": "dict",
    "report_id": "str", "report_summary": "str", "key_findings": "str",
    "stop_id": "str", "stop_reason": "str", "saturation_threshold": "Optional[float]",
    "quality_id": "str", "quality_dimension": "str", "quality_score": "str", "quality_rationale": "str",
    "moat_id": "str", "moat_type": "str", "moat_width": "str", "moat_trend": "str",
    "moat_evidence": "Optional[list[str]]", "moat_depth": "Optional[str]", "moat_durability": "Optional[str]",
    "industry_id": "str", "industry_attractiveness": "str", "industry_dynamics": "str",
    "management_claim_id": "str", "management_statement": "str", "claim_context": "str",
    "outcome_status": "Optional[str]",
    "event_id": "str", "event_type": "str", "event_date": "str", "event_detail": "str",
    "decision_id": "str", "decision_type": "str",
    "outcome_id": "str", "outcome_measurement": "str",
    "dislocation_id": "str", "dislocation_type": "str", "dislocation_severity": "str",
    "impairment_id": "str", "impairment_type": "str", "impairment_severity": "str",
    "explanation_id": "str", "explanation_text": "str", "explanation_type": "str",
    "recovery_id": "str", "recovery_mechanism": "str", "recovery_timeframe": "str",
    "thesis_killer_id": "str", "thesis_killer_evidence": "Optional[list[str]]",
    "flip_evidence_id": "str", "flip_type": "str",
    "financial_fact_id": "str", "fiscal_period": "str", "metric_name": "str",
    "metric_value": "float", "currency": "str",
    "normalized_id": "str", "adjustment_rationale": "str",
    "calc_id": "str", "calc_type": "str", "calc_result": "float", "calc_inputs": "dict",
    "scenario_id": "str", "scenario_name": "str", "scenario_assumptions": "dict",
    "permanent_loss_id": "str", "loss_type": "str", "loss_estimate": "Optional[float]",
    "dcf_id": "str", "implied_expectations": "dict",
    "valuation_id": "str", "valuation_method": "str",
    "valuation_range_low": "float", "valuation_range_high": "float",
    "pie_id": "str", "pie_type": "str", "market_price": "float", "implied_growth": "float",
    "challenge_id": "str", "challenge_type": "str", "challenge_finding": "str",
    "challenge_severity": "str", "challenge_status": "str",
    "finding_id": "str", "finding_type": "str", "finding_detail": "str",
    "audit_id": "str", "audit_scope": "str", "audit_verdict": "str",
    "audit_trail": "Optional[list[str]]",
    "underwriting_id": "str", "underwriter": "str", "underwriting_decision": "str",
    "condition": "Optional[list[str]]",
    "publication_id": "str", "article_slug": "str", "publish_timestamp": "str", "editor": "str",
    "founder_decision_id": "str", "founder_reference": "str",
    "response_id": "str", "response_summary": "str", "response_status": "str",
    "indicator_id": "str", "indicator_type": "str",
    "observation_id": "str", "observation_value": "str",
    "assessment_id": "str", "assessment_verdict": "str",
    "lesson_id": "str", "lesson_type": "str",
    "knowledge_id": "str", "knowledge_domain": "str",
    "playbook_id": "str", "playbook_industry": "str", "playbook_insight": "str",
    "cross_case_id": "str", "comparison_summary": "str",
    "manifest_id": "str", "run_id": "str", "execution_mode": "str", "run_status": "str",
    "pit_context_id": "str", "mode_pit": "str", "as_of_bound": "str", "seal_hash": "Optional[str]",
    "invocation_id": "str", "service_id": "str", "invocation_status": "str",
    "duration_ms": "Optional[int]", "input_summary": "str", "output_summary": "str",
    "retry_id": "str", "retry_count": "int", "max_retries": "int", "last_error": "Optional[str]",
    "lock_id": "str", "locked_by": "str", "lock_acquired": "str", "lock_expiry": "Optional[str]",
    "budget_usage_id": "str", "tokens_used": "int", "cost_usd": "float",
    "model_id": "str", "model_tier": "str", "provider_id": "str",
    "eh_run_id": "str", "evaluation_type": "str", "fixture_ids": "Optional[list[str]]",
    "margins_normal": "Optional[str]", "roic_industry": "Optional[str]",
    "capital_entry_barriers": "Optional[str]", "future_capacity_pipeline": "Optional[str]",
    "porter_forces": "Optional[dict]",
    "mechanism_evidence": "Optional[dict]",
    "false_quality_concerns": "Optional[list[str]]",
    "margins_operating": "Optional[str]",
    "revenue_growth_rate": "Optional[str]",
    "fcf_margin": "Optional[str]",
    "debt_structure": "Optional[str]",
    "capex_profile": "Optional[str]",
    "management_quality": "Optional[str]",
    "governance_concerns": "Optional[str]",
    "related_parties": "Optional[str]",
    "risk_factors": "Optional[list[str]]",
    "key_assumptions": "Optional[dict]",
    "value_drivers": "Optional[list[str]]",
    "margin_of_safety": "Optional[str]",
    "verdict": "str",
    "verdict_rationale": "str",
    "label": "str",
    "detection_method": "str",
    "entry_type": "str",
    "target_price": "Optional[float]",
    "position_rationale": "str",
    "monitoring_triggers": "Optional[list[str]]",
    "adjustment_type": "str",
    "adjustment_amount": "float",
    "fair_value": "float",
    "sensitivity_analysis": "Optional[dict]",
    "testing_status": "str",
    "h1_text": "str",
    "h2_text": "str",
    "h3_text": "str",
    "h4_text": "str",
    "h5_text": "str",
    "priority": "Optional[str]",
    "query": "str",
    "result": "str",
    "resolution": "str",
    "primary_ticker": "str",
    "founder_verdict": "str",
    "founder_notes": "Optional[str]",
    "conclusion": "str",
    "supporting_evidence": "Optional[list[str]]",
    "counter_evidence": "Optional[list[str]]",
    "oom_ratio": "Optional[float]",
    "valuation_implication": "Optional[str]",
    "evidence": "dict",
    "diagnosis": "str",
    "signals": "Optional[list[str]]",
}


def clean_field_name(field: str) -> str:
    """Strip {type: evidence} notation and [] from field names."""
    return re.sub(r"\{.*?\}", "", field).split("[")[0].strip().rstrip("[]{}")


def get_class_name(schema_id: str, name: str) -> str:
    """Derive a unique Python class name from the schema, stripping parenthetical aliases."""
    name = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
    overrides = {
            "RR-01": "RetryRecord",
            "RRM-01": "RunManifestRecord",
            "RSR-01": "ResearchStageRecord",
            "RSR-02": "ResearchStopRecord",
            "MO-01": "MonitoringObservation",
            "MO-02": "ManagementOutcome",
            "CL-01": "CandidateLesson",
            "CLK-01": "CaseLock",
            "RC-01": "ResearchCharter",
            "IC-01": "InvestigatorCharter",
            "EG-01": "EvidenceGap",
        }
    if schema_id in overrides:
        return overrides[schema_id]
    return name.replace(" ", "")


def parse_content(content: str) -> dict:
    """Split content by family section then parse each schema."""
    families = {}
    sections = re.split(r'\n(?=##\s+[A-I]\s+[—\-])', content)
    for section in sections:
        if not section.strip():
            continue
        m_fam = re.search(r'^## ([A-I])\s+[—\-]\s+(.+)$', section, re.MULTILINE)
        if not m_fam:
            continue
        fam_letter = m_fam.group(1)
        families[fam_letter] = []
        schema_blocks = re.split(r'\n(?=###\s+\S)', section)
        for block in schema_blocks:
            if not block.strip():
                continue
            m_id = re.search(r'\|\s*\*\*schema_id\*\*\s*\|\s*(\S+)\s*\|', block)
            if not m_id:
                continue
            sid = m_id.group(1)
            m_name = re.search(r'###\s+\S[^:]*:\s*(.+?)(?:\n|$)', block)
            name = m_name.group(1).strip() if m_name else sid
            req = set()
            m_req = re.search(r'\|\s*\*\*required_fields\*\*\s*\|\s*(.+?)\s*\|', block)
            if m_req:
                req = {clean_field_name(f) for f in re.findall(r'`([^`]+)`', m_req.group(1))}
            opt = set()
            m_opt = re.search(r'\|\s*\*\*optional_fields\*\*\s*\|\s*(.+?)\s*\|', block)
            if m_opt:
                opt = {clean_field_name(f) for f in re.findall(r'`([^`]+)`', m_opt.group(1))}
            pit = set()
            m_pit = re.search(r'\|\s*\*\*PIT fields\*\*\s*\|\s*(.+?)\s*\|', block)
            if m_pit:
                pit = {f.strip() for f in re.findall(r'`([^`]+)`', m_pit.group(1))}
            fks = []
            fk_row = re.search(r'\|\s*\*\*IDs\s*/\s*foreign\s*keys\*\*\s*\|\s*(.+?)\s*\|', block)
            if fk_row:
                fk_matches = re.findall(r'`([^`]+?)\s*→\s*(\S+)\.([^`\s]+)`', fk_row.group(1))
                for field, tgt, tf in fk_matches:
                    fks.append({"field": field.strip().rstrip("[]"), "target": tgt, "target_field": tf})
            families[fam_letter].append({
                "schema_id": sid, "name": name, "required": req, "optional": opt,
                "pit": pit, "fks": fks,
            })
    return families


def generate_family_models(fam_letter: str, schemas: list) -> str:
    fam_title = FAMILY_TITLES.get(fam_letter, "Unknown")
    lines = [
        f'"""Family {fam_letter} — {fam_title}',
        'Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.',
        'Do not edit manually — regenerate via qad/generate_models.py',
        '"""',
        'from __future__ import annotations',
        'from datetime import datetime',
        'from typing import Optional',
        'from pydantic import BaseModel, Field',
        'from qad.provenance import ProvenanceMixin, PITMixin',
        '',
    ]
    for s in sorted(schemas, key=lambda x: x["schema_id"]):
        class_name = get_class_name(s["schema_id"], s["name"])
        all_fields = s["required"] | s["optional"]
        lines.append(f'')
        lines.append(f'class {class_name}(ProvenanceMixin, PITMixin, BaseModel):')
        lines.append(f'    """{s["schema_id"]}: {s["name"]}. Frozen M4A canonical schema."""')
        lines.append(f'    schema_id: str = Field(default="{s["schema_id"]}", frozen=True)')
        for fname in sorted(all_fields):
            fn = fname.replace("[]", "").replace("{}", "")
            py_type = TYPE_MAP.get(fn, "str")
            is_required = fname in s["required"]
            is_immutable = fname in s.get("pit", set()) or fname in ["entity_id"]
            if not is_required:
                if not py_type.startswith("Optional"):
                    py_type = f"Optional[{py_type}]"
            field_args = []
            if not is_required:
                field_args.append("default=None")
            if is_immutable:
                field_args.append("frozen=True")
            field_str = f"    {fn}: {py_type}"
            if field_args:
                field_str += f" = Field({', '.join(field_args)})"
            lines.append(field_str)
        if s["fks"]:
            lines.append('')
            for fk in s["fks"]:
                fk_f = fk["field"].rstrip("[]")
                lines.append(f'    # FK: {fk_f} -> {fk["target"]}.{fk["target_field"]}')
    return '\n'.join(lines)


def main():
    content = SCHEMAS_MD.read_text()
    families = parse_content(content)
    print(f"Generating {sum(len(v) for v in families.values())} schemas across {len(families)} families:")
    for fam in sorted(families.keys()):
        code = generate_family_models(fam, families[fam])
        (OUTPUT / f"family_{fam.lower()}.py").write_text(code)
        print(f"  Family {fam} — {len(families[fam])} schemas")
    all_models = []
    init_lines = ['"""QAD Runtime Schema Models — all 68 frozen M4A canonical schemas."""',
                  'from __future__ import annotations', '']
    for fam in sorted(families.keys()):
        init_lines.append(f'from qad.models.family_{fam.lower()} import (')
        for s in sorted(families[fam], key=lambda x: x["schema_id"]):
            cn = get_class_name(s["schema_id"], s["name"])
            init_lines.append(f'    {cn},')
            all_models.append(cn)
        init_lines.append(')')
        init_lines.append('')
    init_lines.append('')
    init_lines.append('__all__ = [')
    for cn in sorted(all_models):
        init_lines.append(f'    "{cn}",')
    init_lines.append(']')
    (OUTPUT / "__init__.py").write_text('\n'.join(init_lines))
    print(f"\nGenerated __init__.py ({len(all_models)} models)")
    print("Done.")


if __name__ == "__main__":
    main()