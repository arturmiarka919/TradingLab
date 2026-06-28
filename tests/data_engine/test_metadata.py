"""Tests for Data Engine metadata helpers."""

from datetime import date

from tradinglab.data_engine.metadata import metadata_to_dict
from tradinglab.data_engine.models import DatasetMetadata


def test_metadata_to_dict_serializes_dataset_metadata() -> None:
    metadata = DatasetMetadata(
        dataset_id=(
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31"
        ),
        version="v001",
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
        status="created",
    )

    metadata_dict = metadata_to_dict(metadata)

    assert metadata_dict == {
        "dataset_id": (
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31"
        ),
        "version": "v001",
        "provider": "polygon_massive",
        "asset_class": "forex",
        "symbol": "EUR/USD",
        "data_type": "ohlcv",
        "price_type": "provider",
        "interval": "1d",
        "requested_start": "2024-01-01",
        "requested_end": "2024-12-31",
        "status": "created",
    }
