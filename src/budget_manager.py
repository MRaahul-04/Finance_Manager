"""
Manages monthly budget limits per category.

Uses a dictionary-based storage model:
    { "Food": 5000, "Transport": 2000 }
"""

import json
import os
from collections import defaultdict
from src.utils import PROJECT_ROOT

BUDGET_FILE = PROJECT_ROOT / "data" / "budgets.json"


def load_budgets():
    """
    Loads budget configuration from JSON.
    Returns dictionary {category: budget_amount}.
    """
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_budgets(budgets):
    """
    Saves a budget for a category.
    """
    os.makedirs("../data", exist_ok=True)
    with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
        json.dump(budgets, f, indent=4)


def set_budget(category, amount):
    """
    Sets or updates a budget for a category.
    """
    budgets = load_budgets()
    budgets[category] = float(amount)
    save_budgets(budgets)


def delete_budget(category):
    """
    Removes specific budget for a category.
    """
    budgets = load_budgets()
    if category in budgets:
        del budgets[category]
        save_budgets(budgets)


def calculate_category_spend(expenses):
    """
    Calculates and shows the category wise spends
    """
    totals = defaultdict(float)
    for e in expenses:
        totals[e.category] += e.amount
    return dict(totals)


def budget_alerts(expenses):
    """
    Compares actual spending vs budget.

    Algorithm:
    - Aggregate expenses by category
    - Compare totals against budget
    - Generate warnings
    """
    budgets = load_budgets()
    spend = calculate_category_spend(expenses)

    alerts = []
    for cat, limit in budgets.items():
        used = spend.get(cat, 0)
        pct = (used / limit * 100) if limit > 0 else 0

        if pct >= 100:
            alerts.append(f"🔴 {cat}: Budget exceeded ({used:.2f}/{limit:.2f})")
        elif pct >= 80:
            alerts.append(f"🟡 {cat}: {pct:.0f}% of budget used ({used:.2f}/{limit:.2f})")

    return alerts
