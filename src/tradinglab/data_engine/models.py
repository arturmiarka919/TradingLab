"""Data models for TradingLab Data Engine."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class DatasetRequest:
    """Request describing a market data dataset."""

    provider: str
    asset_class: str
    symbol: str
    data_type: str
    price_type: str
    interval: str
    requested_start: date
    requested_end: date


@dataclass(frozen=True)
class DatasetMetadata:
    """Metadata describing a stored dataset version."""

    dataset_id: str
    version: str
    provider: str
    asset_class: str
    symbol: str
    data_type: str
    price_type: str
    interval: str
    requested_start: date
    requested_end: date
    status: str


@dataclass(frozen=True)
class ValidationReport:
    """Validation results for a dataset version."""

    dataset_id: str
    version: str
    status: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    checked_rows: int
    valid_rows: int
    invalid_rows: int


@dataclass(frozen=True)
class DatasetBuildResult:
    """Result describing created dataset version artifacts."""

    dataset_id: str
    version: str
    dataset_path: Path
    metadata_path: Path
    validation_report_path: Path
    status: str
