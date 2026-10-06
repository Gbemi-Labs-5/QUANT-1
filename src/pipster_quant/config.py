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
    timezone: str = "UTC"
    session_open_local: str = "08:00"
    session_close_local: str = "16:00"
    unknowns: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipsterRules":
        contest = data.get("contest", {})
        trading = data.get("trading", {})
        unknowns = data.get("unknowns", {})

        return cls(
            contest_name=str(contest.get("name", "Pipster Halloween 2026")),
            official_rules_source=str(contest.get("official_rules_source", "https://www.pipster.io/faq")),
            status=str(contest.get("status", "public-source-only")),
            timezone=str(trading.get("timezone", "UTC")),
            session_open_local=str(trading.get("session_open_local", "08:00")),
            session_close_local=str(trading.get("session_close_local", "16:00")),
            unknowns={key: value for key, value in unknowns.items()},
        )


def _default_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "pipster_halloween_2026.yaml"


def load_rules(config_path: str | Path | None = None) -> PipsterRules:
    path = Path(config_path) if config_path is not None else _default_config_path()
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return PipsterRules.from_dict(raw)


def load_default_rules() -> PipsterRules:
    return load_rules()
