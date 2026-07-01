"""Tests for Data Engine storage path helpers."""

from pathlib import Path

import tradinglab.data_engine.storage as storage_module
from tradinglab.data_engine.models import DatasetBuildResult
from tradinglab.data_engine.status import DATASET_STATUS_CREATED
from tradinglab.data_engine.storage import (
    build_data_path,
    build_dataset_version_path,
    build_metadata_path,
    build_validation_report_path,
)


DATASET_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


def test_build_dataset_version_path() -> None:
    path = build_dataset_version_path(
        base_data_dir=Path("data"),
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert path == Path("data") / "datasets" / DATASET_ID / "v001"


def test_build_metadata_path() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    path = build_metadata_path(dataset_path)

    assert path == dataset_path / "metadata.json"


def test_build_validation_report_path() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    path = build_validation_report_path(dataset_path)

    assert path == dataset_path / "validation_report.json"


def test_build_data_path() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    path = build_data_path(dataset_path)

    assert path == dataset_path / "data.csv"


def test_storage_helpers_do_not_create_directories_or_files(
    tmp_path: Path,
) -> None:
    base_data_dir = tmp_path / "missing_data"
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=DATASET_ID,
        version="v001",
    )
    data_path = build_data_path(dataset_path)
    metadata_path = build_metadata_path(dataset_path)
    validation_report_path = build_validation_report_path(dataset_path)

    assert not base_data_dir.exists()
    assert not dataset_path.exists()
    assert not data_path.exists()
    assert not metadata_path.exists()
    assert not validation_report_path.exists()


def test_build_dataset_version_path_uses_custom_base_data_dir() -> None:
    base_data_dir = Path("custom") / "market_data"

    path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert path == base_data_dir / "datasets" / DATASET_ID / "v001"


def test_build_dataset_version_path_uses_custom_version() -> None:
    path = build_dataset_version_path(
        base_data_dir=Path("data"),
        dataset_id=DATASET_ID,
        version="v002",
    )

    assert path == Path("data") / "datasets" / DATASET_ID / "v002"
    assert path.name == "v002"


def test_storage_artifact_names_are_consistent_with_dataset_build_result() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    result = DatasetBuildResult(
        dataset_id=DATASET_ID,
        version="v001",
        dataset_path=dataset_path,
        data_path=build_data_path(dataset_path),
        metadata_path=build_metadata_path(dataset_path),
        validation_report_path=build_validation_report_path(dataset_path),
        status=DATASET_STATUS_CREATED,
    )

    assert result.data_path == dataset_path / "data.csv"
    assert result.metadata_path == dataset_path / "metadata.json"
    assert result.validation_report_path == dataset_path / "validation_report.json"
    assert result.data_path.name == "data.csv"
    assert result.metadata_path.name == "metadata.json"
    assert result.validation_report_path.name == "validation_report.json"


def test_storage_does_not_expose_raw_or_normalized_path_helpers_yet() -> None:
    assert not hasattr(storage_module, "build_raw_response_path")
    assert not hasattr(storage_module, "build_normalized_candles_path")
