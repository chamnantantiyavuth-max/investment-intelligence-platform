# STAGE 2F — Memory / USER Preparation Audit

**Purpose:** Audit built-in memory + user-profile content; determine memory limit AFTER cleanup (not fixed 2200); document user.md sync dependency; plan benign write-approval test.
**Status:** DRAFT — no memory/user.md mutation in Stage 2.
**Date:** 2026-08-12

---

## 1. Memory Architecture (verified)

| Layer | File | Role | Loaded by runtime? |
|---|---|---|---|
| Built-in memory (hot) | `profiles/iip/memories/MEMORY.md` (3,793 bytes / 3,489 chars — **97% full** of 3,500 limit) | small operational facts | YES (injected every turn) |
| User profile (hot) | `profiles/iip/memories/USER.md` (1,992 bytes / 1,914 chars — **95% full** of 2,000 limit) | stable Founder preferences | YES |
| Legacy top-level user profile card | `$HERMES_HOME/user.md` (1,773 bytes) | sync target of sync-governance.py | **NO** (runtime loads memories/USER.md — verified: this session's injected USER PROFILE matches memories/USER.md, not top-level user.md) |
| Canonical user card | `shared/user.md` (2,051 bytes) | sync-governance.py CANONICAL source | indirect (via sync targets) |
| Config limits | `memory_char_limit: 3500`, `user_char_limit: 2000` | — | — |

**Key finding:** THREE user-profile mechanisms coexist:
1. `shared/user.md` → synced to `user.md` (top-level) + `memories/USER.md` per profile by sync-governance.py (forward-only, per-profile lines preserved)
2. Runtime actually reads `memories/USER.md` (profile-scoped)
3. `shared/user.md` has DIFFERENT content format (identity card) vs `memories/USER.md` (behavioral prefs)

→ **user.md cannot be deleted** until sync-governance.py USER_TARGETS is redesigned (confirmed dependency, Stage 1.1 finding #9).

## 2. MEMORY.md Content Audit (30 lines, 11 §-separated entries)

**P6 correction (Stage 2.1):** MUTABLE routing facts + historical verification results must NOT live in hot memory — runtime config is authoritative for model routing; secret-scan results are point-in-time, not durable facts.

| Entry | Classification | Action |
|---|---|---|
| GitHub/gh auth, Claude avoid, Codex/Sol path WORKS, Luna fallback, DeepSeek primary | **Mutable routing/state — P6: REMOVE from MEMORY** | **REMOVE** — runtime config (model.default / delegation.model / fallback_providers) is source of truth; provider-choice rationale → FD register |
| Investment domain summary (Close System risk mgmt, FX risk-per-trade, Theme/macro > signals, Avoid Stage 4, Org = fundamental/moat only FD #75) | Domain rule — belongs in AGENTS/spec, not hot memory | **MOVE** → AGENTS.md (already covered there) |
| Interview style (Thai, one Q/turn, options format, FDs with titles) | Founder preference | **MOVE** → USER.md |
| Design: UI/UX Pro Max, Bible-first phrasing rule | Preference + phrasing rule | **MOVE** → USER.md + AGENTS |
| Vault paths, NotebookLM CLI/auth, cron | Operational fact (paths/tools — stable) | **KEEP** (trim) |
| BIBLE-FIRST v2.2 startup procedure | Procedure — belongs in skills | **MOVE** → project-workflow/AGENTS |
| Workflow: diagnostic→answer+evidence, one decision at a time, charts rules | Founder preference + procedure | **MOVE** → USER.md (prefs) + skill |
| **IIP secret scan PASS**, *.env gitignored, re-check git status | **Historical verification result — P6: REMOVE from MEMORY**; convert to procedure | **REMOVE** → procedure: "run secret scan before release/commit" in engineering workflow (v3.8 §Core Principles #8 + verification); *.env gitignored fact → AGENTS/README |
| **FDs 112 summary (#96/#95/#92/#93/#94/#89 + CS Discovery DEFERRED)** | **Task/decision log — NOT memory material (stale in days)** | **REMOVE** → vault FD register owns |
| Auth env (IIP_AUTH_*) | Operational fact (non-secret names) | **KEEP** (trim) |
| IPM-FD-003 + FD #71 | Decision summary | **REMOVE** → repo/FD register |
| Founder UI process (mockup-first) | Founder preference | **MOVE** → USER.md |
| External AI proposals FIT-GAP method | Procedure | **MOVE** → skill (iip skill already) |
| Autonomous execution after approval | Founder preference | **MOVE** → USER.md |
| Blog text-only, Thai font, magazine nesting, Vercel prod | Operational + project facts | **KEEP** (Vercel) / MOVE (blog rules → iip-ui-design/AGENTS) |

**Estimated useful remaining hot memory after cleanup: ~400–800 chars** (stable paths/tools only: vault path, NotebookLM tool, auth env names, Vercel deploy facts) — smaller than the earlier 900–1,300 estimate because routing + secret-scan results are now excluded.

## 3. Memory Limit Determination (post-cleanup, per Founder #10)

```
Process:
1. Clean wrong content (FD summaries, decision logs, domain rules, procedures, prefs) → destinations above
2. Measure remaining legitimate operational facts → target = that size + small headroom
3. Choose limit (NOT sacred 2200): if 900 chars of facts remain → limit 1200–1500
4. Same for USER.md: sync content first, then measure
```

**Stage 2 action:** none (mutation deferred). Proposed: Stage 3 applies cleanup + sets limit from measured reality. Current 3500/2000 stay until then.

## 4. user.md / USER.md Sync Dependency (verified)

- `sync-governance.py` USER_TARGETS = `[HERMES/user.md]` + `[profiles/<p>/memories/USER.md for p in PROFILES]`
- CANON_USER = `shared/user.md`
- Forward-only sync: canonical → targets; per-profile lines preserved in memories/USER.md
- **Deleting top-level user.md without script redesign breaks sync** → confirmed: NO delete in Stage 2
- Stage 3 plan: redesign script (single canonical user card + per-profile prefs merge) with rollback, THEN retire duplicates

## 5. Write-Approval — Benign Test Plan (Stage 3, deferred)

v0.20.0 support verified:
- `memory.write_approval` (config_defaults:1728, default False) + `skills.write_approval` (config_defaults:1902, default False)
- `tools/write_approval.py` has `write_approval_enabled(subsystem)` + staging path ("Staged for approval (memory.write_approval is on)")
- Gateway slash commands: `/memory pending|approve|reject`, `/skill pending|approve|reject` (slash_commands.py:3592-3661)

**Benign test design (Stage 3, non-production):**
1. Use a THROWAWAY profile (e.g. `close-system-learning-lab` or temporary `wa-test`) — NOT iip/org-*
2. Enable `memory.write_approval: true` on that profile only
3. Stage one benign entry (e.g. "wa-test: write-approval smoke test")
4. Verify pending is visible + approvable on the CLI surface the Founder uses
5. Approve → verify file state; reject a second entry → verify no write
6. Clear test state, restore profile config
7. Only if the flow works cleanly on the real surface → propose production enablement

**If the approval workflow is broken/awkward on the active surface:** do NOT silently leave approval off; use stricter profile/tool/filesystem write boundaries until fixed (Harness §35 gate).
