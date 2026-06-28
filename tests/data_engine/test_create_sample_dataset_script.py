"""Tests for manual sample dataset script execution."""

import subprocess
import sys
from pathlib import Path


def test_create_sample_dataset_script_runs_from_command_line(
    tmp_path: Path,
) -> None:
    project_root = Path(__file__).resolve().parents[2]
    script_path = project_root / "scripts" / "create_sample_dataset.py"

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Sample dataset created." in result.stdout
    assert "Dataset path:" in result.stdout
    assert "Metadata path:" in result.stdout
    assert "Validation report path:" in result.stdout
    assert "Data path:" in result.stdout
    assert (tmp_path / "data" / "datasets").is_dir()
