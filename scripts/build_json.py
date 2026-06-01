from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "csv"
JSON_DIR = ROOT / "data" / "json"


def convert_csv_to_json(csv_path: Path) -> None:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    out_path = JSON_DIR / f"{csv_path.stem}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    for csv_path in sorted(CSV_DIR.glob("*.csv")):
        if csv_path.name == "schema.csv":
            continue
        convert_csv_to_json(csv_path)


if __name__ == "__main__":
    main()
