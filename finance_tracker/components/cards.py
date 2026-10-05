import customtkinter as ctk
from typing import Optional
from finance_tracker.utils import COLORS

class StatCard(ctk.CTkFrame):
    """
    Widget kartu ringkasan metrik statistik keuangan dengan aksen warna modern.
    """
    def __init__(
        self,
        parent,
        title: str,
        value: str,
        icon: str = "📊",
        accent_color: str = COLORS["primary"],
        subtitle: str = "",
        progress: Optional[float] = None,
        **kwargs
    ):
        super().__init__(
            parent,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"]),
            **kwargs
        )
        self.accent_color = accent_color

        self.grid_columnconfigure(1, weight=1)

        self.accent_strip = ctk.CTkFrame(
            self,
            width=5,
            corner_radius=3,
            fg_color=accent_color
        )
        self.accent_strip.grid(row=0, column=0, rowspan=4, sticky="ns", padx=(10, 10), pady=12)

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=22)
        )
        self.icon_label.grid(row=0, column=1, sticky="w", pady=(12, 2))

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=(COLORS["text_muted"], COLORS["text_muted"])
        )
        self.title_label.grid(row=1, column=1, sticky="w", pady=(0, 4))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        )
        self.value_label.grid(row=2, column=1, sticky="w", pady=(0, 6))

        if progress is not None:
            clamped = max(0.0, min(1.0, progress))
            bar_color = COLORS["income"] if clamped < 0.75 else (COLORS["budget"] if clamped < 0.9 else COLORS["expense"])
            self.progress_bar = ctk.CTkProgressBar(
                self,
                orientation="horizontal",
                progress_color=bar_color,
                fg_color="#3B3E52",
                height=6,
                corner_radius=3
            )
            self.progress_bar.set(clamped)
            self.progress_bar.grid(row=3, column=1, sticky="ew", padx=(0, 14), pady=(0, 4))

        if subtitle:
            row_idx = 4 if progress is not None else 3
            self.subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(size=11),
                text_color=(COLORS["text_muted"], COLORS["text_muted"])
            )
            self.subtitle_label.grid(row=row_idx, column=1, sticky="w", pady=(0, 12), padx=(0, 14))
        else:
            self.grid_rowconfigure(2, pad=12)

    def update_data(self, value: str, subtitle: Optional[str] = None, progress: Optional[float] = None):
        """Memperbarui isi data kartu secara dinamis."""
        self.value_label.configure(text=value)
        if subtitle is not None and hasattr(self, "subtitle_label"):
            self.subtitle_label.configure(text=subtitle)
        if progress is not None and hasattr(self, "progress_bar"):
            clamped = max(0.0, min(1.0, progress))
            bar_color = COLORS["income"] if clamped < 0.75 else (COLORS["budget"] if clamped < 0.9 else COLORS["expense"])
            self.progress_bar.configure(progress_color=bar_color)
            self.progress_bar.set(clamped)
