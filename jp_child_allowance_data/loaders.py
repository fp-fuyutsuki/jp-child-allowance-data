from __future__ import annotations

import csv
from importlib.resources import files
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any

PACKAGE_ROOT = files("jp_child_allowance_data")
DATA_CSV_DIR = PACKAGE_ROOT.joinpath("data").joinpath("csv")


def _validate_csv_name(name: str) -> None:
    if not isinstance(name, str):
        raise ValueError("CSV resource name must be a string")
    if (
        not name
        or name in {".", ".."}
        or "\x00" in name
        or "/" in name
        or "\\" in name
        or ":" in name
        or PurePosixPath(name).is_absolute()
        or PureWindowsPath(name).is_absolute()
        or PureWindowsPath(name).drive
        or not name.lower().endswith(".csv")
    ):
        raise ValueError("CSV resource name must be a single CSV filename")


def load_csv(name: str) -> list[dict[str, Any]]:
    """Load a CSV resource from the installed package."""
    _validate_csv_name(name)
    resource = DATA_CSV_DIR.joinpath(name)
    if not resource.is_file():
        raise FileNotFoundError(f"CSV data resource not found: {name}")
    with resource.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
