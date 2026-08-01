import pytest

from jp_child_allowance_data.loaders import load_csv


def test_load_csv_resource():
    rows = load_csv("allowance_rules.csv")
    assert rows
    assert rows[0]["monthly_amount_yen"] == "15000"


def test_load_csv_missing_leaf_fails():
    with pytest.raises(FileNotFoundError):
        load_csv("missing.csv")


@pytest.mark.parametrize(
    "name",
    [
        "",
        ".",
        "..",
        "../sources.csv",
        r"..\sources.csv",
        "data/sources.csv",
        r"data\sources.csv",
        "/sources.csv",
        r"C:\sources.csv",
        "C:sources.csv",
        r"\\server\share\sources.csv",
        "sources.txt",
        "sources.csv\x00",
    ],
)
def test_load_csv_rejects_unsafe_resource_names(name: str):
    with pytest.raises(ValueError):
        load_csv(name)
