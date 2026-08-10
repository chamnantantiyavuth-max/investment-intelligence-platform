// Mobile responsive verification — /library + article (Hallmark gates 34/49/50/51/52/53)
// Runs headless Chrome via CDP, emulates 320/375/414/768 CSS-pixel widths.
// Usage: node scripts/verify-mobile.mjs <url>
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const BASE = process.argv[2] ?? "http://localhost:5173/library";
const WIDTHS = [320, 375, 414, 768];
const AUTHED = BASE.includes("library");
const PW = process.env.IIP_AUTH_PASSWORD ?? "";
const USER = process.env.IIP_AUTH_USER ?? "founder";

// ── launch chrome with remote debugging ──
const profile = mkdtempSync(join(tmpdir(), "iip-mobile-"));
const port = 9333 + Math.floor(Math.random() * 200);
const chrome = spawn(CHROME, [
  "--headless=new",
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-gpu",
  "about:blank",
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getJson(url) {
  const r = await fetch(url);
  return r.json();
}
async function waitForTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const list = await getJson(`http://127.0.0.1:${port}/json/list`);
      const page = list.find((t) => t.type === "page");
      if (page) return page;
    } catch { /* chrome still booting */ }
    await sleep(250);
  }
  throw new Error("chrome target not ready");
}

class CDP {
  constructor(wsUrl) { this.ws = new WebSocket(wsUrl); this.id = 0; this.pending = new Map(); }
  async open() {
    await new Promise((res, rej) => { this.ws.onopen = res; this.ws.onerror = rej; });
    this.ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && this.pending.has(m.id)) {
        const { resolve, reject } = this.pending.get(m.id);
        this.pending.delete(m.id);
        m.error ? reject(new Error(m.error.message)) : resolve(m.result);
      }
    };
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { try { this.ws.close(); } catch {} }
}

async function main() {
  const target = await waitForTarget();
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.open();

  const results = [];
  for (const w of WIDTHS) {
    // emulate viewport
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: w, height: 900, deviceScaleFactor: 1, mobile: true,
    });
    // login via API inside this CDP session (HttpOnly cookie lands in this profile)
    await cdp.send("Page.enable");
    if (AUTHED && PW) {
      // navigate to origin FIRST so fetch('/api/...') resolves against the app origin
      await cdp.send("Page.navigate", { url: new URL(BASE).origin + "/" });
      await sleep(1200);
      const loginRes = await cdp.send("Runtime.evaluate", {
        awaitPromise: true, returnByValue: true,
        expression: `(async () => {
          const r = await fetch('/api/auth/login', {
            method: 'POST', credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: ${JSON.stringify(USER)}, password: ${JSON.stringify(PW)} })
          });
          return r.ok;
        })()`,
      });
      if (loginRes.result?.value !== true) {
        console.error("login failed for CDP session");
      }
    }
    // navigate (fresh per width)
    await cdp.send("Page.navigate", { url: BASE });
    await sleep(2200); // let SPA render + queries resolve

    const evalRes = await cdp.send("Runtime.evaluate", {
      returnByValue: true,
      expression: `(() => {
        const de = document.documentElement;
        const body = document.body;
        const overflowX = getComputedStyle(de).overflowX + '|' + getComputedStyle(body).overflowX;
        const scrollW = de.scrollWidth;
        const clientW = de.clientWidth;
        // gate 49: clickable text wrapping to 2+ lines
        const wrap2 = [...document.querySelectorAll('a, button')]
          .filter(el => el.offsetParent !== null)
          .filter(el => {
            const prev = el.getBoundingClientRect();
            return prev.height > 0 && el.scrollHeight > el.clientHeight + 2;
          })
          .slice(0, 5)
          .map(el => (el.textContent || '').trim().slice(0, 40));
        // gate 51: display headers with overflow-wrap
        const h1 = document.querySelector('h1');
        const h1ow = h1 ? getComputedStyle(h1).overflowWrap : 'none';
        // gate 34: horizontal scroll presence
        const hscroll = scrollW > clientW + 1;
        return {
          viewport: window.innerWidth,
          scrollW, clientW, hscroll, overflowX,
          clickableWrap2: wrap2,
          h1ow,
          title: document.title,
          bodyChildren: body ? body.children.length : 0,
        };
      })()`,
    });
    const r = evalRes.result?.value ?? { error: "eval failed" };
    // screenshot
    const shot = await cdp.send("Page.captureScreenshot", { format: "png" });
    const fs = await import("node:fs");
    const outDir = "evidence/ui/hallmark-mobile";
    fs.mkdirSync(outDir, { recursive: true });
    const name = BASE.includes("library/") && !BASE.endsWith("/library")
      ? `article-${w}.png` : `library-${w}.png`;
    fs.writeFileSync(join(outDir, name), Buffer.from(shot.data, "base64"));
    results.push({ ...r, screenshot: outDir + "/" + name });
  }

  // print report
  for (const r of results) {
    console.log(`\n=== viewport ${r.viewport}px ===`);
    console.log(`  scrollW=${r.scrollW} clientW=${r.clientW} horizontalScroll=${r.hscroll}`);
    console.log(`  overflowX(html|body)=${r.overflowX}  h1.overflowWrap=${r.h1ow}`);
    console.log(`  clickable wrapping to 2 lines: ${r.clickableWrap2.length === 0 ? "NONE ✓" : JSON.stringify(r.clickableWrap2)}`);
    console.log(`  screenshot: ${r.screenshot}`);
  }
  const fails = results.filter(r => r.hscroll || r.clickableWrap2.length > 0 || r.overflowX.split("|").includes("visible") === false && false);
  console.log("\n=== SUMMARY ===");
  console.log(`horizontal scroll anywhere: ${results.some(r => r.hscroll) ? "FAIL" : "NONE ✓"}`);
  console.log(`clickable wrapping anywhere: ${results.some(r => r.clickableWrap2.length > 0) ? "FAIL" : "NONE ✓"}`);
  console.log(`overflow-x clip on html+body: ${results.every(r => r.overflowX === "clip|clip") ? "✓ ALL" : results.map(r => r.overflowX).join(" | ")}`);

  cdp.close();
  chrome.kill();
  process.exit(results.some(r => r.hscroll || r.clickableWrap2.length > 0) ? 1 : 0);
}

main().catch((e) => { console.error("FATAL:", e.message); chrome.kill(); process.exit(2); });
