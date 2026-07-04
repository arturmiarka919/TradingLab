"""Tests for public Data Engine read interface."""

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from tradinglab.data_engine import (
    DatasetMetadata,
    OhlcvBar,
    ValidationReport,
    load_metadata,
    load_normalized_candles,
    load_validation_report,
)
from tradinglab.data_engine.data_file import write_ohlcv_csv
from tradinglab.data_engine.metadata import write_metadata
from tradinglab.data_engine.status import (
    DATASET_LIFECYCLE_STATUS_VALIDATED,
    VALIDATION_STATUS_VALID,
)
from tradinglab.data_engine.storage import (
    build_dataset_version_path,
    build_metadata_path,
    build_normalized_candles_path,
    build_normalized_dir_path,
    build_validation_report_path,
)
from tradinglab.data_engine.validation_report import write_validation_report

DATASET_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


def test_public_load_metadata_reads_dataset_metadata(
    tmp_path: Path,
) -> None:
    _write_dataset_artifacts(base_data_dir=tmp_path)

    metadata = load_metadata(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert metadata == _build_metadata()


def test_public_load_validation_report_reads_dataset_validation_report(
    tmp_path: Path,
) -> None:
    _write_dataset_artifacts(base_data_dir=tmp_path)

    validation_report = load_validation_report(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert validation_report == _build_validation_report()


def test_public_load_normalized_candles_reads_dataset_candles(
    tmp_path: Path,
) -> None:
    _write_dataset_artifacts(base_data_dir=tmp_path)

    candles = load_normalized_candles(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v001",
    )

    assert candles == _build_bars()


def test_public_read_functions_use_requested_dataset_version(
    tmp_path: Path,
) -> None:
    _write_dataset_artifacts(base_data_dir=tmp_path, version="v001")
    _write_dataset_artifacts(base_data_dir=tmp_path, version="v002")

    first_metadata = load_metadata(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v001",
    )
    second_metadata = load_metadata(
        base_data_dir=tmp_path,
        dataset_id=DATASET_ID,
        version="v002",
    )

    assert first_metadata.version == "v001"
    assert second_metadata.version == "v002"


def test_public_load_metadata_raises_for_missing_dataset_version(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        load_metadata(
            base_data_dir=tmp_path,
            dataset_id=DATASET_ID,
            version="v001",
        )


def test_public_load_validation_report_raises_for_missing_dataset_version(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        load_validation_report(
            base_data_dir=tmp_path,
            dataset_id=DATASET_ID,
            version="v001",
        )


def test_public_load_normalized_candles_raises_for_missing_dataset_version(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        load_normalized_candles(
            base_data_dir=tmp_path,
            dataset_id=DATASET_ID,
            version="v001",
        )


def _write_dataset_artifacts(
    *,
    base_data_dir: Path,
    version: str = "v001",
) -> None:
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=DATASET_ID,
        version=version,
    )
    normalized_dir_path = build_normalized_dir_path(dataset_path)
    normalized_dir_path.mkdir(parents=True)

    write_metadata(
        build_metadata_path(dataset_path),
        _build_metadata(version=version),
    )
    write_validation_report(
        build_validation_report_path(dataset_path),
        _build_validation_report(version=version),
    )
    write_ohlcv_csv(
        build_normalized_candles_path(dataset_path),
        _build_bars(),
    )


def _build_metadata(version: str = "v001") -> DatasetMetadata:
    return DatasetMetadata(
        dataset_id=DATASET_ID,
        version=version,
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
        status=DATASET_LIFECYCLE_STATUS_VALIDATED,
    )


def _build_validation_report(version: str = "v001") -> ValidationReport:
    return ValidationReport(
        dataset_id=DATASET_ID,
        version=version,
        status=VALIDATION_STATUS_VALID,
        errors=(),
        warnings=(),
        checked_rows=2,
        valid_rows=2,
        invalid_rows=0,
    )


def _build_bars() -> tuple[OhlcvBar, OhlcvBar]:
    return (
        OhlcvBar(
            timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            open=Decimal("1.1000"),
            high=Decimal("1.1200"),
            low=Decimal("1.0900"),
            close=Decimal("1.1100"),
            volume=Decimal("12345.67"),
        ),
        OhlcvBar(
            timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            open=Decimal("1.1100"),
            high=Decimal("1.1300"),
            low=Decimal("1.1000"),
            close=Decimal("1.1250"),
            volume=Decimal("23456.78"),
        ),
    )
