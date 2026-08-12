# DR Rehearsal — S3 Pass B — Per-View Hash Manifest (FREEZE-READY)

**Lane:** S3 — Independent Hermes Pass B (anti-anchoring) · org-quant-validator (Role 08)
**Frozen at:** 2026-08-12 22:46 UTC+7 (post-production; no edits after this timestamp without breaking the manifest)
**Purpose:** freeze artifact for S5 (Freeze First Passes + Reconciliation). Any edit to the view after this manifest invalidates the hash below.

## View artifact (SHA-256)

| Artifact | SHA-256 |
|---|---|
| `pass-B-view-quant-model-validator.md` | `f0ecb9721169df1dbe52bb2cfbd2fa50cbbb12256e31145d558a2b5203cc139f` |

Verification command:

```bash
cd <workspace t_1ec41f0e>
sha256sum pass-B-view-quant-model-validator.md
# expect: f0ecb9721169df1dbe52bb2cfbd2fa50cbbb12256e31145d558a2b5203cc139f
```

## Input snapshot (admitted sources as read — see view §1)

| Source | SHA-256 |
|---|---|
| aapl-10k-fy2025.txt | `1d973ff69c666d3cc29cecbec42f3622f184726f1166249525e98292be31f2d7` |
| aapl-8k-q3fy26-ex991.txt | `26c745f5f42e16161264c6b6a7ce38a2c7a11d944ca4fb6365fcc9d21dcc5224` |
| aapl-10q-q3fy26.txt | `1a993be97c297278333c630fed9c6faffb0348bfa6fadb36ba4702aabeee15df` |
| q1fy26-10q.txt | `e4d4e5104888f074c7866e7ccab4fc1f333341216f81248768b738bbf27f31db` |
| q2fy26-10q.txt | `800ce43256e7937a56bf5c3955bda01eabf08500707938a31034f6be2caa5ff2` |
| aapl-xbrl-facts.json | `73a86c6aedc31f77cac2ea4df5f80f0b3bd7e6eb58bb4e01444fbedf3afb9c43` |
| reports/apple-deep-analysis-2026-08-09.md (admitted case) | `eb47dbb5e245701addc999bdff899a917cceb1ac34cd79c876571a49e5915e92` |

## Headline handoff to S5 (material items)

1. **25-point verification register:** 21/25 reproduced, 3 caveated (FY21–22 segment GM endpoints; Ireland $10.2B), 1 **PIT-stale**: intangibles.
2. **PIT finding (V13):** published "11.093→21.334 (+92.32%)" is Q2 FY26 10-Q dated; Q3 FY26 10-Q shows **20,342 @ 2026-06-27 (+83.4% YTD, −$992M QoQ)**. Thesis survives; magnitude/trajectory differ.
3. **New reconciliation items:** (a) XBRL IntangibleAssetsNetExcludingGoodwill ≠ 10-Q balance-sheet "Intangible assets, net" on every date (gap $2.2B→$5.1B, widening); (b) other non-current liabilities +$13.5B unexplained.
4. **Services margin flat, not inflected:** Q3 Services GM 75.62% = y/y flat; 9M +0.8pp mix-driven.
5. No cross-contamination: Pass A and Gemini outputs were not read.

<!-- 2026-08-12 22:46 UTC+7 -->
