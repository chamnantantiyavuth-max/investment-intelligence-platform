# IIP: GitHub handoff inspection (read-only)

> Published by Grok Bot (Grok Cloud) as a docs-only report for Founder / ChatGPT coordination. No ChatGPT review has occurred. Status: handoff NOT verified (see §8).

Date: 2026-10-17 (all times Asia/Bangkok, UTC+7)
Repo: https://github.com/chamnantantiyavuth-max/investment-intelligence-platform. It is PUBLIC; the default branch is `main`; last push was 2026-10-17 16:22.
Method: read-only (inspection only; no implementation changes). Used GitHub API metadata, an anonymous `git clone` onto the box (/workspace/iip/repo), a detached worktree for tests (/workspace/iip/testrun), and Vercel read-only listing. I created no branches, commits, PRs, issues or comments.

## 1. Branches / PRs
| Branch | Head | Date (UTC+7) | Last commit |
|---|---|---|---|
| main (default) | 5bf1077 | 2026-10-06 16:10 | docs(governance): FD #151 QAD M6 IMPLEMENTATION AUTHORIZED |
| impl/m6-gemini-notebook | 210610e | 2026-10-14 16:36 | docs(governance): FD #156 follow-up: notebooklm-py 0.8.5 compatibility probe = CLASS B (AUTHENTICATION REQUIRED) |
| plan/grok-cloud-migration-20261017 | 5240097 | 2026-10-17 16:22 | docs: stage unified Grok Bot cloud migration and IIP master plan |
| ops/automation | 9e7d95e | 2026-10-04 01:44 | Merge origin/main into ops/automation (cron artifacts up to 2026-10-03) |
| wip/deferred-ops-backlog-20260921 | 8546fd4 | 2026-09-21 11:25 | feat(radar): weekly scan 2026-09-21 |
| wip/o3-pre-ruling-docs-20260923 | d915f96 | 2026-09-21 15:00 | docs(ops): session closeout POST-M5.3 O1 + O3 |
| docs/m6-gemini-notebook-dr | a37e92d | 2026-09-09 15:25 | docs(plan): M6 design-gate compatibility items |
| wip/pre-m53-cp3-local-docs-20260913 | cab62fc | 2026-09-12 22:42 | docs: cron review 12 Sep EVENING tick |
| harness/stage2-prep | fa336ab | 2026-08-20 17:07 | feat(int-g2.1): council sandbox scripts |

- PRs: **none, open or closed** (the API returned an empty list). No tags. No branch protection.
- Older side branches carry unmerged commits that are not in impl: ops/automation 4, wip/deferred-ops 13, wip/o3 1, wip/pre-m53 11, docs/m6-dr 2, harness 33. All are cron artifacts, docs or harness work from Aug–Sep. They're historical, but they're still unmerged.
- Commit authors: 787 "Chamnan Tantiyavuth", 2 "Hermes Cron", and 1 "chamnantantiyavuth-max" (the plan commit, made through the web UI). Hermes commits under the Founder's git identity.

## 2. impl/m6-gemini-notebook
- **87 ahead / 0 behind main**, 141 changed paths, 725 commits in its history. This matches what MASTER_PLAN §B says.
- Last 15 commits (all by Chamnan Tantiyavuth = Hermes):
  - 210610e 10-14 16:36 FD #156 follow-up, 0.8.5 compat probe = CLASS B (AUTH REQUIRED)
  - a163749 10-14 16:24 FD #156, M6.7 remote sync + M6.8 Stage A read-only transport feasibility
  - 57d8972 10-14 16:12 qad-m6.7 FD #151 CLOSED, Round-2 verdict B
  - 30b0ece 10-14 15:58 fix(qad-m6.7) request/run identity preflight
  - 891523c 10-14 15:20 M6.7 independent review = C, evidence
  - e8fd966 10-14 14:59 feat(qad-m6.7) provider adapter + deterministic mock transport (MOCK ONLY)
  - c288aeb 10-14 13:14 M6_RAW_SUCCESS_API_GATE CLOSED (FD #155)
  - f077164 10-14 13:13 FD #155 Path H evidence
  - fa449cd 10-14 12:57 fix(qad) M6.3 public SUCCESS APIs hardened
  - e10e3ad 10-14 12:45 FD #155 governance
  - b8eb25c 10-12 16:46 M6.6 CLOSED (round-17 = B)
  - cb8411e 10-12 16:45 M6.6 round-17 evidence
  - d67f2a6 10-12 16:31 fix(qad) M6.6 round-17
  - 1b533f0 10-12 15:39 M6.6 round-16 = C state
  - c3f8d86 10-12 15:39 M6.6 round-16 evidence
- Latest Hermes work on GitHub covers M6.1–M6.7 (CLOSED, MOCK ONLY) and the M6.8 **Stage A read-only probes only**.
- **Possibly unpushed. These are referenced but absent from GitHub:**
  - Local HEAD `f62ac8f6529f34da12ec856558870d80de699bfc`, described as 2 commits beyond 210610e. MASTER_PLAN §B cites the Hermes transcript of 2026-10-14. That object is not in any remote branch (`git cat-file` fails).
  - `evidence/m6.8/LIVE-DEEP-RESEARCH-SMOKE-2026-10-14.md` does not exist on any branch.
  - Any post-login re-probe or live Deep Research record. The newest remote evidence says auth expired and "Founder action: interactive login" (`evidence/m6.8/STAGE-A-CORRECTION-AND-085-COMPAT-PROBE-2026-10-14.md` §6).
  - Any M6.8 live adapter code. `qad/m6/` holds only mock_transport.py and mock_proof.py, with no NotebookLM transport.
  - Hermes-local runtime: `~/.hermes/profiles/iip/SOUL.md` and `user.md` (AGENTS.md lines 3, 11–12), the `m68-venv-085` venv, the auth profile, the cron jobs.json, and the `hermes_cli` Python package that tests import. None of these are in Git, which is expected.

## 3. MASTER_PLAN.md
- It exists only on branch `plan/grok-cloud-migration-20261017`, at **repo root** `MASTER_PLAN.md` (252 lines). There is no folder named `plan/grok-cloud-migration-20261017/`; that string is the branch name. The branch is 1 commit (5240097) on top of 210610e and adds only this file.
- Summary:
  1. Status is "PROPOSED — NOT YET ADOPTED". It can't override the Constitution, FDs, QAD contracts or test evidence.
  2. Adoption order: reconcile unpushed Hermes commits, integrate the plan into the dev branch, make AGENTS.md portable, then mark ACTIVE.
  3. Scope: QAD research platform. No trading, allocation or broker actions. Provider replaceability (DNA-014) is kept.
  4. §B snapshot (verified against GitHub) and the local claim (unverified): f62ac8f plus smoke results of 48 results, a 33,032-char report, 3 imported sources and 19 citations.
  5. Document authority table: MASTER_PLAN = roadmap, PROJECT_STATE = verified status, Constitution/FDs/QAD contracts = binding. Old plans are kept as history.
  6. Architecture: Lead Bot → Cloud coding agent / QAD Research Lead / Skeptic. GitHub is canonical. Production (Vercel/backend/DB) is kept separate. NotebookLM goes behind an isolated adapter with fallback, and no Windows cookies are copied to the cloud.
  7. Usage: quota isn't known. Measure 3 representative jobs and avoid auto top-up.
  8. Lean team of 3 roles plus on-demand specialists, with an evidence contract per case (DISCOVERED → … → RESEARCH_READY).
  9. WPs: WP0 handoff reconcile → WP1 cloud coding pilot (`feat/grok-pilot-*`, no main merge) → WP2 runtime inventory → WP3 M6.8 adapter portability (read-only/no-auth probe first; classify REAUTH_REQUIRED / PROVIDER_UNAVAILABLE / REGION_EGRESS_BLOCKED) → WP4 one real QAD case → WP5 at most 1 scheduled task. All 5 cron jobs stay PAUSED.
  10. Next action: WP0. Hermes pushes the local M6.8 evidence first, then Grok runs WP1.
- **Conflicts / tensions to resolve during adoption (none is a blocker for read-only work):**
  - AGENTS.md lines 3/11–12 inherit `~/.hermes/profiles/iip/*` and line 230 uses a Windows-local user path (`C:\Users\<user>\...`). PROJECT_INDEX.md lists Windows root and vault paths. The plan itself flags these as non-portable.
  - The FD #144 "IIP Windows Mode A operating contract" and its Gate G scheduling are Windows/Hermes-specific. Migrating needs an FD-level note, not a silent override.
  - FD #151 / PROJECT_STATE "Next allowed action" require per-cluster RED→GREEN plus a **family-independent** review (FD #143 routing). The plan's "risk-based review, ChatGPT as auditor, no review loops" is looser, and it needs a Founder decision that maps ChatGPT review onto the family-independent requirement.
  - The plan's "tests proportional; don't require the full historic suite" sits against the PROJECT_STATE Build Metrics practice of a full-suite count. Compatible if the inherited failures are documented.
  - PROJECT_INDEX authority map ranks "approved implementation plans" at #4. The plan's own text says it stays subordinate to approved plans like `design/qad-pivot/REVISED-QAD-MASTER-PLAN.md`, so as written there's no conflict.

## 4. M6.8 NotebookLM live smoke evidence: **ABSENT on GitHub** (only Stage A probes are PARTIAL)
- Present: `evidence/m6.8/STAGE-A-TRANSPORT-PROBE-2026-10-14.md` (0.7.3, "CSRF token not found", transport non-functional) and `evidence/m6.8/STAGE-A-CORRECTION-AND-085-COMPAT-PROBE-2026-10-14.md`. The second shows: isolated venv with Python 3.11.15; `notebooklm-py==0.8.5` installed and `pip check` clean; CLI 0.8.5 (50493ddf); `doctor` local auth ✓; but `auth check --test --passive` → **"Authentication expired or invalid"** and `list --backend web` → signed-out page redirecting to sign-in. **Classification B: AUTHENTICATION REQUIRED.** There was no login, no Deep Research, no source import and no Q&A. The main Hermes env is still 0.7.3.
- Also present: `evidence/m6.7/TRUST-BOUNDARY-AND-M6.8-ACCEPTANCE-REQUIREMENT-2026-10-14.md` (acceptance rules M6.8 must meet).
- Absent: successful auth, Deep Research run, source import, grounded citations, `LIVE-DEEP-RESEARCH-SMOKE-2026-10-14.md`.

## 5. Structure / runtime / tests / CI
- 1,212 tracked files (impl+plan). Main dirs: `qad/` (QAD core: contract, models families A–I, persistence, m53, m6 provider/ledger/orchestration/mocks), `backend/` (FastAPI, `backend/main.py`, auth, SQLite stores), `api/index.py` (Vercel serverless entry), `frontend/` (React/Vite/TS), legacy modules (`alpha-momentum-v0`, `close_system`, `fundamental-opportunity-v0`, `institutional-intelligence-v0`, `discovery`), `tests/` (locked, ops, qad, py314), plus docs/governance (`operational/`, `design/`, `evidence/` 318 files, `research/` 150 files).
- Python: the docs target 3.11 (start-backend.sh says "3.11 venv"). Dependencies are only `backend/requirements.txt` and `api/requirements.txt` (fastapi, uvicorn, pydantic≥2, PyYAML). There's no pyproject or lockfile and pytest isn't listed; tests also need httpx, and one needs `hermes_cli`. Frontend: `frontend/package.json` (Node; built fine with Node 20.19).
- Tests: `pytest.ini` → testpaths=tests, norecursedirs=py314. Extra locked tests live in module folders (`*/test_locked/`).
- **Box run (Python 3.11.17, impl HEAD 210610e):** 1,331 collected. With `tests/test_capital_office_semantics.py` excluded (ModuleNotFoundError `hermes_cli`): **1,307 passed, 23 failed, 1 error, 20.1s**. **QAD M6 subset: 494/494 passed.**
  - 2 failures (`tests/qad/test_contract_conformance.py`): "Build artifact drift" across 12 generated files. **Root cause confirmed:** the recorded hashes are SHA-256 of CRLF checkouts (Windows autocrlf). For example, family_a.py: LF f1ee68c7055e, CRLF 1a83970964f6 = recorded. Git stores LF, so this fails on any Linux/cloud checkout. PROJECT_STATE already calls it "known inherited `test_schema_build_identity`".
  - 21 failures + 1 error (`tests/locked/test_real_data_api.py`, `test_org_workflow_api.py`): these need gitignored runtime artifacts (`alpha-momentum-v0/output/pipeline_result.json`, kanban/holds data), giving 503 or KeyError. They depend on the environment, not on code regressions. One code-hash mismatch is also likely CRLF.
- Frontend: `npm ci` + `npm run build` pass (exit 0; chunk-size warning only).
- **CI: none.** There is no `.github/` on any branch, so no GitHub Actions and no workflow runs.

## 6. Documented state vs actual
- PROJECT_STATE "Next allowed action" (line 138) still says M6.7 is "local commit e8fd966 … nothing pushed". It's actually pushed, and M6.7 is CLOSED at 57d8972.
- Build Metrics: "Python tests 863/863 PASS (24 Sep)". Actual: 1,331 collected now; on Linux, 23F+1E+1 collection error. Frontend build metric dated 2026-08-13.
- Build Metrics "FDs approved #1–154", but the FD register has #155 and #156.
- The top PROJECT_STATE entry records the remote at a163749. The remote is now 210610e, which is the commit that records that entry itself, so this is consistent.
- "Open constraints: No active blockers." But M6.8 is blocked on interactive NotebookLM re-auth (Founder action).
- AGENTS.md line 175 says "Provisional technology: Python + pandas + Jinja2". The actual stack is FastAPI + React/Vite. AGENTS/PROJECT_INDEX depend on Windows/Hermes paths.
- PROJECT_STATE.md is 425 KB and SESSION_CLOSEOUT.md is 185 KB. Neither is a "compact bootstrap state" in practice.

## 7. Cron / deployment / secrets
- **Vercel** (`vercel.json`: frontend build + `api/index.py` serverless; homepage investment-intelligence-platform-six.vercel.app). The project `investment-intelligence-platform` is Git-connected and **auto-deploys a Preview on every branch push**. The latest Preview was branch plan/... at 5240097, 2026-10-17 16:22 READY; impl 210610e at 2026-10-14 16:56 READY. **Latest Production: main 5bf1077, 2026-10-06 16:10, READY.** Implication: any feature-branch push triggers a Vercel preview build, but not production.
- Cron: there are no scheduler configs in the repo and no GitHub Actions schedules. The IIP cron jobs live in the Hermes Windows profile (`profiles/.../cron/jobs.json`, per `operational/cron-operations-findings-20260914-21.md`). The repo says "5/5 cron PAUSED". The last cron artifacts on `ops/automation` are dated 2026-10-03/04, which is consistent with them being paused. I can't verify Windows-side state from the cloud.
- Secrets (flag only): there's no `.env`, storage_state.json, cookie file, credential JSON, key, or `.db` tracked on any branch or in history by filename. A content regex scan of impl HEAD (GitHub/OpenAI/OpenRouter/AWS/Google API keys, Slack, Telegram bot tokens, private keys, Google SID cookies) found **0 matches**. `.env.example` IIP_AUTH_* values look like placeholders. The only personal data found is the Founder's personal email address, which appears in git commit author metadata on a public repo. Note that `research/companies/...` holds investment research in the PUBLIC repo; MASTER_PLAN §A flags this.

## 8. Verdict
**Partially.** Everything through **210610e** (M6.1–M6.7 CLOSED + M6.8 Stage A probes, 2026-10-14 16:36) is safely on GitHub, and its tests pass where they don't depend on Windows. **The latest claimed Hermes work is NOT on GitHub:**
- local HEAD `f62ac8f6529f34da12ec856558870d80de699bfc` (2 commits beyond 210610e) is missing;
- `evidence/m6.8/LIVE-DEEP-RESEARCH-SMOKE-2026-10-14.md` is missing, along with any record of 0.8.5 live auth, Deep Research (48 results / 33,032 chars), the 3 imported sources and the 19 grounded citations;
- whether any Windows work happened after f62ac8f is unknown.
These need to be fast-forward pushed from the Windows laptop (WP0 step 2). Until then, M6.8 live status on GitHub = AUTH REQUIRED / not implemented. Do not recreate it.

### Candidate WP1 fixes (evidence-based, not started)
1. Make the build-identity hash check EOL-independent, or add `.gitattributes eol=lf` and regenerate the hashes. This fixes 2 failures on Linux, but it touches canonical build identity, so it may need Founder/FD sign-off.
2. Make tests that need gitignored artifacts skip cleanly (or use fixtures) when artifacts are absent. Also make `hermes_cli` an optional import.
3. Add a minimal `requirements-dev.txt` (pytest, httpx) plus a GitHub Actions test workflow, without schedules.
