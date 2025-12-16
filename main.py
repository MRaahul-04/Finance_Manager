# main.py
from menu import main_menu_loop
from file_manager import ensure_dirs


# Testing for commit and

def main():
    ensure_dirs()
    main_menu_loop()


if __name__ == "__main__":
    main()
