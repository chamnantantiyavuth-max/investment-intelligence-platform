#!/usr/bin/env bash
# IIP backend launcher — sources .env (gitignored) so credentials survive session closes.
# Usage: ./start-backend.sh   (from repo root; uses the 3.11 venv `python` on PATH)
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "ERROR: .env missing — copy .env.example and fill IIP_AUTH_* values" >&2
  exit 1
fi
set -a; source .env; set +a
exec python -m uvicorn backend.main:app --port 8000
# <!-- 2026-08-04 00:41 UTC+7 -->
