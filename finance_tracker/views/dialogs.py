import customtkinter as ctk
from datetime import datetime
from typing import Callable, Optional, Dict, Any
from tkinter import messagebox
from finance_tracker.utils import COLORS, format_rupiah, parse_amount, get_today_str
from finance_tracker.database import Database

class AddTransactionDialog(ctk.CTkToplevel):
    """
    Modal Dialog untuk menambah atau mengedit transaksi dengan validasi dan preview otomatis.
    """
    def __init__(
        self,
        parent,
        db: Database,
        on_success: Callable[[], None],
        edit_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(parent)
        self.db = db
        self.on_success = on_success
        self.edit_data = edit_data

        is_edit = edit_data is not None
        self.title("✏️ Edit Transaksi" if is_edit else "➕ Tambah Transaksi Baru")
        self.geometry("440x540")
        self.resizable(False, False)

        self.after(10, self._center_window)

        self.transient(parent)
        self.grab_set()

        self._build_ui(is_edit)

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _build_ui(self, is_edit: bool):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=20)

        # Header Title
        title_text = "Perbarui Transaksi" if is_edit else "Catat Transaksi Baru"
        ctk.CTkLabel(
            container,
            text=title_text,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", pady=(0, 16))

        ctk.CTkLabel(container, text="Tipe Arus Kas:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(4, 2))
        
        default_type = "Pengeluaran"
        if self.edit_data:
            default_type = "Pemasukan" if self.edit_data.get("type") == "income" else "Pengeluaran"

        self.type_var = ctk.StringVar(value=default_type)
        self.type_segmented = ctk.CTkSegmentedButton(
            container,
            values=["💸 Pengeluaran", "💰 Pemasukan"],
            variable=self.type_var,
            command=self._on_type_change,
            selected_color=COLORS["expense"],
            selected_hover_color="#BE123C",
            height=34
        )
    
        if default_type == "Pemasukan":
            self.type_segmented.set("💰 Pemasukan")
            self.type_segmented.configure(selected_color=COLORS["income"], selected_hover_color="#059669")
        else:
            self.type_segmented.set("💸 Pengeluaran")

        self.type_segmented.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(container, text="Nominal (Rp):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        self.amount_var = ctk.StringVar()
        self.amount_entry = ctk.CTkEntry(
            container,
            placeholder_text="Contoh: 50000 atau 1500000",
            textvariable=self.amount_var,
            height=36
        )
        self.amount_entry.pack(fill="x", pady=(0, 2))
        self.amount_var.trace_add("write", self._on_amount_typed)

        self.preview_label = ctk.CTkLabel(
            container,
            text="Rp 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["text_muted"]
        )
        self.preview_label.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(container, text="Kategori:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        self.category_var = ctk.StringVar()
        self.category_dropdown = ctk.CTkOptionMenu(
            container,
            variable=self.category_var,
            values=["Memuat..."],
            height=36,
            dynamic_resizing=False
        )
        self.category_dropdown.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(container, text="Tanggal (YYYY-MM-DD):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        self.date_entry = ctk.CTkEntry(
            container,
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        today = get_today_str()
        self.date_entry.insert(0, today)
        self.date_entry.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(container, text="Catatan (Opsional):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        self.desc_entry = ctk.CTkEntry(
            container,
            placeholder_text="Contoh: Makan siang bareng teman kantor",
            height=36
        )
        self.desc_entry.pack(fill="x", pady=(0, 20))

        if self.edit_data:
            self.amount_entry.delete(0, "end")
            self.amount_entry.insert(0, str(int(self.edit_data.get("amount", 0))))
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, self.edit_data.get("date", today))
            self.desc_entry.delete(0, "end")
            self.desc_entry.insert(0, self.edit_data.get("description", ""))

        self._refresh_categories()

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")

        self.btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Batal",
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["card_border"],
            text_color=(COLORS["dark"], COLORS["text_light"]),
            hover_color=COLORS["gray_hover"],
            command=self.destroy,
            width=100,
            height=38
        )
        self.btn_cancel.pack(side="left")

        self.btn_save = ctk.CTkButton(
            btn_frame,
            text="Simpan Perubahan" if is_edit else "Simpan Transaksi",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._save_transaction,
            height=38
        )
        self.btn_save.pack(side="right", fill="x", expand=True, padx=(12, 0))

        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self._save_transaction())

    def _on_type_change(self, selected_val: str):
        if "Pemasukan" in selected_val:
            self.type_segmented.configure(selected_color=COLORS["income"], selected_hover_color="#059669")
        else:
            self.type_segmented.configure(selected_color=COLORS["expense"], selected_hover_color="#BE123C")
        self._refresh_categories()

    def _refresh_categories(self):
        curr_type = "income" if "Pemasukan" in self.type_var.get() else "expense"
        cats = self.db.get_categories(category_type=curr_type)
        cat_names = [f"{c['icon']} {c['name']}" for c in cats]

        if not cat_names:
            cat_names = ["Lainnya"]

        self.category_dropdown.configure(values=cat_names)

        selected = cat_names[0]
        if self.edit_data:
            target = self.edit_data.get("category", "")
            for name in cat_names:
                if target in name:
                    selected = name
                    break
        self.category_var.set(selected)

    def _on_amount_typed(self, *args):
        val = parse_amount(self.amount_var.get())
        if val is not None:
            self.preview_label.configure(
                text=format_rupiah(val),
                text_color=COLORS["income"] if "Pemasukan" in self.type_var.get() else COLORS["expense"]
            )
        else:
            self.preview_label.configure(text="Rp 0", text_color=COLORS["text_muted"])

    def _save_transaction(self):
        amount = parse_amount(self.amount_var.get())
        if amount is None or amount <= 0:
            messagebox.showerror("Input Tidak Valid", "Masukkan nominal angka yang lebih dari 0!", parent=self)
            self.amount_entry.focus()
            return

        date_val = self.date_entry.get().strip()
        try:
            datetime.strptime(date_val, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Format Tanggal Salah", "Format tanggal harus YYYY-MM-DD (contoh: 2026-09-03)!", parent=self)
            self.date_entry.focus()
            return

        cat_full = self.category_var.get().strip()
        category_name = cat_full.split(" ", 1)[-1] if " " in cat_full else cat_full
        tx_type = "income" if "Pemasukan" in self.type_var.get() else "expense"
        description = self.desc_entry.get().strip()

        if self.edit_data:
            tx_id = self.edit_data["id"]
            self.db.update_transaction(tx_id, tx_type, category_name, amount, date_val, description)
        else:
            self.db.add_transaction(tx_type, category_name, amount, date_val, description)

        self.on_success()
        self.destroy()


class SetBudgetDialog(ctk.CTkToplevel):
    """
    Modal Dialog untuk mengatur target anggaran bulanan.
    """
    def __init__(self, parent, db: Database, current_month: str, on_success: Callable[[], None]):
        super().__init__(parent)
        self.db = db
        self.current_month = current_month
        self.on_success = on_success

        self.title("🎯 Atur Anggaran Bulanan")
        self.geometry("380x300")
        self.resizable(False, False)

        self.after(10, self._center_window)
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            container,
            text="Target Anggaran Bulan Ini",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            container,
            text=f"Bulan: {self.current_month}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w", pady=(0, 16))

        current_limit = self.db.get_budget(self.current_month)

        ctk.CTkLabel(container, text="Batas Maksimal Pengeluaran (Rp):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        self.amount_var = ctk.StringVar(value=str(int(current_limit)) if current_limit > 0 else "")
        self.amount_entry = ctk.CTkEntry(
            container,
            placeholder_text="Contoh: 5000000",
            textvariable=self.amount_var,
            height=36
        )
        self.amount_entry.pack(fill="x", pady=(0, 2))

        self.preview_label = ctk.CTkLabel(
            container,
            text=format_rupiah(current_limit) if current_limit > 0 else "Rp 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["budget"]
        )
        self.preview_label.pack(anchor="w", pady=(0, 20))

        self.amount_var.trace_add("write", self._on_type_amount)

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")

        ctk.CTkButton(
            btn_frame,
            text="Batal",
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["card_border"],
            hover_color=COLORS["gray_hover"],
            command=self.destroy,
            width=90,
            height=36
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame,
            text="Simpan Anggaran",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._save_budget,
            height=36
        ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def _on_type_amount(self, *args):
        val = parse_amount(self.amount_var.get())
        if val is not None:
            self.preview_label.configure(text=format_rupiah(val))
        else:
            self.preview_label.configure(text="Rp 0")

    def _save_budget(self):
        val = parse_amount(self.amount_var.get())
        if val is None or val < 0:
            messagebox.showerror("Error", "Masukkan nominal anggaran yang valid!", parent=self)
            return

        self.db.set_budget(self.current_month, val)
        self.on_success()
        self.destroy()
