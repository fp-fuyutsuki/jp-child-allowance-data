from importlib.metadata import version

import jp_child_allowance_data


def test_runtime_version():
    assert jp_child_allowance_data.__version__ == "0.3.0"


def test_distribution_version():
    assert version("jp-child-allowance-data") == "0.3.0"
