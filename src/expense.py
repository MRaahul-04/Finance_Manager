"""
-----------------------------------------------------------------------------
Defines the Expense data model using Object-Oriented Programming.
Represents a single financial transaction.
-----------------------------------------------------------------------------
"""

from dataclasses import dataclass


@dataclass
class Expense:
    """
        Expense entity representing one transaction.

        Attributes:
        - amount (float): Expense amount
        - category (str): Expense category
        - date (str): Transaction date (YYYY-MM-DD)
        - description (str): Optional description
    """
    amount: float
    category: str
    date: str  # YYYY-MM-DD
    description: str

    def __post_init__(self):
        # Store validated expense attributes
        # ensure amount is float
        self.amount = float(self.amount)

    def to_row(self):
        """Return list representing CSV row"""
        # Converts object into CSV-compatible row
        return [self.date, self.category, f"{self.amount:.2f}", self.description]

    def __str__(self):
        # User-friendly string representation for CLI display
        return f"{self.date} | {self.category}: ₹{self.amount:.2f} - {self.description}"
