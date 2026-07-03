"""Dataset build orchestration helpers for TradingLab Data Engine."""

from pathlib import Path

from tradinglab.data_engine.data_file import write_empty_ohlcv_csv
from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.metadata import write_metadata
from tradinglab.data_engine.models import (
    DatasetBuildResult,
    DatasetMetadata,
    DatasetRequest,
    ValidationReport,
)
from tradinglab.data_engine.status import (
    DATASET_STATUS_CREATED,
    VALIDATION_STATUS_NOT_VALIDATED,
)
from tradinglab.data_engine.storage import (
    build_data_path,
    build_dataset_version_path,
    build_metadata_path,
    build_normalized_dir_path,
    build_raw_dir_path,
    build_validation_report_path,
)
from tradinglab.data_engine.validation_report import write_validation_report


def create_dataset(
    request: DatasetRequest,
    base_data_dir: Path,
    version: str,
) -> DatasetBuildResult:
    """Create dataset version directory, write artifacts and return build result."""
    dataset_id = generate_dataset_id(request)
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )

    dataset_path.mkdir(parents=True, exist_ok=False)

    raw_dir_path = build_raw_dir_path(dataset_path)
    normalized_dir_path = build_normalized_dir_path(dataset_path)

    raw_dir_path.mkdir()
    normalized_dir_path.mkdir()

    metadata_path = build_metadata_path(dataset_path)
    validation_report_path = build_validation_report_path(dataset_path)
    data_path = build_data_path(dataset_path)

    metadata = DatasetMetadata(
        dataset_id=dataset_id,
        version=version,
        provider=request.provider,
        asset_class=request.asset_class,
        symbol=request.symbol,
        data_type=request.data_type,
        price_type=request.price_type,
        interval=request.interval,
        requested_start=request.requested_start,
        requested_end=request.requested_end,
        status=DATASET_STATUS_CREATED,
    )

    validation_report = ValidationReport(
        dataset_id=dataset_id,
        version=version,
        status=VALIDATION_STATUS_NOT_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=0,
        valid_rows=0,
        invalid_rows=0,
    )

    write_metadata(metadata_path, metadata)
    write_validation_report(validation_report_path, validation_report)
    write_empty_ohlcv_csv(data_path)

    return DatasetBuildResult(
        dataset_id=dataset_id,
        version=version,
        dataset_path=dataset_path,
        data_path=data_path,
        metadata_path=metadata_path,
        validation_report_path=validation_report_path,
        status=DATASET_STATUS_CREATED,
    )
