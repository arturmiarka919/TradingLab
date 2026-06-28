"""Tests for Data Engine OHLCV bar model."""

from datetime import UTC, datetime
from decimal import Decimal

from tradinglab.data_engine import OhlcvBar


def test_ohlcv_bar_contains_market_data_values() -> None:
    timestamp = datetime(2024, 1, 2, 0, 0, tzinfo=UTC)

    bar = OhlcvBar(
        timestamp=timestamp,
        open=Decimal("1.1000"),
        high=Decimal("1.1200"),
        low=Decimal("1.0900"),
        close=Decimal("1.1100"),
        volume=Decimal("12345.67"),
    )

    assert bar.timestamp == timestamp
    assert bar.open == Decimal("1.1000")
    assert bar.high == Decimal("1.1200")
    assert bar.low == Decimal("1.0900")
    assert bar.close == Decimal("1.1100")
    assert bar.volume == Decimal("12345.67")
