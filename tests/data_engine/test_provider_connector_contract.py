"""Tests for provider connector base contract."""

from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from tradinglab.data_engine.connectors import (
    ProviderOhlcvConnector,
    ProviderRawResponse,
)
from tradinglab.data_engine.models import DatasetRequest


class FakeProviderConnector:
    """Offline connector implementation used only for contract tests."""

    def __init__(self, raw_payload: dict[str, object]) -> None:
        self.raw_payload = raw_payload
        self.seen_requests: list[DatasetRequest] = []

    def fetch_ohlcv(self, request: DatasetRequest) -> ProviderRawResponse:
        self.seen_requests.append(request)

        return ProviderRawResponse(
            provider=request.provider,
            request=request,
            raw_payload=self.raw_payload,
        )


def test_provider_connector_contract_can_return_raw_response() -> None:
    request = _build_request()
    raw_payload = {
        "ticker": "C:EURUSD",
        "results": [
            {
                "t": 1_704_067_200_000,
                "o": 1.1000,
                "h": 1.1200,
                "l": 1.0900,
                "c": 1.1100,
                "v": 12345,
            },
        ],
    }
    connector = FakeProviderConnector(raw_payload=raw_payload)

    response = connector.fetch_ohlcv(request)

    assert isinstance(connector, ProviderOhlcvConnector)
    assert response == ProviderRawResponse(
        provider="polygon_massive",
        request=request,
        raw_payload=raw_payload,
    )
    assert connector.seen_requests == [request]


def test_provider_raw_response_keeps_request_and_payload_without_disk_write(
    tmp_path,
) -> None:
    request = _build_request()
    raw_payload = {"status": "OK", "results": []}
    connector = FakeProviderConnector(raw_payload=raw_payload)

    response = connector.fetch_ohlcv(request)

    assert response.provider == "polygon_massive"
    assert response.request is request
    assert response.raw_payload == raw_payload
    assert not (tmp_path / "data" / "datasets").exists()


def test_provider_raw_response_is_immutable() -> None:
    response = ProviderRawResponse(
        provider="polygon_massive",
        request=_build_request(),
        raw_payload={"status": "OK"},
    )

    with pytest.raises(FrozenInstanceError):
        response.provider = "other_provider"  # type: ignore[misc]


def _build_request() -> DatasetRequest:
    return DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 1, 3),
    )
