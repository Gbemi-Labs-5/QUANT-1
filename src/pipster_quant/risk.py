from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskEngine:
    daily_drawdown_limit: float = 0.08
    max_drawdown_limit: float = 0.12
    max_exposure: float = 0.15
    max_position_size: float = 1.0
    max_daily_contribution: float | None = None
    enabled: bool = True
    _decision_log: list[str] = field(default_factory=list, init=False)

    def evaluate(self, *, current_equity: float, proposed_exposure: float, daily_pnl: float, gross_exposure: float | None = None, net_exposure: float | None = None, current_drawdown: float | None = None, daily_contribution: float | None = None, position_count: int = 1) -> dict:
        reasons: list[str] = []
        self._decision_log = []

        gross_exposure = float(gross_exposure if gross_exposure is not None else abs(proposed_exposure))
        net_exposure = float(net_exposure if net_exposure is not None else proposed_exposure)
        current_drawdown = float(current_drawdown if current_drawdown is not None else 0.0)
        daily_contribution = float(daily_contribution if daily_contribution is not None else 0.0)

        if abs(proposed_exposure) > self.max_exposure:
            reasons.append("max_exposure")
        if gross_exposure > self.max_exposure:
            reasons.append("gross_exposure")
        if daily_pnl < -self.daily_drawdown_limit * current_equity:
            reasons.append("daily_drawdown")
        if abs(proposed_exposure) > self.max_position_size:
            reasons.append("position_size")
        if current_equity <= 0:
            reasons.append("non_positive_equity")
        if self.max_daily_contribution is not None and abs(daily_contribution) > self.max_daily_contribution:
            reasons.append("daily_contribution")
        if abs(net_exposure) > self.max_exposure:
            reasons.append("net_exposure")
        if position_count <= 0:
            reasons.append("empty_position_count")
        if current_drawdown > self.max_drawdown_limit:
            reasons.append("max_drawdown")

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
            "gross_exposure": gross_exposure,
            "net_exposure": net_exposure,
            "current_drawdown": current_drawdown,
            "daily_contribution": daily_contribution,
            "position_count": position_count,
        }


@dataclass
class PortfolioMetrics:
    equity_curve: list[float]
    daily_pnl: list[float]
    cumulative_pnl: float
    current_drawdown: float
    max_drawdown: float
    trading_days: int
    profitable_days: int
    losing_days: int
    largest_winning_day: float
    largest_losing_day: float
    max_single_day_contribution: float
    exposure: float
    gross_exposure: float
    net_exposure: float
    position_count: int
    concentration: float
    rule_violations: list[str]


class CompetitionRiskEngine(RiskEngine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def evaluate_run(self, equity_curve: list[float], daily_pnl: list[float], exposure: float = 0.0, position_count: int = 0, concentration: float = 0.0) -> PortfolioMetrics:
        if not equity_curve:
            return PortfolioMetrics([], [], 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, [])

        cumulative_pnl = equity_curve[-1] - equity_curve[0]
        running_peak = max(equity_curve)
        drawdown = [max(0.0, (peak - value) / max(peak, 1e-8)) for value, peak in zip(equity_curve, [max(equity_curve[: i + 1]) for i in range(len(equity_curve))])]
        current_drawdown = drawdown[-1] if drawdown else 0.0
        max_drawdown = max(drawdown) if drawdown else 0.0
        trading_days = len(daily_pnl)
        profitable_days = sum(1 for p in daily_pnl if p > 0)
        losing_days = sum(1 for p in daily_pnl if p < 0)
        largest_winning_day = max(daily_pnl) if daily_pnl else 0.0
        largest_losing_day = min(daily_pnl) if daily_pnl else 0.0
        max_single_day_contribution = max(abs(value) for value in daily_pnl) if daily_pnl else 0.0

        violations: list[str] = []
        if self.max_drawdown_limit is not None and max_drawdown > self.max_drawdown_limit:
            violations.append("max_drawdown")
        if self.daily_drawdown_limit is not None and any(d < -self.daily_drawdown_limit * max(1.0, equity_curve[0]) for d in daily_pnl):
            violations.append("daily_drawdown")
        if self.max_daily_contribution is not None and max_single_day_contribution > self.max_daily_contribution:
            violations.append("daily_contribution")

        return PortfolioMetrics(
            equity_curve=equity_curve,
            daily_pnl=daily_pnl,
            cumulative_pnl=float(cumulative_pnl),
            current_drawdown=float(current_drawdown),
            max_drawdown=float(max_drawdown),
            trading_days=int(trading_days),
            profitable_days=int(profitable_days),
            losing_days=int(losing_days),
            largest_winning_day=float(largest_winning_day),
            largest_losing_day=float(largest_losing_day),
            max_single_day_contribution=float(max_single_day_contribution),
            exposure=float(exposure),
            gross_exposure=float(exposure if exposure >= 0 else abs(exposure)),
            net_exposure=float(exposure),
            position_count=int(position_count),
            concentration=float(concentration),
            rule_violations=violations,
        )
