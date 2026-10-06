from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

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
    rows: int = 0
    instruments: list[str] = field(default_factory=list)
    missingness: dict[str, float] = field(default_factory=dict)
    anomalies: dict[str, int] = field(default_factory=dict)
    cleaning_decisions: list[str] = field(default_factory=list)
    quality_score: float = 0.0
    timezone: str = "UNSPECIFIED"
    frequency: str = "UNSPECIFIED"


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


class CSVMarketDataProvider(DataProvider):
    def __init__(self, path: str | Path, symbol: str | None = None, timestamp_col: str = "Date") -> None:
        self.path = Path(path)
        self.symbol = symbol
        self.timestamp_col = timestamp_col

    def load(self) -> pd.DataFrame:
        frame = pd.read_csv(self.path)
        frame = frame.copy()
        if self.timestamp_col in frame.columns:
            frame[self.timestamp_col] = pd.to_datetime(frame[self.timestamp_col], errors="coerce")
        if "timestamp" not in frame.columns and self.timestamp_col in frame.columns:
            frame["timestamp"] = frame[self.timestamp_col]
        if self.symbol is not None and "symbol" not in frame.columns:
            frame["symbol"] = self.symbol
        if "Date" in frame.columns and "timestamp" not in frame.columns:
            frame["timestamp"] = pd.to_datetime(frame["Date"], errors="coerce")
        if "AAPL.Close" in frame.columns and "close" not in frame.columns:
            frame["close"] = frame["AAPL.Close"]
        if "AAPL.Open" in frame.columns and "open" not in frame.columns:
            frame["open"] = frame["AAPL.Open"]
        if "AAPL.High" in frame.columns and "high" not in frame.columns:
            frame["high"] = frame["AAPL.High"]
        if "AAPL.Low" in frame.columns and "low" not in frame.columns:
            frame["low"] = frame["AAPL.Low"]
        if "AAPL.Volume" in frame.columns and "volume" not in frame.columns:
            frame["volume"] = frame["AAPL.Volume"]
        if "AAPL.Adjusted" in frame.columns and "adjusted" not in frame.columns:
            frame["adjusted"] = frame["AAPL.Adjusted"]
        if "symbol" not in frame.columns:
            frame["symbol"] = self.symbol or "UNKNOWN"
        frame = frame.sort_values("timestamp").reset_index(drop=True)
        return frame


class ParquetMarketDataProvider(DataProvider):
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        return pd.read_parquet(self.path)


def validate_market_frame(frame: pd.DataFrame, *, strict: bool = False) -> DataQualityReport:
    if frame.empty:
        return DataQualityReport(False, 0, 0, 0, False)

    required = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        return DataQualityReport(False, 0, 0, len(missing), False, rows=len(frame), anomalies={"missing_columns": len(missing)})

    cleaned = frame.copy()
    cleaning_decisions: list[str] = []
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], errors="coerce")
    if cleaned["timestamp"].isna().any():
        cleaning_decisions.append("dropped_rows_with_invalid_timestamps")
        cleaned = cleaned.dropna(subset=["timestamp"]).copy()

    duplicate_timestamps = int(cleaned.duplicated(subset=["timestamp", "symbol"]).sum())
    if duplicate_timestamps:
        cleaning_decisions.append("dropped_duplicate_timestamp_rows")
        cleaned = cleaned.drop_duplicates(subset=["timestamp", "symbol"], keep="last").copy()

    for col in ["open", "high", "low", "close", "volume"]:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        if cleaned[col].isna().any():
            cleaning_decisions.append(f"dropped_rows_with_invalid_{col}")
            cleaned = cleaned.dropna(subset=[col]).copy()

    impossible_ohlc = int(((cleaned["high"] < cleaned["low"]) | (cleaned["high"] < cleaned["close"]) | (cleaned["low"] > cleaned["close"]) | (cleaned["low"] > cleaned["open"]) | (cleaned["high"] < cleaned["open"])).sum())
    if impossible_ohlc:
        cleaning_decisions.append("dropped_rows_with_impossible_ohlc")
        cleaned = cleaned.loc[~((cleaned["high"] < cleaned["low"]) | (cleaned["high"] < cleaned["close"]) | (cleaned["low"] > cleaned["close"]) | (cleaned["low"] > cleaned["open"]) | (cleaned["high"] < cleaned["open"]))].copy()

    negative_prices = int(((cleaned[["open", "high", "low", "close"]] <= 0).any(axis=1)).sum())
    if negative_prices:
        cleaning_decisions.append("dropped_non_positive_prices")
        cleaned = cleaned.loc[~((cleaned[["open", "high", "low", "close"]] <= 0).any(axis=1))].copy()

    ordered = bool(cleaned["timestamp"].is_monotonic_increasing)
    if not ordered:
        cleaning_decisions.append("sorted_by_timestamp")
        cleaned = cleaned.sort_values("timestamp").reset_index(drop=True)

    missing_values = int(cleaned.isna().sum().sum())
    anomalies = {
        "duplicate_timestamps": int(duplicate_timestamps),
        "impossible_ohlc": int(impossible_ohlc),
        "negative_prices": int(negative_prices),
        "missing_values": int(missing_values),
    }

    frequency = pd.infer_freq(cleaned["timestamp"].sort_values()) if len(cleaned) > 2 else "UNSPECIFIED"
    missingness = {column: float(cleaned[column].isna().mean()) for column in cleaned.columns}
    quality_score = max(0.0, 1.0 - (sum(anomalies.values()) / max(len(cleaned), 1)))
    report = DataQualityReport(
        valid=bool(cleaned.empty is False and not bool(duplicate_timestamps) and not bool(impossible_ohlc) and not bool(negative_prices) and ordered and missing_values == 0),
        duplicate_timestamps=int(duplicate_timestamps),
        negative_spreads=int((cleaned.get("ask", cleaned["close"]) < cleaned.get("bid", cleaned["close"]) if "ask" in cleaned.columns and "bid" in cleaned.columns else 0).sum()),
        missing_values=int(missing_values),
        ordered=bool(ordered),
        rows=int(len(cleaned)),
        instruments=sorted(cleaned["symbol"].dropna().unique().astype(str).tolist()),
        missingness={key: float(value) for key, value in missingness.items()},
        anomalies=anomalies,
        cleaning_decisions=cleaning_decisions,
        quality_score=float(quality_score),
        timezone="UTC" if cleaned["timestamp"].dt.tz is not None else "NAIVE",
        frequency=str(frequency),
    )
    if strict and not report.valid:
        raise ValueError(f"Data validation failed: {report.anomalies}")
    return report
