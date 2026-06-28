"""Data models for TradingLab Data Engine."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DatasetRequest:
    """Request describing a market data dataset."""

    provider: str
    asset_class: str
    symbol: str
    data_type: str
    price_type: str
    interval: str
    requested_start: date
    requested_end: date
