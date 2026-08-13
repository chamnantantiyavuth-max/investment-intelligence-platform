"""Phase -1 acceptance: native Kanban tab restored + board renders + agrees with CLI."""
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:9119/?profile=iip", wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(2000)

    # 1. nav contains Kanban
    nav = pg.eval_on_selector_all("nav a, aside a, [class*='sidebar'] a",
        "els => els.map(e => (e.textContent||'').trim()).filter(Boolean)")
    has_kanban = any('kanban' in n.lower() for n in nav)
    print("NAV HAS KANBAN:", has_kanban)
    print("NAV:", [n for n in nav if n][:22])

    # 2. click Kanban link
    clicked = pg.evaluate("""() => {
        const els = [...document.querySelectorAll('nav a, aside a, [class*=\"sidebar\"] a')];
        const el = els.find(e => (e.textContent||'').toLowerCase().includes('kanban'));
        if (el) { el.click(); return true; } return false;
    }""")
    print("CLICKED KANBAN:", clicked)
    pg.wait_for_timeout(3500)
    print("URL AFTER CLICK:", pg.url)
    body = pg.evaluate("document.body.innerText")
    print("BODY HAS 'Capital Intelligence':", 'capital intelligence' in body.lower())

    # 3. board content — columns + cards
    cols = pg.eval_on_selector_all("[class*='column'] h3, [class*='column'] [class*='header']",
        "els => els.map(e => e.textContent.trim()).filter(Boolean)")
    print("COLUMNS SAMPLE:", cols[:14])
    cards = pg.eval_on_selector_all("[class*='card'] [class*='title'], [class*='card'] h4",
        "els => els.map(e => e.textContent.trim()).filter(Boolean)")
    print("CARD TITLES SAMPLE:", [c[:60] for c in cards[:10]])

    # 4. board selector
    sel = pg.evaluate("""() => {
        const sels = [...document.querySelectorAll('select')];
        return sels.map(s => ({options: [...s.options].map(o => o.text), value: s.value}));
    }""")
    print("SELECTS:", json.dumps(sel)[:400])

    pg.screenshot(path=r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\phase-minus1-kanban-restore\dashboard-kanban-after.png", full_page=False)
    print("CONSOLE ERRORS:", errors[:5])
    b.close()
