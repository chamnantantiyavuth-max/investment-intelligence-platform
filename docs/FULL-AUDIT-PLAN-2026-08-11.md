# FULL AUDIT PLAN — IIP (prepared 11 Aug 2026, execution next round)

**Status:** PLAN READY — execution deferred to next session per Founder
**Execution rule (FD-HERMES-007):** governance/full audit MUST be delegated to
**GPT-5.6 Sol Medium** (openai-codex) — Parent does NOT self-audit. Fallback:
gpt-5.6-luna (openrouter, reasoning=high). Report fallback to Founder.
**Scope basis:** FD #95 (WP1-3) + FD #96 (blog layout) + FD #97 (CS discovery +
WP2 live + inflection research ×4) + WIL #3 + correction-propagation lesson.
Current HEAD `bcbac49`, fd_count 113, suite 206/206 + 5/5 (py314).

---

## 0. Pre-audit snapshot (Parent, 5 min)

- [ ] `git status` clean (except ciw-pilot cron draft) · `git log origin/main..HEAD` = 0
- [ ] `python -m pytest -q` → expect 206/206; `python3 -m pytest tests/py314/ -q` → 5/5
- [ ] Record HEAD + fd_count + library count (33 published / 19 mains expected) into the audit brief

## 1. Governance audit (delegate to Sol Medium — the core mandate)

**Targets (read-only, cross-check consistency, report CONTRADICTIONS only):**

| Doc | Check |
|---|---|
| PROJECT_BIBLE.md + constitutional amendments | vs FOUNDERS-DECISIONS items 1–113 — any approved FD not reflected? any §23.9 correction missing CORRECTIONS-RECORD entry? |
| AGENTS.md | checkpoint fd-79-96 present (lines ~151–156); footer 14:30 UTC+7 11 Aug; no stale claims (checklist "cron F1/F2 CLOSED" reality) |
| operational/FOUNDERS-DECISIONS.md | items contiguous 1..113; each FD has date + delivery status; item 113 (FD #97) matches reality |
| project-definition/ specs | no drift vs new discovery layers (equity_universe, quality_asymmetry, cs_product) — new code must NOT contradict approved domain semantics |
| 02-PROJECT-CONSTITUTION.md | portfolio-blind §23.8.1 intact; advisory-only; no broker/execution introduced |
| ADRs | ADR-001 status; any new architecture claim needs ADR |

**Governance sync (FD-HERMES-008):** shared SOUL == profile SOUL (version string,
3 gates, 3-tier routing) — Parent verifies, Sol Medium confirms no drift.

## 2. Workflow/contract audit (Sol Medium)

- [ ] Template 16 stage 7b (correction propagation) present + binding — confirm the
  silver-anchor lesson is actually encoded (it is: commit `bcbac49`)
- [ ] Template 12 §10 sweep language present
- [ ] FD #88/#89 firewall intact: no auto-card/auto-CoS/auto-publish path in
  equity_inflection / quality_asymmetry / cs_product code (grep for writes to
  kanban/cards or reports/ from discovery code)
- [ ] Kanban cards 0018..0021 in Research state match published reports
  (RM-2026-0005..0008); 0016/0017 triage A recorded
- [ ] Category taxonomy (FD #96) consistent: frontmatter `category` on all 33
  reports; REPORT_CATEGORIES canonical list matches

## 3. Financial-logic audit (Sol Medium, highest care)

- [ ] **4 inflection reports (ABBV/BMY/LLY/VRTX)** — re-derive every headline
  figure from primary filings (8-K/10-Q accessions in evidence-logs):
  Q2 EPS, revenue, growth %, guidance, segment figures. Confirm FACTS LOCKED
  claims (31/31, 31/31, 39/39, 29/29) are real — spot-check the token lists.
- [ ] Scanner arithmetic: universe-scan-2026-08-11.json — H1 TTM EPS math,
  prior-max logic, revenue confirmation (esp. LLY +48% vs scanner +80.5% —
  release wins, documented)
- [ ] WP2 shadow evidence: 62 blocks — confirm all thresholds PROPOSED (FD #53),
  no production claim
- [ ] company_weekly figures vs radar digest 2026-08-10 (point-in-time stamps)
- [ ] **Silver anchor end-state:** no live surface shows 88:1/low-$20s as current
  fact (grep reports/) — correction pointers present on product-note; ratio
  ~67:1 (11 Aug) consistent

## 4. Verification evidence audit (Parent collects, Sol Medium judges)

- [ ] Suite evidence: pytest 206/206 + py314 5/5 outputs captured to
  `evidence/audit-2026-08-XX/` (timestamped)
- [ ] Browser evidence: /library categories + inflection section screenshot
  (existing `evidence/ui/fd97-inflection-reports/`) — Sol Medium re-verifies
  live page if browser available, else accepts captured evidence with caveat
- [ ] Vercel deploy: iip-research.vercel.app live, alias points to latest build
- [ ] No secrets in tree: grep .env / keys / tokens in reports/ + research/
  (git-secret-scan pattern)

## 5. Audit output contract (Sol Medium MUST produce)

Write to `evidence/audit-2026-08-XX/AUDIT-FINDINGS.md`:
- Verdict per section: PASS / FINDINGS (severity MAJOR/MINOR)
- Each finding: concrete + linked to evidence + material impact + smallest
  correction + verify method (per llm-council finding contract)
- **Corrections record:** list of actionable items → Parent applies → re-audit
  if any MAJOR
- No finding = acceptable result (absence is a valid outcome)

## 6. Post-audit (Parent)

- [ ] Apply accepted corrections (smallest fix, one commit per finding or grouped)
- [ ] If MAJOR → re-audit round on the corrected scope
- [ ] Register audit outcome in PROJECT_STATE + closeout + memory
- [ ] No Bible/plan/code edits by Sol Medium — findings only (audit = read-only)

## Execution checklist for next session

1. `bash start-backend.sh` not needed (backend not required for audit)
2. Load `governance-audit` skill + `llm-council` skill (finding contract)
3. `delegate_task` → Sol Medium (openai-codex), goal = audit brief + targets +
   output contract verbatim; context = HEAD, paths, expected values
4. Collect `evidence/audit-2026-08-XX/AUDIT-FINDINGS.md` → verify file exists
   and read it (child self-report = not proof; file is proof)
5. Present findings to Founder → Founder decides fixes/acceptance

---
*Plan prepared 11 Aug 2026 by Parent (Flash) — execution delegated to Sol Medium per FD-HERMES-007. Founder-approved direction: "ผมจะให้ทำ full audit รอบถัดไปคุณเตรียม plan ไว้ให้หน่อย"*
<!-- 2026-08-11 21:15 UTC+7 -->
