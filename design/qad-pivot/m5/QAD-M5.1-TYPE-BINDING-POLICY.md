# QAD-M5.1 Implementation Type Binding Policy

> **Status:** SYNCED / CURRENT (Erratum 001 applied, FD #136)
> **Authority:** FD #135 + FD #136; M4A Canonical Schema Registry (FROZEN + Erratum 001)
> **Date:** 2026-08-24
>
> **Purpose:** Document all technology binding decisions made when translating
> technology-neutral M4A schema notation into Python runtime types. This is
> NOT investment methodology. These bindings are implementation choices that
> may be revisited if the production stack changes.

---

## 1. Collection Shape Binding

| M4A Notation | Python Type | Rationale |
|---|---|---|
| `field[]` | `list[T]` | Frozen M4A explicitly uses `[]` for ordered collections |
| `field{}` | `dict` | Frozen M4A uses `{}` for key-value mappings |
| `field{key: value}` | `dict` | The type annotation is advisory; Python dict covers all cases |
| `field{key: value[]}` | `dict` | Same as above |

**Rule:** A field with `[]` notation MUST be `list` in runtime. A field with `{}` notation MUST be `dict`. No scalar fallback.

---

## 2. Enum Binding

| M4A Declaration | Python Binding | Classification |
|---|---|---|
| enum in schema's `enums` row, matches a field name | `class FooEnum(str, Enum)` | `FIELD_ENUM` |
| enum in continuation row, not a field name, used by multiple fields | `class TypeAlias(str, Enum)` | `TYPE_ALIAS_ENUM` (explicitly mapped in generator) |

**Rule:** Every M4A enum declaration produces a Python `str, Enum` class. Enum values in runtime MUST exactly match the frozen M4A set. Illegal enum values cause Pydantic validation failure.

### CONTRACT_AMBIGUITY Resolution

After **QAD-M4A-SCHEMA-ERRATUM-001 / FD #136** (24 Aug 2026), all four formerly-ambiguous enums are now `FIELD_ENUM`:

```text
EAR-01.admission_method  → EvidenceAdmissionRecordAdmission_method (FIELD_ENUM)
RC-01.charter_state      → ResearchCharterCharter_state           (FIELD_ENUM)
RB-01.budget_state       → ResearchBudgetRecordBudget_state       (FIELD_ENUM)
CCV-01.validation_result → CrossCaseValidationValidation_result   (FIELD_ENUM)
```

**CONTRACT_AMBIGUITY = 0** and **unused enum classes = 0**.

### All 8 TYPE_ALIAS_ENUM mappings

| Schema | Declaration Field | Bound Runtime Fields |
|---|---|---|
| CLM-01 | `claimant_type` | `claimant` |
| DR-01 | `broken_variable` | `broken_variables[]` |
| FF-01 | `metric_family` | `metric_name` |
| HYP-01 | `plausibility` | `initial_plausibility`, `current_plausibility` |
| IR-01 | `stop_rule` | `stop_rule_triggered` |
| MA-01 | `moat_type` | `moat_types[]` |
| MO-02 | `variance_type` | `variance` |
| PLA-01 | `risk_level` | 6 permanent-loss risk dimensions |

---

## 3. Scalar Type Binding

| M4A Concept | Python Type | Rule |
|---|---|---|
| String identifiers | `str` | All IDs, tickers, CIKs, names |
| ISO dates / timestamps | `str` (ISO format) | Stable, language-agnostic. No datetime coercion in M5.1 |
| Boolean flags | `bool` | Fields ending in `_flag`, starting with `is_` or `has_` |
| Count / token fields | `int` | `count`, `tokens`, `retry_count`, `max_retries`, `duration_ms` |
| Monetary / value fields | `float` | `cost`, `price`, `value`, `amount`, `estimate` |
| Percentage / ratio fields | `float` | `rate`, `ratio`, `margin`, `threshold` |
| UUID identifiers | `str` | M4A specifies UUID v7 but Python binding is `str` (validated at persistence layer) |
| Unspecified scalar | `str` | Conservative default. Must be explicitly documented in this policy |

### Explicit ScaleBinding Map (field-level overrides)

The generator consumes `SCALAR_BINDING_MAP` — one machine-readable map that
reconciles policy with runtime. Current entries:

| Field | Type | Schemas |
|---|---|---|
| `amount_consumed` | `float` | BU-01 |
| `cost` | `float` | BU-01, MOD-01, PROV-01 |
| `tokens` | `int` | BU-01 |
| `prompt_tokens` | `int` | MOD-01 |
| `completion_tokens` | `int` | MOD-01 |
| `current_price` | `float` | PIE-01, RDCF-01 |
| `implied_growth_rate` | `float` | PIE-01, RDCF-01 |
| `implied_terminal_value` | `float` | PIE-01, RDCF-01 |
| `asymmetry_estimate` | `float` | VA-01 |
| `damage_gap` | `float` | VA-01 |
| `economic_damage` | `float` | VA-01 |
| `price_damage` | `float` | VA-01 |
| `intrinsic_value_estimate` | `float` | SCEN-01 |
| `recovery_rate_implied` | `float` | PIE-01, RDCF-01 |
| `recovery_capital_needed` | `float` | PLA-01 |
| `probability_weight` | `float` | SCEN-01 |

Fields with `[]`/`{}` container shapes are exempt (collection shape wins over scalar binding) — e.g. `RRM-01.cost` is dict-typed.

**Policy == runtime** verified by test `test_scalar_binding_policy_matches_runtime()`.

---

## 4. Immutability Binding

| M4A Classification | Python Enforcement | Description |
|---|---|---|
| `RECORD_IMMUTABLE` | Per-field `Field(frozen=True)` on all fields | "Record immutable" or "Context immutable" → whole surface frozen |
| `FIELD_IMMUTABLE` | `Field(frozen=True)` | Individual field cannot be mutated after creation |
| `APPEND_ONLY` | Not enforced in M5.1 | State transitions require new version, not mutation |
| `APPEND_ONLY_STATE` | Not enforced in M5.1 | State transitions append-only (M5.2 persistence/state layer) |
| `MUTABLE` | No enforcement | Field may be freely updated |

**PIT fields** are always `FIELD_IMMUTABLE` (point-in-time data cannot change).

**PITContext (PITC-01):** "Context immutable" → `RECORD_IMMUTABLE`. All PITContext fields frozen (`case_id`, `created_by`, `mode`, `pit_context_id`, `exception_reason`, `evidence_count_post`, `evidence_count_pre`). Mutation test verifies failure.

**Conditional rules** (e.g. "manifest immutable after completion") are classified `CONDITIONAL_IMMUTABLE` with runtime enforcement owned by the M5.2 persistence/state layer — not unconditionally frozen in M5.1.

---

## 5. Provenance / PIT Field Binding

Provenance and PIT fields are derived from the frozen M4A `provenance fields` and `PIT fields` rows. They are:

1. Added to the schema's expected surface (as optional unless also declared required)
2. Marked with `is_pit` / `is_provenance` metadata
3. PIT fields have `frozen=True`

**Not implemented in M5.1:** Runtime enforcement of `retrieval_timestamp` > `as_of_date` or similar cross-field validation rules.

---

## 6. Build Identity

Every generated `__init__.py` contains a machine-readable `SCHEMA_BUILD_IDENTITY` dict:

```python
SCHEMA_BUILD_IDENTITY = {
    "spec_source": "QAD-M4A-CANONICAL-SCHEMAS.md",
    "spec_source_sha256": "<sha256 of frozen M4A markdown>",
    "m4a_contract_version": "M4A-FROZEN-20260821",
    "generator_version": "M5.1-20260824",
    "total_schemas": 68,
    "total_models": 68,
    "generated_artifact_hashes": {
        "models/family_a.py": "sha256...",
        ...,
        "contract/fk_registry.py": "sha256...",
        "contract/canonical_boundary.py": "sha256...",
        "contract/contract_descriptor.json": "sha256...",
    },
}
```

### Artifact Hash Policy

`generated_artifact_hashes` covers all non-self-referential compiler outputs:

- `models/family_a.py` … `models/family_i.py`
- `contract/fk_registry.py`
- `contract/canonical_boundary.py`
- `contract/contract_descriptor.json`

**Exclusion rule:** `models/__init__.py` is excluded because it contains the
`SCHEMA_BUILD_IDENTITY` manifest including these hashes — including it would be
self-referential (its own hash would change the file, changing its hash).
All other generated files are hashed directly.

Runtime validator verifies `generated_artifact_hashes` matches actual on-disk
byte hashes, detecting any manual/undocumented artifact drift.

---

## 7. Runtime Validator Scope

`qad/validator.py` implements full contract validation (not claim-only):

- exact runtime field surface (`required`/`optional`/PIT/provenance derived)
- `extra=forbid`
- schema_id present + frozen
- enum declaration → runtime binding (no unbound enum)
- enum value equality vs M4A
- list/dict collection shape
- PIT field frozen
- provenance field present
- immutability descriptor
- FK source/target validity (source field, target schema, target field)
- FK set parity (runtime == descriptor)
- canonical boundary
- family
- scalar type binding
- build identity + generated artifact hashes

`validate_all_contracts()` returns 68/68 PASS with **0 global violations** after Erratum 001.

---

## 8. Unresolved Scalar Bindings

The following fields have ambiguous scalar types that cannot be safely determined
from the M4A notation alone. They are bound as `str` in M5.1 pending domain implementation:

| Schema | Field | Issue |
|---|---|---|
| Various | `data_version` | Could be `str` or `int` |
| Various | `rule_version` | Could be `str` or `int` |
| Various | `model_version` | Could be `str` or `int` |

These are conservative bindings. Revisit when the domain implementation selects a specific versioning scheme.

<!-- 2026-08-24 -->