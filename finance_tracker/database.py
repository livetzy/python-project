import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "finance.db")

DEFAULT_CATEGORIES = [

    ("Gaji & Upah", "income", "💼"),
    ("Bisnis & Freelance", "income", "🚀"),
    ("Investasi", "income", "📈"),
    ("Hadiah & Bonus", "income", "🎁"),
    ("Lainnya (Pemasukan)", "income", "💰"),
    ("Makanan & Minuman", "expense", "🍔"),
    ("Transportasi", "expense", "🚗"),
    ("Tagihan & Utilitas", "expense", "💡"),
    ("Belanja Kebutuhan", "expense", "🛒"),
    ("Hiburan & Hobi", "expense", "🎮"),
    ("Kesehatan & Obat", "expense", "💊"),
    ("Pendidikan", "expense", "📚"),
    ("Donasi / Sosial", "expense", "🤝"),
    ("Lainnya (Pengeluaran)", "expense", "💸"),
]

class Database:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Inisialisasi tabel database SQLite jika belum ada."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                    icon TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT UNIQUE NOT NULL, -- Format 'YYYY-MM'
                    monthly_limit REAL NOT NULL
                )
            """)

            cursor.execute("SELECT COUNT(*) as count FROM categories")
            if cursor.fetchone()["count"] == 0:
                cursor.executemany(
                    "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?)",
                    DEFAULT_CATEGORIES
                )

            conn.commit()

    def get_categories(self, category_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category_type:
                cursor.execute("SELECT * FROM categories WHERE type = ? ORDER BY name ASC", (category_type,))
            else:
                cursor.execute("SELECT * FROM categories ORDER BY type DESC, name ASC")
            return [dict(row) for row in cursor.fetchall()]

    def add_category(self, name: str, category_type: str, icon: str = "🏷️") -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?)",
                    (name.strip(), category_type, icon)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def add_transaction(
        self,
        tx_type: str,
        category: str,
        amount: float,
        date: str,
        description: str = ""
    ) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (type, category, amount, date, description)
                VALUES (?, ?, ?, ?, ?)
            """, (tx_type, category, float(amount), date, description.strip()))
            conn.commit()
            return cursor.lastrowid

    def update_transaction(
        self,
        tx_id: int,
        tx_type: str,
        category: str,
        amount: float,
        date: str,
        description: str = ""
    ) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET type = ?, category = ?, amount = ?, date = ?, description = ?
                WHERE id = ?
            """, (tx_type, category, float(amount), date, description.strip(), tx_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_transaction(self, tx_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_transaction_by_id(self, tx_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_transactions(
        self,
        limit: Optional[int] = None,
        filter_type: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM transactions WHERE 1=1"
        params: List[Any] = []

        if filter_type and filter_type.lower() in ("income", "expense"):
            query += " AND type = ?"
            params.append(filter_type.lower())

        if category and category != "Semua Kategori":
            query += " AND category = ?"
            params.append(category)

        if search:
            query += " AND (description LIKE ? OR category LIKE ?)"
            term = f"%{search.strip()}%"
            params.extend([term, term])

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date DESC, id DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_summary_stats(self, month: Optional[str] = None) -> Dict[str, float]:
        """
        Menghitung total pemasukan, total pengeluaran, dan saldo.
        Jika month disediakan ('YYYY-MM'), hitung hanya untuk bulan tersebut.
        """
        params_income: List[Any] = ["income"]
        params_expense: List[Any] = ["expense"]
        month_filter = ""

        if month:
            month_filter = " AND date LIKE ?"
            params_income.append(f"{month}%")
            params_expense.append(f"{month}%")

        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = ?{month_filter}", params_income)
            total_income = cursor.fetchone()[0]

            cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = ?{month_filter}", params_expense)
            total_expense = cursor.fetchone()[0]

            balance = total_income - total_expense

            count_query = "SELECT COUNT(*) FROM transactions WHERE 1=1"
            count_params = []
            if month:
                count_query += " AND date LIKE ?"
                count_params.append(f"{month}%")

            cursor.execute(count_query, count_params)
            count = cursor.fetchone()[0]

            return {
                "total_income": float(total_income),
                "total_expense": float(total_expense),
                "balance": float(balance),
                "transaction_count": int(count)
            }

    def get_expenses_by_category(self, month: Optional[str] = None) -> List[Tuple[str, float]]:
        """Mengambil total pengeluaran dikelompokkan berdasarkan kategori."""
        params: List[Any] = ["expense"]
        query = "SELECT category, SUM(amount) as total FROM transactions WHERE type = ?"
        if month:
            query += " AND date LIKE ?"
            params.append(f"{month}%")
        query += " GROUP BY category ORDER BY total DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [(row["category"], float(row["total"])) for row in cursor.fetchall()]

    def get_monthly_cashflow(self, num_months: int = 6) -> List[Dict[str, Any]]:
        """Mengambil data arus kas (pemasukan & pengeluaran) per bulan untuk grafik batang."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
           
            cursor.execute("""
                SELECT 
                    substr(date, 1, 7) as month,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
                FROM transactions
                GROUP BY substr(date, 1, 7)
                ORDER BY month DESC
                LIMIT ?
            """, (num_months,))
            rows = cursor.fetchall()
            return [dict(r) for r in reversed(rows)]

    def get_budget(self, month: str) -> float:
        """Mengambil batas anggaran untuk bulan tertentu ('YYYY-MM')."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT monthly_limit FROM budgets WHERE month = ?", (month,))
            row = cursor.fetchone()
            return float(row["monthly_limit"]) if row else 0.0

    def set_budget(self, month: str, limit_amount: float) -> bool:
        """Menyimpan atau memperbarui batas anggaran bulanan."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO budgets (month, monthly_limit)
                VALUES (?, ?)
                ON CONFLICT(month) DO UPDATE SET monthly_limit = excluded.monthly_limit
            """, (month, float(limit_amount)))
            conn.commit()
            return True

  
    def seed_demo_data(self):
        """Membuat beberapa transaksi contoh realistis untuk demonstrasi fitur."""
        today = datetime.now()
        cur_month = today.strftime("%Y-%m")

        if self.get_budget(cur_month) == 0:
            self.set_budget(cur_month, 5000000.0)

        demo_records = [
            ("income", "Gaji & Upah", 8500000.0, today.strftime("%Y-%m-01"), "Gaji Bulanan"),
            ("income", "Bisnis & Freelance", 1750000.0, (today - timedelta(days=2)).strftime("%Y-%m-%d"), "Projek Desain Web"),
            ("expense", "Tagihan & Utilitas", 650000.0, (today - timedelta(days=3)).strftime("%Y-%m-%d"), "Listrik PLN & WiFi Internet"),
            ("expense", "Makanan & Minuman", 125000.0, (today - timedelta(days=1)).strftime("%Y-%m-%d"), "Makan Siang & Kopi"),
            ("expense", "Belanja Kebutuhan", 480000.0, (today - timedelta(days=4)).strftime("%Y-%m-%d"), "Belanja Bulanan Supermarket"),
            ("expense", "Transportasi", 200000.0, (today - timedelta(days=2)).strftime("%Y-%m-%d"), "Bensin Motor & E-Toll"),
            ("expense", "Hiburan & Hobi", 199000.0, today.strftime("%Y-%m-%d"), "Langganan Netflix & Spotify"),
            ("expense", "Kesehatan & Obat", 150000.0, (today - timedelta(days=5)).strftime("%Y-%m-%d"), "Vitamin & Suplemen"),
        ]

        with self._get_connection() as conn:
            cursor = conn.cursor()
            for rec in demo_records:
                cursor.execute("""
                    INSERT INTO transactions (type, category, amount, date, description)
                    VALUES (?, ?, ?, ?, ?)
                """, rec)
            conn.commit()

    def clear_all_transactions(self):
        """Menghapus semua riwayat transaksi untuk memulai dari awal."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
            conn.commit()
