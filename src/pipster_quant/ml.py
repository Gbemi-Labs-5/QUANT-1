from __future__ import annotations

import numpy as np
import pandas as pd


try:
    from sklearn.linear_model import LogisticRegression
except Exception:  # pragma: no cover
    LogisticRegression = None


FEATURE_COLUMNS = [
    "return_1",
    "trend_strength",
    "rsi_14",
    "roc_10",
    "zscore_20",
    "atr_14",
    "realized_vol_20",
    "spread_pct",
]


def prepare_direction_labels(features: pd.DataFrame, horizon: int = 5) -> pd.Series:
    if features.empty:
        return pd.Series(dtype=int)

    future = features["close"].shift(-horizon)
    label = (future - features["close"]).gt(0).astype(int)
    return label.fillna(0).astype(int)


def fit_direction_model(features: pd.DataFrame, horizon: int = 5):
    if LogisticRegression is None:
        raise ImportError("scikit-learn is required to train the direction model")

    frame = features.copy()
    frame["target"] = prepare_direction_labels(frame, horizon=horizon)
    usable = frame.dropna(subset=["target"] + FEATURE_COLUMNS)
    if len(usable) < 10:
        raise ValueError("Not enough data to train the direction model")

    model = LogisticRegression(max_iter=2000)
    X = usable[FEATURE_COLUMNS].to_numpy(dtype=float)
    y = usable["target"].to_numpy(dtype=int)
    model.fit(X, y)
    return model, usable


def predict_direction_probability(model, row: pd.Series) -> float:
    if model is None:
        return 0.5

    values = np.asarray([[float(row.get(column, 0.0)) for column in FEATURE_COLUMNS]], dtype=float)
    probability = model.predict_proba(values)[0, 1]
    return float(np.clip(probability, 0.0, 1.0))
