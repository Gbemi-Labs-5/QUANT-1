from pipster_quant.risk import CompetitionRiskEngine, RiskEngine


def test_risk_engine_rejects_over_limit_positions():
    engine = RiskEngine(daily_drawdown_limit=0.08, max_drawdown_limit=0.12, max_exposure=0.15)

    decision = engine.evaluate(current_equity=1000.0, proposed_exposure=0.20, daily_pnl=-0.10)

    assert decision["allowed"] is False
    assert "max_exposure" in decision["reasons"]


def test_competition_risk_engine_reports_standard_analytics():
    engine = CompetitionRiskEngine(daily_drawdown_limit=0.05, max_drawdown_limit=0.20)

    metrics = engine.evaluate_run(
        equity_curve=[100.0, 101.0, 102.0, 99.0, 103.0],
        daily_pnl=[1.0, 1.0, -3.0, 4.0],
        exposure=0.10,
        position_count=2,
        concentration=0.25,
    )

    assert metrics.analytics is not None
    assert metrics.analytics.sharpe_ratio >= -10.0
    assert metrics.analytics.win_rate > 0.0
    assert metrics.analytics.cumulative_return >= -1.0
    assert metrics.analytics.max_drawdown >= 0.0
