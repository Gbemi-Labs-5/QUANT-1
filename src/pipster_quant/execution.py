from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

import pandas as pd


@dataclass
class MarketOrder:
    symbol: str
    quantity: int
    timestamp: datetime
    side: str
    order_id: str = field(default_factory=lambda: uuid4().hex)


@dataclass
class OrderEvent:
    order: MarketOrder
    type: str = "order"


class EventDrivenBacktester:
    def __init__(self, market_data: pd.DataFrame) -> None:
        self.market_data = market_data.copy().sort_values("timestamp").reset_index(drop=True)
        self.fill_log: list[dict] = []
        self.order_log: list[dict] = []
        self._seen_order_ids: set[str] = set()
        self._seen_order_keys: set[tuple[str, pd.Timestamp]] = set()

    def _bar_for_time(self, timestamp: datetime) -> pd.Series | None:
        if self.market_data.empty:
            return None
        relevant = self.market_data[self.market_data["timestamp"] <= timestamp]
        if relevant.empty:
            return None
        return relevant.iloc[-1]

    def process_order(self, event: OrderEvent) -> dict:
        order = event.order
        if order.quantity <= 0:
            return {"accepted": False, "fills": [], "reason": "non_positive_quantity"}

        if order.side.lower() not in {"buy", "sell"}:
            return {"accepted": False, "fills": [], "reason": "unsupported_side"}

        order_key = (order.symbol, pd.Timestamp(order.timestamp))
        if order.order_id in self._seen_order_ids or order_key in self._seen_order_keys:
            return {"accepted": False, "fills": [], "reason": "duplicate_order"}

        bar = self._bar_for_time(order.timestamp)
        if bar is None:
            return {"accepted": False, "fills": [], "reason": "no_historical_bar"}

        fill_price = float(bar["ask"]) if order.side.lower() == "buy" else float(bar["bid"])
        fill_quantity = int(order.quantity)

        fill = {
            "order_id": order.order_id,
            "symbol": order.symbol,
            "timestamp": pd.Timestamp(order.timestamp),
            "side": order.side,
            "price": fill_price,
            "quantity": fill_quantity,
            "execution_type": "market",
        }

        self._seen_order_ids.add(order.order_id)
        self._seen_order_keys.add((order.symbol, pd.Timestamp(order.timestamp)))
        self.fill_log.append(fill)
        self.order_log.append({"order_id": order.order_id, "timestamp": order.timestamp, "symbol": order.symbol})
        return {"accepted": True, "fills": [fill], "execution_price": fill_price, "bar_timestamp": bar["timestamp"]}

    def process_signal(self, signal, row: pd.Series, risk_limit: float = 1.0) -> dict:
        if signal.direction == 0:
            return {"accepted": False, "fills": [], "reason": "flat_signal"}

        if abs(signal.direction) > 1:
            return {"accepted": False, "fills": [], "reason": "invalid_signal"}

        order_side = "buy" if signal.direction > 0 else "sell"
        order = MarketOrder(
            symbol=str(row.get("symbol", "UNKNOWN")),
            quantity=max(1, int(risk_limit)),
            timestamp=pd.Timestamp(row["timestamp"]),
            side=order_side,
        )
        return self.process_order(OrderEvent(order=order, type="order"))
