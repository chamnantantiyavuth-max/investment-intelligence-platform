# STAGE 4.1 — Governance Closure (G1–G5)

**Status:** COMPLETE — Stage 4 technical closeout APPROVED with governance cleanup; Stage 5 NOT started
**Date:** 2026-08-12
**Branch:** `harness/stage2-prep`
**Authorization:** Founder Stage 4.1 direction (G1–G5)

---

## G1 — Unauthorized / Automatic Skill Mutation Audit ✅

**Finding (the trigger the Founder flagged):** during Stage 4, the Engineering Review subagent's **background review fork** (Hermes built-in post-turn self-improvement, `agent/turn_finalizer.py:760` — fires when `_skill_nudge_interval > 0` and `_iters_since_skill >= interval` and `skill_manage` is in the toolset) auto-patched `governed-review-gates`:

| Item | Value |
|---|---|
| Skill path | `skills-shared/software-development/governed-review-gates/SKILL.md` |
| Before hash | `9560b1b6561ccb15f6c6fe57cced9fd00d7a1ef86ac35ddd72f2e14809048e0b` (v1.5.0, snapshot 3 Aug) |
| After hash | `5e27133e3781f32fa76ad18fcbe8d6dcacbd08ca90222b05cb01f552cb3545c8` (v1.5.1) |
| Diff | +3 sections (visual-council retest lessons, **runtime-enforcement design review — derived from this Stage 4 work**, audit-note integrity controls) + new reference `references/runtime-enforcement-design-review.md` (auto-added 20:19) |
| Trigger | `background_review` fork of Engineering Review subagent session `20260812_200757_a52785` (20:19–20:20) — NOT authorized by Founder, NOT part of S3-F1 scope |
| Auth | NONE — autonomous self-improvement write (guard "not agent-created" refused other candidates, but governed-review-gates passed the curator-managed gate) |

**Full sweep for Stages 2–4:** 35 SKILL.md files with mtime 17:18 today = **Hermes update re-sync** (main.py mtime 17:18:53), NOT mutations. Exactly **1 unauthorized auto-patch** found (governed-review-gates). All other background-curator attempts today were refused by the built-in guard (logged WARNINGs). No other auto-mutations during Stages 2–4.

**Revert (done):**
- `SKILL.md` restored to before-state `9560b1b6` (v1.5.0) — hash verified identical to pre-patch snapshot.
- Auto-added reference `references/runtime-enforcement-design-review.md` removed (no orphan pointer remains — grep 0).
- **Proposed change preserved as candidate evidence** (NOT applied to production): `evidence/harness/g1-skill-mutation-candidate/` (patched SKILL.md + reference + exact diff `g1-exact-diff.txt`).

**Guard (done):** `profiles/iip/config.yaml` → `skills.creation_nudge_interval: 0` (was 15) — disables the background skill-review trigger for the IIP production profile (`turn_finalizer.py:734` requires `_skill_nudge_interval > 0`). Backup: `config.yaml.bak-2026-08-12-stage41`.
**Policy:** agents may PROPOSE/stage skill improvements; agents may NOT silently APPLY canonical skill changes — Founder approval required (matches Harness stage+review model). Any future skill change from a worker/agent must be delivered as a candidate diff for Founder review, never written directly.

## G2 — FD #101 Final-State Reconciliation ✅

FD #101 initially referenced commit `76528cfa` (written before the full async Engineering Review returned). Appended **FD #101-A — Amendment/Correction Record** (not a silent rewrite) to BOTH registers:
- `operational/FOUNDERS-DECISIONS.md` item 118 (worktree)
- vault `fd-register.md` FD-101-A
- Content: final implementation commit **a227ecef** (+ evidence c919e2b, eafa2ed); REWORK verdict resolution (F1–F7); post-FD-101 fixes B1 (matcher `kanban_.*|terminal` fullmatch), B2 (DB path normalization), root fix (profile `.env` startup pin), R-ADD-2 (inline env bypass); final hook suite 8/8; fd_count 118.

## G3 — Delegated-Child Kanban Doctrine ✅

**Runtime fact:** `HERMES_DELEGATED_CHILD_CONTEXT=1` is set in delegate_task child contexts; Kanban mutation from such contexts is **refused by the runtime** (`kanban_db.py:181`, `kanban.py:1220`). This is a **safety boundary**, not a nuisance.

**Production doctrine (recorded for future capital-kanban / workforce procedure):**
```
delegate_task child
  → MUST NOT unset or bypass HERMES_DELEGATED_CHILD_CONTEXT
  → MUST NOT mutate organizational Kanban

Principal / dispatcher / authorized Kanban worker
  → owns organizational task-state mutation
```
The Stage 4 diagnostic unset was **test-only** (to exercise the hook as the orchestrator session); it must NOT become production procedure. Kanban orchestration belongs to principal/dispatcher contexts.

## G4 — S4-F2 Disposition ✅

**Classified: ACCEPTED OPERATIONAL LIMITATION (Severity: Low)**

| Item | Value |
|---|---|
| Behavior | gateway restart can kill an in-flight worker; task claim remains held until `claim_expires` (~15 min observed) before dispatcher reconciles |
| Data loss | none |
| Recovery | dispatcher eventually reconciles; operator block/unblock accelerates re-dispatch (proven Stage 3.2 C3 + Stage 4) |
| Decision | **do NOT patch Hermes core** for this in the current Harness project |

**Runbook note (future Kanban operations):** if a gateway restart happens during a worker run and a task stays `running` past worker death, either (a) wait for claim expiry (~15 min) or (b) operator `block` + `unblock` the task to force immediate re-dispatch. No data loss either way.

## G5 — Closeout State ✅

- Config diff (Stage 4.1): `skills.creation_nudge_interval` 15 → 0 (iip profile) — the only config change in this closure.
- Skill diff: governed-review-gates reverted (no net change vs production; candidate preserved in worktree evidence/).
- Rollback: `config.yaml.bak-2026-08-12-stage41` restores nudge interval; governed-review-gates restore is idempotent (hash-verified).
- Worktree: clean after commit.
- fd_count 118 (FD #101-A) — repo + vault registers agree.

---

## Stage 5 Authorization Status

**NOT STARTED.** Stage 5 (Discovery Recall & Coverage v1.1 — bounded Kanban pilot, non-canonical, no investment/domain state change) may proceed per the existing Integration Plan once the Founder reviews this closure.

---
<!-- 2026-08-12 21:46:33 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
