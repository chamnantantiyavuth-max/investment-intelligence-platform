# QAD-M5.1 Implementation Type Binding Policy

> **Status:** NEW_M5_IMPLEMENTATION_DERIVATION
> **Authority:** FD #135; M4A Canonical Schema Registry (FROZEN)
> **Date:** 2026-08-21
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
| enum in schema's `enums` row | `class FooEnum(str, Enum)` | `FIELD_ENUM` — matches a field name |
| enum in continuation row, not a field name | `class TypeAlias(str, Enum)` | `TYPE_ALIAS_ENUM` — used by multiple fields |

**Rule:** Every M4A enum declaration produces a Python `str, Enum` class. Enum values in runtime MUST exactly match the frozen M4A set. Illegal enum values cause Pydantic validation failure.

**Known TYPE_ALIAS_ENUMs:**
- `plausibility` (HYP-01) — used by `initial_plausibility`, `current_plausibility`

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

---

## 4. Immutability Binding

| M4A Classification | Python Enforcement | Description |
|---|---|---|
| `FIELD_IMMUTABLE` | `Field(frozen=True)` | Individual field cannot be mutated after creation |
| `RECORD_IMMUTABLE` | Model-level convention | Record content is immutable; requires new record for changes |
| `APPEND_ONLY` | Not enforced in M5.1 | State transitions require new version, not mutation |
| `MUTABLE` | No enforcement | Field may be freely updated |

**PIT fields** are always `FIELD_IMMUTABLE` (point-in-time data cannot change).

---

## 5. Provenance / PIT Field Binding

Provenance and PIT fields are derived from the frozen M4A `provenance fields` and `PIT fields` rows. They are:

1. Added to the schema's expected surface (as optional unless also declared required)
2. Marked with `is_pit` / `is_provenance` metadata
3. PIT fields have `frozen=True`

**Not implemented in M5.1:** Runtime enforcement of `retrieval_timestamp` > `as_of_date` or similar cross-field validation rules.

---

## 6. Unresolved Scalar Bindings

The following fields have ambiguous scalar types that cannot be safely determined from the M4A notation alone. They are bound as `str` in M5.1 pending domain implementation:

| Schema | Field | Issue |
|---|---|---|
| Various | `data_version` | Could be `str` or `int` |
| Various | `rule_version` | Could be `str` or `int` |
| Various | `model_version` | Could be `str` or `int` |

These are conservative bindings. Revisit when the domain implementation selects a specific versioning scheme.

---

## 7. Generator Build Identity

Every generated `__init__.py` contains:

```python
# spec_source = QAD-M4A-CANONICAL-SCHEMAS.md
# spec_source_sha256 = <sha256 of frozen M4A markdown>
# generator_version = M5.1-20260821
# total_schemas = 68
```

This enables deterministic verification of the build artifact against the frozen specification.

<!-- 2026-08-21 -->