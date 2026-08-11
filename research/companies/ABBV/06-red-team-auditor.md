# Red Team Auditor — Independent View (ABBV)

**Date:** 2026-08-11 · **Mandate:** RM-2026-0005 · **Scope:** what could make the whole research exercise wrong

## Audit of the process so far

1. **Scanner trigger verified** — arithmetic consistent (TTM EPS × shares ≈ reported NI). No defect found.
2. **Evidence-log correction mid-session** — FY2025 revenue mislabel (58.1 vs 61.2) caught by Verify-First against raw XBRL year-ends. Process worked; the initial error is a warning that annual-series labeling needs the year-end list, never assumption.
3. **Source hierarchy respected** — 8-K/10-Q primary, XBRL totals secondary, scanner output tertiary. No invented figures.

## What could still be wrong

- **A1 — Adjusted EPS is the entire growth case, and it's company-defined.** If the add-backs ($3.9B contingent consideration, $1.0B IPR&D, litigation reserves) return in H2 (they are lumpy, not gone), adjusted growth moderates sharply. The report's durability case rests on a series management controls.
- **A2 — Revenue growth rate basis.** "Operational +9.5%" vs "reported +10.2%" — the 0.7pp gap is FX. Fine. But immunology operational +14.6% vs reported +15.1% — same caveat. Minor.
- **A3 — The comparator.** FY2025 revenue $61.2B (from XBRL) vs the Q2 FY26 release implying FY25 ~$58-59B (16.99/0.102 YoY math says prior-year Q2 was $15.42B; annualizing segments: immunology FY25 ~$33B + neuro ~$11B + onco ~$6.8B + aesthetics ~$5.2B + other ≈ $56-57B). **DISCREPANCY: XBRL FY2025 $61.2B vs segment-sum ~$56-57B.** This needs reconciliation before publish — either the XBRL annual series includes something the segments don't (rare: discontinued ops? Other revenue? calendar-vs-fiscal mismatch?), or my segment sums are wrong. FLAG FOR RESOLUTION.
- **A4 — Debt deal motive is unknown.** The report must not choose (a) pre-funding as fact. Present as open.
- **A5 — Apogee.** No S-4 yet; any accretion math is speculation. Keep to announced dilution (−$0.14).

## Red-team verdict

Publishable IF: (i) the FY2025 revenue discrepancy (A3) is resolved with a source citation; (ii) adjusted EPS is labeled management-defined with add-back list; (iii) debt deal presented as open question; (iv) no claim of "durable step-change". The honest frame (low-base + real growth, fair multiple, open items) survives my attack; the rosy frame does not.
<!-- 2026-08-11 16:30 UTC+7 -->
