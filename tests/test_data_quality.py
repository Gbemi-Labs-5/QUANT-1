from pipster_quant.data_quality import validate_market_data


def test_validate_market_data_rejects_negative_spread_and_duplicates():
    rows = [
        {"timestamp": "2026-10-06T09:00:00Z", "symbol": "EURUSD", "bid": 1.09, "ask": 1.10, "spread": 0.01},
        {"timestamp": "2026-10-06T09:00:00Z", "symbol": "EURUSD", "bid": 1.09, "ask": 1.10, "spread": 0.01},
        {"timestamp": "2026-10-06T09:00:01Z", "symbol": "EURUSD", "bid": 1.10, "ask": 1.08, "spread": -0.02},
    ]

    result = validate_market_data(rows)
    assert result["duplicate_timestamps"] == 1
    assert result["negative_spreads"] == 1
    assert result["valid"] is False
