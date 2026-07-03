"""Tests for Data Engine dataset builder."""

from datetime import date
from pathlib import Path

import pytest

from tradinglab.data_engine import (
    DatasetBuildResult,
    DatasetMetadata,
    DatasetRequest,
    ValidationReport,
    create_dataset,
)
from tradinglab.data_engine.metadata import load_metadata
from tradinglab.data_engine.status import (
    DATASET_STATUS_CREATED,
    VALIDATION_STATUS_NOT_VALIDATED,
)
from tradinglab.data_engine.validation_report import load_validation_report

EXPECTED_DATASET_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)
EXPECTED_OHLCV_HEADER = "timestamp,open,high,low,close,volume"


def test_create_dataset_returns_dataset_build_result_and_creates_directory(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    expected_dataset_path = tmp_path / "datasets" / EXPECTED_DATASET_ID / "v001"

    assert isinstance(result, DatasetBuildResult)
    assert result.dataset_id == EXPECTED_DATASET_ID
    assert result.version == "v001"
    assert result.dataset_path == expected_dataset_path
    assert result.data_path == expected_dataset_path / "data.csv"
    assert result.metadata_path == expected_dataset_path / "metadata.json"
    assert (
        result.validation_report_path
        == expected_dataset_path / "validation_report.json"
    )
    assert result.status == DATASET_STATUS_CREATED

    assert result.dataset_path.is_dir()
    assert (expected_dataset_path / "raw").is_dir()
    assert (expected_dataset_path / "normalized").is_dir()
    assert result.data_path.is_file()
    assert result.metadata_path.is_file()
    assert result.validation_report_path.is_file()


def test_create_dataset_writes_metadata_json(tmp_path: Path) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    loaded_metadata = load_metadata(result.metadata_path)

    assert loaded_metadata == _build_expected_metadata()


def test_create_dataset_writes_initial_validation_report_json(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    loaded_report = load_validation_report(result.validation_report_path)

    assert loaded_report == _build_expected_validation_report()


def test_create_dataset_writes_empty_data_csv_with_ohlcv_header(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    assert result.data_path.read_text(encoding="utf-8").splitlines() == [
        EXPECTED_OHLCV_HEADER
    ]


def test_create_dataset_creates_only_initial_artifacts(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    artifact_names = sorted(path.name for path in result.dataset_path.iterdir())

    assert artifact_names == [
        "data.csv",
        "metadata.json",
        "normalized",
        "raw",
        "validation_report.json",
    ]


def test_create_dataset_creates_empty_raw_and_normalized_directories(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    raw_dir_path = result.dataset_path / "raw"
    normalized_dir_path = result.dataset_path / "normalized"

    assert raw_dir_path.is_dir()
    assert normalized_dir_path.is_dir()
    assert list(raw_dir_path.iterdir()) == []
    assert list(normalized_dir_path.iterdir()) == []


def test_create_dataset_fails_when_dataset_version_already_exists(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    existing_dataset_path = tmp_path / "datasets" / EXPECTED_DATASET_ID / "v001"
    existing_dataset_path.mkdir(parents=True)

    with pytest.raises(FileExistsError):
        create_dataset(
            request=request,
            base_data_dir=tmp_path,
            version="v001",
        )


def test_create_dataset_creates_missing_base_directories(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()
    base_data_dir = tmp_path / "missing" / "data"

    assert not base_data_dir.exists()

    result = create_dataset(
        request=request,
        base_data_dir=base_data_dir,
        version="v001",
    )

    expected_dataset_path = base_data_dir / "datasets" / EXPECTED_DATASET_ID / "v001"

    assert base_data_dir.is_dir()
    assert result.dataset_path == expected_dataset_path
    assert result.dataset_path.is_dir()
    assert (expected_dataset_path / "raw").is_dir()
    assert (expected_dataset_path / "normalized").is_dir()
    assert result.data_path.is_file()
    assert result.metadata_path.is_file()
    assert result.validation_report_path.is_file()


def test_create_dataset_creates_new_version_without_changing_existing_version(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    first_result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )
    second_result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v002",
    )

    assert first_result.dataset_id == second_result.dataset_id
    assert first_result.version == "v001"
    assert second_result.version == "v002"
    assert first_result.dataset_path != second_result.dataset_path

    assert first_result.dataset_path.is_dir()
    assert second_result.dataset_path.is_dir()

    assert (first_result.dataset_path / "raw").is_dir()
    assert (first_result.dataset_path / "normalized").is_dir()
    assert (second_result.dataset_path / "raw").is_dir()
    assert (second_result.dataset_path / "normalized").is_dir()

    assert first_result.data_path.is_file()
    assert first_result.metadata_path.is_file()
    assert first_result.validation_report_path.is_file()
    assert second_result.data_path.is_file()
    assert second_result.metadata_path.is_file()
    assert second_result.validation_report_path.is_file()

    first_metadata = load_metadata(first_result.metadata_path)
    second_metadata = load_metadata(second_result.metadata_path)

    assert first_metadata.version == "v001"
    assert second_metadata.version == "v002"


def test_create_dataset_keeps_initial_statuses_separated_across_artifacts(
    tmp_path: Path,
) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    loaded_metadata = load_metadata(result.metadata_path)
    loaded_report = load_validation_report(result.validation_report_path)

    assert result.status == DATASET_STATUS_CREATED
    assert loaded_metadata.status == DATASET_STATUS_CREATED
    assert loaded_report.status == VALIDATION_STATUS_NOT_VALIDATED


def _build_dataset_request() -> DatasetRequest:
    return DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )


def _build_expected_metadata() -> DatasetMetadata:
    return DatasetMetadata(
        dataset_id=EXPECTED_DATASET_ID,
        version="v001",
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
        status=DATASET_STATUS_CREATED,
    )


def _build_expected_validation_report() -> ValidationReport:
    return ValidationReport(
        dataset_id=EXPECTED_DATASET_ID,
        version="v001",
        status=VALIDATION_STATUS_NOT_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=0,
        valid_rows=0,
        invalid_rows=0,
    )
