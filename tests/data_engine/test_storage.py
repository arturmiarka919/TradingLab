"""Tests for Data Engine storage path helpers."""

from pathlib import Path

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
