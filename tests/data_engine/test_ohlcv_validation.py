"""Tests for Data Engine OHLCV validation helpers."""

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

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


def test_validate_ohlcv_csv_returns_invalid_report_for_empty_dataset(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(data_path, ())

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report == ValidationReport(
        dataset_id="dataset_1",
        version="v001",
        status=DATASET_STATUS_INVALID,
        errors=("OHLCV CSV must contain at least one data row.",),
        warnings=(),
        checked_rows=0,
        valid_rows=0,
        invalid_rows=0,
    )


def test_validate_ohlcv_csv_allows_zero_volume_and_flat_candle(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                open_value="1.1000",
                high_value="1.1000",
                low_value="1.1000",
                close_value="1.1000",
                volume_value="0",
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
        status=DATASET_STATUS_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=1,
        valid_rows=1,
        invalid_rows=0,
    )


@pytest.mark.parametrize(
    ("overrides", "expected_error"),
    [
        (
            {"open_value": "0"},
            "Row 2: open must be greater than 0.",
        ),
        (
            {"high_value": "0"},
            "Row 2: high must be greater than 0.",
        ),
        (
            {"low_value": "0"},
            "Row 2: low must be greater than 0.",
        ),
        (
            {"close_value": "0"},
            "Row 2: close must be greater than 0.",
        ),
        (
            {"volume_value": "-1.00"},
            "Row 2: volume must be greater than or equal to 0.",
        ),
        (
            {
                "high_value": "1.0900",
                "low_value": "1.1000",
            },
            "Row 2: high must be greater than or equal to low.",
        ),
        (
            {
                "open_value": "1.1100",
                "high_value": "1.1000",
                "low_value": "1.0800",
                "close_value": "1.0900",
            },
            "Row 2: high must be greater than or equal to open.",
        ),
        (
            {
                "open_value": "1.0900",
                "high_value": "1.1000",
                "low_value": "1.0800",
                "close_value": "1.1100",
            },
            "Row 2: high must be greater than or equal to close.",
        ),
        (
            {
                "open_value": "1.0900",
                "high_value": "1.1200",
                "low_value": "1.1000",
                "close_value": "1.1100",
            },
            "Row 2: low must be less than or equal to open.",
        ),
        (
            {
                "open_value": "1.1100",
                "high_value": "1.1200",
                "low_value": "1.1000",
                "close_value": "1.0900",
            },
            "Row 2: low must be less than or equal to close.",
        ),
    ],
)
def test_validate_ohlcv_csv_returns_invalid_report_for_candle_quality_error(
    tmp_path: Path,
    overrides: dict[str, str],
    expected_error: str,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (_build_bar(**overrides),),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert expected_error in report.errors
    assert report.checked_rows == 1
    assert report.valid_rows == 0
    assert report.invalid_rows == 1


def test_validate_ohlcv_csv_counts_valid_and_invalid_rows_in_same_file(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
                open_value="1.1100",
                high_value="1.1000",
                low_value="1.0800",
                close_value="1.0900",
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert report.errors == (
        "Row 3: high must be greater than or equal to open.",
    )
    assert report.checked_rows == 2
    assert report.valid_rows == 1
    assert report.invalid_rows == 1


def test_validate_ohlcv_csv_rejects_duplicate_timestamps(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert report.errors == (
        "Row 3: timestamp must be unique.",
        "Row 3: timestamp must be greater than previous row timestamp.",
    )
    assert report.checked_rows == 2
    assert report.valid_rows == 1
    assert report.invalid_rows == 1


def test_validate_ohlcv_csv_rejects_non_increasing_timestamps(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
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
        errors=(
            "Row 3: timestamp must be greater than previous row timestamp.",
        ),
        warnings=(),
        checked_rows=2,
        valid_rows=1,
        invalid_rows=1,
    )


def test_validate_ohlcv_csv_counts_timestamp_and_candle_errors_once_per_row(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
                open_value="1.1100",
                high_value="1.1000",
                low_value="1.0800",
                close_value="1.0900",
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert report.errors == (
        "Row 3: high must be greater than or equal to open.",
        "Row 3: timestamp must be unique.",
        "Row 3: timestamp must be greater than previous row timestamp.",
    )
    assert report.checked_rows == 2
    assert report.valid_rows == 1
    assert report.invalid_rows == 1


def test_validate_ohlcv_csv_counts_non_increasing_timestamp_row_as_invalid(
    tmp_path: Path,
) -> None:
    data_path = tmp_path / "data.csv"

    write_ohlcv_csv(
        data_path,
        (
            _build_bar(
                timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 1, 0, 0, tzinfo=UTC),
            ),
            _build_bar(
                timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            ),
        ),
    )

    report = validate_ohlcv_csv(
        data_path=data_path,
        dataset_id="dataset_1",
        version="v001",
    )

    assert report.status == DATASET_STATUS_INVALID
    assert report.errors == (
        "Row 3: timestamp must be greater than previous row timestamp.",
    )
    assert report.checked_rows == 3
    assert report.valid_rows == 2
    assert report.invalid_rows == 1


def _build_sample_bars() -> tuple[OhlcvBar, OhlcvBar]:
    return (
        _build_bar(
            timestamp=datetime(2024, 1, 2, 0, 0, tzinfo=UTC),
            open_value="1.1000",
            high_value="1.1200",
            low_value="1.0900",
            close_value="1.1100",
            volume_value="12345.67",
        ),
        _build_bar(
            timestamp=datetime(2024, 1, 3, 0, 0, tzinfo=UTC),
            open_value="1.1100",
            high_value="1.1300",
            low_value="1.1000",
            close_value="1.1250",
            volume_value="23456.78",
        ),
    )


def _build_bar(
    *,
    timestamp: datetime | None = None,
    open_value: str = "1.1000",
    high_value: str = "1.1200",
    low_value: str = "1.0900",
    close_value: str = "1.1100",
    volume_value: str = "12345.67",
) -> OhlcvBar:
    if timestamp is None:
        timestamp = datetime(2024, 1, 2, 0, 0, tzinfo=UTC)

    return OhlcvBar(
        timestamp=timestamp,
        open=Decimal(open_value),
        high=Decimal(high_value),
        low=Decimal(low_value),
        close=Decimal(close_value),
        volume=Decimal(volume_value),
    )
