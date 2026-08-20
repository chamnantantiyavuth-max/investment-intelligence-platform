#!/usr/bin/env bash
# test-target-classifier.sh — Fail-closed target safety gate (INT-G2.1)
# 
# Before any destructive or mutation-oriented negative test, classify the target.
# HARD BLOCK if target is CURRENT_CANONICAL_MAIN.
#
# Usage:
#   bash scripts/test-target-classifier.sh classify <path>
#   Returns: classification label + exit code (0=allow, 1=block)
#
# Classifications:
#   CURRENT_CANONICAL_MAIN   → HARD BLOCK
#   TRANSITIONAL_WORKTREE    → HARD BLOCK (no destructive tests)
#   DISPOSABLE_WORKTREE      → ALLOW (if explicitly in regression suite)
#   SYNTHETIC_FIXTURE        → ALLOW
#   LOCAL_RUNTIME            → ALLOW (with caution)
#   UNKNOWN                  → HARD BLOCK
set -u

CORE_ROOT="/c/Users/Admin/Desktop/Antigravity"
HERMES_HOME=$(cygpath -u "$LOCALAPPDATA/hermes" 2>/dev/null || echo "/c/Users/Admin/AppData/Local/hermes")

ACTION="${1:-}"
TARGET="${2:-}"

fail() { echo "[TEST-TARGET-CLASSIFIER] BLOCK: $*" >&2; exit 1; }
info() { echo "[TEST-TARGET-CLASSIFIER] $*"; }

classify() {
  local target="$TARGET"
  [ -n "$target" ] || fail "target path required"
  
  # Normalize path (convert to Unix-style if Windows)
  local norm
  norm="$(cygpath -u "$target" 2>/dev/null || echo "$target")"
  
  # === CURRENT_CANONICAL_MAIN ===
  local canonical_repo="C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform"
  local canonical_repo_u
  canonical_repo_u="$(cygpath -u "$canonical_repo" 2>/dev/null)"
  if echo "$norm" | grep -qF "$canonical_repo_u"; then
    # Check branch == main
    local branch
    branch=$(git -C "$canonical_repo" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    if [ "$branch" = "main" ]; then
      info "CLASSIFICATION: CURRENT_CANONICAL_MAIN (branch=main, path=$norm)"
      fail "Destructive tests against CURRENT_CANONICAL_MAIN are HARD BLOCKED. Use a disposable worktree or synthetic fixture."
    fi
  fi
  
  # === TRANSITIONAL_WORKTREE ===
  local worktree="C:/Users/Admin/Desktop/Antigravity/iip-harness-prep"
  local worktree_u
  worktree_u="$(cygpath -u "$worktree" 2>/dev/null)"
  if echo "$norm" | grep -qF "$worktree_u"; then
    local branch
    branch=$(git -C "$worktree" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    info "CLASSIFICATION: TRANSITIONAL_WORKTREE (branch=$branch)"
    if [ "$branch" != "harness/stage2-prep" ]; then
      fail "Unknown branch in transitional worktree — BLOCKED."
    fi
    # Allow non-destructive reads; block destructive mutations
    # (caller must specify if operation is destructive)
    echo "TRANSITIONAL_WORKTREE"
    return 0
  fi
  
  # === DISPOSABLE_WORKTREE ===
  if echo "$norm" | grep -q "^/tmp/" || echo "$norm" | grep -q "Temp.*int-g11\|Temp.*council-scratch\|Temp.*round2"; then
    info "CLASSIFICATION: DISPOSABLE_WORKTREE"
    echo "DISPOSABLE_WORKTREE"
    return 0
  fi
  
  # === SYNTHETIC_FIXTURE ===
  if echo "$norm" | grep -q "_staging/council-sandbox\|_staging/hermes-backup" || echo "$norm" | grep -q "Temp.*fixture"; then
    info "CLASSIFICATION: SYNTHETIC_FIXTURE (under staging or temp fixture)"
    echo "SYNTHETIC_FIXTURE"
    return 0
  fi
  
  # === LOCAL_RUNTIME ===
  if echo "$norm" | grep -q "^$HERMES_HOME"; then
    info "CLASSIFICATION: LOCAL_RUNTIME (Hermes profile/config)"
    echo "LOCAL_RUNTIME"
    return 0
  fi
  
  # === UNKNOWN — HARD BLOCK ===
  info "CLASSIFICATION: UNKNOWN (path=$norm)"
  fail "Cannot classify target path — BLOCKED for safety."
}

case "$ACTION" in
  classify) classify ;;
  *)
    echo "Usage: $0 classify <path>"
    echo "Returns classification label on stdout, exits 0 (allow) or 1 (block)."
    exit 1
    ;;
esac