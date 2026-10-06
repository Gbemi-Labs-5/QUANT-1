from datetime import datetime, timezone

from pipster_quant.time_contract import TradingClock, SessionBoundary


def test_session_boundary_handles_rollover_and_utc_norm():
    tz = timezone.utc
    clock = TradingClock(timezone=tz)
    sess = SessionBoundary(name="LONDN", tz=tz, open_local="08:00", close_local="16:00")

    start = datetime(2026, 10, 6, 8, 0, tzinfo=tz)
    end = datetime(2026, 10, 6, 16, 30, tzinfo=tz)

    assert clock.normalize(start) == start
    assert sess.in_session(start) is True
    assert sess.in_session(end) is False
