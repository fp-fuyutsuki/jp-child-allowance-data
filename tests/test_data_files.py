import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(name):
    with (ROOT / "data" / "csv" / name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_source_ids_are_defined():
    sources = {row["source_id"] for row in read_csv("sources.csv")}
    for filename in ["allowance_rules.csv", "payment_schedule.csv", "reform_history.csv"]:
        for row in read_csv(filename):
            assert row["source_id"] in sources


def test_json_files_exist():
    for name in ["allowance_rules", "payment_schedule", "reform_history", "sources"]:
        assert (ROOT / "data" / "json" / f"{name}.json").exists()
