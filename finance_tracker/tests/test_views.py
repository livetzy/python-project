import unittest
import os
import tempfile
import customtkinter as ctk
from finance_tracker.database import Database
from finance_tracker.views.dashboard_view import DashboardView
from finance_tracker.views.transactions_view import TransactionsView
from finance_tracker.views.budget_view import BudgetView
from finance_tracker.views.analytics_view import AnalyticsView

class TestUIViews(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_ui.db")
        self.db = Database(self.db_path)
        self.db.seed_demo_data()

        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        import gc
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_dashboard_view(self):
        dash = DashboardView(self.root, self.db, lambda x: None)
        dash.pack()
        self.root.update()
        dash.refresh()
        self.assertIsNotNone(dash.card_balance)
        self.assertIsNotNone(dash.donut_chart)
        dash.destroy()

    def test_transactions_view(self):
        tx_view = TransactionsView(self.root, self.db)
        tx_view.pack()
        self.root.update()
        tx_view.refresh()
        tx_view.destroy()

    def test_budget_view(self):
        b_view = BudgetView(self.root, self.db)
        b_view.pack()
        self.root.update()
        b_view.refresh()
        b_view.destroy()

    def test_analytics_view(self):
        a_view = AnalyticsView(self.root, self.db)
        a_view.pack()
        self.root.update()
        a_view.refresh()
        a_view.destroy()

if __name__ == "__main__":
    unittest.main()
