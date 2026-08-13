"""Phase 3 Working-state capture — canonical CLI path (checkpoint 3).

Create via `hermes kanban create` (canonical claim bookkeeping) -> dispatch
real worker -> poll desks API -> screenshot Working + drawer -> wait for
completion -> recently-completed shot -> archive.
"""
import json, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"
REPO = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform"
sys.path.insert(0, REPO + r"\hermes-plugins\capital-intelligence-office\dashboard")
from hermes_cli import kanban_db  # noqa: E402

# 1) canonical create via CLI — REAL bounded verification run (not [TEST]):
#    [TEST] tasks are diagnostics by design (H2/S3) and can never drive desk
#    state — so the Working-state example uses one genuine verification task
#    on an idle desk; archived afterward (zero residue).
r = subprocess.run(
    ["hermes", "kanban", "--board", "iip", "create",
     "[VERIFY] Live Office Working-state display check",
     "--assignee", "org-options-strategist",
     "--initial-status", "running",
     "--goal",
     "--body", "Run: python -c \"import time; time.sleep(45)\" and then reply with exactly: verify done.",
     "--json"],
    capture_output=True, text=True, cwd=REPO)
print("create rc:", r.returncode)
task = json.loads(r.stdout) if r.stdout.strip() else {}
tid = task.get("id") or task.get("task_id") or ""
print("task:", tid, (r.stderr or "")[:200])

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("console", lambda m: errs.append(f"console[{m.type}]: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)
    token = page.evaluate("window.__HERMES_SESSION_TOKEN__ || ''")

    # 2) dispatch real worker (canonical arg order)
    with open(OUT + r"\dispatch.log", "w") as f:
        proc = subprocess.Popen(
            ["hermes", "kanban", "--board", "iip", "dispatch", "--max", "1"],
            cwd=REPO, stdout=f, stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def desks_api():
        req = urllib.request.Request(BASE + "/api/plugins/capital-intelligence-office/desks",
            headers={"Authorization": "Bearer " + token})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())

    # 3) poll desks API for Working (fast feedback)
    state = None
    profile_target = "org-options-strategist"
    for _ in range(45):
        time.sleep(2)
        try:
            d = desks_api()
            for desk in d.get("desks", []):
                if desk["profile"] == profile_target:
                    state = desk["state"]
        except Exception as e:
            print("api poll err:", e)
        if state == "working":
            break
    print("options desk state (API):", state)
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}\\p3-working.png")
    page.screenshot(path=f"{OUT}\\p3-working-full.png", full_page=True)
    try:
        page.click("text=Options Strategist", timeout=5000)
        page.wait_for_timeout(1200)
        page.screenshot(path=f"{OUT}\\p3-working-drawer.png")
    except Exception as e:
        print("drawer click:", e)

    # 4) wait for completion -> recently_completed
    state2 = state
    for _ in range(40):
        time.sleep(3)
        try:
            d = desks_api()
            for desk in d.get("desks", []):
                if desk["profile"] == profile_target:
                    state2 = desk["state"]
        except Exception:
            pass
        if state2 != "working":
            break
    print("options desk state after worker:", state2)
    page.wait_for_timeout(800)
    page.screenshot(path=f"{OUT}\\p3-working-after.png")
    browser.close()

print("CONSOLE:", len(errs))
for e in errs[:6]:
    print("  ", e[:160])

# 5) archive the probe
conn = kanban_db.connect(board="iip")
kanban_db.archive_task(conn, tid)
conn.close()
print("archived", tid)
