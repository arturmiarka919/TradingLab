"""Tests for Data Engine validation report helpers."""

import json
from pathlib import Path

import pytest

from tradinglab.data_engine.models import ValidationReport
from tradinglab.data_engine.status import VALIDATION_STATUS_INVALID
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
    status=VALIDATION_STATUS_INVALID,
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


def test_write_and_from_dict_roundtrip_preserves_validation_report(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    write_validation_report(report_path, EXPECTED_VALIDATION_REPORT)

    loaded_data = json.loads(report_path.read_text(encoding="utf-8"))
    loaded_report = validation_report_from_dict(loaded_data)

    assert loaded_report == EXPECTED_VALIDATION_REPORT


def test_load_validation_report_reads_validation_report_json(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    write_validation_report(report_path, EXPECTED_VALIDATION_REPORT)

    loaded_report = load_validation_report(report_path)

    assert loaded_report == EXPECTED_VALIDATION_REPORT


def test_validation_report_from_dict_raises_error_when_required_field_is_missing() -> None:
    report_data = dict(EXPECTED_VALIDATION_REPORT_DICT)
    del report_data["dataset_id"]

    with pytest.raises(KeyError):
        validation_report_from_dict(report_data)


def test_load_validation_report_raises_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"
    report_path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_validation_report(report_path)


def test_load_validation_report_raises_error_when_file_is_missing(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    with pytest.raises(FileNotFoundError):
        load_validation_report(report_path)


def test_validation_report_from_dict_normalizes_text_values_to_str() -> None:
    report_data = {
        **EXPECTED_VALIDATION_REPORT_DICT,
        "dataset_id": 123,
        "version": 1,
        "status": False,
        "errors": [10, None],
        "warnings": [True, "warning"],
    }

    report = validation_report_from_dict(report_data)

    assert report.dataset_id == "123"
    assert report.version == "1"
    assert report.status == "False"
    assert report.errors == ("10", "None")
    assert report.warnings == ("True", "warning")


def test_validation_report_from_dict_converts_counter_values_to_int() -> None:
    report_data = {
        **EXPECTED_VALIDATION_REPORT_DICT,
        "checked_rows": "252",
        "valid_rows": "251",
        "invalid_rows": "1",
    }

    report = validation_report_from_dict(report_data)

    assert report.checked_rows == 252
    assert report.valid_rows == 251
    assert report.invalid_rows == 1


def test_validation_report_from_dict_raises_error_for_invalid_counter() -> None:
    report_data = {
        **EXPECTED_VALIDATION_REPORT_DICT,
        "checked_rows": "not-a-number",
    }

    with pytest.raises(ValueError):
        validation_report_from_dict(report_data)


def test_write_validation_report_preserves_non_ascii_characters(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"
    report = ValidationReport(
        dataset_id="\u017c\u00f3\u0142\u0107_dataset",
        version="v001",
        status=VALIDATION_STATUS_INVALID,
        errors=(
            "b\u0142\u0105d \u015bwiecy: "
            "zamkni\u0119cie ni\u017csze ni\u017c minimum",
        ),
        warnings=("ostrze\u017cenie: wolumen zale\u017cny od dostawcy",),
        checked_rows=1,
        valid_rows=0,
        invalid_rows=1,
    )

    write_validation_report(report_path, report)

    json_text = report_path.read_text(encoding="utf-8")

    assert "\u017c\u00f3\u0142\u0107_dataset" in json_text
    assert "b\u0142\u0105d \u015bwiecy" in json_text
    assert "ostrze\u017cenie" in json_text


def test_write_validation_report_writes_single_trailing_newline(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "validation_report.json"

    write_validation_report(report_path, EXPECTED_VALIDATION_REPORT)

    json_text = report_path.read_text(encoding="utf-8")

    assert json_text.endswith("\n")
    assert not json_text.endswith("\n\n")
