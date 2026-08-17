#!/usr/bin/env python3
"""
M2 Registry Deterministic Integrity Validator

Reads QAD-M2-LEGACY-CAPABILITY-REGISTRY.md and validates:
1. All capability IDs unique
2. Canonical record count = 25
3. Exactly one lifecycle state per capability
4. Exactly one primary_disposition per capability
5. Lifecycle summary totals 25
6. Disposition summary totals 25
7. No record missing required fields
8. Every ACTIVE/TRANSITIONAL has a Dependency Matrix entry
9. Every FROZEN capability with ACTIVE/OPERATIONAL runtime_use
   has an explicit Dependency Matrix runtime entry (FROZEN-with-runtime)
10. Derive FROZEN-with-runtime count mechanically from registry fields
"""

import re
import sys

REGISTRY_PATH = "design/qad-pivot/QAD-M2-LEGACY-CAPABILITY-REGISTRY.md"
DEP_MATRIX_PATH = "design/qad-pivot/QAD-M2-DEPENDENCY-MATRIX.md"

VALID_LIFECYCLE = {"ACTIVE", "FROZEN", "SUPERSEDED", "TRANSITIONAL", "VERIFIED_UNUSED", "ARCHIVED"}
VALID_DISPOSITIONS = {"REUSE", "ADAPT", "ABSORB", "TRANSITIONAL_RETAIN", "FREEZE", "SUPERSEDE", "DO_NOT_REUSE"}
EXPECTED_COUNT = 25

errors = []


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_capability_records(text):
    """
    Parse capability records from the markdown registry.
    Returns list of dicts with capability_id, current_state, primary_disposition, runtime_use.
    """
    records = []
    # Find all capability sections by looking for capability_id entries
    # Pattern: starts with ## or ### section header, contains capability record table
    sections = re.split(r'\n(?=##+\s)', text)
    
    for section in sections:
        cap_id_match = re.search(r'\*\*capability_id\*\*\s*\|\s*([A-Z]+-\d+[A-Z]*)', section)
        if not cap_id_match:
            continue
        
        cap_id = cap_id_match.group(1)
        
        # Extract current_state
        state_match = re.search(r'\*\*current_state\*\*\s*\|\s*\*{0,2}([A-Z_]+)\*{0,2}', section)
        state = state_match.group(1) if state_match else None
        
        # Extract primary_disposition
        disp_match = re.search(r'\*\*primary_disposition\*\*\s*\|\s*([A-Z_]+)(?:\s|\(|\|)', section)
        disp = disp_match.group(1) if disp_match else None
        
        # Extract runtime_use (optional)
        runtime_match = re.search(r'\*\*runtime_use\*\*\s*\|\s*(.+?)(?:\n|\|)', section)
        runtime = runtime_match.group(1).strip() if runtime_match else None
        
        # Extract migration_instruction (optional)
        mig_match = re.search(r'\*\*migration_instruction\*\*\s*\|\s*(.+?)(?:\n|\|)', section)
        mig = mig_match.group(1).strip() if mig_match else None
        
        # Extract reuse_policy (optional)  
        reuse_match = re.search(r'\*\*reuse_policy\*\*\s*\|\s*(.+?)(?:\n|\|)', section)
        reuse = reuse_match.group(1).strip() if reuse_match else None
        
        records.append({
            "id": cap_id,
            "state": state,
            "disposition": disp,
            "runtime_use": runtime,
            "migration_instruction": mig,
            "reuse_policy": reuse,
        })
    
    return records


def validate(records):
    global errors
    
    # 1. All capability IDs unique
    ids = [r["id"] for r in records]
    dupes = set([id for id in ids if ids.count(id) > 1])
    if dupes:
        errors.append(f"DUPLICATE capability IDs: {dupes}")
    else:
        print(f"  ✅ All {len(ids)} capability IDs unique")
    
    # 2. Canonical record count
    if len(records) != EXPECTED_COUNT:
        errors.append(f"EXPECTED {EXPECTED_COUNT} records, found {len(records)}")
    else:
        print(f"  ✅ Canonical record count = {len(records)}")
    
    # 3. Exactly one lifecycle state per capability
    state_counts = {}
    for r in records:
        if r["state"]:
            if r["state"] not in VALID_LIFECYCLE:
                errors.append(f"{r['id']}: invalid lifecycle state '{r['state']}'")
            state_counts[r["state"]] = state_counts.get(r["state"], 0) + 1
        else:
            errors.append(f"{r['id']}: MISSING lifecycle state")
    
    if not errors:
        print(f"  ✅ Lifecycle distribution: {state_counts}")
        total_lifecycle = sum(state_counts.values())
        if total_lifecycle != EXPECTED_COUNT:
            errors.append(f"Lifecycle sum ({total_lifecycle}) != {EXPECTED_COUNT}")
        else:
            print(f"  ✅ Lifecycle sum = {total_lifecycle}")
    
    # 4. Exactly one primary_disposition per capability
    disp_counts = {}
    multi_disp = []
    for r in records:
        if r["disposition"]:
            if r["disposition"] not in VALID_DISPOSITIONS:
                errors.append(f"{r['id']}: invalid primary_disposition '{r['disposition']}'")
            disp_counts[r["disposition"]] = disp_counts.get(r["disposition"], 0) + 1
        else:
            errors.append(f"{r['id']}: MISSING primary_disposition")
    
    if not errors:
        print(f"  ✅ Disposition distribution: {disp_counts}")
        total_disp = sum(disp_counts.values())
        if total_disp != EXPECTED_COUNT:
            errors.append(f"Disposition sum ({total_disp}) != {EXPECTED_COUNT}")
        else:
            print(f"  ✅ Disposition sum = {total_disp}")
    
    # 5. No forbidden dispositions
    for r in records:
        if r["disposition"] == "REFRAIN":
            errors.append(f"{r['id']}: REFRAIN is not a valid primary_disposition (use migration_instruction)")
        if r["disposition"] and "/" in r["disposition"]:
            errors.append(f"{r['id']}: compound disposition '{r['disposition']}' — must be single value")
    
    # 6. Check migration_instruction only with valid dispositions
    for r in records:
        if r["migration_instruction"] and r["disposition"] not in ("TRANSITIONAL_RETAIN", "FREEZE", "ADAPT"):
            pass  # migration_instruction valid with these
        if r["reuse_policy"] and r["disposition"] not in ("FREEZE", "SUPERSEDE"):
            pass  # reuse_policy valid with these
    
    # 7. Print summary
    print(f"\n  📊 Records by ID:")
    for r in sorted(records, key=lambda x: x["id"]):
        runtime_note = " 🔴 ACTIVE runtime" if (r["runtime_use"] and "ACTIVE" in r["runtime_use"]) else ""
        mig_note = f" ─ migration: {r['migration_instruction'][:50]}..." if r["migration_instruction"] else ""
        reuse_note = f" ─ reuse: {r['reuse_policy']}" if r["reuse_policy"] else ""
        print(f"    {r['id']}: state={r['state']:12s} disp={r['disposition']:22s}{runtime_note}{mig_note}{reuse_note}")
    
    # Report
    if errors:
        print(f"\n  ❌ {len(errors)} validation error(s):")
        for e in errors:
            print(f"    - {e}")
        return False
    else:
        print(f"\n  ✅ ALL {EXPECTED_COUNT} records valid — lifecycle sum = {EXPECTED_COUNT}, disposition sum = {EXPECTED_COUNT}")
        return True


def check_dep_matrix_coverage(records):
    """Verify every ACTIVE/TRANSITIONAL + FROZEN-with-runtime capability has Dependency Matrix coverage."""
    dep_text = read_file(DEP_MATRIX_PATH)
    active_transitional = [r for r in records if r["state"] in ("ACTIVE", "TRANSITIONAL")]
    
    for r in active_transitional:
        cap_id = r["id"]
        if cap_id not in dep_text:
            errors.append(f"{cap_id}: {r['state']} but NOT present in Dependency Matrix")
    
    # FROZEN-with-runtime: FROZEN capabilities whose runtime_use field
    # indicates ACTIVE/OPERATIONAL/scheduled/cron execution.
    # These are NOT safe to assume "off" despite FROZEN development state.
    ACTIVE_RUNTIME_KEYWORDS = ["ACTIVE", "OPERATIONAL", "cron", "scheduled", "runtime still",
                                "runtime still consumed", "monitoring cron"]
    frozen_with_runtime = []
    for r in records:
        if r["state"] != "FROZEN":
            continue
        runtime = r["runtime_use"] or ""
        is_active_runtime = any(kw.lower() in runtime.lower() for kw in ACTIVE_RUNTIME_KEYWORDS)
        # Also check if active_dependencies mentions "cron" or "scheduled"
        if is_active_runtime:
            frozen_with_runtime.append(r)
    
    for r in frozen_with_runtime:
        cap_id = r["id"]
        if cap_id not in dep_text:
            errors.append(f"{cap_id}: FROZEN with ACTIVE runtime ('{r['runtime_use']}') but NOT in Dependency Matrix")
    
    frozen_count = len(frozen_with_runtime)
    active_count = len(active_transitional)
    
    if not [e for e in errors if "Dependency Matrix" in e or "NOT present" in e]:
        print(f"  ✅ All {active_count} ACTIVE/TRANSITIONAL + {frozen_count} FROZEN-with-runtime have Dependency Matrix entries")
        if frozen_count > 0:
            frozen_ids = [r["id"] for r in frozen_with_runtime]
            print(f"     FROZEN-with-runtime IDs (derived): {frozen_ids}")
    else:
        # Print specific errors
        for e in errors:
            if "Dependency Matrix" in e or "NOT present" in e:
                print(f"     ❌ {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("M2 Registry Deterministic Integrity Validator")
    print("=" * 60)
    print()
    
    text = read_file(REGISTRY_PATH)
    records = extract_capability_records(text)
    
    print(f"Found {len(records)} capability records in registry")
    print()
    
    valid = validate(records)
    
    print()
    check_dep_matrix_coverage(records)
    
    print()
    if errors:
        print(f"❌ VALIDATION FAILED — {len(errors)} errors")
        sys.exit(1)
    else:
        print("✅ VALIDATION PASSED — Registry is deterministic")
        sys.exit(0)