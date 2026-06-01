from jp_child_allowance_data import (
    get_annual_amount,
    get_monthly_amount,
    get_payment_months,
    get_reform_history,
    load_rules,
    load_sources,
)


def test_current_first_child_under_three():
    assert get_monthly_amount(age=2, child_order=1, date="2026-06-01") == 15000


def test_current_third_child_under_three():
    assert get_monthly_amount(age=2, child_order=3, date="2026-06-01") == 30000


def test_current_first_child_age_three_to_eighteen():
    assert get_monthly_amount(age=10, child_order=1, date="2026-06-01") == 10000


def test_current_third_child_age_three_to_eighteen():
    assert get_monthly_amount(age=18, child_order=3, date="2026-06-01") == 30000


def test_current_over_target_age_returns_zero():
    assert get_monthly_amount(age=19, child_order=1, date="2026-06-01") == 0


def test_pre_reform_below_limit_elementary_third_child():
    assert get_monthly_amount(age=8, child_order=3, date="2024-09-01", income_status="below_limit") == 15000


def test_pre_reform_special_benefit():
    assert get_monthly_amount(age=8, child_order=1, date="2024-09-01", income_status="above_limit_below_cap") == 5000


def test_pre_reform_above_cap():
    assert get_monthly_amount(age=8, child_order=1, date="2024-09-01", income_status="above_cap") == 0


def test_annual_amount():
    assert get_annual_amount(age=2, child_order=1, date="2026-06-01") == 180000


def test_payment_months_current():
    assert get_payment_months(2026, date="2026-06-01") == [2, 4, 6, 8, 10, 12]


def test_payment_months_pre_reform():
    assert get_payment_months(2024, date="2024-09-01") == [2, 6, 10]


def test_metadata_loads():
    assert load_rules()
    assert load_sources()
    assert get_reform_history()
