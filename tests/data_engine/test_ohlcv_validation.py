"""Tests for Data Engine OHLCV validation helpers."""

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from tradinglab.data_engine import OhlcvBar, ValidationReport
from tradinglab.data_engine.data_file import write_ohlcv_csv
from tradinglab.data_engine.ohlcv_validation import validate_ohlcv_csv
from tradinglab.data_engine.status import (
    DATASET_STATUS_INVALID,
    DATASET_STATUS_VALIDATED,
)


def test_validate_ohlcv_csv_returns_validated_report_for_valid_file(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    bars = _build_sample_bars()

    write_ohlcv_csv(data_path, bars)

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report == ValidationReport(
        dataset_id="dataset_1",
        version="v001",
        status=DATASET_STATUS_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=2,
        valid_rows=2,
        invalid_rows=0,
    )


def test_validate_ohlcv_csv_returns_invalid_report_for_invalid_header(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text("wrong,header\n", encoding="utf-8")

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report == ValidationReport(
        dataset_id="dataset_1",
        version="v001",
        status=DATASET_STATUS_INVALID,
        errors=("OHLCV CSV header does not match expected header.",),
        warnings=(),
        checked_rows=0,
        valid_rows=0,
        invalid_rows=0,
    )


def test_validate_ohlcv_csv_returns_invalid_report_for_negative_volume(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            OhlcvBar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
                open=Decimal("1.1000"),
                high=Decimal("1.1200"),
                low=Decimal("1.0900"),
                close=Decimal("1.1100"),
                volume=Decimal("-1.00"),
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report == ValidationReport(
        dataset_id="dataset_1",
        version="v001",
        status=DATASET_STATUS_INVALID,
        errors=("Row 2: volume must be greater than or equal to 0.",),
        warnings=(),
        checked_rows=1,
        valid_rows=0,
        invalid_rows=1,
    )


def test_validate_ohlcv_csv_returns_invalid_report_for_wrong_price_range(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            OhlcvBar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
                open=Decimal("1.1000"),
                high=Decimal("1.0900"),
                low=Decimal("1.1200"),
                close=Decimal("1.1100"),
                volume=Decimal("12345.67"),
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert report.checked_rows == 1
    assert report.valid_rows == 0
    assert report.invalid_rows == 1
    assert "Row 2: high must be greater than or equal to low." in report.errors


def _build_sample_bars() -> tuple[OhlcvBar, OhlcvBar]:
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
