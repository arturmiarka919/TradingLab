"""Tests for Data Engine validation report helpers."""

from tradinglab.data_engine.models import ValidationReport
from tradinglab.data_engine.status import DATASET_STATUS_INVALID
from tradinglab.data_engine.validation_report import (
    validation_report_from_dict,
    validation_report_to_dict,
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
