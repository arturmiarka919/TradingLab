"""Tests for Data Engine sample dataset helpers."""

import json
from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.sample_dataset import (
    build_sample_ohlcv_bars,
    create_sample_ohlcv_dataset,
)
from tradinglab.data_engine.status import DATASET_STATUS_VALIDATED


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


def test_create_sample_ohlcv_dataset_writes_validated_metadata_and_report(
    tmp_path: Path,
) -> None:
    result = create_sample_ohlcv_dataset(base_data_dir=tmp_path)
    metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
    validation_report = json.loads(
        result.validation_report_path.read_text(encoding="utf-8")
    )

    assert result.status == DATASET_STATUS_VALIDATED
    assert metadata["status"] == DATASET_STATUS_VALIDATED
    assert validation_report["status"] == DATASET_STATUS_VALIDATED
    assert validation_report["checked_rows"] == 2
    assert validation_report["valid_rows"] == 2
    assert validation_report["invalid_rows"] == 0
    assert validation_report["errors"] == []
    assert validation_report["warnings"] == []
