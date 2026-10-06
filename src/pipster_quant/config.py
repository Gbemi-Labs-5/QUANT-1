from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PipsterRules:
    contest_name: str
    official_rules_source: str
    status: str
    timezone: str
    session_open_local: str
    session_close_local: str
    retrieval_date: str
    rule_scope: str
    daily_drawdown_limit: float | None
    max_drawdown_limit: float | None
    minimum_trading_days: int | None
    max_daily_contribution: float | None
    max_position_size: float | None
    known_verified_values: dict[str, Any] = field(default_factory=dict)
    unknowns: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipsterRules":
        contest = data.get("contest", {})
        trading = data.get("trading", {})
        risk = data.get("risk", {})
        verification = data.get("verification", {})
        unknowns = data.get("unknowns", {})
        known = data.get("verified_rules", {})

        return cls(
            contest_name=str(contest.get("name", "Pipster Halloween 2026")),
            official_rules_source=str(contest.get("official_rules_source", "https://www.pipster.io/how-it-works")),
            status=str(contest.get("status", "public-source-only")),
            timezone=str(trading.get("timezone", "UNVERIFIED")),
            session_open_local=str(trading.get("session_open_local", "UNVERIFIED")),
            session_close_local=str(trading.get("session_close_local", "UNVERIFIED")),
            retrieval_date=str(contest.get("retrieval_date", "2026-10-06")),
            rule_scope=str(contest.get("rule_scope", "official public-product examples; Halloween 2026 contest specifics remain unverified")),
            daily_drawdown_limit=_coerce_optional_float(risk.get("daily_drawdown_limit")),
            max_drawdown_limit=_coerce_optional_float(risk.get("max_drawdown_limit")),
            minimum_trading_days=_coerce_optional_int(risk.get("minimum_trading_days")),
            max_daily_contribution=_coerce_optional_float(risk.get("max_daily_contribution")),
            max_position_size=_coerce_optional_float(risk.get("max_position_size")),
            known_verified_values={key: value for key, value in known.items()},
            unknowns={key: value for key, value in unknowns.items()},
        )


def _coerce_optional_float(value: Any) -> float | None:
    if value is None or value == "UNVERIFIED":
        return None
    return float(value)


def _coerce_optional_int(value: Any) -> int | None:
    if value is None or value == "UNVERIFIED":
        return None
    return int(value)


def _default_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "pipster_halloween_2026.yaml"


def validate_rule_contract(rules: PipsterRules) -> dict[str, Any]:
    unverified = []
    for field_name, value in {
        "timezone": rules.timezone,
        "session_open_local": rules.session_open_local,
        "session_close_local": rules.session_close_local,
        "daily_drawdown_limit": rules.daily_drawdown_limit,
        "max_drawdown_limit": rules.max_drawdown_limit,
        "minimum_trading_days": rules.minimum_trading_days,
        "max_daily_contribution": rules.max_daily_contribution,
        "max_position_size": rules.max_position_size,
    }.items():
        if value in (None, "UNVERIFIED"):
            unverified.append(field_name)

    return {
        "valid": len(unverified) == 0,
        "unverified_fields": unverified,
        "contest_name": rules.contest_name,
        "status": rules.status,
        "retrieval_date": rules.retrieval_date,
    }


def load_rules(config_path: str | Path | None = None) -> PipsterRules:
    path = Path(config_path) if config_path is not None else _default_config_path()
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return PipsterRules.from_dict(raw)


def load_default_rules() -> PipsterRules:
    return load_rules()
