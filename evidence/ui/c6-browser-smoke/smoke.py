"""C6 browser smoke — /kanban + /org-office via Playwright (real browser render).
Headless chromium (playwright) — no interactive Chrome popup needed.
"""
import json, re
from playwright.sync_api import sync_playwright

REPO = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform"
BASE = "http://localhost:5173"

# local test creds (gitignored)
creds = {}
with open(REPO + r"\.env", encoding="utf-8") as f:
    for line in f:
        m = re.match(r"\s*(IIP_AUTH_USER|IIP_AUTH_PASSWORD)\s*=\s*(.+)", line.strip())
        if m:
            creds[m.group(1)] = m.group(2).strip().strip('"').strip("'")
user = creds.get("IIP_AUTH_USER", "founder")
pw = creds.get("IIP_AUTH_PASSWORD", "")

console_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", lambda msg: console_errors.append(f"console[{msg.type}]: {msg.text}") if msg.type in ("error", "warning") else None)
    page.on("pageerror", lambda err: console_errors.append(f"pageerror: {err}"))

    # login
    page.goto(BASE + "/login", wait_until="networkidle")
    page.fill("#username", user)
    page.fill("#password", pw)
    page.click("form button[type=submit]")
    page.wait_for_load_state("networkidle")
    print("LOGIN → path:", page.url.replace(BASE, ""))

    # --- /kanban ---
    page.goto(BASE + "/kanban", wait_until="networkidle")
    page.wait_for_timeout(1200)
    h1 = page.locator("h1").first.text_content()
    # native column headers = <p> labels where textContent = label+count (e.g. "Triage2")
    cols = page.eval_on_selector_all(
        "p", "els => els.map(e => e.textContent.trim()).filter(t => /^(Triage|Todo|Scheduled|Ready|Running|Blocked|Review|Done|Archived)\\d*$/.test(t)).map(t => t.replace(/\\d+$/, ''))"
    )
    # board card titles (GATE / MIGRATED / RADAR)
    titles = page.eval_on_selector_all(
        "p", "els => els.map(e => e.textContent).filter(t => t.includes('[GATE]') || t.includes('[MIGRATED]') || t.includes('[RADAR][INBOX]')).slice(0, 8)"
    )
    print("KANBAN H1:", h1)
    print("KANBAN COLUMNS:", sorted(set(cols)))
    print("KANBAN GATE/MIGRATED/RADAR titles:", titles)
    page.screenshot(path=REPO + r"\evidence\ui\c6-browser-smoke\kanban.png")
    print("KANBAN screenshot saved")

    # --- /org-office ---
    page.goto(BASE + "/org-office", wait_until="networkidle")
    page.wait_for_timeout(1200)
    h1b = page.locator("h1").first.text_content()
    body_text = page.inner_text("body")
    print("ORG-OFFICE H1:", h1b)
    print("ORG-OFFICE has 'Active holds':", "Active holds" in body_text)
    print("ORG-OFFICE has 'No active holds':", "No active holds" in body_text)
    print("ORG-OFFICE mentions Blocked:", "Blocked" in body_text)
    page.screenshot(path=REPO + r"\evidence\ui\c6-browser-smoke\org-office.png")
    print("ORG-OFFICE screenshot saved")

    browser.close()

print("CONSOLE ERRORS/WARNINGS:", len(console_errors))
for e in console_errors[:10]:
    print("  ", e[:160])
