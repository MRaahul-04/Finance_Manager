# reports.py
from collections import defaultdict
from datetime import datetime
from utils import format_currency
from typing import List
from expense import Expense
import matplotlib.pyplot as plt
import csv
import os
import platform
import subprocess
from src.utils import PROJECT_ROOT

REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = PROJECT_ROOT / "charts"

REPORTS_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)


def total_and_average(expenses: List[Expense]):
    total = sum(e.amount for e in expenses)
    average = (total / len(expenses)) if expenses else 0.0
    return total, average


def category_summary(expenses: List[Expense]):
    summary = defaultdict(float)
    for e in expenses:
        summary[e.category] += e.amount
    return dict(summary)


def monthly_summary(expenses: List[Expense]):
    months = defaultdict(float)  # 'YYYY-MM' -> amount
    for e in expenses:
        try:
            m = datetime.strptime(e.date, "%Y-%m-%d").strftime("%Y-%m")
        except Exception:
            continue
        months[m] += e.amount
    return dict(months)


def generate_monthly_report(expenses: List[Expense], month_str: str, out_dir="reports"):
    """
    month_str: 'YYYY-MM' e.g. '2024-01'
    """
    os.makedirs(out_dir, exist_ok=True)
    rows = [e for e in expenses if e.date.startswith(month_str)]
    total, avg = total_and_average(rows)
    file_path = REPORTS_DIR / f"report_{month_str}.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        for r in rows:
            writer.writerow([r.date, r.category, f"{r.amount:.2f}", r.description])
        writer.writerow([])
        writer.writerow(["Total", f"{total:.2f}"])
        writer.writerow(["Average", f"{avg:.2f}"])
    return file_path


def generate_category_chart(expenses, out_dir="reports"):
    """
    Generates a pie chart for category-wise spending
    Saves it as PNG in reports/ folder
    """
    if not expenses:
        return None

    from collections import defaultdict
    import os

    totals = defaultdict(float)
    for e in expenses:
        totals[e.category] += e.amount

    categories = list(totals.keys())
    amounts = list(totals.values())

    os.makedirs(out_dir, exist_ok=True)
    file_path = CHARTS_DIR / "category_spending.png"

    plt.figure()
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Category-wise Spending")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    open_image(file_path)

    return file_path


def generate_monthly_spending_chart(expenses, out_dir="reports"):
    """
    Generates a bar chart for monthly spending.
    Saves PNG in reports/ folder.
    """
    if not expenses:
        return None

    totals = defaultdict(float)

    for e in expenses:
        # Extract month-year: YYYY-MM
        month = datetime.strptime(e.date, "%Y-%m-%d").strftime("%Y-%m")
        totals[month] += e.amount

    # Sort months chronologically
    months = sorted(totals.keys())
    amounts = [totals[m] for m in months]

    os.makedirs(out_dir, exist_ok=True)
    file_path = CHARTS_DIR / "monthly_spending.png"

    plt.figure(figsize=(8,5))
    plt.bar(months, amounts, color='skyblue')
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    open_image(file_path)

    return file_path


def generate_budget_vs_actual_chart(expenses, out_dir="reports"):
    """
    Generates a bar chart comparing budget vs actual spend per category.
    """
    from budget_manager import load_budgets

    if not expenses:
        return None

    budgets = load_budgets()
    actuals = defaultdict(float)

    for e in expenses:
        actuals[e.category] += e.amount

    categories = sorted(set(list(budgets.keys()) + list(actuals.keys())))
    budget_values = [budgets.get(cat, 0) for cat in categories]
    actual_values = [actuals.get(cat, 0) for cat in categories]

    os.makedirs(out_dir, exist_ok=True)
    file_path = CHARTS_DIR / "budget_vs_actual.png"

    import numpy as np
    x = np.arange(len(categories))
    width = 0.35

    plt.figure(figsize=(10,5))
    plt.bar(x - width/2, budget_values, width, label='Budget', color='green', alpha=0.7)
    plt.bar(x + width/2, actual_values, width, label='Actual', color='red', alpha=0.7)
    plt.xticks(x, categories, rotation=45)
    plt.ylabel("Amount (₹)")
    plt.title("Budget vs Actual Spending per Category")
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    open_image(file_path)

    return file_path


def open_image(path):
    """Open image automatically based on OS"""
    if not os.path.exists(path):
        print("❌ File not found:", path)
        return

    if platform.system() == "Darwin":       # macOS
        subprocess.call(["open", path])
    elif platform.system() == "Windows":    # Windows
        os.startfile(path)
    else:                                   # Linux
        subprocess.call(["xdg-open", path])
