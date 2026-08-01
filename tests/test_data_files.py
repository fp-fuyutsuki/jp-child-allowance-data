import csv
import json
from importlib.resources import files
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DATA = files("jp_child_allowance_data").joinpath("data")
CSV_NAMES = {
    "allowance_rules.csv",
    "payment_schedule.csv",
    "reform_history.csv",
    "schema.csv",
    "sources.csv",
}
JSON_NAMES = {
    "allowance_rules.json",
    "payment_schedule.json",
    "reform_history.json",
    "sources.json",
}


def read_csv(name: str):
    resource = PACKAGE_DATA.joinpath("csv").joinpath(name)
    with resource.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_source_ids_are_defined():
    sources = {row["source_id"] for row in read_csv("sources.csv")}
    for filename in ["allowance_rules.csv", "payment_schedule.csv", "reform_history.csv"]:
        for row in read_csv(filename):
            assert row["source_id"] in sources


def test_package_csv_resources_exist():
    csv_dir = PACKAGE_DATA.joinpath("csv")
    assert {entry.name for entry in csv_dir.iterdir() if entry.is_file()} == CSV_NAMES


def test_package_json_resources_exist():
    json_dir = PACKAGE_DATA.joinpath("json")
    assert {entry.name for entry in json_dir.iterdir() if entry.is_file()} == JSON_NAMES


def test_csv_and_json_resources_match():
    for stem in ["allowance_rules", "payment_schedule", "reform_history", "sources"]:
        csv_rows = read_csv(f"{stem}.csv")
        json_resource = PACKAGE_DATA.joinpath("json").joinpath(f"{stem}.json")
        with json_resource.open("r", encoding="utf-8") as f:
            json_rows = json.load(f)
        assert csv_rows == json_rows


def test_old_root_data_directory_is_absent():
    assert not (ROOT / "data").exists()
