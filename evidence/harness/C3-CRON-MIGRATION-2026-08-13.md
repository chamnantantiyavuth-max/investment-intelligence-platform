# C3 — Cron Migration Verification (13 Aug 2026)

> Correction pass C3 per Founder directive. Verifies the two radar cron jobs create
> Hermes `[DISC]`/`[RADAR]` board tasks with date-specific idempotency keys and no
> longer write to the legacy repo board.

## Jobs (post-correction)

| Job | Schedule | Status |
|---|---|---|
| `8ba233e88015` IIP Weekly Radar Scan (FD #78) | Mon 08:00 UTC+7 | enabled, scheduled (next 2026-08-17 08:00) |
| `cda817d17236` IIP Radar Mid-Week Watch (FD #80) | Thu 08:00 UTC+7 | enabled, scheduled (next 2026-08-20 08:00) |

Both prompts rewritten (cronjob update, 13 Aug): STEP 2 creates the run task
`[DISC] ... <YYYY-MM-DD>` with `--idempotency-key radar-weekly-<YYYY-MM-DD>` /
`radar-midweek-<YYYY-MM-DD>`; STEP 2.5 files cards as Hermes board tasks
(`--triage`, key `radar-<weekly|midweek>-<YYYY-MM-DD>-card-<N>`); STEP 3 writes the
digest to `evidence/radar/digests/`; STEP 4 commits ONLY that digest; explicit
boundary: **ZERO writes to `operational/hermes-organization/kanban/`** (frozen).

## Finding (pre-correction)

The 13 Aug mid-week cron run wrote the legacy card `ORG-2026-0022.yaml` AND digest
`2026-08-13-radar-midweek.md` into the old tree and committed them (57b1695) —
the old-board writer path was STILL ACTIVE after the Stage 7.1 freeze marker.
Root cause: both cron prompts still instructed legacy YAML card/digest writes +
commit. Fixed by prompt rewrite above. (Card content duplicated onto the Hermes
board as t_bef038f6 by the same run.)

## Idempotency Proof (live probe on Capital Intelligence board)

| Probe | Key | Result |
|---|---|---|
| W34 create #1 | `radar-weekly-2026-08-17-probe` | t_c335848d |
| W34 retry (same period) | same key | **t_c335848d (SAME task — zero duplicate)** |
| W35 (next period) | `radar-weekly-2026-08-24-probe` | **t_8ce30ed2 (NEW task)** |

Probe tasks archived after proof (not deleted). Semantics verified: same-period
retry → existing task; next-period → new task. Runtime dedup contract confirmed
(CLI: "If a non-archived task with this key exists, its id is returned").

## Obsolete standing tasks archived

- t_535d91be `[DISC][STANDING] IIP Weekly Radar Scan` — archived (fixed-key pattern
  would have deduplicated all future weeks into one task; replaced by per-run keys)
- t_02a53b7b `[DISC][STANDING] IIP Radar Mid-Week Watch` — archived (same reason)

## Zero-legacy-write commitment

- Prompts: explicit ZERO-write boundary for `operational/hermes-organization/kanban/`
- Board-safety hook: extended in C2 to block terminal/write_file/patch writes to the
  old board tree (see C2 evidence)
- Old tree post-C4 contains only frozen migration source (board.md + cards/)

<!-- 2026-08-13 15:40 UTC+7 -->
