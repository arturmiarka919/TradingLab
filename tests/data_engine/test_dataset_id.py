"""Tests for dataset ID generation."""

from dataclasses import replace
from datetime import date
from pathlib import Path

from tradinglab.data_engine.dataset_id import generate_dataset_id
from tradinglab.data_engine.models import DatasetRequest
from tradinglab.data_engine.storage import build_dataset_version_path


EXPECTED_EURUSD_DAILY_ID = (
    "polygon_massive_forex_eurusd_ohlcv_provider_1d_"
    "2024-01-01_2024-12-31"
)


def test_generate_dataset_id_for_eurusd_daily_ohlcv() -> None:
    request = _build_dataset_request()

    dataset_id = generate_dataset_id(request)

    assert dataset_id == EXPECTED_EURUSD_DAILY_ID
    assert dataset_id == dataset_id.lower()
    assert "/" not in dataset_id
    assert " " not in dataset_id


def test_generate_dataset_id_normalizes_symbol_variants() -> None:
    symbols = [
        "EUR/USD",
        "EUR USD",
        " eur / usd ",
        "eur-usd",
        "EUR_USD",
    ]

    for symbol in symbols:
        request = _build_dataset_request(symbol=symbol)

        assert generate_dataset_id(request) == EXPECTED_EURUSD_DAILY_ID


def test_generate_dataset_id_normalizes_common_text_parts() -> None:
    request = _build_dataset_request(
        provider=" Polygon Massive ",
        asset_class=" Forex ",
        data_type=" OHLCV ",
        price_type=" Provider ",
        interval=" 1D ",
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id == EXPECTED_EURUSD_DAILY_ID
    assert dataset_id == dataset_id.lower()
    assert " " not in dataset_id


def test_generate_dataset_id_is_deterministic() -> None:
    request = _build_dataset_request()

    first_dataset_id = generate_dataset_id(request)
    second_dataset_id = generate_dataset_id(request)

    assert first_dataset_id == second_dataset_id


def test_generate_dataset_id_normalizes_special_characters_in_text_parts() -> None:
    request = _build_dataset_request(
        provider=" Polygon + Massive!!! ",
        asset_class="Forex & CFD",
        data_type="OHLCV candles",
        price_type="Provider/Raw",
        interval="1 D",
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id == (
        "polygon_massive_forex_cfd_eurusd_ohlcv_candles_"
        "provider_raw_1_d_2024-01-01_2024-12-31"
    )
    assert "/" not in dataset_id
    assert " " not in dataset_id


def test_generate_dataset_id_removes_redundant_text_separators() -> None:
    request = _build_dataset_request(
        provider="__Polygon    Massive__",
        asset_class="___Forex___",
        data_type="OHLCV___Candles",
        price_type="__Provider___Raw__",
        interval="__1D__",
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id == (
        "polygon_massive_forex_eurusd_ohlcv_candles_"
        "provider_raw_1d_2024-01-01_2024-12-31"
    )
    assert "__" not in dataset_id


def test_generate_dataset_id_normalizes_symbol_with_many_special_characters() -> None:
    symbols = [
        "E/U/R U-S_D",
        " EUR///USD!!! ",
        "EUR.USD",
        "E@U#R$U%S^D",
    ]

    for symbol in symbols:
        request = _build_dataset_request(symbol=symbol)

        assert generate_dataset_id(request) == EXPECTED_EURUSD_DAILY_ID


def test_generate_dataset_id_uses_requested_date_range() -> None:
    request = _build_dataset_request(
        requested_start=date(2023, 2, 3),
        requested_end=date(2024, 4, 5),
    )

    dataset_id = generate_dataset_id(request)

    assert dataset_id.endswith("_2023-02-03_2024-04-05")


def test_generate_dataset_id_does_not_include_dataset_version() -> None:
    request = _build_dataset_request()

    dataset_id = generate_dataset_id(request)

    assert "v001" not in dataset_id
    assert "v002" not in dataset_id


def test_generate_dataset_id_changes_when_identity_field_changes() -> None:
    base_request = _build_dataset_request()
    variant_requests = [
        replace(base_request, provider="other_provider"),
        replace(base_request, asset_class="crypto"),
        replace(base_request, symbol="GBP/USD"),
        replace(base_request, data_type="ticks"),
        replace(base_request, price_type="mid"),
        replace(base_request, interval="1h"),
        replace(base_request, requested_start=date(2024, 1, 2)),
        replace(base_request, requested_end=date(2025, 1, 1)),
    ]

    base_dataset_id = generate_dataset_id(base_request)
    variant_dataset_ids = {
        generate_dataset_id(variant_request)
        for variant_request in variant_requests
    }

    assert base_dataset_id not in variant_dataset_ids
    assert len(variant_dataset_ids) == len(variant_requests)


def test_generate_dataset_id_can_be_used_in_dataset_version_path() -> None:
    request = _build_dataset_request(
        provider=" Polygon + Massive!!! ",
        symbol=" EUR / USD ",
    )

    dataset_id = generate_dataset_id(request)
    dataset_path = build_dataset_version_path(
        base_data_dir=Path("data"),
        dataset_id=dataset_id,
        version="v001",
    )

    assert dataset_path == Path("data") / "datasets" / dataset_id / "v001"
    assert dataset_id in dataset_path.parts
    assert "/" not in dataset_id
    assert "\\" not in dataset_id
    assert " " not in dataset_id


def _build_dataset_request(**overrides: object) -> DatasetRequest:
    request = DatasetRequest(
        provider="polygon_massive",
        asset_class="forex",
        symbol="EUR/USD",
        data_type="ohlcv",
        price_type="provider",
        interval="1d",
        requested_start=date(2024, 1, 1),
        requested_end=date(2024, 12, 31),
    )

    return replace(request, **overrides)
