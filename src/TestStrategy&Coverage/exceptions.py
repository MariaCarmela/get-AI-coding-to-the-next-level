from decimal import Decimal

class PriceCalculationError(Exception):
    """Raised for errors in price calculation input or logic."""
    pass

# Shared constants (if needed in future)
DECIMAL_PRECISION = Decimal("0.01")
