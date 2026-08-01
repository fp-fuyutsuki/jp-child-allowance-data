from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "jp_child_allowance_data" / "data" / "csv"

sys.path.insert(0, str(ROOT))

from jp_child_allowance_data.validation import validate_csv_dir  # noqa: E402


def main() -> None:
    validate_csv_dir(CSV_DIR)


if __name__ == "__main__":
    main()
