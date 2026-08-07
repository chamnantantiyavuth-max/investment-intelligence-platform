# Bounded Re-Audit Note — RM-2026-0003 (JNJ Talc-Litigation Resolution)

**Review role:** Internal Auditor / Red Team (`org-auditor`)  
**Review type:** Bounded re-audit after round-1 corrections  
**Review date:** 2026-08-07  
**Scope:** Only MAJOR-1 through MAJOR-4 and MINOR-5 through MINOR-6, within the re-audit boundaries in `audit-note.md`  
**Verdict:** **REMAINS BLOCKED**

## Verdict basis

Five residuals are fully applied. MAJOR-1 is only **PARTIAL**: the §23.9 history preservation, manifest-derived timestamps, and all three artifact hashes are verified, but the record still does not preserve the round-1-required exact file-by-file input allowlist or a prompt/hash for each task. Its table uses `raw temp dir (8 files) + own role brief` shorthand while calling the allowlist “exact,” and the referenced live logs truncate the kickoff prompt/context. The anti-anchoring record therefore remains insufficiently reproducible under the original re-audit boundary.

No settled arithmetic or primary-source conclusion was reopened.

## Residual dispositions

### MAJOR-1 — **PARTIAL**

**Applied evidence**

- Erroneous values are preserved in the §23.9 block (`first-pass-dispatch.md:50-57`):
  > “**Original (erroneous) values — preserved as history, do not reuse:**”
  > “dispatched **2026-08-07 ~18:55 UTC+7**”
  > “completed ~18:40 / ~18:35 / ~18:44 UTC+7”; “Batch result (returned **~19:05 UTC+7**)”
- Authoritative runtime times are now used (`first-pass-dispatch.md:9-10`):
  > “**Dispatch time:** **2026-08-07 17:32:14 UTC+7** (runtime manifest `manifest.json`, authoritative)”
  > “**Batch completion:** **2026-08-07 17:39:16 UTC+7** (manifest `"completed"` field...)”
- The underlying manifest independently confirms `started: 2026-08-07 17:32:14` and `completed: 2026-08-07 17:39:16` (`manifest.json:3,28`). Commit `594025a` is timestamped `2026-08-07T17:39:55+07:00`, consistent as an upper bound.
- Per-task rows are present for all three tasks (`first-pass-dispatch.md:21-25`), including explicit sibling-output exclusions.
- Artifact hashes are persisted at `first-pass-dispatch.md:34-36` and independently recomputed with `sha256sum`:
  - `first-pass-equity-analyst.md` — `51a2dcdadc6878c49c7f647dfdda9702916592bf6a6cd13cc21660c3899fa589` — **MATCH**
  - `first-pass-cro.md` — `32a891c72c4df3e36569861c343ec12387c9fbdde3eed54d2f2fd80b77a11d65` — **MATCH**
  - `first-pass-data-steward.md` — `3b2f3a83d0517bf663b9dd604bfc3089daf0f0e37adbc7937c6ae2000b014c5a` — **MATCH**

**Residual**

The round-1 correction required an **exact file-by-file allowlist** and exact role brief or prompt hash for each task. The corrected rows still say (`first-pass-dispatch.md:23-25`):

> “mandate file + evidence-log.md + **raw temp dir (8 files) + own role brief**”

No eight raw filenames are enumerated, and no role-brief/prompt hash is recorded. The referenced task logs do not cure this: each kickoff entry truncates the goal/context (`task-0.log:7`, `task-1.log:7`, `task-2.log:7`, each showing `…(+N chars)`). The logs also show additional governance/spec inputs read during execution that are absent from the table (for example `task-0.log:27-40` and `task-1.log:16-28`). The allowlists are per-task and durable at a category level, but not exact or fully reproducible as required by the original boundary.

**Smallest remaining correction:** enumerate the eight admitted raw source filenames and identify the exact per-task role brief/prompt by full retained text or SHA-256; reconcile any admitted governance/spec inputs. Preserve the current correction block append-first.

### MAJOR-2 — **APPLIED**

The three residual overstatements are gone from both `analyst-note.md` and the main report, and the replacements carry the required conditional/non-coordination/non-affordability meaning.

- Conditional path (`analyst-note.md:22`; main report `:28`):
  > “The proposal offers a conditional path to convert apparent procedural leverage into a controlled cash schedule; it has not yet completed that conversion.”
- Concurrent, not established as coordinated (`analyst-note.md:38`; main report `:44`):
  > “The actions are concurrent, but the disclosures do not establish a coordinated sequence...”
- Combined affordability not established (`analyst-note.md:45`; main report `:51`):
  > “The disclosed snapshot does not establish combined affordability; it only shows the dated cash, debt, FCF, and deployment amounts...”

Exact scans found no occurrence of `converts a position of apparent legal strength`, `one coherent story`, or `each individually within disclosed capacity` in either file.

### MAJOR-3 — **APPLIED**

Both change-condition sections now define exactly one operational test and label all remaining items as monitoring indicators.

- Analyst note (`analyst-note.md:60-62`):
  > “The disclosed record supplies **one source-defined failure condition**: the at-least-95% participation condition is not met...”
  > “**Participation confirmation** — *operational test:* at-least-95% threshold met... This is the only source-defined threshold.”
- Analyst note (`analyst-note.md:63-66`): Q3 accrual, residual docket behavior, holdout economics, and capital productivity are each explicitly labeled `monitoring indicator`.
- Main report (`reports/jnj-talc-resolution-2026-08-07.md:55-61`) repeats the same one-test/four-indicator structure.
- Both close with (`analyst-note.md:68`; main report `:63`):
  > “No numeric materiality threshold is invented to repair the gap...”

No second pass/fail test or invented numeric threshold was found.

### MAJOR-4 — **APPLIED**

The bounded thesis/report-summary claim sites now carry dated SRC references, both mandated bridge presentations are present, and no bare SRC-ID attached to a material figure remains.

- Analyst thesis (`analyst-note.md:10`) cites the talc/reserve figures with `[SRC-01, 2026-07-27; SRC-04, 2026-06-28]` and the transaction/guidance figures with `[SRC-02, 2026-07-29; SRC-03, 2026-08-04]`.
- Main-report frontmatter summary (`reports/jnj-talc-resolution-2026-08-07.md:9`) cites its talc/reserve figures with `[SRC-01, 2026-07-27; SRC-04, 2026-06-28]` and transaction/guidance figures with `[SRC-02, 2026-07-29]`.
- Main-report short answer (`reports/jnj-talc-resolution-2026-08-07.md:16`) repeats dated claim-site citations for both figure groups.
- Guidance bridge (`analyst-note.md:42`; main report `:48`):
  > “`$11.68 − $11.04 = $0.64 = $0.46 + $0.18` ... [SRC-06, 2026-07-15; SRC-02, 2026-07-29; derived]”
- Reserve bridge (`analyst-note.md:51`; main report `:76`):
  > “`$11.6B − $7.0B = $4.6B`; `$4.6B − $3.4B = $1.2B` [SRC-05, 2025-12-28; derived]”

A citation scan across `analyst-note.md`, the main report, and the opposing report found **zero** bracketed `SRC-ID` segments lacking a `YYYY-MM-DD` date.

### MINOR-5 — **APPLIED**

`five trading days` is gone from all three bounded artifacts. The required replacement appears at:

- `analyst-note.md:10`:
  > “Within the 28 July–4 August filing window...”
- Main report `reports/jnj-talc-resolution-2026-08-07.md:9,16`:
  > “Within the 28 July–4 August filing window...”
- `secretary-synthesis.md:9`:
  > “Within the 28 July–4 August filing window...”

### MINOR-6 — **APPLIED**

- Main-report wording is corrected (`reports/jnj-talc-resolution-2026-08-07.md:65`):
  > “## The dissenting view (CRO opposing essay, prepared as a review-stage companion)”
- Main → opposing markdown link is explicit (`reports/jnj-talc-resolution-2026-08-07.md:67`):
  > “[`jnj-talc-resolution-opposing-2026-08-07.md`](jnj-talc-resolution-opposing-2026-08-07.md)”
- Opposing → main markdown link is explicit (`reports/jnj-talc-resolution-opposing-2026-08-07.md:14`):
  > “companion to "[JNJ's Talc Proposal: A Conditional Schedule, Not Finality](jnj-talc-resolution-2026-08-07.md)"”
- YAML frontmatter for both reports parsed successfully:
  - main report: `type: company`, `subject: JNJ`, `status: review`, `updated: 2026-08-07` (`:3-8`)
  - opposing report: `type: company`, `subject: JNJ`, `status: review`, `updated: 2026-08-07` (`:3-8`)

Review status is retained; no premature `published as a companion` wording remains.

## New findings introduced by the corrections

**None.** No correction-introduced regression was identified within the bounded sections. No settled item was reopened; no scope-bleed finding was made.

## Clearance condition

**REMAINS BLOCKED** only on the MAJOR-1 residual: replace the category-level per-task input descriptions with exact file-by-file allowlists and retain each exact task role brief/prompt or its SHA-256, then perform a targeted confirmation limited to that dispatch-record evidence. MAJOR-2, MAJOR-3, MAJOR-4, MINOR-5, and MINOR-6 require no further re-audit unless their corrected sections change.
