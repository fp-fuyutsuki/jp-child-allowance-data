"""Machine-readable Japanese child allowance data."""

from .allowance import (
    get_annual_amount,
    get_monthly_amount,
    get_payment_months,
    get_reform_history,
    load_rules,
    load_sources,
)

__all__ = [
    "get_monthly_amount",
    "get_annual_amount",
    "get_payment_months",
    "get_reform_history",
    "load_rules",
    "load_sources",
]

__version__ = "0.1.0"
