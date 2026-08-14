# PRE-CUTOVER REPORT — Free Auxiliary + OpenRouter Integration (IIP)

**Revision 2 (corrections applied) — 2026-08-14 10:35 UTC+7**
**Rev 1 (original): 2026-08-14 09:28 UTC+7 · Author: Hermes (iip profile)**
**Source pack:** `ChatGPT/Integration 14 Aug 2026/` · **HARD HOLD respected:** no production config mutated before 17 Aug Weekly Radar Stage-7 proof. Live Office / Kanban authority / old-board ACL / Stage-8 scope / IPM / research doctrine untouched.

---

## สรุปสำหรับชำนาญ (Revision 2)

1. **7 evidence gaps ปิดครบด้วยหลักฐานจริง** — รวมการแก้คำว่า "ZDR PASS" → data-collection PASS + ZDR ต้องพิสูจน์ด้วย `zdr:true` แยกต่างหาก
2. **ผลชี้ขาดที่สำคัญ — Compression ฟรี FAIL:** canary context จริง 261K tokens (ใหญ่กว่าเป้า 200K) → Nemotron Ultra free บีบเหลือ 3.45% แต่ **Harness Stage 7/8, Live Office, baseline FREEZE, PASS WITH CONDITIONS, 17 Aug deadline, Kanban หายจาก summary ทั้งหมด** — ผิดเกณฑ์ "zero critical-state loss" → **compression ต้องอยู่ DeepSeek paid** (ไม่ promote ฟรี)
3. **ZDR จริง:** ทั้ง 3 ตัวผ่าน `zdr:true` explicit (Ultra เจอ upstream 502 ชั่วคราวรอบนึงแล้วผ่าน) — ใช้ `data_collection: deny` อย่างเดียวไม่พอจริงตามที่ review ชี้
4. **Gemini Auditor ยืนยัน subscription path:** `agy models` เห็น `gemini-3.6-flash-high` + bounded audit canary ผ่าน Antigravity CLI (ไม่ใช้ API key) — ตอบถูกว่า "17 Aug หาย = fidelity failure" ตรงกับผล canary
5. **Fallback design ยืนยันได้ใน v0.20.0 source:** per-task `fallback_chain` + skip เฉพาะ model ที่ล้ม (provider-wide เฉพาะ auth/payment) + per-entry timeout + main-agent safety net → ออกแบบ free→DeepSeek Direct→main ของชำนาญ implement ได้ตรงๆ
6. **Preflight พร้อมใช้จริง** (`free_model_preflight.py`) — ทดสอบ live แล้ว: BLOCK slug ผิด (exit 2), ยืนยัน cost==0, ZDR gate ต่อ slot
7. **Routing freeze ตามตารางชำนาญ** — promotion ทั้งหมดยัง HOLD จนกว่า 17 Aug proof + Stage 8 retirement

---

## 1. Current Routing Map (verified 14 Aug 2026 — live config, unchanged from Rev 1)

| Layer | Value |
|---|---|
| Main | `deepseek-v4-flash` / deepseek (DeepSeek Direct) · delegation same · `fallback_providers: []` |
| Aux slots (11) | all `provider: auto` → run on main model; OpenRouter fallback `google/gemini-3.6-flash` (PAID) when key present |
| Compression | enabled, threshold 0.5, target 0.2, model auto (main) |
| Cron | Weekly Radar `8ba233e88015` Mon 08:00 (17 Aug = proof run) · Mid-Week `cda817d17236` Thu 08:00 · 3 others |
| Profiles | 24 × deepseek-v4-flash, no per-profile overrides |
| Usage 7d | deepseek-v4-flash 1,258M tok · gemini-3.6-flash 240.7K (paid aux) · luna 35K |

## 2. Free Slugs — Live-Verified (OpenRouter /models, 411 models) + ZDR (explicit)

| Slug | Exists | ctx | ZDR `zdr:true` probe | Notes |
|---|---|---|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | ✅ | 1M | ✅ cost=0 (1× transient upstream 502, retry OK) | compression candidate — **FAILED long-context canary** |
| `nvidia/nemotron-3-nano-30b-a3b:free` | ✅ | 256K | ✅ cost=0 | profile_describer/web_extract candidates; title/tags REJECTED |
| `google/gemma-4-26b-a4b-it:free` | ✅ | 262K | ✅ cost=0 (1× 429 transient) | vision candidate — multi-image canary PASSED |

**Privacy terminology (corrected per review):** `data_collection: deny` only avoids data-collecting providers; it is NOT proof of Zero Data Retention. Production free-aux must send `provider {data_collection: deny, zdr: true, require_parameters: true}` per request (encoded in `auxiliary.<slot>.extra_body`). All three verified with explicit `zdr:true`. Slot without a ZDR route = PAID-ONLY (none currently — all 3 have routes, subject to preflight re-check at cutover).

## 3. Canary Results (Revision 2 — all isolated, no config mutation)

**A) LONG-CONTEXT COMPRESSION — Nemotron Ultra free: FAIL at production scale (decisive)**
| Case | Input | Output | Ratio | Verdict |
|---|---|---|---|---|
| C100k (real IIP history, non-sensitive) | 127,762 tok | 9,000 tok (cap) | 7.04% | CONDITIONAL — FD register 73 rows + prose preserved; **17 Aug deadline DROPPED**; FROZEN→"FREEZE" (concept kept, token changed) |
| Cfull (real history, 52 files 703K chars) | 260,972 tok | 9,000 tok (cap) | 3.45% | **FAIL — Stage 7/8, Live Office, baseline FREEZE, PASS WITH CONDITIONS, 17 Aug, Kanban ALL ABSENT**; output = decision register + report titles only |
- Invented-FD check: 0 real inventions at both scales (earlier "FD #1/#10/#22/#23" = range-header / prefix artifacts, verified by inspection — corpus uses bare-number register, model reformats to `FD #N`; e.g. `FD #10` matched inside `FD #107`).
- Negations: NOT APPROVED ✅, DISABLED ✅, dissent ✅ preserved; FROZEN/PASS WITH CONDITIONS dropped at Cfull.
- Per pack criterion "zero critical-state loss = PASS" → **compression free = FAIL → PAID-ONLY.** Options to revisit post-Stage-8 (not now): stricter prompt (date/state-first instruction), higher output budget, hierarchical/split compression, or accept free only for small contexts (<50K tok) with paid above threshold.

**B) TEXT AUX — Nemotron Nano free: 2/4 PASS (unchanged from Rev 1)**
- profile_describer ✅ 10/10 · web_extract ✅ 10/10 (candidates only — retest with exact Hermes slot prompts before promote)
- title_generation ❌ / tts_audio_tags ❌ — instruction-following failure → **keep DeepSeek paid** (Gap 6 closed as REJECT)

**C) VISION — Gemma 4 free: PASS (Gap 7 closed)**
- Multi-image set (3 real IIP screenshots: Briefing, Apple Moat, CS Product Radar) — each identified with correct layout/sections/labels incl. "Thesis: Under Review", Width/Depth/Trend values, synthetic label.

**D) PRIVACY — corrected & completed (Gap 2 closed)**
- `data_collection: deny` alone: PASS (Rev 1) — now labeled **data-collection policy PASS only**
- Explicit `provider.zdr: true` + deny + require_parameters: **PASS 3/3** (Ultra 1× upstream 502 → retry OK; Gemma 1× 429 → retry OK) — ZDR routes exist for all three free models today; **re-verify at cutover** (routes can change).

**E) FAILURE SHAPE — CRITICAL (unchanged from Rev 1):** `:does-not-exist` suffix → HTTP 200 routed to PAID base model with real cost. Free-model preflight is the guard (Gap 5).

## 4. Gap 3 — Gemini Auditor subscription path: VERIFIED
- `agy models` (Antigravity CLI at `C:\Users\Admin\AppData\Local\agy\bin\agy`) exposes `gemini-3.6-flash-high` (+ 3.7 family) to the subscribed account.
- Bounded audit canary via `agy --print ... --model gemini-3.6-flash-high --effort high`: PASSED — confirmed HOLD preserved, **"omitting 17 Aug = fidelity failure"** (matches our compression finding), self-identified as Gemini 3.6 Flash. Runs on subscription quota, **no API-key billing**.
- Constraint honored: Gemini is Auditor-only, not drafting/fallback.

## 5. Gap 4 — Fallback design: CONFIRMED in v0.20.0 source (no free_only:true)
`agent/auxiliary_client.py` + `hermes_cli/config_defaults.py`:
- `auxiliary.<task>.fallback_chain`: ordered list of `{provider, model, base_url, api_key, timeout}` entries — **per-task**, exactly as designed.
- Skip semantics: model-scoped failure (timeout/conn/429/model-incompatible) skips ONLY the failed (provider, model); provider-wide failure (401/402) skips the whole provider (`BackendIdentity` / `FailureScope`, `should_skip_candidate`).
- Per-entry `timeout` (fallback no longer dies on the primary's deadline — real 163K-token compression case #62452).
- Context guard: entry with ctx < task minimum is skipped.
- After chain exhausts → **main-agent model safety net** (`main-agent(<provider>)`, `_try_main_agent_model_fallback`) = last resort, automatic.
- **Decision:** `auxiliary.free_only: true` NOT used globally (per Founder). Design:
```yaml
auxiliary:
  vision:
    provider: openrouter
    model: google/gemma-4-26b-a4b-it:free
    extra_body: {provider: {data_collection: deny, zdr: true, require_parameters: true}}
    fallback_chain:
      - provider: openrouter      # paid reliable vision (e.g. gemini-3.6-flash) — pick at implementation
        model: google/gemini-3.6-flash
  profile_describer: / web_extract:   # Nano free primary, DeepSeek Direct fallback
    provider: openrouter
    model: nvidia/nemotron-3-nano-30b-a3b:free
    extra_body: {provider: {data_collection: deny, zdr: true, require_parameters: true}}
    fallback_chain:
      - provider: deepseek
        model: deepseek-v4-flash
  compression:                   # PAID-ONLY (canary FAIL) — stays on main model
  title_generation: / tts_audio_tags:  # PAID (Nano rejected)
```
- Caveat to prove at cutover (per plan): actual runtime fallback trigger on a live 429 — canary with a temporarily invalid free slug in a sandbox profile first.

## 6. Gap 5 — Free-Model Preflight: DELIVERED + LIVE-TESTED
`ChatGPT/Integration 14 Aug 2026/free_model_preflight.py` (proposal artifact, not wired):
- Step 1: expected slug → GET /models → **exact match required** (no substring/normalization) → missing = BLOCK (exit 2).
- Step 2 (--probe): 1-token ping → returned `model` must equal slug AND `usage.cost == 0` → else ALERT (exit 3) — catches silent paid routing.
- Step 3 (--require-zdr): re-probe with `provider {data_collection: deny, zdr: true, require_parameters: true}` → unavailable = PAID-ONLY mark (exit 4).
- Live tests: Ultra/Nano → all OK (exit 0); `...:typo` → BLOCK exit 2. ✓

## 7. Gap 7 — Vision multi-image: CLOSED (see §3C)

## 8. Estimated Savings (updated)
- Paid aux traffic today: gemini-3.6-flash ~240.7K tok/7d (cents-scale/week). Free-aux is optimization, not the big lever — unchanged from Rev 1.
- **Compression free is now OFF the table** → paid compression stays; savings only from profile_describer/web_extract/vision slots.
- Main migration (Phase C, post-Stage-8) remains the material lever — compare DeepSeek Direct invoice vs OpenRouter `deepseek/deepseek-v4-flash` ($0.14/M in, $0.28/M out) before deciding.

## 9. Frozen Target Routing (per Founder — promotion still gated on 17 Aug + Stage 8)

| งาน | Target | Status |
|---|---|---|
| Main / CoS | DeepSeek V4 Flash High / OpenRouter | post-Stage-8 (invoice compare) |
| Research workers | DeepSeek V4 Flash / OpenRouter | post-Stage-8 |
| **Compression** | **DeepSeek paid (NOT free)** | free FAILED long-context canary |
| Profile description | Nemotron Nano Free | candidate (retest slot prompt) |
| Web extraction | Nemotron Nano Free | candidate (retest slot prompt) |
| Title generation | DeepSeek paid | Nano rejected |
| TTS tags | DeepSeek paid | Nano rejected |
| Vision | Gemma 4 Free (fallback → paid vision) | provisional ✅ |
| Approval / governance | DeepSeek paid | — |
| Kanban decomposer | DeepSeek paid | — |
| Premium escalation | Luna High / OpenRouter | current |
| Auditor | Gemini 3.6 Flash High / Antigravity subscription | ✅ verified |
| Emergency provider | DeepSeek Direct | fallback_chain target |

## 10. Final Recommendation (Revision 2)
- **PRE-CUTOVER = PASS WITH CORRECTIONS** — all 7 gaps closed with live evidence; 17 Aug HARD HOLD preserved; no production mutation.
- **Promotion gate stays HOLD** until: (1) 17 Aug Weekly Radar proof → Stage 7 FINAL PASS, (2) Stage 8 retirement, (3) Founder confirmation.
- **Do NOT promote:** compression free (FAIL), title/tags free (rejected).
- **Promote first (post-gate):** profile_describer + web_extract (Nano, after slot-prompt retest), vision (Gemma), each with ZDR extra_body + fallback_chain + preflight run before cutover.
- STOP after this report per instruction.

## 11. Artifacts
- `ChatGPT/Integration 14 Aug 2026/PRE-CUTOVER-REPORT-2026-08-14.md` (this file, Rev 2)
- `ChatGPT/Integration 14 Aug 2026/free_model_preflight.py` (proposed preflight, tested)
- Canary scripts + outputs: `%LOCALAPPDATA%\Temp\canary_free_aux.py`, `canary_long_ctx_v3.py`, `canary_long_ctx_v4.py`, `corpus_100k.txt`, `corpus_full.txt`, `compress_out_100k.txt`, `compress_out_full.txt`, `canary_zdr_vision.py`
- No production files modified. No FD registered (prep-only; Founder gate pending).

<!-- 2026-08-14 10:35 UTC+7 -->
