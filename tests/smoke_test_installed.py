import csv
import json
from importlib.metadata import version
from importlib.resources import files

import jp_child_allowance_data


assert jp_child_allowance_data.__version__ == "0.3.0"
assert version("jp-child-allowance-data") == "0.3.0"
assert jp_child_allowance_data.get_monthly_amount(age=2, child_order=1, date="2026-06-01") == 15000
assert jp_child_allowance_data.get_monthly_amount(age=2, child_order=3, date="2026-06-01") == 30000
assert jp_child_allowance_data.get_payment_months(2026, date="2026-06-01") == [2, 4, 6, 8, 10, 12]

data_root = files("jp_child_allowance_data").joinpath("data")
csv_dir = data_root.joinpath("csv")
json_dir = data_root.joinpath("json")

csv_names = [
    "allowance_rules.csv",
    "payment_schedule.csv",
    "reform_history.csv",
    "schema.csv",
    "sources.csv",
]
json_names = [
    "allowance_rules.json",
    "payment_schedule.json",
    "reform_history.json",
    "sources.json",
]

for name in csv_names:
    resource = csv_dir.joinpath(name)
    assert resource.is_file()
    with resource.open("r", encoding="utf-8", newline="") as f:
        assert list(csv.DictReader(f))

for name in json_names:
    resource = json_dir.joinpath(name)
    assert resource.is_file()
    with resource.open("r", encoding="utf-8") as f:
        assert json.load(f)

assert jp_child_allowance_data.get_reform_history()
assert jp_child_allowance_data.load_sources()
