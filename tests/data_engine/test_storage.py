"""Tests for Data Engine storage path helpers."""

from pathlib import Path

from tradinglab.data_engine.storage import (
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


def test_build_dataset_version_path_does_not_create_directory(
    tmp_path: Path,
) -> None:
    path = build_dataset_version_path(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert not path.exists()


def test_build_metadata_path() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    metadata_path = build_metadata_path(dataset_path)

    assert metadata_path == dataset_path / "metadata.json"


def test_build_validation_report_path() -> None:
    dataset_path = Path("data") / "datasets" / DATASET_ID / "v001"

    validation_report_path = build_validation_report_path(dataset_path)

    assert validation_report_path == dataset_path / "validation_report.json"
