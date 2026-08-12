---
name: notebooklm-deep-research
description: Use when running NotebookLM Deep Research via browser.
version: 1.0.0
author: Chamnan + Hermes Agent
---

# NotebookLM Deep Research — Browser/CDP Transport

Production architecture (FD #105, Stage 6.6): **PRIMARY DR transport = Gemini NotebookLM PRO via authenticated browser** (subscription, quota 20/day on PRO); **FALLBACK = Google AI Studio API** (`deep-research-max-preview-04-2026` via Interactions API, `GOOGLE_API_KEY`). The v1.4 analytical workflow (frozen prompt → isolated lane → freeze → provenance → reconciliation) is transport-agnostic — the browser path replaces ONLY the transport.

## Setup (one-time)

1. **Dedicated Chrome profile** for Hermes automation — keeps remote-debugging control away from the personal browser:
   - `mkdir -p "$LOCALAPPDATA/hermes-profiles/chrome-iip"`
   - Launch via terminal `background=true` (NOT `&`):
     `"C:/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222 --user-data-dir="$LOCALAPPDATA/hermes-profiles/chrome-iip" --no-first-run --no-default-browser-check "https://notebooklm.google.com/"`
2. **Founder login** (human step): the user signs into Google with the NotebookLM PRO account in that profile. Cannot be automated.
3. Verify: `curl -s http://127.0.0.1:9222/json/version` → Browser version + webSocketDebuggerUrl; `curl -s http://127.0.0.1:9222/json` → list tabs.

## Connect

- Preferred: `browser_exec` (Browser Use CLI) — connects to the CDP-enabled Chrome.
- **Pitfall: browser_exec stdout can return empty after attaching to an externally-launched CDP Chrome** (`{"success": true, "output": null}` every call). The browser works fine; only stdout is lost. **Fall back to raw CDP** (proven pattern):
  - Python `websockets` (available in the hermes venv) → connect `page["webSocketDebuggerUrl"]` from `/json`, send `Runtime.evaluate` with `{"id": N, "method": "Runtime.evaluate", "params": {"expression": ..., "returnByValue": true, "awaitPromise": true}}`, loop `recv()` until `r.get("id") == N`.
  - `curl -s http://127.0.0.1:9222/json` to find the `notebook` tab by URL.
- **Pitfall: keep browser_exec code ASCII-only.** Non-ASCII in the code string (e.g. an em-dash in a comment) → `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x97` on Windows stdin. No non-ASCII characters in browser_exec code.
- Remote-debugging approval: first attach asks the human to tick "Allow remote debugging for this browser instance" in `chrome://inspect`; one more Allow popup appears on each connection (expected, not a re-ask). Launching Chrome directly with `--remote-debugging-port` (per Setup) bypasses the chrome://inspect flow.

## NotebookLM Deep Research UI flow (proven 13 Aug 2026)

1. `notebooklm.google.com` → **Create new** notebook.
2. Sources panel → **Web** dropdown → choose **Deep Research** (option list shows `Fast Research — Great for quick results` / `Deep Research — In-depth report`). Fast Research is the other mode; Deep Research is the subscription feature.
3. DR panel textarea with placeholder "What would you like to research?" (`aria-label` contains "Discover sources"). Set value via the native setter + dispatch `input` + `change` events (React-controlled input):
   ```js
   const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
   setter.call(ta, PROMPT);
   ta.dispatchEvent(new Event('input', {bubbles: true}));
   ta.dispatchEvent(new Event('change', {bubbles: true}));
   ```
4. Click the enabled `button[aria-label="Submit"]` (there may be two — use the enabled one in the DR panel; the top one is disabled until a query exists).
5. Progress: **"Step X/5"** indicator + stop button. Steps complete in sequence; source discovery (Step 2) can take several minutes.
6. Completion banner: **"Deep Research completed!"** + report title + "N sources discovered" + **View** button.
7. Click **View** → report opens with full text; sources list at the bottom (collapsible; "Hide sources" shows URLs with arrow_outward links).

## Capture + provenance (mandatory pattern — reuse from S4/Stage 6)

1. **Prompt frozen before submit**: record SHA-256 of the exact prompt + dispatch timestamp.
2. **Capture full text**: scroll loop until stable — repeatedly set `sc.scrollTop = sc.scrollHeight` (main/chat container or `document.scrollingElement`), sleep ~1.5s, read `document.body.innerText`; stop when length stops growing (lazy rendering).
3. Save RAW → `sha256sum` → copy FROZEN (identical).
4. Provenance JSON: transport, prompt SHA, started/completed (UTC+7), report title, sources count, raw char count, raw SHA.
5. **Anti-anchoring**: the DR view is an isolated lane — freeze before ANY Hermes analysis; reconciliation only after all first passes frozen (Stage 6 S5 pattern).

## Quota (Google Help, cited 2026-08-13; limits may change)

NotebookLM Deep Research: Standard 10/month · Plus 3/day · **PRO 20/day** · Ultra higher. Budget DR runs against the tier.

## Fallback

API path (unchanged, proven Stage 6): `google.genai` client → Interactions API background job `deep-research-max-preview-04-2026`; job IDs + provenance captured the same way. Use only when the browser/subscription path genuinely fails.

## Pitfalls recap

- browser_exec stdout empty after CDP attach → use raw CDP websocket (python `websockets`).
- Non-ASCII in browser_exec code → UnicodeDecodeError on Windows.
- Lazy content → must scroll-loop before capture; single innerText read truncates the report.
- Two Submit buttons → click the enabled one.
- Report opens in the same tab (View) — re-find the notebook tab by URL after navigation.
- Founder login is a human step — never attempt to guess credentials.
