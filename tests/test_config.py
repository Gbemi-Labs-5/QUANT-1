from pipster_quant.config import load_default_rules


def test_default_pipster_rules_are_conservative_and_explicit():
    rules = load_default_rules()

    assert rules.contest_name == "Pipster Halloween 2026"
    assert rules.status == "public-source-only"
    assert rules.timezone == "UTC"
    assert rules.session_open_local == "08:00"
    assert rules.session_close_local == "16:00"
    assert rules.unknowns["start_date"] is None
    assert rules.unknowns["daily_drawdown_limit"] is None
