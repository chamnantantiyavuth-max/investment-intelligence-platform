# IIP MASTER PLAN — Grok Bot Cloud Handoff & Full Integration

**Version:** 2026-10-17 / migration candidate 1  
**Status:** `PROPOSED — NOT YET ADOPTED` (staged on a separate planning branch; do not represent as merged, approved, deployed, or operational)  
**Target repository:** `chamnantantiyavuth-max/investment-intelligence-platform`  
**Migration source:** Hermes on the Founder's Windows laptop  
**Target workflow:** Grok Bot as cloud-based engineering coordinator + bounded QAD research team, primarily operated from mobile  
**Priority:** working software and verifiable research results > perfect process.  
**Scope:** execution/ownership migration; **NOT** a change to the IIP product constitution or permission for live brokerage/trading.

> **One operational entrypoint after adoption:** This file is the sole current *execution roadmap and handoff entrypoint*. It links to binding contracts rather than duplicating them. Older files containing `PLAN`, `ROADMAP`, or `v0.x` become historical/domain references for execution sequencing, not competing instructions. This file **cannot override** the Constitution, approved Founder Decisions, approved QAD contracts, or real implementation/test evidence.
>
> **Updated sequencing (Founder instruction, 2026-10-17):** Grok Cloud WP1 is authorized to proceed NOW from the last verified remote development HEAD without waiting for the absent Hermes local commits. Reconciliation of those local commits is DEFERRED, not waived or reconstructed. Keep the pilot on a new isolated branch. The plan remains PROPOSED until adopted after scoped merge and authority reconciliation; existing approved contracts remain authoritative.

### 2026-10-17 Founder execution decision — remote-first cloud pilot

The Founder cannot access the Windows/Hermes computer during an extended holiday and has explicitly directed Grok Bot to **start the next cloud work package without waiting**. This is a scope-limited execution instruction: it authorizes WP1 cloud engineering and safe feature-branch PRs against GitHub-verified code, **not** promotion of missing local evidence, changes to binding QAD policies, an M6.8 live success claim, production deployment, paid overages, activation of scheduled jobs, or edits to the Founder's laptop. The absent local commits remain `DEFERRED_SYNC`; do not treat them as blockers for unrelated cloud-portable work. When source paths conflict, preserve both branches and use a normal merge/cherry-pick workflow after verifying ancestry.

## A. Product objective and non-negotiable boundaries

IIP is currently a **Quality at Dislocation (QAD) investment intelligence and underwriting research platform**: discover quality businesses, detect dislocation, distinguish temporary impairments from permanent deterioration, build evidence-backed cases, preserve dissent, and return Founder-reviewable research. See `00-FOUNDERS-MANIFESTO.md`, `01-PROJECT-DNA.md`, `02-PROJECT-CONSTITUTION.md`, `operational/PRODUCT-VISION.md`, and the approved QAD domain contracts.

- Do **not** silently repurpose IIP into the Founder's live trading journal, portfolio manager, brokerage execution engine, or Capital Command. Historical AM, Close System, FO, and institutional modules remain as governed; they are not automatically production QAD capabilities.
- AI may analyze, discover, investigate, disagree and recommend research. It does not place trades, allocate real capital, or modify broker accounts.
- No redesign of QAD contract semantics just because Grok Bot is replacing Hermes. Preserve provider replaceability (`DNA-014`).
- No assertion that a model's citations alone establish verified evidence. Retain actual source, observed date/PIT, audit trail, contradiction, and provenance.
- The private `grok-research-team` repository belongs to a different earlier research workflow and is presently a separate/minimal repository. **Do not automatically merge its code, history or authority into IIP.** Reuse roles or insights only after scoped inspection and explicit designation.
- The IIP repository is **PUBLIC** at the time of this review. Never commit personal notes, account data, paid reports without rights, private strategy ideas, provider credentials, cookies, or tokens. Decide on changing visibility and downstream deployment impacts separately.

## B. Verified source snapshot (GitHub check: 2026-10-17)

### Remote facts — independently inspected

| Item | Verified state |
|---|---|
| Repository/default | `chamnantantiyavuth-max/investment-intelligence-platform` / `main` |
| `origin/main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` |
| Active development | `impl/m6-gemini-notebook` |
| Remote development HEAD | `210610e48b8d63ab678bd7bb5ec40a6b1cddac4e` |
| Ahead vs main | 87 commits / 141 changed paths (at inspected refs); 0 behind |
| QAD | Founder-approved QAD pivot, M6.7 completed per remote `PROJECT_STATE.md`; M6.8 live adapter not implemented at remote head |
| Cron | 5/5 PAUSED per existing evidence; do not resume by migration |
| Canonical schemas | 68 per latest recorded project evidence; verify on execution |
| Stack | Python / FastAPI and React / Vite / TypeScript; verify package/runtime compatibility in target |
| Cloud portability | `AGENTS.md` and `PROJECT_INDEX.md` still refer to Windows/Hermes-local paths; cannot be assumed available to Grok cloud |

### Founder-provided local evidence, NOT yet remote-verified

The Hermes transcript dated 2026-10-14 reports local HEAD `f62ac8f6529f34da12ec856558870d80de699bfc` with **two commits not pushed** beyond remote `210610e`. These reportedly record an isolated `notebooklm-py 0.8.5` live smoke test: authentication valid, Deep Research completed (48 results, 33,032-character report), 3 cited sources imported, 19 grounded structured citations. This is an important positive signal, **not** a remote-verified M6.8 implementation.

- Evidence claimed locally: `evidence/m6.8/LIVE-DEEP-RESEARCH-SMOKE-2026-10-14.md`.
- Existing Windows auth profile and `m68-venv-085` live **outside Git** and will not migrate in a clone.
- The repository's main Hermes environment still reportedly uses `notebooklm-py 0.7.3`; isolated successful client used `0.8.5`.
- A prior prompt authorized implementing M6.8 live adapter, but **no successful implementation/result is provided yet**. Treat as OPEN until current evidence confirms otherwise.

**Handoff integrity rule:** Compare origin HEAD, local HEAD, parentage, worktree, commits and `git status`. Fast-forward only; no forced pushes, hard resets, secret transfers, branch overwrites, or claiming a local test as remotely verified.

## C. Document authority — one source of execution truth, without erasing history

| Purpose | Canonical place after adoption |
|---|---|
| Current objectives, execution phases, next tasks, integration decisions | **`MASTER_PLAN.md`** (this file, when adopted) |
| Verified current build state, commit/test evidence, blockers | `PROJECT_STATE.md`, concise factual state **not an alternative roadmap** |
| Highest-order investment/product constraints | `02-PROJECT-CONSTITUTION.md` + approved amendments |
| Explicit approved decisions | `operational/FOUNDERS-DECISIONS.md` |
| Investment domain and accepted QAD behavior | `01-PROJECT-DNA.md`, approved `project-definition/`, `design/qad-pivot/` canonical specs/contracts where ratified |
| Agent loading/rules/commands | `AGENTS.md` (make platform-neutral in a separate scoped commit) |
| Application source/tests | `qad/`, `backend/`, `frontend/`, `tests/` |
| Exact research inputs, sources, result provenance | structured IIP evidence/ledger and bounded `research/`, `reports/`, `evidence/` artifacts |
| Prior plans/design decisions | historical references only; never silently rewrite approval records |

### Agent bootstrap after adoption

1. Read `MASTER_PLAN.md` and latest concise `PROJECT_STATE.md`.
2. Read `AGENTS.md` and only **relevant** approved contract/source files for the current task.
3. Check Git branch SHA, `git status`, and latest tests; reconcile factual conflicts using code and evidence.
4. Choose **one narrow deliverable**, make it work, run targeted tests, record output/commit, report next action.
5. Do not auto-load every previous `PLAN` or `SESSION_CLOSEOUT` into context; search them only for a named unresolved question.
6. No review→correction→review loop unless a material defect affects functionality, integrity, security, or a binding contract.

**If another plan appears to disagree:** interpret it in its original historical scope; do not let an unratified old planning draft supersede a verified current commit or binding contract. Escalate only a material authority conflict, naming both exact sources.

## D. Target architecture (minimum viable hybrid)

```text
FOUNDER (Grok Bot iOS / desktop)
   │ idea, QAD candidate, coding task, approvals
   ▼
IIP Lead Bot (cloud, owns task + GitHub handoff)
   ├── Grok Cloud Coding Agent → feature branch → tests → PR
   ├── QAD Research Lead → investigator(s) when needed → sourced memo
   └── Skeptical Evidence Reviewer → counter-case/citation/source checking
                │
                ├── IIP GitHub: code, plans, tests, public-safe evidence
                ├── Persistent IIP storage/service: deployed runtime and data
                └── NotebookLM adapter (verified provider path, not assumed)
```

**Separate the control plane from production.**

- **Grok Bot cloud computer** is an interactive/recurring agent workspace: persistent per user, usable when the laptop is off, but **not a service uptime/SLA substitute**.
- **GitHub** is the canonical source-control and code-review channel.
- **IIP deployed backend and database** remain separately hosted/deployed as already approved. Do not move live data into the Bot's local filesystem, nor rebuild existing deployment without need.
- **NotebookLM** is an external research tool. Its consumer web/CLI transport is unofficial/uncontracted for permanent headless API operation, may require reauthentication and may be blocked from datacenter egress. Prefer an isolated adapter with failure status and a provider-independent fallback.
- If NotebookLM cannot authenticate on Grok cloud, use **a minimally scoped separate worker** only if a real IIP workflow requires unattended research; do not export the Windows Google `storage_state.json`, primary Google session, or master token to a shared cloud computer as a shortcut.
- Grok Bot does not provide a per-Bot secret-isolation boundary: Bots on the same account **share one cloud computer** and its available files/browser sessions. Use least-privilege connectors and restrict cloud credentials.
- Keep autonomous trade execution, portfolio actions and broker credentials OUTSIDE IIP.

## E. Grok Bot capabilities, known constraints and pilot questions

Official Grok Bot documentation as reviewed 2026-10-17: paid Cursor individual plans are eligible, mobile can interact with the same cloud Bots, Bots can delegate to Cloud Agents, and Bots/Routines can work while the laptop is closed. Actual account entitlement remains unverified until login.

**Usage:** Weekly included allowance, with on-demand/overage possibilities depending on account. A large multi-agent coding + research workload will consume more usage than chat. The exact **account-specific quota, remaining allowance, and price** are NOT known from this repository or public documentation. Inspect `Usage & Billing` / Cursor account, select a monthly on-demand spend cap if available, and measure first three representative tasks (small code change, test run, one research case) before adding more agents or recurring jobs. Avoid auto top-up/unlimited spend until budget is known.

**Cloud limitations to check by hands-on test:**
- GitHub OAuth permission, branch/PR push, CI/status visibility, bot notifications on mobile;
- computer runtime (Python/node, disk/CPU/memory, network, execution timeouts) and durable files across app restart;
- Google NotebookLM login and consumer CLI `0.8.5` functionality from cloud egress;
- GitHub actions or existing external CI for heavy builds;
- latency and quota with 1 coordinator and 1-2 task agents;
- approval prompts: unattended approval may expire; design work to stop safely and resume.

**Security:** This repository is public. Research drafts about holdings and private ideas go into an approved private storage/repo, not public `reports/`. No shared browser session should be treated as restricted to a single Bot.

## F. Research Team — start lean, expand only on evidence of value

### Persistent Bots / roles

1. **IIP Lead Bot** — one accountable owner for the repo, coding backlog, triage, branch handoff, releases. Converts mobile requests to one scoped task, coordinates Cloud Agents and reports concise Thai updates.
2. **QAD Research Lead** — discovery and deep research on **Quality at Dislocation**; does not presume price drop is temporary, seeks sources and causes, writes a traceable investment research memo, never executes trades.
3. **Independent Skeptic** — not a duplicate writer; challenges source authority, point-in-time claims, accounting adjustments, alternative structural-damage thesis, false-confidence, and citation/claim bindings.

**On-demand subagents** (not persistent Bots initially): Filing / Financial Statements Analyst, Industry/Scuttlebutt Investigator, Valuation/Quant, Citation/Source Checker, Engineering Test Runner. Spawn only with a falsifiable research question and bounded sources/cost. Existing QAD scuttlebutt contract has a default investigator concurrency of three; do not bypass it with an autonomous swarm.

### Evidence and decision contract for each research case

`request_id`, company/security identity, thesis question, as-of time, permitted data scope, source URLs/document IDs and publication dates, observation date, extracted claims, contrary evidence, unknowns, financial calculations, citation-to-source bindings, reason for decision relevance, case artifacts and versions, whether Founder-reviewed.

- Distinguish `DISCOVERED`, `SOURCE_IMPORTED`, `CLAIM_EXTRACTED`, `SOURCE_VERIFIED`, `PIT_VALIDATED`, `RESEARCH_READY`. Do not equate citations generated by NotebookLM with IIP independent verification.
- The Skeptic receives the primary evidence, not only the Lead's summary. Preserve disagreements and original versions.
- Default output: concise Thai executive view + one grounded English/Thai research memo and evidence appendix as warranted. No theatrical role-play or 10 parallel essays for simple questions.
- Store outputs back in the **IIP** canonical data/evidence path; use the older `grok-research-team` repository only for separately authorized workflows, never as an implicit second IIP authority.

## G. Migration execution — dependency-ordered work packages

### WP0 — Remote-first handoff with deferred local reconciliation (Cloud development NOT blocked)

**Owner:** Grok validates remote facts now; Founder/Hermes reconciles missing local-only work when the laptop becomes available.

1. **NOW — remote/cloud path:** Validate `origin/impl/m6-gemini-notebook` @ `210610e` (or its actual verified descendant), and use that remote commit as the cloud WP1 baseline. Record absent local evidence honestly. Do not infer that local M6.8 success was pushed, and do not recreate its proof.
2. Start WP1 on a **new isolated cloud feature branch** immediately, preserving source-control ancestry and existing QAD contracts. Running cloud tests and making a scoped code improvement does not depend on a Windows notebook session.
3. Adapt the Grok cloud bootstrap in `AGENTS.md` to remove blocking assumptions that Hermes-local profile paths exist, without deleting historical rules or treating a synthetic substitute as equivalent to a missing approved local source. Link this Master Plan as the proposed execution roadmap.
4. **LATER — local reconciliation:** When the Windows machine becomes available, inspect local status, HEAD, untracked files and unpublished commits; check for secrets; verify `f62ac8f` ancestry and subsequent work; cherry-pick or merge safely onto a dedicated integration branch using normal Git ancestry. No hard reset, force push, overwrite of Grok's new work, or automatic trust promotion of local-only evidence.
5. Adopt this plan as `ACTIVE` only after the necessary scope/authority reconciliation and explicit Founder decision; do not hold WP1 hostage to that adoption or laptop availability.

**Immediate Done condition:** Grok cloud produces a genuinely tested feature/portability PR anchored to a verified remote commit, without any claim that Hermes-local evidence was migrated. **Deferred Done condition:** eventually reconcile Windows-only work separately, preserving both lines of work.

### WP1 — Grok Cloud GitHub and mobile coding pilot (AUTHORIZED TO START BEFORE WP0 LOCAL SYNC)

1. Connect Grok Bot to the IIP GitHub repo with minimal needed permissions.
2. Clone branch/repository on Grok cloud; read `MASTER_PLAN.md`, `PROJECT_STATE.md`, portable `AGENTS.md`. Confirm Python/Node versions and tests.
3. Have a Cloud Coding Agent deliver **one small genuine code or developer-experience fix** from an existing test-backed task, isolated on `feat/grok-pilot-*`.
4. Run targeted tests + applicable gate checks; push feature branch, show diff and link to PR from the iPhone; no `main` merge / production deployment in this pilot.
5. Measure usage, elapsed time, tool compatibility and ability to review/approve from mobile.

**Done when:** a reproducible, tested code change is created by Grok cloud and reviewed on phone, without the laptop.

### WP2 — Existing IIP runtime and storage inventory (no rebuild)

1. Identify what is actually deployed now (hosting, DB, secrets, scheduler, object storage, frontend URL, GitHub deployment mappings) from credentials-aware connected account metadata or source control.
2. Confirm read-only API health and representative UI flow with **no changes**. Record ownership: what Grok controls (code, tests, safe research) versus what the existing deployed services own (availability, state, background jobs).
3. Validate build and runtime portability via targeted integration tests; add environment documentation only for real missing pieces.

**Done when:** Grok can change/test app code without needing to keep the Founder's Windows PC on; backend hosting remains stable.

### WP3 — M6.8 NotebookLM adapter: portability and trust acceptance

1. Inspect most recent M6.8 implementation/tests; **do not assume earlier prompt was executed**.
2. Preserve M6.4/M6.5 contracts, M6.7 mock-first boundary, `M6.8-TRUST-BOUNDARY-ACCEPTANCE`, trusted resolver and FD #153 verified finalizer.
3. Validate clean `notebooklm-py 0.8.5` install in Grok cloud using **a read-only/no-auth probe first**. If approved, do one interactive account setup using a dedicated least-privilege account and safe authentication handoff (not copied primary-account cookies).
4. If cloud authentication succeeds, run **one bounded live end-to-end** request (request-scoped notebook; resume polling, selective cited import, grounded Q&A, correct source/run bindings); no repeated research submissions on timeout.
5. If it fails due to Google's web/session/egress constraints, classify `REAUTH_REQUIRED`, `PROVIDER_UNAVAILABLE` or `REGION_EGRESS_BLOCKED`. Keep mock path working, **do not** weaken verification or immediately build a proxy/VPS. Propose a small external worker only after clear evidence.
6. Verify hostile transport cannot choose resolver, forge citation proof, bypass `accept_success_result()`, write SUCCESS directly, leak credentials or contaminate requests. Test valid and failure cases.
7. Avoid asserting closed-corpus for open-web discovery; only mark evidence independently verified under the original IIP contract.

**Done when:** IIP adapter returns an accepted research result + provenance via existing interfaces; or a precisely classified transport blocker is reproduced without damaging existing IIP capabilities.

### WP4 — QAD research team, one real case

1. Configure the 3 roles above, constrained by approved QAD workflows. No 10-Bot fleet initially.
2. Test ONE Founder-approved QAD question on a real public company, with current first-party filings and independent cross-examination. Research Lead and Skeptic disagree substantively where evidence warrants.
3. Capture and re-open sources, derive at least one verifiable numeric assertion from source data, and show the user a readable mobile summary with source links and unresolved alternatives.
4. Persist evidence, claims, challenged assertions, and case/version IDs to IIP's intended structured destination, without overwriting history.
5. Compare time, cost and quality against the old manual/NotebookLM-assisted workflow.

**Done when:** a real Founder-reviewable research case exists, survives independent checking, and can be recovered later without the original Bot's memory.

### WP5 — Selective automation, not blanket 24/7 agent activity

Only after WP1 and WP4 demonstrate value, enable at most ONE low-cost scheduled research/watch task, using actual source freshness, explicit empty result, capped searches and quota budget. **All 5 existing IIP cron jobs remain PAUSED** until individually authorized/revalidated. Monitor usage and failure states for a week. A Cloud Bot routine is a scheduled task, not a guaranteed always-on market-data daemon.

**Done when:** scheduled work produces a legitimate, traceable signal or an honest empty state from the cloud while user's laptop is off.

## H. Test matrix / release limits

| Scenario | Expected |
|---|---|
| Grok iPhone request → cloud code edit → branch + tests + PR | End-to-end works |
| Two Bots share cloud filesystem | No secrets or mistaken trust segregation |
| `git` references differ from previous handoff | Stop destructive operations; reconcile ancestry |
| Missing primary data or stale prices | Report unavailable/stale; no invented values |
| Provider expires Google session | `REAUTH_REQUIRED`; no repeated silent browser loops |
| Network/NotebookLM consumer API unavailable | bounded `PROVIDER_UNAVAILABLE`; fallback via existing mock only |
| Research running when poll times out | resume same run; no duplicate charge/run |
| Malicious provider content directs software change | treated as data; no instruction execution |
| Fake result hash/source citation | rejected; no SUCCESS |
| Competing agents edit same code | feature branches/worktree separation, lead serializes merge |
| Weekly quota exhausted | stop safely, preserve issue/branch/state; never silently auto-pay |
| Power off laptop | Grok cloud tasks can continue; locally hosted Hermes-only dependencies cannot |

Tests are proportional. Keep targeted regression and CI build; do not require an entire historic test suite to be clean if documented inherited failures are irrelevant, but never declare a known material defect PASS. No `main` merge, broad dependency upgrade, production deployment, broker connection, or new cron activation without a separately authorized scoped action.

## I. Practical mobile operating protocol

Use one ongoing conversation with **IIP Lead Bot**. Example requests:

- `IIP: Research whether [company] is experiencing temporary dislocation or structural damage. Cite sources as of today; show the strongest opposing case. Do not execute trades.`
- `IIP: Implement [small feature] on a new branch, run tests, send PR with a Thai summary. No deployment.`
- `IIP: What changed overnight in the current research queue? Only cite newly verified sources; no change => report zero updates.`

Response contract: `Objective → result (working artifact/PR/case) → evidence/tests → limitations → one next action`. Keep mobile output brief, with linked source artifacts, no long governance transcript.

## J. Usage/security pilot acceptance

During the first three representative jobs, record consumed weekly usage percentage before/after, whether any paid on-demand spend occurred, PR/code quality, run duration (actual, not guessed), and whether laptop was off. Then decide whether the current Cursor subscription suffices. Do not assert a published fixed token allowance not shown to the user.

Use limited GitHub access and safe branches; store provider credentials only in an approved secrets mechanism with least privilege. No broker/IBKR sessions, Google master tokens, personal auth cookie exports, or protected research in the public repo. Review Grok Bot's shared-cloud-computer privacy/data settings and per-action approvals.

## K. Current next action (shortest valid path)

**NOW:** Grok starts **WP1 immediately** from the currently verified remote `impl/m6-gemini-notebook` branch (reported head `210610e`), creates an isolated pilot branch, delivers a useful tested code/portability change and opens a PR. Do not wait for Hermes or demand a Windows login. The Grok handoff inspection PR #1 (`grok/handoff-inspection-20261017`) is **docs-only, not the working pilot**; treat it as evidence and keep it separate. **DEFER:** retrieve and reconcile the unpushed `f62ac8f`/M6.8 smoke evidence from the Windows laptop on its next available session, without overwriting cloud work. Do not begin live NotebookLM or production migration merely to bypass missing auth.

**Open uncertainties:** actual current Windows worktree after October 14; current GitHub/Cloud Bot authorization and quota; actual NotebookLM behavior from Grok datacenter; existing deployed service/database state; whether the Founder wants a separate private repo for unpublished investment research. None is silently assumed resolved.

---

### Source references (read selectively, not as alternate plans)

- `00-FOUNDERS-MANIFESTO.md`, `01-PROJECT-DNA.md`, `02-PROJECT-CONSTITUTION.md`, `operational/FOUNDERS-DECISIONS.md`
- `design/qad-pivot/REVISED-QAD-MASTER-PLAN.md` — the existing approved/design lineage for QAD M0–M15, **not** a competing live migration execution checklist
- `design/qad-pivot/LEAN-CANONICAL-SPEC-PLAN.md` — QAD contract taxonomy
- `evidence/m6.7/TRUST-BOUNDARY-AND-M6.8-ACCEPTANCE-REQUIREMENT-2026-10-14.md`
- `PROJECT_STATE.md`, `AGENTS.md`, `operational/ROADMAP.md` — current facts/rules/historical product phase history (not all separate sources of the next task)
- Official Grok Bot documentation: `https://docs.x.ai/grok-bot/overview`, `https://docs.x.ai/grok-bot/mobile`, `https://docs.x.ai/grok-bot/approvals-security-and-privacy`, `https://docs.x.ai/grok-bot/skills-routines-and-automations`, `https://docs.x.ai/grok-bot/faq`.

**Change policy:** after adoption, amend *this file* for changes in execution priority or integration approach and reference the change's specific commit. Do not create `MASTER_PLAN_v2_FINAL_REAL.md` forks. The objective is one navigable plan with verifiable running software, not file-count growth.
