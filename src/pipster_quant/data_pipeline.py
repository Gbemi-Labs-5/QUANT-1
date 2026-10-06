from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable, Sequence

import numpy as np
import pandas as pd


class DataProvider:
    def load(self) -> pd.DataFrame:
        raise NotImplementedError


@dataclass
class DataQualityReport:
    valid: bool
    duplicate_timestamps: int
    negative_spreads: int
    missing_values: int
    ordered: bool


class SyntheticMarketDataProvider(DataProvider):
    def __init__(
        self,
        symbols: Sequence[str] | None = None,
        rows: int = 200,
        seed: int = 0,
        freq: str = "1min",
        start: datetime | None = None,
    ) -> None:
        self.symbols = list(symbols or ["BTCUSD"])
        self.rows = int(rows)
        self.seed = int(seed)
        self.freq = freq
        self.start = start or datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc)

    def load(self) -> pd.DataFrame:
        rng = np.random.default_rng(self.seed)
        frame_list: list[pd.DataFrame] = []

        for index, symbol in enumerate(self.symbols):
            drift = 0.00018 * np.arange(self.rows, dtype=float)
            noise = rng.normal(0.0, 0.0025, size=self.rows)
            baseline = 100.0 + np.cumsum(drift + noise)
            close = baseline.copy()
            open_ = np.empty(self.rows, dtype=float)
            high = np.empty(self.rows, dtype=float)
            low = np.empty(self.rows, dtype=float)
            volume = rng.integers(100, 600, size=self.rows)

            open_[0] = close[0]
            for i in range(1, self.rows):
                open_[i] = close[i - 1]
                high[i] = max(open_[i], close[i]) * (1.0 + abs(noise[i]) * 1.7)
                low[i] = min(open_[i], close[i]) * (1.0 - abs(noise[i]) * 1.7)

            if self.rows > 1:
                high[0] = max(close[0], open_[0]) * 1.05
                low[0] = min(close[0], open_[0]) * 0.95

            spread = np.maximum(0.20, 0.35 + np.abs(rng.normal(0.0, 0.1, size=self.rows)))
            bid = close - (spread / 2.0)
            ask = close + (spread / 2.0)
            timestamps = pd.date_range(self.start + timedelta(minutes=index * 5), periods=self.rows, freq=self.freq)
            df = pd.DataFrame(
                {
                    "timestamp": timestamps,
                    "symbol": symbol,
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "bid": bid,
                    "ask": ask,
                }
            )
            frame_list.append(df)

        combined = pd.concat(frame_list, ignore_index=True)
        combined = combined.sort_values("timestamp").reset_index(drop=True)
        return combined


def validate_market_frame(frame: pd.DataFrame) -> DataQualityReport:
    if frame.empty:
        return DataQualityReport(False, 0, 0, 0, False)

    required = {"timestamp", "symbol", "open", "high", "low", "close", "volume", "bid", "ask"}
    missing = required - set(frame.columns)
    if missing:
        return DataQualityReport(False, 0, 0, len(missing), False)

    ordered = bool(frame["timestamp"].is_monotonic_increasing)
    duplicate_timestamps = int(frame.duplicated(subset=["timestamp", "symbol"]).sum())
    negative_spreads = int((frame["ask"] < frame["bid"]).sum())
    missing_values = int(frame.isna().sum().sum())

    return DataQualityReport(
        valid=ordered and duplicate_timestamps == 0 and negative_spreads == 0 and missing_values == 0,
        duplicate_timestamps=duplicate_timestamps,
        negative_spreads=negative_spreads,
        missing_values=missing_values,
        ordered=ordered,
    )
