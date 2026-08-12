#!/usr/bin/env bash
# Stage 4 locked acceptance — S3-F1 Board Safety (runs after implementation)
# Usage: bash scripts/stage4-acceptance.sh
set -u
KANBAN_ROOT="/c/Users/Admin/AppData/Local/hermes"
PASS=0; FAIL=0

check() { # $1 = label, $2 = expected, $3 = actual
  if [ "$2" = "$3" ]; then PASS=$((PASS+1)); echo "  ✓ $1 (=$2)";
  else FAIL=$((FAIL+1)); echo "  ✗ $1: expected '$2' got '$3'"; fi
}

echo "=== Stage 4 locked acceptance — board resolution (expected iip) ==="

# 1. fresh shell (no env) → board file = iip
echo "[1] fresh shell (no env):"
env -u HERMES_KANBAN_BOARD bash -c 'tr -d "[:space:]" < "$KANBAN_ROOT/kanban/current"' 2>/dev/null
check "fresh shell resolves" "iip" "$(env -u HERMES_KANBAN_BOARD tr -d '[:space:]' < "$KANBAN_ROOT/kanban/current")"

# 2. board-guard fresh (no env)
echo "[2] board-guard fresh:"
G="$(env -u HERMES_KANBAN_BOARD bash "C:/Users/Admin/Desktop/Antigravity/iip-harness-prep/scripts/board-guard.sh" >/dev/null 2>&1; echo $?)"
check "board-guard fresh exit" "0" "$G"

# 3. board-guard with stale env MUST fail closed
echo "[3] board-guard stale env (other) must BLOCK:"
G="$(HERMES_KANBAN_BOARD=other bash "C:/Users/Admin/Desktop/Antigravity/iip-harness-prep/scripts/board-guard.sh" >/dev/null 2>&1; echo $?)"
check "board-guard stale blocks" "1" "$G"

# 4. current board file = iip
echo "[4] current board file:"
check "kanban/current" "iip" "$(tr -d '[:space:]' < "$KANBAN_ROOT/kanban/current")"

# 5. CLI resolve (hermes kanban boards show)
echo "[5] CLI board resolution:"
B="$(unset HERMES_KANBAN_BOARD; hermes kanban boards show 2>/dev/null | grep -m1 "Display name" | sed 's/.*: //')"
check "boards show name" "Capital Intelligence" "$B"

echo
echo "RESULT: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && echo "ACCEPTANCE: PASS" || echo "ACCEPTANCE: FAIL"
exit $FAIL
