"""Phase 3 visual smoke — captures state screenshots at multiple viewports + drawer.
Usage: python smoke-3.py [mode]
  mode=full   (default) baseline 1440 + 1920 + drawer
  mode=live   create ACTIVE pair probes, screenshot with line/packet, cleanup
"""
import json, re, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"
mode = sys.argv[1] if len(sys.argv) > 1 else "full"

console_errors = []

def go(browser, viewport, tag, wait_ms=2200, click_desk=None, burst=False):
    page = browser.new_page(viewport=viewport)
    errs = []
    page.on("console", lambda msg: errs.append(f"console[{msg.type}]: {msg.text}") if msg.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)
    page.wait_for_timeout(wait_ms)
    if click_desk:
        try:
            page.click("text=" + click_desk, timeout=8000)
            page.wait_for_timeout(1200)
        except Exception as e:
            print("desk click failed:", e)
    body = page.inner_text("body")
    print(f"[{tag}] URL:", page.url)
    print(f"[{tag}] desks:", len(page.eval_on_selector_all(".co-desk-role", "els => els.map(e => e.textContent.trim())")))
    print(f"[{tag}] lines:", page.locator("line.co-handoff-line").count())
    print(f"[{tag}] summary:", page.eval_on_selector_all(".co-sum-k", "els => els.map(e => e.textContent.trim())"))
    print(f"[{tag}] founder rows:", page.locator(".co-founder-row").count())
    print(f"[{tag}] drawer:", page.locator(".co-drawer").count())
    if burst:
        for i in range(4):
            page.screenshot(path=f"{OUT}\\{tag}-{i}.png")
            page.wait_for_timeout(450)
    else:
        page.screenshot(path=f"{OUT}\\{tag}.png")
        page.screenshot(path=f"{OUT}\\{tag}-full.png", full_page=True)
    page.close()
    return errs

with sync_playwright() as p:
    browser = p.chromium.launch()
    if mode == "full":
        console_errors += go(browser, {"width": 1440, "height": 900}, "p3-1440-clean")
        console_errors += go(browser, {"width": 1920, "height": 1080}, "p3-1920-clean")
        console_errors += go(browser, {"width": 1440, "height": 900}, "p3-drawer-cos", click_desk="Chief of Staff")
    browser.close()

print("CONSOLE ERRORS/WARNINGS:", len(console_errors))
for e in console_errors[:10]:
    print("  ", e[:200])
