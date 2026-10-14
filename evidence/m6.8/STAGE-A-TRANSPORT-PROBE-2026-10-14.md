# M6.8 STAGE A — READ-ONLY CONSUMER TRANSPORT FEASIBILITY (FD #156)

Date: 2026-10-14
Scope: bounded READ-ONLY feasibility probe only (Founder-authorized). No store exists in the
provider; nothing was created, deleted, renamed, uploaded, queried or launched.
**NO STATE-CHANGING PROVIDER OPERATION WAS PERFORMED.** No credentials, cookie values, tokens or
notebook contents are recorded here (cookie NAMES are deliberately not recorded either).

## 0. Prerequisite: M6.7 remote sync (completed before the probe)

| Item | Value |
|---|---|
| local chain | `c288aeb` → `e8fd966` → `891523c` → `30b0ece` → `57d8972` |
| push | ordinary fast-forward `c288aeb..57d8972` → `origin/impl/m6-gemini-notebook` (exit 0) |
| remote impl after re-fetch | `57d89728ad30a390e7572c6800965c3535690a82` (= local HEAD) |
| ahead/behind vs remote | `0 0` |
| all four commits visible on remote | YES (`e8fd966`, `891523c`, `30b0ece`, `57d8972`) |
| `origin/main` | `5bf107774b29e5a5fe4dcec5846800b9b48361ba` — unchanged |
| cron | 5/5 PAUSED |

## 1. Prior recorded condition (design-gate evidence)

`design/qad-pivot/m6/QAD-M6.0-DESIGN-GATE-RECONCILIATION.md` line 271:
> **Consumer transport reality (recorded, unchanged):** `CONSUMER_BROWSER_TRANSPORT = CURRENTLY
> NON-FUNCTIONAL`. Not a reason to weaken contracts; not permission to fabricate automation; no
> automated integration may be claimed until a real live canary passes.

## 2. Installed environment (read-only)

| Item | Observed |
|---|---|
| CLI | `notebooklm` (venv entry point) |
| version | **NotebookLM CLI, version 0.7.3** (identical to the version at which the failure was recorded) |
| package | `notebooklm-py 0.7.3` (site-packages; requires click, filelock, httpx, rich) |
| profile | `default` — Auth Status **authenticated** |

## 3. Local authentication diagnostics (read-only) — ALL PASS

`notebooklm doctor` (exit 0): Profile `default` (source: default) · Migration ✓ pass · Profile Dir
`! warn` (permissions 0o777, expected 0o700) · **Auth ✓ pass — local SID cookie present (30
cookies)** · Config ✓ pass. "All checks passed."

`notebooklm auth check` (exit 0): Storage exists ✓ · JSON valid ✓ · Cookies present ✓ (30) · SID
cookie ✓ present for the google / notebook domains · **Token fetch ⊘ skipped** ("use --test to
check").

Interpretation: the SESSION STORE is healthy. The failure is downstream of storage.

## 4. THE FAILING OPERATION (the actual transport read)

Command (single invocation — not repeated, per the no-repeat rule):
`notebooklm --quiet list` → **exit code 2**, stderr:
```
Unexpected error: CSRF token not found in HTML. Final URL: https://notebook.google.com/
This may indicate the page structure has changed.
This may be a bug. Please report at https://github.com/teng-lin/notebooklm-py/issues
```

Token-fetch diagnostic `notebooklm auth check --test` (single invocation): local checks still pass,
but **"Error: Token fetch failed: CSRF token not found in HTML. Final URL:
https://notebook.google.com/ — This may indicate the page structure has changed."**, followed by the
generic footer "Cookies may be expired. Run 'notebooklm login' to refresh."

## 5. Cause classification — UI/HTML STRUCTURE DRIFT (by the client's own discrimination)

Installed source `notebooklm/_auth/extraction.py::extract_csrf_from_html` (lines 234–249)
implements an explicit THREE-WAY discrimination before raising:

1. `is_notebooklm_unavailable_redirect(final_url)` → "unavailable / access gate" class;
2. `is_google_auth_redirect(final_url) or contains_google_auth_redirect(html)` →
   **"Authentication expired or invalid. Run 'notebooklm login' to re-authenticate."**;
3. otherwise → **"CSRF token not found in HTML. Final URL: … This may indicate the page structure
   has changed."**

The observed message is **case 3**. By construction that means the landing URL was NOT a Google
auth redirect and the response body did NOT contain an auth redirect — i.e. **the client itself
classifies this as page-structure drift, not as an authentication failure**. The CSRF token is
scraped out of the page's `WIZ_global_data` JavaScript object, which is exactly the kind of surface
that breaks when the page changes.

Honest caveats:
* The `auth check --test` footer suggests a re-login; that footer is generic and is contradicted by
  the more precise in-code discrimination above (case 2 vs case 3).
* A silently-altered page that returns neither an auth redirect nor the expected structure cannot
  be distinguished from "session expired but served a non-auth page" by this probe alone — this is
  recorded as a residual ambiguity, not resolved by assumption.

## 6. Probe coverage against the mandated checks

| Check | Result |
|---|---|
| A. Session + transport diagnostics | **VERIFIED (partially)** — session/storage classes are diagnosable and healthy; the transport read is resolved as drift |
| B. Notebook listing / metadata retrieval | **FAILS** — `list` exits 2; no listing could be obtained (no second attempt made) |
| C. Reading existing source/research metadata without mutation | **NOT VERIFIED** — unreachable while the transport read fails |
| D. Distinguishing success / auth failure / CSRF-UI drift / network failure / unsupported capability | **PARTIAL** — success, auth-redirect, unavailable-gate, storage/JSON/cookie classes ARE distinguished by the client; **network failure and unsupported-capability classes were NOT tested** |
| E. Plausibility for the M6.8 provider adapter | **NOT SUPPORTED TODAY** — the surface cannot perform even a read-only listing |

## 7. Maintained remedy (independently supported by observed upstream data)

`pip index versions notebooklm-py`: INSTALLED **0.7.3** → LATEST **0.8.5** (0.8.0…0.8.5 published
after 0.7.3). Upstream release notes (public GitHub releases API, read-only):
* **v0.8.5 (2026-10-12)** — latest; Python 3.15 support and CI/doc work.
* **v0.8.4 (2026-10-02)** — multi-profile REST/MCP serving.
* **v0.8.3 (2026-09-26)** — "Web vs Android public-behavior inventory".
* **v0.8.2 (2026-09-02)** — headline: the new **Android backend** — "The Python SDK, CLI, MCP
  server, and REST server can now use NotebookLM's native mobile API as an **alternative to the Web
  backend**" (install the `android` extra; select via `backend="android"`, `--backend android`, or
  `NOTEBOOKLM_BACKEND=android`).

So the Web backend's HTML-scraping transport is the component that drifted, and the maintained
client (two days old at the time of this probe) offers BOTH (i) 13 releases of fixes past the
installed version and (ii) a different backend that does not depend on scraping the Web page's
`WIZ_global_data`.

**No official Google API and no Enterprise entitlement was verified, and none is claimed here.**

## 8. Minimal independent remedy + required Founder authorization

1. **Authorize one bounded dependency update** (environment change, explicitly outside this Stage A
   authorization): upgrade `notebooklm-py` 0.7.3 → **0.8.5** in the Hermes venv, and (only if
   needed) install the `android` extra. Then re-run THIS EXACT read-only probe
   (`doctor` → `auth check` → `list`) once.
2. **If, and only if, the upgraded client reports the auth-expired class (case 2)**, an interactive
   `notebooklm login` would be the sanctioned refresh — that requires a Founder action in a real
   browser window. (Local diagnostics indicate the session store is healthy, so this is expected to
   be unnecessary; it is recorded so the next step is unambiguous if it becomes necessary.)
3. No M6.8 implementation should be authorized until a read-only operation actually succeeds —
   building an adapter around a transport that cannot perform even a listing is exactly what the
   Founder prohibited.

## 9. M6.8 trust boundary (carried forward, UNCHANGED and UNTESTED)

`M6.8-TRUST-BOUNDARY-ACCEPTANCE` remains a mandatory acceptance condition
(`evidence/m6.7/TRUST-BOUNDARY-AND-M6.8-ACCEPTANCE-REQUIREMENT-2026-10-14.md`): provider output
must not be able to inject/replace the trusted proof resolver or reach the low-level atomic SUCCESS
writer; SUCCESS flows only through verified proof + `accept_success_result()`; the real provider's
closed-corpus and request-isolation properties must be GENUINELY verifiable; an unverifiable
property fails closed rather than being relabelled VERIFIED. No FD #152/#153 API was changed by
this probe.

## 10. Command inventory (exhaustive — no state-changing command was run)

Read-only, executed: `profile list` · `doctor` · `auth check` · `auth check --test` ·
`--quiet list` (failed) · local `pip index versions` / `pip show` · local source read.
**NOT executed:** `login` · `auth refresh` · `auth logout` · `auth inspect` · `create` · `delete` ·
`rename` · `ask` · `use` · `clear` · any Deep Research launch · any upload or settings change.
