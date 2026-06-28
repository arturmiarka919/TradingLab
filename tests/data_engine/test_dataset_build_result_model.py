"""Tests for Data Engine dataset build result model."""

from pathlib import Path

from tradinglab.data_engine import DatasetBuildResult
from tradinglab.data_engine.status import DATASET_STATUS_CREATED


def test_dataset_build_result_contains_dataset_artifact_paths() -> None:
    result = DatasetBuildResult(
        dataset_id=(
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31"
        ),
        version="v001",
        dataset_path=Path(
            "data/datasets/"
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31/v001"
        ),
        metadata_path=Path(
            "data/datasets/"
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31/v001/metadata.json"
        ),
        validation_report_path=Path(
            "data/datasets/"
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31/v001/validation_report.json"
        ),
        status=DATASET_STATUS_CREATED,
    )

    assert result.dataset_id == (
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    )
    assert result.version == "v001"
    assert result.dataset_path.name == "v001"
    assert result.metadata_path.name == "metadata.json"
    assert result.validation_report_path.name == "validation_report.json"
    assert result.status == DATASET_STATUS_CREATED
