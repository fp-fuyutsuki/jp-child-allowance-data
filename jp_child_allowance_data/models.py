from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class AllowanceRule:
    effective_from: date
    effective_to: date | None
    age_min: int
    age_max: int
    age_label: str
    child_order_min: int
    child_order_max: int | None
    monthly_amount_yen: int
    income_status: str
    income_limit_applicable: bool
    source_id: str
    notes: str

    def matches(self, *, age: int, child_order: int, on_date: date, income_status: str) -> bool:
        if not (self.effective_from <= on_date):
            return False
        if self.effective_to is not None and on_date > self.effective_to:
            return False
        if not (self.age_min <= age <= self.age_max):
            return False
        if child_order < self.child_order_min:
            return False
        if self.child_order_max is not None and child_order > self.child_order_max:
            return False
        return self.income_status == income_status
