import sys
import os
import pytest

# Aggiungi la cartella src al percorso di ricerca
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/LegacyLogicMigration/')))
from solution import InterestCalculator

class TestInterestCalculator:
    """Test suite for `InterestCalculator`."""

    @pytest.fixture
    def calculator(self):
        """Fixture that creates a new instance for each test."""
        return InterestCalculator()

    # =================================================================
    # BASE CALCULATION TESTS
    # =================================================================

    def test_calculation_standard_90_days(self, calculator):
        """Test standard interest calculation for 90 days."""
        result = calculator.calculate_interest(balance=15000.00, annual_rate=0.0350, days=90)
        assert result["interest"] == pytest.approx(129.45, abs=0.01)
        assert result["final_balance"] == pytest.approx(15129.45, abs=0.01)

    def test_calculation_zero_days(self, calculator):
        """Test interest calculation for zero days."""
        result = calculator.calculate_interest(balance=5000.00, annual_rate=0.05, days=0)
        assert result["interest"] == 0.0
        assert result["final_balance"] == 5000.00

    # Add more tests as needed...

    # =================================================================
    # ERROR HANDLING TESTS
    # =================================================================

    def test_error_negative_balance(self, calculator):
        """Test handling of negative balance."""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_interest(balance=-100.00, annual_rate=0.05, days=30)
        assert "balance" in str(exc_info.value).lower()

    def test_error_rate_greater_than_100(self, calculator):
        """Test handling of annual rate greater than 1.0."""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_interest(balance=1000.00, annual_rate=1.5, days=30)
        assert "rate" in str(exc_info.value).lower()

    # =================================================================
    # PERSISTENCE TESTS (SQLite)
    # =================================================================

    def test_save_movement_returns_id(self, calculator):
        """Test that save_movement returns an integer ID."""
        movement_id = calculator.save_movement(129.45, 'C')
        assert isinstance(movement_id, int)

    def test_save_and_retrieve_movement(self, calculator):
        """Test saving and retrieving a movement."""
        calculator.save_movement(129.45, 'C')
        movements = calculator.get_movements()
        assert len(movements) == 1
        assert movements[0]['amount'] == pytest.approx(129.45, abs=0.01)

    # Add more tests as needed...

if __name__ == "__main__":
    pytest.main()