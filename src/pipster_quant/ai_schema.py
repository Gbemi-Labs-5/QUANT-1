from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


REQUIRED_FIELDS = {
    "event_id",
    "source",
    "published_at",
    "event_type",
    "affected_assets",
    "event_severity",
    "market_relevance",
    "directional_bias",
    "volatility_risk",
    "confidence",
    "facts",
    "uncertainties",
}


@dataclass
class AIEvent:
    event_id: str
    source: str
    published_at: str
    event_type: str
    affected_assets: list[str]
    event_severity: float
    market_relevance: float
    directional_bias: float
    volatility_risk: float
    confidence: float
    facts: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "source": self.source,
            "published_at": self.published_at,
            "event_type": self.event_type,
            "affected_assets": self.affected_assets,
            "event_severity": self.event_severity,
            "market_relevance": self.market_relevance,
            "directional_bias": self.directional_bias,
            "volatility_risk": self.volatility_risk,
            "confidence": self.confidence,
            "facts": self.facts,
            "uncertainties": self.uncertainties,
        }


def validate_event(payload: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - set(payload.keys()))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    return dict(payload)
