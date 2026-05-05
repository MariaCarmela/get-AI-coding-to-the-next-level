from decimal import Decimal
from coupons import apply_coupon


def test_no_coupon():
    assert apply_coupon(Decimal("100.00"), Decimal("100.00"), 1, None) == Decimal("100.00")

def test_save10():
    assert apply_coupon(Decimal("100.00"), Decimal("100.00"), 1, "save10") == Decimal("90.00")

def test_save20_above_threshold():
    assert apply_coupon(Decimal("200.00"), Decimal("200.00"), 1, "save20") == Decimal("160.00")

def test_save20_at_threshold():
    assert apply_coupon(Decimal("100.00"), Decimal("100.00"), 1, "save20") == Decimal("100.00")

def test_bogo_qty2():
    assert apply_coupon(Decimal("200.00"), Decimal("100.00"), 2, "bogo") == Decimal("100.00")

def test_bogo_qty3():
    assert apply_coupon(Decimal("300.00"), Decimal("100.00"), 3, "bogo") == Decimal("200.00")

def test_unknown_coupon_ignored():
    assert apply_coupon(Decimal("100.00"), Decimal("100.00"), 1, "XYZ") == Decimal("100.00")

def test_coupon_case_insensitive():
    assert apply_coupon(Decimal("100.00"), Decimal("100.00"), 1, "SAVE10") == Decimal("90.00")