"""Tests for Data Engine dataset builder."""

from datetime import date
from pathlib import Path

from tradinglab.data_engine import DatasetBuildResult, DatasetRequest, create_dataset
from tradinglab.data_engine.status import DATASET_STATUS_CREATED


EXPECTED_DATASET_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


def test_create_dataset_returns_dataset_build_result() -> None:
    request = DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    result = create_dataset(
        request=request,
        base_data_dir=Path("data"),
        version="v001",
    )

    expected_dataset_path = Path("data") / "datasets" / EXPECTED_DATASET_ID / "v001"

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


def test_create_dataset_does_not_create_directories_yet(tmp_path: Path) -> None:
    request = DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    result = create_dataset(
        request=request,
        base_data_dir=tmp_path,
        version="v001",
    )

    assert not result.dataset_path.exists()
    assert not result.metadata_path.exists()
    assert not result.validation_report_path.exists()
