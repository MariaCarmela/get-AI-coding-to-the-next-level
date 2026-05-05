from decimal import Decimal, InvalidOperation
from exceptions import PriceCalculationError

def parse_base_price(base_price) -> Decimal:
    """
    Convert base_price to Decimal, raising PriceCalculationError on error.
    """
    try:
        price = Decimal(str(base_price))
    except (InvalidOperation, ValueError):
        raise PriceCalculationError("Invalid base price.")
    if price < 0:
        raise PriceCalculationError("Base price cannot be negative.")
    return price

def validate_quantity(quantity) -> int:
    """
    Ensure quantity is a positive integer, else raise PriceCalculationError.
    """
    if not isinstance(quantity, int) or quantity <= 0:
        raise PriceCalculationError("Quantity must be a positive integer.")
    return quantity

def validate_price(price):
    """Validate the price input."""
    if price < 0:
        raise PriceCalculationError("Price cannot be negative.")