import csv
import shutil
from pathlib import Path

import pytest

from jp_child_allowance_data.validation import validate_csv_dir


ROOT = Path(__file__).resolve().parents[1]
CSV_SOURCE_DIR = ROOT / "jp_child_allowance_data" / "data" / "csv"


def _copy_csv_dir(tmp_path: Path) -> Path:
    dst = tmp_path / "csv"
    shutil.copytree(CSV_SOURCE_DIR, dst)
    return dst


def _rewrite_csv(path: Path, *, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_validate_csv_dir_passes_on_repo_data():
    validate_csv_dir(CSV_SOURCE_DIR)


def test_validate_missing_required_column_fails(tmp_path: Path):
    csv_dir = _copy_csv_dir(tmp_path)
    target = csv_dir / "sources.csv"

    with target.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Drop a required column and ensure validation fails.
    new_fieldnames = [c for c in reader.fieldnames if c != "url"]
    for row in rows:
        row.pop("url", None)

    _rewrite_csv(target, fieldnames=new_fieldnames, rows=rows)

    with pytest.raises(ValueError, match=r"sources\.csv: missing required columns: url"):
        validate_csv_dir(csv_dir)


def test_validate_bad_date_fails(tmp_path: Path):
    csv_dir = _copy_csv_dir(tmp_path)
    target = csv_dir / "reform_history.csv"

    with target.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    rows[0]["effective_date"] = "2024/10/01"
    _rewrite_csv(target, fieldnames=fieldnames, rows=rows)

    with pytest.raises(ValueError, match=r"reform_history\.csv:2: invalid date"):
        validate_csv_dir(csv_dir)


def test_validate_non_int_fails(tmp_path: Path):
    csv_dir = _copy_csv_dir(tmp_path)
    target = csv_dir / "payment_schedule.csv"

    with target.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    rows[0]["payment_month"] = "June"
    _rewrite_csv(target, fieldnames=fieldnames, rows=rows)

    with pytest.raises(ValueError, match=r"payment_schedule\.csv:2: invalid integer"):
        validate_csv_dir(csv_dir)
