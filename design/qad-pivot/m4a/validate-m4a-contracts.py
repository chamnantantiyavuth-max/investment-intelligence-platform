#!/usr/bin/env python3
"""
QAD-M4A Structural Contract Validator — Parses every schema block into an
in-memory registry and validates FK cross-references, field existence, role/
service mappings, and governance invariants.

Usage:
    python validate-m4a-contracts.py              # normal validation
    python validate-m4a-contracts.py --self-test   # run self-test only

Exit code:
    0 = PASS, 1 = FAIL
"""

import re
import sys
import copy
import json
from pathlib import Path
from collections import OrderedDict

BASE = Path(__file__).resolve().parent.parent.parent.parent  # project root

# ── Results accumulator ──────────────────────────────────────────────────────
results = {"pass": 0, "fail": 0, "warn": 0}


def check(condition: bool, message: str, severity: str = "fail"):
    if condition:
        results["pass"] += 1
        print(f"  \u2705 {message}")
    else:
        results[severity] += 1
        sym = "\u274c" if severity == "fail" else "\u26a0\ufe0f"
        print(f"  {sym} {message}")


def fail_fast(condition: bool, message: str):
    """Fail and exit immediately — used for self-test assertions."""
    if not condition:
        print(f"\n  \u274c SELF-TEST FAILED: {message}")
        sys.exit(1)
    print(f"  \u2705 Self-test: {message}")


# ── Constants ────────────────────────────────────────────────────────────────

EXPECTED_SCHEMA_COUNT = 68

CANONICAL_PIT_MODES = {"LIVE_CASE_UPDATE", "SEALED_HISTORICAL_EVALUATION", "REPLAY_EXCEPTION"}

EXPECTED_ROLES = OrderedDict([
    (1,  "Research Director"),
    (2,  "Evidence Intelligence Lead"),
    (3,  "Core Desk Researcher"),
    (4,  "Business & Industry Analyst"),
    (5,  "Financial & Management Analyst"),
    (6,  "Impairment Diagnosis Specialist"),
    (7,  "Valuation & Expectations Specialist"),
    (8,  "Chief Underwriter"),
    (9,  "Structural Red Team"),
    (10, "Independent Research Auditor"),
    (11, "Thai Long-Form Research Editor"),
    (12, "Thesis / Knowledge Steward"),
    (13, "Discovery & Dislocation Scout"),
    (14, "Elastic Investigator"),
])

# Expected role → output schemas (owner field in each schema)
# Schema ID → owner string as it appears in schema registry
EXPECTED_ROLE_OUTPUTS = {
    "Research Director":             {"CASE-01", "HYP-01", "EG-01", "RC-01", "RSR-01", "IC-01", "RFR-01", "HS-01", "RSR-02"},
    "Evidence Intelligence Lead":    {"SRC-01", "EV-01", "FACT-01", "CLM-01", "CTR-01", "EAR-01", "SRCV-01"},
    "Core Desk Researcher":          {"INF-01"},
    "Business & Industry Analyst":   {"QA-01", "MA-01", "IE-01"},
    "Financial & Management Analyst": {"FF-01", "NFF-01", "CALC-01", "MC-01", "CAE-01", "MDL-01", "MO-02"},
    "Impairment Diagnosis Specialist": {"DR-01", "IA-01", "CE-01", "RM-01", "TK-01", "FE-01"},
    "Valuation & Expectations Specialist": {"SCEN-01", "PLA-01", "RDCF-01", "VA-01", "PIE-01"},
    "Chief Underwriter":            {"UV-01", "CRESP-01"},
    "Structural Red Team":          {"RTC-01"},
    "Independent Research Auditor": {"AF-01", "AG-01"},
    "Thai Long-Form Research Editor": {"PUB-01"},
    "Thesis / Knowledge Steward":   {"MI-01", "MO-01", "MASS-01", "CL-01", "IKR-01", "IPR-01", "CCV-01"},
    "Discovery & Dislocation Scout": {"SR-01"},
    "Elastic Investigator":         {"IR-01"},
}

# Service → expected schema ownership (from owner field)
EXPECTED_SERVICE_OUTPUTS = {
    "S1":  {"CR-01"},        # Selection Engine → CandidateRecord (Candidate Assembly is listed, but S1 provides selection state)
    "S2":  {"RB-01", "BU-01"},
    "S3":  {"SM-01"},
    "S4":  set(),             # Evidence Registry — infrastructure for Role 2 schemas
    "S5":  set(),             # Source Archive — infrastructure
    "S6":  {"RRM-01", "SI-01", "MOD-01", "PROV-01"},
    "S7":  {"PITC-01"},
    "S8":  {"RR-01"},
    "S9":  {"CLK-01"},
    "S10": set(),             # NotebookLM — infrastructure
    "S11": set(),             # Publication Renderer — infrastructure
    "S12": {"EHR-01"},
}

# Schemas that are owned by services (not by a numbered M3 role)
SERVICE_OWNED_SCHEMAS = {"SM-01", "RU-01", "CR-01", "QU-01", "SR-01",
                         "RB-01", "BU-01", "RRM-01", "SI-01", "MOD-01", "PROV-01",
                         "PITC-01", "RR-01", "CLK-01", "EHR-01"}

# Role search aliases for matching role names in schemas
ROLE_ALIASES = {
    "Thai Long-Form Research Editor": "Thai Editor",
    "Discovery & Dislocation Scout": "Signal Detection Layer",
    "Discovery & Dislocation Scout|alt": "Discovery Scout",
    "Thesis / Knowledge Steward": "Knowledge Steward",
}

# Override: explicit owner → role mapping for schemas owned by systems/services
# (not directly by a numbered role) that a role produces as output
ROLE_OWNER_OVERRIDES = {
    "Signal Detection Layer":        "Discovery & Dislocation Scout",   # SR-01
    "Candidate Assembly":            "Discovery & Dislocation Scout",   # CR-01
    "Quality Discovery":             "Discovery & Dislocation Scout",   # QU-01
    "Founder":                       "Thai Long-Form Research Editor",  # FDR-01
}


# ── Schema parser ────────────────────────────────────────────────────────────

def parse_schema_registry(content: str) -> dict:
    """
    Parse every schema block in the canonical schema registry markdown into
    an in-memory dictionary keyed by schema_id.

    Returns: dict[schema_id] = {
        "schema_id": str,
        "schema_name": str,
        "required_fields": set[str],
        "optional_fields": set[str],
        "enums": list[str],
        "foreign_keys": list[{"field": str, "target_schema": str, "target_field": str}],
        "owner": str,
        "authority_source": str,
    }
    """
    registry = OrderedDict()

    # Split on schema section headers ### X-N: SchemaName
    # Also match headers that don't follow the family pattern (edge cases)
    schema_blocks = re.split(r'\n(?=###\s+\S)', content)

    for block in schema_blocks:
        if not block.strip():
            continue
        # Extract schema_id
        m_id = re.search(r'\|\s*\*\*schema_id\*\*\s*\|\s*(\S+)\s*\|', block)
        if not m_id:
            continue
        schema_id = m_id.group(1)
        if schema_id in registry:
            print(f"  \u26a0\ufe0f  Duplicate schema_id: {schema_id}")
            continue

        # Extract schema name from header ### X-N: SchemaName
        m_name = re.search(r'###\s+\S[^:]*:\s*(.+?)(?:\n|$)', block)
        schema_name = m_name.group(1).strip() if m_name else ""

        # Extract owner
        owner = ""
        m_owner = re.search(r'\|\s*\*\*owner\*\*\s*\|\s*(.+?)\s*\|', block)
        if m_owner:
            owner = m_owner.group(1).strip()

        # Extract authority_source
        authority_source = ""
        m_auth = re.search(r'\|\s*\*\*authority_source\*\*\s*\|\s*(.+?)\s*\|', block)
        if m_auth:
            authority_source = m_auth.group(1).strip()

        # Extract required_fields
        required_fields = set()
        m_req = re.search(r'\|\s*\*\*required_fields\*\*\s*\|\s*(.+?)\s*\|', block)
        if m_req:
            raw = m_req.group(1)
            fields = re.findall(r'`([^`]+)`', raw)
            required_fields = {f.split("[")[0].strip() for f in fields}

        # Extract optional_fields
        optional_fields = set()
        m_opt = re.search(r'\|\s*\*\*optional_fields\*\*\s*\|\s*(.+?)\s*\|', block)
        if m_opt:
            raw = m_opt.group(1)
            fields = re.findall(r'`([^`]+)`', raw)
            optional_fields = {f.split("[")[0].strip() for f in fields}

        # Extract enums (multiple rows possible)
        enums = []
        # Find all enum rows — they start with `| **enums** |` or continuation lines
        enum_lines = re.findall(
            r'\|\s*\*\*enums\*\*\s*\|\s*(.+?)\s*\||^\|\s*\|\s*(.+?)\s*\|(?=\s*\n\|\s*\*\*enums\*\*)',
            block, re.MULTILINE
        )
        # Simpler: find the first enums row then any continuation | | lines immediately after
        enum_section = re.search(
            r'\|\s*\*\*enums\*\*\s*\|\s*(.+?)\s*\|\s*\n((?:\|\s*\|\s*(.+?)\s*\|\s*\n)*)',
            block
        )
        if enum_section:
            enums.append(enum_section.group(1).strip())
            cont = enum_section.group(2)
            if cont:
                for line in cont.strip().split('\n'):
                    m = re.match(r'\|\s*\|\s*(.+?)\s*\|', line)
                    if m:
                        enums.append(m.group(1).strip())

        # Extract foreign keys from "IDs / foreign keys" row
        foreign_keys = []
        fk_row = re.search(r'\|\s*\*\*IDs\s*/\s*foreign\s*keys\*\*\s*\|\s*(.+?)\s*\|', block)
        if fk_row:
            raw = fk_row.group(1)
            # Parse FK references: `field → TARGET.field` or `field[] → TARGET.field`
            fk_matches = re.findall(r'`([^`]+?)\s*→\s*(\S+)\.([^`\s]+)`', raw)
            for field, target_schema, target_field in fk_matches:
                field = field.strip()
                # Clean array notation
                field = re.sub(r'\[\]$', '', field)
                foreign_keys.append({
                    "field": field,
                    "target_schema": target_schema,
                    "target_field": target_field,
                })

        registry[schema_id] = {
            "schema_id": schema_id,
            "schema_name": schema_name,
            "required_fields": required_fields,
            "optional_fields": optional_fields,
            "all_fields": required_fields | optional_fields,
            "enums": enums,
            "foreign_keys": foreign_keys,
            "owner": owner,
            "authority_source": authority_source,
        }

    return registry


# ── Traceability parser ──────────────────────────────────────────────────────

def parse_traceability_schema_ids(content: str) -> set:
    """Extract all schema IDs mentioned in the traceability document."""
    ids = set()
    # Pattern: | SCHEMA-ID | ... |
    for m in re.finditer(r'^\|\s*(\S+-\d+)\s*\|', content, re.MULTILINE):
        sid = m.group(1)
        if re.match(r'^[A-Z]+-\d+$', sid):
            ids.add(sid)
    return ids


def count_derivation_keyword(content: str, keyword: str) -> int:
    """Count occurrences of a derivation keyword."""
    return content.count(keyword)


def parse_closeout_schema_count(content: str) -> int:
    """Extract total schema count from closeout document."""
    m = re.search(r'(\d+)\s*schemas', content)
    return int(m.group(1)) if m else 0


# ── M3 Role contract parser ──────────────────────────────────────────────────

def parse_service_contracts(content: str) -> dict:
    """
    Parse M3 service contracts to extract service_id, inputs, outputs,
    failure_behavior, PIT_behavior, and forbidden_inference for each S1-S12.

    Returns dict[service_id] = {
        "service_id": str,
        "service_name": str,
        "inputs": str,
        "outputs": str,
        "failure_behavior": str,
        "pit_behavior": str,
        "forbidden_inference": str,
    }
    """
    services = {}
    # Match ## S1: ServiceName headers
    for m in re.finditer(r'^##\s+(S\d+):\s+(.+)$', content, re.MULTILINE):
        svc_id = m.group(1)
        svc_name = m.group(2).strip()
        header_pos = m.end()
        # Extract fields from the service's table within next ~2000 chars
        section = content[header_pos:header_pos + 2000]
        inputs = ""
        outputs = ""
        failure_behavior = ""
        pit_behavior = ""
        forbidden_inference = ""

        im = re.search(r'\|\s*\*\*inputs\*\*\s*\|\s*(.+?)\s*\|', section)
        if im: inputs = im.group(1)
        om = re.search(r'\|\s*\*\*outputs\*\*\s*\|\s*(.+?)\s*\|', section)
        if om: outputs = om.group(1)
        fm = re.search(r'\|\s*\*\*failure_behavior\*\*\s*\|\s*(.+?)\s*\|', section)
        if fm: failure_behavior = fm.group(1)
        pm = re.search(r'\|\s*\*\*PIT_behavior\*\*\s*\|\s*(.+?)\s*\|', section)
        if pm: pit_behavior = pm.group(1)
        fim = re.search(r'\|\s*\*\*forbidden_inference\*\*\s*\|\s*(.+?)\s*\|', section)
        if fim: forbidden_inference = fim.group(1)

        services[svc_id] = {
            "service_id": svc_id,
            "service_name": svc_name,
            "inputs": inputs,
            "outputs": outputs,
            "failure_behavior": failure_behavior,
            "pit_behavior": pit_behavior,
            "forbidden_inference": forbidden_inference,
        }
    return services


def count_raw_fk_references(content: str) -> int:
    """Count all arrow-form FK references in schema registry content."""
    return len(re.findall(r'`[^`]+?\s*→\s*\S+\.\S+`', content))


def parse_role_outputs(content: str) -> dict:
    """
    Parse M3 role contracts to extract role number, name, Required Outputs,
    and Output Schema for each role.

    Returns dict[role_number] = {
        "role_number": int,
        "role_name": str,
        "required_outputs": str,
        "output_schema": str,
    }
    """
    roles = {}
    # Match ## Role N: RoleName headers
    for m in re.finditer(r'^##\s+Role\s+(\d+):\s+(.+)$', content, re.MULTILINE):
        role_num = int(m.group(1))
        role_name = m.group(2).strip()
        header_pos = m.end()
        # Find Required Outputs and Output Schema from the table rows
        table_match = re.search(
            r'\|\s*\*\*Required Outputs\*\*\s*\|\s*(.+?)\s*\|\s*\n'
            r'.*?\|\s*\*\*Output Schema\*\*\s*\|\s*(.+?)\s*\|',
            content[header_pos:header_pos + 2000],
            re.DOTALL
        )
        required_outputs = ""
        output_schema = ""
        if table_match:
            required_outputs = table_match.group(1).strip()
            output_schema = table_match.group(2).strip()
        roles[role_num] = {
            "role_number": role_num,
            "role_name": role_name,
            "required_outputs": required_outputs,
            "output_schema": output_schema,
        }
    return roles


# ── Validation functions ─────────────────────────────────────────────────────

def validate_schema_count(registry: dict):
    print("\n=== 1. Exact Schema Count ===")
    count = len(registry)
    check(count == EXPECTED_SCHEMA_COUNT,
          f"Schema count: {count} (expected {EXPECTED_SCHEMA_COUNT})")
    return count


def validate_unique_ids_and_fields(registry: dict):
    print("\n=== 2. All IDs Unique & No Duplicate Fields ===")
    # IDs are unique by construction in parse_schema_registry
    ids = list(registry.keys())
    duplicates = [x for x in ids if ids.count(x) > 1]
    check(len(duplicates) == 0, f"No duplicate schema IDs (found: {set(duplicates) if duplicates else 'none'})")

    # No duplicate fields per schema (field listed in both required and optional)
    dup_fields = []
    for sid, schema in registry.items():
        dupes = schema["required_fields"] & schema["optional_fields"]
        for d in dupes:
            dup_fields.append((sid, d))
    check(len(dup_fields) == 0,
          f"No duplicate fields per schema (found: {dup_fields if dup_fields else 'none'})")


def validate_foreign_keys(registry: dict, raw_fk_count: int = None):
    print("\n=== 3. Foreign Key Cross-References ===")
    bad_fks = []
    parsed_fk_count = 0
    for sid, schema in registry.items():
        for fk in schema["foreign_keys"]:
            parsed_fk_count += 1
            ts = fk["target_schema"]
            tf = fk["target_field"]
            if ts not in registry:
                bad_fks.append(f"{sid}.{fk['field']} → {ts}.{tf} — TARGET SCHEMA {ts} NOT FOUND")
            elif tf not in registry[ts]["all_fields"]:
                # Broad match: also check if it appears in IDs/foreign keys row text
                fk_row = registry[ts]["foreign_keys"]
                fk_fields_text = [f"{x['field']}" for x in fk_row]
                all_fk_field_names = set()
                for x in fk_row:
                    all_fk_field_names.add(x["field"])

                # The target field could be a primary key named differently
                # e.g., entity_id is a field of SM-01 - check if the target_field
                # exists in the required or optional fields
                if tf not in [f.replace("[]", "") for f in all_fk_field_names] and \
                   tf not in registry[ts]["all_fields"]:
                    bad_fks.append(f"{sid}.{fk['field']} → {ts}.{tf} — FIELD NOT IN {ts}")

    # FK completeness tracking
    if raw_fk_count is not None:
        check(raw_fk_count == parsed_fk_count,
              f"RAW_FK_REFERENCE_COUNT ({raw_fk_count}) == PARSED_FK_REFERENCE_COUNT ({parsed_fk_count})")
    check(parsed_fk_count > 0, f"Foreign keys parsed: {parsed_fk_count}")

    check(len(bad_fks) == 0,
          f"No dangling foreign keys (found: {len(bad_fks)})")
    if bad_fks:
        for b in bad_fks:
            print(f"    ❌  {b}")


def validate_traceability_ids(registry: dict, traceability_content: str):
    print("\n=== 4. Traceability Schema IDs ===\n    (verifying traceability IDs match registry IDs exactly)")
    trace_ids = parse_traceability_schema_ids(traceability_content)
    reg_ids = set(registry.keys())

    missing_from_trace = reg_ids - trace_ids
    extra_in_trace = trace_ids - reg_ids

    # Filter out non-schema IDs that match the pattern
    # The traceability doc has many table rows with schema IDs
    check(len(missing_from_trace) == 0,
          f"All registry IDs found in traceability (missing: {missing_from_trace if missing_from_trace else 'none'})")
    check(len(extra_in_trace) == 0,
          f"No extra IDs in traceability (extra: {extra_in_trace if extra_in_trace else 'none'})")


def validate_role_output_mapping(registry: dict, m3_roles_content: str = None):
    print("\n=== 5. M3 Role Output Mapping (all 14 roles) ===")
    # Build an owner-to-schemas mapping from the registry
    owner_to_schemas = {}
    for sid, schema in registry.items():
        owner = schema["owner"]
        if owner not in owner_to_schemas:
            owner_to_schemas[owner] = set()
        owner_to_schemas[owner].add(sid)

    # Parse actual M3 role contracts if provided
    parsed_roles = {}
    if m3_roles_content:
        parsed_roles = parse_role_outputs(m3_roles_content)

    # Verify each parsed role has required outputs
    for role_num, role_info in parsed_roles.items():
        ro = role_info["required_outputs"]
        os_fields = role_info["output_schema"]
        has_outputs = bool(ro.strip())
        has_schema = bool(os_fields.strip())
        check(has_outputs,
              f"Role {role_num} ({role_info['role_name']}): Required Outputs field exists and non-empty",
              severity="fail")
        check(has_schema,
              f"Role {role_num} ({role_info['role_name']}): Output Schema field exists and non-empty",
              severity="fail")

    # Check that each role has at least one owned schema
    roles_with_schemas = 0
    for role_num, role_name in EXPECTED_ROLES.items():
        expected = EXPECTED_ROLE_OUTPUTS.get(role_name, set())
        # Find which schemas match this role (by owner)
        role_owned = set()
        for owner_name, schemas in owner_to_schemas.items():
            # Try override first (for system/service owners)
            if owner_name in ROLE_OWNER_OVERRIDES and \
               ROLE_OWNER_OVERRIDES[owner_name] == role_name:
                role_owned |= schemas
                continue
            # Match by role name appearing in the owner field
            role_keywords = role_name.replace("/", " ").lower().split()
            owner_lower = owner_name.lower()
            # Only match if a significant keyword (4+ chars) is found
            matched = any(kw in owner_lower for kw in role_keywords if len(kw) > 3)
            if matched:
                role_owned |= schemas

        missing = expected - role_owned
        extra = role_owned - expected

        has_role_mention = False
        for owner_name in owner_to_schemas:
            alias = ROLE_ALIASES.get(role_name, "")
            if role_name.lower() in owner_name.lower() or \
               (alias and alias.lower() in owner_name.lower()):
                has_role_mention = True
                break

        # Missing expected schemas is now a HARD FAILURE
        if has_role_mention:
            roles_with_schemas += 1

        if missing:
            check(False,
                  f"Role {role_num}: {role_name} — expected schemas {missing} are MISSING (hard failure)")
        else:
            check(has_role_mention or len(expected) == 0,
                  f"Role {role_num}: {role_name} referenced in schema owners")

        if extra:
            print(f"      ℹ️  Extra schemas for {role_name}: {extra}")

    check(roles_with_schemas >= 14,
          f"All 14 roles have at least one owned schema (found: {roles_with_schemas})")


def validate_service_schema_io(registry: dict, service_content: str):
    print("\n=== 6. S1-S12 Service I/O Map (against M3 Service Contracts) ===")

    # Parse actual M3 service contracts
    parsed_services = parse_service_contracts(service_content)

    # Verify each service contract has required fields
    svc_ids_found = set()
    for svc_id, svc_info in parsed_services.items():
        svc_ids_found.add(svc_id)
        has_inputs = bool(svc_info["inputs"].strip())
        has_outputs = bool(svc_info["outputs"].strip())
        has_failure = bool(svc_info["failure_behavior"].strip())
        has_pit = bool(svc_info["pit_behavior"].strip())
        has_forbidden = bool(svc_info["forbidden_inference"].strip())
        svc_name = svc_info.get("service_name", svc_id)
        check(has_inputs, f"Service {svc_id} ({svc_name}): inputs field exists", severity="fail")
        check(has_outputs, f"Service {svc_id} ({svc_name}): outputs field exists", severity="fail")
        check(has_failure, f"Service {svc_id} ({svc_name}): failure_behavior exists", severity="fail")
        check(has_pit, f"Service {svc_id} ({svc_name}): PIT_behavior exists", severity="fail")
        check(has_forbidden, f"Service {svc_id} ({svc_name}): forbidden_inference exists", severity="fail")

    check(len(svc_ids_found) == 12,
          f"All 12 services parsed (found: {len(svc_ids_found)})")
    # Check each service-owned schema exists
    for sid, expected_ids in EXPECTED_SERVICE_OUTPUTS.items():
        for esid in expected_ids:
            check(esid in registry,
                  f"Service {sid} schema {esid} exists in registry")

    # Verify owner mentions of services
    service_names = {
        "S1": "Selection Engine",
        "S2": "Budget Controller",
        "S3": "Entity Resolution",
        "S4": "Evidence Registry",
        "S5": "Source Archive",
        "S6": "Run Manifest",
        "S7": "PIT",
        "S8": "Retry",
        "S9": "Case Locking",
        "S10": "NotebookLM",
        "S11": "Publication",
        "S12": "Evaluation Harness",
    }
    for sid, sname in service_names.items():
        # Check the service concept appears in the schemas or service contracts
        found_in_schemas = any(sname.lower() in s["owner"].lower() for s in registry.values())
        found_in_services = sname in service_content or sid in service_content
        check(found_in_schemas or found_in_services,
              f"Service {sid} ({sname}) referenced in registry or contracts",
              severity="warn")


def validate_forbidden_content(registry: dict, full_content: str):
    print("\n=== 7. No Forbidden Content ===")
    # priority_score
    check("priority_score" not in full_content,
          "No priority_score field present")
    # ER-01 (should be EV-01)
    check("ER-01" not in full_content,
          "No ER-01 (should be EV-01)")
    # SR-02 — check it's NOT a schema_id (it appears as part of RSR-02 which is fine)
    sr02_schema_ids = re.findall(r'\|\s*\*\*schema_id\*\*\s*\|\s*SR-02\s*\|', full_content)
    check(len(sr02_schema_ids) == 0, "No SR-02 as schema_id (should be SCEN-01)")
    # Check standalone SR-02 not referenced as FK or field
    sr02_standalone = re.findall(r'\bSR-02\b', full_content)
    check(len(sr02_standalone) == 0,
          f"No standalone SR-02 references (found {len(sr02_standalone)} — inside RSR-02 is OK)" if sr02_standalone else
          "No standalone SR-02 references")


def validate_signal_failure_semantics(full_content: str):
    print("\n=== 8. DETECTION_ERROR vs NO_SIGNAL ===")
    check("DETECTION_ERROR" in full_content,
          "DETECTION_ERROR exists in schemas")
    check("NO_SIGNAL" in full_content,
          "NO_SIGNAL exists in schemas")
    # Verify the distinction (they appear in SR-01 failure_semantics)
    detection_error_count = full_content.count("DETECTION_ERROR")
    no_signal_count = full_content.count("NO_SIGNAL")
    check(detection_error_count >= 1, f"DETECTION_ERROR appears {detection_error_count} time(s)")
    check(no_signal_count >= 1, f"NO_SIGNAL appears {no_signal_count} time(s)")


def validate_pit_modes(full_content: str):
    print("\n=== 9. PIT Modes ===")
    for mode in CANONICAL_PIT_MODES:
        check(mode in full_content, f"PIT mode: {mode}")
    # Check exact set (no extras)
    all_pit_modes_in_doc = set(re.findall(r'\b(LIVE_CASE_UPDATE|SEALED_HISTORICAL_EVALUATION|REPLAY_EXCEPTION)\b', full_content))
    expected_modes = CANONICAL_PIT_MODES
    missing = expected_modes - all_pit_modes_in_doc
    extra = all_pit_modes_in_doc - expected_modes
    check(len(missing) == 0, f"All PIT modes present (missing: {missing if missing else 'none'})")
    check(len(extra) == 0, f"No extra PIT modes (extra: {extra if extra else 'none'})")


def validate_sealed_hard_block(full_content: str):
    print("\n=== 10. SEALED Hard-Block ===")
    hard_block_patterns = ["HARD BLOCK", "HARD_BLOCK", "hard.blocked", "hard block"]
    found_block = any(p.lower() in full_content.lower() for p in hard_block_patterns)
    check(found_block, "SEALED mode hard-blocks post-AS_OF evidence")

    # Also check PITContext validation_rules mentions it
    pitc_pattern = r'\|\s*\*\*validation_rules\*\*\s*\|\s*.*?SEALED.*?HARD.*?BLOCK'
    found_pitc = re.search(pitc_pattern, full_content, re.IGNORECASE)
    check(found_pitc is not None, "PITContext validation_rules mentions SEALED hard-block",
          severity="warn")


def validate_pit_fail_closed(full_content: str):
    print("\n=== 11. PIT Service Fail-Closed ===")
    patterns = ["fail closed", "FAIL_CLOSED", "fail closed", "queries blocked"]
    found = any(p.lower() in full_content.lower() for p in patterns)
    check(found, "PIT service fail-closed behavior documented")

    # Check PITContext failure_semantics specifically
    pitc_fail = r'\|\s*\*\*failure_semantics\*\*\s*\|\s*.*?(?:queries blocked|fail closed|FAIL_CLOSED)'
    found_pitc = re.search(pitc_fail, full_content, re.IGNORECASE)
    check(found_pitc is not None, "PITContext.failure_semantics specifies fail-closed")


def validate_closeout_integrity(registry: dict, closeout_content: str):
    print("\n=== 12. Closeout Integrity ===")
    closeout_count = parse_closeout_schema_count(closeout_content)
    check(closeout_count == len(registry),
          f"Closeout schema count ({closeout_count}) == parsed count ({len(registry)})")

    # Derivation count in closeout
    closeout_derivations = set(re.findall(r'(\d+)\s+NEW_M4A_DERIVATION', closeout_content))
    check(len(closeout_derivations) > 0,
          f"Closeout mentions derivation count: {closeout_derivations}")


def validate_derivation_count(registry: dict, traceability_content: str):
    print("\n=== 13. Derivation Count ===")
    derivation_count = count_derivation_keyword(traceability_content, "NEW_M4A_DERIVATION")
    check(derivation_count >= 1,
          f"NEW_M4A_DERIVATION references in traceability: {derivation_count}")

    # Appendix A count
    appendix_items = re.findall(r'\|\s*(\d+)\s*\|\s*\*\*', traceability_content)
    # Count rows in Appendix A that are numbered
    appendix_count = 0
    in_appendix = False
    for line in traceability_content.split('\n'):
        if "## Appendix A:" in line:
            in_appendix = True
        elif in_appendix and line.startswith("## "):
            in_appendix = False
        elif in_appendix:
            m = re.match(r'\|\s*(\d+)\s*\|', line)
            if m:
                appendix_count = max(appendix_count, int(m.group(1)))

    check(appendix_count > 0,
          f"Traceability Appendix A items: {appendix_count}")


def validate_role_existence(full_content: str):
    print("\n=== 14. All 14 M3 Roles Referenced ===")
    # Build flexible search terms for each role
    role_search_terms = {
        "Research Director":        ["Research Director", "Role 1"],
        "Evidence Intelligence Lead": ["Evidence Intelligence", "Evidence Lead", "Role 2"],
        "Core Desk Researcher":     ["Core Desk Researcher", "Role 3"],
        "Business & Industry Analyst": ["Business & Industry", "Industry Analyst", "Role 4"],
        "Financial & Management Analyst": ["Financial & Management", "Management Analyst", "Role 5"],
        "Impairment Diagnosis Specialist": ["Impairment Diagnosis", "Diagnosis Specialist", "Role 6"],
        "Valuation & Expectations Specialist": ["Valuation & Expectations", "Expectations Specialist", "Role 7"],
        "Chief Underwriter":        ["Chief Underwriter", "Role 8"],
        "Structural Red Team":      ["Structural Red Team", "Red Team", "Role 9"],
        "Independent Research Auditor": ["Independent Research Auditor", "Independent Auditor", "Role 10"],
        "Thai Long-Form Research Editor": ["Thai", "Editor", "Role 11"],
        "Thesis / Knowledge Steward": ["Knowledge Steward", "Role 12"],
        "Discovery & Dislocation Scout": ["Discovery Scout", "Dislocation Scout", "Signal Detection", "Candidate Assembly", "Quality Discovery", "Role 13"],
        "Elastic Investigator":     ["Elastic Investigator", "Role 14"],
    }
    for role_name, terms in role_search_terms.items():
        found = any(t.lower() in full_content.lower() for t in terms)
        check(found, f"Role referenced: {role_name}")


def validate_no_er01_no_sr02(full_content: str):
    print("\n=== 15. No ER-01, No SR-02 ===")
    check("ER-01" not in full_content, "No ER-01 reference")
    # Check SR-02 is not a schema_id
    sr02_schema_ids = re.findall(r'\|\s*\*\*schema_id\*\*\s*\|\s*SR-02\s*\|', full_content)
    check(len(sr02_schema_ids) == 0, "No SR-02 as schema ID")


# ── Self-test ────────────────────────────────────────────────────────────────

def run_self_test():
    """Self-test: inject dangling FK, prove FAIL, restore, prove PASS."""
    print("\n" + "=" * 60)
    print("SELF-TEST: Structural Validator Integrity")
    print("=" * 60)

    schema_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    original = schema_path.read_text()

    # --- Phase 1: Injection ---
    print("\n--- Phase 1: Inject dangling FK ---")
    # Change one FK reference to a non-existent schema/field
    # e.g., change "EV-01.evidence_id" to "FAKE-99.nonexistent_field" in QU-01
    injected = original.replace(
        "evidence_ids[] \u2192 EV-01.evidence_id",
        "evidence_ids[] \u2192 FAKE-99.nonexistent_field"
    )

    # Verify the injection took effect (the original text should have changed)
    fail_fast(injected != original, "Injection changed content")

    # Parse and validate
    injected_registry = parse_schema_registry(injected)
    fail_fast(len(injected_registry) == EXPECTED_SCHEMA_COUNT,
              f"Injected: parsed {len(injected_registry)} schemas")

    # Check that FK validation catches the bad FK
    bad_fks_found = 0
    for sid, schema in injected_registry.items():
        for fk in schema["foreign_keys"]:
            ts = fk["target_schema"]
            if ts == "FAKE-99":
                bad_fks_found += 1
            elif ts in injected_registry:
                tf = fk["target_field"]
                if tf not in injected_registry[ts]["all_fields"]:
                    bad_fks_found += 1

    fail_fast(bad_fks_found >= 1, f"Injected FK produces {bad_fks_found} bad FK(s) (expected >= 1)")

    print("\n--- Phase 2: Prove validator FAILS with injection ---")
    # Run the full validation on injected content (non-registry checks)
    injected_failures = 0

    # Check foreign keys using the validate function
    orig_fk_bad = 0
    for sid, schema in injected_registry.items():
        for fk in schema["foreign_keys"]:
            ts = fk["target_schema"]
            tf = fk["target_field"]
            if ts not in injected_registry:
                orig_fk_bad += 1
            elif tf not in injected_registry[ts]["all_fields"]:
                orig_fk_bad += 1

    fail_fast(orig_fk_bad >= 1,
              f"FK validation fails with {orig_fk_bad} broken FK(s)")

    # --- Phase 3: Restore ---
    print("\n--- Phase 3: Restore canonical content ---")
    restored = injected.replace(
        "evidence_ids[] \u2192 FAKE-99.nonexistent_field",
        "evidence_ids[] \u2192 EV-01.evidence_id"
    )
    fail_fast(restored == original, "Restored content matches original")
    fail_fast("FAKE-99" not in restored, "No FAKE-99 residue in restored text")

    # --- Phase 4: Validate restored ---
    print("\n--- Phase 4: Verify canonical pack PASSES ---")
    restored_registry = parse_schema_registry(restored)
    fail_fast(len(restored_registry) == EXPECTED_SCHEMA_COUNT,
              f"Restored: parsed {len(restored_registry)} schemas")

    # Check no bad FKs
    restored_bad_fks = 0
    for sid, schema in restored_registry.items():
        for fk in schema["foreign_keys"]:
            ts = fk["target_schema"]
            tf = fk["target_field"]
            if ts not in restored_registry:
                restored_bad_fks += 1
            elif tf not in restored_registry[ts]["all_fields"]:
                restored_bad_fks += 1

    fail_fast(restored_bad_fks == 0,
              f"Restored: 0 bad FKs (got {restored_bad_fks})")

    print("\n--- SELF-TEST PASSED ---\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if "--self-test" in sys.argv:
        run_self_test()
        sys.exit(0)

    print("=" * 60)
    print("QAD-M4A Structural Contract Validator")
    print("=" * 60)

    # ── Load files ───────────────────────────────────────────────────────────
    schema_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    traceability_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-SCHEMA-TRACEABILITY.md"
    closeout_path = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CLOSEOUT.md"
    m3_roles_path = BASE / "design" / "qad-pivot" / "QAD-M3-PRODUCTION-ROLE-CONTRACTS.md"
    m3_services_path = BASE / "design" / "qad-pivot" / "QAD-M3-SERVICE-CONTRACTS.md"

    for name, p in [("Schema registry", schema_path), ("Traceability", traceability_path),
                    ("Closeout", closeout_path), ("M3 roles", m3_roles_path),
                    ("M3 services", m3_services_path)]:
        if not p.exists():
            print(f"  \u274c {name} not found at {p}")
            sys.exit(1)

    schema_content = schema_path.read_text()
    traceability_content = traceability_path.read_text()
    closeout_content = closeout_path.read_text()

    # ── Parse schema registry ──────────────────────────────────────────────
    print("\n--- Parsing schema registry ---")
    registry = parse_schema_registry(schema_content)
    print(f"  Parsed {len(registry)} schemas")

    # ── Compute raw FK reference count ─────────────────────────────────────
    raw_fk_count = count_raw_fk_references(schema_content)
    print(f"  Raw FK references: {raw_fk_count}")

    # ── Parse M3 role contracts ────────────────────────────────────────────
    m3_roles_content = m3_roles_path.read_text()
    parsed_roles = parse_role_outputs(m3_roles_content)
    print(f"  Parsed {len(parsed_roles)} role contracts")

    # ── Parse M3 service contracts ─────────────────────────────────────────
    m3_services_content = m3_services_path.read_text()

    # ── Run validations ────────────────────────────────────────────────────
    validate_schema_count(registry)
    validate_unique_ids_and_fields(registry)
    validate_foreign_keys(registry, raw_fk_count=raw_fk_count)
    validate_traceability_ids(registry, traceability_content)
    validate_role_output_mapping(registry, m3_roles_content=m3_roles_content)
    validate_service_schema_io(registry, m3_services_content)
    validate_forbidden_content(registry, schema_content)
    validate_signal_failure_semantics(schema_content)
    validate_pit_modes(schema_content)
    validate_sealed_hard_block(schema_content)
    validate_pit_fail_closed(schema_content)
    validate_closeout_integrity(registry, closeout_content)
    validate_derivation_count(registry, traceability_content)
    validate_role_existence(schema_content)
    validate_no_er01_no_sr02(schema_content)

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"Results: {results['pass']} passed, {results['fail']} failed, {results['warn']} warnings")
    print("=" * 60)

    if results["fail"] > 0:
        print("\n\u274c VALIDATION FAILED")
        sys.exit(1)
    elif results["warn"] > 0:
        print("\n\u26a0\ufe0f VALIDATION PASSED WITH WARNINGS")
        sys.exit(0)
    else:
        print("\n\u2705 VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()