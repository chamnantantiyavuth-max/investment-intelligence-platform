# QAD Modern Scuttlebutt Protocol

> **Contract:** M3-05 (M3 Domain Contract Set)
> **Status:** M3 REVIEWED — AWAITING FOUNDER CLOSEOUT
> **Authority:** FD #130; Frozen Architecture (Elastic Investigator Pattern); Constitution §2 (§17 technology-neutral)
> **Traceability:** FD #130 · ARCHITECTURE-DESIGN-GATE-FINAL.md · CONSTITUTION-§2 · NEW_M3_DERIVATION (investigator charter, evidence gap contract, lawful-investigation safeguards, Expected Information Value)

---

## 1. Purpose

Define the elastic investigator network for QAD research — specialized, on-demand investigations deployed from specific evidence gaps, operating under bounded charters, and returning structured evidence to the Canonical Evidence Registry.

Scuttlebutt is NOT desk research. It is primary intelligence gathering from the company's ecosystem: customers, competitors, suppliers, distributors, employees, regulators, technology, science, channels, and geography.

---

## 2. Investigator Type Registry

| Investigator | Domain | Typical Evidence Gaps |
|-------------|--------|----------------------|
| Customer / Product Investigator | End-user experience, product utility, switching costs, satisfaction, churn drivers | "Is the product truly differentiated?" "Do customers have alternatives?" |
| Competitor Investigator | Competitor strategy, market share dynamics, competitive responses | "Are competitors taking share?" "Is the moat under attack?" |
| Supplier Investigator | Input cost trends, supply constraints, supplier relationships | "Are input costs rising unsustainably?" "Is supply chain fragile?" |
| Distributor / Channel Investigator | Channel health, inventory, sell-through, distribution dynamics | "Are distributors destocking?" "Is channel inventory normal?" |
| Employee / Organization Investigator | Talent, culture, execution capability, organizational health | "Is talent leaving?" "Is organizational complexity hurting execution?" |
| Digital / Social Investigator | Web traffic, app rankings, social sentiment, digital footprint | "Is digital engagement consistent with reported revenue?" |
| Regulatory Investigator | Regulatory risk, pending decisions, policy trends | "Is regulatory risk mispriced?" "Are there hidden liabilities?" |
| Technology / IP Investigator | Patent strength, R&D pipeline, innovation trajectory | "Is the technology moat real?" "Are competitors catching up?" |
| Scientific / Clinical Investigator | Clinical trial data, scientific validation, technical feasibility | "Is the science sound?" "What are risks of failure?" |
| Geographic Investigator | Regional dynamics, local competition, regulatory variation | "Is the geographic thesis playing out?" |
| Industry Specialist | Deep industry expertise, cross-company patterns, structural trends | Industry-specific questions beyond generalist capability |

---

## 3. Investigation Charter (Every Investigation)

An investigation may only begin when it has a complete charter. No open-ended research.

| Field | Description |
|-------|-------------|
| **Evidence Gap ID** | Links to the specific unresolved question in the Evidence Gap Map |
| **Falsifiable Question** | What would FALSIFY or CONFIRM the hypothesis? Must be specific |
| **Allowed Source Classes** | L1–L10 levels permitted for this investigation |
| **Population Represented** | Whom/what does the evidence represent? |
| **Sampling Limitations** | What biases or limitations exist? |
| **Time Window** | What period does the evidence cover? |
| **Geography** | What geographic scope? |
| **Independence** | Any conflicts or dependencies? |
| **Stop Rule** | When does investigation stop? (evidence sufficient / budget exhausted / counter-evidence found) |
| **Output Evidence IDs** | What evidence objects will be produced? |
| **Budget** | Maximum cost/token/retrieval allowance |
| **Expected Information Value** | Qualitative estimate of value vs cost (PLAUSIBLE_HIGH / PLAUSIBLE_MEDIUM / PLAUSIBLE_LOW) |

---

## 4. Investigation Protocol

### Initiation
1. Evidence Gap Map identifies an unresolved question requiring primary ecosystem evidence
2. Research Director selects investigator type and drafts charter
3. Research Budget Controller approves budget and charter
4. Investigator deployed

### Execution
1. Investigator gathers evidence from allowed sources only
2. All evidence is tagged with source type (L1-L10), retrieval method, and retrieval timestamp
3. Investigator documents sampling method, limitations, and any bias or conflict
4. If the falsifiable question is answered or the stop rule fires → investigation ends
5. If new, related questions emerge → they are documented as new evidence gaps (separate charter required)

### Return
1. Investigation report produced containing:
   - Original Evidence Gap ID and falsifiable question
   - Summary of evidence gathered
   - Sources used (with pointers)
   - Sampling limitations and biases
   - ANSWERED / NOT_ANSWERED / PARTIALLY_ANSWERED disposition
   - New evidence IDs proposed for canonical admission
2. Report enters Canonical Evidence Registry (Layer 2)
3. Case Evidence Gap Map updated

---

## 5. Lawful, Public, Non-MNPI (Mandatory)

All scuttlebutt investigations must be:

1. **Lawful** — all information gathered through lawful means
2. **Public** — sources available without deception or misrepresentation
3. **Non-MNPI** — no solicitation or acceptance of material non-public information

### Rules

| Permitted | Forbidden |
|-----------|-----------|
| Public company filings and investor materials | ✅ Non-public internal company documents | ❌ |
| Public customer reviews and ratings | ✅ Confidential customer data | ❌ |
| Public competitor pricing and positioning | ✅ Price-fixing or collusion | ❌ |
| Public supplier/vendor lists | ✅ Confidential supplier contracts | ❌ |
| Government data and filings | ✅ Non-public regulatory information | ❌ |
| Public employee data (LinkedIn, Glassdoor) | ✅ Confidential personnel records | ❌ |
| Public patent and scientific literature | ✅ Pre-publication research data | ❌ |
| Public channel checks (store visits, product tests) | ✅ Deceptive pretexting | ❌ |
| Industry expert interviews (lawful, disclosed) | ✅ # Solicitation of confidential information | ❌ |
| Public satellite/imagery data | ✅ Non-public surveillance | ❌ |

**No deceptive pretexting.** No solicitation of confidential information.

---

## 6. Research Budget Controller Authority

- **Research Director** may propose and justify expansion using Expected Information Value
- **Research Budget Controller** applies approved policy — does not second-guess the investigator's domain judgment
- **Research Director does not self-authorize unlimited investigation**
- Budget exhaustion → investigation marked `INCOMPLETE_BUDGET`, not published as complete
- Budget override → Founder only

### Expected Information Value (EIV) Framework

EIV is a qualitative assessment, not a quantified metric:

| EIV | Meaning | Budget Priority |
|-----|---------|----------------|
| **PLAUSIBLE_HIGH** | Evidence likely to resolve a critical question that changes case outcome | High |
| **PLAUSIBLE_MEDIUM** | Evidence likely to add useful context but unlikely to change outcome | Medium |
| **PLAUSIBLE_LOW** | Evidence would be nice to have but not material to the thesis | Low (may be deferred) |

---

## 7. Investigator Deployment

- Investigators are **elastic** — deployed per-charter, not standing agents
- One investigator may handle multiple charters (same type) in sequence
- Multiple investigators may run in parallel for different evidence gaps
- Each charter is independent — no cross-charter dependencies
- Charter-level costs are tracked against the case budget

### Classification

- **Scuttlebutt Investigator = ELASTIC_INVESTIGATOR** (role classification per M3-01 §Role vs Service)
- Not a permanent Hermes profile (logically defined; may map to elastic subagents at runtime)

---

## 8. Quality Gate

Before scuttlebutt evidence enters canonical truth:

1. Source existence verified
2. Likelihood of independence assessed
3. Sampling method documented
4. Time window and geography confirmed
5. L10 evidence flagged (cannot support material conclusion alone)
6. Stop rule compliance verified

Evidence that passes quality gate → **admitted to Canonical Evidence Registry** with full provenance.

Evidence that fails quality gate → **quarantined** with reason, may be re-admitted if remediated.

<!-- 2026-08-19 12:30 UTC+7 -->