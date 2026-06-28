"""Tests for Data Engine data file helpers."""

from pathlib import Path

from tradinglab.data_engine.data_file import OHLCV_HEADER, write_empty_ohlcv_csv


def test_ohlcv_header_contains_expected_columns() -> None:
    assert OHLCV_HEADER == ("timestamp", "open", "high", "low", "close", "volume")


def test_write_empty_ohlcv_csv_writes_header_only(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"

    write_empty_ohlcv_csv(data_path)

    assert data_path.read_text(encoding="utf-8").splitlines() == [
        "timestamp,open,high,low,close,volume"
    ]
