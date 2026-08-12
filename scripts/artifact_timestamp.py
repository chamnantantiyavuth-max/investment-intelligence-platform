#!/usr/bin/env python3
"""Deterministic artifact timestamp helper (M1, Stage 2.1).

Usage:
    python scripts/artifact_timestamp.py            # prints Bangkok local time
    python scripts/artifact_timestamp.py --verify F   # check footer F <= now (tolerance 5s)

Rule (binding, P2 correction): artifact footers MUST be produced by this helper
at write time — never hard-coded by the agent. Verification: footer_time <= now.
"""
import sys
from datetime import datetime, timezone, timedelta

BKK = timezone(timedelta(hours=7), name="UTC+7")
FMT = "%Y-%m-%d %H:%M:%S %z"


def now_bkk() -> datetime:
    return datetime.now(timezone.utc).astimezone(BKK)


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "--verify":
        footer = sys.argv[2].strip()
        try:
            ft = datetime.strptime(footer, FMT).astimezone(BKK)
        except ValueError:
            print(f"UNPARSEABLE footer: {footer!r}")
            return 2
        now = now_bkk()
        ok = ft <= now
        delta = (now - ft).total_seconds()
        print(f"footer={footer} now={now.strftime(FMT)} delta={delta:.1f}s "
              f"VERIFY={'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    print(now_bkk().strftime(FMT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
