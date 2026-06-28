"""Validation report helpers for TradingLab Data Engine."""

from dataclasses import asdict
import json
from pathlib import Path
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


def write_validation_report(path: Path, report: ValidationReport) -> None:
    """Write validation report to a JSON file."""

    report_dict = validation_report_to_dict(report)
    json_text = json.dumps(report_dict, ensure_ascii=False, indent=2)

    path.write_text(f"{json_text}\n", encoding="utf-8")


def load_validation_report(path: Path) -> ValidationReport:
    """Load validation report from a JSON file."""

    loaded_data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

    return validation_report_from_dict(loaded_data)
