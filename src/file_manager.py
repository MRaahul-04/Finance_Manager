"""
Handles all file input/output operations.
Acts as the persistence layer of the application.

Responsibilities:
- Load expenses from CSV
- Save expenses to CSV
- Append records
- Create backups
- Restore backups
"""

import csv
import os
import shutil
from datetime import datetime
from src.expense import Expense
from src.utils import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"
BACKUP_DIR = PROJECT_ROOT / "backups"
DATA_FILE = DATA_DIR / "expenses.csv"

CSV_HEADER = ['Date', 'Category', 'Amount', 'Description']


def ensure_dirs():
    """
        Ensures required directories exist before file operations.
        Prevents runtime FileNotFound errors.
    """
    DATA_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    # ensure file exists with header
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def load_expenses(filename=DATA_FILE):
    """
        Loads expenses from CSV file into Expense objects.

        Algorithm:
        - Read CSV rows
        - Validate content
        - Convert rows → Expense objects
    """
    ensure_dirs()
    expenses = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or all((row.get(h, "").strip() == "") for h in CSV_HEADER):
                continue
            try:
                exp = Expense(
                    amount=float(row['Amount']),
                    category=row['Category'],
                    date=row['Date'],
                    description=row['Description']
                )
                expenses.append(exp)
            except Exception:
                # skip malformed rows
                continue
    return expenses


def save_expenses(expenses, filename=DATA_FILE):
    """
        Saves a list of Expense objects into CSV.
        Overwrites existing data safely.
    """
    ensure_dirs()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        for e in expenses:
            writer.writerow(e.to_row())


def append_expense(expense: Expense, filename=DATA_FILE):
    ensure_dirs()
    # append single expense
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(expense.to_row())


def backup_data():
    ensure_dirs()
    # Backup all saved expenses
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = os.path.join(BACKUP_DIR, f"expenses_backup_{timestamp}.csv")
    shutil.copy2(DATA_FILE, backup_name)
    return backup_name


def list_backups():
    ensure_dirs()
    # list out all saved backups
    files = sorted(os.listdir(BACKUP_DIR))
    return [os.path.join(BACKUP_DIR, f) for f in files if f.endswith('.csv')]


def restore_backup(backup_path):
    ensure_dirs()
    # Restored saved backup to the existing data
    if not os.path.exists(backup_path):
        raise FileNotFoundError("Backup not found.")
    shutil.copy2(backup_path, DATA_FILE)