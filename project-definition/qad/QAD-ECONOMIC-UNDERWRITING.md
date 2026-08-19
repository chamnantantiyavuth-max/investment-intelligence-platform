# QAD Financial Reconstruction, Normalized Economics & Economic Underwriting Contract

> **Contract:** M3-08 (M3 Domain Contract Set)
> **Status:** M3 FINAL DRAFT (CORRECTION COMPLETE — AWAITING INDEPENDENT RE-REVIEW)
> **Authority:** FD #130; Constitution §1 (Central Question); Constitution §2 (QAD capabilities — Financial & Management Analysis, Normalization & Valuation); CAP-007A (FO — ADAPT: methodology); CAP-007B (FO Earnings Quality — ADAPT); FD #43 (Marx signals as supplementary inputs)
> **Traceability:** CONSTITUTION-§1/§2 · FD #43 · FD #130 · CAP-007A (ADAPT: Moat/Earnings quality methodology) · CAP-007B (ADAPT: Earnings Quality) · CAP-007C (SUPERSEDED — historical lineage only; not revived as QAD methodology) · CAP-009 (CIW ABSORB: deterministic calculations) · NEW_M3_DERIVATION (economic scenarios, permanent loss analysis, reverse DCF mandate, calculation lineage)

---

## 1. Purpose

Define the analytical framework for:

1. **Financial Reconstruction** — reconstructing 7–10+ years of financial data with full lineage
2. **Normalized Economics** — estimating what the business would earn under normalized conditions
3. **Economic Underwriting** — valuation as a diagnostic tool, economic damage vs price damage, permanent loss analysis

**Valuation is a diagnostic tool, not a decorative fair-value number.**

---

## 2. Financial Reconstruction

### 2.1 Scope

Reconstruct financial history for **7–10+ years where possible**. For younger companies, use available data and note the limitation.

### 2.2 Required Elements

| Element | Components | Source |
|---------|------------|--------|
| **Income Statement** | Revenue, COGS, SG&A, R&D, D&A, Operating Income, Net Income, EPS (diluted) | 10-K, 10-Q |
| **Revenue Bridge** | Organic vs acquisition, volume vs price vs mix, by segment | Segment reporting |
| **Margin Analysis** | Gross, Operating, EBITDA, Net, FCF margins; trend analysis | Calculated from Income Statement |
| **Cash Flow** | Operating CF, Investing CF, Financing CF, Free Cash Flow | Cash flow statement |
| **Working Capital** | Receivables, Inventory, Payables, DSO, DIO, DPO, Cash Conversion Cycle | Balance sheet + P&L |
| **Capital Allocation** | CapEx, R&D Capitalization, M&A (cash & stock), Buybacks, Dividends, Debt Issuance/Repayment | Cash flow statement |
| **Balance Sheet** | Cash, Debt (short + long), Equity, Goodwill, Intangibles, Tangible Book Value | Balance sheet |
| **ROIC** | NOPAT / Invested Capital — annual and incremental | Calculated |
| **Leverage** | Debt/EBITDA, Interest Coverage, Net Debt/Equity | Calculated |
| **Dilution** | Share count trend (basic and diluted), options/RSU overhang | 10-K, proxy |
| **Per-Share Economics** | EPS, FCF/share, Book Value/share, Tangible Book/share | Calculated |
| **M&A History** | Acquisitions by year, amount paid, earnout, goodwill, write-downs | 10-K, 8-K |

### 2.3 Calculation Lineage

Every derived calculation MUST have explicit lineage:

```text
Formula: FCF = Operating CF - CapEx
Inputs:
  Operating CF:  10-K FY2025 p.45 (Cash Flow Statement)
  CapEx:         10-K FY2025 p.45 (Cash Flow Statement)
Result:          $1.2B
Calculated by:   [Analyst/AI/System]
Timestamp:       ISO datetime
```

Calculations without lineage are not admissible in underwriting.

### 2.4 Normalization Adjustments

Identify and adjust for:

- Non-recurring items (restructuring, impairment, legal settlement, gains/losses)
- Cyclical adjustments (normalized margin, capacity utilization)
- Acquisition accounting adjustments (amortization of acquired intangibles, deferred revenue write-down)
- Pension, stock-based compensation, deferred tax
- Extraordinary items with clear documentation

Each adjustment is tagged: `PERMANENT / TEMPORARY / UNCERTAIN`

---

## 3. Economic Scenarios

Every case must define at minimum five scenarios:

### 3.1 CURRENT

- Based on recent performance (trailing 12 months or latest fiscal year)
- NOT adjusted for cyclical or temporary factors
- Represents the "as-is" economics

### 3.2 NO_RECOVERY

- Assumes current impaired economics are the new normal
- No recovery from dislocation
- No improvement in margins, growth, or returns
- Represents the permanent-damage baseline

### 3.3 PARTIAL_RECOVERY

- Partial recovery from dislocation, but not to pre-dislocation levels
- Margin improvement, but margins remain below historical average
- Growth resumes, but at lower rate
- Represents the MOSTLY_TEMPORARY scenario

### 3.4 NORMALIZATION

- Full recovery to normalized economics
- Margins, growth, returns return to sustainable long-run levels
- Not necessarily = pre-dislocation peak (may be average of cycle)
- Represents the TEMPORARY diagnosis case

### 3.5 QUALITY_COMPOUNDING

- Full recovery PLUS compounding at high returns
- Beyond normalization — the business resumes compounding at attractive incremental ROIC
- Represents the full upside case if impairment was purely temporary AND the moat remains intact

### 3.6 Scenario Parameters

Each scenario must explicitly state assumptions for:

| Parameter | Description |
|-----------|-------------|
| Revenue Growth | Long-run growth rate |
| Operating Margin | Normalized operating margin |
| Tax Rate | Sustainable tax rate |
| CapEx / Depreciation | Maintenance vs growth CapEx |
| Working Capital | Normalized WC as % of revenue |
| Reinvestment Rate | % of earnings reinvested |
| ROIC | Sustainable return on capital |
| Cost of Capital | WACC / discount rate |
| Time Horizon | When does normalization happen? |

---

## 4. Permanent Loss Analysis

For each scenario that implies value destruction:

### 4.1 Required Analysis

| Element | Description |
|---------|-------------|
| **Balance-sheet runway** | How long can the company operate at current cash burn before needing capital? |
| **Dilution risk** | Would a capital raise be required? At what price? What dilution? |
| **Asset impairment** | Are goodwill or intangible assets at risk of impairment? |
| **Covenant risk** | Is the company at risk of debt covenant breach? |
| **Refinancing risk** | Is refinancing feasible at current credit conditions? |
| **Competitive damage** | Is the dislocation permanently harming competitive position? |
| **Recovery capital** | If recovery requires investment, can the company fund it? |

### 4.2 Permanent Loss Estimate

Estimate the range of permanent economic loss under each scenario:

- **Revenue permanently lost**
- **Margin permanently compressed**
- **Market share permanently lost**
- **Investment permanently impaired (goodwill, intangibles, PP&E)**
- **Competitive position permanently weakened**

---

## 5. Valuation as Diagnostic Tool

### 5.1 Reverse DCF (MANDATORY)

Every case MUST include a Reverse DCF analysis:

| Step | Action |
|------|--------|
| 1 | Start from current market price |
| 2 | Derive the implied future cash flow growth rate |
| 3 | Compare implied growth rate to scenario assumptions |
| 4 | Determine: does the market price imply expectations that are far worse than the evidence supports? |

**Reverse DCF Output:**
- Current price vs normalized intrinsic value range
- Implied terminal growth rate vs reasonable long-run growth
- How many years of "no recovery" are priced in?
- What recovery rate does the market imply?

### 5.2 Price-Implied Expectations

For each scenario, what price would be justified?

| Scenario | Intrinsic Value Estimate | vs Current Price |
|----------|--------------------------|------------------|
| CURRENT | $X | Overvalued / Fair / Undervalued |
| NO_RECOVERY | $Y | Overvalued / Fair / Undervalued |
| PARTIAL_RECOVERY | $Z | Overvalued / Fair / Undervalued |
| NORMALIZATION | $W | Overvalued / Fair / Undervalued |
| QUALITY_COMPOUNDING | $V | Overvalued / Fair / Undervalued |

### 5.3 Economic Damage vs Price Damage

| Measure | Calculation | Interpretation |
|---------|-------------|----------------|
| **Economic Damage** | Normalized earnings per share − Current impaired earnings per share | The true economic impact of dislocation |
| **Price Damage** | Pre-dislocation price − Current price | The market's assessment of total damage |
| **Damage Gap** | Price Damage − Economic Damage (normalized) | Gap = market overreaction (QAD opportunity) or market pricing structural damage not yet in earnings |

A large positive gap where Price Damage >> Economic Damage is the QAD opportunity zone. But the gap must be validated: is the market pricing structural damage that hasn't yet appeared in earnings?

### 5.4 Valuation Methods (Supplementary)

- DCF (normalized earnings + growth phase + terminal value)
- Reverse DCF (primary — what growth does the market price imply?)
- Scenario-based intrinsic value range
- Sum-of-the-parts (if applicable)
- Peer multiple comparison (contextual, not determinative)
- Historical multiple range (contextual)

**No single fair value number.** Always a range with scenario weighting.

---

## 6. Forbidden Practices

- **No AI-invented fair value.** Valuation models must have explicit, documented assumptions.
- **No composite QAD score.** Quality + Dislocation + Impairment + Valuation remain separate.
- **No single fair value number.** Always present as a range or scenario.
- **No circular reasoning.** Do not use valuation to prove the dislocation is temporary, or dislocation to prove the valuation is wrong — each is independently supported.
- **No survivorship-biased extrapolation.** Historical returns that assume the business survives a dislocation it may not survive.
- **No decorative valuation.** Every valuation output must connect to a specific decision or question.

---

## 7. Valuation as a Diagnostic Tool

Valuation answers these questions, not "what is the stock worth":

1. What does the current price imply about future expectations?
2. Are those expectations far worse than the evidence supports?
3. What needs to happen for current holders to earn a reasonable return?
4. What is the risk of permanent loss vs the upside of normalization?
5. Under what conditions is this NOT a QAD opportunity?

---

## 8. Output Schema

The full underwriting output must contain:

| Output | Mandatory? |
|--------|-----------|
| Financial Reconstruction (7-10+ years) | ✅ |
| Calculation Lineage (key calculations) | ✅ |
| Normalization Adjustments | ✅ |
| Economic Scenarios (5 minimum) | ✅ |
| Reverse DCF | ✅ |
| Permanent Loss Analysis | ✅ |
| Balance-sheet Runway | ✅ |
| Economic Damage vs Price Damage | ✅ |
| Valuation Asymmetry Estimate | ✅ |
| Thesis Killers (financial) | ✅ |

<!-- 2026-08-19 13:15 UTC+7 -->