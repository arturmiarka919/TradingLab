"""Storage path helpers for TradingLab Data Engine."""

from pathlib import Path


def build_dataset_version_path(
    base_data_dir: Path,
    dataset_id: str,
    version: str,
) -> Path:
    """Build path for a specific dataset version without creating directories."""
    return base_data_dir / "datasets" / dataset_id / version


def build_metadata_path(dataset_path: Path) -> Path:
    """Build metadata JSON path for a dataset version."""
    return dataset_path / "metadata.json"


def build_validation_report_path(dataset_path: Path) -> Path:
    """Build validation report JSON path for a dataset version."""
    return dataset_path / "validation_report.json"


def build_data_path(dataset_path: Path) -> Path:
    """Build temporary main data CSV path for a dataset version."""
    return dataset_path / "data.csv"


def build_raw_dir_path(dataset_path: Path) -> Path:
    """Build raw data directory path for a dataset version."""
    return dataset_path / "raw"


def build_raw_response_path(dataset_path: Path) -> Path:
    """Build raw provider response JSON path for a dataset version."""
    return build_raw_dir_path(dataset_path) / "response.json"


def build_normalized_dir_path(dataset_path: Path) -> Path:
    """Build normalized data directory path for a dataset version."""
    return dataset_path / "normalized"


def build_normalized_candles_path(dataset_path: Path) -> Path:
    """Build normalized OHLCV candles CSV path for a dataset version."""
    return build_normalized_dir_path(dataset_path) / "candles.csv"
