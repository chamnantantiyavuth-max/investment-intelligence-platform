# Final Targeted Confirmation — RM-2026-0003 (JNJ Talc-Litigation Resolution)

**Review role:** Internal Auditor / Red Team (`org-auditor`)  
**Review type:** Final targeted confirmation  
**Review date:** 2026-08-07  
**Scope:** ONLY the remaining MAJOR-1 dispatch-record residual: exact per-task source allowlists, retained prompt records/hashes, and execution-log reconciliation  
**Verdict:** **REMAINS BLOCKED**

## Boundary and verdict basis

The controlling re-audit left MAJOR-1 PARTIAL because the dispatch evidence lacked exact file-by-file per-task input allowlists and retained exact prompts or prompt hashes (`re-audit-note.md:35-43`). Its clearance condition requires correction and a confirmation limited to that dispatch-record evidence; MAJOR-2 through MAJOR-4 and MINOR-5 through MINOR-6 are not to be reopened (`re-audit-note.md:115-117`).

The corrected record now enumerates all eight raw source filenames, provides one per-task allowlist row and one recorded prompt hash for each task, retains complete Goal and Context blocks, and reconciles governance-file reads without admitting a sibling view. However, independent SHA-256 re-performance finds that the recorded Task 2 hash does **not** match the current verbatim `## Task 2` section. Therefore the retained prompt/hash evidence is not fully internally reproducible and MAJOR-1 is not cleared.

## Targeted checks

### (a) Exact eight raw source filenames — **CONFIRMED**

`first-pass-dispatch.md:21` enumerates exactly these eight raw files:

1. `8k-155-ex991-talc.htm`
2. `8k-163-cover.htm`
3. `8k-163-ex991-firefly.htm`
4. `8k-163-ex992-sail.htm`
5. `8k-167-cover.htm`
6. `8k-146-ex991-q2earnings.htm`
7. `10q-20260628.txt`
8. `10k-20251228.txt`

The same line identifies their common raw-source directory. No ninth raw filename is included in that exact list.

### (b) Exact per-task allowlist row for each of the three tasks — **CONFIRMED**

The table header defines an `Exact file-by-file allowlist` column (`first-pass-dispatch.md:25-26`). The three task rows are present at `first-pass-dispatch.md:27-29`:

- Task 0 / Equity Analyst: mandate + evidence log + the exact eight-file list above (`:27`).
- Task 1 / CRO: mandate + evidence log + the exact eight-file list above (`:28`).
- Task 2 / Data Steward: evidence log + the exact eight-file list above (`:29`).

Each row also records the task-specific sibling-prompt/result exclusion (`first-pass-dispatch.md:27-29`). The shared repo packet is resolved to exact paths at `first-pass-dispatch.md:23`; the raw-file reference in every row resolves to the exact eight-name list at `:21`.

### (c) Recorded SHA-256 prompt hash for each task — **CONFIRMED**

The dispatch table records one SHA-256 value in each task row (`first-pass-dispatch.md:27-29`):

- Task 0: `db91c369892e1c2d0a0cbc3c719f5a2b4c655d79b59a7ff4c2bd0a6fad25c7dd` (`:27`).
- Task 1: `62c2c52c37f7b79b423b98a538fc9edd7b5c0d3adfa3cb0146dea41b1dffb2bc` (`:28`).
- Task 2: `1329110b8b919d766ed197ce2ea2268d6f2e3778ddcd8efcfca85eb9a3a3a347` (`:29`).

The record defines these as hashes of each retained verbatim task section in `first-pass-prompts.md` (`first-pass-dispatch.md:31`). This check confirms that values are recorded; their cryptographic validity is tested separately in check (d).

### (d) Recomputed prompt hashes match the verbatim sections — **NOT CONFIRMED**

**Re-performance method:** read `first-pass-prompts.md` as bytes, identify each UTF-8 `## Task N` section from its heading through the byte immediately before the next level-2 `##` heading, and compute `hashlib.sha256(section_bytes).hexdigest()`. The file uses LF line endings. The resulting section byte lengths were 2,984 (Task 0), 3,163 (Task 1), and 2,888 (Task 2).

| Task | Section evidence | Recorded / expected SHA-256 | Independently recomputed SHA-256 | Result |
|---|---|---|---|---|
| 0 | `first-pass-prompts.md:5-14` | `db91c369892e1c2d0a0cbc3c719f5a2b4c655d79b59a7ff4c2bd0a6fad25c7dd` | `db91c369892e1c2d0a0cbc3c719f5a2b4c655d79b59a7ff4c2bd0a6fad25c7dd` | **MATCH** |
| 1 | `first-pass-prompts.md:15-24` | `62c2c52c37f7b79b423b98a538fc9edd7b5c0d3adfa3cb0146dea41b1dffb2bc` | `62c2c52c37f7b79b423b98a538fc9edd7b5c0d3adfa3cb0146dea41b1dffb2bc` | **MATCH** |
| 2 | `first-pass-prompts.md:25-34` | `1329110b8b919d766ed197ce2ea2268d6f2e3778ddcd8efcfca85eb9a3a3a347` | `38dc622bd1fd0a464ad2e529afeb76b1c391b9224d2d6f0c044feecb9b341a06` | **MISMATCH** |

The Task 2 mismatch is a direct failure of the remaining MAJOR-1 clearance condition. It is not a fresh finding on a settled item.

**Prompt-section completeness:** independently confirmed for all three retained sections:

- Task 0 has both `Goal (verbatim)` and `Context (verbatim)` (`first-pass-prompts.md:9-13`).
- Task 1 has both blocks (`first-pass-prompts.md:19-23`).
- Task 2 has both blocks (`first-pass-prompts.md:29-33`).
- The file has a footer timestamp, `2026-08-07 18:00 UTC+7` (`first-pass-prompts.md:44`).

### (e) Execution-log reconciliation and sibling-view exclusion — **CONFIRMED**

The dispatch record explicitly admits the additional governance inputs `PROJECT_INDEX.md`, `PROJECT_BIBLE.md`, `AGENTS.md`, and `PROJECT_STATE.md` for tasks 0-1 and states that they were self-discovered rather than sibling outputs (`first-pass-dispatch.md:32`).

The retained prompt record supplies the execution-log reconciliation at `first-pass-prompts.md:35-42`: task 0's governance-orientation operations are listed at `:38`; task 1 is described as analogous at `:39`; task 2 is limited to the evidence log and raw sources at `:40`; and the record states that these additional inputs were not sibling outputs and that no task read another task's view (`:37,42`).

## New correction-introduced findings

**None separate from the tested residual.** The Task 2 hash mismatch is the failed MAJOR-1 correction itself, not scope expansion. No settled MAJOR-2/3/4 or MINOR-5/6 item was reopened, and no scope-bleed finding is made.

## Required correction for clearance

Replace the Task 2 prompt hash in the dispatch record with the SHA-256 of the retained verbatim Task 2 section, or restore the retained Task 2 section byte-for-byte to the exact content represented by the recorded hash. Then re-run the three section hashes under one documented boundary convention and perform a final confirmation limited to the changed dispatch/prompt evidence.

## Final verdict

**REMAINS BLOCKED** — checks (a), (b), (c), and (e) are CONFIRMED, but check (d) is NOT CONFIRMED because Task 2's recorded prompt SHA-256 does not match its retained verbatim section.
