#!/usr/bin/env bash
# test-target-classifier.sh — Fail-closed target safety gate (INT-G2.1 v2)
# 
# Classify a target path + operation type against safety policy.
# HARD BLOCK on destructive mutation of protected targets.
#
# Usage:
#   bash scripts/test-target-classifier.sh classify read <path>
#   bash scripts/test-target-classifier.sh classify mutate <path>
#   bash scripts/test-target-classifier.sh classify delete <path>
#   bash scripts/test-target-classifier.sh classify execute <path>
#
# Returns: classification label on stdout, exit 0 (allow) or 1 (block).
#
# Policies:
#   CURRENT_CANONICAL_MAIN + mutate/delete/execute → HARD BLOCK
#   TRANSITIONAL_WORKTREE  + mutate/delete          → HARD BLOCK (except pilot-owned paths)
#   PROTECTED_BACKUP       + mutate/delete/execute  → HARD BLOCK
#   LOCAL_RUNTIME          + mutate/delete           → HARD BLOCK unless authorized synthetic
#   DISPOSABLE_FIXTURE     + mutate                 → ALLOW
#   UNKNOWN                + anything               → HARD BLOCK
set -u

CORE_ROOT="/c/Users/Admin/Desktop/Antigravity"
HERMES_HOME=$(cygpath -u "$LOCALAPPDATA/hermes" 2>/dev/null || echo "/c/Users/Admin/AppData/Local/hermes")
BACKUP_ROOT="$CORE_ROOT/_staging/hermes-backup-20260820-int-g2"
COUNCIL_SANDBOX="$CORE_ROOT/_staging/council-sandbox"

fail() { echo "[TEST-TARGET-CLASSIFIER] BLOCK: $*" >&2; exit 1; }
info() { echo "[TEST-TARGET-CLASSIFIER] $*"; }
allow() { echo "$1"; exit 0; }

classify() {
  local operation="${1:-}"
  local target="${2:-}"
  [ -n "$operation" ] || fail "operation required: read|mutate|delete|execute"
  [ -n "$target" ] || fail "target path required"
  
  # Validate operation
  case "$operation" in
    read|mutate|delete|execute) ;;
    *) fail "invalid operation: $operation (must be read|mutate|delete|execute)" ;;
  esac
  
  # Normalize path
  local norm
  norm="$(cygpath -u "$target" 2>/dev/null || echo "$target")"
  
  # === CURRENT_CANONICAL_MAIN ===
  local canonical_repo="C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform"
  local canonical_repo_u
  canonical_repo_u="$(cygpath -u "$canonical_repo" 2>/dev/null)"
  if echo "$norm" | grep -qF "$canonical_repo_u"; then
    local branch
    branch=$(git -C "$canonical_repo" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    if [ "$branch" = "main" ]; then
      info "CLASSIFICATION: CURRENT_CANONICAL_MAIN (op=$operation, path=$norm)"
      case "$operation" in
        mutate|delete|execute)
          fail "HARD BLOCK: Destructive $operation against CURRENT_CANONICAL_MAIN is prohibited. Use a disposable worktree."
          ;;
        read)
          info "Read-only on CURRENT_CANONICAL_MAIN — ALLOWED with caution"
          echo "CURRENT_CANONICAL_MAIN"
          return 0
          ;;
      esac
    fi
  fi
  
  # === TRANSITIONAL_WORKTREE ===
  local worktree="C:/Users/Admin/Desktop/Antigravity/iip-harness-prep"
  local worktree_u
  worktree_u="$(cygpath -u "$worktree" 2>/dev/null)"
  if echo "$norm" | grep -qF "$worktree_u"; then
    local branch
    branch=$(git -C "$worktree" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    info "CLASSIFICATION: TRANSITIONAL_WORKTREE (branch=$branch, op=$operation)"
    case "$operation" in
      mutate|delete)
        # Check if path is explicitly in pilot-owned scripts/ or evidence/
        if echo "$norm" | grep -qE "scripts/council-|scripts/test-target|evidence/FD-INT"; then
          allow "TRANSITIONAL_WORKTREE"
        else
          fail "HARD BLOCK: $operation on TRANSITIONAL_WORKTREE outside pilot-owned paths."
        fi
        ;;
      execute)
        if echo "$norm" | grep -q "^$worktree_u/scripts/"; then
          allow "TRANSITIONAL_WORKTREE"
        else
          fail "HARD BLOCK: execute outside scripts/ on TRANSITIONAL_WORKTREE."
        fi
        ;;
      read)
        allow "TRANSITIONAL_WORKTREE"
        ;;
    esac
  fi
  
  # === PROTECTED_BACKUP ===
  local backup_u
  backup_u="$(cygpath -u "$BACKUP_ROOT" 2>/dev/null)"
  if echo "$norm" | grep -qF "$backup_u"; then
    info "CLASSIFICATION: PROTECTED_BACKUP (op=$operation)"
    case "$operation" in
      mutate|delete|execute)
        fail "HARD BLOCK: $operation against PROTECTED_BACKUP. Backup is rollback asset, never mutable."
        ;;
      read)
        allow "PROTECTED_BACKUP"
        ;;
    esac
  fi
  
  # === LOCAL_RUNTIME ===
  if echo "$norm" | grep -q "^$HERMES_HOME"; then
    info "CLASSIFICATION: LOCAL_RUNTIME (op=$operation, path=$norm)"
    case "$operation" in
      mutate|delete)
        fail "HARD BLOCK: $operation on LOCAL_RUNTIME. Profile/config mutations not authorized during INT-G2."
        ;;
      read|execute)
        allow "LOCAL_RUNTIME"
        ;;
    esac
  fi
  
  # === DISPOSABLE_FIXTURE ===
  local sandbox_u
  sandbox_u="$(cygpath -u "$COUNCIL_SANDBOX" 2>/dev/null)"
  if echo "$norm" | grep -qE "^/tmp/|Temp.*int-g11|Temp.*council-scratch|Temp.*round2|Temp.*boundary"; then
    info "CLASSIFICATION: DISPOSABLE_FIXTURE (temp)"
    allow "DISPOSABLE_FIXTURE"
  fi
  if echo "$norm" | grep -qF "$sandbox_u"; then
    info "CLASSIFICATION: DISPOSABLE_FIXTURE (council sandbox)"
    allow "DISPOSABLE_FIXTURE"
  fi
  
  # === UNKNOWN — HARD BLOCK ===
  info "CLASSIFICATION: UNKNOWN (op=$operation, path=$norm)"
  fail "Cannot classify target path with operation '$operation' — BLOCKED for safety."
}

case "${1:-}" in
  classify)
    shift
    classify "$@" ;;
  *)
    echo "Usage: $0 classify <read|mutate|delete|execute> <path>"
    echo ""
    echo "Returns classification label on stdout, exit 0 (allow) or 1 (block)."
    exit 1
    ;;
esac