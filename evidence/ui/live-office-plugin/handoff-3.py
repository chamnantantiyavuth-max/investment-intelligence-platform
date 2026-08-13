"""Phase 3 ACTIVE handoff + packet capture (checkpoint 5).

Parent created before page load; child created WHILE page open -> WS 'created'
event -> refresh draws the ACTIVE line + 3s packet pulse -> burst screenshots.
Cleanup: archive both + unlink.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"
REPO = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform"
sys.path.insert(0, REPO + r"\hermes-plugins\capital-intelligence-office\dashboard")
from hermes_cli import kanban_db  # noqa: E402

conn = kanban_db.connect(board="iip")
pa = kanban_db.create_task(conn, title="[TEST] P3 handoff parent — active probe",
    assignee="org-cos", created_by="hermes-verify",
    initial_status="running", board="iip")
conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (pa,))
conn.commit()
conn.close()
print("parent:", pa)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("console", lambda m: errs.append(f"console[{m.type}]: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.on("response", lambda r: errs.append(f"HTTP{r.status}: {r.url[:140]}") if r.status >= 400 else None)
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)
    page.wait_for_timeout(2500)
    print("lines before child:", page.locator("line.co-handoff-line").count())

    conn = kanban_db.connect(board="iip")
    ca = kanban_db.create_task(conn, title="[TEST] P3 handoff child — active probe",
        assignee="org-quant-validator", created_by="hermes-verify",
        initial_status="running", parents=[pa], board="iip")
    conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (ca,))
    conn.commit()
    conn.close()
    print("child:", ca)

    # burst IMMEDIATELY — pulse fires within the 2s WS poll and lasts 3s
    page.wait_for_timeout(1200)
    for i in range(12):
        page.screenshot(path=f"{OUT}\\p3-active-handoff-{i}.png")
        page.wait_for_timeout(350)
    page.wait_for_timeout(1000)
    lines = page.locator("line.co-handoff-line").count()
    classes = page.eval_on_selector_all("line.co-handoff-line",
        "els => els.map(e => e.getAttribute('class'))")
    print("lines after child:", lines, classes)
    print("packet present:", page.locator(".co-handoff-packet").count())
    browser.close()

print("CONSOLE:", len(errs))
for e in errs[:6]:
    print("  ", e[:160])

conn = kanban_db.connect(board="iip")
for tid in (pa, ca):
    try:
        kanban_db.archive_task(conn, tid)
        print("archived", tid)
    except Exception as e:
        print("archive fail", tid, e)
conn.execute("DELETE FROM task_links WHERE parent_id=? AND child_id=?", (pa, ca))
conn.commit()
conn.close()
print("cleanup done")
