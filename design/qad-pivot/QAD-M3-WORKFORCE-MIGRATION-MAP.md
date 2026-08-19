# QAD-M3 Workforce Migration Map

> **Contract ID:** M3-MIGRATION
> **Status:** M3 FINAL — FROZEN FOR M4 DERIVATION
> **M3 Phase:** M3.13
> **Canonical since:** 2026-08-19
> **Traceability:** Frozen Architecture (Workforce Migration Map specification) · M2 CAP-018 (Hermes Workforce — ACTIVE / TRANSITIONAL_RETAIN — migration deferred)
> **🛑 WARNING: This is a DESIGN-ONLY artifact. No migration is authorized in M3.**

---

## 1. Design Principles

1. **No profiles are changed during M3.** This map is a design for future execution.
2. **The target is the QAD logical organization** (M3-LOGICAL), not necessarily every box as a separate profile.
3. **Separation of duties overrides convenience** — where two logical roles have mandatory separation, they cannot share one profile.
4. **Cost optimization through role combination** — compatible roles may share profiles where research volume justifies it.
5. **Transitional roles remain until explicitly replaced** — nothing is retired without replacement proof.

---

## 2. Current Hermes Profile Inventory

| # | Profile | Current Role | Created |
|---|---------|-------------|---------|
| 1 | `iip` | Bootstrap/control profile | Original |
| 2 | `org-cos` | Chief of Staff | 5 Aug 2026 |
| 3 | `org-ic-secretary` | Investment Committee Secretary | 5 Aug 2026 |
| 4 | `org-commodity-analyst` | Commodity Analyst | 5 Aug 2026 |
| 5 | `org-macro-strategist` | Macro Strategist | 5 Aug 2026 |
| 6 | `org-equity-analyst` | Equity Analyst | 5 Aug 2026 |
| 7 | `org-cro` | Chief Risk Officer / Challenge | 5 Aug 2026 |
| 8 | `org-quant-validator` | Quantitative Validator | 5 Aug 2026 |
| 9 | `org-data-steward` | Data Steward | 5 Aug 2026 |
| 10 | `org-auditor` | Independent Auditor | 5 Aug 2026 |
| 11 | `org-radar-scout` | Radar/Discovery Scout | 6 Aug 2026 |
| 12–20 | org-* assistants | Delegated subagents | 5 Aug 2026 |
| 21 | `ipm` | Portfolio Manager (separate project) | 6 Aug 2026 |

---

## 3. Profile → QAD Logical Role Mapping

### 3.1 Direct Assignment (High Compatibility)

| Current Profile | QAD Logical Role | Compatibility | Conflict? |
|----------------|-----------------|---------------|-----------|
| `org-cro` | Structural Red Team (Role 9) | HIGH — current CRO role is already adversarial challenge | ✅ None |
| `org-auditor` | Independent Auditor (Role 10) | HIGH — current role is independent audit | ✅ None |
| `org-radar-scout` | Discovery & Dislocation Scout (Role 13) | HIGH — current role is already Radar/Discovery Scout | ✅ Must remain TRANSITIONAL until evaluation |

### 3.2 Merge Candidates (Compatible Roles)

| Proposed Profile | Roles Combined | Rationale |
|-----------------|---------------|-----------|
| **Desk Analyst** | Core Desk Researcher (3) + Business & Industry Analyst (4) + Financial & Management Analyst (5) | Three analytical roles are complementary; no separation-of-duty conflict |
| **Impairment & Valuation Analyst** | Impairment Diagnosis Specialist (6) + Valuation Specialist (7) | Different stages, complementary; no conflict |
| **Editor & Monitor** | Thai Editor (11) + Knowledge Steward (12) | Post-publication functions; editorial and monitoring are compatible |
| **Discovery Operator** | Quality Discovery (Svc role) + Dislocation Radar (Svc role) + Candidate Builder (Svc role) | All deterministic/policy services; no agent judgment required |
| **Selection Operator** | Selection Engine (Svc 1) + Research Budget Controller (Svc 2) | Both policy-governed services; no judgment role conflict |

### 3.3 Must-Remain-Separate (No Combination)

| Current Profile | QAD Role | Cannot Combine With |
|----------------|----------|-------------------|
| Research Director | Role 1 | Role 10 Auditor, Role 9 Red Team |
| Evidence Intelligence Lead | Role 2 | Role 10 Auditor, Role 3/4/5 (own evidence) |
| Chief Underwriter | Role 8 | Any research role, any selection role |

### 3.4 New Profiles Required

| Proposed Profile | Based On | Reason |
|-----------------|----------|--------|
| **Research Director** | Current org-cos or org-ic-secretary (re-framed) | Existing CoS/Secretary roles can be re-framed for case orchestration |
| **Evidence Intelligence Lead** | New profile (or split from org-data-steward) | Evidence gatekeeping requires separation from data stewardship |
| **Chief Underwriter** | New profile (highest judgment role) | Must be independent of all research and selection |
| **Elastic Investigator** | Not a permanent profile | Ephemeral subagent spawned on demand |

---

## 4. Migration Actions

### 4.1 Keep-As-Is

| Profile | Migration Action | Precondition |
|---------|-----------------|--------------|
| `org-radar-scout` | KEEP_AS_IS (TRANSITIONAL) | Until QAD Discovery evaluation proves redundancy or value |
| `org-auditor` | KEEP_AS_IS (later REFRAME) | Audit function preserved; reframe contract to QAD standard |
| `ipm` | KEEP_AS_IS | Separate project; no QAD impact |

### 4.2 Reframe (Update Contract, Keep Profile)

| Profile | New QAD Role | Migration Action |
|---------|-------------|-----------------|
| `org-cro` | Structural Red Team | REFRAME_LATER — update role contract from "risk officer" to "structural red team" |
| `org-cos` | Research Director (partial) | REFRAME_LATER — CoS skills overlap with case orchestration |
| `org-ic-secretary` | Research Director (partial) | REFRAME_LATER — IC secretary skills overlap with case orchestration |
| `org-data-steward` | Evidence Intelligence Lead (partial) | MERGE_LATER — data stewardship + evidence gatekeeping |

### 4.3 Merge

| Source Profile | Target Profile | Migration Action |
|---------------|---------------|-----------------|
| `org-equity-analyst` | New: QAD Desk Analyst | MERGE_LATER — equity → QAD desk role |
| `org-commodity-analyst` | New: QAD Desk Analyst | MERGE_LATER — commodity → QAD desk role |
| `org-macro-strategist` | New: QAD Desk Analyst | MERGE_LATER — macro → QAD desk role |

### 4.4 Retire (After Replacement Proof)

| Profile | Retirement Condition |
|---------|---------------------|
| `org-quant-validator` | After QAD Evaluation Harness (Svc 12) covers quantitative validation |
| `org-* assistant profiles` (12–20) | After QAD workforce stabilizes with the new role structure |

### 4.5 Create New

| New Profile | Creation Precondition |
|-------------|----------------------|
| Research Director | M3 Role Contracts approved; case orchestration workflow defined |
| Chief Underwriter | M3 Role Contracts approved; underwriting synthesis workflow defined |
| Evidence Intelligence Lead | M3 Evidence Model (M3-04) and Admission Gate implemented |
| Elastic Investigator (ephemeral) | M3 Scuttlebutt Protocol (M3-05) implemented |

---

## 5. Migration Sequence (Design Only — Not Authorized)

### Phase A: Contract Alignment (post-M3, pre-M5)
1. Update `org-cro` contract → Structural Red Team
2. Update `org-auditor` contract → QAD Independent Auditor
3. Update `org-radar-scout` contract → QAD Discovery Scout

### Phase B: New Profile Creation (M5 gate)
1. Create **Research Director** profile
2. Create **Chief Underwriter** profile
3. Create **Evidence Intelligence Lead** profile (or split from org-data-steward)

### Phase C: Merge Existing (M5+)
1. Create **QAD Desk Analyst** profile (merges equity + commodity + macro)
2. Create **QAD Impairment/Valuation Analyst** profile
3. Create **QAD Editor/Monitor** profile (merges editorial + knowledge)

### Phase D: Retirement (post-production)
1. Retire `org-quant-validator` after Evaluation Harness proven
2. Retire assistant profiles after role structure stabilizes

---

## 6. Risk Table

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Profile merge reduces parallelism | Some cases wait for available analyst | Accept during transition; monitor queue depth |
| Role combination creates subtle conflict | Separation-of-duty violation | Role combination matrix (M3-ROLES) must be enforced in code |
| Reframed profiles still think in legacy terms | Old behavior patterns persist | New role contracts with mandatory structure; old profiles get updated SOUL |
| `org-radar-scout` redundant after QAD Discovery | Wasted cron budget | Radar remains transitional until evaluation proves redundancy — do NOT pre-retire |

---

## 7. M3.13 Non-Negotiable

**No migration is executed in M3.** This map is a design artifact only. Actual profile migration requires:
1. ✅ Approved M3 Role Contracts
2. ✅ Approved Workforce Migration Map (this document)
3. ⏳ Explicit execution authorization from Founder

<!-- 2026-08-19 15:55 UTC+7 -->