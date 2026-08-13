# P4 — Public-Repo Kanban Snapshot Privacy Audit (13 Aug 2026)

> Founder round-3 directive: the repository is PUBLIC and the push range
> `9967459..1469de9` includes a full SQLite snapshot of the live Hermes board.
> Audit content deterministically BEFORE any destructive action. Clock basis:
> `scripts/artifact_timestamp.py`.

## 0. Facts

- Repo visibility (gh CLI): **PUBLIC** — https://github.com/chamnantantiyavuth-max/investment-intelligence-platform
- File: `evidence/harness/stage8-preflight-baseline/kanban-iip.db.snapshot-2026-08-13`
  (565,248 bytes; SHA-256 `10a71c1b0db96a30…`), introduced in commit `8ed372e`
  (correction pass, pushed 13 Aug) — **present in public history**.
- Companion file `board-iip.json.snapshot-2026-08-13` (279 B) = benign board
  metadata (slug/name/description/icons) — PUBLIC-SAFE.

## 1. Deterministic inventory (sqlite3 read-only)

| Table | Rows | Notable columns |
|---|---|---|
| tasks | 72 | id, title, **body**, assignee, status, priority, **result**, **workspace_path**, tenant, model_override, provider_override, skills, branch_name, block_kind, goal_mode… |
| task_comments | 50 | task_id, author, **body** |
| task_events | 850 | task_id, run_id, kind, **payload** (full event history: claimed/spawned/completed/crashed…) |
| task_runs | 80 | profile, status, **summary** (69), **metadata** (71), **error** (11), worker_pid, claim_lock |
| task_attachments | 44 | filename, **stored_path** (absolute), content_type, size |
| task_links | 39 | parent/child |
| kanban_notify_subs | 0 | (empty) |
| sqlite_sequence | 4 | — |

## 2. Exposure findings

| Finding | Evidence | Public-internet implication |
|---|---|---|
| **Absolute local filesystem paths** | `workspace_path` 67× = `C:\Users\Admin\AppData\Local\hermes\kanban\boards\iip\workspaces\t_*`; `stored_path` 44× = `C:\Users\Admin\AppData\Local\hermes\...\attachments\...` | Leaks Windows username + full hermes data location + internal layout |
| **Internal operational prompts/briefs** | task bodies (71 non-empty) incl. Luna REVIEW BRIEF, [GATE] contexts (0004/0012), publish-gate text, radar/idempotency keys, Hormuz research context (3), "portfolio" mentions (5, benign per Luna board scan) | Internal research-workflow detail exposed publicly |
| **Internal artifact filenames** | attachments: `S4-DISPATCH-P…`, `S4-GEMINI-VIE…`, `CLOSE_SYSTEM_…`, `ORG-2026-0022…`, `2026-08-13-ra…` | Reveals internal stage-4 harness artifact names |
| **Model/provider routing** | model_override ∈ {openai/gpt-5.6-luna, gpt-5.6-sol}; provider ∈ {openai-codex, openrouter}; tenant ∈ {iip, ipm} | Internal routing/architecture detail |
| **Run metadata + errors** | task_runs summary/metadata/error (11 errors), events payloads | Internal operational history |
| **Roles/assignees** | 14 assignee profiles (org-* roles + ipm + harness-*) | Org structure exposure (minor) |

## 3. NOT found (scanned)

- Email/user identity: **0** (kanban_notify_subs empty; no email regex hits)
- Tokens/API keys: **0** (sk-/ghp_/AIza… zero; consistent with pre-push secret scan PASS)
- Portfolio-sensitive data: **0** — no holdings/positions/cost-basis/quantities/accounts;
  IPM-tenant task = `[PILOT-NONCANONICAL] IPM Tenant Pilot — sanitized review` (explicitly sanitized);
  only benign "portfolio-blind"-style mentions
- task body "position"/"ticker" hits: 1 each (benign context — matched Luna's scan)

## 4. Classification

> **PUBLIC-UNSAFE.**

Reason: metadata-safe for the SHARED IIP/IPM board does NOT equal public-internet-safe.
The snapshot exposes absolute local paths (incl. Windows username), internal
research/operational prompts, internal artifact names, model-routing detail, and
full event/run history — none of which were designed for public exposure. No
secrets or portfolio data, but the content is internal operational material.

## 5. Remediation options (NO action taken — Founder authorization required)

| Option | Effect | Destructive? |
|---|---|---|
| **A. Stop publishing raw DBs** (recommended): remove snapshot from tree going forward + `.gitignore` `stage8-preflight-baseline/*.db*`; keep the file locally (it remains on disk; blob STAYS in public history) | Stops future exposure; history retains the blob | No (non-destructive) |
| **B. Purge from history**: `git filter-repo` / `filter-branch` on `8ed372e` blob + force-push (requires push-force; GitHub may retain cached copies in forks/PRs; rewrites the 12-commit range SHAs) | Removes blob from history | YES — history rewrite + force-push; needs explicit authorization |
| **C. Keep + document**: accept the exposure (content has no secrets/portfolio data), document the assessment | No change | No |
| **D. Make repo private** | Removes public exposure | Policy change |

## 6. Future rollback-checkpoint pattern (evaluation — adopt after Founder pick)

For `stage8-preflight-baseline` and any future checkpoint, store in the repo ONLY:
- sha256 of the DB (immutable hash);
- sanitized board export (titles + statuses + counts, NO bodies/comments/paths);
- task/state counts;
- backup location OUTSIDE the public repository (e.g., `iip-harness-prep/evidence/harness/stage8-preflight-baseline/` — separate private worktree — or a local backup dir);
- NEVER the raw SQLite DB / board DB binary.

This preserves rollback integrity (hash-verifiable, restore from the private backup
location) while keeping the public repo metadata-clean.

<!-- 2026-08-13 15:05 UTC+7 (artifact_timestamp.py clock basis) -->
