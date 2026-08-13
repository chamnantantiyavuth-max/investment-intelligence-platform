"""Phase 2.1 browser smoke — Hermes dashboard Capital Office (Playwright headless).

Verifies: plugin nav present, 11 desks rendered, founder gates intact,
handoff lines area honest (no stale lines), history toggle present,
no console errors, screenshot for visual QA.
"""
import re
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"

console_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", lambda msg: console_errors.append(f"console[{msg.type}]: {msg.text}") if msg.type in ("error", "warning") else None)
    page.on("pageerror", lambda err: console_errors.append(f"pageerror: {err}"))

    page.goto(BASE + "/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1500)
    print("TITLE:", page.title())
    nav = page.eval_on_selector_all("nav a, aside a, header a",
        "els => els.map(e => e.textContent.trim()).filter(t => t)")
    print("NAV items:", nav)

    # click Capital Office nav item
    try:
        page.click("text=Capital Office", timeout=8000)
        page.wait_for_timeout(2500)
    except Exception as e:
        print("NAV CLICK failed:", e)
        page.goto(BASE + "/capital-intelligence-office", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2500)

    body = page.inner_text("body")
    print("URL:", page.url)
    print("has LIVE:", "LIVE" in body)
    print("has FOUNDER DESK:", "FOUNDER DESK" in body)
    # 11 desks
    desks = page.eval_on_selector_all("[class*=co-desk-role], .co-desk-role",
        "els => els.map(e => e.textContent.trim())")
    print("desk roles (%d):" % len(desks), desks)
    # handoff lines drawn (SVG line elements)
    lines = page.eval_on_selector_all("line.co-handoff-line",
        "els => els.map(e => e.getAttribute('class'))")
    print("handoff line elements:", len(lines), "| classes:", lines[:8])
    # history toggle
    hist = page.eval_on_selector_all(".co-rail-history",
        "els => els.map(e => e.textContent.trim())")
    print("history toggle:", hist)
    # founder decision rows
    frows = page.eval_on_selector_all(".co-founder-row",
        "els => els.map(e => e.textContent.trim())")
    print("founder rows (%d):" % len(frows), [r[:60] for r in frows])

    page.screenshot(path=OUT + r"\phase2.1-semantic-hardening-1440x900.png")
    print("screenshot saved")

    # state agreement sanity: desk badges
    badges = page.eval_on_selector_all(".co-desk-badge",
        "els => els.map(e => e.textContent.trim())")
    print("desk badges:", badges)

    browser.close()

print("CONSOLE ERRORS/WARNINGS:", len(console_errors))
for e in console_errors[:10]:
    print("  ", e[:200])
