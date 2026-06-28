"""Tests for Data Engine data file helpers."""

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from tradinglab.data_engine import OhlcvBar
from tradinglab.data_engine.data_file import (
    OHLCV_HEADER,
    csv_row_to_ohlcv_bar,
    ohlcv_bar_to_csv_row,
    read_ohlcv_csv,
    write_empty_ohlcv_csv,
    write_ohlcv_csv,
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


def test_csv_row_to_ohlcv_bar_converts_strings_to_values() -> None:
    row = (
        "2024-01-02T00:00:00+00:00",
        "1.1000",
        "1.1200",
        "1.0900",
        "1.1100",
        "12345.67",
    )

    bar = csv_row_to_ohlcv_bar(row)

    assert bar == OhlcvBar(
        timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
        open=Decimal("1.1000"),
        high=Decimal("1.1200"),
        low=Decimal("1.0900"),
        close=Decimal("1.1100"),
        volume=Decimal("12345.67"),
    )


def test_csv_row_to_ohlcv_bar_rejects_invalid_row_length() -> None:
    row = ("2024-01-02T00:00:00+00:00", "1.1000")

    with pytest.raises(
        ValueError,
        match="OHLCV CSV row must contain exactly 6 values.",
    ):
        csv_row_to_ohlcv_bar(row)


def test_write_empty_ohlcv_csv_writes_header_only(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"

    write_empty_ohlcv_csv(data_path)

    assert data_path.read_text(encoding="utf-8").splitlines() == [
        "timestamp,open,high,low,close,volume"
    ]


def test_write_ohlcv_csv_writes_header_and_bars(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    bars = _build_sample_bars()

    write_ohlcv_csv(data_path, bars)

    assert data_path.read_text(encoding="utf-8").splitlines() == [
        "timestamp,open,high,low,close,volume",
        "2024-01-02T00:00:00+00:00,1.1000,1.1200,1.0900,1.1100,12345.67",
        "2024-01-03T00:00:00+00:00,1.1100,1.1300,1.1000,1.1250,23456.78",
    ]


def test_read_ohlcv_csv_reads_header_and_bars(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2024-01-02T00:00:00+00:00,1.1000,1.1200,1.0900,1.1100,12345.67",
                "2024-01-03T00:00:00+00:00,1.1100,1.1300,1.1000,1.1250,23456.78",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bars = read_ohlcv_csv(data_path)

    assert bars == _build_sample_bars()


def test_read_ohlcv_csv_rejects_invalid_header(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text("wrong,header\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="OHLCV CSV header does not match expected header.",
    ):
        read_ohlcv_csv(data_path)


def _build_sample_bars() -> tuple[OhlcvBar, OhlcvBar]:
    return (
        OhlcvBar(
            timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            open=Decimal("1.1000"),
            high=Decimal("1.1200"),
            low=Decimal("1.0900"),
            close=Decimal("1.1100"),
            volume=Decimal("12345.67"),
        ),
        OhlcvBar(
            timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            open=Decimal("1.1100"),
            high=Decimal("1.1300"),
            low=Decimal("1.1000"),
            close=Decimal("1.1250"),
            volume=Decimal("23456.78"),
        ),
    )
