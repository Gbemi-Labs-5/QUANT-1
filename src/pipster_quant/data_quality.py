from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


def validate_market_data(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    seen: Counter[tuple[str, str]] = Counter()
    negative_spreads = 0
    invalid_rows = 0
    valid = True

    for row in rows:
        ts = str(row.get("timestamp", ""))
        symbol = str(row.get("symbol", ""))
        key = (ts, symbol)
        seen[key] += 1

        bid = float(row.get("bid", 0.0))
        ask = float(row.get("ask", 0.0))
        spread = float(row.get("spread", ask - bid))
        if ask < bid or spread < 0:
            negative_spreads += 1
            valid = False

    duplicate_timestamps = sum(1 for count in seen.values() if count > 1)
    if duplicate_timestamps:
        valid = False
    if negative_spreads:
        valid = False

    return {
        "duplicate_timestamps": duplicate_timestamps,
        "negative_spreads": negative_spreads,
        "invalid_rows": invalid_rows,
        "valid": valid,
    }
