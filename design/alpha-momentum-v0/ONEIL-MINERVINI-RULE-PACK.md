# O'Neil / Minervini Rule Pack

**Status:** Approved Domain Specification (Phase 7, FD #39)
**Version:** 0.1
**Owner:** Founder
**Authority:** Approved Domain Specification subordinate to the Constitution and Founder's Decisions
**Derived from:** Investment Intelligence Platform Constitution v0.4 §6; FD #27, #39
**Approval:** FD #39 (25 July 2026)

---

## 1. Purpose

Formalize the momentum methodology framework used by Alpha Momentum V0. This document defines the **conceptual framework** — stage analysis, CANSLIM principles, Volatility Contraction Pattern (VCP), and entry/exit heuristics — that the system references when assessing candidates.

This is a **spec document**, not code. Exact formulas, windows, weights, thresholds, and automated scoring implementation remain deferred until explicitly approved.

---

## 2. Stage Analysis (Stan Weinstein / Mark Minervini)

Every stock exists in one of four stages. Alpha Momentum V0 targets **Stage 2 (Advancing)** — confirmed uptrends with institutional accumulation.

### 2.1 Stage 1 — Basing / Accumulation

| Characteristic | Signal |
|---|---|
| Price action | Sideways, range-bound. No clear trend. |
| Moving averages | 50-day and 150-day MA flattening. Price oscillates around both. |
| Volume | Declining — no conviction either direction. |
| Relative strength | Flat vs market. Not leading or lagging. |
| Duration | Weeks to months (or years for deep bases). |
| Psychology | Apathy, neglect. No one cares about this stock. |

**V0 signal:** `thesis_status = "Emerging"` + price above flattening 150-day MA + RS neutral.

### 2.2 Stage 2 — Advancing / Uptrend

| Characteristic | Signal |
|---|---|
| Price action | Higher highs, higher lows. Consistent uptrend. |
| Moving averages | 50-day above 150-day, both sloping up. Price above both. |
| Volume | Expanding on up days, contracting on down days — institutional accumulation. |
| Relative strength | Outperforming market (RS line making new highs). |
| Breakout | Price breaks above Stage 1 resistance on +50% average volume. |
| Psychology | Growing optimism, then belief, then euphoria. |

**V0 signal:** `thesis_status = "Confirmed"` or `"Strengthening"` + Stage 2 characteristics. This is the **primary hunting ground** for Alpha Momentum.

### 2.3 Stage 3 — Topping / Distribution

| Characteristic | Signal |
|---|---|
| Price action | Choppy, wide swings. Higher highs failing. Lower lows appearing. |
| Moving averages | 50-day flattening, crossing below 150-day. Whipsaw action. |
| Volume | High volume on down days, low volume on up days — distribution. |
| Relative strength | RS deteriorating, making lower highs. |
| Psychology | Excitement → denial → anxiety. "It'll come back." |

**V0 signal:** `thesis_status = "Weakening"` + distribution characteristics → candidate flagged for review. Not automatic sell — but thesis weakening.

### 2.4 Stage 4 — Declining / Downtrend

| Characteristic | Signal |
|---|---|
| Price action | Lower highs, lower lows. Consistent downtrend. |
| Moving averages | 50-day below 150-day, both sloping down. Price below both. |
| Volume | High volume on selloffs — capitulation. Low volume bounces. |
| Relative strength | RS collapsing. Stock is a market laggard. |
| Psychology | Fear → desperation → capitulation → apathy. |

**V0 signal:** STAY AWAY. `thesis_status = "Invalidated"`. Never enter Stage 4. Never average down in Stage 4.

---

## 3. CANSLIM Principles (William O'Neil)

### 3.1 C — Current Quarterly Earnings

| Principle | Description |
|---|---|
| Earnings growth | Current quarter EPS up 25%+ YoY. The bigger, the better. |
| Acceleration | EPS growth rate accelerating (QoQ sequential improvement). |
| Sales growth | Revenue up 20%+ — earnings must be driven by sales, not cost-cutting. |
| Quality | Look for new products, new management, new industry conditions driving growth. |

**V0 usage:** `Candidate Quality Assessment (S3)` evaluates earnings strength. V0 uses synthetic data; exact EPS thresholds deferred.

### 3.2 A — Annual Earnings Growth

| Principle | Description |
|---|---|
| Consistency | Annual EPS growth for last 3 years. Stable 25%+ annual growth rate. |
| ROE | Return on Equity 17%+ — management creating shareholder value. |
| Trend | Recent years stronger than earlier years (accelerating). |

**V0 usage:** Integrated into fundamental momentum analysis (Operating Model §6.3). Deferred for V0 synthetic data.

### 3.3 N — New Product, New Management, New Highs

| Principle | Description |
|---|---|
| Catalyst | Something NEW driving the stock: new product, new CEO, new industry conditions, new legislation. |
| Price highs | Stocks making new 52-week highs tend to go higher. Don't fear new highs — embrace them. |
| Innovation | The biggest winners have a revolutionary new product or service. |

**V0 usage:** Theme context provides "N" — a theme (AI capex, cybersecurity demand, electrification) IS the new condition. Candidate QC narrative explains the "N" for each stock.

### 3.4 S — Supply and Demand

| Principle | Description |
|---|---|
| Shares outstanding | Smaller float → bigger moves on demand spikes. |
| Volume | Track volume on breakout days. Big volume = institutional conviction. |
| Buybacks | Share count reduction = EPS boost + demand signal. |
| Insider activity | Insider buying = positive; heavy insider selling = red flag. |

**V0 usage:** Volume analysis in entry readiness (S4). Float size considered in data confidence.

### 3.5 L — Leader or Laggard

| Principle | Description |
|---|---|
| Relative Strength | Buy the #1 or #2 stock in an industry group. Leaders lead. |
| RS Rating | RS line at new high BEFORE price reaches new high — leading indicator. |
| Industry Group | 80% of a stock's move is determined by its industry group. Strong group = tailwind. |

**V0 usage:** `relative_strength` assessment in S4. Theme-level strength as proxy for group strength. This is the core principle Alpha Momentum V0 is built on.

### 3.6 I — Institutional Sponsorship

| Principle | Description |
|---|---|
| Fund ownership | At least a few top-performing funds own the stock. |
| Accumulation | Increasing fund ownership quarter-over-quarter. |
| Quality | Look for funds with good track records, not just any institution. |

**V0 usage:** `institutional_accumulation` signal in Evidence. AN-003 (institutional accumulation signal) drives candidate addition decisions (see GAP-001).

### 3.7 M — Market Direction

| Principle | Description |
|---|---|
| Follow the market | 75% of stocks follow the general market. Don't fight the trend. |
| Market in correction | Raise cash, build watchlist, do NOT buy. |
| Follow-through day | Key signal confirming new uptrend after correction — +1.7% on higher volume day 4+ after low. |
| Distribution days | Count distribution days on indices — 5+ in 4 weeks = market under pressure. |

**V0 usage:** Market regime assessment (Operating Model §6.1). V0 currently assumes bullish regime for synthetic fixtures.

---

## 4. Volatility Contraction Pattern — VCP (Mark Minervini)

### 4.1 Pattern Definition

VCP is a technical pattern where volatility decreases with each successive contraction, forming a "tightening" base before a breakout.

| Characteristic | Description |
|---|---|
| Contractions | 2-4 waves of price contraction, each smaller than the last. |
| Volatility | Each pullback is shallower (% decline decreases in each contraction). |
| Volume | Volume dries up during contractions — no selling pressure. |
| Tightness | Final contraction: tight range, low volume — the "spring coiling." |
| Pivot point | Price level where stock breaks out of the contraction pattern. |
| Ideal pivot | Tight closes (3 days in a row within 1% of closing price). |

### 4.2 VCP Quality Hierarchy

| Quality | Characteristics |
|---|---|
| **Ideal** | 3+ contractions, VCP symmetry, tight closes at pivot, volume dry-up |
| **Good** | 2 contractions, reasonable symmetry, volume declining |
| **Acceptable** | 1 contraction, decent structure |
| **Reject** | No contraction — wild swings, no tightening, "loose" pattern |

### 4.3 VCP Entry

| Condition | Rule |
|---|---|
| Breakout level | Price breaks above pivot (the highest point of the pattern). |
| Volume confirmation | Breakout volume at least +50% above 50-day average. |
| Entry | Enter on breakout day or within 1-3% of pivot for lower risk. |
| Stop-loss | Below the low of the contraction that preceded the breakout. |

**V0 usage:** VCP is part of `entry_trigger` assessment in S4. V0 uses descriptive strings ("Watching for VCP contraction #2, pivot at $X") — automated pattern detection deferred.

---

## 5. Entry Rules — Alpha Momentum V0

### 5.1 Entry Conditions (All Must Be Met)

| # | Condition | Source |
|---|---|---|
| 1 | Stock is in **Stage 2** Advancing | Weinstein / Minervini |
| 2 | Theme is **Approved** and monitoring is **Active** | IIP Constitution |
| 3 | Relative Strength is **positive** (outperforming market) | CANSLIM §3.5 (L) |
| 4 | Volume confirms trend (accumulation, not distribution) | CANSLIM §3.4 (S) |
| 5 | Market regime is **not bearish** (no Stage 4 market) | CANSLIM §3.7 (M) |
| 6 | Entry trigger conditions are **met** (VCP breakout / pullback to MA / base breakout) | Minervini |
| 7 | Conviction is **Moderate** or **High** | Founder review |
| 8 | Candidate status is **Confirmed** or **Strengthening** | Thesis Lifecycle |

### 5.2 Entry Trigger Types

| Trigger | Description | When |
|---|---|---|
| **VCP Breakout** | Price breaks pivot on +50% volume after volatility contraction | After base formation |
| **Pullback to 50-day MA** | Price pulls back to rising 50-day MA on low volume | In sustained uptrend |
| **Cup-with-Handle Breakout** | Breakout from cup-with-handle pattern on volume | After 7-65 week base |
| **IPO Base Breakout** | First base after IPO — often the most explosive | Recent IPO (1-12 months) |
| **Flag/Pennant** | Tight consolidation after strong move — continuation pattern | Mid-trend |
| **RS Line New High** | RS line makes new high BEFORE price → leading indicator | Anytime |

**V0 usage:** Each candidate declares an `entry_trigger` with descriptive conditions. V0 does not auto-detect patterns — Founder review required.

---

## 6. Exit Rules — Q-Conditions

See `alpha-momentum-v0/q_conditions.py` for implementation. The conceptual framework:

### 6.1 Thesis Invalidation (Sell Immediately)

| Condition | Example |
|---|---|
| Theme weakens | Core thesis driver disappears (e.g., regulation kills industry) |
| Stage change (2 → 3 or 4) | Technical structure breaks — stock enters distribution or downtrend |
| Earnings breakdown | Two consecutive quarters of decelerating earnings growth |
| Management issues | Fraud, scandal, CEO departure without succession |
| Competitive disruption | Core product made obsolete by new technology |

### 6.2 Technical Breakdown (Sell/Reduce)

| Condition | Example |
|---|---|
| 50-day crosses below 150-day MA | Death cross — trend reversal signal |
| High-volume breakdown | Price drops 5%+ below key support on +50% volume |
| RS line collapsing | RS line breaking to new lows while market healthy |
| Failed breakout | Price breaks above pivot then reverses below within 3 days |
| Climax top | Parabolic move + exhaustion gap + highest volume in months |

### 6.3 Risk Management (Non-Negotiable)

| Rule | Principle |
|---|---|
| **Cut losses at 7-8%** | Max loss per position (O'Neil rule). No exceptions. |
| **Never average down** | Adding to losers compounds mistakes. Only add to winners. |
| **Position size by risk** | Size = max risk per trade / (entry - stop-loss). |
| **Never let a gain become a loss** | If up 10-15%, raise stop to breakeven. |
| **Sell into strength** | Take partial profits on extended moves (20-25% gain in 1-3 weeks). |

> **Note:** Position sizing, stop-loss execution, and allocation belong to **Capital Command** (external). The Investment Intelligence Platform identifies exit conditions and surfaces alerts — it does not execute or allocate.

---

## 7. Watchlist Lifecycle

Per Operating Model §6.8. Conceptual states (proposals until separately approved in strategy design):

```
Discovered → Qualified → Watchlist → Setup Forming → Ready for Review
    → Trigger Observed → Extended → Failed / Invalidated / Archived
```

### 7.1 State Definitions

| State | Meaning | Action |
|---|---|---|
| **Discovered** | Appeared in pipeline for the first time | Initial QC assessment |
| **Qualified** | Passed minimum criteria (Stage 2, positive RS, theme alignment) | Add to watchlist |
| **Watchlist** | Active monitoring, no setup yet | Daily data check |
| **Setup Forming** | VCP, base, or pullback developing | Close monitoring |
| **Ready for Review** | Setup complete, entry trigger conditions defined | **Surface to Founder** |
| **Trigger Observed** | Entry condition met per spec | Founder authorizes (or waits) |
| **Extended** | Price too far above entry — risk/reward unfavorable | Wait for pullback |
| **Failed** | Thesis invalidated or technical breakdown | Remove from active |
| **Invalidated** | Theme or thesis is no longer valid | Archive with lessons |
| **Archived** | Historical record — what happened + lessons learned | Reference only |

### 7.2 State Transitions

| From | To | Trigger |
|---|---|---|
| Discovered | Qualified | Pass QC minimum thresholds |
| Qualified | Watchlist | Founder approval (or auto if QC High) |
| Watchlist | Setup Forming | Price structure tightening (VCP forming) |
| Setup Forming | Ready for Review | Entry trigger conditions defined |
| Ready for Review | Trigger Observed | Price/volume meets trigger spec |
| Any | Failed | Thesis invalidation or Stage 3/4 |
| Any | Invalidated | Theme/evidence no longer supports |
| Trigger Observed | Extended | Price +15% above trigger without entry |
| Extended | Watchlist | Price pulls back to 50-day MA |

---

## 8. Conviction Framework

### 8.1 Conviction Drivers

| Driver | Weight | Description |
|---|---|---|
| Theme strength | High | Is the theme confirmed by multiple evidence types? |
| Stage clarity | High | Clear Stage 2? Clean base structure? |
| Institutional confirmation | High | Are funds accumulating? Volume confirming? |
| RS leadership | High | Is this the #1-2 stock in its theme/group? |
| Earnings trends | Moderate | Accelerating earnings and sales? |
| Entry readiness | Moderate | Is a setup forming? Entry trigger defined? |
| Market regime | Veto | Bear market = no entries regardless of other signals. |

### 8.2 Conviction Levels

| Level | Layers Aligned | Action |
|---|---|---|
| **High** | 5-7 drivers positive, no material contradiction | Priority Research (advisory per FD #13) |
| **Moderate** | 3-5 drivers positive, some uncertainty | Active monitoring |
| **Low** | 1-2 drivers positive, significant gaps | Requires explicit entry_trigger + Waiting status (ERP-004, FD #37) |

---

## 9. Version Boundaries

| Capability | V0 (Phase 7) | V1 (Phase 8+) |
|---|---|---|
| Stage definitions | ✅ | ✅ |
| CANSLIM framework | ✅ | ✅ |
| VCP definition | ✅ | ✅ |
| Entry/exit rules (conceptual) | ✅ | ✅ |
| Watchlist Lifecycle states | ✅ | ✅ |
| Conviction framework | ✅ | ✅ |
| Automated Stage detection | — | ✅ |
| Automated VCP pattern recognition | — | ✅ |
| Quantified CANSLIM scoring (EPS, RS, SMR ratings) | — | ✅ |
| Automated entry trigger detection | — | ✅ |
| Backtest framework with O'Neil/Minervini rules | — | ✅ |

---

## 10. References

- William J. O'Neil, *How to Make Money in Stocks* (CANSLIM, IBD)
- Mark Minervini, *Trade Like a Stock Market Wizard* (SEPA, VCP)
- Mark Minervini, *Think & Trade Like a Champion*
- Stan Weinstein, *Secrets for Profiting in Bull and Bear Markets* (Stage Analysis)
- Investment Intelligence Platform Constitution v0.4 §6 (Momentum & Market Leadership Intelligence)
- INVESTMENT-INTELLIGENCE-OPERATING-MODEL v0.1 §6 (Momentum path)
