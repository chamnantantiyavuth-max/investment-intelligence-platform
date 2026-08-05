# IIP Hermes AI Workforce — Runtime Verification Evidence

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED (pre-merge evidence, branch `org-pack-v0.1`)
**Date:** 2026-08-05
**Authority:** FD #54 (Q1 as proposed / Q2 Holds org-workflow-only / Q3 Option C zero-profile pilot)
**Companion:** `operational/hermes-organization/installation/RUNTIME-VERIFICATION-CHECKLIST.md`
**Evidence tags:** TEST_VERIFIED (commands executed) · STATIC_OBSERVATION (inspection) · INFERENCE (mapping claims)

---

## 1. Stage 1 — Docs Verification (STATIC_OBSERVATION + TEST_VERIFIED greps)

| Check | Result | Evidence |
|---|---|---|
| No second constitution title in org artifacts | ✅ PASS | `grep -i "organization constitution"` hits are meta-references only in the analysis/checklist docs (FIT-GAP, INTEGRATION-PLAN, RUNTIME-VERIFICATION-CHECKLIST) — no artifact titled/claiming "Organization Constitution" |
| Two-axis Theme governance present | ✅ PASS | `approval_status` + `monitoring_status` both in KANBAN-CONTRACT §3 |
| Flat `governance_state` absent | ✅ PASS | only meta-references (disposition/checklist notes) |
| Pack research-lifecycle values absent | ✅ PASS | no "Observation / Hypothesis / Draft / Reviewed" state model anywhere |
| Rejected templates absent | ✅ PASS | no `04-*` / `05-*` in templates/ |
| Standard's amendment rule → Constitution §21 | ✅ PASS | Standard §15: "NO independent amendment authority… Constitution §21" |
| Hold semantics org-workflow only (Q2) | ✅ PASS | Standard §10 + AUTHORITY-MATRIX §6: "org-workflow scope only — never canonical state" |
| CIW boundary in Equity role (F-09) | ✅ PASS | `roles/05-equity-alpha-analyst/PRINCIPAL.md` — 2 explicit CIW-boundary references |
| Sol Medium routing in Auditor role (F-11) | ✅ PASS | `roles/10-internal-auditor-red-team/PRINCIPAL.md` — 4 Sol Medium references |

## 2. Stage 2 — Roles and Templates Verification (STATIC_OBSERVATION + TEST_VERIFIED)

| Check | Result | Evidence |
|---|---|---|
| §23.5 contract fields per role | ✅ PASS 10/10 | each PRINCIPAL.md has 5/5 of: Prohibited Actions, Permitted Evidence, Deterministic Dependencies, Failure Behavior, Escalation (+ authority boundary, IO contract, provenance, review) |
| Assistant label + prohibition envelope | ✅ PASS | every ASSISTANT.md carries the label contract + prohibitions |
| Portfolio-blind in every role | ✅ PASS | 0/10 PRINCIPAL.md files lack a portfolio-blind clause; no holdings/positions/cost-basis grants anywhere |
| Template mapping to canonical sources | ✅ PASS | templates/README.md disposition table; 13 forms, 04/05 rejected |
| `iip` profile untouched | ✅ PASS | hash unchanged (see §4) |

## 3. Stage 3 — Installation Docs (STATIC_OBSERVATION)

- `installation/HERMES-PROFILE-MAPPING.md` — real runtime paths (AppData\Local\hermes\profiles), 10-profile table, sync extension, rollback ✅
- `installation/PROFILE-STARTUP-CONTRACT.md` — thin loader, label contract, memory discipline, degraded operation ✅
- `installation/RUNTIME-VERIFICATION-CHECKLIST.md` — this checklist ✅
- `kanban/` — board.md + cards (ORG-2026-0001..0005) + holds ✅

## 4. Stage 4 — Profile Installation Verification (TEST_VERIFIED)

| Check | Result | Evidence |
|---|---|---|
| Rollback branch/checkpoint created BEFORE modification | ✅ | branch `org-pack-v0.1` created 2026-08-05 14:36 (from clean main @ be93aff); runtime backup `_staging\hermes-backup-20260805\` (shared SOUL/user, project-context, sync + watchdog scripts, iip config) |
| 10 principal profiles installed | ✅ | `hermes profile list`: org-auditor, org-commodity-analyst, org-cos, org-cro, org-data-steward, org-equity-analyst, org-ic-secretary, org-macro-strategist, org-options-strategist, org-quant-validator (18 profiles total) |
| No Assistant profiles installed | ✅ | only 10 org-* Principal profiles (FD #54 Q1 topology) |
| Sync idempotent | ✅ | `sync-governance.py` re-run SILENT (exit 0, no drift) after initial create pass |
| Existing 8 profiles' SOUL unchanged | ✅ | SHA-256(16) prefix identical pre/post for iip, capcmd, fxtrading, notebooklm, antigravity-orchestrator, close-system-learning-lab, profirm + SHARED_SOUL (see §5 hashes) |
| Watchdog coverage | ✅ | `cross-profile-sync-watchdog.py`: "SOUL.md cores: 16 profiles checked"; skills 201; no alerts |
| Profile config loads | ✅ | `hermes --profile org-cos config get model.default` = deepseek-v4-flash; same for org-auditor |
| SOUL compose correct | ✅ | org-cos SOUL: canonical core hash matches shared SOUL core (context stripped); PROFILE_CONTEXT splice present (BEGIN/END intact) |
| No secrets in org profiles | ✅ | 0 `.env` / `auth.json` files across org-* profiles |
| Config identity | ✅ | org-* config.yaml semantically identical to iip config (CRLF-only diff) |
| Skills junction | ✅ | `skills` → skills-shared junction created for all 10 |

## 5. Hash Snapshot (pre-install → post-install)

| File | Pre-install (SHA-256[:16]) | Post-install | Status |
|---|---|---|---|
| profiles/iip/SOUL.md | f3fcae28d356ec44 | f3fcae28d356ec44 | UNCHANGED |
| profiles/capcmd/SOUL.md | 28d81a1194871df0 | 28d81a1194871df0 | UNCHANGED |
| profiles/fxtrading/SOUL.md | 0951338ea69d6e25 | 0951338ea69d6e25 | UNCHANGED |
| profiles/notebooklm/SOUL.md | 7daaf4d3655769d1 | 7daaf4d3655769d1 | UNCHANGED |
| profiles/antigravity-orchestrator/SOUL.md | 4cd31f69451ed197 | 4cd31f69451ed197 | UNCHANGED |
| profiles/close-system-learning-lab/SOUL.md | 35ecb250fa46a511 | 35ecb250fa46a511 | UNCHANGED |
| profiles/profirm/SOUL.md | 4cd31f69451ed197 | 4cd31f69451ed197 | UNCHANGED |
| shared/SOUL.md | 2a5898551d172385 | 2a5898551d172385 | UNCHANGED |

## 6. Stage 5 — Dry-Run Pilot (Option C)

COMPLETE — PILOT PASS (8/8 criteria). Artifacts: `evidence/organization/pilot/` (brief, worklog, data report, risk memo, decision pack) + `kanban/holds/` (HOLD-DATA-001, HOLD-RISK-001 — issued + cleared by issuer). Report: `evidence/organization/pilot/PILOT-REPORT.md`.

| Criterion | Result |
|---|---|
| 5/5 handoffs named owner + IO + next state | ✅ |
| 3/3 memos trace to source map, zero fabricated refs | ✅ |
| 2/2 Holds issued + cleared by issuing role only | ✅ |
| Dissent preserved after simulated approval | ✅ |
| Packet failed once ADMINISTRATIVELY INCOMPLETE → re-pass | ✅ |
| Zero canonical changes by pilot | ✅ |
| Portfolio-blind (grep-verified; hits are meta/clause text only) | ✅ |
| No CIW-path work (zero writes under docs/ciw-pilot-msft/) | ✅ |

Deviations disclosed: Round-1 delegated subagent did not complete in-window → in-session role-contract simulation (single-agent); write race between subagent and orchestrator surfaced pilot learning L1 (single-writer discipline required — confirmed KANBAN-CONTRACT §10) + L2 (delegation reliability — Standard §23.7 applies to delegation itself).

## 7. Ad-Hoc Verification of Changed Scripts + Kanban Cards (TEST_VERIFIED — temp script, not suite green)

Temp verification script (`hermes-verify-*.py`, created + removed under `%TEMP%`) executed 2026-08-05 ~15:12:

| Check | Result |
|---|---|
| `py_compile` sync-governance.py (patched PROFILES) | PASS |
| `py_compile` cross-profile-sync-watchdog.py (patched PROFILES) | PASS |
| sync-governance.py run — exit 0 + silent (idempotent) | PASS |
| watchdog — 16 SOUL cores checked, zero SOUL drift | PASS |
| 5 kanban cards YAML parse + required fields (KANBAN-CONTRACT §3) | PASS 5/5 |
| Existing 7 profile SOUL hashes unchanged (drift guard) | PASS 7/7 |
| org-* profile count == 10 | PASS |

Watchdog exit code 1 is a **pre-existing, unrelated memory-hygiene alert** (CHECK 3 reads the antigravity-orchestrator profile: MEMORY 99%, USER 98% — at the same levels before this session's first watchdog run; org-* profiles have empty MEMORY.md). Not a regression from the org-pack change. Flagged for the closeout hygiene backlog (parallel to C-05 vault rebuild).

---

*Runtime verification evidence v0.1 — FD #54. Branch org-pack-v0.1; pre-merge review pending Founder acceptance.*
<!-- 2026-08-05 15:12 UTC+7 -->
