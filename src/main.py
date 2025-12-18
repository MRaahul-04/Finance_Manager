"""
Main entry point for the Personal Finance Manager application.

This file initializes the application and launches the
command-line menu loop.

Execution starts here when running:
    python -m src.main
"""

from src.menu import main_menu_loop
from src.file_manager import ensure_dirs


# Testing for commit and

def main():
    ensure_dirs()
    # Start the interactive CLI menu
    main_menu_loop()


if __name__ == "__main__":
    main()
