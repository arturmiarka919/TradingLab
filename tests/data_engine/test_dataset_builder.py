"""Tests for Data Engine dataset builder."""

from datetime import date
from pathlib import Path

import pytest

from tradinglab.data_engine import DatasetBuildResult, DatasetRequest, create_dataset
from tradinglab.data_engine.status import DATASET_STATUS_CREATED


EXPECTED_DATASET_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


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
    assert result.metadata_path == expected_dataset_path / "metadata.json"
    assert (
        result.validation_report_path
        == expected_dataset_path / "validation_report.json"
    )
    assert result.status == DATASET_STATUS_CREATED
    assert result.dataset_path.is_dir()


def test_create_dataset_does_not_create_artifact_files_yet(tmp_path: Path) -> None:
    request = _build_dataset_request()

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    assert result.dataset_path.exists()
    assert not result.metadata_path.exists()
    assert not result.validation_report_path.exists()


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
