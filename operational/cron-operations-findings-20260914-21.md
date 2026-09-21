# Cron Operations Findings — 2026-09-14 → 2026-09-21 (Reconstructed)

> **Purpose:** Durable operational findings from the deferred cron/radar/monitoring
> backlog (`wip/deferred-ops-backlog-20260921`, 13 commits 14–21 Sep 2026),
> reconstructed cleanly onto current main AFTER the M5.3 freeze (FD #141).
> The original findings lived inside superseded SESSION_CLOSEOUT / PROJECT_STATE
> entries and those stale hunks are NOT restored — this note preserves only the
> durable operational content.
>
> **Source commits (reconstructed, not cherry-picked):** `4f061f1` (16 Sep),
> `8f68003` (17 Sep), `36eb5b2` (21 Sep).
> **Authorized:** Phase O1 Founder disposition (21 Sep 2026).
> **Status:** OBSERVATION + HYPOTHESIS + RECOMMENDATION separated per finding.
> Open operational decisions (N2 disposition, cron write architecture, gateway
> cadence remediation) are RECORDED ONLY — NOT decided or implemented in O1.
>
> No new Founder Decision was created for this reconstruction.

---

## N1 — Host power-state explains some tick gaps (16 Sep)

**OBSERVATION (factual):** The skipped 15 Sep 23:24 tick and the ~19.7 h scheduler
inactivity gap coincided with a Windows power event: `LastBootUpTime` =
16 Sep 2026 11:24:47 (uptime 05m30s at the 16 Sep review) while the scheduler
heartbeat file last updated 15 Sep 15:46:18.

**HYPOTHESIS (superseded in part by N4):** the host was powered off during the
gap (power state, not a gateway crash). A supervisor process cannot fire while
the OS is off, so a durable-gateway-supervision fix cannot cover this class.

**RECOMMENDATION (open):** (A) keep host awake / disable sleep; (B) accept late
catch-up execution as normal; (C) move 08:00 radar slots into the observed
uptime window (~09:30–11:30 UTC+7). — N4 later identified the authoritative
structural cause for the still-awake gaps; both mechanisms coexist.

---

## N2 — Duplicate legacy IIP review job (16 Sep, undisposed)

**OBSERVATION (factual):** `profiles/antigravity-orchestrator/cron/jobs.json`
contains job **`642a42f8cb2e`** "IIP Daily Learning Loop":

- schedule `0 19 * * *` — duplicate of the canonical iip-profile job
  `1f5f03f9236d` (the job that produced the reviewed ticks)
- provider `deepseek` / model `deepseek-v4-pro` — NOT in the FD #111/#112
  frozen routing
- **enabled at discovery** (16 Sep 2026)
- observed firing late 15 Sep 15:44:48, output `[SILENT]`
- **no repo writes observed in the cited run** (kept read-only)
- prompt instructs loading `project-workflow` for an IIP review — contrary to
  the FD-2026-08-14 trigger scoping (research tasks must not auto-load the
  engineering workflow)

**HYPOTHESIS:** duplicate-coverage noise; legacy routing/provider mismatch.

**RECOMMENDATION (OPEN DECISION A — NOT DECIDED IN O1):** retire vs
disable/archive vs re-point `642a42f8cb2e`. It was NOT retired, re-pointed or
modified during O1.

---

## N3 — Global (non-IIP) Hermes cron hygiene (16 Sep)

**OBSERVATION (factual):** two non-IIP jobs failing:

- `06720b5a8470` Identity Sync Watchdog — script path mangled
  (`/bin/bash: C:UsersAdminAppDataLocalHermesscriptsidentity-watchdog.sh:
  No such file or directory`, exit 127); open incident since 26 Aug; last
  attempt 15 Sep 15:44.
- `9d1e5d8a2d7a` Obsidian Session Auto-Save — provider-side failure 15 Sep
  15:45 ("Our servers are currently overloaded"); incident open.

**SCOPE MARKER:** both are OUTSIDE IIP project authority. Recorded for global
Hermes hygiene only; IIP does not own their remediation.

---

## N4 — Gateway trigger root cause (17 Sep, supersedes N1 for awake-gaps)

**OBSERVATION (factual, 3rd independent confirmation by 21 Sep tick):** the
gateway supervisor is the Windows Scheduled Task **`Hermes_Gateway_iip`**
whose ONLY trigger is **At logon** (LastRunTime 21 Sep 10:59:18, NextRunTime
EMPTY, State Ready, schedule type "At logon time"; host up 4d23h at 21 Sep
review with ZERO scheduler activity 18–21 Sep). Launch chain:
`...\profiles\iip\gateway-service\Hermes_Gateway_iip.vbs` →
`python -m hermes_cli.main --profile iip gateway run`.

**HYPOTHESIS (root cause):** because the task fires only at logon, the gateway
(the scheduler owner) is up only after a logon (~11:12–13:1x UTC+7). Any
08:00/09:00 radar/CIW/AM slot scheduled before the daemon starts gets a
late catch-up run at best, and some occurrences are consumed as claims that
never start (see N6).

**RECOMMENDATION (OPEN DECISION C — NOT DECIDED IN O1):** add a repeating
trigger to `Hermes_Gateway_iip` (e.g. daily 07:30 start + repetition every
30 min; trigger-only, no code change) so the morning slots can fire while
the host is on. Multiple independent confirmations now exist (16/17/18/21 Sep).

---

## F8 / F9 — Session-table parsing + closeout-gap findings (17 Sep)

**OBSERVATION (factual):**

- **F8 — Session-table pipe corruption fixed:** a malformed/truncated row in
  the Hermes session table broke parsing during the 16→17 Sep window; the
  review tick repaired the read path (parsing fix, not data fabrication).
- **F9 — closeout-log gap closed:** the 15 Sep and 16 Sep review ticks wrote
  their PROJECT_STATE rows but left no SESSION_CLOSEOUT narrative entry
  (one-sided-closeout pattern); the 17 Sep tick reconstructed those two
  entries with explicit "reconstructed entry" markers (honest provenance).

**HYPOTHESIS:** the one-sided-closeout pattern is a recurring tick bug class
(report written, narrative omitted).

**RECOMMENDATION (open):** make the closeout narrative write part of the same
atomic step as the PROJECT_STATE row (not yet designed — Phase O3+ scope).

---

## N6 — Single-worker claim-starvation mechanism (21 Sep) — CORRECTED CONCLUSION

**OBSERVATION (factual, mechanism):** when the gateway catches up after a
logon, the scheduler detects multiple missed jobs and marks them `claimed`;
the single serial worker then runs the long weekly AM pipeline (~5 min)
AHEAD of the claimed radar/CIW jobs; the claims sit with `started_at` NULL
while `next_run_at` auto-advances. On 21 Sep 10:59 the Learning Loop,
Weekly Radar (08:00 slot) and CIW (09:00 slot) were all claimed; the AM run
occupied the worker 10:59:44→11:04:38 and the radar/CIW claims were still
unstarted at the 11:35 re-check. This is a REAL delay/starvation mechanism.

**HYPOTHESIS (corrected — DO NOT repeat the original "LOST" claim):** the
original 36eb5b2 tick text said the 21 Sep Radar + CIW cycles were "LOST".
That conclusion was PREMATURE. The record on the parking branch itself shows:

- **Weekly Radar 21 Sep eventually completed LATE** and produced the
  `2026-09-21-radar-digest.md` (commit `8546fd4`, 11:25) — 1 Task Idea
  Card (WTI crash), digest present.
- **CIW produced the 21 Sep monitoring draft LATE** (written 11:13, present
  in the working tree and admitted into main in Phase O1 — MSFT NO TRIGGER).

Therefore the cycles were **DELAYED / STARVED, not permanently lost**. The
starvation mechanism is real; the "lost" conclusion is corrected here.

**RECOMMENDATION (open):** order the catch-up queue or prevent `next_run_at`
advancement while a claim is unstarted (Phase O3 design scope; not
implemented in O1). Note the 21 Sep catch-up DID execute for radar + CIW
(11:13/11:25), unlike a genuine loss.

---

## OPEN OPERATIONAL DECISIONS (recorded only — NOT decided in O1)

| # | Decision | Options | Status |
|---|----------|---------|--------|
| A | Duplicate legacy cron `642a42f8cb2e` | retire vs disable/archive vs re-point | OPEN — untouched |
| B | Canonical cron write architecture | status quo vs dedicated ops branch / other isolation (incl. C+ whitelisted-promotion variant) | OPEN — Phase O3 packaging required; Founder has NOT authorized implementation |
| C | Scheduler/gateway cadence remediation | repeating-trigger on `Hermes_Gateway_iip` vs host-power options vs slot re-timing | OPEN |

None were silently implemented in O1. Five repo-writing cron jobs
(`1f5f03f9236d`, `73e611584447`, `8b1cd19aba7d`, `8ba233e88015`,
`cda817d17236`) remain PAUSED.

---

## Scope truth

- Reconstructed from bucket-B commits `4f061f1` / `8f68003` / `36eb5b2`;
  stale PROJECT_STATE / SESSION_CLOSEOUT hunks from those commits were NOT
  restored to main.
- No M5.3 state wording imported ("READY / NOT CLOSED" phrases absent).
- No Founder Decision created. M5.3 remains FOUNDER ACCEPTED / CLOSED /
  FROZEN (FD #141).

<!-- 2026-09-21 13:05 UTC+7 -->