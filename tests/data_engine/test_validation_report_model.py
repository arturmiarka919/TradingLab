"""Tests for Data Engine validation report model."""

from tradinglab.data_engine.models import ValidationReport
from tradinglab.data_engine.status import (
    DATASET_STATUS_INVALID,
    DATASET_STATUS_VALIDATED,
)


def test_validation_report_can_describe_valid_dataset() -> None:
    report = ValidationReport(
        dataset_id=(
            "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
            "2024-01-01_2024-12-31"
        ),
        version="v001",
        status=DATASET_STATUS_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=252,
        valid_rows=252,
        invalid_rows=0,
    )

    assert report.status == "validated"
    assert report.errors == ()
    assert report.warnings == ()
    assert report.checked_rows == 252
    assert report.valid_rows == 252
    assert report.invalid_rows == 0


def test_validation_report_can_describe_invalid_dataset() -> None:
    report = ValidationReport(
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

    assert report.status == "invalid"
    assert report.errors == ("row 10: close price is missing",)
    assert report.warnings == ("volume is provider-specific",)
    assert report.checked_rows == 252
    assert report.valid_rows == 251
    assert report.invalid_rows == 1
