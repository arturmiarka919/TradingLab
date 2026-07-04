"""Public Data Engine read interface."""

from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.metadata import (
    load_metadata as _load_metadata_from_path,
)
from tradinglab.data_engine.models import DatasetMetadata, OhlcvBar, ValidationReport
from tradinglab.data_engine.storage import (
    build_dataset_version_path,
    build_metadata_path,
    build_normalized_candles_path,
    build_validation_report_path,
)
from tradinglab.data_engine.validation_report import (
    load_validation_report as _load_validation_report_from_path,
)


def load_metadata(
    *,
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> DatasetMetadata:
    """Load metadata for a dataset version."""
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )
    metadata_path = build_metadata_path(dataset_path)

    return _load_metadata_from_path(metadata_path)


def load_validation_report(
    *,
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> ValidationReport:
    """Load validation report for a dataset version."""
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )
    validation_report_path = build_validation_report_path(dataset_path)

    return _load_validation_report_from_path(validation_report_path)


def load_normalized_candles(
    *,
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> tuple[OhlcvBar, ...]:
    """Load normalized OHLCV candles for a dataset version."""
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )
    normalized_candles_path = build_normalized_candles_path(dataset_path)

    return read_ohlcv_csv(normalized_candles_path)
