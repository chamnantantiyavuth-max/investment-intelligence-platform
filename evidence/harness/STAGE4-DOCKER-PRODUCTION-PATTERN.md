# Stage 4 — Production Docker Profile / Mount / Credential Pattern (design)

**Status:** Design only — NOT activated. Production IPM remains inactive (FD #100 prohibition).
**Date:** 2026-08-12
**Purpose:** Define how production IIP/IPM profiles will use the Docker terminal backend for hard filesystem isolation WITHOUT copying `.env`/`auth.json` into test profiles (as the Stage 3.2 C4 test did temporarily — now cleaned).

---

## 1. What the Stage 3.2 test did (and why it must not be the production pattern)

The C4 compatibility test created `harness-docker-test` / `harness-docker-ipm` profiles and **copied `iip/.env` + `iip/auth.json`** into them so the docker-backend workers could authenticate. That was acceptable for a bounded synthetic test (credentials removed immediately after, secret scan clean), but it violates least-privilege for production: credentials would multiply across profiles and drift.

**Cleanup done (C5/FD #100):** `.env` + `auth.json` removed from both test profiles; verified absent; no secret material in harness artifacts or git-tracked files; production `iip/.env` untouched.

## 2. Production credential mechanism (v0.20.0 native — no copying)

Hermes v0.20.0 resolves provider credentials from, in order: **env vars → auth.json (profile) → credential pool**. The Docker terminal backend supports `docker_forward_env` (forward selected host env vars into the container, e.g. `["DEEPSEEK_API_KEY"]`).

**Pattern for production docker profiles:**

```yaml
# profile config.yaml (per profile, NOT copied)
terminal:
  backend: docker
  docker_image: nikolaik/python-nodejs:python3.11-nodejs20
  docker_forward_env:            # forward creds from host env into container
    - DEEPSEEK_API_KEY
    - OPENROUTER_API_KEY
  docker_volumes:                # IIP-only or IPM-only mount mapping
    - "C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform:/workspace/iip"
  docker_mount_cwd_to_workspace: false
  container_persistent: false
```

- **One credential source per profile** = the profile's own `.env`/auth.json on the HOST (unchanged, gitignored), forwarded into the container via `docker_forward_env`.
- **No `.env` copies inside profile dirs beyond the canonical one**; no auth.json copies.
- If a profile needs NO network creds (pure filesystem work), `docker_forward_env: []`.

## 3. Mount isolation mapping (production)

| Profile | Mounts (read-only where possible) | Never mounted |
|---|---|---|
| iip / org-* (research) | IIP repo + harness-pilot/iip + skills-shared (read-only) | independent-portfolio-manager, harness-pilot/ipm |
| ipm (portfolio) | independent-portfolio-manager + harness-pilot/ipm | IIP research workspace internals (published reports read via IIP repo read-only is a Stage 7 decision) |
| shared skills (canonical) | read-only mount (`:ro`) into both — never writable from container | — |

**Read-only shared skills:** `skills-shared` should mount `:ro` in worker containers so workers can load skills but never mutate the canonical skill tree (Harness §33 read-only/admin-writer model).

## 4. Activation gate

- This pattern is NOT activated in Stage 4 (no production IPM; iip workers still `local` backend — Stage 3/3.2 proved docker capability).
- Activation = Stage 7 cutover decision, Founder-approved, after: (a) production IPM model decision, (b) per-profile mount map review, (c) `docker_forward_env` credential smoke test on a synthetic task, (d) board privacy policy unchanged.
- Rollback: revert profile `terminal.backend` to `local` + restore config backup (pattern already proven in Stage 3.2 rollback test).

## 5. Test-profile retirement

`harness-docker-test` / `harness-docker-ipm` remain installed (credentials stripped) as reusable docker-compat test fixtures for future A2 re-verification. They contain no secrets and no real workspace mounts beyond synthetic `harness-pilot/` (unchanged). Retire/delete at Stage 7 if no longer needed.

<!-- 2026-08-12 20:38:20 +0700 — captured via scripts/artifact_timestamp.py (system clock at write) -->
