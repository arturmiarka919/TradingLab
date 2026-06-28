"""Tests for dataset ID generation."""

from datetime import date

from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.models import DatasetRequest


EXPECTED_EURUSD_DAILY_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


def test_generate_dataset_id_for_eurusd_daily_ohlcv() -> None:
    request = DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id == EXPECTED_EURUSD_DAILY_ID
    assert dataset_id == dataset_id.lower()
    assert "/" not in dataset_id
    assert " " not in dataset_id


def test_generate_dataset_id_normalizes_symbol_variants() -> None:
    symbols = [
        "EUR/USD",
        "EUR USD",
        " eur / usd ",
        "eur-usd",
        "EUR_USD",
    ]

    for symbol in symbols:
        request = DatasetRequest(
            provider="polygon_massive",
            asset_class="forex",
            symbol=symbol,
            data_type="ohlcv",
            price_type="provider",
            interval="1d",
            requested_start=date(2024, 1, 1),
            requested_end=date(2024, 12, 31),
        )

        assert generate_dataset_id(request) == EXPECTED_EURUSD_DAILY_ID


def test_generate_dataset_id_normalizes_common_text_parts() -> None:
    request = DatasetRequest(
        provider=" Polygon Massive ",
        asset_class=" Forex ",
        symbol="EUR/USD",
        data_type=" OHLCV ",
        price_type=" Provider ",
        interval=" 1D ",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id == EXPECTED_EURUSD_DAILY_ID
    assert dataset_id == dataset_id.lower()
    assert " " not in dataset_id


def test_generate_dataset_id_is_deterministic() -> None:
    request = DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    first_dataset_id = generate_dataset_id(request)
    second_dataset_id = generate_dataset_id(request)

    assert first_dataset_id == second_dataset_id