"""Validation report helpers for TradingLab Data Engine."""

from dataclasses import asdict
from typing import Any

from tradinglab.data_engine.models import ValidationReport


def validation_report_to_dict(report: ValidationReport) -> dict[str, Any]:
    """Convert validation report to a JSON-ready dictionary."""

    report_dict = asdict(report)
    report_dict["errors"] = list(report.errors)
    report_dict["warnings"] = list(report.warnings)

    return report_dict


def validation_report_from_dict(data: dict[str, Any]) -> ValidationReport:
    """Convert dictionary loaded from JSON-like data to validation report."""

    return ValidationReport(
        dataset_id=str(data["dataset_id"]),
        version=str(data["version"]),
        status=str(data["status"]),
        errors=tuple(str(error) for error in data["errors"]),
        warnings=tuple(str(warning) for warning in data["warnings"]),
        checked_rows=int(data["checked_rows"]),
        valid_rows=int(data["valid_rows"]),
        invalid_rows=int(data["invalid_rows"]),
    )
