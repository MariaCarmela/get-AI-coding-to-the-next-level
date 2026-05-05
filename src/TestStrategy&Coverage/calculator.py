from decimal import Decimal
from datetime import datetime
from typing import Optional

from exceptions import PriceCalculationError, DECIMAL_PRECISION
from validation import parse_base_price, validate_quantity
from coupons import apply_coupon
from time_rules import get_effective_purchase_datetime, is_time_sale

def calculate_price(
    base_price,
    coupon_code: Optional[str] = None,
    quantity: int = 1,
    user_status: str = "regular",
    purchased_at: Optional[datetime] = None
) -> Decimal:
    price = parse_base_price(base_price)
    quantity = validate_quantity(quantity)
    total = price * quantity
    total = apply_coupon(total, price, quantity, coupon_code)
    if user_status == "vip":
        total *= Decimal("0.85")
    elif user_status == "staff":
        total *= Decimal("0.50")
    dt = get_effective_purchase_datetime(purchased_at)
    if is_time_sale(dt):
        total *= Decimal("0.90")
    return total.quantize(DECIMAL_PRECISION)