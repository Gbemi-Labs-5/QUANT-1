from datetime import datetime, timedelta, timezone

import pandas as pd

from pipster_quant.data_pipeline import SyntheticMarketDataProvider
from pipster_quant.execution import EventDrivenBacktester, MarketOrder, OrderEvent
from pipster_quant.features import compute_feature_frame
from pipster_quant.regime import detect_regime
from pipster_quant.strategies import TrendFollowingStrategy


def test_synthetic_provider_generates_ordered_market_data():
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=50, seed=7)
    data = provider.load()

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == [
        "timestamp",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "bid",
        "ask",
    ]
    assert len(data) == 50
    assert data["timestamp"].is_monotonic_increasing
    assert (data["ask"] >= data["bid"]).all()


def test_feature_frame_includes_momentum_and_mean_reversion_features():
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=120, seed=11)
    data = provider.load()
    features = compute_feature_frame(data, lookback=14)

    assert "rsi_14" in features.columns
    assert "zscore_20" in features.columns
    assert "atr_14" in features.columns
    assert "trend_strength" in features.columns
    assert not features.isna().all().all()


def test_regime_detector_identifies_market_state():
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=220, seed=23)
    data = provider.load()
    features = compute_feature_frame(data, lookback=14)
    regime = detect_regime(features)

    assert regime in {"TRENDING_UP", "TRENDING_DOWN", "RANGE", "HIGH_VOLATILITY", "LOW_VOLATILITY", "TRANSITION"}


def test_strategy_signal_has_direction_confidence_and_stop_distance():
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=200, seed=29)
    data = provider.load()
    features = compute_feature_frame(data, lookback=14)
    strategy = TrendFollowingStrategy()
    signal = strategy.generate_signal(features.iloc[-1], price=float(features.iloc[-1]["close"]))

    assert signal.direction in {-1, 0, 1}
    assert 0.0 <= signal.confidence <= 1.0
    assert signal.stop_distance >= 0.0
    assert signal.take_profit_distance >= 0.0


def test_backtester_prevents_lookahead_and_records_fill():
    now = datetime(2026, 10, 6, 9, 30, tzinfo=timezone.utc)
    tz = timezone.utc
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=40, seed=31)
    frame = provider.load().copy()
    frame["timestamp"] = [now + timedelta(minutes=i) for i in range(len(frame))]
    frame["ask"] = frame["close"] + 0.5
    frame["bid"] = frame["close"] - 0.5

    backtester = EventDrivenBacktester(frame)
    order = MarketOrder(symbol="BTCUSD", quantity=1, timestamp=frame.iloc[10]["timestamp"], side="buy")
    event = OrderEvent(order=order, type="order")

    result = backtester.process_order(event)
    assert result["accepted"] is True
    assert result["fills"][0]["quantity"] == 1

    with_lag = MarketOrder(symbol="BTCUSD", quantity=1, timestamp=frame.iloc[10]["timestamp"], side="buy")
    with_lag_event = OrderEvent(order=with_lag, type="order")
    lookahead = backtester.process_order(with_lag_event)
    assert len(lookahead["fills"]) == 0 or lookahead["accepted"] is False
