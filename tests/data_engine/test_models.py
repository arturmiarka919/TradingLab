"""Tests for Data Engine models."""

from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from tradinglab.data_engine.models import DatasetMetadata
from tradinglab.data_engine.status import (
    DATASET_LIFECYCLE_STATUS_RAW,
    DATASET_LIFECYCLE_STATUS_VALIDATED,
)


def test_dataset_metadata_can_describe_eurusd_dataset_version() -> None:
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
        status=DATASET_LIFECYCLE_STATUS_RAW,
    )

    assert metadata.dataset_id == (
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    )
    assert metadata.version == "v001"
    assert metadata.provider == "polygon_massive"
    assert metadata.symbol == "EUR/USD"
    assert metadata.status == DATASET_LIFECYCLE_STATUS_RAW


def test_dataset_metadata_is_immutable() -> None:
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
        status=DATASET_LIFECYCLE_STATUS_RAW,
    )

    with pytest.raises(FrozenInstanceError):
        metadata.status = DATASET_LIFECYCLE_STATUS_VALIDATED  # type: ignore[misc]
