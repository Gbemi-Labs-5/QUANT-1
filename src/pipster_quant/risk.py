from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskEngine:
    daily_drawdown_limit: float = 0.08
    max_drawdown_limit: float = 0.12
    max_exposure: float = 0.15
    max_position_size: float = 1.0
    enabled: bool = True
    _decision_log: list[str] = field(default_factory=list, init=False)

    def evaluate(self, *, current_equity: float, proposed_exposure: float, daily_pnl: float) -> dict:
        reasons: list[str] = []
        self._decision_log = []

        if proposed_exposure > self.max_exposure:
            reasons.append("max_exposure")
        if daily_pnl < -self.daily_drawdown_limit * current_equity:
            reasons.append("daily_drawdown")
        if abs(proposed_exposure) > self.max_position_size:
            reasons.append("position_size")
        if current_equity <= 0:
            reasons.append("non_positive_equity")

        allowed = len(reasons) == 0 and self.enabled
        if allowed:
            self._decision_log.append("allowed")
        else:
            self._decision_log.extend(reasons)

        return {
            "allowed": allowed,
            "reasons": reasons,
            "decision_log": self._decision_log,
            "current_equity": current_equity,
            "proposed_exposure": proposed_exposure,
            "daily_pnl": daily_pnl,
        }
