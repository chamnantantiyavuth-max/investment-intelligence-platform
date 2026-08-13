"""Phase -1 diagnosis: Hermes dashboard — is the Kanban tab present?"""
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:9119/?profile=iip", wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(2500)
    print("TITLE:", pg.title())
    # sidebar nav items
    nav = pg.eval_on_selector_all("nav a, aside a, [class*='sidebar'] a, [class*='nav'] a",
        "els => els.map(e => (e.textContent||'').trim()).filter(Boolean)")
    print("NAV ITEMS:", [n for n in nav if n][:40])
    # check any element mentioning kanban
    body_text = pg.evaluate("document.body.innerText")
    print("BODY HAS 'Kanban':", "kanban" in body_text.lower())
    # plugin list via the page's own fetch (token injected by dashboard JS)
    plugins = pg.evaluate("""async () => {
        const t = window.__HERMES_SESSION_TOKEN__ || '';
        const r = await fetch('/api/dashboard/plugins', {headers: t ? {'Authorization': 'Bearer ' + t} : {}});
        return {status: r.status, body: await r.text()};
    }""")
    print("PLUGINS API:", json.dumps(plugins)[:900])
    pg.screenshot(path=r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\phase-minus1-kanban-restore\dashboard-before.png")
    print("CONSOLE ERRORS:", errors[:5])
    b.close()
