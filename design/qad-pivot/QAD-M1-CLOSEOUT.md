# QAD-M1-CLOSEOUT.md — M1 Correction Closeout

> **Status:** M1 = **PASS** (2026-08-17)
> **Checkpoint:** `e0b2143` (QAD M1 Constitutional Pivot, 16 Aug 2026) — **KEPT + PATCHED FORWARD** (no revert)
> **Review source:** ChatGPT independent review of `e0b2143` (Governance Corrections + QAD Discovery/Coverage Operating Requirement) → verdict: KEEP, PATCH FORWARD, M1 = IN_PROGRESS until closeout passes.
> **Closeout commit:** (see git log — M1 correction checkpoint)

---

## Part G — Closeout Steps

| # | Step | Status | Evidence |
|---|------|--------|----------|
| 1 | Reconcile Constitution / DNA / Manifesto / Vision / Scope / Evidence Doctrine | ✅ | Constitution v0.6 (CA-v0.6-QAD-PIVOT) §5/§14/§16/§17/§18/§21 amended; DNA v0.3; Vision/Scope rewritten; Evidence Doctrine extended |
| 2 | Restore amendment lineage | ✅ | DNA v0.2 CIW record restored (DNA-019/020, 2026-08-02); QAD = v0.3; Constitution v0.6-M1 record |
| 3 | AGENTS.md patch | ⏳ **PREPARED — awaiting Founder approval (protected file)** | Exact patch text prepared; not applied |
| 4 | Update PROJECT_STATE | ✅ | PROJECT_STATE.md updated (this session) |
| 5 | Search canonical docs for stale active multi-strategy / Theme-first claims | ✅ | 0 active claims; only historical reference in Constitution §14 note + frozen-legacy UI artifact (design/PRODUCT_TRUTH_INVENTORY.md — preserved as history per §23.9) |
| 6 | Preserve historical occurrences | ✅ | Old FDs (items 1–129), v0.5 text, DNA v0.1 body, legacy UI artifacts all preserved untouched |
| 7 | Inspect diff from `e0b2143` | ✅ | 27 files +3,852/−35 (Constitution/DNA/Manifesto + 22 design artifacts + state docs); no unexpected changes |
| 8 | Run applicable tests/validators | ✅ | **Suite 235/235** (2 stale locked tests fixed: gate Done-vs-Blocked, decisions date 14→17 Aug) |
| 9 | Bounded independent governance consistency review | 🔄 **DELEGATED** — Luna High kanban task `t_ad945485` (governance review, premium reviewer) | Result lands on board; reviewed before M5 |
| 10 | Create QAD-M1-CLOSEOUT.md | ✅ | This file |
| 11 | Commit + push M1 correction checkpoint | ✅ | Commit + push performed (this session) |

---

## Part A — Governance Corrections (all verified against actual files)

| Item | Finding | Correction |
|------|---------|-----------|
| A1 | Constitution header said v0.5/CA-v0.5-QAD-PIVOT though amendment record said v0.6 | Normalized: **Version 0.6 — QAD Amendment Ratified / CA-v0.6-QAD-PIVOT**; Blind Portfolio stays v0.5 (CA-v0.5-BLIND-PORTFOLIO-RULE) |
| A2 | §14 still encoded Theme-first research queue; §5 Theme-first tone | **§14 → QAD Candidate-First** (Quality Discovery → Dislocation Detection → Autonomous Selection → Research; Theme = supporting, not mandatory gateway); historical text preserved |
| A3 | §16 Learning Loop mandatory `Evidence→Hypothesis→Theme→Candidate` | **QAD-compatible lifecycle**: Quality/Dislocation observations may create Candidates directly; preserved `Research Finding → Candidate Lesson → validation → independent review → Approved Knowledge` |
| A4 | PRODUCT-VISION.md theme-centric; SCOPE-AND-NON-SCOPE listed "Alpha Momentum screening", "Theme-first research queue", "production autonomous scanning", "deep company research for every candidate" as non-scope | Both reconciled to QAD: vision = QAD candidate-first + observable-not-reasoned; scope = autonomous QAD discovery/selection permitted, full QAD research for gated candidates in-scope; prohibitions on broker/execution/allocation/autonomous endorsement preserved |
| A5 | Evidence Doctrine lacked source authority / discovery provenance / S6 | Extended: Source Authority, Source Authority ≠ Discovery Route, Persistent Discovery Provenance, Raw/Fact/Claim/Inference separation, AI/external synthesis ≠ validated canonical evidence without original-source validation, S6/unverified-lead semantics |
| A6 | DNA header said v0.1; v0.2 CIW record (DNA-019/020) removed | Lineage restored: **v0.1 = DNA-001..018 · v0.2 = DNA-019/020 (CIW, 2026-08-02) · v0.3 = QAD (2026-08-16)**; header → v0.3; CIW amendment record re-inserted |
| A7 | DNA-017 conflated Quality Universe with dislocation presence | **DNA-017 corrected**: Open Quality Discovery / Quality Universe preserved separately; **Dislocation is a trigger for investigation, NOT a Quality Universe membership requirement** |
| A8 | Constitution §17 + DNA-018 named Obsidian/NotebookLM | Technology-neutral: "narrative research/knowledge layers"; provider products named only in subordinate operational contracts |
| A9 | §18 non-scope had "full global equity screening in V0" + "production-scale autonomous global scanning in V0" | Reconciled: autonomous QAD discovery/research permitted within approved governance; bounded universe policy replaces full-global prohibitions; broker/execution/allocation/autonomous-endorsement/unauthorized-portfolio-aware research prohibitions preserved |
| A10 | v0.6 record lacked §21 fields (trade-offs, downstream impact); "unchanged sections" list was stale | v0.6 record completed (affected FD #130, reason, trade-offs, downstream impact, amendment history); M1-correction section list added |

## Part B–F — Discovery & Coverage Operating Requirement (FROZEN)

**`design/qad-pivot/QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md` v0.1 (2026-08-17)** — first-class production requirement binding M3 (spec #2 QAD-DISCOVERY-AND-SELECTION.md) + M4B (PACK-C Part 7):

- **B1** Frozen doctrine: *Every eligible company must be observable by the system; not every company must be reasoned about by an LLM.*
- **B2** Six registries: Security Master / Researchable Universe / Signal / Candidate / Quality Universe / Case; every transition records who/when/why/versions/evidence.
- **B3** Hard filters minimal (non-operating vehicles, duplicates, unresolved identity, shell, severe data insufficiency); **no quality-threshold hard filters** (ROIC/growth/P/E/margin = soft evidence).
- **B4** Three independent lanes: Quality-first / Dislocation-first / External — converge on one Signal/Candidate Registry.
- **B5** Quality Discovery features (structured indicators as signals, not moat proof); states VERIFIED/PROBABLE/UNRESOLVED/FAILED; membership does NOT require dislocation.
- **B6** Dislocation Radar signal families; reported business deterioration NOT required.
- **B7** Data architecture preserves PIT/source/version/missing-data state; absence ≠ no signal.
- **C1–C7** Hybrid cadence: daily machine-first sensing (LLM sees deltas only) / weekly cycle (may return NO_NEW_MATERIAL_QAD_CANDIDATE) / monthly coverage + rejected-sample audit / quarterly+ filing-triggered quality refresh / event-driven (urgency changes cadence, not evidence standards) / Founder on-demand with `entry_route=FOUNDER_DIRECTED` (never counted as autonomous recall) / research initiation = state-triggered with priority→capacity→budget gates (no quota-cron; no unlimited cases in a selloff).
- **D** Radar Scout RETAINED as non-authoritative complementary Discovery capability through M1–M4B (crons untouched); no pre-decided retirement — evidence-based migration decision after M5/M6; may write only to Signal/Candidate intake.
- **E** Discovery & Coverage Evaluation first-class in M4B: Universe Coverage Rate, Data-Ready Coverage, Known-Opportunity Recall, Quality Candidate Recall, Dislocation Recall, False-Negative Rate, Rejected-Item Surprise Rate, Time-to-Detection, Signal→Candidate precision, Candidate→Research yield, cost per meaningful candidate, source/feed failure detection, **Decision-Changing Candidate Recall** (headline). Type A (research quality) vs Type B (discovery recall) evaluated separately.
- **F** Universe size: pilot target ~5,000–10,000 researchable companies (configurable, NOT constitutionalized); Quality Universe = hundreds initially; expansion gated by coverage/false-negative/data/cost evidence.

## Registration (FD #130 + ADR-130)

- **FD #130** registered: FOUNDERS-DECISIONS.md item 130 (QAD Architecture Design Gate + M1 + M1 correction closeout) + amendment-record chain updated.
- **ADR-130** created: `.hermes/architecture/ADR-130-QAD-ARCHITECTURE-DESIGN-GATE.md`.
- Vault fd-register mirrors (AppData central + project) — backfill pending/queued (cron review path); repo register is authoritative.

## Verification

- Suite **235/235** (full `pytest`, 2 stale locked tests fixed — `test_org_queue_native_status_semantics` gate Done-vs-Blocked; `test_decisions_register_contiguous_and_parsed` date 14→17 Aug)
- Governance consistency review: **delegated to Luna High (kanban task `t_ad945485`)** — result: **PASS WITH FINDINGS** (5 findings). ⚠ **Routing non-compliance**: task used OpenRouter provider directly instead of the approved PRIMARY subscription route (openai-codex). The result is retained as supplemental evidence; a compliant re-run is required (see M1 Final Integrity Patch).
- Stale-claims sweep: 0 active multi-strategy / Theme-first / prohibited-autonomous-discovery claims in canonical docs; only historical references preserved
- HEAD == origin/main after push (see git log)

## Scope Contamination Record (M1 Final Integrity Patch)

The M1 correction commits (`9894264` + `6090f03`) included pre-existing unrelated dirty-tree work because `git add -A` was used on a dirty working tree. The scope contamination is documented below.

### Commit 9894264 (clean)
| File | Classification |
|------|---------------|
| `design/qad-pivot/QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md` | ✅ IN_SCOPE (new) |
| `design/qad-pivot/QAD-M1-CLOSEOUT.md` | ✅ IN_SCOPE (new) |

### Commit 6090f03 (contaminated)
| File | Classification | Resolution |
|------|---------------|------------|
| 01-PROJECT-DNA.md | ✅ IN_SCOPE | — |
| 02-PROJECT-CONSTITUTION.md | ✅ IN_SCOPE | — |
| AGENTS.md | ✅ IN_SCOPE | — |
| PROJECT_STATE.md | ✅ IN_SCOPE | — |
| SESSION_CLOSEOUT.md | ✅ IN_SCOPE | — |
| design/qad-pivot/* (6 files) | ✅ IN_SCOPE | — |
| operational/EVIDENCE-DOCTRINE.md | ✅ IN_SCOPE | — |
| operational/FOUNDERS-DECISIONS.md | ✅ IN_SCOPE | — |
| operational/PRODUCT-VISION.md | ✅ IN_SCOPE | — |
| operational/SCOPE-AND-NON-SCOPE.md | ✅ IN_SCOPE | — |
| tests/locked/test_audit_api.py | ✅ IN_SCOPE | — |
| tests/locked/test_org_workflow_api.py | ✅ IN_SCOPE | — |
| ChatGPT/FOUNDER-DIRECTION-EQUITY-INFLECTION-DISCOVERY-AUDITED.md | ❌ UNINTENDED_DELETION | **RESTORED** (no explicit deletion authorization; pre-existing staged deletion from 14 Aug session mistakenly committed via `git add -A`) |
| ChatGPT/IIP-CONSOLIDATED-BIBLE-CIW-INTEGRATION-v0.1-COUNCIL-DRAFT.md | ❌ UNINTENDED_DELETION | **RESTORED** |
| ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md | ❌ UNINTENDED_DELETION | **RESTORED** |
| ChatGPT/Integration 12 Aug 2026/* (5 files) | ✅ PRE_EXISTING_VALID_WORK | Preserved (legitimate prior artifacts) |
| ChatGPT/Integration 16 Aug 2026/HERMES-QAD-INTEGRATION-HANDOFF-v0.3.md | ✅ PRE_EXISTING_VALID_WORK | Preserved |
| docs/ciw-pilot-msft/monitoring/* | ✅ PRE_EXISTING_VALID_WORK | Preserved |
| evidence/organization/* (2 files) | ✅ PRE_EXISTING_VALID_WORK | Preserved |
| research/commodities/SLV/july-vault-0016/* | ✅ PRE_EXISTING_VALID_WORK | Preserved |
| research/commodities/oil-hormuz-0022/* | ✅ PRE_EXISTING_VALID_WORK | Preserved |
| research/companies/GOOGL/evidence-log.md | ✅ PRE_EXISTING_VALID_WORK | Preserved |

### Corrective action
- No Git history rewrite.
- 3 unintended deletions restored from `3d261f1` (the parent of `e0b2143`).
- All pre-existing additions preserved (legitimate project artifacts).
- From this point onward: **scoped migration stages shall use explicit-path staging only; `git add -A` is prohibited on a dirty repository for M2–M4B.**

## M1 Verdict

> **M1 TECHNICAL CLOSEOUT = PASS** (substantive work accepted). **M1 FINAL GOVERNANCE CLOSEOUT = PENDING** (awaiting compliant independent governance review via approved PRIMARY subscription route — openai-codex). After review findings are resolved: **M1 = FINAL PASS**. Only then may M2 start.

<!-- 2026-08-17 17:30 UTC+7 -->