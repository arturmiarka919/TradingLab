"""Tests for Data Engine sample dataset helpers."""

import json
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.metadata import load_metadata
from tradinglab.data_engine.sample_dataset import (
    SAMPLE_DATASET_VERSION,
    build_sample_dataset_request,
    build_sample_ohlcv_bars,
    create_sample_ohlcv_dataset,
)
from tradinglab.data_engine.status import (
    DATASET_STATUS_VALIDATED,
    VALIDATION_STATUS_VALID,
)
from tradinglab.data_engine.validation_report import load_validation_report


def test_create_sample_ohlcv_dataset_writes_expected_artifacts(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)

    artifact_names = sorted(path.name for path in result.dataset_path.iterdir())

    assert artifact_names == ["data.csv", "metadata.json", "validation_report.json"]
    assert result.metadata_path.is_file()
    assert result.validation_report_path.is_file()
    assert result.data_path.is_file()


def test_create_sample_ohlcv_dataset_writes_sample_bars(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)

    bars = read_ohlcv_csv(result.data_path)

    assert bars == build_sample_ohlcv_bars()


def test_create_sample_ohlcv_dataset_writes_validated_metadata_and_valid_report(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
    validation_report = json.loads(
        result.validation_report_path.read_text(encoding="utf-8")
    )

    assert result.status == DATASET_STATUS_VALIDATED
    assert metadata["status"] == DATASET_STATUS_VALIDATED
    assert validation_report["status"] == VALIDATION_STATUS_VALID
    assert validation_report["checked_rows"] == 2
    assert validation_report["valid_rows"] == 2
    assert validation_report["invalid_rows"] == 0
    assert validation_report["errors"] == []
    assert validation_report["warnings"] == []


def test_build_sample_dataset_request_returns_expected_request() -> None:
    request = build_sample_dataset_request()

    assert request.provider == "sample"
    assert request.asset_class == "forex"
    assert request.symbol == "EUR/USD"
    assert request.data_type == "ohlcv"
    assert request.price_type == "sample"
    assert request.interval == "1d"
    assert request.requested_start == date(2024, 1, 1)
    assert request.requested_end == date(2024, 1, 3)


def test_build_sample_ohlcv_bars_returns_expected_bars() -> None:
    bars = build_sample_ohlcv_bars()

    assert len(bars) == 2

    first_bar = bars[0]
    second_bar = bars[1]

    assert first_bar.timestamp == datetime(2024, 1, 2, 0, 0, tzinfo=UTC)
    assert first_bar.open == Decimal("1.1000")
    assert first_bar.high == Decimal("1.1200")
    assert first_bar.low == Decimal("1.0900")
    assert first_bar.close == Decimal("1.1100")
    assert first_bar.volume == Decimal("12345.67")

    assert second_bar.timestamp == datetime(2024, 1, 3, 0, 0, tzinfo=UTC)
    assert second_bar.open == Decimal("1.1100")
    assert second_bar.high == Decimal("1.1300")
    assert second_bar.low == Decimal("1.1000")
    assert second_bar.close == Decimal("1.1250")
    assert second_bar.volume == Decimal("23456.78")


def test_create_sample_ohlcv_dataset_uses_default_version(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    metadata = load_metadata(result.metadata_path)
    validation_report = load_validation_report(result.validation_report_path)

    assert SAMPLE_DATASET_VERSION == "v001"
    assert result.version == SAMPLE_DATASET_VERSION
    assert metadata.version == SAMPLE_DATASET_VERSION
    assert validation_report.version == SAMPLE_DATASET_VERSION


def test_create_sample_ohlcv_dataset_uses_custom_version(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(
        base_data_dir=tmp_path,
        version="v002",
    )
    metadata = load_metadata(result.metadata_path)
    validation_report = load_validation_report(result.validation_report_path)

    assert result.version == "v002"
    assert result.dataset_path.name == "v002"
    assert metadata.version == "v002"
    assert validation_report.version == "v002"


def test_create_sample_ohlcv_dataset_fails_without_overwrite(
    tmp_path: Path,
) -> None:
    first_result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    stale_data = "stale data that must not be overwritten\n"
    first_result.data_path.write_text(stale_data, encoding="utf-8")

    with pytest.raises(FileExistsError):
        create_sample_ohlcv_dataset(base_data_dir=tmp_path)

    assert first_result.data_path.read_text(encoding="utf-8") == stale_data


def test_create_sample_ohlcv_dataset_overwrite_recreates_existing_version(
    tmp_path: Path,
) -> None:
    first_result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    stale_file = first_result.dataset_path / "stale.txt"
    stale_file.write_text("stale artifact\n", encoding="utf-8")
    first_result.data_path.write_text("stale data\n", encoding="utf-8")

    second_result = create_sample_ohlcv_dataset(
        base_data_dir=tmp_path,
        overwrite=True,
    )

    artifact_names = sorted(path.name for path in second_result.dataset_path.iterdir())

    assert second_result.dataset_path == first_result.dataset_path
    assert not stale_file.exists()
    assert artifact_names == ["data.csv", "metadata.json", "validation_report.json"]
    assert read_ohlcv_csv(second_result.data_path) == build_sample_ohlcv_bars()
    assert second_result.status == DATASET_STATUS_VALIDATED


def test_create_sample_ohlcv_dataset_keeps_metadata_fields_from_request(
    tmp_path: Path,
) -> None:
    request = build_sample_dataset_request()

    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)

    metadata = load_metadata(result.metadata_path)

    assert metadata.dataset_id == result.dataset_id
    assert metadata.version == result.version
    assert metadata.provider == request.provider
    assert metadata.asset_class == request.asset_class
    assert metadata.symbol == request.symbol
    assert metadata.data_type == request.data_type
    assert metadata.price_type == request.price_type
    assert metadata.interval == request.interval
    assert metadata.requested_start == request.requested_start
    assert metadata.requested_end == request.requested_end
    assert metadata.status == DATASET_STATUS_VALIDATED


def test_create_sample_ohlcv_dataset_returns_consistent_result(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    validation_report = load_validation_report(result.validation_report_path)

    assert result.status == DATASET_STATUS_VALIDATED
    assert validation_report.status == VALIDATION_STATUS_VALID
    assert result.data_path == result.dataset_path / "data.csv"
    assert result.metadata_path == result.dataset_path / "metadata.json"
    assert result.validation_report_path == (
        result.dataset_path / "validation_report.json"
    )
    assert result.dataset_path.is_dir()
    assert result.data_path.is_file()
    assert result.metadata_path.is_file()
    assert result.validation_report_path.is_file()
