"""Data file helpers for TradingLab Data Engine."""

import csv
from collections.abc import Iterable, Sequence
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from tradinglab.data_engine.models import OhlcvBar


OHLCV_HEADER = ("timestamp", "open", "high", "low", "close", "volume")


def ohlcv_bar_to_csv_row(bar: OhlcvBar) -> tuple[str, str, str, str, str, str]:
    """Convert OHLCV bar to CSV row values."""

    return (
        bar.timestamp.isoformat(),
        str(bar.open),
        str(bar.high),
        str(bar.low),
        str(bar.close),
        str(bar.volume),
    )


def csv_row_to_ohlcv_bar(row: Sequence[str]) -> OhlcvBar:
    """Convert CSV row values to OHLCV bar."""

    if len(row) != len(OHLCV_HEADER):
        raise ValueError("OHLCV CSV row must contain exactly 6 values.")

    return OhlcvBar(
        timestamp=datetime.fromisoformat(row[0]),
        open=Decimal(row[1]),
        high=Decimal(row[2]),
        low=Decimal(row[3]),
        close=Decimal(row[4]),
        volume=Decimal(row[5]),
    )


def write_empty_ohlcv_csv(path: Path) -> None:
    """Write empty OHLCV CSV file with header only."""

    write_ohlcv_csv(path, bars=())


def write_ohlcv_csv(path: Path, bars: Iterable[OhlcvBar]) -> None:
    """Write OHLCV CSV file with header and bars."""

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(OHLCV_HEADER)
        writer.writerows(ohlcv_bar_to_csv_row(bar) for bar in bars)
