import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Any, Optional
from finance_tracker.utils import COLORS
from finance_tracker.database import Database
from finance_tracker.views.dashboard_view import DashboardView
from finance_tracker.views.transactions_view import TransactionsView
from finance_tracker.views.budget_view import BudgetView
from finance_tracker.views.analytics_view import AnalyticsView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FinanceTrackerApp(ctk.CTk):
    """
    Jendela Utama Aplikasi Personal Finance Tracker (FinTrack).
    Mengatur Sidebar Navigasi, Routing Halaman, Tema, dan Database.
    """
    def __init__(self, db_path: Optional[str] = None):
        super().__init__()
        self.db = Database(db_path) if db_path else Database()

        self.title("FinTrack — Personal Finance Tracker")
        self.geometry("1180x750")
        self.minsize(980, 640)

        self._center_window()
        self._init_layout()
        self._show_view("dashboard")

    def _center_window(self):
        self.update_idletasks()
        w = 1180
        h = 750
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _init_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=(COLORS["white"], COLORS["sidebar_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"])
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        self.sidebar.grid_propagate(False)

        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.pack(fill="x", padx=16, pady=(24, 24))

        ctk.CTkLabel(
            logo_box,
            text="💰 FinTrack",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_box,
            text="Personal Finance Tracker",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.nav_buttons = {}
        menu_items = [
            ("dashboard", "📊  Dashboard"),
            ("transactions", "💳  Transaksi"),
            ("budget", "🎯  Anggaran"),
            ("analytics", "📈  Analisis")
        ]

        for view_key, label in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=(COLORS["dark"], COLORS["text_light"]),
                hover_color=COLORS["gray_hover"],
                command=lambda k=view_key: self._show_view(k)
            )
            btn.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[view_key] = btn

        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom", padx=14, pady=20)

        self.btn_demo = ctk.CTkButton(
            bottom_frame,
            text="✨ Muat Data Demo",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["card_border"],
            text_color=(COLORS["dark"], COLORS["text_light"]),
            hover_color=COLORS["gray_hover"],
            height=34,
            command=self._load_demo_data
        )
        self.btn_demo.pack(fill="x", pady=(0, 6))

        self.btn_reset = ctk.CTkButton(
            bottom_frame,
            text="🗑️ Reset Transaksi",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["card_border"],
            text_color=COLORS["expense"],
            hover_color=COLORS["gray_hover"],
            height=34,
            command=self._reset_transactions
        )
        self.btn_reset.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            bottom_frame,
            text="TEMA APLIKASI",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_muted"]
        ).pack(anchor="w", pady=(0, 4))

        self.theme_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=["Dark Mode", "Light Mode"],
            command=self._change_theme,
            height=32
        )
        self.theme_menu.pack(fill="x")

        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.current_view_name = None
        self.current_view_widget = None

    def _show_view(self, view_name: str):
        if self.current_view_name == view_name and self.current_view_widget:
            
            if hasattr(self.current_view_widget, "refresh"):
                self.current_view_widget.refresh()
            return

        if self.current_view_widget:
            self.current_view_widget.destroy()

        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.configure(
                    fg_color=COLORS["primary"],
                    hover_color=COLORS["primary_hover"],
                    text_color=COLORS["white"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=COLORS["gray_hover"],
                    text_color=(COLORS["dark"], COLORS["text_light"])
                )

        if view_name == "dashboard":
            self.current_view_widget = DashboardView(self.content_area, self.db, self._show_view)
        elif view_name == "transactions":
            self.current_view_widget = TransactionsView(self.content_area, self.db)
        elif view_name == "budget":
            self.current_view_widget = BudgetView(self.content_area, self.db)
        elif view_name == "analytics":
            self.current_view_widget = AnalyticsView(self.content_area, self.db)

        self.current_view_widget.grid(row=0, column=0, sticky="nsew")
        self.current_view_name = view_name

    def _load_demo_data(self):
        confirm = messagebox.askyesno(
            "Muat Data Demo",
            "Aplikasi akan menambahkan beberapa transaksi contoh (gaji, makan, belanja, dll.) ke database agar Anda dapat melihat tampilan grafik secara langsung.\n\nLanjutkan?",
            parent=self
        )
        if confirm:
            self.db.seed_demo_data()
            if hasattr(self.current_view_widget, "refresh"):
                self.current_view_widget.refresh()
            messagebox.showinfo("Sukses", "Data demo berhasil ditambahkan! Silakan cek grafik dan transaksi Anda.", parent=self)

    def _reset_transactions(self):
        confirm = messagebox.askyesno(
            "Konfirmasi Reset",
            "Apakah Anda yakin ingin menghapus SEMUA data transaksi?\nTindakan ini tidak dapat dibatalkan.",
            parent=self
        )
        if confirm:
            self.db.clear_all_transactions()
            if hasattr(self.current_view_widget, "refresh"):
                self.current_view_widget.refresh()
            messagebox.showinfo("Reset Selesai", "Semua riwayat transaksi telah dikosongkan.", parent=self)

    def _change_theme(self, choice: str):
        if "Dark" in choice:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        
        if hasattr(self.current_view_widget, "refresh"):
            self.current_view_widget.refresh()

def run_app():
    app = FinanceTrackerApp()
    app.mainloop()

if __name__ == "__main__":
    run_app()
