# Company Intelligence Workbench — Publication Standard

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §4, §8, §10; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #6, #8; FD-CIW-004, FD-CIW-005, FD-CIW-006; proposal §13, §16, §17 (adapted)
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. Principle: Founder Review for Every Canonical Change

Per **FD-CIW-004**, during the pilot the **Founder reviews every canonical analytical, thesis, valuation, confidence, and classification change**. Nothing canonical publishes without explicit Founder approval.

- "Canonical" includes: official thesis state changes, valuation ranges/official valuation use, confidence changes, Moat/Earnings-Quality/Value-Trap classification impacts, Current Authoritative artifact versions.
- Approval must identify the exact artifact/change being approved (Constitution §21). Casual agreement is not approval.
- **AI and Cron cannot create authoritative state** — publication is a Founder-only transition (LIFECYCLE §2, §7).

## 2. What May Publish Automatically: The Deterministic-Metadata Allowlist

Required Change #6: **Class C (automatic canonical publication) is disabled during the pilot.** The only exception is an explicit **Founder-approved allowlist of deterministic metadata fields** that:

- are **deterministic** (no model judgment, no interpretation);
- **cannot alter** evidence, thesis, valuation, confidence, classification, or narrative conclusions;
- are versioned and auditable.

Example allowlist candidates (Founder must approve the exact list): source retrieval timestamps, source revision identifiers, filing period labels, publication dates, document hashes. The allowlist **never** includes: thesis status, confidence, valuation figures, classification, or any narrative conclusion.

**Negative test target:** Class C cannot modify canonical analytical content or authoritative state — including through retries or partial updates (Required Change #6 verification).

## 3. Cron Authority (FD-CIW-005)

- **Class A (Scheduled Observation):** permitted — check for new filings, earnings calendars, new official sources, monitor approved Themes/companies, source freshness, detect potentially material events. May create detection records. May **not** change an official thesis.
- **Class B (Scheduled Draft Analysis):** permitted — compare new results with prior expectations, update deterministic calculations, draft an earnings update, propose valuation changes, identify thesis-strengthening/weakening evidence, propose a material review. Output remains **draft or pending review**.
- **Class C (Scheduled Publication):** **disabled for the pilot** (Required Change #6) — no automatic publication to authoritative state.
- Scheduling does not create authority; no Cron job may promote a Theme, approve a Candidate/thesis/valuation/lesson, alter an official rule, or change Founder decisions (proposal §16.2).
- Cron implementation still requires separate Phase 11 authorization (FD-CIW-005) — this standard does not authorize any Cron job.

## 4. Minimum Evidence for Official Thesis / Valuation / Paper Changes (Required Change #8)

Any relevant evidence may **open review**, but an official change requires:

1. **Source-grounded update package** — new facts, new claims, changes from prior period, guidance, financial changes, owner-earnings impact, capital-allocation changes, moat indicators, thesis-supporting/weakening evidence, new risks, valuation impact, unresolved questions, proposed paper changes, confidence and source limitations (proposal §17.3 structure);
2. **Rerun deterministic calculations** from raw sources;
3. **Visible counterevidence** — contradictions preserved, never averaged away;
4. **Independent review** (QUALITY-GATES — mandatory separation);
5. **Founder approval**.

**"Thesis Broken"** requires a **predeclared invalidation condition** or an **explicit Founder decision** — never an AI-only determination (LIFECYCLE §3).

## 5. Append-First and Version Discipline

- The update package is created **before** the canonical artifact is revised (append-first, proposal §17.5).
- Prior versions remain **retrievable**; supersession is explicit and Founder-approved (LIFECYCLE §5).
- One `Current Authoritative` version per artifact at a time.
- A presentation is **never** the canonical source of analytical truth (proposal §13.3) — the Master Research Paper (later slice) is canonical narrative; presentations summarize.

## 6. Obsidian Role (FD-CIW-006)

- Obsidian is the **narrative knowledge layer** — confirmed; it is **never the sole source of structured official state**.
- Obsidian may store research papers, earnings updates, case studies, management histories, moat evolution, thesis history, postmortems, cross-company patterns, approved lessons, playbooks (proposal §13.4).
- Structured official state (state, lineage, evidence identity, decisions, outcomes, official versions) lives in the structured registry — DNA-018.
- Obsidian publication is **not** canonical publication; canonical publication is the Founder-approved structured artifact.

## 7. Publication States and Flow

```
Independent Review pass (reviewer)
  → Founder Review (Founder)
  → Founder approval
  → Published / Current Authoritative (structured result)
  → Monitoring (later slice)
```

Publication requires all prior gates (RESULT-CONTRACT completeness, QUALITY-GATES pass). No gate may be skipped by declaring a change "non-material" (QUALITY-GATES §2).

## 8. Verification Targets

- Negative tests: Class C cannot modify canonical analytical content or authoritative state, including retries/partial updates (Required Change #6).
- Replay test: one earnings update from raw sources reconstructs old paper → proposed changes → review → approval → new authoritative version (Required Change #8).
- Transition tests: AI and automation cannot create authoritative states (Required Change #5).

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #6, #8; Amendment Map §4, §8, §10; FD-CIW-004/005/006; proposal §13/§16/§17 adapted.*
<!-- 2026-08-02 23:48 UTC+7 -->
