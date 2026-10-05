import customtkinter as ctk
from datetime import datetime
from typing import Callable
from finance_tracker.utils import COLORS, format_rupiah, format_display_date
from finance_tracker.database import Database
from finance_tracker.components.cards import StatCard
from finance_tracker.components.charts import DonutChartFrame, CashflowBarChartFrame
from finance_tracker.views.dialogs import AddTransactionDialog

class DashboardView(ctk.CTkScrollableFrame):
    """
    Halaman Dashboard Utama: Menampilkan ringkasan saldo, metrik utama,
    grafik donat pengeluaran, grafik batang arus kas, dan 5 transaksi terkini.
    """
    def __init__(self, parent, db: Database, navigate_callback: Callable[[str], None], **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.db = db
        self.navigate_callback = navigate_callback

        self._build_header()
        self._build_metric_cards()
        self._build_charts_section()
        self._build_recent_transactions_section()

        self.refresh()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="Ringkasan Keuangan",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w")

        today_str = datetime.now().strftime("%d %B %Y")
        ctk.CTkLabel(
            title_box,
            text=f"Pantau kondisi finansial per {today_str}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.btn_quick_add = ctk.CTkButton(
            header_frame,
            text="➕ Tambah Transaksi",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=38,
            corner_radius=8,
            command=self._open_add_transaction
        )
        self.btn_quick_add.pack(side="right")

    def _build_metric_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=(0, 20))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        # 1. Saldo Saat Ini
        self.card_balance = StatCard(
            self.cards_frame,
            title="TOTAL SALDO",
            value="Rp 0",
            icon="💼",
            accent_color=COLORS["balance"],
            subtitle="Saldo akumulasi saat ini"
        )
        self.card_balance.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.card_income = StatCard(
            self.cards_frame,
            title="TOTAL PEMASUKAN",
            value="Rp 0",
            icon="📈",
            accent_color=COLORS["income"],
            subtitle="Total seluruh pemasukan"
        )
        self.card_income.grid(row=0, column=1, sticky="ew", padx=8)

        self.card_expense = StatCard(
            self.cards_frame,
            title="TOTAL PENGELUARAN",
            value="Rp 0",
            icon="📉",
            accent_color=COLORS["expense"],
            subtitle="Total seluruh pengeluaran"
        )
        self.card_expense.grid(row=0, column=2, sticky="ew", padx=8)

        self.card_budget = StatCard(
            self.cards_frame,
            title="ANGGARAN BULAN INI",
            value="Rp 0",
            icon="🎯",
            accent_color=COLORS["budget"],
            subtitle="Limit bulanan",
            progress=0.0
        )
        self.card_budget.grid(row=0, column=3, sticky="ew", padx=(8, 0))

    def _build_charts_section(self):
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.pack(fill="x", pady=(0, 20))
        charts_frame.grid_columnconfigure((0, 1), weight=1, uniform="chart")

        self.donut_chart = DonutChartFrame(charts_frame)
        self.donut_chart.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.bar_chart = CashflowBarChartFrame(charts_frame)
        self.bar_chart.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    def _build_recent_transactions_section(self):
        recent_box = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        recent_box.pack(fill="x", pady=(0, 20))

        header = ctk.CTkFrame(recent_box, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            header,
            text="🕒 5 Transaksi Terkini",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(side="left")

        btn_view_all = ctk.CTkButton(
            header,
            text="Lihat Semua ➔",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=COLORS["primary"],
            hover_color=COLORS["gray_hover"],
            width=80,
            height=28,
            command=lambda: self.navigate_callback("transactions")
        )
        btn_view_all.pack(side="right")

        self.recent_list_container = ctk.CTkFrame(recent_box, fg_color="transparent")
        self.recent_list_container.pack(fill="x", padx=16, pady=(0, 14))

    def _open_add_transaction(self):
        dialog = AddTransactionDialog(
            parent=self.winfo_toplevel(),
            db=self.db,
            on_success=self.refresh
        )

    def refresh(self):
        """Memperbarui semua data statistik, grafik, dan list transaksi."""

        stats = self.db.get_summary_stats()
        self.card_balance.update_data(format_rupiah(stats["balance"]))
        self.card_income.update_data(
            format_rupiah(stats["total_income"]),
            subtitle=f"{stats['transaction_count']} total transaksi"
        )
        self.card_expense.update_data(format_rupiah(stats["total_expense"]))

        cur_month = datetime.now().strftime("%Y-%m")
        budget_limit = self.db.get_budget(cur_month)
        month_stats = self.db.get_summary_stats(month=cur_month)
        month_expense = month_stats["total_expense"]

        if budget_limit > 0:
            ratio = month_expense / budget_limit
            pct = int(ratio * 100)
            status_text = f"{pct}% terpakai (Sisa {format_rupiah(max(0, budget_limit - month_expense))})"
            self.card_budget.update_data(
                format_rupiah(budget_limit),
                subtitle=status_text,
                progress=ratio
            )
        else:
            self.card_budget.update_data(
                "Belum diatur",
                subtitle="Klik menu Anggaran untuk mengatur",
                progress=0.0
            )

        category_expenses = self.db.get_expenses_by_category()
        self.donut_chart.render(category_expenses)

        cashflow_data = self.db.get_monthly_cashflow(num_months=6)
        self.bar_chart.render(cashflow_data)

        for child in self.recent_list_container.winfo_children():
            child.destroy()

        recent_txs = self.db.get_transactions(limit=5)
        if not recent_txs:
            ctk.CTkLabel(
                self.recent_list_container,
                text="Belum ada transaksi tercatat. Klik tombol '+ Tambah Transaksi' untuk memulai.",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"]
            ).pack(pady=16)
        else:
            for tx in recent_txs:
                self._render_tx_row(self.recent_list_container, tx)

    def _render_tx_row(self, container, tx):
        row = ctk.CTkFrame(
            container,
            fg_color=(COLORS["row_light"], COLORS["row_dark"]),
            corner_radius=8,
            height=48
        )
        row.pack(fill="x", pady=4)
        row.pack_propagate(False)

        is_income = tx["type"] == "income"
        icon_badge = "💰" if is_income else "💸"
        color = COLORS["income"] if is_income else COLORS["expense"]
        prefix = "+" if is_income else "-"

        ctk.CTkLabel(
            row,
            text=icon_badge,
            font=ctk.CTkFont(size=18),
            width=40
        ).pack(side="left", padx=(10, 4))

        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="y", pady=6)

        ctk.CTkLabel(
            info_frame,
            text=tx["category"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w")

        desc_text = tx["description"] if tx["description"] else "Tanpa keterangan"
        ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        right_frame = ctk.CTkFrame(row, fg_color="transparent")
        right_frame.pack(side="right", padx=14, pady=6)

        ctk.CTkLabel(
            right_frame,
            text=f"{prefix}{format_rupiah(tx['amount'])}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color
        ).pack(anchor="e")

        ctk.CTkLabel(
            right_frame,
            text=format_display_date(tx["date"]),
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack(anchor="e")
