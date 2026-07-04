"""Public Data Engine interface."""

from dataclasses import replace
from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.metadata import (
    load_metadata as _load_metadata_from_path,
    write_metadata,
)
from tradinglab.data_engine.models import DatasetMetadata, OhlcvBar, ValidationReport
from tradinglab.data_engine.ohlcv_validation import validate_ohlcv_csv
from tradinglab.data_engine.status import (
    DATASET_LIFECYCLE_STATUS_QUARANTINED,
    DATASET_LIFECYCLE_STATUS_VALIDATED,
    VALIDATION_STATUS_INVALID,
    VALIDATION_STATUS_VALID,
    VALIDATION_STATUS_VALID_WITH_WARNINGS,
)
from tradinglab.data_engine.storage import (
    build_dataset_version_path,
    build_metadata_path,
    build_normalized_candles_path,
    build_validation_report_path,
)
from tradinglab.data_engine.validation_report import (
    load_validation_report as _load_validation_report_from_path,
    write_validation_report,
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


def validate_dataset(
    *,
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> ValidationReport:
    """Validate normalized OHLCV candles for a dataset version."""
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )
    metadata_path = build_metadata_path(dataset_path)
    normalized_candles_path = build_normalized_candles_path(dataset_path)
    validation_report_path = build_validation_report_path(dataset_path)

    metadata = _load_metadata_from_path(metadata_path)
    validation_report = validate_ohlcv_csv(
        data_path=normalized_candles_path,
        dataset_id=dataset_id,
        version=version,
    )
    lifecycle_status = _resolve_lifecycle_status(validation_report.status)

    write_validation_report(validation_report_path, validation_report)
    write_metadata(
        metadata_path,
        replace(metadata, status=lifecycle_status),
    )

    return validation_report


def _resolve_lifecycle_status(validation_status: str) -> str:
    if validation_status in (
        VALIDATION_STATUS_VALID,
        VALIDATION_STATUS_VALID_WITH_WARNINGS,
    ):
        return DATASET_LIFECYCLE_STATUS_VALIDATED

    if validation_status == VALIDATION_STATUS_INVALID:
        return DATASET_LIFECYCLE_STATUS_QUARANTINED

    raise ValueError(f"Unsupported validation status: {validation_status}")
