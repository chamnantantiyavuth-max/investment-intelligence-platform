# F1 — Silent Skill Self-Improvement Recurrence: Audit + Fix (Stage 6.6, 13 Aug 2026)

## Event (as reported by Founder)

`Self-improvement review: Patched SKILL.md in skill 'cross-profile-governance-sync' (1 replacement).`

## Audit result — root cause (answers A/B/C/D)

| Hypothesis | Verdict | Evidence |
|---|---|---|
| A. nudge=0 ไม่ครอบคลุม context นี้ | ❌ ไม่ใช่หลัก | nudge=0 ถูกตั้ง Stage 4.1 แต่… |
| B. fork จาก profile อื่นที่เปิดอยู่ | ❌ ไม่ใช่ | fork มาจาก session หลัก `20260812_173534_4700a7` เอง (bg-review:17420 spawn 01:45:39) |
| **C. session เก่าถือ config เดิม** | ✅ **ใช่ (ส่วนหนึ่ง)** | Session หลัก boot 17:35 — **ก่อน** Stage 4.1 ตั้ง nudge:0 (~21:00) → session นี้ถือ `_skill_nudge_interval=15` ตลอดชีวิต; config reload เฉพาะ session ใหม่ |
| **D. self-improvement อีกเส้นหนึ่ง** | ✅ **ใช่ (ส่วนหนึ่ง)** | กลไก = **memory review fork** (`flush_min_turns`/`memory.nudge_interval` ยัง active) → fork spawn ทุก ~10 turns; fork prompt สั่ง "update the skill library. Be ACTIVE" → fork มีสิทธิ์ skill_manage เต็ม |

**Root cause แท้ (3 ชั้น):**
1. `skills.write_approval: False` (default) — fork/agent เขียน skill ได้เลย ไม่มี approval gate
2. Memory-review fork ยัง spawn (memory nudge ≠ skill nudge) และ prompt สั่งให้ "update skill library" → fork ทดลอง skill_manage
3. Session เก่า (boot ก่อน nudge:0) ถือ config เดิม → nudge=0 ไม่มีผลกับ session ที่รันอยู่

**Fork ทำงานอะไร (01:45–02:04):**
- 01:46:27 skill_manage model-routing → **REFUSED** (not curator-managed — guard เดิมทำงาน)
- 01:46:52 + 01:46:58 + 01:47:22 → **PATCH สำเร็จ** cross-profile-governance-sync (เพิ่ม reference line) + อื่น
- 02:03 → **สร้าง skill ใหม่** `notebooklm-deep-research` (หลัง R4 rehearsal — fork บันทึก flow + pitfalls จริง)
- 02:03–02:04 → สร้าง `references/model-routing-migration-sweep-2026-08-13.md` + พยายาม patch/remove_file (บางส่วน refused)

## Fix — Guard ที่ถูกต้อง

1. **`skills.write_approval: true`** บน **13 production profiles** (iip + 11 org-* + ipm):
   - semantics (config_defaults L1891-1902): "applied to BOTH foreground agent turns AND the background self-improvement review fork"; write → **staged** (ไม่ commit) → Founder ตรวจ `/skills diff <id>` → `/skills approve <id>` / `/skills reject <id>`
   - "skills always stage rather than prompt" → fork จะไม่ timeout (silence ≠ consent แต่ staged รอ review ไม่ใช่เขียนทับ)
2. **`creation_nudge_interval: 0`** ยืนยันครบ 13 profiles (เจอ 4 profiles — macro/options/radar/ipm — ยังเป็น 15! ไม่เคยถูก preflight → แก้เป็น 0)
3. Config backups: `*.bak-2026-08-13-f1` ทุก profile

## Revert (unauthorized fork mutations → candidate)

| Fork mutation | Action | Candidate location |
|---|---|---|
| `skills-shared/research/notebooklm-deep-research/SKILL.md` (fork สร้างใหม่ 02:03, content ดี — proven flow + cp1252 pitfall + CDP pattern) | REMOVED จาก production | `evidence/harness/f1-fork-candidates/notebooklm-deep-research-skill-fork-created/` |
| `references/model-routing-migration-sweep-2026-08-13.md` (fork เพิ่ม 02:04) | REMOVED จาก production | `evidence/harness/f1-fork-candidates/model-routing-migration-sweep-ref-fork-added.md` |
| cross-profile-governance-sync SKILL.md reference line (fork เพิ่ม) | REMOVED (บรรทัดอ้างอิง) | (diff ใน candidate folder) |
| cross-profile-governance-sync Sol→Luna content (Stage 6.5 authorized — ไม่ใช่ fork) | KEPT (authorized) | — |

## Verification (bounded trigger-cross)

- Snapshot hashes ก่อน: cross-profile `73cc286f` · llm-council `7b0a8990` · notebooklm absent
- รัน **20 tool iterations** (เกิน nudge threshold เดิม 15) → รอ fork spawn
- **AFTER hashes: unchanged** (`73cc286f` / `7b0a8990` / absent) → **ZERO canonical skill mutation** ✅
- `hermes skills list-modified`: "No user-modified bundled skills" ✅

## Target invariant (now enforced)

```
Agent discovers skill improvement
→ candidate/staged diff (write_approval: true)
→ Founder/admin review (/skills diff)
→ explicit promotion (/skills approve)

Never:
agent/background reviewer → silently mutate canonical production skill
```

## Operational note (NotebookLM transport — per Founder)

- `browser_exec` stdout path = **defective on Windows** (cp1252 UnicodeDecodeError on non-ASCII stdin) — recorded
- Direct CDP websocket control = **currently proven working transport** — recorded
- Both captured in the fork-created candidate skill (reviewable for promotion)

---
<!-- 2026-08-13 02:18:26 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
