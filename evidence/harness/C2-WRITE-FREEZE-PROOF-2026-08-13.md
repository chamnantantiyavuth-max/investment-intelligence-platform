# C2 — Old-Board WRITE Freeze Proof (13 Aug 2026)

> Correction pass C2 per Founder directive: a FROZEN marker alone is not a
> technical freeze. Every legacy writer path identified; benign write-attempt
> tests executed; active writer paths disabled. Zero old-board filesystem delta.

## Writer-path inventory (post-C3/C5)

| Writer path | Status |
|---|---|
| Cron prompts `8ba233e88015` / `cda817d17236` (legacy YAML card + digest + commit) | **DISABLED** — prompts rewritten (C3): board tasks only, digest → `evidence/radar/digests/`, explicit zero-write boundary for the old tree |
| Governance docs teaching repo-board writes (KANBAN-CONTRACT, role 11 PRINCIPAL, PROFILE-STARTUP-CONTRACT, STANDARD, AUTHORITY-MATRIX, ROLE-REGISTRY) | **DISABLED** — superseded (C5/M7B) |
| Agent tool access: `write_file` / `patch` / terminal writes to the old tree | **BLOCKED — two layers** (below) |

## Layer 1 — board-safety-hook extension (script-level)

`iip-harness-prep/scripts/board-safety-hook.sh` extended with
`guard_repo_board_write()` (blocks write_file/patch/edit_file whose path is under
`operational/hermes-organization/kanban/`) + `guard_terminal_write()` (blocks
terminal commands referencing the tree with write indicators: git add/commit/rm/mv,
`>`, `>>`, tee, cp, mv, touch, mkdir, rm, sed -i, python, echo, printf, cat >).
Matcher extended `kanban_.*|terminal|write_file|patch` on all 13 profiles
(iip + 11 org-* + ipm), verified in all 13 config.yaml files.

Script-level tests (8/8): write_file→old tree BLOCK · patch→old tree BLOCK
(both C:/ and MSYS forms) · terminal git add / git mv → BLOCK · write_file→backend
ALLOW · terminal cat (read) → ALLOW · kanban create wrong board → BLOCK.

## Layer 2 — OS-level read-only ACL (the hard technical freeze)

**Runtime finding:** shell hooks are registered only at the CLI/gateway entry
(`hermes_cli/main.py`, `gateway/run.py`) — **delegated subagent sessions do not
load shell hooks**, so a subagent's write_file is NOT hook-guarded. A live probe
confirmed the hook did not fire for a subagent write_file (file created; deleted
immediately by the probe protocol — zero residual).

→ Applied a Windows ACL deny-write/delete on the whole old board tree:

```
icacls "...\operational\hermes-organization\kanban" /t /deny "*S-1-1-0:(WD,AD,DC,DE)"
```
(Everyone: deny WriteData, AddFile, DeleteChild, Delete — explicit deny beats
allow, so this holds for every user/agent including Admin.)

**Live benign write-attempt tests (must refuse → zero delta):**

| Attempt | Result |
|---|---|
| create new file `kanban/cards/ORG-2026-9999.yaml` (terminal) | **Permission denied** ✅ |
| append to `kanban/board.md` (terminal) | **Permission denied** ✅ |
| delete `kanban/cards/ORG-2026-0022.yaml` | **Permission denied** ✅ |
| subagent (fresh session) `write_file` to `kanban/cards/ORG-2026-9999.yaml` | **Permission denied** (quoted error returned to the subagent) ✅ |
| subagent `echo probe > kanban/cards/ORG-2026-9999.yaml` | **Permission denied** (exit 1) ✅ |

Zero filesystem delta verified: board.md sha256 unchanged
(`dd0138d3…dcf0e7f`), no ORG-2026-9999 file, all 22 cards intact, reads
unaffected (cat/ls/git status still work).

## Residual / notes

- The old board remains READABLE as frozen migration evidence (ACL denies only
  write/delete) — exactly the Stage-7.1 intent.
- Stage 8 (deletion, pending Founder GO): remove the ACL first —
  `icacls "...\kanban" /t /remove:d "*S-1-1-0"` — then delete the tree.
- Hook Layer 1 still guards kanban board routing + CLI mutations in sessions
  that load hooks (gateway/CLI); Layer 2 covers everything else.
- ACL applies to the working-tree copy only; git objects/history are untouched
  (historical record preserved per Harness).

<!-- 2026-08-13 16:20 UTC+7 -->
