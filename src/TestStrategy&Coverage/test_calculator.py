from decimal import Decimal
from datetime import datetime
import pytest
from calculator import calculate_price
from exceptions import PriceCalculationError


class TestCalculator:

    def test_no_coupon(self):
        assert calculate_price(100.0) == Decimal("100.00")

    def test_save10_coupon(self):
        assert calculate_price(100.0, coupon_code="save10") == Decimal("90.00")

    def test_save20_coupon_above_threshold(self):
        assert calculate_price(200.0, coupon_code="save20") == Decimal("160.00")

    def test_save20_coupon_at_threshold(self):
        # total == 100, no discount applies
        assert calculate_price(100.0, coupon_code="save20") == Decimal("100.00")

    def test_bogo_coupon_qty3(self):
        # qty=3, price=100 → total=300, free=1 → 300-100=200
        assert calculate_price(100.0, coupon_code="bogo", quantity=3) == Decimal("200.00")

    def test_bogo_coupon_qty2(self):
        # qty=2, price=100 → total=200, free=1 → 200-100=100
        assert calculate_price(100.0, coupon_code="bogo", quantity=2) == Decimal("100.00")

    def test_unknown_coupon_ignored(self):
        assert calculate_price(100.0, coupon_code="INVALID") == Decimal("100.00")

    def test_negative_price_raises(self):
        with pytest.raises(PriceCalculationError):
            calculate_price(-10.0)

    def test_vip_status(self):
        assert calculate_price(100.0, user_status="vip") == Decimal("85.00")

    def test_staff_status(self):
        assert calculate_price(100.0, user_status="staff") == Decimal("50.00")

    def test_time_sale_active(self):
        # 18:00 → is_time_sale = True → 10% extra discount
        dt = datetime(2024, 1, 1, 18, 0, 0)
        assert calculate_price(100.0, purchased_at=dt) == Decimal("90.00")

    def test_time_sale_inactive(self):
        # 10:00 → is_time_sale = False → no extra discount
        dt = datetime(2024, 1, 1, 10, 0, 0)
        assert calculate_price(100.0, purchased_at=dt) == Decimal("100.00")

    def test_time_sale_boundary_23(self):
        dt = datetime(2024, 1, 1, 23, 0, 0)
        assert calculate_price(100.0, purchased_at=dt) == Decimal("90.00")

    def test_vip_with_time_sale(self):
        # vip 15% off + time sale 10% off → 100 * 0.85 * 0.90 = 76.50
        dt = datetime(2024, 1, 1, 20, 0, 0)
        assert calculate_price(100.0, user_status="vip", purchased_at=dt) == Decimal("76.50")