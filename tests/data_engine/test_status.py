"""Tests for Data Engine status constants."""

from tradinglab.data_engine.status import (
    DATASET_LIFECYCLE_STATUS_ACCEPTED,
    DATASET_LIFECYCLE_STATUS_DEPRECATED,
    DATASET_LIFECYCLE_STATUS_QUARANTINED,
    DATASET_LIFECYCLE_STATUS_RAW,
    DATASET_LIFECYCLE_STATUS_REJECTED,
    DATASET_LIFECYCLE_STATUS_VALIDATED,
    DATASET_LIFECYCLE_STATUSES,
    DATASET_STATUS_CREATED,
    DATASET_STATUS_INVALID,
    DATASET_STATUS_VALIDATED,
    LEGACY_DATASET_STATUSES,
    VALIDATION_STATUS_INVALID,
    VALIDATION_STATUS_NOT_VALIDATED,
    VALIDATION_STATUS_VALID,
    VALIDATION_STATUS_VALID_WITH_WARNINGS,
    VALIDATION_STATUSES,
)


def test_dataset_lifecycle_status_constants_have_expected_values() -> None:
    assert DATASET_LIFECYCLE_STATUS_RAW == "RAW"
    assert DATASET_LIFECYCLE_STATUS_VALIDATED == "VALIDATED"
    assert DATASET_LIFECYCLE_STATUS_ACCEPTED == "ACCEPTED"
    assert DATASET_LIFECYCLE_STATUS_QUARANTINED == "QUARANTINED"
    assert DATASET_LIFECYCLE_STATUS_REJECTED == "REJECTED"
    assert DATASET_LIFECYCLE_STATUS_DEPRECATED == "DEPRECATED"


def test_validation_status_constants_have_expected_values() -> None:
    assert VALIDATION_STATUS_NOT_VALIDATED == "not_validated"
    assert VALIDATION_STATUS_VALID == "valid"
    assert VALIDATION_STATUS_VALID_WITH_WARNINGS == "valid_with_warnings"
    assert VALIDATION_STATUS_INVALID == "invalid"


def test_legacy_dataset_status_constants_have_expected_values() -> None:
    assert DATASET_STATUS_CREATED == "created"
    assert DATASET_STATUS_VALIDATED == "validated"
    assert DATASET_STATUS_INVALID == "invalid"


def test_dataset_lifecycle_statuses_are_unique() -> None:
    assert len(DATASET_LIFECYCLE_STATUSES) == 6
    assert len(set(DATASET_LIFECYCLE_STATUSES)) == len(DATASET_LIFECYCLE_STATUSES)


def test_validation_statuses_are_unique() -> None:
    assert len(VALIDATION_STATUSES) == 4
    assert len(set(VALIDATION_STATUSES)) == len(VALIDATION_STATUSES)


def test_legacy_dataset_statuses_are_unique() -> None:
    assert len(LEGACY_DATASET_STATUSES) == 3
    assert len(set(LEGACY_DATASET_STATUSES)) == len(LEGACY_DATASET_STATUSES)


def test_dataset_lifecycle_and_validation_statuses_do_not_overlap() -> None:
    assert set(DATASET_LIFECYCLE_STATUSES).isdisjoint(VALIDATION_STATUSES)
