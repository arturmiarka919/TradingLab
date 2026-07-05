"""Create local sample OHLCV dataset for manual inspection."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from tradinglab.data_engine import load_dataset  # noqa: E402
from tradinglab.data_engine.sample_dataset import create_sample_ohlcv_dataset  # noqa: E402


def main() -> None:
    """Create, validate and load sample dataset under local data directory."""

    result = create_sample_ohlcv_dataset(
        base_data_dir=Path("data"),
        overwrite=True,
    )
    loaded_dataset = load_dataset(
        base_data_dir=Path("data"),
        dataset_id=result.dataset_id,
        version=result.version,
    )

    print("Sample dataset created.")
    print(f"Dataset path: {result.dataset_path}")
    print(f"Metadata path: {result.metadata_path}")
    print(f"Validation report path: {result.validation_report_path}")
    print(f"Data path: {result.data_path}")
    print(f"Loaded dataset status: {loaded_dataset.status}")
    print(f"Loaded validation status: {loaded_dataset.validation_report.status}")
    print(f"Loaded candles rows: {len(loaded_dataset.normalized_candles)}")


if __name__ == "__main__":
    main()
