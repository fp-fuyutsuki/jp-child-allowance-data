import pytest

from scripts.check_dist_contents import _archive_basename


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (
            "dist/jp_child_allowance_data-0.3.0-py3-none-any.whl",
            "jp_child_allowance_data-0.3.0-py3-none-any.whl",
        ),
        (
            r"dist\jp_child_allowance_data-0.3.0-py3-none-any.whl",
            "jp_child_allowance_data-0.3.0-py3-none-any.whl",
        ),
        (
            r"C:\temp\jp_child_allowance_data-0.3.0-py3-none-any.whl",
            "jp_child_allowance_data-0.3.0-py3-none-any.whl",
        ),
        (
            "dist/jp_child_allowance_data-0.3.0.tar.gz",
            "jp_child_allowance_data-0.3.0.tar.gz",
        ),
        (
            r"dist\jp_child_allowance_data-0.3.0.tar.gz",
            "jp_child_allowance_data-0.3.0.tar.gz",
        ),
        (
            r"C:\temp\jp_child_allowance_data-0.3.0.tar.gz",
            "jp_child_allowance_data-0.3.0.tar.gz",
        ),
    ],
)
def test_archive_basename_is_os_independent(path, expected):
    assert _archive_basename(path) == expected
