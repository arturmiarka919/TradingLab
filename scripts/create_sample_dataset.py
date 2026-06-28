"""Create local sample OHLCV dataset for manual inspection."""

from pathlib import Path

from tradinglab.data_engine.sample_dataset import create_sample_ohlcv_dataset


def main() -> None:
    """Create sample dataset under local data directory."""

    result = create_sample_ohlcv_dataset(
        base_data_dir=Path("data"),
        overwrite=True,
    )

    print("Sample dataset created.")
    print(f"Dataset path: {result.dataset_path}")
    print(f"Metadata path: {result.metadata_path}")
    print(f"Validation report path: {result.validation_report_path}")
    print(f"Data path: {result.data_path}")


if __name__ == "__main__":
    main()
