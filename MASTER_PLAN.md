# IIP MASTER PLAN — QAD Research Bot Institution & Grok Cloud Execution

**Version:** 2026-10-18 / Founder Research Bot Institution decision  
**Status:** `FOUNDER-ADOPTED EXECUTION DIRECTION — IMPLEMENTATION IN PROGRESS`. Adoption is by the Founder's explicit 2026-10-18 instruction to make this file the execution source of truth for the separate-Bot Research Institution. This document's adoption **does not** assert that 26 Bots exist, PRs have merged, runtime gates pass, or production is approved.  
**Target repository:** `chamnantantiyavuth-max/investment-intelligence-platform`  
**Migration source:** Hermes on the Founder's Windows laptop  
**Target workflow:** One existing IIP Lead Grok Bot coordinating 25 dedicated durable research/assurance/operations Grok Bots; native Cursor Subagents remain optional execution helpers, **not substitutes** for these Bots; researcher roles and scope constrained by QAD contracts  
**Priority:** working software and verifiable research results > perfect process.  
**Scope:** execution/ownership migration; **NOT** a change to the IIP product constitution or permission for live brokerage/trading.

 > **Single operational source of execution truth:** This file is the current *execution roadmap, Bot roster and rollout entrypoint*. It links to binding contracts rather than duplicating them. Older files containing `PLAN`, `ROADMAP`, or `v0.x` become historical/domain references for execution sequencing, not competing instructions. This file **cannot override** the Constitution, approved Founder Decisions, approved QAD contracts, or real implementation/test evidence.
>
> **Updated authority and sequencing (Founder direction, 2026-10-18):** Founder explicitly chooses **separate persistent Grok Bots per Research Dimension**, authorizes phased Bot-team setup, and directs that this Master Plan become the execution source of truth. Earlier 3-Bot and Subagent-first staffing proposals in this plan are superseded. Prior WP0–WP1 pilots have produced GitHub PRs; local-only Hermes M6.8 evidence remains `DEFERRED_SYNC`. These instructions remain subordinate to the approved Constitution, Founder Decisions and QAD contracts.

### Founder decisions — 2026-10-17 cloud pilot; 2026-10-18 separate Research Bots

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

| Purpose | Canonical place as adopted |
|---|---|
| Current objectives, execution phases, next tasks, integration decisions | **`MASTER_PLAN.md`** (this file, as adopted) |
| Verified current build state, commit/test evidence, blockers | `PROJECT_STATE.md`, concise factual state **not an alternative roadmap** |
| Highest-order investment/product constraints | `02-PROJECT-CONSTITUTION.md` + approved amendments |
| Explicit approved decisions | `operational/FOUNDERS-DECISIONS.md` |
| Investment domain and accepted QAD behavior | `01-PROJECT-DNA.md`, approved `project-definition/`, `design/qad-pivot/` canonical specs/contracts where ratified |
| Agent loading/rules/commands | `AGENTS.md` (make platform-neutral in a separate scoped commit) |
| Application source/tests | `qad/`, `backend/`, `frontend/`, `tests/` |
| Exact research inputs, sources, result provenance | structured IIP evidence/ledger and bounded `research/`, `reports/`, `evidence/` artifacts |
| Prior plans/design decisions | historical references only; never silently rewrite approval records |

### Agent bootstrap for every Bot and Cloud Agent

1. Read `MASTER_PLAN.md` (Sections F and L are decisive for Bot ownership) and latest concise `PROJECT_STATE.md`.
2. Read `AGENTS.md` and only **relevant** approved contract/source files for the current task.
3. Check Git branch SHA, `git status`, and latest tests; reconcile factual conflicts using code and evidence.
4. Choose **one narrow deliverable**, make it work, run targeted tests, record output/commit, report next action.
5. Do not auto-load every previous `PLAN` or `SESSION_CLOSEOUT` into context; search them only for a named unresolved question.
6. No review→correction→review loop unless a material defect affects functionality, integrity, security, or a binding contract.

**If another plan appears to disagree:** interpret it in its original historical scope; do not let an unratified old planning draft supersede a verified current commit or binding contract. Escalate only a material authority conflict, naming both exact sources.

## D. Target architecture — genuine collaborating Grok Bots (Founder-adopted)

```text
FOUNDER (mobile / iPhone; investment and approval authority)
       │
       ▼
IIP Lead Bot — executive/program owner, engineering/PR coordination
       │
       ├── Discovery Scout Bot → signals / public intelligence
       │         └─ deterministic S1 Selection Engine (policy service, NOT a Bot)
       │
       └── Research Director Bot — one case owner, H1–H5 + Evidence Gap Map
                 │
                 ├── Core Bots (6 separate durable Bots)
                 │     Business | Industry | Financial | Management | Impairment | Valuation
                 ├── Elastic Investigator Bots (11 separate durable Bots, invoked on demand)
                 │     Customer | Competitor | Supplier | Channel | Employee |
                 │     Digital | Regulatory | Technology/IP | Clinical | Geographic | Industry Specialist
                 └── Evidence Intelligence Lead Bot — original-source verification / admission
                              │
                              ▼
                   Structural Red Team Bot [independent]
                              │
                              ▼
                   Independent Auditor Bot [independent]
                              │
                              ▼
                   Chief Underwriter Bot [independent from analysts and selection]
                              │
                              ▼
                   Thai Editor Bot → Founder research review → Thesis Steward Bot
```

**The number refers to distinct, durable Grok Bot identities with separate conversations and role memory**, not Cursor project subagent definitions, `actor_id` strings, Cloud Agent processes or Markdown config files. One Bot may use temporary Cursor/Cloud subagents to perform its own scoped work; the accountable owner remains the durable Bot. The Founder may contact any Bot directly; IIP Lead is the default entrypoint.

**Actual coordination:** Bots can message other Bots asynchronously and reply; 2–6 Bots can share a task-focused group conversation. Handoffs must name `case_id`, `case_version`, `gap_id`, request owner, falsifiable question, PIT/as-of, source access, requested output, deadline/budget, next owner, and stop rules. Bot messages are coordination *events*, not authoritative financial evidence. Canonical IIP records / immutable source snapshots in approved storage are the handoff truth. Do not transfer long reports as mutable conversation-only text.

**Platform caveats:** Bots in one account share the cloud computer, browser sessions, files, app plugins and sign-ins. Distinct Bot identity/role memory is NOT a credential or security boundary; a separate chat alone does NOT prove independent research judgment. Independent Assurance starts a clean case-specific analysis using the underlying original sources, separate assignment and an auditable challenge record. No brokerage, primary Google cookies/master token, private holdings or confidential thesis on this public repo/shared Bot computer.

## E. Grok Bot capabilities, known constraints and pilot questions

Official Grok Bot documentation reviewed 2026-10-17/18: paid Cursor individual plans are eligible, mobile can interact with the same cloud Bots, Bots can delegate to Cloud Agents, and Bots/Routines can work while the laptop is closed. Actual account entitlement remains unverified until login.

**Usage:** Weekly included allowance, with on-demand/overage possibilities depending on account. A large multi-agent coding + research workload will consume more usage than chat. The exact **account-specific quota, remaining allowance, and price** are NOT known from this repository or public documentation. Inspect `Usage & Billing` / Cursor account, select a monthly on-demand spend cap if available, and measure first three representative tasks (small code change, test run, one research case) before adding more agents or recurring jobs. Avoid auto top-up/unlimited spend until budget is known.

**Cloud limitations to check by hands-on test:**
- GitHub OAuth permission, branch/PR push, CI/status visibility, bot notifications on mobile;
- computer runtime (Python/node, disk/CPU/memory, network, execution timeouts) and durable files across app restart;
- Google NotebookLM login and consumer CLI `0.8.5` functionality from cloud egress;
- GitHub actions or existing external CI for heavy builds;
- latency and quota with 1 coordinator and 1-2 task agents;
- approval prompts: unattended approval may expire; design work to stop safely and resume.

**Security:** This repository is public. Research drafts about holdings and private ideas go into an approved private storage/repo, not public `reports/`. No shared browser session should be treated as restricted to a single Bot.

## F. Founder-approved Research Bot Organization — 26 durable Bots, phased activation

**Roster target: 26 durable Grok Bots total = 17 dimension-specialist Bots + 9 coordination/assurance/publication Bots, counting the existing IIP Lead Bot.** Register a real `Bot link/ID` and owning role for each created Bot in the roster below or a linked roster record controlled by this Master Plan. This is a **target structure, not a claim of existing Bots or permission for 26 simultaneous runs**. Set up distinct Bots progressively; dormant Bots have no scheduled routine and do no research until assigned. Confirm actual tool/plan entitlements before making assumptions.

### F1. Durable Bot roster — control, independence and publication (9)

| Bot name (create/retain) | Canonical QAD responsibility | Independent boundary / concrete deliverable |
|---|---|---|
| **IIP-Lead** (retain existing Grok Bot) | Program management / engineering integration; not the Selection Engine | Single accountable delivery coordinator, GitHub work queue, PR and mobile handoff; cannot declare research audit/underwriting on others' behalf |
| **IIP-Discovery-Scout** | Role 13 Discovery & Dislocation Scout; Lane C, plus monitor A/B signals as input | Public signals with source/as-of; **must not assign S1 selection states** |
| **IIP-Research-Director** | Role 1 Research Director / Case Orchestrator | Case opening after approved selection or tagged FOUNDER_DIRECTED; H1–H5 charter, Evidence Gap Map, EIV-based staffing and evidence requests; no underwriting/auditing own case |
| **IIP-Evidence-Lead** | Role 2 Evidence Intelligence Lead | Original source index, evidence admission verification, source/PIT/provenance; **cannot audit own admission** |
| **IIP-Structural-Red-Team** | Role 9 independent adversarial research | Fresh source-level value-trap/false-quality/structural hypothesis; never self-selects or writes the producer conclusion; dissent preserved |
| **IIP-Independent-Auditor** | Role 10 independent source/calc/PIT integrity | Verification and material findings; cannot author or certify own research or canonical admission |
| **IIP-Chief-Underwriter** | Role 8 separate final investment research judgment | Independent synthesis, adjudicates Red Team evidence and verdict; cannot act as selecting agent, portfolio allocator or upstream producer |
| **IIP-Thai-Editor** | Role 11 Thai Long-Form Research Editor | Faithful Thai report and companion challenge article; no promotion to publication without applicable audit/underwriting/Founder states |
| **IIP-Thesis-Steward** | Role 12 Thesis / Knowledge Steward | Monitor material thesis evidence changes and validation, track lessons; only approved lessons may become knowledge |

**Research Budget Controller (S2), Autonomous Selection Engine (S1), identity resolution (S3), Evidence Registry/Archive (S4/S5), PIT locking (S7), Run Manifest (S6), execution/retry (S8), idempotency (S9), NotebookLM interface (S10), renderer (S11) and evaluation (S12) are policy, deterministic, or infrastructure services: NOT additional discretionary Bots.** Do not invent a Budget Approval Bot that can waive binding limits. Founder's approval remains human.

### F2. Durable Core Research Bots — 6

| Bot name | Canonical analytical role | Research output |
|---|---|---|
| **IIP-Business-Moat** | Role 4 Business & Industry Analyst | Business model, customer economics, six canonical moats, durability, false-quality hypothesis |
| **IIP-Industry-Economics** | Role 4 Business & Industry Analyst | Industry demand→supply→capacity→utilization→pricing→margins→ROIC→capital entry/exit, competitive structure |
| **IIP-Financial-Accounting** | Role 5 Financial & Management Analyst | 7–10+ years of financial reconstruction, cash conversion, normalized accounting, working capital, dilution, per-share |
| **IIP-Management-Allocation** | Role 5 Financial & Management Analyst | Management claim-vs-outcome and capital-allocation ledgers, incentives, M&A/buybacks, governance |
| **IIP-Impairment-Recovery** | Role 6 Impairment Diagnosis Specialist | H1/H2/H3/H4 alternative causal models, impairment and recovery mechanism, falsification |
| **IIP-Valuation-Expectations** | Role 7 Valuation & Expectations Specialist | Normalized economics, reverse DCF, market-implied assumptions, asymmetric downside/permanent loss, H5 |

### F3. Durable Elastic Investigator Bots — 11

Each is a real durable Bot identity, **not a standing investigator run**. Activation requires a scoped Evidence Gap, falsifiable question, authorized source classes, charter, EIV, budget/stop condition and accountable Research Director. Unless actual lawful fieldwork is arranged, these Bots do **public-document desk research**, not interviews/surveys/site visits. Store honest sampling limits.

| Bot name | Scuttlebutt specialization |
|---|---|
| **IIP-Customer-Product** | Customer needs, product experience, retention, switching costs, public customer/provider voices |
| **IIP-Competitor** | Peer competitive responses, share shift, alternative substitutes, evidence of moat erosion |
| **IIP-Supplier** | Supplier economics, bargaining power, input availability, supply constraints |
| **IIP-Channel-Distribution** | Distributors, inventory, route to market, channel health |
| **IIP-Employee-Organization** | Organization, talent, execution and culture using lawful published signals |
| **IIP-Digital-Social** | Public web/app metrics, digital ecosystem, social signals with sampling bias |
| **IIP-Regulatory** | Regulation, rate changes, legal exposure, agency action; date-specific rules |
| **IIP-Technology-IP** | Technology displacement, patents, R&D and technical moat |
| **IIP-Scientific-Clinical** | Scientific evidence, clinical trial publications, methodological critique |
| **IIP-Geographic** | Regional dynamics, market differences, local competition |
| **IIP-Industry-Specialist** | Sector-specific domain expertise and cross-company patterns beyond the general industry Bot |

The 17 specialists reuse `qad/specialists/configs/dimensions.json` from **PR #6 only after review/correction and integration**. Bot profile = durable owner; config = task skill/contract reference; Cloud subagent = optional disposable helper. Do not mistake one for another.

### F4. Work distribution and real team collaboration

**Case flow must preserve the approved M3 sequence:**

1. **Discovery lanes A/B/C** feed identity, Signal, Quality Universe and Candidate Registry. The deterministic **S1 policy** alone sets `AUTO_RESEARCH_NOW`, watch or reject states; Founder-directed manual cases explicitly marked `FOUNDER_DIRECTED`, never counted as autonomous selection.
2. **Research Director** opens case under actual authority, writes Research Charter with **H1–H5**, source scope, budget, evidence gap map and case owner. Evidence Lead checks evidence/protocol completeness; S2 authorizes budget under existing policy. Draft remains draft until required validation. Underwriter has no Charter approval or selection role.
3. **Primary-source foundation + initial analysis:** Evidence Lead and Core Desk obtain source snapshots with source date, retrieval date, issuer/CIK, PIT, section/page, hash and contradictions; no AI synthesis promoted to facts.
4. **Core analysis:** six Core Bots can exchange observations across dimensions via compact scoped handoffs. Each has independent producer ownership and tracks `SUPPORTED / INFERRED / UNRESOLVED` as report descriptions, without inventing canonical status enums.
5. **Elastic field/ecosystem investigation:** Research Director selectively calls **only relevant** Investigator Bots on an Evidence Gap + falsifiable claim; default active investigators <=3 per the accepted scuttlebutt constraints. Each report records actual method, public sources, population, bias, counterevidence, stop rule and remaining gap.
6. **Evidence admission:** Evidence Lead checks that cited passages **actually exist** in independently obtained original source bytes or verified immutable snapshot, then applies the existing canonical admission boundary. Provenance-looking fields and self-supplied quotations alone DO NOT make `FACT-01=VERIFIED`. Failed claims stay unverified/quarantined with reason.
7. **Dislocation/impairment and valuation:** dedicated Core Bots compare peer and sector damage against company-specific damage, normalize earnings, build recovery vs permanent-loss scenarios, and test H5 valuation relevance. No invented precise fair value.
8. **Independent challenge:** Structural Red Team independently reads original source corpus, generates strong structural/value-trap/false-quality alternative and challenges claims. Analyst replies with evidence, not opinion. Preserve unresolved challenges.
9. **Independent assurance and adjudication:** Independent Auditor tests original sources/PIT/calc integrity per M3 stage ordering; Chief Underwriter independently adjudicates Red Team and synthesizes permitted underwriting verdict, relying on actual completed outputs. No role can write its own approval or fabricate stage PASS. If audit/underwriting ordering differs within approved contracts, follow the binding M3 workflow, not this shorthand.
10. **Thai publication + Founder + monitoring:** Thai Editor creates accurate readable draft with separate counter-thesis. Founder alone makes the actual investment decision; approved publication/monitoring starts only under existing gates, and Thesis Steward tracks falsifiers over time.

**Handoff contract for every Bot→Bot task:** `case_id`, `case_version`, `as_of/pit_mode`, `evidence_gap_id`, `assigner_bot`, `assignee_bot`, `canonical_role`, `charter_ref`, `hypothesis_test`, `source_snapshot_refs`, `scope`, `EIV`, `authorized_budget`, `stop_rule`, `deliverable_ref`, `execution_id (if exposed)`, `acknowledged_at`, `disposition`, `next_owner`. Use existing canonical models/ledger where applicable; this is a **handoff envelope/guide, not a new 69th canonical schema**. A bot-to-bot message is the notification; persistent IIP case records and source archive own durable truth. Version new results; never silently overwrite adverse evidence.

**Coordination surfaces:** 
- Founder ↔ IIP-Lead main DM on iPhone.
- Task-focused Grok group chats of **2–6 Bots max**, e.g. `QAD/UNH–Research` = Director + Evidence + Industry + Customer + Management (5); `QAD/UNH–Challenge` = Red Team + Evidence Lead + Auditor, with Underwriter receiving immutable full packet separately to preserve analytical independence.
- Asynchronous `@Bot` handoff for direct questions. Every stage has one owner; do not ask `@everyone` to duplicate work.
- Code/PR state and public-safe artifacts in GitHub; confidential research only in approved private IIP storage. Internal Bot chat transcript/memory is **not** publication, evidence verification or approval.

### F5. Activation vs existence — truthful roster states

For every target Bot, record **`NOT_CREATED` → `CREATED` → `PROFILE_CONFIGURED` → `HANDOFF_TESTED` → `ACTIVE_ON_DEMAND`** in a human-readable deployment checklist linked from this plan (not new canonical runtime enums). No Bot is declared `ACTIVE_ON_DEMAND` without a real direct or group Bot-to-Bot task with acknowledged handoff, original-source output and useful result. If creation requires Founder interaction or plan entitlement, return the exact iPhone UI step/blocker; **do not substitute subagent files, actor_id strings or Cloud Agents as proof of durable Bot creation.**

Separate genuine Bot collaboration from audit independence: each assurance role must use separate assignment/execution, independently reopen primary sources and document challenge/adjudication trace; shared account credentials are still shared. Human approval boundaries apply regardless of Bot count.

## G. Migration execution — dependency-ordered work packages

### WP0 — Remote-first handoff with deferred local reconciliation (Cloud development NOT blocked)

**Owner:** Grok validates remote facts now; Founder/Hermes reconciles missing local-only work when the laptop becomes available.

1. **NOW — remote/cloud path:** Validate `origin/impl/m6-gemini-notebook` @ `210610e` (or its actual verified descendant), and use that remote commit as the cloud WP1 baseline. Record absent local evidence honestly. Do not infer that local M6.8 success was pushed, and do not recreate its proof.
2. Start WP1 on a **new isolated cloud feature branch** immediately, preserving source-control ancestry and existing QAD contracts. Running cloud tests and making a scoped code improvement does not depend on a Windows notebook session.
3. Adapt the Grok cloud bootstrap in `AGENTS.md` to remove blocking assumptions that Hermes-local profile paths exist, without deleting historical rules or treating a synthetic substitute as equivalent to a missing approved local source. Link this Master Plan as the proposed execution roadmap.
4. **LATER — local reconciliation:** When the Windows machine becomes available, inspect local status, HEAD, untracked files and unpublished commits; check for secrets; verify `f62ac8f` ancestry and subsequent work; cherry-pick or merge safely onto a dedicated integration branch using normal Git ancestry. No hard reset, force push, overwrite of Grok's new work, or automatic trust promotion of local-only evidence.
5. Founder has now given explicit adoption authority on 2026-10-18 for the **execution plan**, subject to integration into the development branch. Do not confuse plan adoption with local Hermes evidence authentication, implementation acceptance or release approval.

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

1. Use the **26-role durable Bot target in Section F**, create real separate Bots in phases rather than activating an expensive permanent 26-way swarm. Start with the existing Lead and a small Director/Evidence/Industry/Customer/Management pilot cohort; prove real inter-Bot handoff first.
2. Reuse the existing UNH R&D case from PRs #3–#6. Demonstrate an actually coordinated Bot handoff on a NEW material Evidence Gap, with original-source validation and independent challenge. Do not repeat already completed UNH specialist work merely to populate Bot histories.
3. Capture and re-open sources, derive at least one verifiable numeric assertion from source data, and show the user a readable mobile summary with source links and unresolved alternatives.
4. Persist evidence, claims, challenged assertions, and case/version IDs to IIP's intended structured destination, without overwriting history.
5. Compare time, cost and quality against the old manual/NotebookLM-assisted workflow.

**Done when:** a real **Bot→Bot** task handoff yields source-checked case evidence and independently challenged findings, and its durable case record can be recovered after a process restart and read through the authenticated IIP path, without any Bot memory.

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

## K. Current next action — Founder-approved separate-Bot Research Institution

**Decision already made:** Founder wants distinct durable Grok Bots per Research Dimension and a coordinated IIP Research Institution. **Do not ask again whether Subagents would be cheaper** and do not relabel Cursor Subagents as actual Bots. This directs safe Bot creation, configuration and manual tests. It does NOT authorize new paid overages, automated job schedules, changed canonical policies, migration of Google/broker credentials or publication/trading.

**Observed GitHub checkpoint (2026-10-17):** `impl/m6-gemini-notebook@210610e`; unmerged PR #2 WP1 fixture, #3 UNH draft, **#4 integrated branch@32dd21e**, **#5 UNH canonical slice@343d582**, **#6 specialist catalog/router + three UNH result artifacts@08daab0**. These form an ancestry chain of feature PRs, **not merged into development/main**. No separately created 17 Bots are proven by these files. Earlier tests are **Grok-reported**, not independently reproduced CI; PR #6 still carries **two material blockers**: (a) externally supplied quotation metadata incorrectly promoted to VERIFIED fact without independently inspecting original source; (b) in-memory specialist ingests do not survive a fresh canonical Case API read. These are repair tasks, not reasons to stop creating Bot identities.

**Shortest sequence:** (1) adopt this plan in `impl/m6-gemini-notebook` (not `main`), (2) ask **IIP-Lead** to create/configure the first distinct Bots and show their actual Bot names/links/DM handoff; retain completed Grok research outputs, (3) on a bounded engineering branch fix both critical PR #6 integrity defects with tests/read-back, (4) run one fresh Evidence Gap with two distinct Bots plus Evidence Lead and Independent challenge, (5) expand durable roster to 17+9 as proof and usage justify, but only on-demand execution. Do not start 26 agents concurrently. Existing local Hermes work stays `DEFERRED_SYNC`.

**Immediate work package:** Section L phase B0→B2. Deliver one real Bot-to-Bot handoff and safe evidence recovery rather than another planning report.

**Explicit no-go:** don't claim Group Chat transcripts, Bot IDs, bot-to-bot messages, a Vercel preview, or an agent-generated citation establishes a verified canonical fact; don't turn 5 paused cron jobs on; don't merge into `main` or deploy production; don't create a false independent assurance role in the same execution.

## L. Separate Research Bot deployment plan — implementation in measurable increments

| Phase | Real capability (not paper) | Acceptance check | Bot population |
|---|---|---|---|
| **B0 — Roster registration (immediate)** | Founder-used IIP Lead checks actual Grok Bot create/message/group features, creates or requests creation of **Research Director + Evidence Lead + 3 pilot Specialist Bots**. Each has a distinctive real Bot profile, conversation, IIP contract link and no routine. | Real Bot profile/link for each; read current repo Master Plan; none mistakenly represented by .cursor/agents files. Do not migrate credentials. | **6 including Lead** |
| **B1 — Bot collaboration smoke (immediate)** | In a group/async handoff Director sends scoped `CASE-2026-001` question to e.g. Customer Bot and Industry Bot, Evidence Lead independently checks source. | Actual delivered + acknowledged Bot messages and returned linked output, one owner per task, no duplicated research or fake source; show links/IDs if platform exposes them. | **same 6** |
| **B2 — Evidence/recovery fix (parallel engineering)** | Scoped correction of PR #6 unverified-fact promotion and in-memory post-ingest loss; use original source or verified source snapshot + canonical persistence/replay. | Attack test: fake quotation at real URL never yields VERIFIED; process-restart + fresh authenticated Case API returns accepted evidence, IR/stage state; old real data preserved, no new canonical schema. | **same 6** |
| **B3 — Independent decision chain** | Instantiate Structural Red Team, Auditor, Chief Underwriter as separate durable Bots. Run a real sample challenge on the new research with fresh source reads, independent audit and evidence-grounded adjudication; leave unavailable QAD stages incomplete. | Separate Bot links and actual independent source-level challenge/audit; conflicting finding visible; no unfounded `FOUNDER_READY`. | **9 total** |
| **B4 — Complete dimension roster** | Create/configure all remaining 6 Core +11 Investigator durable Bots; add Discovery Scout, Thai Editor and Thesis Steward at the relevant stage. Distinct Bot links, role definitions, handoff paths. **No permanent 26-way background work.** | **26 distinct Bots**, handoff smoke for each role only when triggered by a real material Evidence Gap; standby profiles not counted as a completed research run. | **26 target** |
| **B5 — Full QAD vertical slice** | One full research case end-to-end per existing M3 contracts: Discovery→Selection→Charter H1–H5→Evidence→Core analysis→material Scuttlebutt→Impairment→Valuation→Red Team→Audit→Underwriter→Thai Editor→Founder Review→Monitoring. Reuse stage states; don't auto-complete gaps. | Genuine evidence-gated Case record and mobile reading path with source trail, independent challenge, explicit missing work and correct Founder decision requirement. | Selective on-demand Bots |
| **B6 — Optional routines** | After B5 and quota/usage checks, propose a single low-cost signal/report routine; each existing cron separately reauthorized if ever needed. | Real measured utility, no hidden overages, 5/5 existing cron PAUSED until authorized. | As needed |

**Execution budget:** Research Director selects bots by Evidence Gap and EIV; at most 3 parallel active investigators unless existing policy explicitly permits more. The 17+9 Bots are durable role owners, not a quota of simultaneous LLM contexts. Capture observed per-task time/cost when the platform exposes it; record `NOT_EXPOSED` rather than fake 0. Avoid approving paid overages. Bot names must remain stable; duplicate work prevented by case/gap/version owner and idempotent storage.

**One-case working proof:** IIP Lead (existing) → real Director Bot hands a specific *unresolved* UNH gap to a real specialist Bot → specialist reopens public source and returns falsifiable analysis with original-document anchors → Evidence Lead checks source content and provenance → separate Red Team challenges → proof stored/recovered in IIP Case → Founder reads the report on iPhone. If a step is technically missing, deliver the last verified working step and name the missing component without marking it complete.

**Workflow rules:** No separate persistence or source-of-truth in Bot chat or an old `grok-research-team` repo; no 17 permanent worker polling loops; no confidential thesis in public IIP repository. Treat Bot creation as authorized by this Founder decision but any external service account login, quota overage, secret grant, production release or mandatory policy override still follows its actual applicable approval.

---

### Source references (read selectively, not as alternate plans)

- `00-FOUNDERS-MANIFESTO.md`, `01-PROJECT-DNA.md`, `02-PROJECT-CONSTITUTION.md`, `operational/FOUNDERS-DECISIONS.md`
- `design/qad-pivot/REVISED-QAD-MASTER-PLAN.md` — the existing approved/design lineage for QAD M0–M15, **not** a competing live migration execution checklist
- `design/qad-pivot/LEAN-CANONICAL-SPEC-PLAN.md` — QAD contract taxonomy
- `evidence/m6.7/TRUST-BOUNDARY-AND-M6.8-ACCEPTANCE-REQUIREMENT-2026-10-14.md`
- `PROJECT_STATE.md`, `AGENTS.md`, `operational/ROADMAP.md` — current facts/rules/historical product phase history (not all separate sources of the next task)
- Official Grok Bot documentation: `https://cursor.com/docs/grok-bot/work` (durable Bots, creation, direct Bot-to-Bot handoffs, 2–6 Bot groups, shared cloud computer), `https://prod.cursor.com/docs/agent/projects` (Cursor Project coordinators, distinct from durable Bots), `https://cursor.com/docs/subagents` (task-scoped subagents, distinct from durable Bots), `https://prod.cursor.com/docs/cloud-agent`.

**Change policy:** amend *this file* for changes in execution priority or integration approach and reference the change's specific commit. Do not create `MASTER_PLAN_v2_FINAL_REAL.md` forks. The objective is one navigable plan with verifiable running software, not file-count growth.
