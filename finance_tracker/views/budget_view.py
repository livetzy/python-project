import customtkinter as ctk
from datetime import datetime
from finance_tracker.utils import COLORS, format_rupiah
from finance_tracker.database import Database
from finance_tracker.views.dialogs import SetBudgetDialog

class BudgetView(ctk.CTkScrollableFrame):
    """
    Halaman Manajemen Anggaran Bulanan: Menampilkan batas anggaran,
    pengeluaran aktual, sisa anggaran, persentase keterpakaian, dan rincian alokasi per kategori.
    """
    def __init__(self, parent, db: Database, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.db = db
        self.current_month = datetime.now().strftime("%Y-%m")

        self._build_header()
        self._build_budget_hero_card()
        self._build_category_breakdown()
        self._build_financial_tips()

        self.refresh()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="Manajemen Anggaran Bulanan",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Tetapkan batas pengeluaran bulanan dan pantau disiplin finansial Anda",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        # Tombol Ubah Anggaran
        self.btn_set_budget = ctk.CTkButton(
            header_frame,
            text="🎯 Atur Target Anggaran",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=36,
            command=self._open_set_budget_dialog
        )
        self.btn_set_budget.pack(side="right")

    def _build_budget_hero_card(self):
        self.hero_card = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.hero_card.pack(fill="x", pady=(0, 20))

        inner = ctk.CTkFrame(self.hero_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=20)

        # Baris Judul & Status Badge
        top_row = ctk.CTkFrame(inner, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 16))

        month_dt = datetime.strptime(self.current_month, "%Y-%m")
        month_name = month_dt.strftime("%B %Y")
        ctk.CTkLabel(
            top_row,
            text=f"Status Anggaran ({month_name})",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(side="left")

        self.status_badge = ctk.CTkLabel(
            top_row,
            text="Aman",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["income"],
            text_color=COLORS["white"],
            corner_radius=6,
            padx=10,
            pady=2
        )
        self.status_badge.pack(side="right")

        # Kolom Ringkasan (Limit, Aktual, Sisa)
        stats_row = ctk.CTkFrame(inner, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 16))
        stats_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="stat")

        # 1. Target Batas
        col1 = ctk.CTkFrame(stats_row, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(col1, text="TARGET ANGGARAN", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["text_muted"]).pack(anchor="w")
        self.val_limit = ctk.CTkLabel(col1, text="Rp 0", font=ctk.CTkFont(size=18, weight="bold"))
        self.val_limit.pack(anchor="w")

        # 2. Terpakai
        col2 = ctk.CTkFrame(stats_row, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(col2, text="PENGELUARAN AKTUAL", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["text_muted"]).pack(anchor="w")
        self.val_spent = ctk.CTkLabel(col2, text="Rp 0", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["expense"])
        self.val_spent.pack(anchor="w")

        # 3. Sisa
        col3 = ctk.CTkFrame(stats_row, fg_color="transparent")
        col3.grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(col3, text="SISA ANGGARAN", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["text_muted"]).pack(anchor="w")
        self.val_remaining = ctk.CTkLabel(col3, text="Rp 0", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["income"])
        self.val_remaining.pack(anchor="w")

        # Progress Bar Besar
        self.progress_bar = ctk.CTkProgressBar(
            inner,
            orientation="horizontal",
            progress_color=COLORS["income"],
            fg_color="#3B3E52",
            height=12,
            corner_radius=6
        )
        self.progress_bar.pack(fill="x", pady=(0, 6))

        # Keterangan Persentase di Bawah Bar
        self.progress_label = ctk.CTkLabel(
            inner,
            text="0% Terpakai",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        )
        self.progress_label.pack(anchor="w")

    def _build_category_breakdown(self):
        cat_box = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        cat_box.pack(fill="x", pady=(0, 20))

        # Header
        header = ctk.CTkFrame(cat_box, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            header,
            text="🏷️ Rincian Pengeluaran Bulan Ini",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(side="left")

        self.category_list_container = ctk.CTkFrame(cat_box, fg_color="transparent")
        self.category_list_container.pack(fill="x", padx=16, pady=(0, 14))

    def _build_financial_tips(self):
        tips_card = ctk.CTkFrame(
            self,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        tips_card.pack(fill="x", pady=(0, 20))

        inner = ctk.CTkFrame(tips_card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            inner,
            text="💡 Tips Finansial Cerdas (Metode 50/30/20)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["budget"]
        ).pack(anchor="w", pady=(0, 8))

        tips_text = (
            "• 50% Kebutuhan Pokok: Gunakan untuk sewa/rumah, makan pokok, tagihan listrik & transportasi rutin.\n"
            "• 30% Keinginan Pribadi: Alokasikan untuk hiburan, belanja hobi, nongkrong, dan liburan santai.\n"
            "• 20% Tabungan & Investasi: Sisihkan di awal bulan untuk dana darurat minimal 3-6 bulan pengeluaran."
        )
        ctk.CTkLabel(
            inner,
            text=tips_text,
            font=ctk.CTkFont(size=12),
            text_color=(COLORS["dark"], COLORS["text_light"]),
            justify="left"
        ).pack(anchor="w")

    def _open_set_budget_dialog(self):
        SetBudgetDialog(
            parent=self.winfo_toplevel(),
            db=self.db,
            current_month=self.current_month,
            on_success=self.refresh
        )

    def refresh(self):
        limit = self.db.get_budget(self.current_month)
        stats = self.db.get_summary_stats(month=self.current_month)
        spent = stats["total_expense"]
        remaining = max(0, limit - spent) if limit > 0 else 0

        self.val_limit.configure(text=format_rupiah(limit) if limit > 0 else "Belum Diatur")
        self.val_spent.configure(text=format_rupiah(spent))
        self.val_remaining.configure(text=format_rupiah(remaining) if limit > 0 else "-")

        if limit > 0:
            ratio = spent / limit
            pct = int(ratio * 100)
            clamped_ratio = max(0.0, min(1.0, ratio))

            if ratio < 0.70:
                status_txt = "✅ Aman"
                status_color = COLORS["income"]
            elif ratio <= 1.0:
                status_txt = "⚠️ Waspada"
                status_color = COLORS["budget"]
            else:
                status_txt = f"🚨 Overbudget ({pct}%)"
                status_color = COLORS["expense"]

            self.status_badge.configure(text=status_txt, fg_color=status_color)
            self.progress_bar.configure(progress_color=status_color)
            self.progress_bar.set(clamped_ratio)
            self.progress_label.configure(
                text=f"{pct}% telah terpakai dari total anggaran {format_rupiah(limit)}"
            )
        else:
            self.status_badge.configure(text="Belum Diatur", fg_color=COLORS["text_muted"])
            self.progress_bar.configure(progress_color=COLORS["text_muted"])
            self.progress_bar.set(0.0)
            self.progress_label.configure(text="Klik tombol 'Atur Target Anggaran' untuk menetapkan batas.")

        # Update rincian pengeluaran kategori bulan ini
        for child in self.category_list_container.winfo_children():
            child.destroy()

        categories = self.db.get_expenses_by_category(month=self.current_month)
        if not categories:
            ctk.CTkLabel(
                self.category_list_container,
                text="Belum ada pengeluaran yang tercatat pada bulan ini.",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"]
            ).pack(pady=12)
        else:
            total_cat_spent = sum(amt for _, amt in categories)
            for cat_name, amt in categories:
                cat_row = ctk.CTkFrame(self.category_list_container, fg_color="transparent")
                cat_row.pack(fill="x", pady=4)

                cat_pct = (amt / total_cat_spent) * 100 if total_cat_spent > 0 else 0

                top_sub = ctk.CTkFrame(cat_row, fg_color="transparent")
                top_sub.pack(fill="x")

                ctk.CTkLabel(
                    top_sub,
                    text=cat_name,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=(COLORS["dark"], COLORS["white"])
                ).pack(side="left")

                ctk.CTkLabel(
                    top_sub,
                    text=f"{format_rupiah(amt)} ({cat_pct:.1f}%)",
                    font=ctk.CTkFont(size=12),
                    text_color=COLORS["expense"]
                ).pack(side="right")

                # Progress Bar kecil untuk proporsi kategori
                mini_bar = ctk.CTkProgressBar(
                    cat_row,
                    orientation="horizontal",
                    progress_color=COLORS["primary"],
                    fg_color="#3B3E52",
                    height=5,
                    corner_radius=2
                )
                mini_bar.set(cat_pct / 100.0)
                mini_bar.pack(fill="x", pady=(2, 4))
