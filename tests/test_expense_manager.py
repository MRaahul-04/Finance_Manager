# Budget calculations & alerts

import pytest
import os
import sys
from src.budget_manager import set_budget, load_budgets, delete_budget, budget_alerts
from src.expense import Expense

BUDGET_FILE = "data/budgets.json"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_expenses():
    return [
        Expense(400, "Food", "2025-12-01", "Groceries"),
        Expense(100, "Transport", "2025-12-01", "Cab ride"),
        Expense(600, "Food", "2025-12-02", "Dining out")
    ]


def test_set_and_load_budget():
    set_budget("Food", 1000)
    budgets = load_budgets()
    assert budgets["Food"] == 1000


def test_delete_budget():
    set_budget("TestCat", 500)
    delete_budget("TestCat")
    budgets = load_budgets()
    assert "TestCat" not in budgets


def test_budget_alerts(sample_expenses):
    set_budget("Food", 1000)
    set_budget("Transport", 200)
    alerts = budget_alerts(sample_expenses)
    # Should trigger Food alert (100%) and Transport alert (<100%)
    assert any("Food" in a for a in alerts)
