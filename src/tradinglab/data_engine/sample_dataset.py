"""Sample dataset helpers for local TradingLab Data Engine demos."""

import json
from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from shutil import rmtree

from tradinglab.data_engine.data_file import write_ohlcv_csv
from tradinglab.data_engine.dataset_builder import create_dataset
from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.metadata import write_metadata
from tradinglab.data_engine.models import (
    DatasetBuildResult,
    DatasetMetadata,
    DatasetRequest,
    OhlcvBar,
)
from tradinglab.data_engine.ohlcv_validation import validate_ohlcv_csv
from tradinglab.data_engine.status import DATASET_LIFECYCLE_STATUS_VALIDATED
from tradinglab.data_engine.storage import (
    build_dataset_version_path,
    build_normalized_candles_path,
    build_raw_response_path,
)
from tradinglab.data_engine.validation_report import write_validation_report

SAMPLE_DATASET_VERSION = "v001"


def build_sample_dataset_request() -> DatasetRequest:
    """Build sample OHLCV dataset request for local demos."""
    return DatasetRequest(
        provider="sample",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="sample",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 1, 3),
    )


def build_sample_ohlcv_bars() -> tuple[OhlcvBar, OhlcvBar]:
    """Build sample OHLCV bars for local demos."""
    return (
        OhlcvBar(
            timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            open=Decimal("1.1000"),
            high=Decimal("1.1200"),
            low=Decimal("1.0900"),
            close=Decimal("1.1100"),
            volume=Decimal("12345.67"),
        ),
        OhlcvBar(
            timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            open=Decimal("1.1100"),
            high=Decimal("1.1300"),
            low=Decimal("1.1000"),
            close=Decimal("1.1250"),
            volume=Decimal("23456.78"),
        ),
    )


def build_sample_raw_response() -> dict[str, object]:
    """Build transitional sample raw provider response for local demos."""
    return {
        "provider": "sample",
        "symbol": "EUR/USD",
        "interval": "1d",
        "results": [
            {
                "timestamp": "2024-01-02T00:00:00Z",
                "open": "1.1000",
                "high": "1.1200",
                "low": "1.0900",
                "close": "1.1100",
                "volume": "12345.67",
            },
            {
                "timestamp": "2024-01-03T00:00:00Z",
                "open": "1.1100",
                "high": "1.1300",
                "low": "1.1000",
                "close": "1.1250",
                "volume": "23456.78",
            },
        ],
    }


def create_sample_ohlcv_dataset(
    base_data_dir: Path,
    version: str = SAMPLE_DATASET_VERSION,
    overwrite: bool = False,
) -> DatasetBuildResult:
    """Create local sample OHLCV dataset, write sample bars and validate it."""
    request = build_sample_dataset_request()
    dataset_id = generate_dataset_id(request)
    dataset_path = build_dataset_version_path(
        base_data_dir=base_data_dir,
        dataset_id=dataset_id,
        version=version,
    )

    if overwrite and dataset_path.exists():
        rmtree(dataset_path)

    result = create_dataset(
        request=request,
        base_data_dir=base_data_dir,
        version=version,
    )

    raw_response_path = build_raw_response_path(result.dataset_path)
    raw_response_path.write_text(
        json.dumps(build_sample_raw_response(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    normalized_candles_path = build_normalized_candles_path(result.dataset_path)
    write_ohlcv_csv(normalized_candles_path, build_sample_ohlcv_bars())

    validation_report = validate_ohlcv_csv(
        data_path=normalized_candles_path,
        dataset_id=result.dataset_id,
        version=result.version,
    )
    write_validation_report(result.validation_report_path, validation_report)

    write_metadata(
        result.metadata_path,
        DatasetMetadata(
            dataset_id=result.dataset_id,
            version=result.version,
            provider=request.provider,
            asset_class=request.asset_class,
            symbol=request.symbol,
            data_type=request.data_type,
            price_type=request.price_type,
            interval=request.interval,
            requested_start=request.requested_start,
            requested_end=request.requested_end,
            status=DATASET_LIFECYCLE_STATUS_VALIDATED,
        ),
    )

    return replace(
        result,
        data_path=normalized_candles_path,
        status=DATASET_LIFECYCLE_STATUS_VALIDATED,
    )
