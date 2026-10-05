import csv
from datetime import datetime
from typing import List, Dict, Any, Optional


COLORS = {
    "bg_dark": "#181825",
    "card_dark": "#24273A",
    "card_border": "#363A4F",
    "sidebar_dark": "#1E2030",
    "primary": "#6366F1",       
    "primary_hover": "#4F46E5",
    "income": "#10B981",        
    "income_light": "#D1FAE5",
    "expense": "#F43F5E",       
    "expense_light": "#FFE4E6",
    "balance": "#3B82F6",       
    "budget": "#F59E0B",        
    "text_light": "#CAD3F5",
    "text_muted": "#8087A2",
    "white": "#FFFFFF",
    "dark": "#11111B",
    "gray_hover": "#363A4F",
    "row_light": "#F1F5F9",
    "row_dark": "#1E2030"
}

def format_rupiah(amount: float) -> str:
  
    try:
        val = float(amount)
    except (ValueError, TypeError):
        val = 0.0

    is_negative = val < 0
    val = abs(val)
    
   
    formatted = f"{val:,.0f}".replace(",", ".")
    if is_negative:
        return f"-Rp {formatted}"
    return f"Rp {formatted}"

def parse_amount(text: str) -> Optional[float]:

    if not text:
        return None
    cleaned = (
        text.strip()
        .replace("Rp", "")
        .replace("rp", "")
        .replace(" ", "")
        .replace(".", "")
        .replace(",", ".")
    )
    try:
        val = float(cleaned)
        return val if val >= 0 else None
    except ValueError:
        return None

def get_today_str() -> str:
   
    return datetime.now().strftime("%Y-%m-%d")

def format_display_date(date_str: str) -> str:

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        bulan = [
            "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
            "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
        ]
        return f"{dt.day:02d} {bulan[dt.month - 1]} {dt.year}"
    except Exception:
        return date_str

def export_transactions_to_csv(transactions: List[Dict[str, Any]], filepath: str) -> bool:
  
    try:
        fieldnames = ["id", "date", "type", "category", "amount", "description"]
        with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for tx in transactions:
                writer.writerow({
                    "id": tx.get("id"),
                    "date": tx.get("date"),
                    "type": "Pemasukan" if tx.get("type") == "income" else "Pengeluaran",
                    "category": tx.get("category"),
                    "amount": tx.get("amount"),
                    "description": tx.get("description", "")
                })
        return True
    except Exception as e:
        print(f"Gagal mengekspor CSV: {e}")
        return False
