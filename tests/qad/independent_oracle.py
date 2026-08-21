"""M5.1 — Independent Contract Oracle.
Parses QAD-M4A-CANONICAL-SCHEMAS.md using test-only logic that does NOT
import qad.generate_models, production parser functions, or generated artifacts.
This is the genuinely independent reference for contract conformance tests.
"""
import hashlib
import re
from pathlib import Path
from collections import OrderedDict

BASE = Path(__file__).resolve().parent.parent.parent
SCHEMAS_MD = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"


def get_field(block: str, label: str) -> str:
    m = re.search(rf'\| \*\*{re.escape(label)}\*\* \| (.+?) \|', block, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


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


def parse_schema_block(block: str, family: str) -> dict | None:
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

    pit_raw = get_field(block, "PIT fields")
    pit_fields = set()
    if pit_raw:
        pit_fields = {f.strip() for f in re.findall(r'`([^`]+)`', pit_raw)}

    prov_raw = get_field(block, "provenance fields")
    prov_fields = set()
    if prov_raw:
        prov_fields = {f.strip() for f in re.findall(r'`([^`]+)`', prov_raw)}

    # PIT/provenance-only fields added to expected surface
    for pf in pit_fields | prov_fields:
        pf_clean, _ = parse_field_shape(pf)
        if pf_clean and pf_clean not in required and pf_clean not in optional:
            optional.add(pf_clean)

    expected_surface = required | optional

    # Field shapes
    field_shapes = {}
    if required_raw:
        for f in re.findall(r'`([^`]+)`', required_raw):
            clean, container = parse_field_shape(f)
            if clean:
                field_shapes[clean] = container
    if optional_raw:
        for f in re.findall(r'`([^`]+)`', optional_raw):
            clean, container = parse_field_shape(f)
            if clean:
                field_shapes[clean] = container
    # PIT/provenance-only fields (scalar by default)
    for pf in pit_fields | prov_fields:
        pf_clean, container = parse_field_shape(pf)
        if pf_clean and pf_clean not in field_shapes:
            field_shapes[pf_clean] = container

    enums = parse_enum_rows(block)
    fks = parse_fk_rows(block)

    cb = get_field(block, "canonical_boundary")
    is_canonical = cb.lower().startswith("canonical") or (
        "canonical" in cb.lower() and "noncanonical" not in cb.lower())
    if schema_id == "PUB-01":
        is_canonical = True

    return {
        "schema_id": schema_id, "name": name, "family": family,
        "required": required, "optional": optional,
        "expected_surface": expected_surface,
        "field_shapes": field_shapes,
        "enums": enums, "fks": fks,
        "pit_fields": pit_fields, "provenance_fields": prov_fields,
        "is_canonical": is_canonical, "canonical_boundary": cb,
    }


def parse_all() -> dict[str, dict]:
    """Parse all schemas from M4A markdown. Returns dict[schema_id] = descriptor."""
    content = SCHEMAS_MD.read_text()
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


ORACLE = parse_all()
ORACLE_SOURCE_HASH = hashlib.sha256(SCHEMAS_MD.read_bytes()).hexdigest()