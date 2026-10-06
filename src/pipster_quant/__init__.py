"""Pipster quant research and execution scaffolding."""

__all__ = [
    "AIEvent",
    "PipsterRules",
    "RiskEngine",
    "SessionBoundary",
    "TradingClock",
    "SyntheticMarketDataProvider",
    "compute_feature_frame",
    "detect_regime",
    "TrendFollowingStrategy",
    "MomentumStrategy",
    "MeanReversionStrategy",
    "BreakoutStrategy",
    "EnsembleStrategy",
    "EventDrivenBacktester",
    "load_default_rules",
    "load_rules",
    "validate_event",
    "validate_market_data",
]

from .ai_schema import AIEvent, validate_event
from .config import PipsterRules, load_default_rules, load_rules
from .data_pipeline import SyntheticMarketDataProvider
from .data_quality import validate_market_data
from .execution import EventDrivenBacktester
from .features import compute_feature_frame
from .ml import fit_direction_model, predict_direction_probability
from .regime import detect_regime
from .risk import RiskEngine
from .strategies import (
    BreakoutStrategy,
    EnsembleStrategy,
    MeanReversionStrategy,
    MomentumStrategy,
    TrendFollowingStrategy,
)
from .time_contract import SessionBoundary, TradingClock
