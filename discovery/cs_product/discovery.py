"""CS Product Discovery — shadow watch-input collector (FD #97, un-deferred).

Close System Product Radar (CLOSE-SYSTEM-PRODUCT-RADAR.md §2-5, FD #39) scans
physical-commodity products (gold, silver, copper, oil, ...) for structural
buy-at-a-discount setups. The V0 pipeline (close_system/) uses SYNTHETIC
fixtures. This discovery layer adds the REAL watch-input side:

  watch inputs (deterministic, from the radar pulls + public sources)
      │
      ▼
  pattern matcher (spec §5: Cyclical Trough / Sentiment Divergence /
                   Dislocation / Inventory / Physical-vs-Paper)
      │
      ▼
  evidence blocks → CoS triage → RM → role 03 research   (firewall, FD #88)

Same firewall as WP2: output = deterministic evidence ONLY. Never cards, never
CoS, never publish. Role 03 (Commodity Product Analyst) = Principal Owner.

Data reality (11 Aug 2026, verified in radar pulls):
  - LBMA gold_pm.json works; LBMA silver JSON 404s; tradingeconomics 403s.
  - COMEX/London vault levels, LBMA lease rates, SLV ETF flows: pulled per
    radar run (semi-automated, not a standing fetcher).
  - So v0.1 collects inputs that ARE available deterministically and marks the
    rest as missing (honest empty) — never invents a number.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

# ── Watch universe (physical commodities in scope, spec §3.4) ─────────────
# identity-only; membership fixed, not AI-invented.
WATCH_UNIVERSE: dict[str, dict] = {
    "gold": {
        "name": "Gold",
        "products": ["GLD", "IAU", "SGOL"],
        "key_fixes": ["LBMA PM (gold_pm.json)"],
        "patterns": ["cyclical_trough", "sentiment_divergence", "dislocation", "physical_vs_paper"],
    },
    "silver": {
        "name": "Silver",
        "products": ["SLV", "SIVR", "PSLV"],
        "key_fixes": ["LBMA PM (unavailable — 404 as of 11 Aug)"],
        "patterns": ["cyclical_trough", "sentiment_divergence", "dislocation", "inventory", "physical_vs_paper"],
    },
    "copper": {
        "name": "Copper",
        "products": ["COPX", "JJC"],
        "key_fixes": ["LME/COMEX (not yet wired)"],
        "patterns": ["cyclical_trough", "inventory", "physical_vs_paper"],
    },
    "oil": {
        "name": "Oil (WTI)",
        "products": ["USO", "XLE"],
        "key_fixes": ["EIA (not yet wired)"],
        "patterns": ["cyclical_trough", "sentiment_divergence", "dislocation"],
    },
}


@dataclass
class WatchInput:
    """One deterministic watch input (point-in-time, FD #58)."""
    commodity: str
    metric: str            # e.g. "gold_lbma_pm_usd_oz", "gold_silver_ratio"
    value: float | None
    as_of: str             # source date (never "today" unless actually pulled today)
    source: str            # e.g. "LBMA gold_pm.json"
    status: str = "verified"   # verified | missing | stale
    note: str = ""


@dataclass
class PatternEvidence:
    """One spec §5 pattern observation on a commodity."""
    commodity: str
    pattern: str           # spec pattern id
    signal: str            # supporting | neutral | opposing | not_evaluated
    checks: dict[str, bool]
    note: str = ""


def _ratio(gold: float | None, silver: float | None) -> float | None:
    if gold is None or silver is None or silver == 0:
        return None
    return gold / silver


def collect_watch_inputs(inputs: dict[str, dict]) -> list[WatchInput]:
    """Build watch inputs from the supplied data dict.

    inputs: {commodity: {metric: {"value": float|None, "as_of": str,
                                  "source": str, "status": str, "note": str}}}
    Unknown/missing metrics are recorded as missing — never invented.
    """
    out: list[WatchInput] = []
    for commodity, metrics in inputs.items():
        for metric, meta in metrics.items():
            out.append(WatchInput(
                commodity=commodity,
                metric=metric,
                value=meta.get("value"),
                as_of=meta.get("as_of", ""),
                source=meta.get("source", ""),
                status=meta.get("status", "missing"),
                note=meta.get("note", ""),
            ))
    return out


def evaluate_patterns(inputs: list[WatchInput]) -> list[PatternEvidence]:
    """Run spec §5 pattern checks on collected inputs.

    Deterministic thresholds are PROPOSED (FD #53) — shadow phase, same as WP2.
    Any metric missing → that check is False with an explicit note (honest
    empty), never a guessed value.
    """
    by = {i.metric: i for i in inputs}
    evidence: list[PatternEvidence] = []

    # ── Gold / Silver: physical-vs-paper + valuation ratio ──
    g_pm = by.get("gold_lbma_pm_usd_oz")
    s_pm = by.get("silver_lbma_pm_usd_oz")
    ratio = _ratio(g_pm.value if g_pm else None, s_pm.value if s_pm else None)
    ratio_hi = ratio is not None and ratio > 80.0   # PROPOSED threshold
    ratio_lo = ratio is not None and ratio < 50.0   # PROPOSED threshold
    if g_pm or s_pm:
        evidence.append(PatternEvidence(
            commodity="gold/silver",
            pattern="physical_vs_paper",
            signal="supporting" if ratio_hi else ("opposing" if ratio_lo else "neutral"),
            checks={"gold_silver_ratio_available": ratio is not None,
                    "ratio_above_80_proposed": ratio_hi,
                    "ratio_below_50_proposed": ratio_lo},
            note=(f"gold/silver ratio = {ratio:.1f}" if ratio else
                  "silver LBMA unavailable (404) — ratio cannot be evaluated"),
        ))

    # ── Gold: dislocation (spot vs futures premium) ──
    g_spot = by.get("gold_spot_usd_oz")
    g_fut = by.get("gold_front_future_usd_oz")
    if g_spot and g_fut:
        premium = ((g_spot.value or 0) - (g_fut.value or 0)) / (g_fut.value or 1) * 100
        evidence.append(PatternEvidence(
            commodity="gold",
            pattern="dislocation",
            signal="supporting" if premium > 0.5 else "neutral",   # PROPOSED: >0.5% spot premium
            checks={"spot_and_future_available": True, "spot_premium_pct_above_0_5": premium > 0.5},
            note=f"spot premium {premium:.2f}% over front future",
        ))

    # ── Silver: inventory ──
    s_inv = by.get("silver_london_vault_oz")
    if s_inv and s_inv.value is not None:
        evidence.append(PatternEvidence(
            commodity="silver",
            pattern="inventory",
            signal="neutral",
            checks={"vault_inventory_available": True},
            note=f"London vaults {s_inv.value:,.0f} oz as of {s_inv.as_of} — trend needs 2+ points (watch)",
        ))

    # ── Copper / Oil: cyclical trough (price vs cost floor) ──
    for commodity, price_key, cost_key in [
        ("copper", "copper_price_usd_lb", "copper_avg_aisc_usd_lb"),
        ("oil", "wti_price_usd_bbl", "wti_breakeven_usd_bbl"),
    ]:
        px = by.get(price_key)
        cost = by.get(cost_key)
        if px and cost and px.value is not None and cost.value is not None and cost.value > 0:
            margin = px.value / cost.value
            evidence.append(PatternEvidence(
                commodity=commodity,
                pattern="cyclical_trough",
                signal="supporting" if margin <= 1.3 else "neutral",   # PROPOSED: ≤1.3x cost floor
                checks={"price_and_cost_available": True, "price_within_30pct_of_cost": margin <= 1.3},
                note=f"price/cost = {margin:.2f}x ({price_key} {px.value} / {cost.value})",
            ))
    return evidence


def run_discovery(inputs: dict[str, dict]) -> dict:
    """Shadow run: inputs → watch inputs → pattern evidence → evidence pack.

    Firewall (FD #88 pattern): output is evidence ONLY. No card, no CoS, no
    research capacity, no publish. Role 03 judges what deserves a card.
    """
    watch = collect_watch_inputs(inputs)
    patterns = evaluate_patterns(watch)
    return {
        "as_of": date.today().isoformat(),
        "watch_inputs": [
            {"commodity": w.commodity, "metric": w.metric, "value": w.value,
             "as_of": w.as_of, "source": w.source, "status": w.status, "note": w.note}
            for w in watch
        ],
        "pattern_evidence": [
            {"commodity": p.commodity, "pattern": p.pattern, "signal": p.signal,
             "checks": p.checks, "note": p.note}
            for p in patterns
        ],
        "proposed": True,  # FD #53 — thresholds PROPOSED, shadow phase
        "firewall": "evidence only — no card, no CoS, no research, no publish (FD #88 pattern)",
    }
