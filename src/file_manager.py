
import csv
import os
import shutil
from datetime import datetime
from src.expense import Expense

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "expenses.csv")
BACKUP_DIR = "../backups"

CSV_HEADER = ['Date', 'Category', 'Amount', 'Description']


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    # ensure file exists with header
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def load_expenses(filename=DATA_FILE):
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = os.path.join(BACKUP_DIR, f"expenses_backup_{timestamp}.csv")
    shutil.copy2(DATA_FILE, backup_name)
    return backup_name


def list_backups():
    ensure_dirs()
    files = sorted(os.listdir(BACKUP_DIR))
    return [os.path.join(BACKUP_DIR, f) for f in files if f.endswith('.csv')]


def restore_backup(backup_path):
    ensure_dirs()
    if not os.path.exists(backup_path):
        raise FileNotFoundError("Backup not found.")
    shutil.copy2(backup_path, DATA_FILE)