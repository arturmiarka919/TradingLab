"""Dataset ID generation for TradingLab Data Engine."""

import re
from datetime import date

from tradinglab.data_engine.models import DatasetRequest


def generate_dataset_id(request: DatasetRequest) -> str:
    """Generate deterministic dataset ID from dataset request."""

    parts = [
        _normalize_part(request.provider),
        _normalize_part(request.asset_class),
        _normalize_symbol(request.symbol),
        _normalize_part(request.data_type),
        _normalize_part(request.price_type),
        _normalize_part(request.interval),
        _format_date(request.requested_start),
        _format_date(request.requested_end),
    ]

    return "_".join(parts)


def _normalize_part(value: str) -> str:
    normalized = value.strip().lower()
    normalized = normalized.replace(" ", "_")
    normalized = re.sub(r"[^a-z0-9_-]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)

    return normalized.strip("_")


def _normalize_symbol(value: str) -> str:
    normalized = value.strip().lower()

    return re.sub(r"[^a-z0-9]+", "", normalized)


def _format_date(value: date) -> str:
    return value.isoformat()
