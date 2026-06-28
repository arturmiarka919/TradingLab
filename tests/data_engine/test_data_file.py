"""Tests for Data Engine data file helpers."""

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from tradinglab.data_engine import OhlcvBar
from tradinglab.data_engine.data_file import (
    OHLCV_HEADER,
    ohlcv_bar_to_csv_row,
    write_empty_ohlcv_csv,
)


def test_ohlcv_header_contains_expected_columns() -> None:
    assert OHLCV_HEADER == ("timestamp", "open", "high", "low", "close", "volume")


def test_ohlcv_bar_to_csv_row_converts_values_to_strings() -> None:
    bar = OhlcvBar(
        timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
        open=Decimal("1.1000"),
        high=Decimal("1.1200"),
        low=Decimal("1.0900"),
        close=Decimal("1.1100"),
        volume=Decimal("12345.67"),
    )

    row = ohlcv_bar_to_csv_row(bar)

    assert row == (
        "2024-01-02T00:00:00+00:00",
        "1.1000",
        "1.1200",
        "1.0900",
        "1.1100",
        "12345.67",
    )


def test_write_empty_ohlcv_csv_writes_header_only(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"

    write_empty_ohlcv_csv(data_path)

    assert data_path.read_text(encoding="utf-8").splitlines() == [
        "timestamp,open,high,low,close,volume"
    ]
