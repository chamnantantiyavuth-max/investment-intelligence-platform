"""Phase 3 live scenarios v2 — bounded synthetic verification (checkpoint 3 & 5).

A) ACTIVE handoff + packet: parent created BEFORE page load; child created
   WHILE page open -> WS 'created' event -> line + packet pulse (burst shots).
B) Working: real worker via `hermes kanban --board iip dispatch` (correct arg
   order) on a bounded sleep goal task -> WORKING desk shot + drawer.
Cleanup: archive all probes + unlink.
"""
import subprocess, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"
REPO = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform"
sys.path.insert(0, REPO + r"\hermes-plugins\capital-intelligence-office\dashboard")
from hermes_cli import kanban_db  # noqa: E402

conn = kanban_db.connect(board="iip")

def mk(title, assignee, status, parents=(), body=None, goal=False):
    tid = kanban_db.create_task(conn, title=title, assignee=assignee,
        created_by="hermes-verify", initial_status="running",
        parents=parents, board="iip", body=body, goal_mode=goal)
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, tid))
    return tid

# --- A) ACTIVE handoff ----------------------------------------------------
pa = mk("[TEST] P3 handoff parent — active probe", "org-quant-validator", "todo")
print("parent:", pa)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("console", lambda m: errs.append(f"console[{m.type}]: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)
    page.wait_for_timeout(2500)
    before = page.locator("line.co-handoff-line").count()
    print("lines before child:", before)

    # create child WHILE page open -> WS created event -> pulse
    ca = mk("[TEST] P3 handoff child — active probe", "org-data-steward", "todo", parents=[pa])
    print("child:", ca)
    page.wait_for_timeout(600)  # let WS deliver + refresh + line draw
    after = page.locator("line.co-handoff-line").count()
    classes = page.eval_on_selector_all("line.co-handoff-line",
        "els => els.map(e => e.getAttribute('class'))")
    print("lines after child:", after, classes)

    for i in range(8):  # burst to catch the 3s packet window
        page.screenshot(path=f"{OUT}\\p3-active-handoff-{i}.png")
        page.wait_for_timeout(350)
    browser.close()

print("CONSOLE (handoff phase):", len(errs))
for e in errs[:6]:
    print("  ", e[:160])

# --- B) Working state via real bounded worker ---------------------------
conn = kanban_db.connect(board="iip")
wt = mk("[TEST] P3 working probe — bounded sleep", "org-equity-analyst", "running",
        body="Run: python -c \"import time; time.sleep(45)\" and then reply with exactly: probe done.",
        goal=True)
conn.close()
print("working task:", wt)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("console", lambda m: errs.append(f"console[{m.type}]: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)

    proc = subprocess.Popen(
        ["hermes", "kanban", "--board", "iip", "dispatch", "--max", "1"],
        cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    state = None
    for _ in range(40):
        page.wait_for_timeout(2000)
        roles = page.eval_on_selector_all(".co-desk-role", "els => els.map(e => e.textContent.trim())")
        badges = page.eval_on_selector_all(".co-desk-badge", "els => els.map(e => e.textContent.trim())")
        idx = roles.index("Equity Alpha Analyst") if "Equity Alpha Analyst" in roles else -1
        state = badges[idx] if 0 <= idx < len(badges) else state
        if state == "Working":
            break
    print("equity desk state while worker runs:", state)
    page.screenshot(path=f"{OUT}\\p3-working.png")
    page.screenshot(path=f"{OUT}\\p3-working-full.png", full_page=True)
    try:
        page.click("text=Equity Alpha Analyst", timeout=5000)
        page.wait_for_timeout(1200)
        page.screenshot(path=f"{OUT}\\p3-working-drawer.png")
    except Exception as e:
        print("drawer click:", e)
    # wait for the run to finish -> recently_completed example
    state2 = state
    for _ in range(30):
        page.wait_for_timeout(3000)
        roles = page.eval_on_selector_all(".co-desk-role", "els => els.map(e => e.textContent.trim())")
        badges = page.eval_on_selector_all(".co-desk-badge", "els => els.map(e => e.textContent.trim())")
        idx = roles.index("Equity Alpha Analyst") if "Equity Alpha Analyst" in roles else -1
        state2 = badges[idx] if 0 <= idx < len(badges) else state2
        if state2 != "Working":
            break
    print("equity desk state after worker:", state2)
    page.screenshot(path=f"{OUT}\\p3-working-after.png")
    browser.close()

print("CONSOLE (working phase):", len(errs))
for e in errs[:6]:
    print("  ", e[:160])

# --- cleanup --------------------------------------------------------------
conn = kanban_db.connect(board="iip")
for tid in (pa, ca, wt):
    try:
        kanban_db.archive_task(conn, tid)
        print("archived", tid)
    except Exception as e:
        print("archive fail", tid, e)
conn.execute("DELETE FROM task_links WHERE parent_id=? AND child_id=?", (pa, ca))
conn.commit()
conn.close()
print("cleanup done")
