# S7.8 — Cutover Declaration + Stage 7 Closeout (13 Aug 2026)

## VERDICT: **CUTOVER PASS** ✅

**ONE authoritative organizational work-state source = Hermes Capital Intelligence board** (`kanban/boards/iip/`, display name "Capital Intelligence"). Old repo board FROZEN/read-only (not deleted — Stage 8 pending).

---

## 1. Baseline / Repository Reconciliation (S7.0)

| Repo | HEAD | State |
|---|---|---|
| main | `f1ec9ec` (+ `280c98b` P2, parent `9967459`) | PRE-EXISTING unrelated dirty work left untouched (3 deleted ChatGPT files, M PROJECT_STATE, M SESSION_CLOSEOUT, untracked) — **not stashed/deleted/overwritten/committed** |
| harness/stage2-prep | `94c4080` (clean) | Stage evidence/checkpoints committed |

Commits entering production: `280c98b` + `f1ec9ec` (AGENTS.md routing only). Backups: `stage7-baseline/kanban-iip.db.bak` + `board-iip.json.bak`.

## 2. Migrated Live-Card Mapping (S7.3) — 12/12

| Legacy card | Hermes task | Status |
|---|---|---|
| ORG-2026-0001 Pilot bounded review | t_729eee21 | done (pilot completed on migration) |
| ORG-2026-0002 Pilot data readiness | t_daa9d7c8 | done |
| ORG-2026-0003 Pilot risk challenge | t_c4cf4ba2 | done |
| ORG-2026-0004 Pilot Founder pack | t_82a8bbb6 | done |
| ORG-2026-0005 Pilot governance/lineage | t_cb9864d9 | done |
| ORG-2026-0012 Radar Gold/real-yields (Blocked) | t_7ee31d54 | running (live work continued) |
| ORG-2026-0016 Radar London silver vaults | t_8411623f | running |
| ORG-2026-0017 Radar Alphabet capital-raising | t_d5019196 | running |
| ORG-2026-0018 Inflection ABBV | t_c75826ee | done |
| ORG-2026-0019 Inflection BMY | t_644d9446 | done |
| ORG-2026-0020 Inflection LLY | t_99a8e763 | done |
| ORG-2026-0021 Inflection VRTX | t_c3195d47 | done |

Every migrated task carries: legacy ref in title (`[MIGRATED:ORG-####]`), body with legacy column/owner/status, frozen source path, idempotency key (`s7-migrate-*`).

## 3. Production Profile Activation List (S7.2) — 13 profiles

iip · org-cos · org-data-steward · org-quant-validator · org-auditor · org-equity-analyst · org-commodity-analyst · org-cro · org-ic-secretary · org-macro-strategist · org-options-strategist · org-radar-scout · ipm — **all: board pin=iip + safety hook allowlisted + write_approval:true + nudge:0**. (S7.0 gap: 4 profiles lacked pin/hook → fixed.)

## 4. IPM Production Docker Canary (S7.4) — PASS 4/4

Synthetic canary (t_9bd4de60, `harness-canary-ipm` profile, docker backend, IPM-workspace-only mount):
1. IPM sentinel visible: `IPM-CANARY-SENTINEL-2026-08-13` ✓
2. IIP private workspace NOT mounted (exit 2 expected) ✓
3. Host paths NOT visible (exit 2 expected) ✓
4. echo ok ✓
→ portfolio-aware IPM work may be enabled (after real IPM repo exists; none today — simulated only).

## 5. /kanban + /org-office Read-Path (S7.5) — PASS

- New `backend/hermes_kanban_store.py` — read-only adapter over Hermes iip board DB (SQLite, mode=ro URI), OrgCard shape, columns = board reality (Ready/In Progress/Blocked/Done/Cancelled — legacy 11-column state machine NOT recreated)
- `org_routes.py /org-queue` rewired → Hermes board; **fail-closed 503** if board unavailable (never falls back to frozen legacy board as live state)
- Read-only: no mutation endpoints exposed to browser (unchanged); holds = [] on Hermes board (legacy holds stay frozen)
- Verified: 64 tasks served, data_source=hermes_kanban_board, authoritative_since=2026-08-13

## 6. Cron Idempotency (S7.6) — PASS

- Weekly Radar (FD #78 cron `8ba233e88015`) → `[DISC][STANDING]` task t_535d91be
- Mid-Week Watch (FD #80 cron `cda817d17236`) → `[DISC][STANDING]` task t_02a53b7b
- **Idempotency verified:** re-create with same key returned existing task (t_535d91be, 1 row in DB — zero duplicates)
- Unrelated cron (Nick-Weekly, IIP Daily Learning, ciw-msft) UNCHANGED (per cutover discipline)

## 7. Privacy / Leak Scan (S7.7) — PASS

7 keyword hits reviewed — ALL benign: "portfolio" = "portfolio-blind" constraint phrase in pilot bodies; "P/L"/"margin" = substring false positives (e.g. Stage 4b hook body) / GM-margin research context. **Zero portfolio-sensitive data** in board text/comments/results/attachments. IPM tenant tasks contain SYNTHETIC-only data.

## 8. Old-vs-New Reconciliation (S7.7) — PASS

- 12/12 legacy live cards mapped 1:1 (titles match)
- Old board FROZEN marker appended (S7.1 commit) — read-only, historical record preserved
- 9 legacy non-live cards (Published/Closed) NOT re-created as live (per Founder: don't recreate closed history as live tasks) — remain in frozen repo board as record
- ONE authoritative source = Hermes board (verified via adapter)

## 9. Rollback Evidence

- `evidence/harness/stage7-baseline/kanban-iip.db.bak-2026-08-13` + `board-iip.json.bak` (pre-migration board state)
- Git: main `9967459` pre-cutover parent; harness `94c4080`; all Stage 7 commits revertible (`git revert`)
- Legacy board untouched (FROZEN marker only — original YAML intact)
- Config backups: `.bak-2026-08-13-f1` (13 profiles), `.bak-2026-08-13-stage65/66`
- Rollback = restore DB backup + point org_routes back to legacy store (git revert) + unfreeze marker

## 10. Unresolved Findings (backlog, not blockers)

1. **browser_exec stdout Unicode defect** (cp1252) — direct CDP is working transport; candidate skill saved for review (f1-fork-candidates)
2. **Real IPM repo does not exist yet** — IPM boundary proven synthetically (canary); real portfolio-context work requires IPM repo + Docker worker setup (post-cutover, separate task)
3. **Legacy card statuses** (Pilot cards done on migration — workers auto-completed benign pilot work; radar cards running = live work continuing)
4. 4 profiles got board pin/hook in S7.0 (were missing) — now uniform
5. `/org-holds` returns empty (Hermes board has no holds concept) — legacy HOLD-DATA-001/HOLD-RISK-001 remain frozen in repo board; UI shows no holds (honest absence)

## 11. Recommendation

**CUTOVER PASS** — proceed to Stage 8 (old repo-board deletion) only after independent reconciliation/observation, per Integration Plan. NOT started (per Founder: STOP before Stage 8 deletion).

---
<!-- 2026-08-13 02:33:32 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
