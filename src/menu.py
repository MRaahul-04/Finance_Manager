"""
This module handles all command-line user interactions.
It acts as the presentation layer of the application.

Responsibilities:
- Display menus
- Collect user input
- Call business logic functions
- Control application flow
"""

import os
from time import sleep
from src.file_manager import load_expenses, append_expense, save_expenses, backup_data, list_backups, restore_backup
from src.expense import Expense
from src.utils import validate_amount, validate_date, validate_category, CATEGORIES, format_currency, truncate
from src.reports import total_and_average, category_summary, monthly_summary, generate_monthly_report
from src.budget_manager import set_budget, delete_budget, load_budgets, budget_alerts
from src.file_manager import load_expenses
from src.budget_manager import budget_alerts
from src.reports import generate_category_chart, generate_monthly_spending_chart, generate_budget_vs_actual_chart


def clear():
    """
    Safely clear the terminal screen across:
    - Windows
    - macOS
    - Linux
    - PyCharm / VS Code
    - Docker
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        # Unix-based systems (macOS/Linux)
        if os.getenv("TERM"):
            os.system('clear')
        else:
            # Fallback for environments without TERM (PyCharm, Docker)
            print("\n" * 2)


def pause():
    input("\nPress Enter to continue...")


def add_new_expense():
    # Adding new expenses to the tracker
    clear()
    print("ADD NEW EXPENSE:")
    while True:
        amt_in = input("Enter amount: ").strip()
        ok, val = validate_amount(amt_in)
        if not ok:
            print("Error:", val)
            continue
        amount = val
        break
    print("Suggested categories:", ", ".join(CATEGORIES))
    while True:
        cat_in = input("Enter category: ").strip()
        ok, val = validate_category(cat_in)
        if not ok:
            print("Error:", val);
            continue
        category = val
        break
    while True:
        date_in = input("Enter date (YYYY-MM-DD): ").strip()
        ok, val = validate_date(date_in)
        if not ok:
            print("Error:", val);
            continue
        date = val
        break
    desc = input("Enter description: ").strip()
    exp = Expense(amount=amount, category=category, date=date, description=desc)
    append_expense(exp)
    print("\n✅ Expense added successfully!")

    # 🔔 CHECK BUDGET ALERTS
    alerts = budget_alerts(load_expenses())
    if alerts:
        print("\n⚠️ BUDGET ALERTS:")
        for a in alerts:
            print(a)

    pause()


def view_all_expenses():
    # View all saved expenses
    clear()
    exps = load_expenses()
    print("ALL EXPENSES:")
    if not exps:
        print("No expenses recorded.")
    else:
        for idx, e in enumerate(exps, start=1):
            print(f"[{idx}] {e}")
    pause()


def view_category_summary():
    # View summary of all category wise expenses
    clear()
    exps = load_expenses()
    if not exps:
        print("No expenses.")
        pause();
        return
    summary = category_summary(exps)
    total, avg = total_and_average(exps)
    print("CATEGORY-WISE SUMMARY:")
    for cat, amt in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"{cat:15} {format_currency(amt)}")
    print("\nTotal:", format_currency(total))
    print("Average per record:", format_currency(avg))

    from budget_manager import budget_alerts
    alerts = budget_alerts(exps)
    if alerts:
        print("\n⚠️ BUDGET ALERTS:")
        for a in alerts:
            print(a)

    pause()


def generate_month_report():
    # Generate report for the specific month
    clear()
    exps = load_expenses()
    if not exps:
        print("No expenses.")
        pause();
        return
    month = input("Enter month (YYYY-MM) e.g. 2024-01: ").strip()
    try:
        path = generate_monthly_report(exps, month)
        print(f"Monthly report saved to: {path}")

    except Exception as e:
        print("Error:", e)
    pause()


def search_expenses():
    # Search any required expense using Date, Cat, Amount, Keyword.
    clear()
    exps = load_expenses()
    if not exps:
        print("No expenses.")
        pause();
        return
    print("SEARCH BY: 1) Date  2) Category  3) Amount range  4) Keyword")
    choice = input("Choice (1-4): ").strip()
    results = []
    if choice == '1':
        d = input("Enter date (YYYY-MM-DD): ").strip()
        results = [e for e in exps if e.date == d]
    elif choice == '2':
        c = input("Enter category: ").strip()
        results = [e for e in exps if e.category.lower() == c.lower()]
    elif choice == '3':
        mn = input("Min amount: ").strip();
        mx = input("Max amount: ").strip()
        try:
            mn = float(mn);
            mx = float(mx)
            results = [e for e in exps if mn <= e.amount <= mx]
        except ValueError:
            print("Invalid numbers.")
            pause();
            return
    else:
        kw = input("Enter keyword: ").strip().lower()
        results = [e for e in exps if kw in e.description.lower() or kw in e.category.lower()]
    print(f"\nFound {len(results)} result(s):")
    for r in results:
        print(r)
    pause()


def backup_menu():
    # Shows the backup menu
    clear()
    print("BACKUP & RESTORE")
    print("1. Create backup")
    print("2. List backups")
    print("3. Restore from backup")
    ch = input("Choice (1-3): ").strip()
    if ch == '1':
        path = backup_data()
        print("Backup created:", path)
    elif ch == '2':
        for p in list_backups():
            print(p)
    elif ch == '3':
        backups = list_backups()
        if not backups:
            print("No backups available.")
            pause();
            return
        for idx, p in enumerate(backups, start=1):
            print(f"{idx}. {p}")
        sel = input("Choose backup number to restore: ").strip()
        try:
            sel_i = int(sel) - 1
            if sel_i < 0 or sel_i >= len(backups):
                print("Invalid selection.")
            else:
                restore_backup(backups[sel_i])
                print("Restored backup to data file.")
        except ValueError:
            print("Invalid input.")
    pause()


def generate_charts_menu():
    clear()
    exps = load_expenses()

    if not exps:
        print("No expenses available for chart generation.")
        pause()
        return

    print("GENERATE CHARTS")
    print("1. Category-wise Spending Chart")
    print("2. Monthly Spending Chart")
    print("3. Budget vs Actual Chart")
    print("4. Back")

    choice = input("Choice (1-4): ").strip()

    if choice == '1': # Generates category wise chart summary
        path = generate_category_chart(exps)
        if path:
            print(f"\n📊 Chart generated successfully!")
            print(f"Saved at: {path}")
        else:
            print("Failed to generate chart.")
        pause()

    elif choice == '2':  # Monthly chart handling
        path = generate_monthly_spending_chart(exps)
        if path:
            print(f"\n📊 Monthly chart generated successfully!")
            print(f"Saved at: {path}")
        else:
            print("Failed to generate chart.")
        pause()

    elif choice == '3':  # Budget vs Actual chart distribution
        path = generate_budget_vs_actual_chart(exps)
        if path:
            print(f"\n📊 Budget vs Actual chart generated successfully!\nSaved at: {path}")
        pause()


def main_menu_loop():
    """
    Infinite loop displaying menu until user exits.

    Pattern:
    - Display options
    - Route to feature functions
    - Return control safely
    """
    while True:
        clear()
        print("=" * 42)
        print("     PERSONAL FINANCE MANAGER")
        print("=" * 42)
        print("\nMAIN MENU:")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. View Category-wise Summary")
        print("6. Budget Management")
        print("7. Generate Monthly Report")
        print("8. Search Expenses")
        print("9. Backup / Restore Data")
        print("10. Generate Spending Charts")
        print("0. Exit")
        choice = input("\nEnter your choice (1-10): ").strip()
        if choice == '1':
            add_new_expense()
        elif choice == '2':
            view_all_expenses()
        elif choice == '3':
            edit_expense()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            view_category_summary()
        elif choice == '6':
            budget_menu()
        elif choice == '7':
            generate_month_report()
        elif choice == '8':
            search_expenses()
        elif choice == '9':
            backup_menu()
        elif choice == '10':
            generate_charts_menu()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            sleep(1)


def edit_expense():
    # Edit any existing expense based on the Expense ID
    clear()
    exps = load_expenses()
    if not exps:
        print("No expenses to edit.")
        pause()
        return

    for idx, e in enumerate(exps, start=1):
        print(f"[{idx}] {e}")

    try:
        choice = int(input("\nEnter Expense ID to edit: "))
        if choice < 1 or choice > len(exps):
            raise ValueError
    except ValueError:
        print("Invalid Expense ID.")
        pause()
        return

    exp = exps[choice - 1]
    print("\nPress Enter to keep existing value.")

    new_amt = input(f"Amount ({exp.amount}): ").strip()
    if new_amt:
        ok, val = validate_amount(new_amt)
        if ok:
            exp.amount = val

    new_cat = input(f"Category ({exp.category}): ").strip()
    if new_cat:
        exp.category = new_cat

    new_date = input(f"Date ({exp.date}): ").strip()
    if new_date:
        ok, val = validate_date(new_date)
        if ok:
            exp.date = val

    new_desc = input(f"Description ({exp.description}): ").strip()
    if new_desc:
        exp.description = new_desc

    save_expenses(exps)
    print("\n✏️ Expense updated successfully!")
    pause()


def delete_expense():
    # Delete any existing expense based on Expense ID
    clear()
    exps = load_expenses()
    if not exps:
        print("No expenses to delete.")
        pause()
        return

    for idx, e in enumerate(exps, start=1):
        print(f"[{idx}] {e}")

    try:
        choice = int(input("\nEnter Expense ID to delete: "))
        if choice < 1 or choice > len(exps):
            raise ValueError
    except ValueError:
        print("Invalid Expense ID.")
        pause()
        return

    confirm = input("Are you sure you want to delete this expense? (y/n): ").lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        pause()
        return

    deleted = exps.pop(choice - 1)
    save_expenses(exps)

    print("\n🗑️ Deleted:")
    print(deleted)
    pause()


def budget_menu():
    # Shows Budget menu for modification or deletion
    clear()
    budgets = load_budgets()

    print("BUDGET MANAGEMENT")
    print("------------------")
    if budgets:
        for cat, amt in budgets.items():
            print(f"{cat:15} ₹{amt:.2f}")
    else:
        print("No budgets set.")

    print("\n1. Set / Update Budget")
    print("2. Delete Budget")
    print("3. Back")

    choice = input("Choice (1-3): ").strip()

    if choice == '1':
        cat = input("Enter category: ").strip()
        amt = input("Enter monthly budget amount: ").strip()
        try:
            set_budget(cat, float(amt))
            print("✅ Budget saved.")
        except ValueError:
            print("Invalid amount.")
        pause()

    elif choice == '2':
        cat = input("Enter category to delete: ").strip()
        delete_budget(cat)
        print("🗑️ Budget removed (if existed).")
        pause()