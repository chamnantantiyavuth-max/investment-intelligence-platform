# COUNCIL DECISION

## Gate
Plan (Lite — Phase 3)

## Verdict
PASS WITH FIXES

## Material Findings
1. Locked tests were ordered after the implementation they must govern (T1–T5 verify against `tests/locked/test_real_data_api.py` created only at T9). → TDD RED-first reorder (T1 becomes the pre-implementation contract).
2. T8 artifacts + `.env.example` cannot be committed under current ignore rules; `/backend/data/*.db*` rule absent. → config/hygiene task (order-aware un-ignore, `.env.example`).
3. T6 runner propagation surface incomplete (mode must flow `run_pipeline` → `build_research_package` → `_supporting_evidence`; II `display.py:134-141` writer unlisted). → backward-compatible mode param + display.py in scope.
4. T7 omitted part of the frontend migration surface (`types/fo.ts`, FO pages, AM provenance labels, dashboard response type). → full surface enumerated.
5. Adapter-version code-hash implementation absent (registry/hash contract). → T4 adapter registry + immutable hash.
6. `gate-check.sh`/`isolation-scan.sh` do not exist; per-directory baseline commands missing. → create scripts + enumerate 5 pytest commands with expected counts.
7. T1 mutation-check wording contradicts immutable-run contract. → distinguish embedded-run-id (reject) vs hash-derived (new id) cases.
8. D1–D4 are dependencies but not an execution gate. → T0 precondition requiring recorded Founder approval.

## Required Changes
1. Move locked-test creation before implementation (TDD RED-first).
2. Add config hygiene task (.gitignore *.db + artifact exceptions + .env.example).
3. Specify full mode propagation + II display.py atomic writer.
4. Complete frontend migration surface (fo types/pages, AM provenance, dashboard client).
5. Implement adapter registry + immutable code hash.
6. Create gate-check.sh + isolation-scan.sh with per-directory baselines.
7. Lock both immutable-run mutation cases.
8. Gate implementation on recorded D1–D4 approvals (T0).

## Evidence Gaps
- None at plan level (architecture v0.4 reviewed across 3 adversarial 2R rounds).

## Founder Decisions Required
- D1–D4 (all recommended Option A) — recorded as FD #47 at T0.

## Minority Warning
- None.

## Scope Expansion Check
- None — plan stays within FD #46 scope.

<!-- 2026-08-03 21:00 UTC+7 -->
