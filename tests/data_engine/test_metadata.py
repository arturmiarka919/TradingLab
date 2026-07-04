"""Tests for Data Engine metadata helpers."""

from datetime import date
import json
from pathlib import Path

import pytest

from tradinglab.data_engine.metadata import (
    load_metadata,
    metadata_from_dict,
    metadata_to_dict,
    write_metadata,
)
from tradinglab.data_engine.models import DatasetMetadata
from tradinglab.data_engine.status import DATASET_LIFECYCLE_STATUS_RAW

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
    "status": DATASET_LIFECYCLE_STATUS_RAW,
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
    status=DATASET_LIFECYCLE_STATUS_RAW,
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
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == (
        EXPECTED_METADATA_DICT
    )


def test_write_metadata_can_be_read_back_as_dataset_metadata(
    tmp_path: Path,
) -> None:
    metadata_path = tmp_path / "metadata.json"

    write_metadata(metadata_path, EXPECTED_METADATA)

    loaded_data = json.loads(metadata_path.read_text(encoding="utf-8"))
    loaded_metadata = metadata_from_dict(loaded_data)

    assert loaded_metadata == EXPECTED_METADATA


def test_load_metadata_reads_metadata_json(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"

    write_metadata(metadata_path, EXPECTED_METADATA)

    loaded_metadata = load_metadata(metadata_path)

    assert loaded_metadata == EXPECTED_METADATA


def test_metadata_from_dict_raises_for_missing_required_field() -> None:
    metadata_dict = dict(EXPECTED_METADATA_DICT)
    del metadata_dict["dataset_id"]

    with pytest.raises(KeyError):
        metadata_from_dict(metadata_dict)


def test_metadata_from_dict_rejects_invalid_requested_start() -> None:
    metadata_dict = {
        **EXPECTED_METADATA_DICT,
        "requested_start": "not-a-date",
    }

    with pytest.raises(ValueError):
        metadata_from_dict(metadata_dict)


def test_metadata_from_dict_rejects_invalid_requested_end() -> None:
    metadata_dict = {
        **EXPECTED_METADATA_DICT,
        "requested_end": "not-a-date",
    }

    with pytest.raises(ValueError):
        metadata_from_dict(metadata_dict)


def test_load_metadata_rejects_invalid_json(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text("{invalid-json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_metadata(metadata_path)


def test_load_metadata_raises_for_missing_file(tmp_path: Path) -> None:
    metadata_path = tmp_path / "missing_metadata.json"

    with pytest.raises(FileNotFoundError):
        load_metadata(metadata_path)


def test_metadata_from_dict_normalizes_text_fields_to_strings() -> None:
    metadata_dict = {
        **EXPECTED_METADATA_DICT,
        "dataset_id": 123,
        "version": 1,
        "provider": "polygon_massive",
        "asset_class": "forex",
        "symbol": 456,
        "data_type": "ohlcv",
        "price_type": "provider",
        "interval": 789,
        "status": False,
    }

    metadata = metadata_from_dict(metadata_dict)

    assert metadata.dataset_id == "123"
    assert metadata.version == "1"
    assert metadata.symbol == "456"
    assert metadata.interval == "789"
    assert metadata.status == "False"


def test_write_metadata_preserves_non_ascii_characters(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"
    metadata = DatasetMetadata(
        dataset_id="test_zażółć_€",
        version="v001",
        provider="źródło_testowe",
        asset_class="forex",
        symbol="EUR/PLN/zażółć",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
        status=DATASET_LIFECYCLE_STATUS_RAW,
    )

    write_metadata(metadata_path, metadata)

    metadata_text = metadata_path.read_text(encoding="utf-8")

    assert "zażółć" in metadata_text
    assert "źródło_testowe" in metadata_text
    assert "€" in metadata_text


def test_write_metadata_ends_file_with_single_newline(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata.json"

    write_metadata(metadata_path, EXPECTED_METADATA)

    metadata_text = metadata_path.read_text(encoding="utf-8")

    assert metadata_text.endswith("\n")
    assert not metadata_text.endswith("\n\n")
