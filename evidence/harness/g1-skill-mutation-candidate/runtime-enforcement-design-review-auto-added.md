# Runtime-Enforcement Design Review Probes

Use these probes when reviewing a local guard, hook, middleware, policy gate, or startup mitigation against an installed runtime.

## 1. Trace the effective mutation destination

Do not stop at the documented “current target” resolver. Trace the full call chain to the final resource open/write and inventory every higher-precedence override:

- explicit per-call argument;
- direct resource/path environment override;
- scoped/context-local override;
- process environment selection;
- persisted current/default selection.

A guard that validates only one selector can pass while the mutation lands elsewhere. Acceptance must assert the destination resource itself (for example, before/after rows in both expected and forbidden stores).

## 2. Separate registered failure semantics from registration failure

“Fail closed” usually applies only after the guard is installed and invoked. Review independently:

1. config parsing;
2. consent/allowlisting;
3. registration at every host entrypoint;
4. matcher semantics;
5. invocation on each mutation path;
6. timeout/crash/malformed-output behavior;
7. modes that disable custom hooks or middleware;
8. restart/reload behavior.

A missing, skipped, unapproved, disabled, or startup-failed hook is not protected merely because the hook itself is fail-closed.

## 3. Verify lifecycle outputs are actually consumed

An event firing does not imply its return value affects runtime behavior. Inspect both producer and consumer:

- where the event is invoked;
- whether return values are collected or discarded;
- which event actually supports blocking, context injection, or mutation;
- whether behavior differs on first turn, continuation, CLI, gateway, cron, or worker.

Do not credit an observer-only lifecycle hook as an enforcement or context-injection mechanism.

## 4. Cover bypass surfaces, not only the named tool

For every protected mutation, enumerate all reachable surfaces:

- native/in-process tool;
- generic terminal or shell tool invoking the CLI;
- explicit target flags or per-call target fields;
- dispatcher/worker internal writes;
- cron, gateway, dashboard/API, plugin, and helper paths;
- direct library/database access where it is an in-scope supported path.

Policy text and operator-run diagnostic scripts are defense in depth, not automatic enforcement.

## 5. Prove hook protocol compatibility

When adapting an existing shell script into a structured hook, verify stdout and exit-code contracts. A human-readable diagnostic script may become fail-closed garbage output under a JSON hook protocol. Lock these cases:

- valid allow/no-op response;
- explicit block response;
- designated block exit code;
- ordinary non-zero exit;
- malformed/non-object output;
- timeout;
- missing/non-executable handler;
- Unicode, quoting, escaped JSON, and Windows paths with spaces.

Use the runtime’s actual matcher behavior (for example, regex `fullmatch`, not assumed glob semantics).

## 6. Acceptance mapping standard

Each named acceptance must prove its own claim through the production path:

- positive mutation reaches the expected destination;
- negative mutation produces no delta in every forbidden destination;
- fresh process/session/gateway assertions inspect live runtime state, not merely config text;
- dispatcher and worker lifecycle assertions include create/claim/spawn/complete/block/comment/heartbeat as applicable;
- unrelated projects test every named isolation class, not one convenient sample;
- restart and rollback are separately exercised.

Duplicate or vague acceptance rows should be rewritten as concrete setup → action → oracle → cleanup cases without changing the governing requirement.

## 7. Prefer the smallest root correction plus one enforcement layer

When the defect is stale inherited startup state, first look for a profile-local startup configuration that deterministically overrides the stale value before the runtime pins it. Then retain one enforcement hook for deliberate per-call bypasses. Advisory context and policy text are optional visibility/defense-in-depth layers and must not be counted as safety mechanisms.

Do not globalize a project-local pin, patch upstream core when prohibited, or force unrelated projects onto the protected target.

## 8. Rollback contract

A reviewable design must name:

- exact configuration and handler artifacts to restore/remove;
- allowlist/consent entries affected;
- processes requiring restart;
- pre-change backup/checkpoint;
- post-rollback health checks;
- proof that unrelated projects and worker lifecycle still function.

Rollback is incomplete until exercised, not merely described.