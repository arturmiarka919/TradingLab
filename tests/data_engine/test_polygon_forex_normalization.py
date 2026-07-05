"""Tests for offline Polygon/Massive Forex OHLCV normalization."""

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from tradinglab.data_engine.connectors import (
    ProviderRawResponse,
    normalize_polygon_forex_ohlcv_response,
)
from tradinglab.data_engine.models import DatasetRequest, OhlcvBar


def test_normalize_polygon_forex_ohlcv_response_maps_payload_to_bars() -> None:
    raw_response = _build_raw_response()

    bars = normalize_polygon_forex_ohlcv_response(raw_response)

    assert bars == [
        OhlcvBar(
            timestamp=datetime(2021, 7, 22, 0, 0, tzinfo=UTC),
            open=Decimal("1.17921"),
            high=Decimal("1.18305"),
            low=Decimal("1.1756"),
            close=Decimal("1.17721"),
            volume=Decimal("125329"),
        ),
        OhlcvBar(
            timestamp=datetime(2021, 7, 23, 0, 0, tzinfo=UTC),
            open=Decimal("1.17721"),
            high=Decimal("1.184"),
            low=Decimal("1.1765"),
            close=Decimal("1.1801"),
            volume=Decimal("125330"),
        ),
    ]


def test_normalize_polygon_forex_ohlcv_response_preserves_payload_order() -> None:
    raw_response = _build_raw_response()

    bars = normalize_polygon_forex_ohlcv_response(raw_response)

    assert [bar.timestamp for bar in bars] == [
        datetime(2021, 7, 22, 0, 0, tzinfo=UTC),
        datetime(2021, 7, 23, 0, 0, tzinfo=UTC),
    ]


def test_normalize_polygon_forex_ohlcv_response_does_not_write_dataset(
    tmp_path: Path,
) -> None:
    raw_response = _build_raw_response()

    normalize_polygon_forex_ohlcv_response(raw_response)

    assert not (tmp_path / "data" / "datasets").exists()


def test_normalize_polygon_forex_ohlcv_response_rejects_wrong_provider() -> None:
    raw_response = ProviderRawResponse(
        provider="other_provider",
        request=_build_request(),
        raw_payload=_build_payload(),
    )

    with pytest.raises(ValueError, match="polygon_massive"):
        normalize_polygon_forex_ohlcv_response(raw_response)


def _build_raw_response() -> ProviderRawResponse:
    return ProviderRawResponse(
        provider="polygon_massive",
        request=_build_request(),
        raw_payload=_build_payload(),
    )


def _build_request() -> DatasetRequest:
    return DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2021, 7, 22),
        requested_end=date(2021, 7, 23),
    )


def _build_payload() -> dict[str, object]:
    return {
        "adjusted": True,
        "queryCount": 2,
        "request_id": "offline-test-request",
        "results": [
            {
                "c": 1.17721,
                "h": 1.18305,
                "l": 1.17560,
                "n": 125329,
                "o": 1.17921,
                "t": 1_626_912_000_000,
                "v": 125329,
                "vw": 1.17890,
            },
            {
                "c": 1.18010,
                "h": 1.18400,
                "l": 1.17650,
                "n": 125330,
                "o": 1.17721,
                "t": 1_626_998_400_000,
                "v": 125330,
                "vw": 1.18000,
            },
        ],
        "resultsCount": 2,
        "status": "OK",
        "ticker": "C:EURUSD",
    }
