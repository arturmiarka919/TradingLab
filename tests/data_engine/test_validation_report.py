"""Tests for Data Engine validation report helpers."""

import json
from pathlib import Path

from tradinglab.data_engine.models import ValidationReport
from tradinglab.data_engine.status import DATASET_STATUS_INVALID
from tradinglab.data_engine.validation_report import (
    load_validation_report,
    validation_report_from_dict,
    validation_report_to_dict,
    write_validation_report,
)


EXPECTED_VALIDATION_REPORT_DICT = {
    "dataset_id": (
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    ),
    "version": "v001",
    "status": "invalid",
    "errors": ["row 10: close price is missing"],
    "warnings": ["volume is provider-specific"],
    "checked_rows": 252,
    "valid_rows": 251,
    "invalid_rows": 1,
}


EXPECTED_VALIDATION_REPORT = ValidationReport(
    dataset_id=(
        "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
        "2024-01-01_2024-12-31"
    ),
    version="v001",
    status=DATASET_STATUS_INVALID,
    errors=("row 10: close price is missing",),
    warnings=("volume is provider-specific",),
    checked_rows=252,
    valid_rows=251,
    invalid_rows=1,
)


def test_validation_report_to_dict_serializes_validation_report() -> None:
    report_dict = validation_report_to_dict(EXPECTED_VALIDATION_REPORT)

    assert report_dict == EXPECTED_VALIDATION_REPORT_DICT


def test_validation_report_from_dict_deserializes_validation_report() -> None:
    report = validation_report_from_dict(EXPECTED_VALIDATION_REPORT_DICT)

    assert report == EXPECTED_VALIDATION_REPORT


def test_write_validation_report_writes_validation_report_json(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    write_validation_report(report_path, EXPECTED_VALIDATION_REPORT)

    assert report_path.exists()
    assert (
        json.loads(report_path.read_text(encoding="utf-8"))
        == EXPECTED_VALIDATION_REPORT_DICT
    )


def test_load_validation_report_reads_validation_report_json(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    write_validation_report(report_path, EXPECTED_VALIDATION_REPORT)

    loaded_report = load_validation_report(report_path)

    assert loaded_report == EXPECTED_VALIDATION_REPORT
