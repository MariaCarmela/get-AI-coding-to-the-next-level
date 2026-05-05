import sqlite3
from typing import Any


class InterestCalculator:
    """Calculates debit interest on bank accounts and persists accounting movements.

    Each instance uses an isolated in-memory SQLite database for movement storage.
    """

    def __init__(self) -> None:
        """Initialize the calculator with an isolated in-memory SQLite connection."""
        self._connection: sqlite3.Connection = self._create_connection()
        self._create_table()

    def _create_connection(self) -> sqlite3.Connection:
        """Create and return an in-memory SQLite connection."""
        return sqlite3.connect(":memory:")

    def _create_table(self) -> None:
        """Create the movements table if it does not exist."""
        cursor: sqlite3.Cursor = self._connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                type TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def calculate_interest(
        self, balance: float, annual_rate: float, days: int
    ) -> dict[str, float]:
        """Calculate debit interest on a given balance.

        Formula: interest = (balance * annual_rate * days) / 365

        Args:
            balance: The account principal balance (must be >= 0).
            annual_rate: The annual interest rate as decimal (0.0 to 1.0 inclusive).
            days: The number of days for interest accrual (must be >= 0).

        Returns:
            A dictionary with 'interest' and 'final_balance' rounded to 2 decimals.

        Raises:
            ValueError: If balance is negative, annual_rate > 1.0 or < 0, or days < 0.
        """
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        if annual_rate > 1.0:
            raise ValueError("Annual rate cannot exceed 1.0")
        if annual_rate < 0:
            raise ValueError("Annual rate cannot be negative")
        if days < 0:
            raise ValueError("Days cannot be negative")

        if days == 0:
            return {"interest": 0.0, "final_balance": round(balance, 2)}

        interest: float = round((balance * annual_rate * days) / 365, 2)
        final_balance: float = round(balance + interest, 2)

        return {"interest": interest, "final_balance": final_balance}

    def save_movement(self, amount: float, type_: str) -> int:
        """Persist an accounting movement to the in-memory database.

        Args:
            amount: The monetary amount of the movement.
            type_: The movement type ('C' for credit, 'D' for debit).

        Returns:
            The progressive integer ID assigned to the movement.

        Raises:
            ValueError: If type_ is not 'C' or 'D'.
        """
        if type_ not in ("C", "D"):
            raise ValueError("Movement type must be 'C' or 'D'")

        cursor: sqlite3.Cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO movements (amount, type) VALUES (?, ?)",
            (amount, type_),
        )
        self._connection.commit()
        return cursor.lastrowid  # type: ignore[return-value]

    def get_movements(self) -> list[dict[str, Any]]:
        """Retrieve all stored movements.

        Returns:
            A list of dictionaries with keys 'id', 'amount', and 'type'.
        """
        cursor: sqlite3.Cursor = self._connection.cursor()
        cursor.execute("SELECT id, amount, type FROM movements ORDER BY id")
        rows: list[tuple[Any, ...]] = cursor.fetchall()
        return [{"id": row[0], "amount": row[1], "type": row[2]} for row in rows]
