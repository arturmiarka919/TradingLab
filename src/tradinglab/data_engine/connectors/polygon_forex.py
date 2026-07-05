"""Polygon/Massive Forex response normalization."""

from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation

from tradinglab.data_engine.connectors.base import ProviderRawResponse
from tradinglab.data_engine.models import OhlcvBar


POLYGON_MASSIVE_PROVIDER = "polygon_massive"
REQUIRED_POLYGON_OHLCV_FIELDS = ("t", "o", "h", "l", "c", "v")


class PolygonForexPayloadError(ValueError):
    """Raised when Polygon/Massive Forex payload cannot be normalized."""


def normalize_polygon_forex_ohlcv_response(
    raw_response: ProviderRawResponse,
) -> list[OhlcvBar]:
    """Normalize Polygon/Massive Forex OHLCV payload to OHLCV bars."""

    if raw_response.provider != POLYGON_MASSIVE_PROVIDER:
        raise PolygonForexPayloadError(
            "Polygon forex normalizer expected provider "
            f"{POLYGON_MASSIVE_PROVIDER!r}, got {raw_response.provider!r}."
        )

    payload = _require_mapping(
        raw_response.raw_payload,
        message="Polygon forex raw_payload must be a mapping.",
    )

    if "results" not in payload:
        raise PolygonForexPayloadError(
            "Polygon forex payload is missing required field 'results'."
        )

    raw_results = payload["results"]

    if not isinstance(raw_results, list):
        raise PolygonForexPayloadError(
            "Polygon forex payload field 'results' must be a list."
        )

    return [
        _normalize_result(result, result_index=result_index)
        for result_index, result in enumerate(raw_results)
    ]


def _normalize_result(result: object, *, result_index: int) -> OhlcvBar:
    result_mapping = _require_mapping(
        result,
        message=(
            "Polygon forex result item at index "
            f"{result_index} must be a mapping."
        ),
    )

    for field_name in REQUIRED_POLYGON_OHLCV_FIELDS:
        _require_field(result_mapping, field_name, result_index=result_index)

    return OhlcvBar(
        timestamp=_timestamp_from_unix_ms(
            result_mapping["t"],
            result_index=result_index,
        ),
        open=_decimal_from_provider_value(
            result_mapping["o"],
            field_name="o",
            result_index=result_index,
        ),
        high=_decimal_from_provider_value(
            result_mapping["h"],
            field_name="h",
            result_index=result_index,
        ),
        low=_decimal_from_provider_value(
            result_mapping["l"],
            field_name="l",
            result_index=result_index,
        ),
        close=_decimal_from_provider_value(
            result_mapping["c"],
            field_name="c",
            result_index=result_index,
        ),
        volume=_decimal_from_provider_value(
            result_mapping["v"],
            field_name="v",
            result_index=result_index,
        ),
    )


def _require_mapping(value: object, *, message: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PolygonForexPayloadError(message)

    return value


def _require_field(
    result_mapping: Mapping[str, object],
    field_name: str,
    *,
    result_index: int,
) -> None:
    if field_name not in result_mapping:
        raise PolygonForexPayloadError(
            "Polygon forex result item at index "
            f"{result_index} is missing required field {field_name!r}."
        )


def _timestamp_from_unix_ms(value: object, *, result_index: int) -> datetime:
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=UTC)
    except (TypeError, ValueError, OverflowError, OSError) as exc:
        raise PolygonForexPayloadError(
            "Polygon forex result item at index "
            f"{result_index} field 't' must be Unix milliseconds "
            "convertible to UTC datetime."
        ) from exc


def _decimal_from_provider_value(
    value: object,
    *,
    field_name: str,
    result_index: int,
) -> Decimal:
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PolygonForexPayloadError(
            "Polygon forex result item at index "
            f"{result_index} field {field_name!r} must be convertible "
            "to Decimal."
        ) from exc

    if not decimal_value.is_finite():
        raise PolygonForexPayloadError(
            "Polygon forex result item at index "
            f"{result_index} field {field_name!r} must be a finite Decimal."
        )

    return decimal_value
