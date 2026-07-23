"""
experimental/anomaly.py — Statistical Anomaly Detection Engine

Phase 5 Theme Intelligence V1 (T2)
Authorized: FD #27 (23 July 2026)
Re-architected: T2 — statistical detection (24 July 2026)

Per FD #27 §2: Must be ACTUAL COMPUTATION — not hand-written fixtures.
Uses Python stdlib math/statistics only — no numpy, scipy, pandas.

Detection types:
  - Sector Divergence: theme RS trend vs sector benchmark (z-score)
  - Single-Stock Outlier: stock returns vs peer group (z-score > 2σ)
  - Volume Anomaly: current volume vs average (ratio > 2x or z-score)
  - Missing Correlation: correlation breakdown (|r| < 0.5 threshold)

Circular Feedback Guard (FD #27 §4):
  - Anomalies promoted to hypothesis are suppressed for 30-day cooldown
  - State persists via in-memory promotion tracker
"""

import math
import statistics
import uuid
from datetime import date, datetime

# ── Inbox API for writing/reading anomalies and hypotheses ──
from experimental.inbox import add_anomaly, list_anomalies, list_hypotheses

# ══════════════════════════════════════════════════════════════
# CIRCULAR FEEDBACK GUARD — Cooldown state (in-memory, FD #27 §4)
# ══════════════════════════════════════════════════════════════
_promotion_tracker = {}  # anomaly_id -> date when promoted

# Detection thresholds
ZSCORE_THRESHOLD = 2.0
VOLUME_RATIO_THRESHOLD = 2.0
CORRELATION_THRESHOLD = 0.5


# ══════════════════════════════════════════════════════════════
# STATISTICAL UTILITIES (stdlib only)
# ══════════════════════════════════════════════════════════════

def _pearson_r(x, y):
    """Compute Pearson correlation coefficient r between two sequences.

    Uses sample covariance / (sample_std_x * sample_std_y).
    Returns 0.0 if either sequence has < 2 points or zero variance.
    """
    n = min(len(x), len(y))
    if n < 2:
        return 0.0
    x_mean = statistics.mean(x[:n])
    y_mean = statistics.mean(y[:n])
    cov = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    try:
        sx = statistics.stdev(x[:n])
        sy = statistics.stdev(y[:n])
    except statistics.StatisticsError:
        return 0.0
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return cov / ((n - 1) * sx * sy)


def _z_score(value, mean, stdev):
    """Compute z-score. Returns 0 if stdev is 0."""
    if stdev == 0.0:
        return 0.0
    return (value - mean) / stdev


def _make_anomaly(anomaly_type, description, related_theme=None, related_tickers=None):
    """Build a well-formed anomaly dict and write it to the inbox.

    Returns the anomaly dict with the actual inbox-assigned ID.
    """
    data = {
        "type": anomaly_type,
        "description": description,
        "first_observed": datetime.now().strftime("%Y-%m-%d"),
        "status": "Unexplained",
        "source": "E1-Anomaly Detection (statistical)",
    }
    if related_theme:
        data["related_theme"] = related_theme
    if related_tickers:
        data["related_tickers"] = related_tickers
    else:
        data["related_tickers"] = []

    # Write to in-box; get the persisted ID
    persisted_id = add_anomaly(data)

    # Return a full anomaly dict matching what the inbox stores
    return {
        "id": persisted_id,
        "type": anomaly_type,
        "description": description,
        "first_observed": data["first_observed"],
        "related_theme": related_theme,
        "related_tickers": related_tickers or [],
        "status": "Unexplained",
        "source": data["source"],
    }


# ══════════════════════════════════════════════════════════════
# DETECTION FUNCTIONS
# ══════════════════════════════════════════════════════════════

def detect_sector_divergence(theme_rs_data, benchmark=None):
    """Detect sector-level divergence between theme RS and sector benchmark.

    Uses z-score of each theme's RS values compared to the benchmark.
    A theme with |z| > 2.0 relative to the benchmark is flagged as anomalous.

    Args:
        theme_rs_data: dict of theme_id -> list of RS values (float)
        benchmark: scalar benchmark RS value, or None (uses theme mean)

    Returns:
        list of anomaly dicts, each written to inbox via add_anomaly()
    """
    anomalies = []

    for theme_id, rs_values in theme_rs_data.items():
        if len(rs_values) < 2:
            continue

        mean_rs = statistics.mean(rs_values)
        try:
            std_rs = statistics.stdev(rs_values)
        except statistics.StatisticsError:
            std_rs = 0.0

        b = benchmark if benchmark is not None else mean_rs
        z = _z_score(mean_rs, b, std_rs)

        if abs(z) > ZSCORE_THRESHOLD:
            direction = "above" if z > 0 else "below"
            an = _make_anomaly(
                anomaly_type="Sector Divergence",
                description=(
                    f"Theme {theme_id} RS (mean={mean_rs:.1f}) diverges "
                    f"from benchmark ({b}) with z-score={z:.2f} ({direction} "
                    f"benchmark). Theme trend is anomalous relative to sector."
                ),
                related_theme=theme_id,
            )
            anomalies.append(an)

    return anomalies


def detect_single_stock_outlier(price_data, benchmark):
    """Detect single-stock outliers whose returns deviate from benchmark peers.

    Computes periodic returns for each stock and compares their mean return
    to the benchmark distribution. Stocks with |z| > 2.0 are flagged.

    Args:
        price_data: dict of ticker -> list of prices
        benchmark: dict of benchmark ticker -> list of prices

    Returns:
        list of anomaly dicts
    """
    anomalies = []

    # Compute benchmark return distribution
    bench_returns = []
    for ticker, prices in benchmark.items():
        if len(prices) < 2:
            continue
        for i in range(1, len(prices)):
            if prices[i - 1] != 0:
                bench_returns.append((prices[i] - prices[i - 1]) / prices[i - 1])

    if not bench_returns:
        return []

    bench_mean = statistics.mean(bench_returns)
    bench_std = statistics.stdev(bench_returns) if len(bench_returns) > 1 else 0.0

    for ticker, prices in price_data.items():
        if len(prices) < 2:
            continue

        stock_returns = []
        for i in range(1, len(prices)):
            if prices[i - 1] != 0:
                stock_returns.append((prices[i] - prices[i - 1]) / prices[i - 1])

        if len(stock_returns) < 2:
            continue

        stock_mean = statistics.mean(stock_returns)

        # Compare stock's mean return to benchmark distribution
        z = _z_score(stock_mean, bench_mean, bench_std)

        if abs(z) > ZSCORE_THRESHOLD:
            direction = "outperforming" if z > 0 else "underperforming"
            an = _make_anomaly(
                anomaly_type="Single-Stock Outlier",
                description=(
                    f"{ticker} mean return ({stock_mean:.4f}) deviates from "
                    f"benchmark ({bench_mean:.4f}) with z-score={z:.2f}. "
                    f"Stock is {direction} its peer group."
                ),
                related_tickers=[ticker],
            )
            anomalies.append(an)

    return anomalies


def detect_volume_anomaly(volume_data, avg_baseline=None):
    """Detect unusual volume spikes relative to average volume baseline.

    For each ticker, compares individual volume entries against the average
    (either a provided baseline or computed from the data). Flags if the
    ratio exceeds 2.0x or z-score exceeds 2.0σ.

    Args:
        volume_data: dict of ticker -> list of volume values
        avg_baseline: optional scalar baseline volume

    Returns:
        list of anomaly dicts
    """
    anomalies = []

    for ticker, volumes in volume_data.items():
        if len(volumes) < 2:
            continue

        data_mean = statistics.mean(volumes)
        baseline = avg_baseline if avg_baseline is not None else data_mean

        if baseline == 0:
            continue

        try:
            data_std = statistics.stdev(volumes)
        except statistics.StatisticsError:
            data_std = 0.0

        for i, vol in enumerate(volumes):
            # Check ratio vs baseline
            ratio = vol / baseline if baseline != 0 else 0.0

            # Check z-score within the series
            z = _z_score(vol, data_mean, data_std)

            if ratio > VOLUME_RATIO_THRESHOLD or abs(z) > ZSCORE_THRESHOLD:
                an = _make_anomaly(
                    anomaly_type="Volume Anomaly",
                    description=(
                        f"{ticker} volume {vol:.0f} at index {i} is "
                        f"abnormal: ratio={ratio:.2f}x baseline={baseline:.0f}, "
                        f"z-score={z:.2f}. Potential accumulation or distribution signal."
                    ),
                    related_tickers=[ticker],
                )
                anomalies.append(an)
                # Only flag the first anomalous point per ticker to avoid spam
                break

    return anomalies


def detect_missing_correlation(etf_data, candidate_data):
    """Detect missing correlations between ETF and candidate price series.

    Computes Pearson r between each ETF and each candidate. Flags if
    |r| < CORRELATION_THRESHOLD (0.5), indicating an expected relationship
    has broken down.

    Args:
        etf_data: dict of ETF ticker -> list of prices
        candidate_data: dict of candidate ticker -> list of prices

    Returns:
        list of anomaly dicts
    """
    anomalies = []

    for etf_ticker, etf_prices in etf_data.items():
        for cand_ticker, cand_prices in candidate_data.items():
            n = min(len(etf_prices), len(cand_prices))
            if n < 2:
                continue

            r = _pearson_r(etf_prices[:n], cand_prices[:n])

            if abs(r) < CORRELATION_THRESHOLD:
                strength = "no" if abs(r) < 0.2 else "weak"
                an = _make_anomaly(
                    anomaly_type="Missing Correlation",
                    description=(
                        f"Correlation between {etf_ticker} and {cand_ticker} "
                        f"is r={r:.3f} ({strength} correlation, |r| < "
                        f"{CORRELATION_THRESHOLD}). Expected relationship "
                        f"appears to have broken down."
                    ),
                    related_tickers=[etf_ticker, cand_ticker],
                )
                anomalies.append(an)

    return anomalies


# ══════════════════════════════════════════════════════════════
# CIRCULAR FEEDBACK GUARD (FD #27 §4)
# ══════════════════════════════════════════════════════════════

def check_cooldown(anomaly_id, last_promoted_date, today, cooldown_days=30):
    """Check if an anomaly should be suppressed due to cooldown.

    Args:
        anomaly_id: str — the anomaly signature ID
        last_promoted_date: date or None — when this anomaly was last promoted
        today: date — current date for comparison
        cooldown_days: int — cooldown window (default 30)

    Returns:
        dict with keys:
            suppress: bool — True if anomaly should NOT fire
            cooldown_remaining_days: int — days remaining in cooldown (0 if allowed)
    """
    if last_promoted_date is None:
        return {"suppress": False, "cooldown_remaining_days": 0}

    delta = (today - last_promoted_date).days

    if delta < cooldown_days:
        return {
            "suppress": True,
            "cooldown_remaining_days": cooldown_days - delta,
        }

    return {"suppress": False, "cooldown_remaining_days": 0}


def record_promotion(anomaly_id, promotion_date):
    """Record that an anomaly was promoted (for circular feedback guard).

    Stores the promotion date in the in-memory tracker so that subsequent
    detection cycles can check the cooldown.

    Args:
        anomaly_id: str — the anomaly signature ID
        promotion_date: date — when the promotion occurred
    """
    _promotion_tracker[anomaly_id] = promotion_date


def clear_promotion_tracking():
    """Clear all promotion tracking state (for testing / reset)."""
    _promotion_tracker.clear()
