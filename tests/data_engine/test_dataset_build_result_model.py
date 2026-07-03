"""Tests for Data Engine dataset build result model."""

from pathlib import Path

from tradinglab.data_engine.models import DatasetBuildResult
from tradinglab.data_engine.status import DATASET_STATUS_CREATED


def test_dataset_build_result_contains_dataset_artifact_paths() -> None:
    dataset_path = Path("data") / "datasets" / "dataset_1" / "v001"

    result = DatasetBuildResult(
        dataset_id="dataset_1",
        version="v001",
        dataset_path=dataset_path,
        data_path=dataset_path / "normalized" / "candles.csv",
        metadata_path=dataset_path / "metadata.json",
        validation_report_path=dataset_path / "validation_report.json",
        status=DATASET_STATUS_CREATED,
    )

    assert result.dataset_id == "dataset_1"
    assert result.version == "v001"
    assert result.dataset_path == dataset_path
    assert result.data_path == dataset_path / "normalized" / "candles.csv"
    assert result.metadata_path == dataset_path / "metadata.json"
    assert result.validation_report_path == dataset_path / "validation_report.json"
    assert result.status == DATASET_STATUS_CREATED
