"""Base provider connector contracts for TradingLab Data Engine."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from tradinglab.data_engine.models import DatasetRequest


@dataclass(frozen=True)
class ProviderRawResponse:
    """Raw response returned by a provider connector."""

    provider: str
    request: DatasetRequest
    raw_payload: object


@runtime_checkable
class ProviderOhlcvConnector(Protocol):
    """Protocol for provider connectors returning raw OHLCV payloads."""

    def fetch_ohlcv(self, request: DatasetRequest) -> ProviderRawResponse:
        """Fetch raw OHLCV response for a dataset request."""
        ...
