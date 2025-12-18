from dataclasses import dataclass

@dataclass
class Expense:
    amount: float
    category: str
    date: str  # YYYY-MM-DD
    description: str

    def __post_init__(self):
        # ensure amount is float
        self.amount = float(self.amount)

    def to_row(self):
        """Return list representing CSV row"""
        return [self.date, self.category, f"{self.amount:.2f}", self.description]

    def __str__(self):
        return f"{self.date} | {self.category}: ₹{self.amount:.2f} - {self.description}"
