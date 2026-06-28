"""Metadata helpers for TradingLab Data Engine."""

from dataclasses import asdict
from datetime import date
from typing import Any

from tradinglab.data_engine.models import DatasetMetadata


def metadata_to_dict(metadata: DatasetMetadata) -> dict[str, Any]:
    """Convert dataset metadata to a JSON-ready dictionary."""

    metadata_dict = asdict(metadata)
    metadata_dict["requested_start"] = _format_date(metadata.requested_start)
    metadata_dict["requested_end"] = _format_date(metadata.requested_end)

    return metadata_dict


def _format_date(value: date) -> str:
    return value.isoformat()
