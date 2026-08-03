#!/usr/bin/env bash
# =============================================================================
# isolation-scan.sh — Forbidden-path violation scanner (v3.3.0), adapted for IIP (FD #46)
# Usage: bash scripts/isolation-scan.sh [task_contract_file]
# Exit 0 = no violations. Exit 1 = forbidden path(s) modified.
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Forbidden paths for the Real-Data Production Path workstream (FD #46)
# — broker/execution/allocation surfaces must NEVER be touched
FORBIDDEN_PATTERNS=(
    "src/broker/"
    "src/execution/"
    "src/allocation/"
    "broker_"
    "execution"
    "portfolio_allocation"
)

FAILURES=0
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
pass() { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; FAILURES=$((FAILURES + 1)); }

echo "=== Isolation Scan (FD #46) ==="
echo ""

# Scan working tree changes (tracked + untracked)
CHANGED=$(git status --porcelain | awk '{print $2}' | grep -v '^"')
if [ -z "$CHANGED" ]; then
    pass "No working-tree changes to scan"
    exit 0
fi

VIOLATION=false
for f in $CHANGED; do
    for pat in "${FORBIDDEN_PATTERNS[@]}"; do
        if [[ "$f" == *"$pat"* ]]; then
            fail "FORBIDDEN PATH touched: $f (matches '$pat')"
            VIOLATION=true
        fi
    done
done

if [ "$VIOLATION" = false ]; then
    pass "No forbidden-path violations in working tree"
fi

echo ""
echo "=== Isolation Scan Complete ==="
if [ $FAILURES -eq 0 ]; then
    exit 0
else
    echo -e "${RED}$FAILURES violation(s)${NC}"
    exit 1
fi
