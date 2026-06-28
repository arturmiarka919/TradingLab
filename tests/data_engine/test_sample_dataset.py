"""Tests for Data Engine sample dataset helpers."""

from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.sample_dataset import (
    build_sample_ohlcv_bars,
    create_sample_ohlcv_dataset,
)


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
