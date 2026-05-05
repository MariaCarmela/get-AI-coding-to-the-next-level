from decimal import Decimal
from typing import Optional

def apply_coupon(total: Decimal, price: Decimal, quantity: int, coupon_code: Optional[str]) -> Decimal:
    """
    Apply coupon logic to the total, replicating the original rules.
    """
    if not coupon_code:
        return total
    normalized = coupon_code.strip().lower()
    if normalized == "save10":
        return total * Decimal("0.90")
    elif normalized == "save20":
        if total > 100:
            return total * Decimal("0.80")
        return total
    elif normalized == "bogo":
        free_items = quantity // 2
        return total - price * free_items
    # Unknown coupon: ignore
    return total
