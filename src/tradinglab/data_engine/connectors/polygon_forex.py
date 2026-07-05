"""Polygon/Massive Forex response normalization."""

from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal

from tradinglab.data_engine.connectors.base import ProviderRawResponse
from tradinglab.data_engine.models import OhlcvBar


POLYGON_MASSIVE_PROVIDER = "polygon_massive"


def normalize_polygon_forex_ohlcv_response(
    raw_response: ProviderRawResponse,
) -> list[OhlcvBar]:
    """Normalize Polygon/Massive Forex OHLCV payload to OHLCV bars."""

    if raw_response.provider != POLYGON_MASSIVE_PROVIDER:
        raise ValueError(
            "Polygon forex normalizer supports only provider "
            f"{POLYGON_MASSIVE_PROVIDER!r}."
        )

    payload = _require_mapping(
        raw_response.raw_payload,
        message="Polygon forex payload must be a mapping.",
    )
    raw_results = payload.get("results")

    if not isinstance(raw_results, list):
        raise ValueError("Polygon forex payload must contain 'results' list.")

    return [_normalize_result(result) for result in raw_results]


def _normalize_result(result: object) -> OhlcvBar:
    result_mapping = _require_mapping(
        result,
        message="Polygon forex result item must be a mapping.",
    )

    return OhlcvBar(
        timestamp=_timestamp_from_unix_ms(result_mapping["t"]),
        open=_decimal_from_provider_value(result_mapping["o"]),
        high=_decimal_from_provider_value(result_mapping["h"]),
        low=_decimal_from_provider_value(result_mapping["l"]),
        close=_decimal_from_provider_value(result_mapping["c"]),
        volume=_decimal_from_provider_value(result_mapping["v"]),
    )


def _require_mapping(value: object, *, message: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(message)

    return value


def _timestamp_from_unix_ms(value: object) -> datetime:
    return datetime.fromtimestamp(int(value) / 1000, tz=UTC)


def _decimal_from_provider_value(value: object) -> Decimal:
    return Decimal(str(value))
