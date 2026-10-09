# M6.5 — Inherited-failure attribution (known, non-M6.5)

Status: PROVEN PRE-EXISTING · NOT an M6.5 regression · NOT fixed inside M6.5

## Test

    tests/qad/test_contract_conformance.py::test_schema_build_identity

## Observation

At the M6.5 review head under review:

    $ pytest tests/qad/test_contract_conformance.py::test_schema_build_identity -q
    1 failed

## Attribution proof (real output, this session)

The same test was run against a throwaway git worktree checked out at the CLEAN M6.4
baseline `e13a64e`, where the M6.5 module does not exist:

    $ git worktree add -f <scratch>/attr-e13a64e e13a64e
    $ ls qad/m6/
    __init__.py  eligibility.py  ledger.py  research_contract.py  snapshot.py
    $ pytest tests/qad/test_contract_conformance.py::test_schema_build_identity -q
    1 failed

`qad/m6/orchestration.py` is ABSENT at `e13a64e` — i.e. M6.5 introduced nothing that the
failing assertion could depend on — and the test fails identically.

The worktree was removed after the check (`git worktree remove --force`), leaving no
residue.

## Conclusion

- The failure is inherited, not introduced by M6.5.
- The shared QAD regression count for M6.5 is reported as: `tests/qad` = 832 passed /
  1 inherited failure (this one).
- Per the M6.5 brief, this test is NOT part of M6.5 and is deliberately NOT fixed inside
  this cluster.

<!-- 2026-10-09 14:20 UTC+7 -->
