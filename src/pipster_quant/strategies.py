from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    direction: int
    confidence: float
    expected_edge: float
    stop_distance: float
    take_profit_distance: float
    rationale: str = ""


class BaseStrategy:
    def generate_signal(self, row, price: float) -> Signal:
        raise NotImplementedError


class TrendFollowingStrategy(BaseStrategy):
    def generate_signal(self, row, price: float) -> Signal:
        trend = float(row.get("trend_strength", 0.0))
        rsi = float(row.get("rsi_14", 50.0))
        atr = float(row.get("atr_14", 0.0))

        if trend > 0.01 and rsi > 52:
            direction = 1
        elif trend < -0.01 and rsi < 48:
            direction = -1
        else:
            direction = 0

        confidence = min(1.0, abs(trend) * 40.0 + abs(rsi - 50.0) / 100.0)
        stop_distance = max(atr * 1.2, 1e-8)
        take_profit_distance = max(stop_distance * 2.0, 1e-8)
        expected_edge = trend * 100.0
        return Signal(direction, confidence, expected_edge, stop_distance, take_profit_distance, "trend_following")


class MomentumStrategy(BaseStrategy):
    def generate_signal(self, row, price: float) -> Signal:
        roc = float(row.get("roc_10", 0.0))
        rsi = float(row.get("rsi_14", 50.0))
        atr = float(row.get("atr_14", 0.0))

        if roc > 0.01 and rsi > 55:
            direction = 1
        elif roc < -0.01 and rsi < 45:
            direction = -1
        else:
            direction = 0

        confidence = min(1.0, abs(roc) * 40.0 + abs(rsi - 50.0) / 100.0)
        stop_distance = max(atr * 1.5, 1e-8)
        take_profit_distance = max(stop_distance * 2.0, 1e-8)
        expected_edge = roc * 100.0
        return Signal(direction, confidence, expected_edge, stop_distance, take_profit_distance, "momentum")


class MeanReversionStrategy(BaseStrategy):
    def generate_signal(self, row, price: float) -> Signal:
        zscore = float(row.get("zscore_20", 0.0))
        atr = float(row.get("atr_14", 0.0))

        if zscore > 1.5:
            direction = -1
        elif zscore < -1.5:
            direction = 1
        else:
            direction = 0

        confidence = min(1.0, abs(zscore) / 3.0)
        stop_distance = max(atr * 1.8, 1e-8)
        take_profit_distance = max(stop_distance * 2.0, 1e-8)
        expected_edge = -zscore * 10.0
        return Signal(direction, confidence, expected_edge, stop_distance, take_profit_distance, "mean_reversion")


class BreakoutStrategy(BaseStrategy):
    def generate_signal(self, row, price: float) -> Signal:
        breakout = float(row.get("breakout_strength", 0.0))
        atr = float(row.get("atr_14", 0.0))

        if breakout > 0.6:
            direction = 1
        elif breakout < 0.4:
            direction = -1
        else:
            direction = 0

        confidence = min(1.0, abs(breakout - 0.5) * 2.0)
        stop_distance = max(atr * 1.5, 1e-8)
        take_profit_distance = max(stop_distance * 2.5, 1e-8)
        expected_edge = breakout * 50.0
        return Signal(direction, confidence, expected_edge, stop_distance, take_profit_distance, "breakout")


class RegimeAdaptiveStrategy(BaseStrategy):
    def __init__(self, base_strategy: BaseStrategy | None = None) -> None:
        self.base_strategy = base_strategy or TrendFollowingStrategy()

    def generate_signal(self, row, price: float) -> Signal:
        regime = str(row.get("regime", "RANGE"))
        signal = self.base_strategy.generate_signal(row, price)

        if regime == "RANGE":
            direction = signal.direction if signal.direction in {-1, 1} else 0
            confidence = min(1.0, signal.confidence * 0.9)
            return Signal(direction, confidence, signal.expected_edge, signal.stop_distance, signal.take_profit_distance, f"regime_adaptive:{regime}")

        if regime in {"TRENDING_UP", "TRENDING_DOWN"}:
            return signal

        if regime in {"HIGH_VOLATILITY", "TRANSITION"}:
            return Signal(0, 0.0, 0.0, signal.stop_distance, signal.take_profit_distance, f"regime_adaptive:{regime}")

        return signal


class EnsembleStrategy(BaseStrategy):
    def __init__(self, strategies: list[BaseStrategy] | None = None) -> None:
        self.strategies = strategies or [TrendFollowingStrategy(), MomentumStrategy(), MeanReversionStrategy(), BreakoutStrategy()]

    def generate_signal(self, row, price: float) -> Signal:
        signals = [strategy.generate_signal(row, price) for strategy in self.strategies]
        direction_scores = {1: 0.0, -1: 0.0, 0: 0.0}
        for signal in signals:
            direction_scores[signal.direction] += signal.confidence

        best_direction = max(direction_scores, key=direction_scores.get)
        confidence = direction_scores[best_direction] / max(sum(direction_scores.values()), 1e-8)
        stop_distance = max((signal.stop_distance for signal in signals), default=0.0)
        take_profit_distance = max((signal.take_profit_distance for signal in signals), default=0.0)
        expected_edge = sum(signal.expected_edge for signal in signals) / max(len(signals), 1)
        return Signal(int(best_direction), float(confidence), float(expected_edge), float(stop_distance), float(take_profit_distance), "ensemble")
