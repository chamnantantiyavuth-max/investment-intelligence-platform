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

### Founder output correction — 2026-10-18: FREE-FORM GOOGLE DOCS, NOT THE LEGACY REPORT PLATFORM

**EFFECTIVE IMMEDIATELY FOR ALL NEW QAD RESEARCH.** The Founder retired the fixed-pattern IIP website/blog/Research Library as the QAD report product because prescribed categories, article structure and layout constrained analyst freedom. The Founder reaffirmed on 2026-10-18: **the primary human-readable research report is a free-form Google Doc stored in a stable PRIVATE Google Drive case folder**. This supersedes only historical **delivery-channel, template, mandatory PDF and `/library`/blog** directions in Hermes M11 and earlier QAD M3 Publication/Thai Editor contracts. Research hypothesis discipline, source/PIT verification, case records, Red Team/Audit/Underwriter independence, actual stage transitions, and Founder authority stay binding. Do **not** interpret old FD #62/#72/#94/#96 blog implementation approvals as authority to revive a later-cancelled report platform.

**Output and authority split:**
1. **Canonical research (unchanged):** Structured IIP QAD `CASE-01`, `SRC-01`, `EV-01`, `FACT-01`, claim/audit/underwriting records, states and immutable source provenance remain authoritative. **Google Docs are reading/presentation deliverables, not canonical evidence or verified facts.**
2. **Main Founder deliverable (NEW M11 interpretation):** `IIP-Thai-Editor` and underwriting team produce a **cohesive, independently synthesized Thai Google Doc**, with free choice of narrative, headings, depth, prose, ordering, causal framing and emphasis. Do not require fixed report categories, article frontmatter, the 42-item *suggested* historical outline, forced checklists, one-section-per-Bot, generic canned language, or an agent-output collage. Depth follows material evidence gaps. Present the core economic argument, credible contradictions, source links, assumptions and uncertainties, plus the strongest opposing thesis within the Doc or linked alongside it. Preserve truthful `DRAFT / NOT FOUNDER_READY` while stages are incomplete; no Founder endorsement without an actual Founder decision. **PDF is OPTIONAL export only upon Founder request or genuine external need.**
3. **Stable private Drive storage:** Create/reuse the dedicated root **`IIP — QAD Research`** in My Drive (separate from `Fundamental Inflection Research`/FIRF). Keep minimal folders: `00_ACTIVE_CASES/<TICKER>__<CASE_ID>/` for the current free-form main Doc and optional supporting/updates, `01_SHARED_SOURCES/` for reusable source archives, and `99_ARCHIVED_CASES/` when cases conclude. Only create case folders as needed. Associate each existing IIP case ID with a private Google Doc URL and Drive folder pointer (minimal index), without creating a second evidence registry. Private IDs/links, non-public analysis and rights-restricted source documents must **not** go into the PUBLIC GitHub repo. **Do not mass-move or delete any scattered existing Docs** until provenance, ownership and permissions are known.
4. **No abandoned frontend as report product:** `/library`, `reports/*.md` blog render, `ReportArticlePage.tsx`, Vercel Preview authentication/mobile web article and custom PDF renderer are **not QAD research-output dependencies**. Keep legacy app files for other functions/history without reviving them. iPhone delivery means opening the actual Google Doc from its Drive link, **not** a successful website preview.

**One bounded immediate correction:** Stop dev effort on old IIP report/preview/UI as a QAD deliverable. Retain PR #6 real verification/ingest/recovery code. Create/use `CASE-2026-001` (UNH) private Drive folder and transform the existing B1 18-source draft into **one free-form, carefully sourced Thai Google Doc** labeled DRAFT; preserve the single genuinely verified SEC sentence and label all other still-unverified findings honestly. Give Founder a working private Google Doc link and demonstrate that it opens on mobile; do not pretend the case has cleared Red Team/Audit/Underwriting or is FOUNDER_READY. Then proceed with useful substantive research rather than new documentation or repeat reviews. No cron/routine activation, trading action, schema change, paid overage or production merge.

**Root-cause reconciliation:** Hermes `REVISED-QAD-MASTER-PLAN.md` M11 required PDF; the older QAD M3 Thai Editor + Publication contracts still said `/library`; current Grok `MASTER_PLAN.md` omitted a clear post-cancellation Google Docs delivery direction. Prior ChatGPT review also incorrectly pushed the team to integrate B1 into the old website to make it 'iPhone readable'. This Founder correction is the current authoritative execution instruction for *delivery format/channel only*, without weakening the QAD analytical/evidence rules.

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
| Exact research inputs, sources, result provenance | structured IIP evidence/ledger and bounded private sources; public GitHub only for public-safe material |
| Primary Founder-facing QAD research output | **Free-form Thai Google Doc in PRIVATE Google Drive case folder; NOT `/library` or mandatory PDF** |
| Legacy IIP research blog and `reports/` | Historical files, not QAD publication destination |
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

## F. Founder-approved Research Bot Organization — provision all 26 now; activate on demand

**Founder directive (2026-10-18): PROVISION ALL 26 durable Grok Bot identities NOW in the first Bot-provisioning work package**, not in later research milestones. Total = 17 dimension-specialist Bots + 9 coordination/assurance/publication Bots, **including the existing IIP Lead Bot**, so provision **25 new Bots plus retain/confirm Lead**. The creation backlog must not disappear after pilot work begins. Register the actual Bot links/IDs and owner/role in the **26-row Bot Provisioning Tracker in Section L**; until proved, state remains `UNVERIFIED`, not `CREATED`. Completion target: **within 48 hours of delivery of the first provisioning prompt**, subject to platform limits and mandatory user interaction; if blocked, return the exact blocked Bot(s), mechanism and next UI action immediately. This is a scheduling target, not a claim of unattended guaranteed completion or approval of paid usage. **Create/configure the roster in one bounded campaign, but activate each Bot only when a task exists**: no 26-way simultaneous runs, idle schedules, speculative research, or standing group-chat messages. Confirm actual entitlement and use existing subscription; never enable paid overages without approval.

### F0. Seven Departments — permanent homes, case-based matrix execution

**Founder clarification (2026-10-18):** organize all **26 already-authorized durable Bots** into seven departments. A department is an organizational home/sidebar Section, **not** a new canonical role, independent security tenant, ongoing agent run or new paid Bot. Research cases form **temporary cross-department Case Teams**, directed by the Research Director under the existing M3 contracts.

| Department / suggested Sidebar Section | Bots | Members |
|---|---:|---|
| **01 · Executive & Research Management** | 2 | `IIP-Lead`, `IIP-Research-Director` |
| **02 · Data & Discovery** | 2 | `IIP-Discovery-Scout`, `IIP-Evidence-Lead` |
| **03 · Equity & Valuation Research** | 5 | `IIP-Business-Moat`, `IIP-Financial-Accounting`, `IIP-Management-Allocation`, `IIP-Impairment-Recovery`, `IIP-Valuation-Expectations` |
| **04 · Industry & Competitive Intelligence** | 6 | `IIP-Industry-Economics`, `IIP-Competitor`, `IIP-Supplier`, `IIP-Channel-Distribution`, `IIP-Geographic`, `IIP-Industry-Specialist` |
| **05 · Customer & Specialized Intelligence** | 6 | `IIP-Customer-Product`, `IIP-Employee-Organization`, `IIP-Digital-Social`, `IIP-Regulatory`, `IIP-Technology-IP`, `IIP-Scientific-Clinical` |
| **06 · Independent Assurance & Underwriting** | 3 | `IIP-Structural-Red-Team`, `IIP-Independent-Auditor`, `IIP-Chief-Underwriter` |
| **07 · Editorial & Knowledge** | 2 | `IIP-Thai-Editor`, `IIP-Thesis-Steward` |
| **Total** | **26** | The original 26 roles, with no additions or omissions |

**Authority, not just chart layout:** Founder makes final decisions. `IIP-Lead` manages engineering/work queues and Bot coordination, while `IIP-Research-Director` owns Case Charters, assignments and evidence gaps. Research teams do not control deterministic S1 candidate selection or S2 budget authorization. The Evidence Lead is in Data & Discovery for source ownership but cannot audit its own admission; Discovery Scout cannot assign selection states. Red Team, Independent Auditor and Chief Underwriter are structurally separate from upstream producers and from each other; Research Director/Lead cannot silence dissent or declare their PASS. Editorial does not approve investments.

**No artificial Data Bot proliferation:** SEC ingestion, source archiving, entity normalization, PIT locks, numeric extraction, selection rules and budget controllers are already-approved software/services; they are **not additional Bots**. Assign software coding to bounded Cloud Agents under IIP-Lead as needed without changing the standing 26-Bot roster.

**Actual UI arrangement:** Grok Bot supports Sidebar **Sections** on iOS/desktop. Create the seven named sections and place the actual persistent Bots in them (iOS: hold a Bot → New Section / Move to). Departmental Sections do not set credentials or access controls. Use temporary 2–6-Bot group chats for a single case and async direct handoffs, never one 26-Bot room.

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
| **IIP-Thai-Editor** | Role 11 Thai Long-Form Research Editor | Coherent free-form Thai Google Doc in private Drive case folder with opposing thesis retained; applicable audit/underwriting/Founder states remain binding |
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
10. **Free-form Google Doc + Founder + monitoring:** Thai Editor writes an original narrative Thai Google Doc in the private QAD case folder, with coherent counter-thesis and source refs. Founder alone decides; stage gates and honest DRAFT status remain binding, and Thesis Steward tracks falsifiers.

**Handoff contract for every Bot→Bot task:** `case_id`, `case_version`, `as_of/pit_mode`, `evidence_gap_id`, `assigner_bot`, `assignee_bot`, `canonical_role`, `charter_ref`, `hypothesis_test`, `source_snapshot_refs`, `scope`, `EIV`, `authorized_budget`, `stop_rule`, `deliverable_ref`, `execution_id (if exposed)`, `acknowledged_at`, `disposition`, `next_owner`. Use existing canonical models/ledger where applicable; this is a **handoff envelope/guide, not a new 69th canonical schema**. A bot-to-bot message is the notification; persistent IIP case records and source archive own durable truth. Version new results; never silently overwrite adverse evidence.

**Coordination surfaces:** 
- Founder ↔ IIP-Lead main DM on iPhone.
- Task-focused Grok group chats of **2–6 Bots max**, e.g. `QAD/UNH–Research` = Director + Evidence + Industry + Customer + Management (5); `QAD/UNH–Challenge` = Red Team + Evidence Lead + Auditor, with Underwriter receiving immutable full packet separately to preserve analytical independence.
- Asynchronous `@Bot` handoff for direct questions. Every stage has one owner; do not ask `@everyone` to duplicate work.
- Code/PR state and public-safe artifacts in GitHub; confidential research only in approved private IIP storage. Internal Bot chat transcript/memory is **not** publication, evidence verification or approval.

### F5. Activation vs existence — truthful roster states

For every target Bot, record **`UNVERIFIED` → `CREATED` → `PROFILE_CONFIGURED` → `HANDOFF_TESTED` → `ACTIVE_ON_DEMAND`** in the **Section L tracker** (these are deployment bookkeeping labels, not new canonical QAD status enums). **Provisioning Done = 26 distinct accessible Bot profiles with durable names, role instructions, and working Bot links/IDs; the untested 20+ standby Bots remain `PROFILE_CONFIGURED`, not `ACTIVE_ON_DEMAND`.** A Bot is `ACTIVE_ON_DEMAND` only after a real acknowledged handoff and output. Maintain the full 26-row roster in this one plan and report `created/26`, `configured/26`, `handoff-tested/26`; do not drop unavailable Bots silently. If creation requires Founder interaction or entitlement, return exact mobile UI steps and a per-Bot blocker without creating substitute agents. **Neither `.cursor/agents/` files, `actor_id` strings nor task-scoped Cloud Agents prove a durable Bot exists.**

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

1. **Create/configure all 26 durable Bot profiles upfront in Section L B0** (retain the existing IIP Lead plus create 25), rather than deferring role creation by research milestones. **Activate only the Director/Evidence/Industry/Customer/Management pilot cohort** for the first Bot-to-Bot demonstration; 26 created does NOT mean 26 simultaneously working.
2. Reuse the existing UNH R&D case from PRs #3–#6. Demonstrate an actually coordinated Bot handoff on a NEW material Evidence Gap, with original-source validation and independent challenge. Do not repeat already completed UNH specialist work merely to populate Bot histories.
3. Capture and re-open sources, derive at least one verifiable assertion from source data, and **deliver one free-form Google Doc in the private Drive case folder** accessible from the Founder's iPhone; do not treat the legacy `/library` frontend as research output.
4. Persist evidence, claims, challenged assertions, and case/version IDs to IIP's intended structured destination, without overwriting history.
5. Compare time, cost and quality against the old manual/NotebookLM-assisted workflow.

**Done when:** a real **Bot→Bot** task yields source-checked, recoverable canonical QAD case evidence and a truthful free-form DRAFT Google Doc accessible to the Founder in its stable Drive case folder. The website `/library`/Vercel preview is not a QAD output gate.

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

**Updated shortest sequence (Founder 2026-10-18):** (1) **IIP-Lead provisions/registers all 26 real Bots in a single first work package**, retaining the Lead and creating 25 new Bots. Record exact ID/link and baseline role config per row before leaving provisioning. (2) After all accessible Bots are created/configured, do one real bounded Director→Specialist→Evidence Lead handoff; dormant 20+ Bots incur no scheduled tasks. (3) In parallel, scoped engineering fixes both critical PR #6 evidence trust and case-recovery defects with tests. (4) Test independent assurance and a fresh UNH evidence gap, then proceed with case workflow. **Do not defer any missing Bot to an unspecified future research phase**. If platform limits prevent all 26, report the exact shortfall promptly and retain a named owner/date/next action for each remaining row. No 26-way concurrent research. Hermes local work stays `DEFERRED_SYNC`.

**CURRENT immediate work package (Founder 2026-10-18 afternoon; overrides older B0/B1 sequencing above):** 26/26 Grok Bot creation and B1/B2 public-source research have been reported; PR #6 latest research/evidence work is on `grok/qad-specialist-routing@d68f9524` and remains unmerged. **Do not resume rebuilding the old `/library` web report, or spend more effort debugging its Vercel Preview for QAD delivery.** Instead deliver one **free-form Thai Google Doc** from the existing `CASE-2026-001` B1 findings in the private **`IIP — QAD Research/00_ACTIVE_CASES/UNH__CASE-2026-001/`** folder now created in the Founder's Google Drive. Report private live Doc URL, DRAFT state, sources/limitations, and confirm Founder can open it on iPhone. No 42-claim re-research, no routine activation, no public/private secrets crossover, no added approval paperwork. Continue substantive QAD research once this reading path works.

**Explicit no-go:** don't claim Group Chat transcripts, Bot IDs, bot-to-bot messages, a Vercel preview, or an agent-generated citation establishes a verified canonical fact; don't turn 5 paused cron jobs on; don't merge into `main` or deploy production; don't create a false independent assurance role in the same execution.

## L. Separate Research Bot deployment plan — all 26 provisioned first, gradual operational activation

| Phase | Real capability (not paper) | Acceptance check | Bot population |
|---|---|---|---|
| **B0 — Provision entire roster NOW (first work package)** | Keep/confirm **IIP-Lead**, create **all 25 other durable Bots** listed in Sections F1–F3 **before the workstream moves on**, and set each Bot's name, bounded job, canonical role, source-of-truth URL and forbidden actions. Use a manageable sequential/batched creation process; do not open 25 research jobs. | **26/26 actual Bot profiles** accessible and named, role configured, exact IDs/links recorded in tracker below. Deadline target **48 hours after prompt receipt**; if blocked by quota/UI, report exact uncreated count, concrete error, Founder-required action and updated completion date (do not fake count). | **26 provisioned; only Lead working** |
| **B1 — Small Bot collaboration smoke** | Create one task-focused group or direct handoff: Research Director → one relevant Specialist → Evidence Lead (optionally a second specialist), using a fresh material UNH gap without duplicating old results. | Actual handoff acknowledgment, sources checked by recipient, case ID/gap ID preserved, returned research result; do **not** mark all idle Bots active merely for existing. | **26 exist; 3–4 active on one task** |
| **B2 — Evidence/recovery fix (parallel engineering)** | Correct PR #6 unverified-fact promotion and transient post-ingest loss via approved original-source verification and persistence/replay. | Fabricated quote at real URL never becomes VERIFIED; fresh process/authenticated Case API recovers accepted evidence/IR/stage state; no new schema. | **26 remain available; no mass invocation** |
| **B3 — Independent decision chain** | With **already-provisioned** Red Team, Independent Auditor and Chief Underwriter, run separately assigned source-level challenge, evidence audit and underwriting deliberation on the permitted partial case; preserve incomplete status. | Three **distinct existing Bot identities** actually execute independent contributions; record unresolved challenge; no false `FOUNDER_READY`. | **26 exist; 3 assurance Bots selectively activated** |
| **B4 — Roster configuration/coverage check (NOT late Bot creation)** | Audit all 26 role scopes, links and on-demand reachability without fabricating research outputs; selectively smoke-test remaining specialist routing only when a relevant task exists. | **26/26 provisioned since B0**; confirm correct ownership, compatible contracts, no duplicate research/overlap, no automatic routines. | **26 ready/standby** |
| **B5 — Full QAD vertical slice** | One full research case per accepted M3 stages: Discovery→Selection→H1–H5 Charter→Evidence→Core→Scuttlebutt→Impairment→Valuation→Red Team→Audit→Underwriter→Thai Editor→Founder Review→Monitoring. | Reproducible evidence-gated case record, original sources, genuine independent challenge and mobile reading; do not auto-approve missing work. | **Selective on-demand Bots only** |
| **B6 — Optional routines** | Only after B5 and measured quota, propose at most one useful low-cost routine; existing five cron jobs remain separately gated. | Real measured value, no silent overages or unapproved job activation. | As needed |

### L1. Mandatory 26-Bot Provisioning Tracker (update rows as Bots are actually created)

**Trigger:** Founder sends the first Bot-provisioning instruction to IIP-Lead. **Due target:** all 26 distinct Bot identities within **48 hours from prompt receipt**; if account/UI limitations block progress, promptly return a complete blocked roster and the action needed rather than silently delaying B0. Do not infer actual creation from a report, group-chat role, subagent file, shared computer folder or `actor_id`. The roster is a deployment index only; IIP analytical records remain authoritative for research. GitHub cannot itself create personal Grok Bots.

| # | Bot name | Department | Org group | Verified state at plan update | Actual Bot link / ID |
|---:|---|---|---|---|
| 1 | `IIP-Lead` | Executive & Research Management | Control | EXISTING — link to verify | — |
| 2 | `IIP-Discovery-Scout` | Data & Discovery | Control | UNVERIFIED | — |
| 3 | `IIP-Research-Director` | Executive & Research Management | Control | UNVERIFIED | — |
| 4 | `IIP-Evidence-Lead` | Data & Discovery | Assurance | UNVERIFIED | — |
| 5 | `IIP-Structural-Red-Team` | Independent Assurance & Underwriting | Assurance | UNVERIFIED | — |
| 6 | `IIP-Independent-Auditor` | Independent Assurance & Underwriting | Assurance | UNVERIFIED | — |
| 7 | `IIP-Chief-Underwriter` | Independent Assurance & Underwriting | Assurance | UNVERIFIED | — |
| 8 | `IIP-Thai-Editor` | Editorial & Knowledge | Publication | UNVERIFIED | — |
| 9 | `IIP-Thesis-Steward` | Editorial & Knowledge | Monitoring | UNVERIFIED | — |
| 10 | `IIP-Business-Moat` | Equity & Valuation Research | Core | UNVERIFIED | — |
| 11 | `IIP-Industry-Economics` | Industry & Competitive Intelligence | Core | UNVERIFIED | — |
| 12 | `IIP-Financial-Accounting` | Equity & Valuation Research | Core | UNVERIFIED | — |
| 13 | `IIP-Management-Allocation` | Equity & Valuation Research | Core | UNVERIFIED | — |
| 14 | `IIP-Impairment-Recovery` | Equity & Valuation Research | Core | UNVERIFIED | — |
| 15 | `IIP-Valuation-Expectations` | Equity & Valuation Research | Core | UNVERIFIED | — |
| 16 | `IIP-Customer-Product` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 17 | `IIP-Competitor` | Industry & Competitive Intelligence | Investigator | UNVERIFIED | — |
| 18 | `IIP-Supplier` | Industry & Competitive Intelligence | Investigator | UNVERIFIED | — |
| 19 | `IIP-Channel-Distribution` | Industry & Competitive Intelligence | Investigator | UNVERIFIED | — |
| 20 | `IIP-Employee-Organization` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 21 | `IIP-Digital-Social` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 22 | `IIP-Regulatory` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 23 | `IIP-Technology-IP` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 24 | `IIP-Scientific-Clinical` | Customer & Specialized Intelligence | Investigator | UNVERIFIED | — |
| 25 | `IIP-Geographic` | Industry & Competitive Intelligence | Investigator | UNVERIFIED | — |
| 26 | `IIP-Industry-Specialist` | Industry & Competitive Intelligence | Investigator | UNVERIFIED | — |
 
**Public-repository safety:** This GitHub repository is public. Track non-sensitive Bot names, provisioned counts and masked/opaque references here. Do **not** publish private conversation deep links, invite/share tokens, credentials, or secret-bearing identifiers in this tracker. Keep full private Bot links and verification screenshots in the Founder's private Grok Bot workspace, with an unambiguous private-registry pointer here. An accessible personal Bot link for the Founder may be returned in the private IIP Lead chat instead of being committed to GitHub. Genuine proof remains required; public-safe redaction is not proof of non-existence.

**Bot creation status must not be conflated with use:** `CREATED` = real separate Bot exists; `PROFILE_CONFIGURED` = role and bounded permissions configured; `HANDOFF_TESTED` = actual Bot-to-Bot message with acknowledgment; `ACTIVE_ON_DEMAND` = first substantive scoped result. All 26 are created/configured up front; only a small working subset needs a live handoff in B1. Do not schedule regular tasks for dormant profiles. Update the 26 rows in **one batch commit** when possible to avoid 26 documentation-only PRs.

**Execution budget:** Research Director selects bots by Evidence Gap and EIV; at most 3 parallel active investigators unless existing policy explicitly permits more. The 17+9 Bots are durable role owners, not a quota of simultaneous LLM contexts. Capture observed per-task time/cost when the platform exposes it; record `NOT_EXPOSED` rather than fake 0. Avoid approving paid overages. Bot names must remain stable; duplicate work prevented by case/gap/version owner and idempotent storage.

**One-case working proof:** IIP Lead → Research Director delegates an unresolved UNH gap to real specialist → Evidence Lead checks independent original-source provenance → challenge when stage permits → canonical IIP case recovered → **Founder reads a truthful DRAFT free-form Google Doc via private Drive on iPhone**. Never require legacy `/library`. If incomplete, deliver only the last proven stage and identify missing pieces.

**Workflow rules:** No separate persistence or source-of-truth in Bot chat or an old `grok-research-team` repo; no 17 permanent worker polling loops; no confidential thesis in public IIP repository. Treat Bot creation as authorized by this Founder decision but any external service account login, quota overage, secret grant, production release or mandatory policy override still follows its actual applicable approval.

## M. Department workflow and Routines/Schedules — proposed, not activated

### M1. Organizational workflow — permanent departments vs per-case team

```text
Founder → IIP-Lead (Executive: coordination / engineering)
            ├─ Data & Discovery: structured source sensors + Scout
            │       → Registry → S1 policy Selection Engine (software, not Bot)
            └─ Research Director (Executive: one accountable Case owner)
                    → H1–H5 Charter + gap map + Evidence Lead check + S2 budget
                    → Equity & Valuation Research: Business, Financial, Management
                    ↔ Industry & Competitive Intelligence: sector, peers, supply chain
                    ↔ Customer & Specialized Intelligence: customer, tech, policy etc.
                       (select only material Evidence Gaps; <=3 active investigators)
                    → Data & Discovery: Evidence Lead independently checks originals
                    → Equity: Impairment/Recovery → Valuation/Expectations
                    → Independent Assurance: Structural Red Team → Independent Audit
                    → Independent Assurance: Chief Underwriter adjudication
                    → Editorial & Knowledge: Thai Editor writes free-form Google Doc in private IIP/QAD Drive
                    → Founder Review / Decision (human authority)
                    → Thesis Steward monitors approved thesis and new evidence
```

This depicts **artifact flow, not approval authority or an override of M3 state transitions**. The binding order, stop conditions, independent audit/underwriting requirements and 18 research stages remain in `project-definition/qad/QAD-FULL-RESEARCH-PROTOCOL.md`, M3-01 and M3 role/service registry. Original source material must independently substantiate each VERIFIED financial claim; a Bot's citation is not proof. No QA/Audit/Underwriting gate is replaced by a simple Bot opinion.

A Case Team (e.g. `QAD/CASE-2026-001`) assembles 1 Research Director, relevant dimension Bots (usually 2–3), Evidence Lead and separately scheduled challenge/assurance Bots. Every handoff names case ID/version, evidence gap, charter/source refs, PIT, hypothesis, work owner, output, limits and receipt. Preserve disagreement. **Durable knowledge resides in canonical IIP Case/Evidence services**, not group chats.

### M2. Routine/Schedule operating model (all suggested routines **OFF**)

**Create 26 Bot identities in B0 with ZERO scheduled routines.** A Bot may own a Grok Routine triggered by time or a supported event; **a Routine is not a Bot, a GitHub Action, nor an IIP cron job**. On-demand Bot-to-Bot messaging from a triggered owner is permissible within role/budget constraints. Keep existing IIP **five cron jobs PAUSED (5/5)**; no implicit activation. Below are **candidate cadences in Asia/Bangkok**, not operational schedules or authorization:

| Proposed cadence/trigger | Owner(s) | Intended behavior | Status |
|---|---|---|---|
| Event: an approved ingestion job detects new SEC filing / source | Deterministic Data services + Evidence Lead | Archive original, check issuer/period/hash/PIT, update provenance; cheap software first, not LLM polling | **PAUSED / EVENT NOT WIRED** |
| Weekdays Bangkok morning, after prior U.S. trading session | Discovery Scout (one trial owner), summary via IIP-Lead | Digest ONLY material new candidate/gap deltas; deterministic S1 owns selection; zero-change result explicit or suppressed as authorized | **NOT CONFIGURED** |
| Event: approved candidate or Founder direction | Research Director | Case-open/H1–H5 charter and source plan, idempotent `case_id` | **MANUAL; NOT WIRED** |
| Event: valid high-EIV material Evidence Gap and authorized budget | Relevant Core/Elastic Bot | Bounded investigation, source checks, contradictory facts, stop condition; max 3 active investigators | **MANUAL ONLY** |
| Event: specialist evidence awaiting admission | Evidence Lead | Independently read original sources; fact remains RAW/UNVERIFIED until real verification and durable admission | **MANUAL; PR #6 TRUST FIX OPEN** |
| Event: required stage outputs truly ready | Structural Red Team, Auditor, Underwriter in approved order | Separate source-facing challenge, source/calculation audit and independent adjudication | **MANUAL ONLY** |
| Weekly Friday Bangkok morning, approved active cases only | Thesis Steward | Watch thesis falsifiers and material changes; reopen research question only under approved state transition | **NOT CONFIGURED** |
| Weekly Monday Bangkok morning, or bundled into daily digest | IIP-Lead | One compact operating report: 26/26 roster, work-in-progress, case queue, stalled gaps, usage | **NOT CONFIGURED** |
| Monthly / manual | IIP-Lead + deterministic checks | Verify Bot links/roles, run history, schedule health and data-source coverage without 26-Bot roll call | **MANUAL** |

**Rules and activation sequence:**
1. First **B0: create/configure all 26**, no scheduled work; B1: prove manual Bot-to-Bot collaboration; B2: fix PR #6 evidence trust and persistence; B5: validate one meaningful vertical research workflow. Then Founder may separately authorize **one low-cost pilot Routine** with actual usage cap, source freshness and stop behavior. No automatic schedule rollout merely because a Bot is created.
2. At approval time specify owner, exact interval/time zone, event filter, idempotency key, input bounds, maximum tools/sources/cost, scope, allowed writes, empty and error outputs, escalation and pause/kill control. Set each owner Bot's Timezone to `Asia/Bangkok` where applicable and inspect routine saved schedule/run history in the Bot profile.
3. Avoid duplicate workflows between 5 paused cron jobs, Routines and GitHub Actions. Prefer cheap structured sensors for universe-wide work; let a paid reasoning Bot work only on a narrowed, evidence-bearing candidate. No 26-way daily polling, and no automatic trade/production/Founder approval.
4. All five prior IIP cron jobs remain PAUSED until individually reauthorized with working evidence, unaffected by this document. Failed source retrieval, quota exhaustion or no new evidence must not fabricate research findings.
5. Group chats and Bot-to-Bot messages consume usage. Department staffing does not imply scheduled work or secure isolation; all personal Bots share their owner's cloud computer/logins.

**Platform references:** https://prod.cursor.com/help/grok-bot/how-to (iOS/desktop Sections); https://prod.cursor.com/help/grok-bot/group-chats (actual Bot-to-Bot/group behavior); https://prod.cursor.com/help/grok-bot/routines (schedule/event Routines, timezone, usage and paused state).

---

### Source references (read selectively, not as alternate plans)

- `00-FOUNDERS-MANIFESTO.md`, `01-PROJECT-DNA.md`, `02-PROJECT-CONSTITUTION.md`, `operational/FOUNDERS-DECISIONS.md`
- `design/qad-pivot/REVISED-QAD-MASTER-PLAN.md` — the existing approved/design lineage for QAD M0–M15, **not** a competing live migration execution checklist
- `design/qad-pivot/LEAN-CANONICAL-SPEC-PLAN.md` — QAD contract taxonomy
- `evidence/m6.7/TRUST-BOUNDARY-AND-M6.8-ACCEPTANCE-REQUIREMENT-2026-10-14.md`
- `PROJECT_STATE.md`, `AGENTS.md`, `operational/ROADMAP.md` — current facts/rules/historical product phase history (not all separate sources of the next task)
- Official Grok Bot documentation: `https://cursor.com/docs/grok-bot/work` (durable Bots, creation, direct Bot-to-Bot handoffs, 2–6 Bot groups, shared cloud computer), `https://prod.cursor.com/docs/agent/projects` (Cursor Project coordinators, distinct from durable Bots), `https://cursor.com/docs/subagents` (task-scoped subagents, distinct from durable Bots), `https://prod.cursor.com/docs/cloud-agent`.

**Change policy:** amend *this file* for changes in execution priority or integration approach and reference the change's specific commit. Do not create `MASTER_PLAN_v2_FINAL_REAL.md` forks. The objective is one navigable plan with verifiable running software, not file-count growth.
