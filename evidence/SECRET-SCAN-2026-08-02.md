# SECRET SCAN — Investment Intelligence Platform

**Date:** 2026-08-02
**Scope:** Read-only verification — no files modified, nothing staged/committed, no history rewritten, no credentials rotated.
**Repo:** C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform
**HEAD:** 2c41c43 (2026-07-28 23:43:35 +0700) — main branch, 68 commits reachable (all branches + tags)
**Branches:** main, origin/main, agent/T0-phase5-arch, agent/T1-weak-signal, agent/T2-anomaly, agent/T3-hypothesis, agent/T4-radar
**Tags (7):** foundation-v0.1..v0.3, am-v0-design-plan-v0.1, am-v0-gate-a-structure-v0.1, project-definition-v0.1, iip-phase5-v1.0

---

## 1. Executive Verdict

**PASS WITH WARNINGS** — no secret was found in tracked files, untracked files, staged/unstaged changes, or anywhere in Git history across all branches and tags. The two Hermes credential stores (global .env + profile .env) live OUTSIDE this repository and were not read. Warnings are configuration/process risks, not committed secrets (see §8).

---

## 2. Files Inspected

| Scope | Files | Method |
|---|---|---|
| All tracked files (current) | 218 files via `git ls-files` | full listing reviewed; secret-pattern grep over all |
| All tracked content, ALL 68 commits (every branch + tag) | every blob reachable | `git grep -n -I -i -E <pattern> $(git rev-list --all)` |
| Untracked files | CODEBUDDY.md, evidence/COUNCIL_DECISION-full-review-2026-08-02.md, evidence/FULL_PROJECT_REVIEW-2026-08-02.md | read + pattern grep (ripgrep, respects .gitignore) |
| Modified files (unstaged) | PROJECT_STATE.md, frontend/package.json, package-lock.json, main.tsx, api/foClient.ts, pages/CheapQualityPage.tsx, FundamentalDetailPage.tsx, FundamentalQueuePage.tsx, types/fo.ts, operational/FOUNDERS-DECISIONS.md | full `git diff` + credential-pattern grep |
| Staged changes | AGENTS.md | `git diff --cached` + pattern grep |
| Ignore rules | .gitignore (root) + 4 subdirectory .gitignores | `git check-ignore -v` + content review |
| Hidden/credential-type files | repo-wide find | `.npmrc`, `.netrc`, `*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, `.*` files — none present |
| Hermes credential stores | C:\Users\Admin\AppData\Local\hermes\.env (global, 25,289 B) and profiles\iip\.env (profile, 25,262 B) | existence confirmed only — contents NOT read (per task rules) |

**Confirmed no tracked files match** env/config/secret patterns except benign `frontend/tsconfig*.json` + `vite.config.ts` (build configs, no credentials).

---

## 3. Commands Run

```bash
git status --short                          # working tree state (twice — tree mutates concurrently)
git diff                                    # unstaged changes, full
git diff --cached                           # staged changes, full
git ls-files                                # full tracked inventory (218 files)
git log --all --oneline --decorate          # 68 commits, all branches/tags
git log --all -p                            # full history patches; added lines filtered for credential patterns
git log --all --oneline -S '<string>'       # pickaxe probes (16 strings)
git log --all --oneline -G '<pattern>'      # regex pickaxe (equivalent coverage)
git branch -a ; git tag ; git stash list    # ref inventory
git check-ignore -v .env "**/.env" "*.env" ".env.*"
git grep -n -I -i -E '<pattern>' $(git rev-list --all) -- .   # every blob in every commit
find . -name '*.env*' -o -name '.npmrc' -o -name '*.pem' ...  # credential-file hunt
```

Patterns scanned (case-insensitive): `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `sk-<16+ alnum>`, `AKIA<16 A-Z0-9>`, `ghp_/gho_/github_pat_`, `xox[bap]-`, `BEGIN (RSA|OPENSSH|EC|DSA|PGP) PRIVATE KEY`, `postgres(ql)://user:pass@`, `mongodb://`, `supabase`, `eyJ...` (JWT), `client_secret`, `Authorization: Bearer`, `api_key`/`apikey`/`API_KEY` assignments, `password=`/`password:` assignments, `token=` assignments, `access key`, `private key`, `secret key`, `token`.

**Tooling note:** gitleaks / trufflehog / git-secrets are NOT installed. Per task rules nothing was installed; scanning used git-native grep/pickaxe + manual pattern review. A sanity probe (`git grep -l AGENTS.md $(git rev-list --all)`) returned exit 0, proving the pattern engine searched all 68 trees (zero-match results are real, not a broken command).

---

## 4. Current Working Tree Findings

| Question | Finding | Evidence |
|---|---|---|
| Secrets in tracked files? | **NONE.** Zero matches for all credential patterns across all tracked files. | TEST_VERIFIED |
| Secrets staged? | **NONE.** `git diff --cached` (AGENTS.md loop-protocol edit) — zero credential matches. | TEST_VERIFIED |
| Secrets in untracked files? | **NONE.** CODEBUDDY.md + evidence/*.md (Council decision + full review reports) — zero matches. | TEST_VERIFIED |
| Profile .env tracked/ignored? | **Not in repo.** Lives at `~/AppData/Local/hermes/profiles/iip/.env` — outside the repository, cannot be tracked here. Root `.gitignore` line 2 ignores `.hermes/` inside the repo ("may contain credentials, never commit"). | STATIC_OBSERVATION |
| Global .env tracked/ignored? | **Not in repo.** Lives at `~/AppData/Local/hermes/.env` — outside the repository. Same `.hermes/` protection for any repo-local copy. | STATIC_OBSERVATION |

**⚠️ Concurrent mutation observed:** the working tree changed between scan passes — `git status` grew from 2 modified files to 6 modified (frontend package.json/package-lock.json/main.tsx/foClient.ts/pages + FOUNDERS-DECISIONS.md FD #44) plus 2 untracked, consistent with the FD #44 "Full Project Review Recovery" task being implemented by a concurrent session. HEAD stayed at 2c41c43. All diff content was scanned for credentials — zero matches (only doc prose and the @tanstack/react-query dependency addition). **This scan is a point-in-time snapshot; re-run after the recovery task commits.**

---

## 5. Git History Findings

| Question | Finding | Evidence |
|---|---|---|
| Any secret ever in any commit? | **NO.** Blob-grep of all 68 reachable commit trees: zero matches for any credential pattern. | TEST_VERIFIED |
| Introduced by which commit/file/line? | N/A — no secret found. | — |
| Still present in current history? | N/A. | — |
| Removed but recoverable? | N/A — never entered history. | — |
| Added-line scan | `git log --all -p` filtered to added lines matching credential patterns: **zero lines** in the entire history of every branch. | TEST_VERIFIED |
| Pickaxe probes | 16 named strings (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `supabase`, `client_secret`, `BEGIN RSA/OPENSSH PRIVATE KEY`, `postgres://`, `postgresql://`, `mongodb://`, `Authorization: Bearer`, `API_KEY`, `api_key`, `apikey`, `access key`, `secret key`): **zero commits** ever added/removed them. | TEST_VERIFIED |
| Prose-only hits (benign) | "private key" appears in 3 commits — `60a1522`, `115e90a`, `bbee00c` — exclusively in security guidance prose: "never request or store broker credentials, private keys…" (hermes/HERMES-ONBOARDING-PROMPT.md:16, operational/SECURITY-AND-UNTRUSTED-CONTENT.md:65). "token" appears in 5 commits as prose; no token VALUES matched any key pattern. | STATIC_OBSERVATION |
| Reflog / dangling objects | Not scanned (reachable refs only). See residual risk R5. | MISSING_EVIDENCE |

---

## 6. .gitignore Findings

| File / pattern | Protected? | Rule |
|---|---|---|
| `.env` (any directory) | ✅ YES | `.gitignore:15` — `.env` |
| `.env.local`, `.env.production`, any `.env.*` | ✅ YES | `.gitignore:16` — `.env.*` |
| `.hermes/` (Hermes session data — "may contain credentials, never commit") | ✅ YES | `.gitignore:2` |
| `nul` (Windows NUL device, blocks `git add -A`) | ✅ YES | `.gitignore:21` |
| `data/cache/*.json` | ✅ YES | `.gitignore:23` |
| **`*.env` (e.g. `prod.env`, `secrets.env`, `foo.env`)** | ❌ **NOT ignored** | no rule matches the `*.env` glob |
| `.npmrc`, `.netrc`, `*.pem`, `*.key`, `id_rsa*` | N/A — no such files exist in repo | STATIC_OBSERVATION |

**Could `git add .` stage a credential file today?** Only if someone creates a file matching no ignore rule — the realistic risk is a `*.env`-named file (`prod.env`, `staging.env`, etc.), which is **not** ignored. Exact `.env` and `.env.*` are safe. No .env-type file currently exists anywhere in the repo (find returned zero). Subdirectory .gitignores (alpha-momentum-v0, fundamental-opportunity-v0, institutional-intelligence-v0, frontend) contain no env/secret rules — they rely on inherited root patterns, which cover `.env`/`.env.*`/`.hermes/`.

---

## 7. Provider-Specific Findings (OpenRouter / OpenAI / Codex / ChatGPT OAuth / other providers)

| Provider credential | Ever committed? | Evidence |
|---|---|---|
| `OPENROUTER_API_KEY` | **NO** | -S pickaxe: zero commits; blob grep: zero matches; `git log --all -p` added-line scan: zero |
| `OPENAI_API_KEY` / `sk-…` keys | **NO** | same — zero |
| `ANTHROPIC_API_KEY` / `DEEPSEEK_API_KEY` / `GEMINI_API_KEY` | **NO** | same — zero |
| Codex credentials / ChatGPT OAuth tokens | **NO** | `codex`, `oauth`, `openai` appear in ZERO commit messages; no token/JSON-credential content in any tree |
| Any other provider config | **NO** | no `.npmrc`/`.netrc`/credential file ever tracked; no commit message mentions providers/secrets at all |

Where provider credentials actually live: the **global** `.env` (`~/AppData/Local/hermes/.env`) and the **profile** `.env` (`~/AppData/Local/hermes/profiles/iip/.env`) — both **outside this repository**. The profile copy (noted in prior governance-audit context as needed for Luna fallback) exists and is newer than the global copy — but it is a filesystem file, untrackable by this repo's git. Contents were NOT read during this scan.

---

## 8. Residual Risks

1. **`*.env` glob gap (R1)** — a future file named `*.env` (e.g. `prod.env`, `secrets.env`) would NOT be ignored and a `git add .` would stage it. Low likelihood today (no such file exists, `.env`/`.env.*` covered) but a real gap.
2. **Concurrent tree mutation (R2)** — the FD #44 recovery task is being written to the working tree right now. This scan is a snapshot; the concurrent session's output must be re-scanned at its closeout.
3. **No secret-scan tooling (R3)** — gitleaks/trufflehog/git-secrets absent; coverage relied on pattern-based git scans. Durable protection would need a tool or pre-commit hook.
4. **Hermes credential stores outside repo (R4)** — the actual provider secrets live in two .env files outside the repo. They are the real attack surface; they must never be copied into the repo (`.hermes/` + `.env.*` rules protect against accidental commits).
5. **Reflog/dangling objects not scanned (R5)** — `rev-list --all` covers reachable refs only. A secret in a garbage-collected dangling blob would be invisible here. Risk negligible given no secret ever reached any reachable commit.
6. **Obfuscated secrets (R6)** — pattern scans catch known formats/named keys; a deliberately obfuscated credential (e.g. base64 of a key in a config) cannot be fully ruled out. No config file with any credential-like value was found.

---

## 9. Recommended Remediation (report only — NOT executed; requires Founder approval)

| Priority | Action | Addresses |
|---|---|---|
| 1 | Add `*.env` and `!*.env.example` to root `.gitignore` | R1 |
| 2 | After the FD #44 recovery task commits, re-run this scan (or `gitleaks detect` if installed) | R2 |
| 3 | Install gitleaks (or equivalent) as a pre-commit hook for durable, tool-based coverage | R3, R6 |
| 4 | Keep the two Hermes .env files outside the repo; never copy provider credentials into repo files | R4 |
| 5 | (Optional) `git reflog expire` + `git gc --prune=now` if a full forensic sweep is ever wanted | R5 |

No secret was found, so no credential rotation, history rewrite, or removal is required.

---

*Scan performed read-only. No files modified, nothing committed, .gitignore untouched, no credentials rotated. Report created as evidence/SECRET-SCAN-2026-08-02.md per task requirements.*
<!-- 2026-08-02 05:00 UTC+7 -->
