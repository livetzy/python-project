import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Tuple, Dict, Any
from finance_tracker.utils import COLORS, format_rupiah


CHART_COLORS = [
    "#F43F5E", "#3B82F6", "#10B981", "#F59E0B",
    "#8B5CF6", "#EC4899", "#14B8A6", "#6366F1",
    "#06B6D4", "#EAB308", "#84CC16", "#A855F7"
]

class DonutChartFrame(ctk.CTkFrame):
    """
    Frame berisi Donut Chart Matplotlib untuk visualisasi pengeluaran per kategori.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"]),
            **kwargs
        )
        self.canvas = None
        self.fig = None

       
        self.header_label = ctk.CTkLabel(
            self,
            text="🍩 Pengeluaran per Kategori",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        )
        self.header_label.pack(anchor="w", padx=16, pady=(12, 4))

        
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def render(self, category_data: List[Tuple[str, float]], is_dark_mode: bool = True):
        """
        Merender grafik donat.
        category_data: [('Makanan & Minuman', 500000), ('Transportasi', 200000), ...]
        """
       
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            if self.fig:
                plt.close(self.fig)

        bg_color = "#24273A" if is_dark_mode else "#FFFFFF"
        text_color = "#CAD3F5" if is_dark_mode else "#1E293B"

        self.fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=100)
        self.fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        if not category_data or sum(val for _, val in category_data) == 0:
            ax.text(
                0.5, 0.5, "Belum ada transaksi\npengeluaran",
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=11,
                color="#8087A2",
                transform=ax.transAxes
            )
            ax.axis('off')
        else:
           
            if len(category_data) > 6:
                top_items = category_data[:5]
                other_sum = sum(val for _, val in category_data[5:])
                plot_data = top_items + [("Lainnya", other_sum)]
            else:
                plot_data = category_data

            labels = [item[0] for item in plot_data]
            values = [item[1] for item in plot_data]
            total_expense = sum(values)

            colors = CHART_COLORS[:len(values)]

          
            wedges, _ = ax.pie(
                values,
                labels=None,
                colors=colors,
                startangle=140,
                wedgeprops=dict(width=0.42, edgecolor=bg_color, linewidth=2)
            )

        
            ax.text(
                0, 0, f"Total\n{format_rupiah(total_expense)}",
                ha='center', va='center',
                fontsize=9, weight='bold',
                color=text_color
            )

        
            legend_labels = [
                f"{lbl[:14]}.. ({(val/total_expense)*100:.0f}%)" if len(lbl) > 16 else f"{lbl} ({(val/total_expense)*100:.0f}%)"
                for lbl, val in zip(labels, values)
            ]
            ax.legend(
                wedges,
                legend_labels,
                loc="center left",
                bbox_to_anchor=(0.95, 0.5),
                fontsize=8,
                frameon=False,
                labelcolor=text_color
            )

            ax.axis('equal')

        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


class CashflowBarChartFrame(ctk.CTkFrame):
    """
    Frame berisi Bar Chart Matplotlib untuk perbandingan Pemasukan vs Pengeluaran bulanan.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            corner_radius=14,
            fg_color=(COLORS["white"], COLORS["card_dark"]),
            border_width=1,
            border_color=(COLORS["card_border"], COLORS["card_border"]),
            **kwargs
        )
        self.canvas = None
        self.fig = None

        self.header_label = ctk.CTkLabel(
            self,
            text="📊 Arus Kas Pemasukan vs Pengeluaran",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(COLORS["dark"], COLORS["white"])
        )
        self.header_label.pack(anchor="w", padx=16, pady=(12, 4))

        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def render(self, cashflow_data: List[Dict[str, Any]], is_dark_mode: bool = True):
        """
        cashflow_data: [{'month': '2026-04', 'income': 5000000, 'expense': 3000000}, ...]
        """
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            if self.fig:
                plt.close(self.fig)

        bg_color = "#24273A" if is_dark_mode else "#FFFFFF"
        text_color = "#CAD3F5" if is_dark_mode else "#1E293B"
        grid_color = "#363A4F" if is_dark_mode else "#E2E8F0"

        self.fig, ax = plt.subplots(figsize=(5.0, 3.2), dpi=100)
        self.fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        if not cashflow_data:
            ax.text(
                0.5, 0.5, "Belum ada riwayat data bulanan",
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=11,
                color="#8087A2",
                transform=ax.transAxes
            )
            ax.axis('off')
        else:
            months = [d["month"] for d in cashflow_data]
            incomes = [d["income"] for d in cashflow_data]
            expenses = [d["expense"] for d in cashflow_data]

            import numpy as np
            x = np.arange(len(months))
            width = 0.35

            rects1 = ax.bar(x - width/2, [inc / 1e6 for inc in incomes], width, label='Pemasukan', color=COLORS["income"], alpha=0.9, edgecolor='none')
            rects2 = ax.bar(x + width/2, [exp / 1e6 for exp in expenses], width, label='Pengeluaran', color=COLORS["expense"], alpha=0.9, edgecolor='none')

            ax.set_ylabel('Juta Rupiah (Jt)', color=text_color, fontsize=8)
            ax.set_xticks(x)
            ax.set_xticklabels(months, color=text_color, fontsize=8)
            ax.tick_params(colors=text_color)
            ax.grid(axis='y', linestyle='--', alpha=0.3, color=grid_color)
            
        
            for spine in ['top', 'right']:
                ax.spines[spine].set_visible(False)
            for spine in ['left', 'bottom']:
                ax.spines[spine].set_color(grid_color)

            ax.legend(loc='upper right', frameon=False, labelcolor=text_color, fontsize=8)

        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
