from __future__ import annotations

from datetime import date, datetime
from typing import Any

from .loaders import load_csv
from .models import AllowanceRule

DEFAULT_DATE = date.today()
DEFAULT_INCOME_STATUS = "no_income_limit"


def _parse_date(value: str | None) -> date | None:
    if value is None or value == "":
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "y"}


def _parse_int_or_none(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _coerce_date(value: date | str | None) -> date:
    if value is None:
        return DEFAULT_DATE
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_rules() -> list[AllowanceRule]:
    """Load child allowance amount rules as typed dataclass objects."""
    rows = load_csv("allowance_rules.csv")
    return [
        AllowanceRule(
            effective_from=_parse_date(row["effective_from"]),  # type: ignore[arg-type]
            effective_to=_parse_date(row["effective_to"]),
            age_min=int(row["age_min"]),
            age_max=int(row["age_max"]),
            age_label=row["age_label"],
            child_order_min=int(row["child_order_min"]),
            child_order_max=_parse_int_or_none(row["child_order_max"]),
            monthly_amount_yen=int(row["monthly_amount_yen"]),
            income_status=row["income_status"],
            income_limit_applicable=_parse_bool(row["income_limit_applicable"]),
            source_id=row["source_id"],
            notes=row["notes"],
        )
        for row in rows
    ]


def load_sources() -> list[dict[str, Any]]:
    """Load source metadata."""
    return load_csv("sources.csv")


def get_monthly_amount(
    age: int,
    child_order: int,
    date: date | str | None = None,
    income_status: str | None = None,
) -> int:
    """Return the monthly child allowance amount in yen.

    Parameters
    ----------
    age:
        Child age. This package intentionally uses a simple age field and does
        not implement fiscal-year birthday edge cases.
    child_order:
        Birth/order count used for the child allowance rule. Use 3 or greater
        for the third child and later.
    date:
        Rule date. Defaults to today.
    income_status:
        For current rules, omit this argument. For pre-2024-10 rules, pass
        one of: below_limit, above_limit_below_cap, above_cap.
    """
    if age < 0:
        raise ValueError("age must be non-negative")
    if child_order < 1:
        raise ValueError("child_order must be 1 or greater")

    on_date = _coerce_date(date)
    status = income_status
    if status is None:
        status = "no_income_limit" if on_date >= datetime.strptime("2024-10-01", "%Y-%m-%d").date() else "below_limit"

    matches = [
        rule for rule in load_rules()
        if rule.matches(age=age, child_order=child_order, on_date=on_date, income_status=status)
    ]
    if not matches:
        return 0
    # Prefer the most recent effective_from if multiple rules match.
    return sorted(matches, key=lambda r: r.effective_from, reverse=True)[0].monthly_amount_yen


def get_annual_amount(
    age: int,
    child_order: int,
    date: date | str | None = None,
    income_status: str | None = None,
) -> int:
    """Return the annualized amount as monthly_amount * 12."""
    return get_monthly_amount(age, child_order, date, income_status) * 12


def get_payment_months(year: int, date: date | str | None = None) -> list[int]:
    """Return scheduled payment months for the rule period containing date.

    This returns only payment months, not municipality-specific payment dates.
    """
    on_date = _coerce_date(date)
    rows = load_csv("payment_schedule.csv")
    months: list[int] = []
    for row in rows:
        start = _parse_date(row["effective_from"])
        end = _parse_date(row["effective_to"])
        if start is None:
            continue
        if start <= on_date and (end is None or on_date <= end):
            months.append(int(row["payment_month"]))
    return sorted(months)


def get_reform_history() -> list[dict[str, Any]]:
    """Load reform history entries."""
    return load_csv("reform_history.csv")
