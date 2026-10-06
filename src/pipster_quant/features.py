from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_float(value: float | pd.Series, default: float = 0.0):
    if isinstance(value, pd.Series):
        return value.fillna(default).replace([np.inf, -np.inf], default)
    if pd.isna(value):
        return default
    if np.isinf(value):
        return default
    return float(value)


def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = (-delta.clip(upper=0)).replace(0, 0.0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def compute_feature_frame(frame: pd.DataFrame, lookback: int = 14) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()

    out = frame.copy().sort_values("timestamp").reset_index(drop=True)
    for column in ["close", "high", "low", "volume", "bid", "ask"]:
        out[column] = pd.to_numeric(out[column], errors="coerce")

    out["return_1"] = out["close"].pct_change().fillna(0.0)
    out["sma_20"] = out["close"].rolling(20).mean()
    out["ema_12"] = out["close"].ewm(span=12, adjust=False).mean()
    out["ema_26"] = out["close"].ewm(span=26, adjust=False).mean()
    out["trend_strength"] = (out["close"] - out["sma_20"]) / out["sma_20"].replace(0, np.nan)
    out["trend_strength"] = out["trend_strength"].fillna(0.0)

    out["rsi_14"] = _rsi(out["close"], 14)
    out["roc_10"] = out["close"].pct_change(10).fillna(0.0)
    out["momentum_10"] = out["close"].diff(10).fillna(0.0)

    prev_close = out["close"].shift(1)
    tr = pd.concat(
        [
            out["high"] - out["low"],
            (out["high"] - prev_close).abs(),
            (out["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out["atr_14"] = tr.rolling(14).mean().fillna(0.0)
    out["realized_vol_20"] = out["return_1"].rolling(20).std().fillna(0.0)
    out["rolling_std_20"] = out["close"].rolling(20).std().fillna(0.0)
    out["zscore_20"] = (
        (out["close"] - out["close"].rolling(20).mean())
        / out["close"].rolling(20).std().replace(0, np.nan)
    ).fillna(0.0)

    out["rolling_high_20"] = out["close"].rolling(20).max().fillna(out["close"])
    out["rolling_low_20"] = out["close"].rolling(20).min().fillna(out["close"])
    out["breakout_strength"] = (out["close"] - out["rolling_low_20"]) / (out["rolling_high_20"] - out["rolling_low_20"]).replace(0, np.nan)
    out["breakout_strength"] = out["breakout_strength"].fillna(0.0)

    spread = out["ask"] - out["bid"]
    out["spread"] = spread.fillna(0.0)
    out["spread_pct"] = (spread / out["close"].replace(0, np.nan)).fillna(0.0)
    out["volatility_regime"] = np.where(out["realized_vol_20"] > out["realized_vol_20"].quantile(0.75), 1.0, 0.0)

    out = out.replace([np.inf, -np.inf], 0.0).fillna(0.0)
    return out
