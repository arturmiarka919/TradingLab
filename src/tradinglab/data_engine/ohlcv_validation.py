"""OHLCV data validation helpers for TradingLab Data Engine."""

from pathlib import Path

from tradinglab.data_engine.data_file import read_ohlcv_csv
from tradinglab.data_engine.models import ValidationReport
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

    return ValidationReport(
        dataset_id=dataset_id,
        version=version,
        status=DATASET_STATUS_VALIDATED,
        errors=(),
        warnings=(),
        checked_rows=checked_rows,
        valid_rows=checked_rows,
        invalid_rows=0,
    )
