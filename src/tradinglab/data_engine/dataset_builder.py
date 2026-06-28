"""Dataset build orchestration helpers for TradingLab Data Engine."""

from pathlib import Path

from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.models import DatasetBuildResult, DatasetRequest
from tradinglab.data_engine.status import DATASET_STATUS_CREATED
from tradinglab.data_engine.storage import (
    build_dataset_version_path,
    build_metadata_path,
    build_validation_report_path,
)


def create_dataset(
    request: DatasetRequest,
    base_data_dir: Path,
    version: str,
) -> DatasetBuildResult:
    """Create dataset version directory and return dataset build result."""

    dataset_id = generate_dataset_id(request)
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )

    dataset_path.mkdir(parents=True, exist_ok=False)

    return DatasetBuildResult(
        dataset_id=dataset_id,
        version=version,
        dataset_path=dataset_path,
        metadata_path=build_metadata_path(dataset_path),
        validation_report_path=build_validation_report_path(dataset_path),
        status=DATASET_STATUS_CREATED,
    )
