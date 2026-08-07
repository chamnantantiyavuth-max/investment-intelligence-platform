# Internal Audit Note — RM-2026-0003 (JNJ Talc-Litigation Resolution)

**Audit role:** Internal Auditor / Red Team (`org-auditor`)  
**Audit date:** 2026-08-07, point-in-time through 17:48 UTC+7  
**Artifact under audit:** `analyst-note.md`, with packet/process records, CRO companion, raw primary sources, and the two review-stage report candidates inspected  
**Verdict:** **REMAINS BLOCKED**

## Basis for verdict

The packet's central sourced amounts are genuine, the required arithmetic re-performs, the Data Steward's seven stated corrections are present in the actual evidence log and analyst note, the 27 July press-release / 28 July filing chronology is corrected, and the 4 August 8-K is correctly treated as an officer-change filing rather than a notes offering. The CRO companion is a coherent standalone opposing thesis, not a risk list. Advisory-only, portfolio-blind, mandate-scope, and point-in-time controls are otherwise respected.

Clearance is nevertheless blocked by four MAJOR defects: impossible anti-anchoring provenance timestamps, residual cross-examination overstatement in controlling body language, non-operational change conditions left after a SUSTAINED finding, and repeated claim-site citation/formula omissions that have propagated into the review-stage report. Two MINOR defects also require correction.

No CRITICAL finding was identified.

## Arithmetic re-performance

| Check | Independent calculation | Result |
|---|---:|---|
| Commitment vs Q2 reserve | `$5.5B - $3.7B = $1.8B` | **PASS** — unlike bases; not a measured shortfall |
| Transaction EPS components | `$0.46 + $0.18 = $0.64` | **PASS** |
| Guidance midpoint cut | `$11.68 - $11.04 = $0.64` | **PASS** |
| H1-2026 buyback monthly pace | `$4,253M / 6 = $708.833M/month` | **PASS** |
| FY2025 buyback monthly pace | `$5,953M / 12 = $496.083M/month` | **PASS** |
| Buyback run-rate increase | `(($4,253M/6) / ($5,953M/12)) - 1 = 0.4288594 = 42.8859%`, rounded `42.89%` / `~43%` | **PASS** — arithmetic only, not guidance |
| Maximum holdouts at exactly 95% participation | `76,000 × 5% = 3,800` | **PASS** — conditional maximum, not an observed count |
| Simple reserve bridge | `$11.6B - $7.0B = $4.6B`; `$4.6B - $3.4B = $1.2B` | **PASS arithmetic / attribution UNVERIFIED** |
| Cash and securities | `$20,422M + $336M = $20,758M` | **PASS** |
| Total debt | `$11,692M + $37,344M = $49,036M` | **PASS** |

Primary-source reinspection confirmed the talc exhibit's 27 July 2026 date, $5.5B commitment, at-least-95% condition, first payment of no more than $3B in 2027, and no additional payments before 2028. It also confirmed that the 4 August cover page labels the note classes as securities registered under Section 12(b) and contains operative Items 5.02 and 9.01 only. No central transaction, reserve, guidance, liquidity, or repurchase amount was found to be fabricated.

## Numbered findings

### 1. **MAJOR — Anti-anchoring dispatch provenance is chronologically impossible and the per-task allowlist evidence is not durable**

**Evidence**

- `first-pass-dispatch.md:7`: **“Job: delegate_task batch (3 tasks), dispatched 2026-08-07 ~18:55 UTC+7”**.
- `first-pass-dispatch.md:29-31`: **“completed … ~18:40”**, **“~18:35”**, and **“~18:44 UTC+7”** — all before the claimed 18:55 dispatch.
- `first-pass-dispatch.md:33`: **“Batch result (returned 2026-08-07 ~19:05 UTC+7)”**.
- The repository independently contradicts those times: commit `0c9ad54` at **17:32:22 UTC+7** already contained the claimed future 18:55 dispatch time; commit `594025a` at **17:39:55 UTC+7** already contained the claimed 18:35–18:44 completion times and 19:05 return time. The current file mtime was 17:39:54 UTC+7, and the live clock during audit was 17:48:28 UTC+7.
- `first-pass-dispatch.md:15` states only a generic rule: **“the shared packet ONLY + its own role brief + its own primary-source re-check instructions”**. The exact three role briefs/prompts, exact file-by-file allowlists per task, and prompt hashes/full retained prompts are not persisted. The task table gives lenses, not a durable per-task input record.

**Impact**

The outputs may in fact have been isolated, but the record cannot prove it. The retained chronology is impossible, and a generic self-attestation does not establish what each task actually received. This violates the required reproducible lineage and correction doctrine controls.

**Exact correction needed**

1. Preserve the erroneous record and append a clearly labeled §23.9 correction block; do not silently replace the existing timestamps.
2. Recover the actual dispatch, per-task completion, and batch-return timestamps from the delegation runtime/log. If the times cannot be recovered, state **UNRECOVERABLE / NOT VERIFIED** and use git times only as independently established upper bounds, not invented substitutes.
3. Persist for each of tasks 1–3: delegation/job ID, provider/model/reasoning setting, exact role brief or its hash, exact input-file allowlist, explicit exclusion of sibling outputs, dispatch/completion time, and output artifact/hash.
4. Explain the timezone/source that produced the false future timestamps.

**Re-audit boundary**

Re-audit only the corrected `first-pass-dispatch.md`, underlying delegation/log evidence, git metadata, and the three first-pass artifact hashes/input allowlists. Do not reopen analyst arithmetic or primary-source checks unless those artifacts are modified.

---

### 2. **MAJOR — SUSTAINED/PARTIAL cross-examination corrections are not fully applied to controlling body language**

**Evidence**

- `analyst-note.md:22`: **“The proposal converts a position of apparent legal strength into a controlled cash schedule”**. The arrangement is proposed and participation-gated; conversion has not occurred. `cross-examination.md:45` specifically identifies definitive **“converts”** language as outrunning the corrected conclusion.
- `analyst-note.md:38`: **“The cluster's financial actions tell one coherent story — fund pipeline optionality with retained sequencing control, while legal cash obligations are pushed to 2027+”**. This preserves the coordination/sequencing inference even while the same sentence admits that affordability and internal consistency are not demonstrated.
- `analyst-note.md:45`: **“each individually within disclosed capacity on current figures”** is a semantic restatement of the challenged **“each individually affordable”** claim. `cross-examination.md:29-31` says no liquidity waterfall, maturity schedule, minimum-cash assumption, or downside case supports that conclusion and requires removal.
- The same residuals propagated into `reports/jnj-talc-resolution-2026-08-07.md:44` and `:51`.

**Impact**

The corrected thesis and conclusion are conditional, but the body still states the disputed mechanism as accomplished/coherent and still makes an unsupported capacity conclusion. This creates internal inconsistency and means the two PARTIALLY SUSTAINED findings and calculation/control PARTIAL finding were not genuinely dispositioned.

**Exact correction needed**

- Replace line 22 with: **“The proposal offers a conditional path to convert apparent procedural leverage into a controlled cash schedule; it has not yet completed that conversion.”**
- Replace the opening of line 38 with: **“The actions are concurrent, but the disclosures do not establish a coordinated sequence: pipeline commitments and shareholder distributions may overlap with legal cash obligations from 2027 onward.”**
- Delete **“each individually within disclosed capacity on current figures”**. Replace it with: **“The disclosed snapshot does not establish combined affordability; it only shows the dated cash, debt, FCF, and deployment amounts.”**
- Apply the same corrections to the review-stage main report and its summary wherever the language was propagated.

**Re-audit boundary**

Re-audit `analyst-note.md` thesis, line 22, capital-deployment section, strongest counter-case, and conclusion/change-condition linkage, plus the corresponding propagated passages in `reports/jnj-talc-resolution-2026-08-07.md`. Do not reopen unaffected source facts unless numbers change.

---

### 3. **MAJOR — The SUSTAINED change-condition finding remains only partially corrected**

**Evidence**

- `analyst-note.md:60`: the note promises **“operational tests where observable.”**
- `analyst-note.md:63-66` identifies fields and admits partial/non-observability, but does not provide a baseline, observation window, formula, or decision rule for reserve movements, “bounded” recognition, residual docket behavior, or capital productivity.
- `analyst-note.md:68` still declares failure on **“an accrual materially inconsistent with a bounded schedule”** or holdouts that remain **“economically meaningful.”** Neither “materially inconsistent,” “bounded,” nor “economically meaningful” is defined or observable under the admitted disclosure gaps.
- `cross-examination.md:33-39` SUSTAINED this issue and required a filed field, formula, baseline, window, and decision rule, or an explicit **not observable from current disclosures** designation.
- The same vague failure rule appears in `reports/jnj-talc-resolution-2026-08-07.md:55-63`.

**Impact**

The note has improved its disclosure-field mapping, but it still presents non-operational judgments as thesis-failure rules. This risks inventing ex post thresholds and falsely labeling a monitoring question as a falsifiable condition.

**Exact correction needed**

- Keep the at-least-95% participation test as the only currently operational threshold.
- Reclassify accrual/reserve, residual docket, holdout economics, and capital productivity as **monitoring indicators, not pass/fail tests**, unless a source-defined threshold, baseline, period, and formula exists.
- Replace line 68 with wording such as: **“The current evidence supplies one source-defined failure condition: the at-least-95% participation condition is not met. Accrual scope, residual docket economics, and capital productivity remain monitoring judgments; no source-supported ex ante pass/fail threshold is available from the current disclosures.”**
- Do not invent a numeric materiality threshold to repair this defect.

**Re-audit boundary**

Re-audit only the change-condition/monitoring sections in the analyst note and main report, and their consistency with the CRO's decisive test. Reopen other sections only if new thresholds or figures are introduced.

---

### 4. **MAJOR — Material figures are not consistently sourced with SRC-ID + date at claim site, and two derived bridges lack complete claim-site formulas**

**Evidence**

- `analyst-note.md:10` repeats the central $5.5B, at-least-95%, $3B, $3.7B, $1B, $785M, $2.58B, and $0.64 figures with no SRC-ID citations at the thesis claim site.
- `analyst-note.md:20` gives the correct `$5.5B − $3.7B = ~$1.8B` formula but cites **“[SRC-01; SRC-04]”** without the required dates.
- `analyst-note.md:42` shows `$0.46 + $0.18 = $0.64` but does not show the midpoint-cut formula `$11.68 − $11.04 = $0.64` at that claim site.
- `analyst-note.md:51` states a ~$4.6B balance and ~$1.2B residual without the formulas `$11.6B − $7.0B = $4.6B` and `$4.6B − $3.4B = $1.2B`, and cites only the Data Steward rather than primary SRC-ID + date.
- `analyst-note.md:45`, `:49`, and `:52` use bare `[SRC-04]`, `[SRC-05]`, `[SRC-01]`, or `[SRC-02]` without the source date at the claim site.
- The review-stage main report repeats these defects in its numeric frontmatter summary (`reports/jnj-talc-resolution-2026-08-07.md:9`), short answer (`:16`), midpoint bridge (`:48`), capacity paragraph (`:51`), and reserve residual (`:74`).

**Impact**

The numbers are recoverable and mostly correct, but the report contract requires each material figure to be dated and sourced, while derived figures require rerunnable claim-level formulas. A source inventory at the end does not cure repeated claim-site omissions. The current text therefore overstates that all Data Steward/cross-ex corrections were incorporated.

**Exact correction needed**

1. Add compact claim-site citations to the thesis and report summaries: `[SRC-01, 2026-07-27]`, `[SRC-02, 2026-07-29]`, `[SRC-03, 2026-08-04]`, `[SRC-04, 2026-06-28]`, `[SRC-05, 2025-12-28]`, and `[SRC-06, 2026-07-15]` as applicable.
2. Change line 20 to `[SRC-01, 2026-07-27; SRC-04, 2026-06-28; derived]`.
3. Change the midpoint sentence to show both bridges explicitly: **`$11.68 − $11.04 = $0.64 = $0.46 + $0.18`**.
4. Change the reserve-residual sentence to: **“simple arithmetic only: `$11.6B − $7.0B = $4.6B`; `$4.6B − $3.4B = $1.2B` [SRC-05, 2025-12-28; derived]. The $1.2B attribution is unverified.”**
5. Add dates to all remaining bare SRC citations attached to material figures.
6. Apply the same controls to both review-stage report files, including frontmatter summaries; alternatively remove material figures from summaries that cannot carry clear source/date text.

**Re-audit boundary**

Re-audit every numeric claim line in the analyst note and both review-stage reports, the SRC-ID/date mapping, and the four mandated calculations ($1.8B, $0.64 components and midpoint, 42.89%, 3,800). Reinspect raw sources only for newly introduced or changed figures.

---

### 5. **MINOR — “Same five trading days” is an unsupported and inaccurate interval description**

**Evidence**

- `analyst-note.md:10`: **“In the same five trading days”**.
- The stated 28 July–4 August 2026 window contains six weekdays/trading sessions inclusive: 28, 29, 30, and 31 July; 3 and 4 August. The phrase also appears in `reports/jnj-talc-resolution-2026-08-07.md:9` and `:16`.

**Exact correction needed**

Replace the phrase in every occurrence with **“within the 28 July–4 August filing window”**. Do not substitute another counted-session claim unless the counting convention is stated.

---

### 6. **MINOR — Review-stage report wording prematurely says the CRO companion is published**

**Evidence**

- `reports/jnj-talc-resolution-2026-08-07.md:7` and `reports/jnj-talc-resolution-opposing-2026-08-07.md:7` both correctly set `status: review`.
- `reports/jnj-talc-resolution-2026-08-07.md:65` nevertheless labels the CRO essay **“published as a companion.”** Founder-only publication has not occurred.
- The pair otherwise satisfies the report contract: both have complete frontmatter, `type: company`, `subject: "JNJ"`, the same date/series identity, and reciprocal title-level references. The CRO report is a standalone thesis rather than a risk list.

**Exact correction needed**

Change **“published as a companion”** to **“prepared as a review-stage companion.”** Add explicit relative markdown links between the two report filenames in both directions before Founder review; retain `status: review` until the Founder explicitly publishes them.

## Verified controls / no finding

1. **Data Steward corrections applied:** evidence-log wording now says “at least 95%”; payment wording says “no additional payments due before 2028”; Sail's $785M/$465M/$140M/$2.58B terms are disclosed; “not yet accrued” is labeled unverified; the ~$1.2B reserve residual is unexplained; repurchase bases are distinguished; FY2023's $5,054M source is corrected to the consolidated statement of equity.
2. **Chronology corrected:** the talc PR is dated 27 July 2026 and the 8-K was filed 28 July; the 4 August 8-K is officer change only, not a notes offering. The analyst note reflects both corrections.
3. **Governance posture:** no price target, valuation formula, buy/sell/allocate advice, execution direction, portfolio data, momentum screen, legal-outcome prediction, or invented contingent-liability amount appears. The note is advisory and portfolio-blind.
4. **Point-in-time discipline:** figures are drawn from current issuer/SEC filings available through the 7 August 2026 pull, not stale reference-book figures; dates and period bases are generally explicit apart from Finding 4's claim-site omissions.
5. **CRO companion quality:** `cro-opposing-essay.md` advances one connected opposing mechanism, a multi-year path, strongest counterevidence, and a decisive test. It is not a generic risk inventory.
6. **Controlling-position cleanup partly succeeded:** “deliberate” is removed from the analyst's own thesis; “strongest legal position” and “only legally available channel” appear only as rejected/issuer-attributed formulations; “internally consistent” is explicitly denied rather than asserted. The residual overstatements are bounded in Finding 2.

## Clearance condition

**REMAINS BLOCKED** until all four MAJOR findings are corrected and re-audited within their stated boundaries. The two MINOR corrections may be verified in the same bounded pass. Publication status must remain `review`; Founder-only publication is outside audit authority.
