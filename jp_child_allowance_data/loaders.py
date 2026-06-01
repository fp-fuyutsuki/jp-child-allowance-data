from __future__ import annotations

import csv
from importlib.resources import files
from pathlib import Path
from typing import Any

PACKAGE_ROOT = files("jp_child_allowance_data")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_CSV_DIR = PROJECT_ROOT / "data" / "csv"


def load_csv(name: str) -> list[dict[str, Any]]:
    """Load a CSV file from the repository data/csv directory."""
    path = DATA_CSV_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"CSV data file not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
