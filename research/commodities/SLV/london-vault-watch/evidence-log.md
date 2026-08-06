# London Silver Vaults — Evidence Log (ORG-2026-0009)

**Question (card):** Does the rise in reported London silver-vault holdings through June 2026 indicate easing physical availability, inventory relocation, or a change in the relationship between visible stocks and lease-market liquidity?
**Card:** ORG-2026-0009 (RADAR-001 round 2) · **Workspace:** research/commodities/SLV/london-vault-watch/
**Point-in-time rule (FD #58):** every figure valid only at its source date.

## Source register — LBMA London Vault Data (monthly, silver in million troy ounces)

Source: LBMA London Vault Data — https://www.lbma.org.uk/prices-and-data/london-vault-data ; underlying data endpoint https://www.lbma.org.uk/vault-holdings-data/data.json (array of [epoch_ms, gold_thousand_oz, silver_thousand_oz]); pulled 2026-08-07 via browser console; monthly points May 2025 → June 2026:

| Month | Silver (Moz) | Δ MoM (Moz) | Note |
|---|---|---|---|
| 2025-05 | 751.261 | — | |
| 2025-06 | 764.889 | +13.6 | radar match ✓ |
| 2025-07 | 778.013 | +13.1 | |
| 2025-08 | 792.392 | +14.4 | |
| 2025-09 | 790.309 | −2.1 | |
| 2025-10 | 844.105 | **+53.8** | Oct-2025 squeeze period → metal returns to London (confirms World Silver Survey statement quantitatively) |
| 2025-11 | 874.066 | +30.0 | |
| 2025-12 | 894.357 | +20.3 | |
| 2026-01 | 891.511 | −2.8 | |
| 2026-02 | 870.170 | −21.3 | radar match ✓ |
| 2026-03 | 883.743 | +13.6 | |
| 2026-04 | 882.655 | −1.1 | |
| 2026-05 | 887.725 | +5.1 | |
| 2026-06 | 902.843 | +15.1 | **series high (displayed range) — radar match ✓** |

## Derived figures (for cross-exam/audit re-run)

- Jun 2025 → Jun 2026: 764.889 → 902.843 Moz = **+137.954 Moz (+18.04% YoY)**
- Oct 2025 MoM: +53.8 Moz (+6.8%) — the largest single-month jump in the window
- Nov 2025 + Dec 2025 cumulative: +50.3 Moz (squeeze unwind absorption)
- Gold vaults same window: 282,141 → 304,285 thoz = +22,144 thoz (+7.85% YoY) — context for the gold-transmission note's official/investment absorption watch items
- June 2026 reading 902.843 Moz ≈ 2.5× the 2025+2026F cumulative deficits (40.3 + 46.3 = 86.6 Moz)

## Draft framing (for the analyst note)

1. **The observation:** London visible silver stocks at a series high (902.843 Moz, Jun 2026), +18.0% YoY, while the market recorded 40.3 Moz (2025) and 46.3 Moz (2026F) accounting deficits. Visible stocks ROSE ~138 Moz in 12 months — more than the entire 2025 deficit.
2. **What it does to the published challenge memo's framework:** the SLV challenge memo (`reports/silver-deficit-challenge-2026-08-06.md`) specified: the inventory/liquidity interpretation "would be weakened if vault availability rebuilds, lease rates and premiums normalize, and investment flows fail to absorb metal." Vault rebuild = the memo's OWN break condition → the first watch-item data point (vaults) has moved AGAINST the inventory-liquidity hypothesis. The deficit appears to be financed from visible-stock inflows — metal is arriving in London, not leaving.
3. **What it confirms:** the World Silver Survey's "October 2025 liquidity squeeze subsequently eased as metal returned to London" — the Oct 2025 vault jump (+53.8 Moz) is the quantitative footprint.
4. **The open questions:** where is the metal coming from? (mine supply is flat per Survey; candidates: unreported/other-location stocks, ETF liquidation, imports, ownership transfers that never left London). Does rising visible stock mean the deficit is an accounting/flow artifact rather than physical scarcity — or is the "deficit" being supplied by above-ground redistribution with no net creation? What do lease rates say (data not re-pulled — CME/LBMA lease sources failed)?
5. **Interpretive caution (per the challenge memo's discipline):** a single stock observation does not settle the deficit-character question — needs lease rates, COMEX stocks, premiums, and flow decomposition. The note must not overclaim.

## Data gaps (named)

- CME COMEX deliverable stocks — source failed this pass (HTTP/2 protocol error, both curl + browser)
- Lease rates (LBMA forward/lease data) — not re-pulled
- Shanghai premium persistence — not re-pulled
- ETF (SLV) holdings trend — single reading only (486.467M oz as of 2026-08-05, iShares)
- Solar-demand / industrial-demand decomposition — unchanged from the published challenge memo

## Sources & limitations

LBMA vault data is the official London vault-holding series (monthly, loco London). Figures are point-in-time as of their month-end. The analysis is advisory-only, portfolio-blind — no price target, no buy/sell.

<!-- 2026-08-07 02:00 UTC+7 -->
