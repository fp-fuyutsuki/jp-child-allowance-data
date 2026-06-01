from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "csv"

REQUIRED_FILES = [
    "allowance_rules.csv",
    "payment_schedule.csv",
    "reform_history.csv",
    "sources.csv",
]


def read_rows(name: str):
    path = CSV_DIR / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    for name in REQUIRED_FILES:
        rows = read_rows(name)
        if not rows:
            raise ValueError(f"{name} has no rows")

    sources = {row["source_id"] for row in read_rows("sources.csv")}
    for filename in ["allowance_rules.csv", "payment_schedule.csv", "reform_history.csv"]:
        for row in read_rows(filename):
            if row["source_id"] not in sources:
                raise ValueError(f"Unknown source_id in {filename}: {row['source_id']}")

    for row in read_rows("allowance_rules.csv"):
        amount = int(row["monthly_amount_yen"])
        if amount < 0:
            raise ValueError("monthly_amount_yen must be non-negative")
        if int(row["age_min"]) > int(row["age_max"]):
            raise ValueError("age_min must be <= age_max")
        if row["child_order_max"] and int(row["child_order_min"]) > int(row["child_order_max"]):
            raise ValueError("child_order_min must be <= child_order_max")


if __name__ == "__main__":
    main()
