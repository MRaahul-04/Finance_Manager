"""
Utility and helper functions used across the application.

Includes:
- Input validation
- Date parsing
- Currency formatting
- Constants
"""

from datetime import datetime
from pathlib import Path

# Project root directory (Finance_Manager/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Health', 'Other']


def validate_amount(amount_str):
    """
    Validates numeric amount input.
    Returns (success, value/message).
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0."
        return True, float(amount)
    except ValueError:
        return False, "Invalid number format."


def validate_date(date_str):
    # validate date format, Accept YYYY-MM-DD
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return True, dt.strftime("%Y-%m-%d")
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."


def validate_category(cat_str):
    # Validates from listed categories
    cat = cat_str.strip()
    if not cat:
        return False, "Category cannot be empty."
    # allow custom categories but suggest existing
    return True, cat


def format_currency(amount):
    # Format a numeric amount as Indian currency (₹) with commas and 2 decimals.
    return f"₹{amount:,.2f}"


def truncate(text, n=60):
    # Shorten long text to a fixed length and append ellipsis if truncated.
    return text if len(text) <= n else text[:n - 3] + "..."
