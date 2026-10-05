import unittest
import os
import tempfile
from finance_tracker.database import Database
from finance_tracker.utils import format_rupiah, parse_amount, export_transactions_to_csv

class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_finance.db")
        self.db = Database(self.db_path)

    def tearDown(self):
        import gc
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_add_and_get_transaction(self):
        tx_id = self.db.add_transaction(
            tx_type="income",
            category="Gaji & Upah",
            amount=5000000.0,
            date="2026-09-01",
            description="Gaji Pertama"
        )
        self.assertIsInstance(tx_id, int)
        
        txs = self.db.get_transactions()
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0]["amount"], 5000000.0)
        self.assertEqual(txs[0]["category"], "Gaji & Upah")
        self.assertEqual(txs[0]["type"], "income")

    def test_summary_stats(self):
        self.db.add_transaction("income", "Gaji & Upah", 10000000.0, "2026-09-01", "Gaji")
        self.db.add_transaction("expense", "Makanan & Minuman", 250000.0, "2026-09-02", "Restoran")
        self.db.add_transaction("expense", "Transportasi", 150000.0, "2026-09-03", "Bensin")

        stats = self.db.get_summary_stats()
        self.assertEqual(stats["total_income"], 10000000.0)
        self.assertEqual(stats["total_expense"], 400000.0)
        self.assertEqual(stats["balance"], 9600000.0)
        self.assertEqual(stats["transaction_count"], 3)

    def test_category_breakdown(self):
        self.db.add_transaction("expense", "Makanan & Minuman", 200000.0, "2026-09-01", "Makan 1")
        self.db.add_transaction("expense", "Makanan & Minuman", 300000.0, "2026-09-02", "Makan 2")
        self.db.add_transaction("expense", "Transportasi", 100000.0, "2026-09-03", "Ojek")

        breakdown = self.db.get_expenses_by_category()
        self.assertEqual(len(breakdown), 2)
        self.assertEqual(breakdown[0], ("Makanan & Minuman", 500000.0))
        self.assertEqual(breakdown[1], ("Transportasi", 100000.0))

    def test_budget_management(self):
        self.assertEqual(self.db.get_budget("2026-09"), 0.0)
        self.db.set_budget("2026-09", 4500000.0)
        self.assertEqual(self.db.get_budget("2026-09"), 4500000.0)
        # Update budget
        self.db.set_budget("2026-09", 5000000.0)
        self.assertEqual(self.db.get_budget("2026-09"), 5000000.0)

    def test_utils_formatting(self):
        self.assertEqual(format_rupiah(1500000), "Rp 1.500.000")
        self.assertEqual(format_rupiah(0), "Rp 0")
        self.assertEqual(format_rupiah(-250000), "-Rp 250.000")

        self.assertEqual(parse_amount("1.500.000"), 1500000.0)
        self.assertEqual(parse_amount("Rp 250.000"), 250000.0)
        self.assertEqual(parse_amount("50000"), 50000.0)
        self.assertIsNone(parse_amount("bukan angka"))

    def test_export_csv(self):
        self.db.add_transaction("income", "Gaji & Upah", 5000000.0, "2026-09-01", "Gaji")
        txs = self.db.get_transactions()
        csv_file = os.path.join(self.temp_dir.name, "export.csv")
        success = export_transactions_to_csv(txs, csv_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_file))

if __name__ == "__main__":
    unittest.main()
