"""Tests for Data Engine dataset status constants."""

from tradinglab.data_engine.status import (
    DATASET_STATUS_CREATED,
    DATASET_STATUS_INVALID,
    DATASET_STATUS_VALIDATED,
)


def test_dataset_status_constants_have_expected_values() -> None:
    assert DATASET_STATUS_CREATED == "created"
    assert DATASET_STATUS_VALIDATED == "validated"
    assert DATASET_STATUS_INVALID == "invalid"


def test_dataset_status_constants_are_unique() -> None:
    statuses = {
        DATASET_STATUS_CREATED,
        DATASET_STATUS_VALIDATED,
        DATASET_STATUS_INVALID,
    }

    assert len(statuses) == 3
