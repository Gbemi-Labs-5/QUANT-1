from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .data_pipeline import SyntheticMarketDataProvider, validate_market_frame
from .features import compute_feature_frame
from .regime import detect_regime
from .strategies import BreakoutStrategy, EnsembleStrategy, MeanReversionStrategy, MomentumStrategy, Signal, TrendFollowingStrategy


@dataclass
class StrategyEvaluation:
    strategy: str
    total_return: float
    win_rate: float
    sharpe: float
    average_trade: float
    num_trades: int


def _evaluate_strategy(frame: pd.DataFrame, strategy_name: str, strategy) -> StrategyEvaluation:
    features = compute_feature_frame(frame, lookback=14)
    if "regime" not in features.columns:
        features["regime"] = "RANGE"

    equity = 1.0
    pnl_history: list[float] = []
    trades = 0
    wins = 0

    for index in range(1, len(features)):
        row = features.iloc[index].copy()
        row["regime"] = detect_regime(features.iloc[: index + 1].copy())
        signal = strategy.generate_signal(row, float(row["close"]))
        prev_close = float(features.iloc[index - 1]["close"])
        current_close = float(row["close"])

        if signal.direction == 0:
            continue

        pnl = ((current_close / prev_close) - 1.0) * signal.direction
        equity *= 1.0 + pnl
        pnl_history.append(float(pnl))
        trades += 1
        if pnl > 0:
            wins += 1

    win_rate = wins / max(trades, 1)
    mean_return = sum(pnl_history) / max(len(pnl_history), 1)
    sharpe = (mean_return / (pd.Series(pnl_history).std(ddof=0) + 1e-8)) if len(pnl_history) > 1 else 0.0

    return StrategyEvaluation(
        strategy=strategy_name,
        total_return=float(equity - 1.0),
        win_rate=float(win_rate),
        sharpe=float(sharpe),
        average_trade=float(mean_return),
        num_trades=int(trades),
    )


def run_research() -> dict:
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=240, seed=4)
    frame = provider.load()
    feature_frame = compute_feature_frame(frame, lookback=14)
    feature_frame["regime"] = feature_frame.apply(detect_regime, axis=1)

    strategies = {
        "trend": TrendFollowingStrategy(),
        "momentum": MomentumStrategy(),
        "mean_reversion": MeanReversionStrategy(),
        "breakout": BreakoutStrategy(),
        "ensemble": EnsembleStrategy(),
    }

    results = [
        _evaluate_strategy(feature_frame, name, strategy)
        for name, strategy in strategies.items()
    ]
    ranking = sorted(results, key=lambda item: (item.total_return, item.sharpe), reverse=True)
    return {
        "dataset": "synthetic_test",
        "results": [result.__dict__ for result in ranking],
        "best_strategy": ranking[0].strategy if ranking else None,
        "quality": validate_market_frame(frame).__dict__,
    }


def save_report(results: dict, out_dir: str | Path) -> Path:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    json_path = path / "research_report.json"
    markdown_path = path / "research_report.md"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    markdown_lines = [
        "# Research Report",
        "",
        f"- Best strategy: {results.get('best_strategy', 'n/a')}",
        "",
    ]
    for result in results.get("results", []):
        markdown_lines.append(
            f"- {result['strategy']}: return={result['total_return']:.4f}, win_rate={result['win_rate']:.3f}, sharpe={result['sharpe']:.3f}"
        )
    markdown_path.write_text("\n".join(markdown_lines), encoding="utf-8")
    return json_path
