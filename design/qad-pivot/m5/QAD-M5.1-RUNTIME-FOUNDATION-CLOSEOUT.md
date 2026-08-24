# QAD-M5.1 Runtime Foundation Closeout

> **Status:** M5.1 = FINAL / CONTRACT-CONFORMANT
> **Authority:** FD #135; M4A Canonical Schema Registry (FROZEN)
> **M5.1 Proof-Closure Baseline:** `2563614503b93325d94bd7fd6e89da44b0393ae7`
> **Proof-Closure Final Commit:** recorded by git history
>
> **Design principle:** All 68 frozen M4A schemas are materialized as
> Pydantic v2 models via a deterministic contract compiler.
> EVERYTHING derives from the ONE parsed representation of frozen M4A.

---

## 1. Contract Conformance

| Metric | Value | Method |
|---|---|---|
| Frozen schemas | 68 | M4A Canonical Schema Registry |
| Runtime models | 68 | Generated Pydantic v2 models |
| Required field match | 68/68 | Independent oracle vs runtime |
| Optional field match | 68/68 | Independent oracle vs runtime |
| No extra fields | 68/68 | Schema_id excluded |
| Collection shape match | 68/68 | `[]` → `list`, `{}` → `dict` |
| PIT field match | 68/68 | Per-schema PIT fields metadata |
| Provenance field match | 68/68 | Per-schema provenance fields metadata |
| PIT fields frozen | Verified | All PIT fields have `frozen=True` |
| Canonical boundary match | 68/68 | Per-schema `canonical_boundary` text preserved |
| Family I canonical | 9/9 | Family I not marked non-canonical |

---

## 2. Enum Coverage

| Metric | Value |
|---|---|
| Enum declarations parsed | 80 |
| FIELD_ENUM (matches field) | 68 |
| TYPE_ALIAS_ENUM (shared type) | 8 |
| CONTRACT_AMBIGUITY (documented) | 4 |
| Enum values match frozen | Verified per schema |
| Illegal enum rejected | Verified via negative test |
| Unused enum classes | 4 (all CONTRACT_AMBIGUITY) |

**TYPE_ALIAS_ENUM bindings (8):**
- CLM-01.claimant_type → `claimant`
- DR-01.broken_variable → `broken_variables[]`
- FF-01.metric_family → `metric_name`
- HYP-01.plausibility → `initial_plausibility`, `current_plausibility`
- IR-01.stop_rule → `stop_rule_triggered`
- MA-01.moat_type → `moat_types[]`
- MO-02.variance_type → `variance`
- PLA-01.risk_level → 6 permanent-loss risk dimensions

**CONTRACT_AMBIGUITY (4 — M4A declares enum with no matching field):**
- CCV-01.validation_result
- EAR-01.admission_method
- RB-01.budget_state
- RC-01.charter_state

No enum declaration is silently skipped. Every declaration is classified.

---

## 3. FK Coverage

| Metric | Value |
|---|---|
| FK references in frozen M4A | 87 |
| Runtime FK_REGISTRY | 87 |
| FK source fields exist | 87/87 |
| FK target schemas exist | 87/87 |
| FK target fields exist | 87/87 |
| No phantom FKs | Verified |
| No dropped FKs | Verified |
| Generator self-sufficient | Yes — SCHEMA_REGISTRY generated |

---

## 4. Self-Contained Generation

| Check | Result |
|---|---|
| Clean `rm models/` → regenerate | All 68 models + SCHEMA_REGISTRY + contract artifacts |
| Regeneration determinism | Byte-identical across ALL artifacts |
| Artifacts covered | models/*, contract/*.py, contract/contract_descriptor.json |
| Manual patch required | None — SCHEMA_REGISTRY in generated code |
| Build identity persisted | Machine-readable `SCHEMA_BUILD_IDENTITY` dict |
| `SCHEMA_REGISTRY` importable | 68 entries |
| `FK_REGISTRY` importable | 87 references |

---

## 5. Scalar Type Binding

| Check | Result |
|---|---|
| Policy vs runtime agreement | 100% — all 16 explicit scalar bindings verified |
| BU-01.amount_consumed | `float` ✅ |
| BU-01.cost | `Optional[float]` ✅ |
| BU-01.tokens | `Optional[int]` ✅ |
| MOD-01.prompt_tokens | `int` ✅ |
| MOD-01.completion_tokens | `int` ✅ |
| MOD-01.cost | `float` ✅ |
| PIE-01.current_price | `float` ✅ |
| PIE-01.implied_growth_rate | `float` ✅ |
| PIE-01.implied_terminal_value | `float` ✅ |
| RDCF-01.current_price | `float` ✅ |
| RDCF-01.implied_growth_rate | `float` ✅ |
| RDCF-01.implied_terminal_value | `float` ✅ |
| Container-shaped fields exempt (e.g. RRM-01.cost{}) | ✅ |

---

## 6. Immutability Classification

| Policy | Field Count |
|---|---|
| RECORD_IMMUTABLE | 251 |
| FIELD_IMMUTABLE | 125 |
| MUTABLE | 413 |
| CONDITIONAL / APPEND_ONLY | 54 |

**PITContext (PITC-01) — "Context immutable":** ALL fields frozen.
- `case_id` frozen ✅
- `created_by` frozen ✅
- `mode` frozen ✅
- `pit_context_id` frozen ✅
- `exception_reason` frozen (Optional) ✅
- `evidence_count_post` frozen (Optional) ✅
- `evidence_count_pre` frozen (Optional) ✅
- Mutation test verifies PITContext mutations fail ✅

---

## 7. Negative Tests

| Test | Result |
|---|---|
| Missing required field → FAIL | 68/68 schemas verified |
| Illegal enum value → FAIL | Verified |
| Scalar to list field → FAIL | Verified |
| Extra field → FAIL | Verified |
| Immutable field mutation → FAIL | Verified |
| Family I non-canonical → FAIL | Verified |
| Oracle source hash deterministic | Verified |
| PITContext mutation → FAIL | Verified |
| Scalar binding policy == runtime | 100% ✅ |
| Unused enum class detection | 4 documented CONTRACT_AMBIGUITY |
| All generated artifacts importable | ✅ |
| Runtime validator 68/68 | ✅ |

---

## 8. Runtime Validator

| Check | Result |
|---|---|
| `validate_contract()` per schema | 68/68 PASS |
| `validate_all_contracts()` | 68 per-schema PASS + 4 documented CONTRACT_AMBIGUITY |
| Build identity validation | PASS |
| negative test: PITContext mutation | PASS |
| negative test: scalar binding drift | PASS |
| negative test: FK integrity | PASS |

---

## 9. Verification Suite

| Check | Result |
|---|---|
| M4A structural validator | 173/173 PASS |
| FAKE-99 negative self-test | PASS |
| PIT leakage proof | 9/9 PASS |
| M4B validator | 93/93 PASS |
| Full contract conformance tests | 103/103 PASS |
| Runtime validator 68/68 | PASS |

---

## 10. Artifacts Produced

| Artifact | Path |
|---|---|
| Pydantic model files | `qad/models/family_{a-i}.py` |
| Schema registry | `qad/models/__init__.py` (SCHEMA_REGISTRY + SCHEMA_BUILD_IDENTITY) |
| FK registry | `qad/contract/fk_registry.py` |
| Canonical boundary | `qad/contract/canonical_boundary.py` |
| Contract descriptor | `qad/contract/contract_descriptor.json` |
| Schema registry shim | `qad/schema_registry.py` |
| Type binding policy | `design/qad-pivot/m5/QAD-M5.1-TYPE-BINDING-POLICY.md` |
| Independent test oracle | `tests/qad/independent_oracle.py` |
| Contract conformance tests | `tests/qad/test_contract_conformance.py` |
| Runtime validator | `qad/validator.py` |
| This closeout | `design/qad-pivot/m5/QAD-M5.1-RUNTIME-FOUNDATION-CLOSEOUT.md` |

---

## 11. Gates

```
M5.1 = FINAL / CONTRACT-CONFORMANT
M5.2 = PROCEED UNDER FD #135
Production Release = NOT AUTHORIZED
```

<!-- 2026-08-24 -->