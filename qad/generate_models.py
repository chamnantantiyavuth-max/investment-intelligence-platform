#!/usr/bin/env python3
"""M5.1 — Canonical Schema Code Generator (Contract Compiler).
Reads QAD-M4A-CANONICAL-SCHEMAS.md and generates Pydantic v2 models.
EVERYTHING derives from the ONE parsed representation of frozen M4A.
"""
import hashlib
import json
import re
from pathlib import Path
from collections import OrderedDict

BASE = Path(__file__).resolve().parent
SCHEMAS_MD = BASE.parent / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
OUTPUT = BASE / "models"
OUTPUT.mkdir(parents=True, exist_ok=True)
CONTRACT_DIR = BASE / "contract"
CONTRACT_DIR.mkdir(parents=True, exist_ok=True)

FAMILY_TITLES = OrderedDict([
    ("A", "Identity & Coverage"),
    ("B", "Source & Evidence"),
    ("C", "Research Governance"),
    ("D", "Business / Industry / Management"),
    ("E", "Impairment & Recovery"),
    ("F", "Financial & Economic Underwriting"),
    ("G", "Challenge / Underwriting / Publication"),
    ("H", "Monitoring & Knowledge"),
    ("I", "Reproducibility & Operations"),
])

SCALAR_PATTERNS = {
    "duration_ms": "int", "tokens_used": "int", "retry_count": "int", "max_retries": "int",
    "cost_usd": "float", "market_price": "float", "implied_growth": "float",
    "metric_value": "float", "valuation_range_low": "float", "valuation_range_high": "float",
    "budget_allocated": "float", "budget_consumed": "float", "calc_result": "float",
    "loss_estimate": "float", "saturation_threshold": "float", "oom_ratio": "float",
    "adjustment_amount": "float", "fair_value": "float", "target_price": "float",
    "adr_flag": "bool", "quality_flag": "bool", "dislocation_flag": "bool",
    "is_resolved": "bool", "resolved": "bool",
}


def parse_field_shape(field_name: str) -> tuple[str, str]:
    """Parse field name into (clean_name, container_type). 'list', 'dict', or ''."""
    if field_name.endswith("[]"):
        return field_name[:-2], "list"
    dict_match = re.match(r'^(\w+)\{(.+)\}$', field_name)
    if dict_match:
        return dict_match.group(1), "dict"
    if field_name.endswith("{}"):
        return field_name[:-2], "dict"
    return field_name, ""


def parse_enum_rows(block: str) -> list[dict]:
    """Parse enums from a schema block, including continuation rows."""
    enums = []
    m = re.search(r'\|\s*\*\*enums\*\*\s*\|\s*(.+?)\s*\|', block)
    if not m:
        return enums
    first = m.group(1).strip()
    if first:
        m2 = re.match(r'`(\w+):\s*(.+?)`', first)
        if m2:
            enums.append({"field": m2.group(1), "values": [v.strip() for v in m2.group(2).split("/")]})
    rest = block[m.end():]
    for line in rest.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith('| | '):
            break
        content = stripped.strip('| ').strip()
        m3 = re.match(r'`(\w+):\s*(.+?)`', content)
        if m3:
            enums.append({"field": m3.group(1), "values": [v.strip() for v in m3.group(2).split("/")]})
    return enums


def parse_fk_rows(block: str) -> list[dict]:
    """Parse IDs / foreign keys from a schema block."""
    fks = []
    fk_row = re.search(r'\| \*\*IDs\s*/\s*foreign\s*keys\*\* \| (.+?) \|', block, re.MULTILINE | re.DOTALL)
    if not fk_row:
        return fks
    raw = fk_row.group(1)
    for m in re.finditer(r'`([^`]+?)\s*→\s*(\S+)\.([^`\s]+)`', raw):
        raw_field = m.group(1).strip()
        cardinality = "list" if "[]" in raw_field else "single"
        clean_field = raw_field.split("[")[0].split("{")[0].strip()
        fks.append({"field": clean_field, "target": m.group(2),
                    "target_field": m.group(3), "cardinality": cardinality})
    return fks


def get_field(block: str, label: str) -> str:
    m = re.search(rf'\| \*\*{re.escape(label)}\*\* \| (.+?) \|', block, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def classify_immutability(imm_rules: str, field_name: str, schema_id: str) -> tuple[str, str]:
    """Classify immutability into (policy, detail)."""
    rules_lower = imm_rules.lower()
    # Record-level rules
    if "record immutable" in rules_lower or "content immutable" in rules_lower:
        if field_name in ("content", "context", "evidence_id", "fact_id", "claim_id", "inference_id"):
            return ("FIELD_IMMUTABLE", "field content immutable per contract")
        return ("RECORD_IMMUTABLE", "record immutable per contract")
    if "append-only" in rules_lower and "state" in rules_lower:
        return ("APPEND_ONLY_STATE", "state transitions are append-only")
    if "append-only" in rules_lower:
        if field_name in ("entity_id", "schema_id", "pit_context_id", "case_id"):
            return ("FIELD_IMMUTABLE", "identity field immutable")
        return ("APPEND_ONLY", "schema append-only")
    if field_name in ("entity_id", "schema_id"):
        return ("FIELD_IMMUTABLE", "identity field immutable")
    return ("MUTABLE", "no immutability constraint")


def parse_schema_block(block: str, family: str) -> dict | None:
    """Parse one schema block into a structured descriptor."""
    m_id = re.search(r'\| \*\*schema_id\*\* \| (\S+) \|', block)
    if not m_id:
        return None
    schema_id = m_id.group(1)
    m_name = re.search(r'^### \S[^:]*:\s*(.+?)(?:\n|$)', block, re.MULTILINE)
    name = m_name.group(1).strip() if m_name else schema_id

    required_raw = get_field(block, "required_fields")
    optional_raw = get_field(block, "optional_fields")

    required = set()
    optional = set()
    if required_raw:
        for f in re.findall(r'`([^`]+)`', required_raw):
            clean, _ = parse_field_shape(f)
            if clean:
                required.add(clean)
    if optional_raw:
        for f in re.findall(r'`([^`]+)`', optional_raw):
            clean, _ = parse_field_shape(f)
            if clean:
                optional.add(clean)

    enums = parse_enum_rows(block)
    fks = parse_fk_rows(block)

    pit_raw = get_field(block, "PIT fields")
    pit_fields = set()
    if pit_raw:
        pit_fields = {f.strip() for f in re.findall(r'`([^`]+)`', pit_raw)}

    prov_raw = get_field(block, "provenance fields")
    prov_fields = set()
    if prov_raw:
        prov_fields = {f.strip() for f in re.findall(r'`([^`]+)`', prov_raw)}

    # PIT/provenance-only fields: add to expected surface
    all_pit_prov = pit_fields | prov_fields
    for pf in all_pit_prov:
        pf_clean, _ = parse_field_shape(pf)
        if pf_clean and pf_clean not in required and pf_clean not in optional:
            optional.add(pf_clean)

    # Rebuild all_fields_raw from the complete surface (required + optional + PIT + provenance)
    all_fields_raw = []
    raw_fields_seen = set()
    # Re-parse from original to get raw names with []/{}
    if required_raw:
        for f in re.findall(r'`([^`]+)`', required_raw):
            clean, _ = parse_field_shape(f)
            if clean and clean not in raw_fields_seen:
                all_fields_raw.append(f)
                raw_fields_seen.add(clean)
    if optional_raw:
        for f in re.findall(r'`([^`]+)`', optional_raw):
            clean, _ = parse_field_shape(f)
            if clean and clean not in raw_fields_seen:
                all_fields_raw.append(f)
                raw_fields_seen.add(clean)
    # Add PIT/provenance-only fields with clean names
    for pf in sorted(all_pit_prov):
        pf_clean, _ = parse_field_shape(pf)
        if pf_clean and pf_clean not in raw_fields_seen:
            all_fields_raw.append(pf_clean)
            raw_fields_seen.add(pf_clean)

    cb = get_field(block, "canonical_boundary")
    is_canonical = cb.lower().startswith("canonical") or (
        "canonical" in cb.lower() and "noncanonical" not in cb.lower())
    if schema_id == "PUB-01":
        is_canonical = True

    immutability = get_field(block, "immutability_rules")

    # Build field descriptors — NOW PIT/provenance fields are included
    field_descs = OrderedDict()
    for raw_field in all_fields_raw:
        clean_name, container = parse_field_shape(raw_field)
        if not clean_name or clean_name in field_descs:
            continue
        is_req = clean_name in required
        enum_values = None
        for e in enums:
            if e["field"] == clean_name:
                enum_values = e["values"]
                break
        imm_policy, imm_detail = classify_immutability(immutability, clean_name, schema_id)
        # PIT fields are frozen (point-in-time immutability)
        if clean_name in pit_fields:
            imm_policy = "FIELD_IMMUTABLE"
        is_immutable = imm_policy in ("FIELD_IMMUTABLE", "RECORD_IMMUTABLE")
        field_descs[clean_name] = {
            "raw_name": raw_field, "container": container,
            "required": is_req, "enum_values": enum_values,
            "is_pit": clean_name in pit_fields,
            "is_provenance": clean_name in prov_fields,
            "immutable": is_immutable,
            "immutable_policy": imm_policy,
        }

    return {
        "schema_id": schema_id, "name": name, "family": family,
        "required": required, "optional": optional,
        "field_descriptors": field_descs, "enums": enums, "fks": fks,
        "pit_fields": pit_fields, "provenance_fields": prov_fields,
        "is_canonical": is_canonical,
        "validation_rules": get_field(block, "validation_rules"),
        "immutability_rules": immutability,
        "canonical_boundary": cb,
    }


def parse_all_schemas(content: str) -> dict[str, dict]:
    schemas = OrderedDict()
    sections = re.split(r'\n(?=## [A-I] [—\-])', content)
    for section in sections:
        if not section.strip():
            continue
        m_fam = re.search(r'^## ([A-I])', section, re.MULTILINE)
        if not m_fam:
            continue
        family = m_fam.group(1)
        for block in re.split(r'\n(?=### \S)', section):
            desc = parse_schema_block(block, family)
            if desc:
                schemas[desc["schema_id"]] = desc
    return schemas


def get_class_name(schema_id: str, name: str) -> str:
    overrides = {
        "RR-01": "RetryRecord", "RRM-01": "RunManifestRecord",
        "RSR-01": "ResearchStageRecord", "RSR-02": "ResearchStopRecord",
        "MO-01": "MonitoringObservation", "MO-02": "ManagementOutcome",
        "CL-01": "CandidateLesson", "CLK-01": "CaseLock",
        "RC-01": "ResearchCharter", "IC-01": "InvestigatorCharter",
        "EG-01": "EvidenceGap",
    }
    if schema_id in overrides:
        return overrides[schema_id]
    name = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
    return name.replace(" ", "")


def emit_field(lines, fname, fd, schema, all_enums):
    enum_values = fd.get("enum_values")
    container = fd.get("container", "")
    is_required = fd.get("required", False)
    is_immutable = fd.get("immutable", False)

    if enum_values:
        py_type = f'{get_class_name(schema["schema_id"], schema["name"])}{fname.capitalize()}'
    else:
        base = SCALAR_PATTERNS.get(fname, "str")
        if container == "list":
            py_type = f"list[{base}]"
        elif container == "dict":
            py_type = "dict"
        else:
            py_type = base
    if not is_required and not py_type.startswith("Optional"):
        py_type = f"Optional[{py_type}]"
    field_args = []
    if not is_required:
        field_args.append("default=None")
    if is_immutable:
        field_args.append("frozen=True")
    field_str = f'    {fname}: {py_type}'
    if field_args:
        field_str += f' = Field({", ".join(field_args)})'
    lines.append(field_str)


def generate_enum_class(enum_name: str, values: list[str]) -> str:
    lines = [f'\nclass {enum_name}(str, Enum):']
    for val in values:
        py_name = re.sub(r'[^a-zA-Z0-9_]', '', val.upper().replace(" ", "_").replace("-", "_").replace("/", "_"))
        if not py_name or py_name[0].isdigit():
            py_name = f"V_{py_name}"
        lines.append(f'    {py_name} = "{val}"')
    return '\n'.join(lines)


def generate_family_models(family: str, schemas: list[dict], all_schemas: dict) -> str:
    fam_title = FAMILY_TITLES.get(family, "Unknown")
    lines = [
        f'"""Family {family} — {fam_title}',
        'Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.',
        'Do not edit manually — regenerate via qad/generate_models.py',
        '"""',
        'from __future__ import annotations',
        'from enum import Enum',
        'from typing import Optional',
        'from pydantic import BaseModel, Field',
        '',
    ]
    all_enums = OrderedDict()
    for s in schemas:
        for e in s["enums"]:
            enum_name = f'{get_class_name(s["schema_id"], s["name"])}{e["field"].capitalize()}'
            if enum_name not in all_enums:
                all_enums[enum_name] = e["values"]
    for enum_name, values in all_enums.items():
        lines.append(generate_enum_class(enum_name, values))
    for s in schemas:
        class_name = get_class_name(s["schema_id"], s["name"])
        fds = s["field_descriptors"]
        lines.append('')
        lines.append('')
        lines.append(f'class {class_name}(BaseModel):')
        lines.append(f'    """{s["schema_id"]}: {s["name"]}. Frozen M4A canonical schema. Family {family}. """')
        lines.append(f'    model_config = {{"extra": "forbid"}}')
        lines.append('')
        lines.append(f'    schema_id: str = Field(default="{s["schema_id"]}", frozen=True)')
        for fname in sorted(s["required"]):
            if fname == "schema_id":
                continue
            fd = fds.get(fname, {})
            emit_field(lines, fname, fd, s, all_enums)
        for fname in sorted(s["optional"]):
            fd = fds.get(fname, {})
            emit_field(lines, fname, fd, s, all_enums)
        if s["fks"]:
            lines.append('')
            for fk in s["fks"]:
                card = "[]" if fk["cardinality"] == "list" else ""
                lines.append(f'    # FK: {fk["field"]}{card} -> {fk["target"]}.{fk["target_field"]}')
    return '\n'.join(lines)


def generate_contract_descriptor(schemas: dict[str, dict]) -> str:
    contracts = []
    for sid in sorted(schemas.keys()):
        s = schemas[sid]
        fields = []
        for fname in sorted(s["field_descriptors"].keys()):
            fd = s["field_descriptors"][fname]
            fields.append({
                "name": fname, "raw_name": fd["raw_name"],
                "container": fd["container"], "required": fd["required"],
                "enum_values": fd["enum_values"],
                "is_pit": fd["is_pit"], "is_provenance": fd["is_provenance"],
                "immutable": fd["immutable"], "immutable_policy": fd["immutable_policy"],
            })
        contracts.append({
            "schema_id": s["schema_id"], "name": s["name"], "family": s["family"],
            "required_fields": sorted(s["required"]), "optional_fields": sorted(s["optional"]),
            "fields": fields,
            "enums": [{"field": e["field"], "values": e["values"]} for e in s["enums"]],
            "fks": [{"field": fk["field"], "target": fk["target"],
                     "target_field": fk["target_field"], "cardinality": fk["cardinality"]}
                    for fk in s["fks"]],
            "pit_fields": sorted(s["pit_fields"]), "provenance_fields": sorted(s["provenance_fields"]),
            "is_canonical": s["is_canonical"], "canonical_boundary": s["canonical_boundary"],
            "immutability_rules": s["immutability_rules"],
        })
    return json.dumps({"schemas": contracts, "count": len(contracts)}, indent=2)


def generate_fk_registry(schemas: dict[str, dict]) -> str:
    lines = ['"""FK Registry (auto-generated from M4A parser)."""', '', 'FK_REGISTRY: dict[str, list[dict]] = {']
    for sid in sorted(schemas.keys()):
        s = schemas[sid]
        if not s["fks"]:
            continue
        lines.append(f'    "{sid}": [')
        for fk in s["fks"]:
            lines.append(f'        {{"field": "{fk["field"]}", "target": "{fk["target"]}", '
                         f'"target_field": "{fk["target_field"]}", '
                         f'"cardinality": "{fk["cardinality"]}"}},')
        lines.append('    ],')
    lines.append('}')
    fk_count = sum(len(s["fks"]) for s in schemas.values())
    lines.append(f'# Total FK references: {fk_count}')
    return '\n'.join(lines)


def generate_canonical_boundary(schemas: dict[str, dict]) -> str:
    canonical = [sid for sid, s in schemas.items() if s["is_canonical"]]
    non_canonical = [sid for sid, s in schemas.items() if not s["is_canonical"]]
    lines = ['"""Canonical Boundary (auto-generated from M4A parser)."""', '', '# Canonical schemas',
             'CANONICAL_SCHEMAS = {']
    for sid in sorted(canonical):
        lines.append(f'    "{sid}",')
    lines.append('}')
    lines.append('')
    lines.append('# Non-canonical schemas')
    lines.append('NON_CANONICAL_SCHEMAS = {')
    for sid in sorted(non_canonical):
        lines.append(f'    "{sid}",')
    lines.append('}')
    # Also add family index
    lines.append('')
    lines.append('# Family index (infrastructure = Family I)')
    lines.append('SCHEMA_FAMILIES = {')
    for sid in sorted(schemas.keys()):
        lines.append(f'    "{sid}": "{schemas[sid]["family"]}",')
    lines.append('}')
    lines.append('')
    lines.append('# Canonical boundary text (preserved exactly from M4A)')
    lines.append('CANONICAL_BOUNDARY_TEXT = {')
    for sid in sorted(schemas.keys()):
        cb = schemas[sid]["canonical_boundary"]
        # Escape for Python string
        cb_escaped = cb.replace('"', '\\"')
        lines.append(f'    "{sid}": "{cb_escaped}",')
    lines.append('}')
    return '\n'.join(lines)


def main():
    content = SCHEMAS_MD.read_text()
    source_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    generator_version = "M5.1-20260821"
    schemas = parse_all_schemas(content)
    print(f"Parsed {len(schemas)} schemas from M4A canonical registry (hash: {source_hash[:16]})")

    by_family = OrderedDict()
    for sid, s in schemas.items():
        by_family.setdefault(s["family"], []).append(s)
    for fam in by_family:
        by_family[fam].sort(key=lambda x: x["schema_id"])

    # Generate model files
    for fam in sorted(by_family.keys()):
        code = generate_family_models(fam, by_family[fam], schemas)
        (OUTPUT / f"family_{fam.lower()}.py").write_text(code)
        print(f"  Family {fam} — {len(by_family[fam])} schemas")

    # Generate __init__.py WITH SCHEMA_REGISTRY
    init_lines = [
        '"""QAD Runtime Schema Models — all 68 frozen M4A canonical schemas."""',
        'from __future__ import annotations', '',
    ]
    all_models = []
    for fam in sorted(by_family.keys()):
        init_lines.append(f'from qad.models.family_{fam.lower()} import (')
        for s in by_family[fam]:
            cn = get_class_name(s["schema_id"], s["name"])
            init_lines.append(f'    {cn},')
            all_models.append(cn)
        init_lines.append(')')
        init_lines.append('')
    init_lines.append('')
    init_lines.append('__all__ = [')
    for cn in sorted(set(all_models)):
        init_lines.append(f'    "{cn}",')
    init_lines.append(']')
    init_lines.append('')
    init_lines.append('')
    init_lines.append('# Schema registry: maps schema_id to model class (auto-generated)')
    init_lines.append('SCHEMA_REGISTRY: dict[str, type] = {')
    for sid in sorted(schemas.keys()):
        cn = get_class_name(schemas[sid]["schema_id"], schemas[sid]["name"])
        init_lines.append(f'    "{sid}": {cn},')
    init_lines.append('}')
    init_lines.append('')
    init_lines.append(f'# Build identity: spec_source = QAD-M4A-CANONICAL-SCHEMAS.md')
    init_lines.append(f'# spec_source_sha256 = {source_hash}')
    init_lines.append(f'# generator_version = {generator_version}')
    init_lines.append(f'# total_schemas = {len(schemas)}')
    (OUTPUT / "__init__.py").write_text('\n'.join(init_lines))

    # Generate contract artifacts
    (CONTRACT_DIR / "fk_registry.py").write_text(generate_fk_registry(schemas))
    (CONTRACT_DIR / "canonical_boundary.py").write_text(generate_canonical_boundary(schemas))

    descriptor = generate_contract_descriptor(schemas)
    (CONTRACT_DIR / "contract_descriptor.json").write_text(descriptor)

    fk_count = sum(len(s["fks"]) for s in schemas.values())
    canonical = sum(1 for s in schemas.values() if s["is_canonical"])
    enum_count = sum(len(s["enums"]) for s in schemas.values())
    print(f"\n  Source hash: {source_hash[:16]}")
    print(f"  FK references: {fk_count}")
    print(f"  Canonical: {canonical}, Non-canonical: {len(schemas) - canonical}")
    print(f"  Enum fields: {enum_count}")
    print("Done.")


if __name__ == "__main__":
    main()