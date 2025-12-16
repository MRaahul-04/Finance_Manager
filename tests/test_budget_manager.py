import json
import os
from expense import Expense
from budget_manager import (
    set_budget,
    load_budgets,
    calculate_category_spend,
    budget_alerts
)

BUDGET_FILE = "data/budgets.json"


def backup_budgets():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            return f.read()
    return None


def restore_budgets(data):
    if data is not None:
        with open(BUDGET_FILE, "w") as f:
            f.write(data)


def test_budget_functions():
    # Backup real budgets
    backup = backup_budgets()

    # Set budgets
    set_budget("Food", 1000)
    set_budget("Transport", 300)

    budgets = load_budgets()
    assert budgets["Food"] == 1000
    assert budgets["Transport"] == 300

    expenses = [
        Expense(400, "Food", "2024-12-01", "Groceries"),
        Expense(700, "Food", "2024-12-02", "Dining"),
        Expense(100, "Transport", "2024-12-03", "Bus"),
    ]

    totals = calculate_category_spend(expenses)
    assert totals["Food"] == 1100
    assert totals["Transport"] == 100

    alerts = budget_alerts(expenses)
    assert any("Food" in alert for alert in alerts)

    # Restore real budgets
    restore_budgets(backup)
