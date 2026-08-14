#!/usr/bin/env python3
"""IIP FREE-MODEL PREFLIGHT (PROPOSED — not installed, not wired to production).

Purpose (Gap 5 / billing guard): prevent silent paid routing on :free typos.
OpenRouter silently drops unknown :suffix and routes to the PAID base model
(verified 2026-08-14: nvidia/nemotron-3-ultra-550b-a55b:does-not-exist
returned HTTP 200 on the paid base with real cost). This preflight blocks
that class of mistake at startup/config-validation time.

Design:
  1. expected slug  -> OpenRouter GET /api/v1/models -> EXACT match must exist
     (no substring, no normalization). Missing = BLOCK (exit 2).
  2. Optional bounded first-call probe: 1-token ping via the slug; the
     returned usage.cost MUST be 0 and returned model id MUST equal the slug.
     cost != 0 or different model id = ALERT (exit 3).
  3. ZDR gate (optional, --require-zdr): re-probe with extra_body
     provider {data_collection: deny, zdr: true, require_parameters: true};
     failure = mark slot PAID-ONLY (per Founder rule, not an error here).

Usage:
  python free_model_preflight.py --slug nvidia/nemotron-3-ultra-550b-a55b:free [--probe] [--require-zdr]
  python free_model_preflight.py --file expected_slugs.txt [--probe] [--require-zdr]

Exit codes: 0 = ok, 1 = config error, 2 = slug not found (BLOCK), 3 = paid-routing detected (ALERT), 4 = ZDR route unavailable.
"""
import argparse, json, os, re, sys, urllib.request, urllib.error
from pathlib import Path

API = "https://openrouter.ai/api/v1/models"
CHAT = "https://openrouter.ai/api/v1/chat/completions"

def load_key():
    k = os.environ.get("OPENROUTER_API_KEY", "")
    if not k:
        env = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "profiles" / "iip" / ".env"
        if env.exists():
            m = re.search(r'^\s*OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\s]+)', env.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m: k = m.group(1)
    return k

def get_models():
    req = urllib.request.Request(API)
    with urllib.request.urlopen(req, timeout=60) as r:
        return {m["id"] for m in json.loads(r.read().decode())["data"]}

def ping(slug, key, zdr=False, timeout=90):
    body = {"model": slug, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1}
    if zdr:
        body["extra_body"] = {"provider": {"data_collection": "deny", "zdr": True, "require_parameters": True}}
    req = urllib.request.Request(CHAT, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode())
        if "error" in d:
            return {"ok": False, "err": f"upstream error: {d['error'].get('message','')[:120]}", "code": d["error"].get("code")}
        return {"ok": True, "model": d.get("model"), "cost": d.get("usage", {}).get("cost")}
    except urllib.error.HTTPError as e:
        return {"ok": False, "err": e.read().decode(errors="ignore")[:200], "code": e.code}
    except Exception as e:
        return {"ok": False, "err": str(e)[:150]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug"); ap.add_argument("--file")
    ap.add_argument("--probe", action="store_true"); ap.add_argument("--require-zdr", action="store_true")
    a = ap.parse_args()
    if not a.slug and not a.file:
        print("need --slug or --file"); return 1
    slugs = [a.slug] if a.slug else [l.strip() for l in Path(a.file).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    key = load_key()
    if a.probe and not key:
        print("OPENROUTER_API_KEY required for --probe"); return 1
    models = get_models()
    rc = 0
    for s in slugs:
        exact = s in models
        print(f"[{'OK ' if exact else 'BLOCK'}] slug {s} — exact match: {exact}")
        if not exact:
            rc = max(rc, 2); continue
        if a.probe:
            p = ping(s, key)
            if not p["ok"]:
                print(f"  probe FAIL: {p.get('err')}"); rc = max(rc, 3); continue
            paid = (p.get("cost") or 0) != 0 or p.get("model") != s
            print(f"  probe: returned_model={p.get('model')} cost={p.get('cost')} {'PAID-ROUTING ALERT' if paid else 'free-confirmed'}")
            if paid: rc = max(rc, 3)
        if a.require_zdr:
            z = ping(s, key, zdr=True)
            if z["ok"] and (z.get("cost") or 0) == 0:
                print(f"  ZDR route: OK (cost={z.get('cost')})")
            else:
                print(f"  ZDR route: UNAVAILABLE ({z.get('err')}) -> slot PAID-ONLY per IIP rule")
                rc = max(rc, 4)
    print(f"PREFLIGHT EXIT {rc}")
    return rc

if __name__ == "__main__":
    sys.exit(main())
