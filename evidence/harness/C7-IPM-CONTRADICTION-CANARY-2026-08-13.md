# C7 — IPM Repository Contradiction Resolution + Production Docker Canary (13 Aug 2026)

> Correction pass C7 per Founder directive.

## 1. Contradiction resolved

| Source | Claim |
|---|---|
| Stage 1 runtime audit (`evidence/harness/STAGE1-REPORT-2026-08-12.md` line 7) | "IIP repo HEAD 9967459 + **IPM repo HEAD abc7436**" — the real IPM repo was recorded |
| Stage 7 closeout (`S7-CUTOVER-CLOSEOUT-2026-08-13.md` §4 + §10 finding 2) | "real IPM repo does not exist yet — simulated only" |

**Verdict: Stage 7 made a path-resolution error.** The real IPM repository EXISTS at
`C:\Users\Admin\Desktop\Antigravity\independent-portfolio-manager`:

```
HEAD abc7436  feat(ipm): IPM-DECISION-001 — deliberate no-action on silver; ...
             ee427a9  Week 1 PM Letter + Finding 001 (IPM-FD-003 first full review)
             98f21fb  IPM-FD-003 — IPM consumes published IIP reports (Option A)
```

Content verified on disk: AGENTS.md, IPM-CONSTITUTION.md (v0.2, amended by
IPM-FD-003), decisions/, evidence/, findings/, philosophy/, portfolio-ledger/
(ledger.md + reconcile.py — 200,000.00 no-trade reconciles), postmortems/,
research/, roles/, weekly-letters/. Own Hermes profile `ipm` installed. HEAD
`abc7436` matches the Stage-1 record exactly.

## 2. Production Docker isolation canary — ACTUAL IPM workspace (not synthetic)

Command: `docker run --rm -v "C:/Users/Admin/Desktop/Antigravity/independent-portfolio-manager:/workspace/ipm" nikolaik/python-nodejs:python3.11-nodejs20`

| # | Check | Result |
|---|---|---|
| 1 | Real IPM sentinel visible (`/workspace/ipm/IPM-CONSTITUTION.md`, v0.2 content) | ✅ PASS |
| 2 | IIP private workspace NOT mounted (`ls /workspace/iip` fails) | ✅ PASS |
| 3 | Host paths NOT visible (`ls /c/Users/Admin` fails) | ✅ PASS |
| 3b | `/workspace` contains ONLY `ipm` — zero IIP repo paths | ✅ PASS |
| 4 | Portfolio ledger present inside the IPM-only mount (portfolio data isolated to IPM workspace, never on the shared board) | ✅ PASS |
| 5 | echo ok | ✅ PASS |

**PASS 5/5** — the production Docker isolation pattern (mount mapping per
`STAGE4-DOCKER-PRODUCTION-PATTERN.md`) works against the REAL IPM workspace:
real content visible, IIP private workspace + host paths isolated, portfolio
data confined to the IPM mount.

## 3. Status after C7

- Shared board remains **metadata-only** (sanitized operational references —
  per Master Integration v1.1 privacy boundary; IPM-sensitive artifacts stay in
  the authorized IPM workspace).
- **real portfolio-aware IPM execution = still DISABLED** — the C7 precondition
  (locate real repo ✅ + production canary pass ✅) is now satisfied, but
  ENABLING portfolio-context execution remains a separate Founder decision
  (production docker profile config: docker_forward_env + per-profile mount map
  + credential smoke test + board privacy re-check per the Stage-4 activation
  gate).
- IIP portfolio-blind preserved (IPM→IIP flow remains prohibited).

<!-- 2026-08-13 16:45 UTC+7 -->
