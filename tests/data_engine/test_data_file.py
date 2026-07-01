"""Tests for Data Engine data file helpers."""

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
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


def test_write_then_read_ohlcv_csv_returns_same_bars(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    expected_bars = _build_sample_bars()

    write_ohlcv_csv(data_path, expected_bars)

    loaded_bars = read_ohlcv_csv(data_path)

    assert loaded_bars == expected_bars

def test_read_ohlcv_csv_raises_for_missing_file(tmp_path: Path) -> None:
    data_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        read_ohlcv_csv(data_path)


def test_read_ohlcv_csv_rejects_empty_file_without_header(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text("", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="OHLCV CSV header does not match expected header.",
    ):
        read_ohlcv_csv(data_path)


def test_read_ohlcv_csv_rejects_data_row_with_missing_column(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2024-01-02T00:00:00+00:00,1.1000,1.1200,1.0900,1.1100",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="OHLCV CSV row must contain exactly 6 values.",
    ):
        read_ohlcv_csv(data_path)


def test_read_ohlcv_csv_rejects_data_row_with_extra_column(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2024-01-02T00:00:00+00:00,1.1000,1.1200,1.0900,1.1100,12345.67,extra",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="OHLCV CSV row must contain exactly 6 values.",
    ):
        read_ohlcv_csv(data_path)


def test_read_ohlcv_csv_rejects_unparseable_timestamp(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "not-a-timestamp,1.1000,1.1200,1.0900,1.1100,12345.67",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        read_ohlcv_csv(data_path)


def test_read_ohlcv_csv_rejects_unparseable_decimal_value(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2024-01-02T00:00:00+00:00,not-a-decimal,1.1200,1.0900,1.1100,12345.67",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(InvalidOperation):
        read_ohlcv_csv(data_path)


def test_write_then_read_ohlcv_csv_preserves_decimal_precision(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    expected_bar = OhlcvBar(
        timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
        open=Decimal("1.100000"),
        high=Decimal("1.120000"),
        low=Decimal("1.090000"),
        close=Decimal("1.110000"),
        volume=Decimal("12345.6700"),
    )

    write_ohlcv_csv(data_path, (expected_bar,))

    loaded_bars = read_ohlcv_csv(data_path)

    assert loaded_bars == (expected_bar,)
    assert loaded_bars[0].open.as_tuple() == expected_bar.open.as_tuple()
    assert loaded_bars[0].high.as_tuple() == expected_bar.high.as_tuple()
    assert loaded_bars[0].low.as_tuple() == expected_bar.low.as_tuple()
    assert loaded_bars[0].close.as_tuple() == expected_bar.close.as_tuple()
    assert loaded_bars[0].volume.as_tuple() == expected_bar.volume.as_tuple()

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
