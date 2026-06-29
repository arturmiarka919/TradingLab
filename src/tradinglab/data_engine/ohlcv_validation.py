"""OHLCV data validation helpers for TradingLab Data Engine."""

from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.models import OhlcvBar, ValidationReport
from tradinglab.data_engine.status import (
    DATASET_STATUS_INVALID,
    DATASET_STATUS_VALIDATED,
)


def validate_ohlcv_csv(
    data_path: Path,
    dataset_id: str,
    version: str,
) -> ValidationReport:
    """Validate OHLCV CSV file and return validation report."""

    try:
        bars = read_ohlcv_csv(data_path)
    except (ArithmeticError, OSError, ValueError) as error:
        return ValidationReport(
            dataset_id=dataset_id,
            version=version,
            status=DATASET_STATUS_INVALID,
            errors=(str(error),),
            warnings=(),
            checked_rows=0,
            valid_rows=0,
            invalid_rows=0,
        )

    checked_rows = len(bars)
    errors: list[str] = []
    invalid_rows = 0

    for csv_row_number, bar in enumerate(bars, start=2):
        row_errors = _validate_ohlcv_bar(
            bar=bar,
            csv_row_number=csv_row_number,
        )

        if row_errors:
            invalid_rows += 1
            errors.extend(row_errors)

    valid_rows = checked_rows - invalid_rows
    status = DATASET_STATUS_INVALID if errors else DATASET_STATUS_VALIDATED

    return ValidationReport(
        dataset_id=dataset_id,
        version=version,
        status=status,
        errors=tuple(errors),
        warnings=(),
        checked_rows=checked_rows,
        valid_rows=valid_rows,
        invalid_rows=invalid_rows,
    )


def _validate_ohlcv_bar(
    bar: OhlcvBar,
    csv_row_number: int,
) -> tuple[str, ...]:
    """Validate single OHLCV bar and return row errors."""

    errors: list[str] = []

    if bar.open <= 0:
        errors.append(f"Row {csv_row_number}: open must be greater than 0.")

    if bar.high <= 0:
        errors.append(f"Row {csv_row_number}: high must be greater than 0.")

    if bar.low <= 0:
        errors.append(f"Row {csv_row_number}: low must be greater than 0.")

    if bar.close <= 0:
        errors.append(f"Row {csv_row_number}: close must be greater than 0.")

    if bar.volume < 0:
        errors.append(
            f"Row {csv_row_number}: volume must be greater than or equal to 0."
        )

    if bar.high < bar.low:
        errors.append(
            f"Row {csv_row_number}: high must be greater than or equal to low."
        )

    if bar.high < bar.open:
        errors.append(
            f"Row {csv_row_number}: high must be greater than or equal to open."
        )

    if bar.high < bar.close:
        errors.append(
            f"Row {csv_row_number}: high must be greater than or equal to close."
        )

    if bar.low > bar.open:
        errors.append(
            f"Row {csv_row_number}: low must be less than or equal to open."
        )

    if bar.low > bar.close:
        errors.append(
            f"Row {csv_row_number}: low must be less than or equal to close."
        )

    return tuple(errors)
