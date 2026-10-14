# M6.8 STAGE A — CORRECTION + notebooklm-py 0.8.5 COMPATIBILITY PROBE (FD #156 follow-up)

Date: 2026-10-14
Scope: isolated dependency compatibility probe + read-only diagnostics ONLY. Founder-authorized.
**NO STATE-CHANGING PROVIDER OPERATION WAS PERFORMED** (no login, no auth refresh, no credential
migration, no notebook create/rename/delete, no upload, no Deep Research). No credentials, cookie
values, tokens, account identifiers, notebook titles or IDs are recorded anywhere in this file.

## 1. CORRECTION OF THE PRIOR DIAGNOSTIC INTERPRETATION (SUPERSEDED — do not carry forward)

The FD #156 / Stage A record (`evidence/m6.8/STAGE-A-TRANSPORT-PROBE-2026-10-14.md`, §5) stated the
v0.7.3 failure was **"NOT an authentication failure"** and classified it as page-structure/UI drift
on the strength of the v0.7.3 client's own three-way discrimination. **That categorical claim is
WITHDRAWN as unsupported.**

Why it was wrong (Founder-supplied upstream fact, now confirmed empirically here):
* notebooklm-py **v0.8.5 (2026-10-12)** release notes explicitly fix: **"Signed-out sessions
  misreported as a page-structure change."** A *signed-out* session could serve a tokenless app
  landing page with **no** authentication redirect — which is exactly the shape that v0.7.3's
  discrimination maps to the structure-drift branch.
* v0.8.5 instead **checks the application's `/login` state** to distinguish expired authentication
  from genuine structural drift.
* The isolated 0.8.5 probe below reproduces this corrected classification directly.

**Also withdrawn as insufficient:** "30 cookies + a SID are present" does **not** prove
server-side authentication. It only proves the local cookie store is populated.

What survives from the earlier record (still true): the v0.7.3 error text was real and
reproducible, the local session *store* is well-formed, and `CONSUMER_BROWSER_TRANSPORT =
CURRENTLY NON-FUNCTIONAL` was a correct observation of the OUTCOME. Only the CAUSE attribution was
wrong.

**CORRECTED CAUSE (observed, not inferred): expired / signed-out authentication.**

## 2. M6.7 / FD #156 synchronization (completed before the probe)

| Item | Value |
|---|---|
| push | ordinary fast-forward `57d8972..a163749` → `origin/impl/m6-gemini-notebook` (exit 0) |
| sole local descendant | verified: exactly 1 commit (`a163749`) ahead, worktree clean, `origin/impl` an ancestor |
| remote impl after re-fetch | **`a163749099312a143784503601807bbfcc7929c8`** (= local HEAD) |
| ahead/behind | `0 0` |
| `origin/main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` — unchanged |
| M6.7 accepted tip | `57d89728ad30a390e7572c6800965c3535690a82` (remote-verified) |

## 3. Isolated 0.8.5 installation (main runtime NOT touched)

* Environment: NEW venv **outside the IIP repository** —
  `<iip profile>/cache/scratch/m68-venv-085` (Python 3.11.15, pip 24.0).
* Installed: **`notebooklm-py==0.8.5`** (official upstream package; **no `android` extra**).
* `pip show notebooklm-py` → `Version: 0.8.5`, `Requires: click, filelock, httpx, idna, rich`.
* `pip check` → **"No broken requirements found."**
* CLI: **`NotebookLM CLI, version 0.8.5 (50493ddf)`**.
* **Main Hermes runtime still `notebooklm-py 0.7.3`** (rollback intact; not upgraded).
* Profile used: the EXISTING authorized consumer profile (`default`) via its existing store — **no
  credential value was copied, duplicated, printed or committed.**

## 4. Observed results (sanitized)

**`doctor` (0.8.5, exit 0):** Profile `default` ✓ · Migration ✓ · Profile Dir ✓ · **Auth ✓ "local
auth cookies usable"** · Config ✓ · one non-blocking warn (Headless Reauth unavailable: browser
extra not installed). It prints: *"Local checks raised a warning. **Online authentication was not
tested.**"*

**`auth check` (0.8.5):** storage exists ✓ · JSON valid ✓ · 30 cookies ✓ · SID cookie ✓ ·
`__Secure-1PSIDTS` ✓ · **Token fetch ⊘ skipped** · **Account: unknown** · **Master token: not
present**.

**`auth check --test --passive` (0.8.5, exit 1 — single call, passive = no refresh):**
```
Token fetch      ✗ fail
Error: Token fetch failed: Authentication expired or invalid.
Run 'notebooklm login' to re-authenticate.
```

**`list --backend web` (0.8.5, exit 1 — single call, WEB backend explicitly selected):**
```
Authentication error: Authentication expired or invalid. https://notebook.google.com/ served a
signed-out page, and its sign-in check redirected to https://accounts.google.com/<redacted>
Run 'notebooklm login' to re-authenticate.
```

## 5. CLASSIFICATION (from actual observations)

**B — AUTHENTICATION REQUIRED.**

The response is the corrected v0.8.5 auth classification: Google served a **signed-out page** and
the sign-in check **redirected to the accounts sign-in surface**. This is not a transport, CSRF,
protocol or access failure, and it is not an environment/dependency failure (§3 is clean).

Per the Founder's branch rule, the provider test **STOPS here**. No further provider calls were
made and no credential recovery or autonomous reauthentication was attempted.

## 6. REQUIRED FOUNDER ACTION (ordinary interactive login)

An ordinary interactive login of the EXISTING `default` profile is required, by the Founder, in a
real browser window:

```
<iip profile>/cache/scratch/m68-venv-085/Scripts/notebooklm.exe --profile default login
```

* This opens the interactive sign-in flow; the Founder signs in to the intended Google account and
  the CLI rewrites the SAME profile store it already uses (no credential values are handled by me).
* Note from the 0.8.5 doctor: **headless re-auth is unavailable without the `browser` extra**
  (playwright). An interactive login normally drives a real browser window and may not need it, but
  if the login command reports a missing browser dependency, that is the one additional
  dependency decision to make (NOT installed here).
* After a successful login, the next step is simply to **re-run the same read-only probe once** in
  this isolated 0.8.5 environment.
* I did NOT run `login`, did NOT run `auth refresh`, and did NOT attempt any credential migration.

## 7. Android backend assessment (NOT approved, NOT needed for this blocker)

| Question | Assessment (observed basis only) |
|---|---|
| Is Web v0.8.5 genuinely still blocked? | It is blocked — but by **expired authentication**, not by a Web transport defect. The Web path has NOT been shown to be broken post-login. |
| Android's required authentication/bootstrap | The Android backend needs a **master token**, which the 0.8.5 `auth check` shows as **"not present"**; the release notes require the separate `android` extra and its own provisioning. Existing Web cookies are **not** sufficient. |
| Credential storage / access implications | A master token is a longer-lived, broader credential than the web profile store — higher blast radius, additional storage and rotation handling. Not justified by a blocker that a login appears to fix. |
| Required read-only API operations available? | **NOT VERIFIED** — no Android provisioning exists here and none was attempted. |
| Closed-corpus / request-isolation verification limits | Unchanged and unproven: neither backend provides the closed-corpus or request-isolation guarantees M6.8 must VERIFY; those remain to be established by real probes, and an unverifiable property must FAIL CLOSED. |

**Recommendation:** do NOT take the Android path yet. Retry the Web backend after an ordinary login;
only if Web still fails post-login does Android become the candidate — and it would then need its
own separate authorization, dependencies and bootstrap.

## 8. Invariants preserved

`M6.8-TRUST-BOUNDARY-ACCEPTANCE` retained unchanged. No provider-controlled proof resolver; no
provider-controlled low-level atomic SUCCESS write; no SUCCESS without trusted proof verification;
no fabricated closed-corpus or request-isolation guarantee; no M6.8 implementation; no real Deep
Research; no notebook mutation; no credential extraction; no cron activation; no schema change; no
`main` merge. M6.7 remains CLOSED. 5/5 cron PAUSED.

## 9. Command inventory (exhaustive)

Executed (all read-only): venv create · `pip install notebooklm-py==0.8.5` · `pip show` · `pip
check` · `notebooklm --version` · `notebooklm doctor` · `notebooklm auth check` ·
`notebooklm auth check --test --passive` (single) · `notebooklm --backend web --quiet list`
(single) · version/help inspection · `pip show` on the main env (verification only).
**NOT executed:** `login` · `auth refresh` · `auth logout` · `auth inspect` · `create` · `delete` ·
`rename` · `ask` · `use` · `clear` · any upload · any settings change · any Deep Research · any
Android provisioning.
