import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox
from typing import Callable, Optional
from finance_tracker.utils import COLORS, format_rupiah, format_display_date, export_transactions_to_csv
from finance_tracker.database import Database
from finance_tracker.views.dialogs import AddTransactionDialog

class TransactionsView(ctk.CTkFrame):
    """
    Halaman Riwayat Transaksi: Menampilkan seluruh daftar transaksi,
    pencarian, filter tipe & kategori, tombol tambah, edit, hapus, dan ekspor CSV.
    """
    def __init__(self, parent, db: Database, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.db = db

        self._build_header()
        self._build_filters()
        self._build_transactions_list()

        self.refresh()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))

        # Judul Halaman
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="Riwayat Transaksi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Kelola dan pantau semua aliran pemasukan & pengeluaran Anda",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        # Tombol Aksi di Kanan (Ekspor CSV & Tambah)
        btn_group = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_group.pack(side="right")

        self.btn_export = ctk.CTkButton(
            btn_group,
            text="📥 Ekspor CSV",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["card_border"],
            text_color=(COLORS["dark"], COLORS["text_light"]),
            hover_color=COLORS["gray_hover"],
            height=36,
            command=self._export_csv
        )
        self.btn_export.pack(side="left", padx=(0, 8))

        self.btn_add = ctk.CTkButton(
            btn_group,
            text="➕ Tambah Transaksi",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=36,
            command=self._open_add_dialog
        )
        self.btn_add.pack(side="left")

    def _build_filters(self):
        filter_bar = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        filter_bar.pack(fill="x", pady=(0, 16))

        inner = ctk.CTkFrame(filter_bar, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=10)

        # Input Pencarian
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            inner,
            placeholder_text="🔍 Cari catatan atau kategori...",
            textvariable=self.search_var,
            width=260,
            height=34
        )
        self.search_entry.pack(side="left", padx=(0, 12))
        self.search_var.trace_add("write", lambda *args: self.refresh())

        # Filter Tipe (Semua / Pemasukan / Pengeluaran)
        self.type_filter_var = ctk.StringVar(value="Semua Tipe")
        self.type_menu = ctk.CTkOptionMenu(
            inner,
            variable=self.type_filter_var,
            values=["Semua Tipe", "Pemasukan", "Pengeluaran"],
            command=lambda val: self.refresh(),
            width=140,
            height=34
        )
        self.type_menu.pack(side="left", padx=(0, 12))

        # Filter Kategori
        self.cat_filter_var = ctk.StringVar(value="Semua Kategori")
        self.cat_menu = ctk.CTkOptionMenu(
            inner,
            variable=self.cat_filter_var,
            values=["Semua Kategori"],
            command=lambda val: self.refresh(),
            width=170,
            height=34
        )
        self.cat_menu.pack(side="left")

        # Label Ringkasan Hasil Filter (kanan)
        self.summary_count_label = ctk.CTkLabel(
            inner,
            text="0 Transaksi",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        )
        self.summary_count_label.pack(side="right", padx=6)

    def _build_transactions_list(self):
        # Container tabel list dengan scroll
        self.scroll_list = ctk.CTkScrollableFrame(
            self,
            corner_radius=12,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.scroll_list.pack(fill="both", expand=True)

    def _populate_category_dropdown(self):
        categories = self.db.get_categories()
        unique_names = sorted(list(set(c["name"] for c in categories)))
        self.cat_menu.configure(values=["Semua Kategori"] + unique_names)

    def _open_add_dialog(self, edit_data: Optional[dict] = None):
        AddTransactionDialog(
            parent=self.winfo_toplevel(),
            db=self.db,
            on_success=self.refresh,
            edit_data=edit_data
        )

    def _export_csv(self):
        today_str = datetime.now().strftime("%Y%m%d_%H%M")
        default_filename = f"fintrack_transaksi_{today_str}.csv"
        
        filepath = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Simpan Laporan Transaksi CSV",
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("CSV Spreadsheet", "*.csv"), ("Semua File", "*.*")]
        )
        if filepath:
            transactions = self.db.get_transactions()
            success = export_transactions_to_csv(transactions, filepath)
            if success:
                messagebox.showinfo("Ekspor Berhasil", f"Data transaksi berhasil disimpan ke:\n{filepath}", parent=self.winfo_toplevel())
            else:
                messagebox.showerror("Gagal Ekspor", "Terjadi kesalahan saat menyimpan file CSV.", parent=self.winfo_toplevel())

    def _confirm_delete(self, tx_id: int, desc: str, amount_str: str):
        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus transaksi ini?\n\n{desc} ({amount_str})",
            parent=self.winfo_toplevel()
        )
        if confirm:
            self.db.delete_transaction(tx_id)
            self.refresh()

    def refresh(self):
        self._populate_category_dropdown()

        # Parse filter
        type_val = self.type_filter_var.get()
        filter_type = "income" if type_val == "Pemasukan" else ("expense" if type_val == "Pengeluaran" else None)
        
        category_val = self.cat_filter_var.get()
        search_val = self.search_var.get().strip() or None

        transactions = self.db.get_transactions(
            filter_type=filter_type,
            category=category_val,
            search=search_val
        )

        # Update label jumlah
        self.summary_count_label.configure(text=f"{len(transactions)} Transaksi Ditemukan")

        # Bersihkan list lama
        for child in self.scroll_list.winfo_children():
            child.destroy()

        if not transactions:
            empty_box = ctk.CTkFrame(self.scroll_list, fg_color="transparent")
            empty_box.pack(fill="both", expand=True, pady=40)

            ctk.CTkLabel(
                empty_box,
                text="📂",
                font=ctk.CTkFont(size=40)
            ).pack()

            ctk.CTkLabel(
                empty_box,
                text="Tidak ada transaksi yang cocok",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=COLORS["text_muted"]
            ).pack(pady=(8, 4))

            ctk.CTkLabel(
                empty_box,
                text="Coba ubah kata kunci pencarian atau reset filter di atas.",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_muted"]
            ).pack()
            return

        # Render baris-baris transaksi
        for tx in transactions:
            self._render_row(tx)

    def _render_row(self, tx: dict):
        row = ctk.CTkFrame(
            self.scroll_list,
            fg_color=(COLORS["row_light"], COLORS["row_dark"]),
            corner_radius=10,
            height=54
        )
        row.pack(fill="x", pady=4, padx=4)
        row.pack_propagate(False)

        is_income = tx["type"] == "income"
        icon_badge = "💰" if is_income else "💸"
        color = COLORS["income"] if is_income else COLORS["expense"]
        prefix = "+" if is_income else "-"
        amount_fmt = f"{prefix}{format_rupiah(tx['amount'])}"

        # 1. Icon badge
        ctk.CTkLabel(
            row,
            text=icon_badge,
            font=ctk.CTkFont(size=20),
            width=40
        ).pack(side="left", padx=(10, 4))

        # 2. Category & Description
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="y", pady=8, padx=4)

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

        # 3. Action buttons (Edit & Delete) di paling kanan
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=(8, 12))

        btn_del = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=COLORS["gray_hover"],
            font=ctk.CTkFont(size=13),
            command=lambda: self._confirm_delete(tx["id"], tx["category"], amount_fmt)
        )
        btn_del.pack(side="right", padx=(4, 0))

        btn_edit = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=COLORS["gray_hover"],
            font=ctk.CTkFont(size=13),
            command=lambda: self._open_add_dialog(edit_data=tx)
        )
        btn_edit.pack(side="right")

        # 4. Amount & Date
        amt_frame = ctk.CTkFrame(row, fg_color="transparent")
        amt_frame.pack(side="right", padx=(0, 16), pady=8)

        ctk.CTkLabel(
            amt_frame,
            text=amount_fmt,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color
        ).pack(anchor="e")

        ctk.CTkLabel(
            amt_frame,
            text=format_display_date(tx["date"]),
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack(anchor="e")
