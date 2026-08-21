"""FK Registry (auto-generated from M4A parser)."""

FK_REGISTRY: dict[str, list[dict]] = {
    "AF-01": [
        {"field": "audit_id", "target": "AG-01", "target_field": "audit_id", "cardinality": "single"},
    ],
    "AG-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "findings", "target": "AF-01", "target_field": "finding_id", "cardinality": "list"},
    ],
    "BU-01": [
        {"field": "budget_id", "target": "RB-01", "target_field": "budget_id", "cardinality": "single"},
    ],
    "CAE-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "CALC-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "CASE-01": [
        {"field": "entity_id", "target": "SM-01", "target_field": "entity_id", "cardinality": "single"},
        {"field": "candidate_id", "target": "CR-01", "target_field": "candidate_id", "cardinality": "single"},
    ],
    "CCV-01": [
        {"field": "lesson_id", "target": "CL-01", "target_field": "lesson_id", "cardinality": "single"},
        {"field": "validating_case_ids", "target": "CASE-01", "target_field": "case_id", "cardinality": "list"},
    ],
    "CE-01": [
        {"field": "impairment_id", "target": "IA-01", "target_field": "impairment_id", "cardinality": "single"},
    ],
    "CL-01": [
        {"field": "source_case_ids", "target": "CASE-01", "target_field": "case_id", "cardinality": "list"},
    ],
    "CLK-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "CLM-01": [
        {"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id", "cardinality": "single"},
    ],
    "CR-01": [
        {"field": "entity_id", "target": "SM-01", "target_field": "entity_id", "cardinality": "single"},
        {"field": "signal_ids", "target": "SR-01", "target_field": "signal_id", "cardinality": "list"},
    ],
    "CRESP-01": [
        {"field": "challenge_id", "target": "RTC-01", "target_field": "challenge_id", "cardinality": "single"},
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "CTR-01": [
        {"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id", "cardinality": "list"},
    ],
    "DR-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "EAR-01": [
        {"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id", "cardinality": "single"},
    ],
    "EG-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "EV-01": [
        {"field": "source_id", "target": "SRC-01", "target_field": "source_id", "cardinality": "single"},
        {"field": "contradicts_ids", "target": "EV-01", "target_field": "evidence_id", "cardinality": "list"},
    ],
    "FACT-01": [
        {"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id", "cardinality": "single"},
    ],
    "FDR-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "publication_id", "target": "PUB-01", "target_field": "publication_id", "cardinality": "single"},
    ],
    "FE-01": [
        {"field": "impairment_id", "target": "IA-01", "target_field": "impairment_id", "cardinality": "single"},
    ],
    "FF-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "source_id", "target": "SRC-01", "target_field": "source_id", "cardinality": "single"},
    ],
    "HS-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "hypothesis_ids", "target": "HYP-01", "target_field": "hypothesis_id", "cardinality": "list"},
    ],
    "HYP-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "IA-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "IC-01": [
        {"field": "gap_id", "target": "EG-01", "target_field": "gap_id", "cardinality": "single"},
    ],
    "IE-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "IKR-01": [
        {"field": "lesson_id", "target": "CL-01", "target_field": "lesson_id", "cardinality": "single"},
    ],
    "INF-01": [
        {"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id", "cardinality": "list"},
    ],
    "IPR-01": [
        {"field": "knowledge_ids", "target": "IKR-01", "target_field": "knowledge_id", "cardinality": "list"},
    ],
    "IR-01": [
        {"field": "investigator_charter_id", "target": "IC-01", "target_field": "investigator_charter_id", "cardinality": "single"},
        {"field": "evidence_gap_id", "target": "EG-01", "target_field": "gap_id", "cardinality": "single"},
    ],
    "MA-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "MASS-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "indicator_ids", "target": "MI-01", "target_field": "indicator_id", "cardinality": "list"},
    ],
    "MC-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "source_id", "target": "SRC-01", "target_field": "source_id", "cardinality": "single"},
    ],
    "MDL-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "MI-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "MO-01": [
        {"field": "indicator_id", "target": "MI-01", "target_field": "indicator_id", "cardinality": "single"},
    ],
    "MO-02": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "management_claim_id", "target": "MC-01", "target_field": "claim_id", "cardinality": "single"},
    ],
    "MOD-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "NFF-01": [
        {"field": "financial_fact_id", "target": "FF-01", "target_field": "financial_fact_id", "cardinality": "single"},
    ],
    "PIE-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "PITC-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "PLA-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "PROV-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "model_invocation_ids", "target": "MOD-01", "target_field": "model_invocation_id", "cardinality": "list"},
    ],
    "PUB-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "verdict_id", "target": "UV-01", "target_field": "verdict_id", "cardinality": "single"},
    ],
    "QA-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id", "cardinality": "list"},
    ],
    "QU-01": [
        {"field": "entity_id", "target": "SM-01", "target_field": "entity_id", "cardinality": "single"},
        {"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id", "cardinality": "list"},
    ],
    "RB-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RC-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "hypothesis_ids", "target": "HYP-01", "target_field": "hypothesis_id", "cardinality": "list"},
    ],
    "RDCF-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RFR-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RM-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RR-01": [
        {"field": "invocation_id", "target": "SI-01", "target_field": "invocation_id", "cardinality": "single"},
    ],
    "RRM-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RSR-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RSR-02": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RTC-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "RU-01": [
        {"field": "entity_id", "target": "SM-01", "target_field": "entity_id", "cardinality": "single"},
    ],
    "SCEN-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "SI-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "SR-01": [
        {"field": "entity_id", "target": "SM-01", "target_field": "entity_id", "cardinality": "single"},
    ],
    "SRCV-01": [
        {"field": "source_id", "target": "SRC-01", "target_field": "source_id", "cardinality": "single"},
    ],
    "TK-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
    ],
    "UV-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "red_team_challenge_id", "target": "RTC-01", "target_field": "challenge_id", "cardinality": "single"},
        {"field": "audit_report_id", "target": "AG-01", "target_field": "audit_id", "cardinality": "single"},
    ],
    "VA-01": [
        {"field": "case_id", "target": "CASE-01", "target_field": "case_id", "cardinality": "single"},
        {"field": "r_dcf_id", "target": "RDCF-01", "target_field": "r_dcf_id", "cardinality": "single"},
        {"field": "permanent_loss_id", "target": "PLA-01", "target_field": "assessment_id", "cardinality": "single"},
    ],
}

# Total FK references: 87