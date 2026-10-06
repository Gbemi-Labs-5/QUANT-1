from pipster_quant.ai_schema import AIEvent, validate_event


def test_aievent_validates_required_fields():
    payload = {
        "event_id": "evt-001",
        "source": "ECB",
        "published_at": "2026-10-06T09:00:00Z",
        "event_type": "macro",
        "affected_assets": ["EURUSD"],
        "event_severity": 0.9,
        "market_relevance": 0.8,
        "directional_bias": -0.2,
        "volatility_risk": 0.7,
        "confidence": 0.88,
        "facts": ["ECB rate decision"],
        "uncertainties": [],
    }

    event = AIEvent(**payload)
    assert validate_event(event.model_dump()) == payload
