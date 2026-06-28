"""Tests for Data Engine storage path helpers."""

from pathlib import Path

from tradinglab.data_engine.storage import build_dataset_version_path


def test_build_dataset_version_path() -> None:
    dataset_id = (
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    )

    path = build_dataset_version_path(
        base_data_dir=Path("data"),
        dataset_id=dataset_id,
        version="v001",
    )

    assert path == Path("data") / "datasets" / dataset_id / "v001"


def test_build_dataset_version_path_does_not_create_directory(tmp_path: Path) -> None:
    dataset_id = (
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    )

    path = build_dataset_version_path(
        base_data_dir=tmp_path,
        dataset_id=dataset_id,
        version="v001",
    )

    assert path == tmp_path / "datasets" / dataset_id / "v001"
    assert not path.exists()
