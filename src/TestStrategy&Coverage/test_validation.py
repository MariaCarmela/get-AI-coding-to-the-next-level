import pytest
from validation import parse_base_price, validate_quantity
from exceptions import PriceCalculationError


class TestValidation:

    def test_parse_valid_price(self):
        from decimal import Decimal
        assert parse_base_price(100.0) == Decimal("100.00")

    def test_parse_invalid_string(self):
        with pytest.raises(PriceCalculationError):
            parse_base_price("abc")

    def test_parse_negative_price(self):
        with pytest.raises(PriceCalculationError):
            parse_base_price(-5.0)

    def test_validate_quantity_valid(self):
        assert validate_quantity(3) == 3

    def test_validate_quantity_zero(self):
        with pytest.raises(PriceCalculationError):
            validate_quantity(0)

    def test_validate_quantity_negative(self):
        with pytest.raises(PriceCalculationError):
            validate_quantity(-1)

    def test_validate_quantity_float(self):
        with pytest.raises(PriceCalculationError):
            validate_quantity(1.5)