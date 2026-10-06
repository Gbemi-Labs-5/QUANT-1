from __future__ import annotations

import pandas as pd


def detect_regime(features: pd.DataFrame | pd.Series) -> str:
    if isinstance(features, pd.Series):
        row = features
        trend = float(row.get("trend_strength", 0.0))
        realized_vol = float(row.get("realized_vol_20", 0.0))
        zscore = float(row.get("zscore_20", 0.0))
        rsi = float(row.get("rsi_14", 50.0))
        if abs(trend) > 0.025 and abs(zscore) > 0.8:
            if trend > 0:
                return "TRENDING_UP"
            return "TRENDING_DOWN"
        if realized_vol > 0.002:
            return "HIGH_VOLATILITY"
        if abs(zscore) < 0.75 and abs(trend) < 0.015:
            return "RANGE"
        if rsi < 30 or rsi > 70:
            return "TRANSITION"
        return "RANGE"

    if features.empty:
        return "TRANSITION"

    trend = float(features["trend_strength"].iloc[-1])
    realized_vol = float(features["realized_vol_20"].iloc[-1])
    zscore = float(features["zscore_20"].iloc[-1])
    rsi = float(features["rsi_14"].iloc[-1])
    volatility_threshold = float(features["realized_vol_20"].quantile(0.75))
    low_volatility_threshold = float(features["realized_vol_20"].quantile(0.25))

    if abs(trend) > 0.025 and abs(zscore) > 0.8:
        if trend > 0:
            return "TRENDING_UP"
        return "TRENDING_DOWN"

    if realized_vol > max(volatility_threshold * 1.2, 0.002):
        return "HIGH_VOLATILITY"

    if abs(zscore) < 0.75 and abs(trend) < 0.015:
        return "RANGE"

    if realized_vol < max(low_volatility_threshold * 0.8, 1e-8):
        return "LOW_VOLATILITY"

    if rsi < 30 or rsi > 70:
        return "TRANSITION"

    return "RANGE"
