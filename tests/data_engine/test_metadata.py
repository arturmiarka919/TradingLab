"""Tests for Data Engine metadata helpers."""

from datetime import date
import json
from pathlib import Path

from tradinglab.data_engine.metadata import (
    metadata_from_dict,
    metadata_to_dict,
    write_metadata,
)
from tradinglab.data_engine.models import DatasetMetadata


EXPECTED_METADATA_DICT = {
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


EXPECTED_METADATA = DatasetMetadata(
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


def test_metadata_to_dict_serializes_dataset_metadata() -> None:
    metadata_dict = metadata_to_dict(EXPECTED_METADATA)

    assert metadata_dict == EXPECTED_METADATA_DICT


def test_metadata_from_dict_deserializes_dataset_metadata() -> None:
    metadata = metadata_from_dict(EXPECTED_METADATA_DICT)

    assert metadata == EXPECTED_METADATA


def test_write_metadata_writes_metadata_json(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"

    write_metadata(metadata_path, EXPECTED_METADATA)

    assert metadata_path.exists()
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == EXPECTED_METADATA_DICT


def test_write_metadata_can_be_read_back_as_dataset_metadata(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"

    write_metadata(metadata_path, EXPECTED_METADATA)

    loaded_data = json.loads(metadata_path.read_text(encoding="utf-8"))
    loaded_metadata = metadata_from_dict(loaded_data)

    assert loaded_metadata == EXPECTED_METADATA
