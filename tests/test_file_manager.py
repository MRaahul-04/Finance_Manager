import os
from expense import Expense
from file_manager import save_expenses, load_expenses

TEST_DIR = "tests"
TEST_FILE = os.path.join(TEST_DIR, "test_expenses.csv")


def test_save_and_load_expenses():
    # Ensure test directory exists
    os.makedirs(TEST_DIR, exist_ok=True)

    expenses = [
        Expense(120.5, "Food", "2024-12-01", "Groceries"),
        Expense(80, "Transport", "2024-12-02", "Auto"),
    ]

    # Save test data
    save_expenses(expenses, TEST_FILE)

    # Load test data
    loaded = load_expenses(TEST_FILE)

    assert len(loaded) == 2
    assert loaded[0].category == "Food"
    assert loaded[0].amount == 120.5
    assert loaded[1].category == "Transport"

    # Cleanup
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
