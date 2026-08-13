"""Phase 3.1 live bounded verification — R1 reconnect catch-up, R2 auth
fail-closed E2E, R3 drawer profile accuracy. Cleanup after.
"""
import json, sys, time, urllib.request
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9119"
OUT = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform\evidence\ui\live-office-plugin"
REPO = r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform"
sys.path.insert(0, REPO + r"\hermes-plugins\capital-intelligence-office\dashboard")
from hermes_cli import kanban_db  # noqa: E402

WRAP = """
window.__wsRec = { urls: [], sockets: [] };
const _Orig = window.WebSocket;
window.WebSocket = new Proxy(_Orig, {
  construct(t, args) {
    const url = String(args[0]);
    window.__wsRec.urls.push(url);
    const s = new t(...args);
    window.__wsRec.sockets.push(s);
    return s;
  }
});
"""

# --- R1: reconnect catch-up ------------------------------------------------
conn = kanban_db.connect(board="iip")
t_a = kanban_db.create_task(conn, title="[TEST] 3.1 reconnect probe A", assignee="org-data-steward",
    created_by="hermes-verify", initial_status="running", board="iip")
conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (t_a,)); conn.commit(); conn.close()
print("probe A:", t_a)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("console", lambda m: errs.append(f"console[{m.type}]: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    page.add_init_script(WRAP)
    page.goto(BASE + "/capital-office", wait_until="networkidle", timeout=40000)
    page.wait_for_timeout(4500)  # first WS connected + baseline cursor message (2s poll)
    urls0 = page.evaluate("window.__wsRec.urls.slice()")
    print("ws urls so far:", urls0)
    assert len(urls0) >= 1 and "since=" not in urls0[0], "first load must be live-tail (no since)"
    sub_before = page.locator(".co-sub").inner_text()
    print("sub before:", sub_before)
    # disconnect: force-close the socket(s)
    page.evaluate("window.__wsRec.sockets.forEach(function(w){ try { w.close(); } catch(e){} });")
    # mutate while disconnected
    conn = kanban_db.connect(board="iip")
    t_b = kanban_db.create_task(conn, title="[TEST] 3.1 reconnect probe B (gap event)", assignee="org-data-steward",
        created_by="hermes-verify", initial_status="running", board="iip")
    conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (t_b,)); conn.commit(); conn.close()
    print("probe B (created during gap):", t_b)
    page.wait_for_timeout(7000)  # reconnect at ~3s with since + catch-up + refresh
    urls1 = page.evaluate("window.__wsRec.urls.slice()")
    print("ws urls after reconnect:", urls1)
    reconnects = [u for u in urls1[len(urls0):]]
    assert reconnects and all("since=" in u for u in reconnects), \
        "reconnect MUST send ?since=<last cursor>"
    sub_after = page.locator(".co-sub").inner_text()
    print("sub after:", sub_after)
    assert sub_after != sub_before and "created" in sub_after, \
        "WS catch-up must deliver the gap event (lastEvent advanced) — stale otherwise"
    token = page.evaluate("window.__HERMES_SESSION_TOKEN__ || ''")
    req = urllib.request.Request(BASE + "/api/plugins/capital-intelligence-office/desks",
        headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=15) as r:
        desks = json.loads(r.read())["desks"]
    ds = next(d for d in desks if d["profile"] == "org-data-steward")
    diag_ready = (ds.get("diagnostics") or {}).get("ready", 0)
    print("data steward DIAG ready after catch-up:", diag_ready)
    assert diag_ready >= 2, "B must reconcile (A + B both in DIAG) without a future event"
    page.screenshot(path=f"{OUT}\\p31-reconnect-catchup.png")
    browser.close()

print("CONSOLE (R1 phase):", len(errs))
for e in errs[:6]:
    print("  ", e[:150])

# --- R2: auth fail-closed E2E (missing + invalid credential) ----------------
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "/capital-office", wait_until="domcontentloaded", timeout=30000)
    res = page.evaluate("""async () => {
      function tryWs(url) {
        return new Promise(function (resolve) {
          var ws = new WebSocket(url);
          ws.onopen = function () { resolve({ stage: "open" }); };
          ws.onclose = function (e) { resolve({ stage: "close", code: e.code }); };
          ws.onerror = function () { resolve({ stage: "error" }); };
          setTimeout(function () { resolve({ stage: "timeout" }); }, 7000);
        });
      }
      var base = (location.protocol === "https:" ? "wss://" : "ws://") + location.host
        + "/api/plugins/capital-intelligence-office/events";
      var noToken = await tryWs(base);
      var badToken = await tryWs(base + "?token=definitely-invalid-token-12345");
      return { noToken: noToken, badToken: badToken };
    }""")
    print("R2 E2E:", json.dumps(res))
    for key in ("noToken", "badToken"):
        r = res[key]
        assert r["stage"] in ("close", "error"), f"{key} must be REJECTED (got {r})"
    browser.close()

# --- R3: drawer profile accuracy E2E (filter before limit on live board) ----
conn = kanban_db.connect(board="iip")
t_c = kanban_db.create_task(conn, title="[TEST] 3.1 drawer target (older)", assignee="org-cro",
    created_by="hermes-verify", initial_status="running", board="iip")
conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (t_c,)); conn.commit()
t_d = kanban_db.create_task(conn, title="[TEST] 3.1 drawer noise (newer)", assignee="org-cos",
    created_by="hermes-verify", initial_status="running", parents=[], board="iip")
conn.execute("UPDATE tasks SET status='todo' WHERE id=?", (t_d,)); conn.commit(); conn.close()
print("R3 probes:", t_c, "(target, older)", t_d, "(noise, newer)")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "/capital-office", wait_until="domcontentloaded", timeout=30000)
    token = page.evaluate("window.__HERMES_SESSION_TOKEN__ || ''")
    browser.close()
req = urllib.request.Request(BASE + "/api/plugins/capital-intelligence-office/activity?profile=org-cro&limit=8",
    headers={"Authorization": "Bearer " + token})
with urllib.request.urlopen(req, timeout=15) as r:
    items = json.loads(r.read())["items"]
print("org-cro drawer items:", [it["task_id"] for it in items])
assert any(it["task_id"] == t_c for it in items), \
    "target profile event must be returned despite newer noise (R3 filter-before-limit)"

# --- cleanup ----------------------------------------------------------------
conn = kanban_db.connect(board="iip")
for tid in (t_a, t_b, t_c, t_d):
    try:
        kanban_db.archive_task(conn, tid)
        print("archived", tid)
    except Exception as e:
        print("archive fail", tid, e)
conn.close()
print("cleanup done")
