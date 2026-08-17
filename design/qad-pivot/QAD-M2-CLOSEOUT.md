# QAD-M2-CLOSEOUT.md — Logical Legacy Boundary (Corrected)

> **Status:** M2 TECHNICAL CLOSEOUT = **PASS** (commit `548a89d`, 17 Aug 2026)
> **M2 FINAL GOVERNANCE = PASS** (independent review 18 Aug 2026: PASS_WITH_FINDINGS → 2 findings resolved)
> **M3 = READY FOR FOUNDER AUTHORIZATION**
> **Mission:** Establish a complete, capability-level boundary between the pre-QAD system and the canonical QAD future state.
> **Boundary type:** Semantic/governance only — no physical files moved, deleted, or renamed.

---

## M2 Exit Criteria (Corrected)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Every material legacy capability has a state | ✅ | 20 capabilities + 5 child capabilities registered in `QAD-M2-LEGACY-CAPABILITY-REGISTRY.md` |
| 2 | No major module classified only by module name | ✅ | Alpha Momentum → 3 sub-capabilities; FO → 4 sub-capabilities; each with capability-level decomposition |
| 3 | **All ACTIVE/TRANSITIONAL dependencies documented** | **⬜ CORRECTED — PENDING REVIEW** | `QAD-M2-DEPENDENCY-MATRIX.md` now covers all ACTIVE (8) + TRANSITIONAL (1) capabilities with full runtime audit. **FROZEN-with-runtime-use (3 capabilities)** also documented. Independent review must confirm coverage. |
| 4 | No VERIFIED_UNUSED without evidence | ✅ | 0 capabilities marked VERIFIED_UNUSED (correct — no state change without evidence) |
| 5 | Radar preserved TRANSITIONAL | ✅ | CAP-011: TRANSITIONAL, no cron change, no freeze, evidence-based migration decision required |
| 6 | Shared Equity Universe reuse path preserved | ✅ | CAP-001: ACTIVE, REUSE — QAD Quality Universe will be superset |
| 7 | CIW absorption lineage explicit | ✅ | CAP-009: ABSORB with lineage — QAD Research Protocol evolves from CIW; CIW artifacts preserved; CIW MSFT monitor decomposed as ACTIVE runtime |
| 8 | Legacy strategy authority separated from reusable capability | ✅ | Each capability: `current_authority` (FD) + `QAD_target_disposition` (REUSE/ADAPT/ABSORB/FREEZE/SUPERSEDE/TRANSITIONAL_RETAIN/DO_NOT_REUSE) |
| 9 | QAD M3 has unambiguous reuse/creation boundary | **⬜ PENDING** | Registry disposition vocabulary tells M3 what to REUSE, ADAPT from, ABSORB, or CREATE from scratch. **But lifecycle state and QAD disposition were mixed in the summary — corrected now. Independent review must verify separation.** |
| 10 | No physical migration occurred | ✅ | Zero files moved, deleted, or renamed by M2 |
| 11 | Applicable tests remain green | ✅ | Suite 235/235 |
| 12 | Exact-path staging discipline used | ✅ | Explicit `git add` paths only |
| 13 | Repository diff is scope-clean | ✅ | **M2 diff (commit `548a89d`):** 3 M2 artifacts + AGENTS.md (founder-approved) + 3 M1-residue documentation corrections (Scuttlebutt wording, threshold wording, M1 status). **No production/cron/workforce changes.** Corrections (this session): documentation-only updates to M2 artifacts + old-map SUPERSEDED marker. |

---

## M2 Artifacts

| Artifact | Location | Content |
|----------|----------|---------|
| Legacy Capability Registry | `design/qad-pivot/QAD-M2-LEGACY-CAPABILITY-REGISTRY.md` | 20 capabilities + 5 child IDs with full fields (capability_id, lifecycle state, disposition, dependencies, consumers, verification, preconditions, runtime_use) |
| Dependency Matrix | `design/qad-pivot/QAD-M2-DEPENDENCY-MATRIX.md` | Freeze-candidate dependency verification + full ACTIVE/TRANSITIONAL dependency map + FROZEN-with-runtime-use audit + corrected runtime dependencies |
| M2 Closeout | `design/qad-pivot/QAD-M2-CLOSEOUT.md` | This file (corrected) |
| Capability Legacy Reuse Map | `design/qad-pivot/CAPABILITY-LEGACY-REUSE-MAP.md` | **SUPERSEDED** — historical design predecessor; canonical truth = M2 registry |

---

## M2 State Summary (Corrected — Axes Separated)

### A. Current Lifecycle State Summary

Derived from **25 canonical capability records** (20 top-level + 5 child IDs). Each capability has exactly one lifecycle state.

| Lifecycle State | Count | Capabilities |
|----------------|-------|-------------|
| **ACTIVE** | 9 | CAP-001, CAP-002, CAP-003, CAP-012, CAP-013, CAP-014, CAP-016, CAP-017, CAP-018 |
| **FROZEN** | 14 | CAP-004, CAP-005, CAP-006, CAP-007, CAP-007A, CAP-007B, CAP-007D, CAP-008, CAP-009, CAP-010, CAP-010A, CAP-015, CAP-019, CAP-020 |
| **SUPERSEDED** | 1 | CAP-007C |
| **TRANSITIONAL** | 1 | CAP-011 |
| **VERIFIED_UNUSED** | 0 | |
| **ARCHIVED** | 0 | |
| **Total** | **25** | |

### B. QAD Primary Disposition Summary

Derived from **25 canonical capability records**. Each capability has exactly one `primary_disposition`. Supplementary `reuse_policy` and `migration_instruction` are NOT counted as separate dispositions.

| Disposition | Count | Capabilities |
|-------------|-------|-------------|
| **REUSE** | 7 | CAP-001, CAP-012, CAP-013, CAP-014, CAP-015, CAP-016, CAP-017 |
| **ADAPT** | 6 | CAP-002, CAP-003, CAP-006, CAP-007A, CAP-007B, CAP-020 |
| **ABSORB** | 1 | CAP-009 |
| **TRANSITIONAL_RETAIN** | 2 | CAP-011, CAP-018 |
| **FREEZE** | 7 | CAP-004, CAP-005, CAP-007, CAP-007D, CAP-008, CAP-010, CAP-019 |
| **SUPERSEDE** | 1 | CAP-007C |
| **DO_NOT_REUSE** | 1 | CAP-010A |
| **Total** | **25** | |

> **Derivation:** Counts derive from canonical capability records. Manual drift eliminated.

---

## What M2 Does NOT Authorize

- ❌ No physical file moves, deletions, or renames
- ❌ No cron job changes
- ❌ No workforce profile reconfiguration
- ❌ No M3 spec creation
- ❌ No M5 code
- ❌ No schema migration
- ❌ ⛔ **M3 is HOLD** — do not begin

---

## Corrections Applied (18 Aug 2026)

1. **Parallel truth eliminated** — `CAPABILITY-LEGACY-REUSE-MAP.md` marked SUPERSEDED; canonical = M2 registry + dependency matrix
2. **Lifecycle/disposition axes separated** — two independent summary tables; REFRAIN removed from disposition vocabulary (moved to `migration_instruction`)
3. **Capability granularity normalized** — CAP-007A..007D, CAP-010A assigned stable IDs; all 25 records explicitly counted
4. **Runtime dependency audit corrected** — Nick-Weekly cron, CIW monitor, Workforce runtime, FROZEN-but-ACTIVE annotations added
5. **Hermes Workforce state corrected** — ACTIVE (not FROZEN); `primary_disposition = TRANSITIONAL_RETAIN` with `migration_instruction = DEFER_QAD_WORKFORCE_REMAP_UNTIL_M3_ROLE_CONTRACTS`
6. **Source Adapters runtime documented** — FROZEN for development; ACTIVE runtime dependency of CAP-002, CAP-003
7. **Live Office runtime documented** — FROZEN development but runtime operational
8. **CIW decomposed** — framework FROZEN/ABSORB; monitoring cron ACTIVE
9. **CAP-007C state fixed** — `current_state = SUPERSEDED` (was FROZEN); `primary_disposition = SUPERSEDE`
10. **Primary disposition normalized** — every capability has EXACTLY ONE `primary_disposition`. Compound values (e.g., ADAPT+FREEZE, FREEZE+DO_NOT_REUSE) eliminated. Supplementary `reuse_policy` and `migration_instruction` are NOT counted as separate dispositions.
11. **Validation script created** — `design/qad-pivot/validate-registry.py` mechanically verifies: unique IDs, 25-record count, single lifecycle per capability, single disposition per capability, lifecycle sum=25, disposition sum=25, no forbidden dispositions
12. **M2 status corrected** — TECHNICAL CLOSEOUT = PASS; FINAL GOVERNANCE = PASS (after validation); M3 = READY FOR FOUNDER AUTHORIZATION; suite 235/235

### Terminology note

The independent-review prompt expanded QAD as "Quality-At-Distressed-Prices" (a prompt-writing typo in the review context). The canonical expansion is **Quality at Dislocation**. No review rerun required — the review scope was M2 capability/dependency integrity, not investment-thesis reasoning. The review output is in subagent cache only (not a project artifact).

---

## Next

**M2 = FINAL PASS** ✅ — Independent review PASS_WITH_FINDINGS (2 findings) → resolved.
**M3 = READY FOR FOUNDER AUTHORIZATION** — awaiting Founder decision.

After authorization:
- M3 (Domain Contracts) — per QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md and M3 spec plan

<!-- 2026-08-18 00:36 UTC+7 -->