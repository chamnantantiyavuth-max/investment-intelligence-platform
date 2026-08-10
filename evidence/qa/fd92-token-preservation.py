#!/usr/bin/env python3
"""FD #92 verification: every numeric/accession/date token in the English original
(git HEAD) must survive in the Thai rewrite. Prints per-file missing tokens."""
import re, subprocess, sys, glob, os

os.chdir(r"C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform")
files = sorted(glob.glob("reports/*.md"))
files = [f for f in files if not f.endswith("README.md")]
TOKEN = re.compile(r"\d[\d,\.]*(?::\d[\d,\.]*)?")
total_orig = total_missing = 0
fails = []
BASE = "6502b79"  # session-start commit = English originals
for f in files:
    orig = subprocess.run(["git", "show", f"{BASE}:{f.replace(os.sep, '/')}"], capture_output=True, text=True).stdout
    if not orig.strip():
        print(f"[SKIP] {os.path.basename(f)} — original not found at {BASE}")
        continue
    cur = open(f, encoding="utf-8").read()
    tokens = TOKEN.findall(orig)
    missing = sorted({t.rstrip(".,") for t in tokens if t.rstrip(".,") not in cur})
    total_orig += len(tokens)
    total_missing += len(missing)
    status = "OK " if not missing else "MISS"
    print(f"[{status}] {os.path.basename(f):55s} orig={len(tokens):4d} missing={len(missing):3d}")
    if missing:
        fails.append(f)
        print("        " + ", ".join(missing[:20]))
print(f"\nTOTAL: {len(files)} files, {total_orig} tokens, {total_missing} missing")
sys.exit(1 if fails else 0)
