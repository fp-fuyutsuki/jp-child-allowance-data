from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True)
class CsvSpec:
    filename: str
    required_columns: tuple[str, ...]


CSV_SPECS: tuple[CsvSpec, ...] = (
    CsvSpec(
        filename="allowance_rules.csv",
        required_columns=(
            "effective_from",
            "effective_to",
            "age_min",
            "age_max",
            "age_label",
            "child_order_min",
            "child_order_max",
            "monthly_amount_yen",
            "income_status",
            "income_limit_applicable",
            "source_id",
            "notes",
        ),
    ),
    CsvSpec(
        filename="payment_schedule.csv",
        required_columns=(
            "effective_from",
            "effective_to",
            "payment_month",
            "covered_months",
            "source_id",
            "notes",
        ),
    ),
    CsvSpec(
        filename="reform_history.csv",
        required_columns=("effective_date", "title", "summary", "source_id"),
    ),
    CsvSpec(
        filename="sources.csv",
        required_columns=("source_id", "title", "publisher", "url", "accessed_date", "notes"),
    ),
    CsvSpec(
        filename="schema.csv",
        required_columns=("file", "column", "type", "required", "description"),
    ),
)


def _require_columns(*, filename: str, fieldnames: Iterable[str] | None, required: tuple[str, ...]) -> None:
    if not fieldnames:
        raise ValueError(f"{filename}: missing header row")
    present = set(fieldnames)
    missing = [c for c in required if c not in present]
    if missing:
        raise ValueError(f"{filename}: missing required columns: {', '.join(missing)}")


def _parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as e:
        raise ValueError(f"invalid date (expected YYYY-MM-DD): {value}") from e


def _parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"invalid integer: {value}") from e


def _parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ValueError(f"invalid boolean (expected true/false): {value}")


def _validate_all_rows(
    *,
    filename: str,
    rows: list[dict[str, str]],
    validators: list[Callable[[dict[str, str]], None]],
) -> None:
    for i, row in enumerate(rows, start=2):  # header is line 1
        try:
            for v in validators:
                v(row)
        except ValueError as e:
            raise ValueError(f"{filename}:{i}: {e}") from e


def validate_csv_dir(csv_dir: Path) -> None:
    if not csv_dir.exists():
        raise FileNotFoundError(csv_dir)

    # Basic presence + header checks
    rows_by_file: dict[str, list[dict[str, str]]] = {}
    for spec in CSV_SPECS:
        path = csv_dir / spec.filename
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            _require_columns(filename=spec.filename, fieldnames=reader.fieldnames, required=spec.required_columns)
            rows = list(reader)
        if not rows:
            raise ValueError(f"{spec.filename}: has no rows")
        rows_by_file[spec.filename] = rows

    # Cross-file reference checks
    sources = {row["source_id"] for row in rows_by_file["sources.csv"]}
    for filename in ("allowance_rules.csv", "payment_schedule.csv", "reform_history.csv"):
        for row in rows_by_file[filename]:
            if row["source_id"] not in sources:
                raise ValueError(f"{filename}: unknown source_id: {row['source_id']}")

    # Type + semantic validation
    def _v_allowance(row: dict[str, str]) -> None:
        _parse_date(row["effective_from"])
        if row["effective_to"]:
            _parse_date(row["effective_to"])
        age_min = _parse_int(row["age_min"])
        age_max = _parse_int(row["age_max"])
        if age_min > age_max:
            raise ValueError("age_min must be <= age_max")
        child_order_min = _parse_int(row["child_order_min"])
        child_order_max = _parse_int(row["child_order_max"]) if row["child_order_max"] else None
        if child_order_max is not None and child_order_min > child_order_max:
            raise ValueError("child_order_min must be <= child_order_max")
        amount = _parse_int(row["monthly_amount_yen"])
        if amount < 0:
            raise ValueError("monthly_amount_yen must be non-negative")
        _parse_bool(row["income_limit_applicable"])

    def _v_payment_schedule(row: dict[str, str]) -> None:
        _parse_date(row["effective_from"])
        if row["effective_to"]:
            _parse_date(row["effective_to"])
        payment_month = _parse_int(row["payment_month"])
        if not (1 <= payment_month <= 12):
            raise ValueError("payment_month must be 1..12")
        covered = [p.strip() for p in row["covered_months"].split(";") if p.strip()]
        if not covered:
            raise ValueError("covered_months must not be empty")
        covered_ints = [_parse_int(p) for p in covered]
        if any(m < 1 or m > 12 for m in covered_ints):
            raise ValueError("covered_months values must be 1..12")
        if len(set(covered_ints)) != len(covered_ints):
            raise ValueError("covered_months must not contain duplicates")

    def _v_reform_history(row: dict[str, str]) -> None:
        _parse_date(row["effective_date"])

    def _v_sources(row: dict[str, str]) -> None:
        _parse_date(row["accessed_date"])
        if not row["url"].startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")

    _validate_all_rows(filename="allowance_rules.csv", rows=rows_by_file["allowance_rules.csv"], validators=[_v_allowance])
    _validate_all_rows(
        filename="payment_schedule.csv",
        rows=rows_by_file["payment_schedule.csv"],
        validators=[_v_payment_schedule],
    )
    _validate_all_rows(
        filename="reform_history.csv",
        rows=rows_by_file["reform_history.csv"],
        validators=[_v_reform_history],
    )
    _validate_all_rows(filename="sources.csv", rows=rows_by_file["sources.csv"], validators=[_v_sources])

