"""Data file helpers for TradingLab Data Engine."""

import csv
from pathlib import Path


OHLCV_HEADER = ("timestamp", "open", "high", "low", "close", "volume")


def write_empty_ohlcv_csv(path: Path) -> None:
    """Write empty OHLCV CSV file with header only."""

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(OHLCV_HEADER)
