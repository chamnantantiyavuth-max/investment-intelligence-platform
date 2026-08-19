# QAD-M3 Traceability Matrix

> **Contract ID:** M3-TRACE
> **Status:** M3 DRAFT (INTERNAL_REVIEW)
> **M3 Phase:** M3.14
> **Canonical since:** 2026-08-19
> **Purpose:** Comprehensive cross-reference table tracing every M3 contract clause to its authoritative source.
> **Source Types:**
> - `Constitution` — 02-PROJECT-CONSTITUTION.md
> - `DNA` — 01-PROJECT-DNA.md
> - `FD` — Founder Decision (e.g., FD #130)
> - `Frozen Architecture` — Architecture Design Gate (ChatGPT prompt)
> - `M2 Capability` — CAP-XXX from QAD-M2-LEGACY-CAPABILITY-REGISTRY.md
> - `CIW Inherited` — CIW pilot (FD-CIW-XXX)
> - `Evidence Doctrine` — operational/EVIDENCE-DOCTRINE.md
> - `Discovery Requirement` — QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md
> - `NEW_M3_DERIVATION` — new derivation created in M3

---

## Matrix Key

| Abbreviation | Full Reference |
|---|---|
| Constitution §N | 02-PROJECT-CONSTITUTION.md, Section N |
| DNA-NNN | 01-PROJECT-DNA.md, Article NNN |
| FD #N | Founder Decision #N (operational/FOUNDERS-DECISIONS.md) |
| FD-CIW-NNN | CIW Pilot Founder Decision |
| Frozen Architecture | Architecture Design Gate (ChatGPT prompt / final adversarial review) |
| CAP-NNN | QAD-M2-LEGACY-CAPABILITY-REGISTRY.md |
| Discovery Req. v0.1 §X | QAD-DISCOVERY-AND-COVERAGE-OPERATING-REQUIREMENT.md v0.1 |
| Evidence Doctrine | operational/EVIDENCE-DOCTRINE.md |
| NEW_M3_DERIVATION | New derivation created in M3 phase (see Appendix A) |

---

## 1. M3-01 — QAD Operating Model

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-01 | §1 Purpose | Define QAD as research & underwriting institution | Constitution | Constitution §1/§2/§18 | — |
| M3-01 | §1 Purpose | Backbone contract; M4A/M4B derives schemas | Frozen Architecture | Architecture Design Gate — system architecture mandate | — |
| M3-01 | §2 North Star | IIP mission: identify situations where temporary impairment is priced as permanent | Constitution | Constitution §1 (central question) | — |
| M3-01 | §2 North Star | Four independent QAD propositions (Quality + Dislocation + Impairment Diagnosis + Valuation Asymmetry) | Constitution | Constitution §1 | — |
| M3-01 | §2 North Star | No composite QAD score; each proposition stands independently | Constitution | Constitution §1 | — |
| M3-01 | §2 North Star | No assumption "good company + low price = QAD" | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §2 North Star | Every case must begin with H1–H5 | Constitution | Constitution §2 | — |
| M3-01 | §2 North Star | Architecture must prevent silent collapse of H1–H5 | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §3.1 Flow Diagram | End-to-end stage flow (Observation → Knowledge Compounding) | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §3.2 Major Lifecycle Phases | 11-phase lifecycle table | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §3.3 Stage State Machine | NOT_STARTED → IN_PROGRESS → COMPLETED/FAILED/INCOMPLETE/SKIPPED | Frozen Architecture | Architecture Design Gate — state machine mandate | — |
| M3-01 | §3.3 Stage State Machine | Stage transitions are append-only; immutable after COMPLETED | Frozen Architecture | Architecture Design Gate — append-only requirement | — |
| M3-01 | §3.4 Canonical vs Noncanonical Boundary | Raw Source Archive, Evidence Registry, Claims, Analytical State = canonical | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-01 | §3.4 Canonical vs Noncanonical Boundary | NotebookLM, AI reasoning, Publication = noncanonical | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-01 | §3.4 Canonical vs Noncanonical Boundary | Only canonical layers produce authoritative outputs | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-01 | §4.1 System-Level Inputs | Security Master, EDGAR, price/volume, industry data, discovery inputs | Frozen Architecture | Architecture Design Gate — system inputs | — |
| M3-01 | §4.2 System-Level Outputs | Case State, Evidence Graph, Red Team, Audit, Underwriting, Publication, Monitoring, Knowledge | Frozen Architecture | Architecture Design Gate — system outputs | — |
| M3-01 | §5.1 Mandatory Separations | 10 separation-of-duty rules | Constitution | Constitution §18 | — |
| M3-01 | §5.1 Mandatory Separations | Discovery ≠ Selection; Selection ≠ Underwriting; Research ≠ Audit; Primary Thesis ≠ Red Team | Constitution | Constitution §18 — separation of duties | — |
| M3-01 | §5.1 Mandatory Separations | Evidence Discovery ≠ Canonical Admission; Calculation Production ≠ Recalculation | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §5.2 Founder Authority | Founder exclusive authority (constitutional changes, FOUNDER_ENDORSED, investment decisions) | Constitution | Constitution §2/§18 | — |
| M3-01 | §5.3 Competing Hypotheses H1–H5 | H1 Temporary impairment; H2 Structural; H3 Mixed; H4 Quality wrong; H5 Valuation fair | Constitution | Constitution §2 | — |
| M3-01 | §5.3 Competing Hypotheses H1–H5 | Architectural requirement: prevent silent collapse into bullish thesis | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §6.1 Failure Mode Definitions | FAILED / INCOMPLETE / SKIPPED states with recovery rules | Frozen Architecture | Architecture Design Gate — failure states | — |
| M3-01 | §6.2 Cardinal Rule | "Failure must never silently become completeness" | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §6.3 Bounded Retries | Max retry count per stage; preserve prior outputs | Frozen Architecture | Architecture Design Gate — bounded retries | — |
| M3-01 | §7.1 Standard Escalation | Analyst → Research Director → Chief Underwriter → Founder | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §7.2 Auditor Escalation | Auditor reports directly to Founder | Constitution | Constitution §18 — auditor independence | — |
| M3-01 | §7.3 Authorized Overrides | Skip stage, increase budget, reopen case, exceptional override | Frozen Architecture | Architecture Design Gate — override policy | — |
| M3-01 | §7.4 Case Replay | Replay conditions (new evidence, material error, Founder authorization) | Frozen Architecture | Architecture Design Gate — replay | — |
| M3-01 | §8.1 Idempotent Stages | Entity Resolution, Financial Calculations, Source Retrieval, Evidence Registry writes | Frozen Architecture | Architecture Design Gate — idempotency | — |
| M3-01 | §8.2 Checkpoints | Checkpoints at every stage boundary | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §8.3 Dependency Tracking | Every stage declares dependencies; validation before execution | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §8.4 Case Locking | Per-case locking; timeout releases as INCOMPLETE | NEW_M3_DERIVATION | Derived from frozen architecture concurrency requirement | — |
| M3-01 | §8.5 Deduplication | Duplicate case, evidence, and signal detection | NEW_M3_DERIVATION | Derived from frozen architecture data integrity requirement | — |
| M3-01 | §9 Research Run Manifest | Mandatory fields (research_run_id → output_version) | Frozen Architecture | Architecture Design Gate — Run Manifest specification | — |
| M3-01 | §9.1 Point-in-Time Lock | AS_OF_DATE set at case opening; no post-date evidence | Evidence Doctrine | Evidence Doctrine; CIW PIT discipline | CAP-017 |
| M3-01 | §9.1 Point-in-Time Lock | Historical evaluation must prohibit post-AS_OF_DATE evidence | Evidence Doctrine | Evidence Doctrine; CIW PIT discipline | CAP-017 |
| M3-01 | §10 Relationship to Other M3 Contracts | Cross-contract dependency map (M3-02 through M3-10) | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | §11 M4A Readiness Note | Derivable schemas for M4A implementation | Frozen Architecture | Architecture Design Gate | — |
| M3-01 | Header Traceability | Constitution §1/§2/§18 · DNA-001–021 · FD #130 · Discovery & Coverage Req. · M2 CAP-009 | FD | FD #130 | CAP-009 |

---

## 2. M3-02 — Discovery & Autonomous Selection Contract

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-02 | §1 Purpose | Materialize Discovery & Coverage Operating Requirement v0.1 | Discovery Requirement | Discovery Req. v0.1 (B1–B7, C1–C7, D, E, F) | — |
| M3-02 | §1 Purpose | "Every eligible company observable; not every company reasoned by LLM" | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §2 Six Registries | Security Master → Researchable Universe → Signal → Candidate → Quality → Case | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §2.1 SECURITY_MASTER | CIK-based primary identity; ticker/sedol/cusip as aliases | M2 Capability | CAP-001 (REUSE) | CAP-001 |
| M3-02 | §2.1 SECURITY_MASTER | Append-only; ticker changes create new records | M2 Capability | CAP-001 (REUSE) | CAP-001 |
| M3-02 | §2.2 RESEARCHABLE_UNIVERSE | Hard exclusion for non-operating vehicles, shell SPAC, duplicates | Frozen Architecture | Architecture Design Gate — hard filters | — |
| M3-02 | §2.2 RESEARCHABLE_UNIVERSE | FORBIDDEN hard exclusions: ROIC, FCF margin, revenue growth, etc. | Constitution | Constitution §18 | — |
| M3-02 | §2.2 RESEARCHABLE_UNIVERSE | State per company: INCLUDED/EXCLUDED/PENDING_RESOLUTION | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §2.2 RESEARCHABLE_UNIVERSE | Silent omissions prohibited | DNA | DNA-004 (Breadth Before Depth) | — |
| M3-02 | §2.3 SIGNAL_REGISTRY | Per-signal provenance (who, when, data version, model version) | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §2.3 SIGNAL_REGISTRY | Three signal families: Quality (Lane A), Dislocation (Lane B), External (Lane C) | Frozen Architecture | Architecture Design Gate — three discovery lanes | — |
| M3-02 | §2.3 SIGNAL_REGISTRY | Merge policy: same ticker + type + date → update | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §2.3 SIGNAL_REGISTRY | Never deleted — only superseded | DNA | DNA-003 (Information Preservation) | — |
| M3-02 | §2.4 CANDIDATE_REGISTRY | Candidate states (6 states) | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §2.5 QUALITY_UNIVERSE | NOT conditioned on active dislocation | DNA | DNA-017 | — |
| M3-02 | §2.5 QUALITY_UNIVERSE | Quality states: VERIFIED/PROBABLE/UNRESOLVED/FAILED | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §2.6 CASE_REGISTRY | Entry routes: AUTONOMOUS_SELECTION / FOUNDER_DIRECTED / MONITORING_ESCALATION | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §2.6 CASE_REGISTRY | Founder-directed labelled entry_route; never counted as autonomous recall | FD | FD #130 | — |
| M3-02 | §3.1 Lane A — Quality-First | Quality Discovery uses structured indicators; deterministic (no LLM) | Discovery Requirement | Discovery Req. v0.1 — Lane A | CAP-001 |
| M3-02 | §3.2 Lane B — Dislocation-First | Dislocation Radar detection → Quick Quality Investigation → candidate | Discovery Requirement | Discovery Req. v0.1 — Lane B | CAP-002 |
| M3-02 | §3.2 Lane B | Signal families for Dislocation Radar (price, earnings, margin, inventory, etc.) | Frozen Architecture | Architecture Design Gate — dislocation signals | CAP-002 |
| M3-02 | §3.2 Lane B | "Reported business deterioration is NOT required" | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §3.3 Lane C — External Discovery | Radar Scout, Founder nomination, competitor/supplier, etc. | Discovery Requirement | Discovery Req. v0.1 — Lane C | CAP-011 |
| M3-02 | §3.3 Lane C | Founder-directed entries labelled FOUNDER_DIRECTED | FD | FD #130 | — |
| M3-02 | §3.4 Lane Convergence | All lanes converge into same Signal/Candidate Registry | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §4.1 Selection States | AUTO_RESEARCH_NOW / WATCH_PRICE / WATCH_EVIDENCE / DATA_LIMITED_WATCH / REJECT | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §4.2 Selection Engine | POLICY_SERVICE (not judgment role); deterministic/policy-governed | Frozen Architecture | Architecture Design Gate — ROLE vs SERVICE distinction | — |
| M3-02 | §4.2 Selection Engine | Cannot be overridden by Research Director or Chief Underwriter | Constitution | Constitution §18 — separation of duties | — |
| M3-02 | §4.3 Priority Ordering | Rank ordering; no composite numerical score | DNA | DNA-009 (Falsifiable Hypotheses) | — |
| M3-02 | §4.4 Capacity Check | Research Budget Controller approval; dedup; case locking | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §4.4 Capacity Check | "Never open unlimited cases during market-wide selloff" | FD | FD #130 | — |
| M3-02 | §5.1 Hard Filters | Hard exclusions only for defined categories; soft evidence never hard filters | Frozen Architecture | Architecture Design Gate — hard vs soft | — |
| M3-02 | §5.2 Soft Evidence | ROIC, FCF margin, revenue growth, debt/EBITDA, P/E, margin — never automatic exclusions | Constitution | Constitution §18 | — |
| M3-02 | §5.3 Signal Quality | Provenance, evidence link, confidence, contradicting evidence | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §5.4 Candidate Quality | Quality signal + dislocation signal + evidence timeline + gaps + researchability | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §6.1 Daily Sensing | Machine-first deterministic sensors; LLM inspects deltas only | Frozen Architecture | Architecture Design Gate | — |
| M3-02 | §6.2 Weekly Discovery Cycle | Full coverage cycle; valid output: NO_NEW_MATERIAL_QAD_CANDIDATE | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §6.3 Monthly Coverage & Rejection Audit | Rejected Sample Audit: 50–100 rejected candidates | Discovery Requirement | Discovery Req. v0.1 — Part E | — |
| M3-02 | §6.4 Quarterly Quality Refresh | Quality evidence state dynamics; triggered by material filings | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-02 | §6.5 Event-Driven | Urgency changes cadence, not evidence standards | DNA | DNA-004 (Breadth Before Depth) | — |
| M3-02 | §6.6 Founder On-Demand | Founder may nominate any company; evidence standards remain intact | Constitution | Constitution §18 — Founder authority | — |
| M3-02 | §6.7 Research Initiation | State-triggered, not quota-cron | DNA | DNA-006 (Hybrid Discovery) | — |
| M3-02 | §7 Radar Scout Disposition | "Radar raises questions; it never answers them" — TRANSITIONAL | FD | FD #130 | CAP-011 |
| M3-02 | §8 M2 Capability Consumption | CAP-001 REUSE; CAP-002 ADAPT; CAP-003 ADAPT; CAP-011 TRANSITIONAL_RETAIN | M2 Capability | M2 Capability Registry | CAP-001, 002, 003, 011 |
| M3-02 | Header Traceability | Constitution §1/§2/§18 · DNA-004/006 · FD #130 · Discovery Req. · M2 CAP-001/-002/-003/-011 | FD | FD #130 | CAP-001, 002, 003, 011 |

---

## 3. M3-03 — Full Research Protocol

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-03 | §1 Purpose | Evolves CIW with full lineage preservation; CIW is ABSORBED | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §1 Purpose | Preserved from CIW: Result Contract, Quality Gates, Claim/source lineage, Deterministic calculations, PIT, Publication gates | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §2.1 Complete Flow | Case Open → Research Charter → Source Foundation → Analysis → Challenge → Audit → Underwriting → Publication | Frozen Architecture | Architecture Design Gate — workflow | — |
| M3-03 | §2.2 Case Open Trigger | 4 conditions: candidate AUTO_RESEARCH_NOW, capacity, budget, dedup | Frozen Architecture | Architecture Design Gate | — |
| M3-03 | §2.2 Case Fields | case_id, company_id, dislocation_event_id, entry_route, as_of_date, stage_state, research_run_id | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §2.3 Research Charter | H1–H5 assessment, evidence strengths/gaps, modules, omissions, budget, stop conditions | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §2.3 Research Charter | Justified module omissions per DNA-019 | DNA | DNA-019 (Deep Research Must Earn Its Cost) | — |
| M3-03 | §2.4 Competing Hypotheses H1–H5 | Initial assessment, key differentiating questions, falsification criteria | Constitution | Constitution §2 | — |
| M3-03 | §3.1 Primary Source Foundation | L1–L10 source priorities (from M3-04); Source Map document | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-03 | §3.2 PIT Lock | as_of_date lock; no post-date evidence | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-03 | §3.3 Evidence Gap Map | Gap ID, domain, question, evidence, method, priority | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §3.3 Evidence Gap Map | Gap classification: resolvable with existing, scuttlebutt, or unresolvable | NEW_M3_DERIVATION | Formalization of CIW evidence gap practice | — |
| M3-03 | §3.4 Deep Research | Reuses Deep Research Contract (CAP-012) — 11-stage workflow | M2 Capability | CAP-012 (REUSE) | CAP-012 |
| M3-03 | §3.4 Deep Research | Spawned from evidence gaps; bounded scope; dissent preserved | M2 Capability | CAP-012 (REUSE) | CAP-012 |
| M3-03 | §3.4 Deep Research | Investigation layer, not conclusive analysis; outputs need validation | M2 Capability | CAP-012 (REUSE) | CAP-012 |
| M3-03 | §3.5 Evidence Graph | Sources → Facts → Claims → Inferences → Hypotheses | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §3.5 Evidence Graph | Edge: evidence_id, relationship (SUPPORTS/CONTRADICTS/MODIFIES/UNRELATED), strength, analyst | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §4.1 CIW Result Contract | Result structure, Quality Gate status, Claim/source lineage, deterministic calculations | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §4.2 CIW Quality Gates (G1–G7) | Source Map → Evidence Foundation → Analysis → Challenge → Audit → Underwriting → Publication | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §4.3 Claim/Source Lineage | Source → Extract → Fact → Claim → Inference | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §4.3 Claim/Source Lineage | Lineage mandatory for quantitative figures, material qualitative assertions, causal statements | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §4.4 PIT Discipline | Source_date on every evidence; as_of_date on analytical output | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-03 | §5.1 Classification | NotebookLM as Research Evidence Room, Persistent Corpus, Cross-source Interrogation, Deep Research Interface | CIW Inherited | FD-CIW-001..016 | — |
| M3-03 | §5.2 Rule | AI synthesis finding must be validated against original source before canonical admission | Evidence Doctrine | Evidence Doctrine (CAP-017) | — |
| M3-03 | §5.3 Abstract Provider Contract | Deep research and research corpus as abstract providers | Frozen Architecture | Architecture Design Gate — abstract interfaces | — |
| M3-03 | §6 Stop Conditions | Thesis-killer, H2/H4/H5 dominates, budget exhausted, acquired/delisted, Founder stop | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-03 | §6 Stop Conditions | Cleaned/terminated case preserved for future reference | DNA | DNA-003 (Information Preservation) | — |
| M3-03 | §7 M4A Readiness Note | Case, ResearchCharter, SourceMap, EvidenceGap, EvidenceGraph schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-03 | Header Traceability | Constitution §1/§2 · DNA-001/019/020 · FD-CIW-001..016 · M2 CAP-009/-012 | CIW Inherited | FD-CIW-001..016 | CAP-009, 012 |

---

## 4. M3-04 — Evidence, Source & Canonical Truth Model

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-04 | §1 Purpose | Formalizes existing Evidence Doctrine under QAD | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §2.1 Source Tier Definitions | L1 Corporate Primary (highest) through L10 Lead-Only Social/Forum (lowest) | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §2.1 Source Tier Definitions | Tiers, examples, weight, requires validation flag per tier | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §2.2 L10 Rule | L10 cannot independently support material conclusion | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §2.3 Source Provenance | source_id, URL, retrieval_timestamp, source_date, source_tier, authority, format, content_hash | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.1 Five-Layer Canonical Model | Raw Source Archive → Evidence Registry → Claims → Analytical State → Publication | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.2 Raw Source Archive | Append-only; never modified; content hash verified on read | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.3 Canonical Evidence Registry | Structured objects; append-only; FACT/CLAIM/INFERENCE/HYPOTHESIS | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.4 Claims / Contradictions / Calculations | Contradictions never resolved by deleting one side | DNA | DNA-002 (Evidence First) | — |
| M3-04 | §3.4 Claims / Contradictions / Calculations | Calculations: formula, input variables, intermediate values, output | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.5 Analytical State | Input hashes, method version, output, uncertainty, contradictions | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.6 Publication Layer | "Publication is presentation, not canonical truth" | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §3.6 Publication Layer | Publications carry PIT disclaimer, case_id, research_run_id, section labels | DNA | DNA-003 (Information Preservation) | — |
| M3-04 | §4.1 FACT schema | fact_id, source_id, source_location, extracted_text, fact_type, as_of_date, verification_status | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §4.2 CLAIM schema | claim_id, supporting_fact_ids, contradicting_fact_ids, claim_text, confidence | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §4.3 INFERENCE schema | inference_id, supporting_claim_ids, infererence_text, domain | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §4.4 HYPOTHESIS schema | hypothesis_id, case_id, hypothesis_type (H1–H5), falsification_criteria, status | Constitution | Constitution §2 | — |
| M3-04 | §5.1 Admission Rules | 7 checks: source exists, tier, extract accuracy, classification, provenance, PIT, contradictions | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-04 | §5.2 Admission Authority | Evidence Intelligence Lead manages admission; Discovery ≠ Admission | Constitution | Constitution §18 — separation of duties | — |
| M3-04 | §5.3 AI Synthesis Validation Rule | AI finding must be validated against original source before admission | Evidence Doctrine | Evidence Doctrine (CAP-017) | — |
| M3-04 | §6 NotebookLM / Deep Research Boundary | NotebookLM as evidence room, not database or truth authority | CIW Inherited | FD-CIW-001..016 | — |
| M3-04 | §7 M2 Capability Consumption | CAP-017 REUSE; CAP-012 REUSE | M2 Capability | M2 Capability Registry | CAP-017, 012 |
| M3-04 | §8 M4A Readiness Note | Source, Fact, Claim, Inference, Hypothesis, EvidenceAdmission schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-04 | Header Traceability | Constitution §4 · DNA-002/003/009 · FD #130 · Evidence Doctrine · M2 CAP-017 | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |

---

## 5. M3-05 — Modern Scuttlebutt Protocol

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-05 | §1 Purpose | Define Modern Scuttlebutt Protocol: lawful, elastic investigator network | NEW_M3_DERIVATION | M3 — formalizes CIW underspecified scuttlebutt practice | CAP-009 |
| M3-05 | §1 Philosophy | Building mosaic from independent sources; not corporate espionage | NEW_M3_DERIVATION | M3 — CIW had ad-hoc scuttlebutt only via Deep Research | — |
| M3-05 | §1 Trigger | Spawned from evidence gap in Research Charter or Evidence Gap Map | NEW_M3_DERIVATION | M3 — formal trigger condition | — |
| M3-05 | §2.1 Investigator Types | 11 investigator types (Customer, Competitor, Supplier, etc.) | NEW_M3_DERIVATION | M3 — formal investigator taxonomy | — |
| M3-05 | §2.2 Classification | ELASTIC_INVESTIGATOR — ephemeral, purpose-built, bounded contract | NEW_M3_DERIVATION | M3 — elastic investigator pattern | — |
| M3-05 | §3 Investigation Contract | Formal contract: investigation_id, evidence_gap_id, falsifiable_question, source_classes | NEW_M3_DERIVATION | M3 — structured investigation contract | — |
| M3-05 | §3.1 Falsifiable Question | Must be falsifiable; examples of good vs bad questions | NEW_M3_DERIVATION | M3 — falsifiability discipline | — |
| M3-05 | §3.2 Independence Requirement | Independence from target company AND from research team | NEW_M3_DERIVATION | M3 — independence safeguard | — |
| M3-05 | §3.3 Stop Rules | Evidence saturation, budget limit, time window, question answered | NEW_M3_DERIVATION | M3 — bounded investigation with stop rules | — |
| M3-05 | §4.1 Hard Prohibitions | No deceptive pretexting, no MNPI solicitation, no IR contact, no social engineering | Constitution | Constitution §18 — lawful research | — |
| M3-05 | §4.2 Allowed Methods | Public filings, reviews, public web, patents, clinical trials, etc. | Constitution | Constitution §18 | — |
| M3-05 | §4.3 Research Budget Controller Oversight | Director proposes, Budget Controller approves | Frozen Architecture | Architecture Design Gate — budget control | — |
| M3-05 | §5.1 Investigation Output | Evidence IDs, Investigation Report, Source List | NEW_M3_DERIVATION | M3 — structured output contract | — |
| M3-05 | §5.2 Evidence Admission Path | Scuttlebutt findings enter same Evidence Registry via Admission Gate | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-05 | §6 Expected Information Value | HIGH/MEDIUM/LOW/DE_MINIMIS with budget and approval levels | NEW_M3_DERIVATION | M3 — EIV framework | — |
| M3-05 | §6.2 Override | Budget Controller may deny; Founder may override | Frozen Architecture | Architecture Design Gate | — |
| M3-05 | §7 M4A Readiness Note | InvestigationContract, InvestigatorType, InvestigationOutput, StopRecord schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-05 | Header Traceability | Constitution §1 · DNA-003 · FD #130 · M2 CAP-009 (CIW absorbed) | FD | FD #130 | CAP-009 |

---

## 6. M3-06 — Business Quality, Industry Economics & Management Contract

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-06 | §1 Purpose | Quality assessed independently of price, dislocation, or impairment | Constitution | Constitution §1 (QAD mission) | — |
| M3-06 | §2.1 Business Anatomy | Products, revenue model, customers, problem solved, retention reasons | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §2.2 Customer Economics | CAC, LTV, LTV/CAC, churn, retention, unit economics | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §2.3 Moat Mechanism Analysis | 12 mechanisms: Switching Cost, Pricing Power, Scale, Network Effects, etc. | Frozen Architecture | Architecture Design Gate (FD #95 precursor) | CAP-003 |
| M3-06 | §2.4 Quality Verification States | VERIFIED / PROBABLE / UNRESOLVED / FAILED | Frozen Architecture | Architecture Design Gate — derived from frozen decisions (FD #95/#130) | CAP-003 |
| M3-06 | §2.4 Quality Verification States | State-specific evidence requirements | Frozen Architecture | Architecture Design Gate — structured quality states | — |
| M3-06 | §2.5 False-Quality Test | 6 tests: good business vs good industry, leverage, sustainability, growth value destruction, melting ice cube, owner-earnings | Frozen Architecture | Architecture Design Gate (FD #95) | CAP-003 |
| M3-06 | §3.1 Industry Structure Framework | Demand → Supply → Capacity → Utilization → Pricing → Margins → ROIC → Capital Entry/Exit | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §3.2 Required Industry Dimensions | Demand, Supply, Capacity, Pricing, Margins, ROIC, Capital, Substitution Risk | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §3.3 Competitive Position | Rank, relative margins, cost, market share trend, competitor assessment | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.1 Management Principle | "Management assessed through Decision History, not charisma" | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.1 Management DO NOT Assess | Presentation style, public persona, vision statements without track record | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.2 Management Claim Ledger | Track management claims vs outcomes (FULFILLED/NOT_FULFILLED) | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.3 Capital Allocation Ledger | Action, amount, rationale, outcome, per-share impact | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.4 Required Management Dimensions | Capital Allocation, Promise vs Outcome, Incentive Alignment, Per-Share Value, etc. | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §4.5 Management Assessment States | STRONG / ADEQUATE / WEAK / UNTESTED / CONCERNING | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §5.1 Quality Analysis Output | Business Anatomy, Moat Assessment, Quality State, False-Quality Test, Unknowns | Frozen Architecture | Architecture Design Gate | CAP-003 |
| M3-06 | §5.2 Industry Analysis Output | Economics summary, competitive position, ROIC/margin structure, risks | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §5.3 Management Analysis Output | Claim Ledger, Capital Ledger, Management State, Incentive Alignment, Risks | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-06 | §6 M4A Readiness Note | QualityAssessment, MoatMechanism, IndustryAnalysis, ManagementLedger, CapitalAllocation schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-06 | Header Traceability | Constitution §1 · FD #130 · FD #95 · M2 CAP-003 · Evidence Doctrine CAP-017 | FD | FD #95, FD #130 | CAP-003, CAP-017 |

---

## 7. M3-07 — Dislocation, Impairment & Recovery Contract

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-07 | §1 Purpose | Central QAD question: temporary vs permanent impairment | Constitution | Constitution §1 | — |
| M3-07 | §2.1 What Broke? | 9 dislocation dimensions: Revenue, Volume, Price, Mix, Margin, Share, Churn, ROIC, Cash | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §2.2 Decomposition | Cyclical / Structural / One-time / Accounting components | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §2.3 Diagnostic Gates | 6 gates: Cause, Peer Test, Moat Test, Reversibility, Balance-Sheet Runway, External Evidence | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §3.1 Impairment States | TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED | Frozen Architecture | Architecture Design Gate — derived from Constitution §1 | — |
| M3-07 | §3.2 Mandatory Output | Primary Diagnosis + Strongest Competing + Why Dominates + Weakest Link + Flip Evidence | Frozen Architecture | Architecture Design Gate — flip evidence mandate | — |
| M3-07 | §3.3 Prohibited Reasoning | "Never use: historically great company, therefore will recover" | DNA | DNA-002 (Evidence First) | — |
| M3-07 | §3.3 Prohibited Reasoning | Allowed: causal reasoning based on demonstrated moat mechanisms | DNA | DNA-009 (Falsifiable Hypotheses) | — |
| M3-07 | §4.1 Recovery Model Structure | Cause, Mechanism, Leading Evidence, Expected Sequence, Time Horizon, Invalidation | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §4.2 Recovery Types | Cyclical, Operational Fix, Market Share, Balance-Sheet, Regulatory, Restructuring, None Identified | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §4.3 Recovery States | NOT_YET_EVIDENT / EARLY_SIGNS / CONFIRMING / STALLED / COMPLETED / NOT_APPLICABLE | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | §5 Thesis Killers | 7 killer types: Quality, Impairment, Valuation, Balance-Sheet, Management, Industry, Regulatory | Frozen Architecture | Architecture Design Gate — thesis killer tracking | — |
| M3-07 | §5 Thesis Killers | Tracked throughout case lifecycle; materialization triggers immediate re-evaluation | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-07 | §6 M4A Readiness Note | DislocationReconstruction, ImpairmentDiagnosis, RecoveryModel, ThesisKiller schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-07 | Header Traceability | Constitution §1 · FD #130 · M2 CAP-002 (ADAPT as input) | FD | FD #130 | CAP-002 |

---

## 8. M3-08 — Financial Reconstruction, Normalized Economics & Economic Underwriting

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-08 | §1 Purpose | 5 questions: earning power, normalized economics, permanent loss, price-implied expectations, valuation asymmetry | Frozen Architecture | Architecture Design Gate | CAP-009 |
| M3-08 | §1 Purpose | "Valuation is a diagnostic tool, not a decorative fair-value number" | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §2.1 Scope | 7–10+ years financial reconstruction; shorter history documented | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-08 | §2.2 Required Sections | Revenue Bridge, Margins, FCF, Working Capital, ROIC, Incremental ROIC, Leverage, Dilution, Per-Share, M&A, Capital Allocation | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-08 | §2.3 Calculation Lineage | Every calculation must have formula, inputs with fact IDs, intermediates, output | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-08 | §2.3 Calculation Lineage | "No black-box calculations" — independently reproducible | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-08 | §3.1 Normalized Economics | Estimate at "business as usual" under normal conditions — NOT a forecast | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §3.2 Normalized Estimation Method | Pre-dislocation run-rate, industry typical margins, company long-run averages, structural adjustments | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §3.3 Normalized Components | Revenue, Margin, FCF, ROIC, Growth — each with estimation method | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §4.1 Scenario Definitions | 5 scenarios: CURRENT / NO_RECOVERY / PARTIAL_RECOVERY / NORMALIZATION / QUALITY_COMPOUNDING | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §4.2 Scenario Requirements | Explicit traceable assumptions; falsifiable; no blends; most probable stated | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §5.1 Permanent Loss Analysis | Mandatory: loss if impairment is permanent; downside scenario range | Frozen Architecture | Architecture Design Gate — mandatory permanent loss | — |
| M3-08 | §5.2 Balance-Sheet Runway | Cash, credit, maturities, obligations, FCF burn, quarters of runway, dilution risk | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §5.3 Reverse DCF | Mandatory for every QAD case; implied growth/margin/ROIC from current price | Frozen Architecture | Architecture Design Gate — Reverse DCF mandatory | — |
| M3-08 | §5.4 Price-Implied Expectations | Per scenario: what does market believe vs your evidence | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §5.5 Economic Damage vs Price Damage | Separately estimate; asymmetry if Price Damage > Economic Damage | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §5.6 Valuation Asymmetry | Favorable / Unfavorable / Symmetric / Unclear — diagnostic only, not buy/sell | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §5.7 Scenario Ranges | Probability ranges (never single point); set of distinct outcomes, not weighted average | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | §6 Prohibited Outputs | No single fair value; no weighted average; no buy/sell/hold; no 12-month target | Frozen Architecture | Architecture Design Gate — prohibited outputs | — |
| M3-08 | §7 M4A Readiness Note | FinancialStatement, FinancialReconstruction, NormalizedEconomics, EconomicScenario, ReverseDCF, ValuationAsymmetry schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-08 | Header Traceability | Constitution §1 · FD #130 · M2 CAP-009 (CIW absorbed — CIW second-slice was valuation/underwriting prototype) | CIW Inherited | FD-CIW-001..016 | CAP-009 |

---

## 9. M3-09 — Challenge, Audit, Underwriting & Publication Contract

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-09 | §1 Purpose | 4 functions with independence and veto matrix | Constitution | Constitution §1/§10 (Dissent · False Confidence) | — |
| M3-09 | §1 Separation of Duties | Research ≠ Audit; Primary Thesis ≠ Red Team; Calculation ≠ Recalculation — non-negotiable | Constitution | Constitution §18 | — |
| M3-09 | §2.1 Red Team Mission | "Assume the QAD thesis is wrong and the market may be correct" | DNA | DNA-010 (Human Authority Preserves Dissent) | — |
| M3-09 | §2.2 Red Team Inputs | Full case state, Evidence Graph, Research Charter, H1–H5 | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | §2.3 Red Team Outputs | Strongest Structural Case, Quality-Challenge, Valuation-Challenge, Threat Assessment, Counter-Evidence, Unresolved Risks | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | §2.4 Red Team Rules | **No veto**; outputs preserved even if rejected; structurally separate; no access to modify evidence | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | §2.5 Challenge Outcomes | ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE / UNRESOLVED | Frozen Architecture | Architecture Design Gate — explicit outcomes | — |
| M3-09 | §3.1 Auditor Mission | Verify process integrity, not conclusions | CIW Inherited | FD-CIW-001..016 | CAP-016 |
| M3-09 | §3.1 Auditor Checks | Source existence, original-source inspection, citation correctness, PIT integrity, calculation reproducibility, contradiction preservation, model provenance, self-review separation, publication gates | M2 Capability | CAP-016 (REUSE) | CAP-016 |
| M3-09 | §3.2 Auditor Authority | **May block FOUNDER_READY**; reports directly to Founder | Constitution | Constitution §18 — auditor independence | — |
| M3-09 | §3.3 Audit Outcomes | PASS / PASS_WITH_MINORS / FINDINGS_REQUIRED / BLOCKED | CIW Inherited | FD-CIW-001..016 | CAP-016 |
| M3-09 | §3.4 Re-Audit | Mandatory after FINDINGS_REQUIRED or BLOCKED | CIW Inherited | FD-CIW-001..016 | CAP-016 |
| M3-09 | §4.1 Underwriter Mission | Synthesize all work into final verdict — highest AI-judgment function | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | §4.2 Underwriter Inputs | Quality, Industry, Financial, Management, Impairment, Recovery, Valuation, Red Team, Audit | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | §4.3 Final Research Verdict States | QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED / NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION | Frozen Architecture | Architecture Design Gate — verdict states | — |
| M3-09 | §4.4 Underwriter Prohibitions | Cannot choose own cases, allocate capital, size positions, execute trades, create FOUNDER_ENDORSED | Constitution | Constitution §18 | — |
| M3-09 | §5.1 Publication States | RESEARCH_COMPLETE / FOUNDER_READY | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-09 | §5.2 FOUNDER_READY vs FOUNDER_ENDORSED | System creates FOUNDER_READY; only Founder creates FOUNDER_ENDORSED | Constitution | Constitution §18 — Founder authority | — |
| M3-09 | §5.3 Publication Outputs | Thai Long-Form Report, Companion Dissent Report, Structured Case State | CIW Inherited | FD-CIW-001..016; CAP-014 | CAP-014 |
| M3-09 | §5.4 Publication Rules | PDF/HTML = presentation, not truth; Editor does not change analytical content | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-09 | §6 Separation of Duties Matrix | 10 separation pairs with rationale | Constitution | Constitution §18 — separation of duties | — |
| M3-09 | §7 M4A Readiness Note | RedTeamAssessment, AuditReport, UnderwritingVerdict, PublicationState schemas | Frozen Architecture | Architecture Design Gate | — |
| M3-09 | Header Traceability | Constitution §1/§10 · DNA-010/002 · FD #130 · M2 CAP-009/-016 | CIW Inherited | FD-CIW-001..016 | CAP-009, 016 |

---

## 10. M3-10 — Monitoring, Knowledge & Evaluation Contract

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-10 | §1 Purpose | 3 functions: Monitoring, Knowledge Compounding, Evaluation | CIW Inherited | FD-CIW-001..016; FD #130 | CAP-009 |
| M3-10 | §2.1 Monitoring States | RECOVERY_CONFIRMING / ON_TRACK / UNCERTAIN / WEAKENING / BROKEN | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-10 | §2.2 Monitoring Model | Thesis-specific indicators (1–3 key indicators with thresholds, cadence, escalation) | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-10 | §2.3 Event-Driven Monitoring | New filings, earnings, management changes, regulatory actions, competitor developments | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-10 | §2.4 Monitoring Outputs | State update, trigger alert, quarterly digest | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-10 | §2.5 Monitoring Authority | Non-authoritative; cannot close thesis or reverse FOUNDER_ENDORSED | Constitution | Constitution §18 — Founder authority | — |
| M3-10 | §3.1 Knowledge Lifecycle | Research Finding → Candidate Lesson → Cross-Case Validation → Independent Review → APPROVED KNOWLEDGE → Industry Playbook | DNA | DNA-011 (Learning Never Rewrites History) | — |
| M3-10 | §3.1 Knowledge Rule | "Single case does not automatically become institutional knowledge" | DNA | DNA-012 (Controlled Learning) | — |
| M3-10 | §3.2 Knowledge Stages | 6 stages with gates (Research Director → Independent Review → Founder/CU approval) | DNA | DNA-012 (Controlled Learning) | — |
| M3-10 | §3.3 Knowledge Types | Industry Pattern, Moat Pattern, Management Pattern, Impairment Pattern, Valuation Pattern, Methodology Improvement | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-10 | §3.4 Knowledge Repository | Industry Playbooks, Pattern Library, Methodology Reference — NOT inline prompts or SOUL.md | DNA | DNA-012 (Controlled Learning) | — |
| M3-10 | §4.1 Two Failure Types | Type A (Research Quality) and Type B (Discovery Recall) | Discovery Requirement | Discovery Req. v0.1 — Part E (M1 correction closeout) | — |
| M3-10 | §4.2 Evaluation Metrics | 17 metrics covering Type A and Type B | Discovery Requirement | Discovery Req. v0.1 — Part E/F | — |
| M3-10 | §4.3 Decision-Changing Evidence Recall (DCER) | Periodic process: post-case evidence → would it change thesis? | Discovery Requirement | Discovery Req. v0.1 — Part E | — |
| M3-10 | §4.4 Decision-Changing Candidate Recall (DCCR) | Rejected Sample Audit → missed candidates → root cause | Discovery Requirement | Discovery Req. v0.1 — Part E | — |
| M3-10 | §4.5 Rejected Sample Audit | Monthly stratified/random 50–100 sample | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-10 | §4.6 Evaluation Cadence | Continuous / Per-case / Monthly / Quarterly / Semi-Annual | Discovery Requirement | Discovery Req. v0.1 | — |
| M3-10 | §4.7 Threshold Calibration | Deferred to M4B — M3 does not set quantitative pass thresholds | FD | FD #130 — M3/M4B boundary | — |
| M3-10 | §5 M2 Capability Consumption | CAP-009 ABSORB, CAP-012 REUSE, CAP-014 REUSE, CAP-015 REUSE, CAP-016 REUSE | M2 Capability | M2 Capability Registry | CAP-009, 012, 014, 015, 016 |
| M3-10 | §6 M4A/M4B Readiness Note | MonitoringState, KnowledgeSchema, EvaluationMetric schemas for M4A; metric definitions for M4B | Frozen Architecture | Architecture Design Gate | — |
| M3-10 | Header Traceability | Constitution §10 · DNA-011/012 · FD #130 · M2 CAP-009 | FD | FD #130 | CAP-009 |

---

## 11. M3-LOGICAL — Logical Organization & Role Classification

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-LOGICAL | §1 Principles (1) | Logical components are NOT Hermes profiles | Frozen Architecture | Architecture Design Gate — ROLE vs SERVICE distinction | CAP-018 |
| M3-LOGICAL | §1 Principles (2) | Separation of duties overrides convenience | Constitution | Constitution §18 | — |
| M3-LOGICAL | §1 Principles (3) | Not every box needs an AI agent (deterministic/policy/infrastructure) | Frozen Architecture | Architecture Design Gate | — |
| M3-LOGICAL | §1 Principles (4) | Elastic investigators are ephemeral | NEW_M3_DERIVATION | M3 — elastic investigator pattern from M3-05 | — |
| M3-LOGICAL | §2 Logical Organization Diagram | 29 logical components under Founder | Frozen Architecture | Architecture Design Gate — target logical organization tree | CAP-018 |
| M3-LOGICAL | §3.1 Discovery & Coverage | 5 components: Quality Discovery, Dislocation Radar, Discovery Scout, Candidate Builder, Selection Engine | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-LOGICAL | §3.2 Research Institution | 8 components: Research Director, Evidence Intelligence, Core Desk Researcher, Business/Industry, Financial/Management, Impairment, Valuation, Elastic Investigator | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-LOGICAL | §3.3 Independent Assurance | Structural Red Team, Independent Auditor | Frozen Architecture | Architecture Design Gate | — |
| M3-LOGICAL | §3.4 Underwriting & Publication | Chief Underwriter, Thai Editor | Frozen Architecture | Architecture Design Gate | — |
| M3-LOGICAL | §3.5 Post-Publication | Thesis Monitor, Knowledge Steward | Frozen Architecture | Architecture Design Gate | — |
| M3-LOGICAL | §3.6 Horizontal Services | 10 services: Budget Controller, Evidence Registry, Source Archive, PIT Infra, Run Manifest, NotebookLM Interface, Publication Infra, Evaluation Lab, Entity Resolution, Case Locking | Frozen Architecture | Architecture Design Gate | — |
| M3-LOGICAL | §4 Classification Summary | 7 types across 29 components | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-LOGICAL | §5 Separation of Duties Matrix | 12 separation/pairing rules | Constitution | Constitution §18 | — |
| M3-LOGICAL | §6 M3 Non-Negotiable | No profile changes during M3 | FD | FD #130 — M3 scope | — |
| M3-LOGICAL | §6 M3 Non-Negotiable | Current org-* profiles remain operational; Radar Scout TRANSITIONAL | FD | FD #130 | CAP-018 |
| M3-LOGICAL | Header Traceability | Constitution §1/§2/§18 · FD #130 · Frozen Architecture · M2 CAP-018 | Frozen Architecture | Architecture Design Gate | CAP-018 |

---

## 12. M3-ROLES — Production Role Contracts

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-ROLES | Role 1: Research Director | Orchestrate full case: Charter to Underwriting-ready | Frozen Architecture | Architecture Design Gate — 14 logical roles | — |
| M3-ROLES | Role 1: Authority/Forbidden | Cannot select own cases; cannot override Auditor | Constitution | Constitution §18 | — |
| M3-ROLES | Role 2: Evidence Intelligence Lead | Gatekeep evidence admission | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Role 2: Separation | Evidence Discovery ≠ Canonical Admission | Constitution | Constitution §18 | — |
| M3-ROLES | Role 3: Core Desk Researcher | Execute deep research from evidence gaps | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-ROLES | Role 4: Business & Industry Analyst | Assess business quality and industry economics | Frozen Architecture | Architecture Design Gate | CAP-003 |
| M3-ROLES | Role 5: Financial & Management Analyst | Financial reconstruction; management assessment | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-ROLES | Role 5: Separation | Calculation Production ≠ Independent Recalculation | Constitution | Constitution §18 | — |
| M3-ROLES | Role 6: Impairment Diagnosis Specialist | Diagnose impairment nature and permanence | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Role 6: Forbidden | Cannot use "historically great company, therefore will recover" | DNA | DNA-002 | — |
| M3-ROLES | Role 7: Valuation & Expectations Specialist | Normalized economics, Reverse DCF, scenario analysis | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Role 7: Forbidden | Cannot produce single fair value; cannot issue buy/sell/hold | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Role 8: Chief Underwriter | Final verdict synthesizing all work | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Role 8: Forbidden | Cannot select own cases; cannot allocate capital | Constitution | Constitution §18 | — |
| M3-ROLES | Role 9: Structural Red Team | Assume thesis wrong; strongest opposing case | DNA | DNA-010 (Human Authority Preserves Dissent) | — |
| M3-ROLES | Role 9: Authority | No veto; cannot block case | Constitution | Constitution §10 (Dissent) | — |
| M3-ROLES | Role 10: Independent Auditor | Verify process integrity | M2 Capability | CAP-016 (REUSE) | CAP-016 |
| M3-ROLES | Role 10: Authority | May block FOUNDER_READY | Constitution | Constitution §18 | — |
| M3-ROLES | Role 11: Thai Editor | Transform verdict into Thai report | M2 Capability | CAP-014 (Thai Editorial Standard) | CAP-014 |
| M3-ROLES | Role 11: Forbidden | Cannot change analytical content | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-ROLES | Role 12: Thesis/Knowledge Steward | Monitor theses; manage knowledge lifecycle | CIW Inherited | FD-CIW-001..016 | CAP-009 |
| M3-ROLES | Role 12: Authority | Cannot close endorsed thesis (Founder only) | Constitution | Constitution §18 | — |
| M3-ROLES | Role 13: Discovery Scout (TRANSITIONAL) | Surface external anomalies | Frozen Architecture | Architecture Design Gate | CAP-011 |
| M3-ROLES | Role 13: Separation | Discovery ≠ Selection; Discovery ≠ Underwriting | Constitution | Constitution §18 | — |
| M3-ROLES | Role 14: Elastic Investigator | Bounded, lawful scuttlebutt investigations | NEW_M3_DERIVATION | M3 — formal elastic investigator from M3-05 | — |
| M3-ROLES | Role Combination Matrix | 14 role pairs with can-combine rules | Constitution | Constitution §18 — separation of duties | — |
| M3-ROLES | Profile Count Estimate | 6–9 Hermes profiles for 14 logical roles | Frozen Architecture | Architecture Design Gate | — |
| M3-ROLES | Header Traceability | Frozen Architecture · M2 CAP-018 | Frozen Architecture | Architecture Design Gate | CAP-018 |

---

## 13. M3-SERVICES — System Service Contracts

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-SERVICES | Service 1: Selection Engine | POLICY-GOVERNED; FAIL_OPEN failure behavior; 3 retries | Frozen Architecture | Architecture Design Gate — horizontal services | — |
| M3-SERVICES | Service 1: Forbidden | Must NOT use AI judgment; must NOT apply unpublished rules | Frozen Architecture | Architecture Design Gate | — |
| M3-SERVICES | Service 2: Research Budget Controller | POLICY-GOVERNED; FAIL_CLOSED | Frozen Architecture | Architecture Design Gate | — |
| M3-SERVICES | Service 3: Entity Resolution | DETERMINISTIC; CIK-based identity | M2 Capability | CAP-001 (REUSE) | CAP-001 |
| M3-SERVICES | Service 4: Evidence Registry | INFRASTRUCTURE; append-only; FAIL_CLOSED | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-SERVICES | Service 5: Raw Source Archive | INFRASTRUCTURE; append-only; content hashes | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-SERVICES | Service 6: Run Manifest Service | INFRASTRUCTURE; FAIL_CLOSED; full manifest per M3-01 §9 | Frozen Architecture | Architecture Design Gate — Run Manifest | — |
| M3-SERVICES | Service 7: PIT Lock Service | INFRASTRUCTURE; FAIL_OPEN with warning flag | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-SERVICES | Service 8: Budget/Retry Controller | INFRASTRUCTURE; FAIL_OPEN; must NOT weaken quality gates | Frozen Architecture | Architecture Design Gate — bounded retries | — |
| M3-SERVICES | Service 9: Case Locking/Idempotency | INFRASTRUCTURE; FAIL_CLOSED; dedup enforcement | NEW_M3_DERIVATION | M3 — derived from M3-01 §8.4/§8.5 | — |
| M3-SERVICES | Service 10: NotebookLM Interface | INTERFACE; FAIL_OPEN; output NONCANONICAL | Frozen Architecture | Architecture Design Gate — abstract provider | — |
| M3-SERVICES | Service 11: Publication Renderer | INFRASTRUCTURE; FAIL_RETRY; must NOT change content | Evidence Doctrine | Evidence Doctrine (CAP-017) | CAP-017 |
| M3-SERVICES | Service 12: Evaluation Harness | INFRASTRUCTURE; FAIL_REPORT; must NOT suppress metrics | Frozen Architecture | Architecture Design Gate — evaluation | — |
| M3-SERVICES | Service 13: Quality/Dislocation Sensors | DETERMINISTIC; FAIL_INDIVIDUAL; must NOT use AI judgment | Frozen Architecture | Architecture Design Gate | CAP-001, 002 |
| M3-SERVICES | Service Dependency Map | Dependency flow diagram | Frozen Architecture | Architecture Design Gate | — |
| M3-SERVICES | Header Traceability | Frozen Architecture · M3-01 §8/§9 | Frozen Architecture | Architecture Design Gate | — |

---

## 14. M3-MIGRATION — Workforce Migration Map

| Contract | Section | Clause/Rule | Source Type | Source Reference | M2 Capability |
|---|---|---|---|---|---|
| M3-MIGRATION | §1 Design Principles | No profiles changed during M3 | FD | FD #130 — M3 scope | — |
| M3-MIGRATION | §1 Design Principles | Target = logical organization; not every box a separate profile | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-MIGRATION | §1 Design Principles | Separation of duties overrides convenience | Constitution | Constitution §18 | — |
| M3-MIGRATION | §1 Design Principles | Transitional roles remain until explicitly replaced | FD | FD #130 | CAP-018 |
| M3-MIGRATION | §2 Current Profile Inventory | 21 profiles (iip, org-*, ipm) | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-MIGRATION | §3.1 Direct Assignment | org-cro → Structural Red Team (HIGH compatibility) | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-MIGRATION | §3.1 Direct Assignment | org-auditor → Independent Auditor (HIGH compatibility) | Frozen Architecture | Architecture Design Gate | CAP-016 |
| M3-MIGRATION | §3.1 Direct Assignment | org-radar-scout → Discovery Scout (TRANSITIONAL) | Frozen Architecture | Architecture Design Gate | CAP-011 |
| M3-MIGRATION | §3.2 Merge Candidates | Desk Analyst (Core + Business + Financial) — compatible | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §3.2 Merge Candidates | Impairment & Valuation Analyst — compatible | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §3.2 Merge Candidates | Editor & Monitor — compatible post-publication functions | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §3.2 Merge Candidates | Discovery Operator — deterministic/policy services | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §3.2 Merge Candidates | Selection Operator — policy-governed services | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §3.3 Must-Remain-Separate | Research Director ≠ Auditor/Red Team; Evidence ≠ own evidence; Underwriter ≠ any | Constitution | Constitution §18 | — |
| M3-MIGRATION | §3.4 New Profiles Required | Research Director, Evidence Intelligence Lead, Chief Underwriter, Elastic Investigator (ephemeral) | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §4.1 Keep-As-Is | org-radar-scout (TRANSITIONAL), org-auditor, ipm | FD | FD #130 | CAP-011 |
| M3-MIGRATION | §4.2 Reframe (Later) | org-cro → Structural Red Team; org-cos/org-ic-secretary → Research Director; org-data-steward → Evidence Intelligence | Frozen Architecture | Architecture Design Gate | CAP-018 |
| M3-MIGRATION | §4.3 Merge (Later) | org-equity/commodity/macro-analyst → QAD Desk Analyst | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §4.4 Retire (Later) | org-quant-validator → after Evaluation Harness proven; org-* assistants after stabilization | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §4.5 Create New (Later) | Research Director, Chief Underwriter, Evidence Intelligence Lead (post-M3 approval) | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §5 Migration Sequence | Phase A (Contract Alignment), Phase B (New Profiles), Phase C (Merge), Phase D (Retirement) | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §6 Risk Table | 4 risks: reduced parallelism, subtle conflict, legacy thinking, redundancy | Frozen Architecture | Architecture Design Gate | — |
| M3-MIGRATION | §7 Non-Negotiable | No migration executed in M3 — design artifact only | FD | FD #130 | — |
| M3-MIGRATION | Header Traceability | Frozen Architecture · M2 CAP-018 | Frozen Architecture | Architecture Design Gate | CAP-018 |

---

## Appendix A: NEW_M3_DERIVATION Items

This appendix lists every clause/rule traced as `NEW_M3_DERIVATION` with explanation of why M3 created it rather than inheriting from an existing source.

| # | Contract | Section | NEW_M3_DERIVATION Item | Why Necessary |
|---|---|---|---|---|
| 1 | M3-01 | §8.4 Case Locking | Per-case locking with timeout → INCOMPLETE release | Frozen architecture required concurrent write protection at the concurrency level, but CIW had no formal case-locking mechanism. M3 derived the specific lock/timeout/release pattern from the general concurrency requirement. |
| 2 | M3-01 | §8.5 Deduplication | Dedup for cases, evidence, and signals | Frozen architecture mandated data integrity; CIW had ad-hoc dedup. M3 formalized three distinct dedup rules (case re-creation, evidence re-ingestion, signal re-entry) as a derivation from the integrity requirement. |
| 3 | M3-03 | §3.3 Evidence Gap Map classification | Gap classification: RESOLVABLE_WITH_EXISTING_SOURCES / RESOLVABLE_WITH_SCUTTLEBUNT / CURRENTLY_UNRESOLVABLE | CIW had a flat evidence-gap list with no classification. The frozen architecture required scuttlebutt to be spawned from evidence gaps (M3-05 trigger). M3 derived the three-class taxonomy to make scuttlebutt spawning deterministic. |
| 4 | M3-05 | §1 Purpose (entire contract) | Modern Scuttlebutt Protocol as formal elastic investigator network | CIW had only ad-hoc scuttlebutt via Deep Research (no structured protocol). The frozen architecture required *"Scuttlebutt as a formal elastic investigator network with explicit contracts"*. M3 created the entire protocol from this directive. |
| 5 | M3-05 | §2.1 Investigator Types | 11-type investigator taxonomy | No prior taxonomy existed. Derived from the frozen architecture's requirement for *"elastic investigator network"* — M3 decomposed the generic investigator concept into specific, bounded domains. |
| 6 | M3-05 | §2.2 Classification | ELASTIC_INVESTIGATOR as ephemeral, purpose-built classification | Frozen architecture distinguished role types but did not define the elastic investigator pattern. M3 derived this classification to match the ephemeral/purpose-built/contract-bounded nature of scuttlebutt investigations. |
| 7 | M3-05 | §3 Investigation Contract | Formal investigation contract template (12 fields) | No prior template existed. Derived from the frozen architecture requirement that each investigation have a *"bounded scope, falsifiable question, stop rules, and budget"*. |
| 8 | M3-05 | §3.1 Falsifiable Question | Must be falsifiable; good/bad examples | Derived from DNA-009 (Falsifiable Hypotheses) extended to the investigation context. No prior scuttlebutt-specific falsifiability rule existed. |
| 9 | M3-05 | §3.2 Independence Requirement | Independence from target AND from research team | CIW had no investigator-independence rule. Derived from the frozen architecture's separation-of-duties mandate applied to the investigator function. |
| 10 | M3-05 | §3.3 Stop Rules | 5 stop rules: saturation, budget, time, answered, exhausted | No prior stop-rule framework existed. Derived from the frozen architecture requirement for bounded investigation with defined termination. |
| 11 | M3-05 | §5.1 Investigation Output | Structured output: Evidence IDs + Investigation Report + Source List | No prior output format existed. Derived from the need to integrate scuttlebutt findings into the canonical evidence pipeline (M3-04). |
| 12 | M3-05 | §6 EIV Framework | Expected Information Value classification (HIGH/MEDIUM/LOW/DE_MINIMIS) | No prior budget-prioritization framework for investigations existed. Derived from the frozen architecture's budget-control requirement applied to elastic investigations. |
| 13 | M3-LOGICAL | §1 Principle (4) | "Elastic investigators are ephemeral — spawned on demand, retired when done" | Derived from M3-05's elastic investigator pattern. Not present in frozen architecture directly — M3 derived this operational principle from the investigator design. |
| 14 | M3-ROLES | Role 14: Elastic Investigator | Full role contract for elastic investigator | New role created for M3-05's investigator pattern. Frozen architecture specified 14 logical roles but the Elastic Investigator contract details were left to M3 to derive from the Scuttlebutt Protocol. |
| 15 | M3-SERVICES | Service 9: Case Locking/Idempotency | Case locking service with dedup enforcement | New infrastructure service derived from M3-01 §8.4/§8.5. Frozen architecture specified concurrency requirements but not the specific service. M3 derived this as a dedicated infrastructure service. |

### Summary of NEW_M3_DERIVATION

| Metric | Count |
|--------|-------|
| Total NEW_M3_DERIVATION items | 15 |
| Contracts affected | M3-01, M3-03, M3-05, M3-LOGICAL, M3-ROLES, M3-SERVICES |
| Contracts with zero NEW_M3_DERIVATION | M3-02, M3-04, M3-06, M3-07, M3-08, M3-09, M3-10, M3-MIGRATION |
| Heavy cluster | M3-05 (Modern Scuttlebutt Protocol) — 9 of 15 items |

**Observation:** The heavy concentration in M3-05 reflects that the CIW pilot had no formal scuttlebutt protocol — this was an acknowledged gap that M3 resolved by deriving a complete elastic investigator framework from first principles. All other contracts trace directly to frozen architecture, Constitution, DNA, FD, CIW, or Evidence Doctrine sources without requiring new derivation.

---

*End of QAD-M3 Traceability Matrix. Generated 2026-08-19 from 10 domain contracts + 4 design artifacts.*