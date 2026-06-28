"""Data file helpers for TradingLab Data Engine."""

import csv
from collections.abc import Iterable
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


def write_empty_ohlcv_csv(path: Path) -> None:
    """Write empty OHLCV CSV file with header only."""

    write_ohlcv_csv(path, bars=())


def write_ohlcv_csv(path: Path, bars: Iterable[OhlcvBar]) -> None:
    """Write OHLCV CSV file with header and bars."""

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(OHLCV_HEADER)
        writer.writerows(ohlcv_bar_to_csv_row(bar) for bar in bars)
