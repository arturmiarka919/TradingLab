"""Storage path helpers for TradingLab Data Engine."""

from pathlib import Path


def build_dataset_version_path(
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> Path:
    """Build path for a specific dataset version without creating directories."""

    return base_data_dir / "datasets" / dataset_id / version
