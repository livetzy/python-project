
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from finance_tracker.app import run_app

if __name__ == "__main__":
    print("Memulai aplikasi Personal Finance Tracker...")
    run_app()
