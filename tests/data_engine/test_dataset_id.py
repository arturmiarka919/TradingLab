"""Tests for dataset ID generation."""

from datetime import date

from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.models import DatasetRequest


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

    assert (
        dataset_id
        == "polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31"
    )
    assert dataset_id == dataset_id.lower()
    assert "/" not in dataset_id
    assert " " not in dataset_id
