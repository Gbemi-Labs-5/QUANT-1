from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, tzinfo


@dataclass(frozen=True)
class SessionBoundary:
    name: str
    tz: tzinfo
    open_local: str
    close_local: str

    def _to_time(self, value: str) -> time:
        return datetime.strptime(value, "%H:%M").time()

    def in_session(self, timestamp: datetime) -> bool:
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=self.tz)
        local = timestamp.astimezone(self.tz)
        start = self._to_time(self.open_local)
        end = self._to_time(self.close_local)
        return start <= local.time() < end


@dataclass(frozen=True)
class TradingClock:
    timezone: tzinfo

    def normalize(self, timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None:
            return timestamp.replace(tzinfo=self.timezone)
        return timestamp.astimezone(self.timezone)

    def is_valid_utc_reference(self, timestamp: datetime) -> bool:
        return timestamp.tzinfo is not None
