"""Metadata helpers for TradingLab Data Engine."""

from dataclasses import asdict
from datetime import date
import json
from pathlib import Path
from typing import Any

from tradinglab.data_engine.models import DatasetMetadata


def metadata_to_dict(metadata: DatasetMetadata) -> dict[str, Any]:
    """Convert dataset metadata to a JSON-ready dictionary."""

    metadata_dict = asdict(metadata)
    metadata_dict["requested_start"] = _format_date(metadata.requested_start)
    metadata_dict["requested_end"] = _format_date(metadata.requested_end)

    return metadata_dict


def metadata_from_dict(data: dict[str, Any]) -> DatasetMetadata:
    """Convert dictionary loaded from JSON-like data to dataset metadata."""

    return DatasetMetadata(
        dataset_id=str(data["dataset_id"]),
        version=str(data["version"]),
        provider=str(data["provider"]),
        asset_class=str(data["asset_class"]),
        symbol=str(data["symbol"]),
        data_type=str(data["data_type"]),
        price_type=str(data["price_type"]),
        interval=str(data["interval"]),
        requested_start=_parse_date(str(data["requested_start"])),
        requested_end=_parse_date(str(data["requested_end"])),
        status=str(data["status"]),
    )


def write_metadata(path: Path, metadata: DatasetMetadata) -> None:
    """Write dataset metadata to a JSON file."""

    metadata_dict = metadata_to_dict(metadata)
    json_text = json.dumps(metadata_dict, ensure_ascii=False, indent=2)

    path.write_text(f"{json_text}\n", encoding="utf-8")


def _format_date(value: date) -> str:
    return value.isoformat()


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)
