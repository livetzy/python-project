import customtkinter as ctk
from datetime import datetime
from finance_tracker.utils import COLORS, format_rupiah
from finance_tracker.database import Database

class AnalyticsView(ctk.CTkScrollableFrame):
    """
    Halaman Analisis & Kesehatan Finansial:
    Menghitung Savings Rate (Tingkat Tabungan), Rata-rata pengeluaran harian,
    identifikasi pos pengeluaran terbesar, dan rasio keuangan cerdas.
    """
    def __init__(self, parent, db: Database, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.db = db

        self._build_header()
        self._build_health_cards()
        self._build_detailed_table()

        self.refresh()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="Analisis & Kesehatan Finansial",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Evaluasi kebiasaan belanja dan tingkat tabungan (Savings Rate) Anda",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

    def _build_health_cards(self):
        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.pack(fill="x", pady=(0, 20))
        cards_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="health_card")

        # 1. Card Savings Rate
        self.card_savings = ctk.CTkFrame(
            cards_row,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.card_savings.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self._fill_stat_box(self.card_savings, "SAVINGS RATE", "0%", "💼", COLORS["income"], "Tingkat tabungan dari pemasukan")

        # 2. Card Pengeluaran Terbesar
        self.card_top_exp = ctk.CTkFrame(
            cards_row,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.card_top_exp.grid(row=0, column=1, sticky="ew", padx=8)
        self._fill_stat_box(self.card_top_exp, "PENGELUARAN TERBESAR", "-", "🔥", COLORS["expense"], "Pos belanja paling dominan")

        # 3. Card Rata-rata per Transaksi
        self.card_avg = ctk.CTkFrame(
            cards_row,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.card_avg.grid(row=0, column=2, sticky="ew", padx=(8, 0))
        self._fill_stat_box(self.card_avg, "RATA-RATA PENGELUARAN", "Rp 0", "🏷️", COLORS["primary"], "Per transaksi pengeluaran")

    def _fill_stat_box(self, parent, title, val_text, icon, color, subtitle):
        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=icon, font=ctk.CTkFont(size=20)).pack(side="left")
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_muted"]
        ).pack(side="left", padx=(8, 0))

        val_label = ctk.CTkLabel(
            inner,
            text=val_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color
        )
        val_label.pack(anchor="w", pady=(8, 4))
        parent.val_label = val_label

        sub_label = ctk.CTkLabel(
            inner,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        )
        sub_label.pack(anchor="w")
        parent.sub_label = sub_label

    def _build_detailed_table(self):
        table_box = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        table_box.pack(fill="x", pady=(0, 20))

        inner = ctk.CTkFrame(table_box, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            inner,
            text="📊 Rincian Lengkap Pengeluaran Berdasarkan Kategori",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w", pady=(0, 12))

        # Tabel Header
        t_header = ctk.CTkFrame(inner, fg_color=COLORS["gray_hover"], corner_radius=6, height=36)
        t_header.pack(fill="x", pady=(0, 6))
        t_header.pack_propagate(False)

        ctk.CTkLabel(t_header, text="Kategori", font=ctk.CTkFont(size=12, weight="bold"), width=200, anchor="w").pack(side="left", padx=12)
        ctk.CTkLabel(t_header, text="Total Pengeluaran", font=ctk.CTkFont(size=12, weight="bold"), width=150, anchor="e").pack(side="left", padx=12)
        ctk.CTkLabel(t_header, text="Kontribusi (%)", font=ctk.CTkFont(size=12, weight="bold"), width=130, anchor="e").pack(side="left", padx=12)
        ctk.CTkLabel(t_header, text="Status Alokasi", font=ctk.CTkFont(size=12, weight="bold"), width=120, anchor="center").pack(side="right", padx=12)

        self.table_rows_container = ctk.CTkFrame(inner, fg_color="transparent")
        self.table_rows_container.pack(fill="x")

    def refresh(self):
        stats = self.db.get_summary_stats()
        income = stats["total_income"]
        expense = stats["total_expense"]

        # Savings Rate
        if income > 0:
            savings_pct = max(0.0, ((income - expense) / income) * 100)
            self.card_savings.val_label.configure(text=f"{savings_pct:.1f}%")
            if savings_pct >= 30:
                health_txt = "🌟 Sangat Sehat (≥30%)"
            elif savings_pct >= 15:
                health_txt = "👍 Sehat (15-30%)"
            else:
                health_txt = "⚠️ Kurang (<15%)"
            self.card_savings.sub_label.configure(text=health_txt)
        else:
            self.card_savings.val_label.configure(text="0%")
            self.card_savings.sub_label.configure(text="Belum ada pemasukan")

        # Top Expense & Category Breakdown
        categories = self.db.get_expenses_by_category()
        if categories:
            top_cat, top_amt = categories[0]
            self.card_top_exp.val_label.configure(text=top_cat[:16])
            self.card_top_exp.sub_label.configure(text=f"{format_rupiah(top_amt)} total")
        else:
            self.card_top_exp.val_label.configure(text="-")
            self.card_top_exp.sub_label.configure(text="Belum ada data")

        # Rata-rata per transaksi pengeluaran
        tx_expenses = self.db.get_transactions(filter_type="expense")
        if tx_expenses:
            avg_exp = expense / len(tx_expenses)
            self.card_avg.val_label.configure(text=format_rupiah(avg_exp))
            self.card_avg.sub_label.configure(text=f"Dari {len(tx_expenses)} transaksi pengeluaran")
        else:
            self.card_avg.val_label.configure(text="Rp 0")
            self.card_avg.sub_label.configure(text="0 transaksi pengeluaran")

        # Render rows
        for child in self.table_rows_container.winfo_children():
            child.destroy()

        if not categories:
            ctk.CTkLabel(
                self.table_rows_container,
                text="Belum ada pengeluaran yang tercatat.",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"]
            ).pack(pady=16)
        else:
            for cat_name, amt in categories:
                row = ctk.CTkFrame(self.table_rows_container, fg_color="transparent", height=36)
                row.pack(fill="x", pady=2)
                row.pack_propagate(False)

                pct = (amt / expense) * 100 if expense > 0 else 0
                status = "Tinggi" if pct > 35 else ("Sedang" if pct > 15 else "Rendah")
                badge_color = COLORS["expense"] if pct > 35 else (COLORS["budget"] if pct > 15 else COLORS["income"])

                ctk.CTkLabel(row, text=f"🏷️ {cat_name}", font=ctk.CTkFont(size=12), width=200, anchor="w").pack(side="left", padx=12)
                ctk.CTkLabel(row, text=format_rupiah(amt), font=ctk.CTkFont(size=12, weight="bold"), width=150, anchor="e").pack(side="left", padx=12)
                ctk.CTkLabel(row, text=f"{pct:.1f}%", font=ctk.CTkFont(size=12), width=130, anchor="e", text_color=COLORS["text_muted"]).pack(side="left", padx=12)

                badge = ctk.CTkLabel(
                    row,
                    text=status,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color=badge_color,
                    text_color=COLORS["white"],
                    corner_radius=6,
                    width=80,
                    height=22
                )
                badge.pack(side="right", padx=18)
