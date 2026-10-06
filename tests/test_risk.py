from pipster_quant.risk import RiskEngine


def test_risk_engine_rejects_over_limit_positions():
    engine = RiskEngine(daily_drawdown_limit=0.08, max_drawdown_limit=0.12, max_exposure=0.15)

    decision = engine.evaluate(current_equity=1000.0, proposed_exposure=0.20, daily_pnl=-0.10)

    assert decision["allowed"] is False
    assert "max_exposure" in decision["reasons"]
