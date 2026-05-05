from datetime import datetime
from time_rules import get_effective_purchase_datetime, is_time_sale


def test_is_time_sale_at_18():
    assert is_time_sale(datetime(2024, 1, 1, 18, 0)) is True

def test_is_time_sale_at_23():
    assert is_time_sale(datetime(2024, 1, 1, 23, 0)) is True

def test_is_time_sale_at_17():
    assert is_time_sale(datetime(2024, 1, 1, 17, 0)) is False

def test_is_time_sale_at_midnight():
    assert is_time_sale(datetime(2024, 1, 1, 0, 0)) is False

def test_get_effective_datetime_provided():
    dt = datetime(2024, 6, 15, 10, 0)
    assert get_effective_purchase_datetime(dt) == dt

def test_get_effective_datetime_none():
    result = get_effective_purchase_datetime(None)
    assert isinstance(result, datetime)