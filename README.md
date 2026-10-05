# 💰 FinTrack — Personal Finance Tracker

Aplikasi pencatat keuangan pribadi modern, elegan, dan mudah digunakan yang dibangun dengan **Python**, antarmuka modern **CustomTkinter**, visualisasi data interaktif **Matplotlib**, dan penyimpanan database **SQLite**.

---

## 🌟 Fitur Utama

- **📊 Dashboard Interaktif**:
  - Kartu metrik: **Total Saldo**, **Pemasukan**, **Pengeluaran**, dan **Status Anggaran**.
  - **Donut Chart**: Komposisi pengeluaran berdasarkan kategori secara visual.
  - **Bar Chart**: Perbandingan arus kas bulanan (Pemasukan vs Pengeluaran).
  - Ringkasan 5 transaksi terkini.
- **💳 Riwayat Transaksi**:
  - Pencarian real-time berdasarkan deskripsi atau nama kategori.
  - Filter berdasarkan tipe transaksi (*Semua*, *Pemasukan*, *Pengeluaran*) dan kategori.
  - Tambah, edit, dan hapus transaksi dengan konfirmasi.
  - **Ekspor CSV**: Simpan seluruh riwayat transaksi ke format `.csv` untuk dibuka di Excel atau Google Sheets.
- **🎯 Manajemen Anggaran (Budgeting)**:
  - Tetapkan batas anggaran pengeluaran bulanan.
  - Progress bar visual dinamis: **Aman (Hijau)**, **Waspada (Kuning)**, dan **Overbudget (Merah)**.
  - Rincian kontribusi pengeluaran per kategori.
  - Tips finansial berbasis metode cerdas 50/30/20.
- **📈 Analisis & Kesehatan Finansial**:
  - Perhitungan otomatis **Savings Rate** (Tingkat Tabungan).
  - Deteksi pos pengeluaran terbesar.
  - Rata-rata pengeluaran per transaksi.
  - Tabel rincian alokasi biaya per kategori lengkap dengan persentase.
- **✨ Fitur Tambahan**:
  - **Muat Data Demo**: Coba semua fitur dan grafik dalam 1 klik tanpa perlu input data manual di awal.
  - **Reset Data**: Bersihkan semua data untuk mulai dari awal kapan saja.
  - **Dark Mode & Light Mode**: Dukungan mode gelap dan terang yang nyaman di mata.
  - **Format Rupiah Otomatis**: Format angka otomatis (`Rp 1.500.000`).

---

## 🚀 Cara Menjalankan Aplikasi

Pastikan Python dan dependensi telah terpasang:

```powershell
pip install customtkinter matplotlib
```

Jalankan perintah berikut di folder proyek:

```powershell
python run_finance_tracker.py
```

---

## 📁 Struktur Proyek

```
c:\Users\jabes\OneDrive\Documents\python\
├── run_finance_tracker.py         # Launcher utama aplikasi
├── README.md                      # Dokumentasi & panduan
└── finance_tracker/
    ├── __init__.py
    ├── app.py                     # Window utama, sidebar, dan router navigasi
    ├── database.py                # Database SQLite (transaksi, kategori, anggaran)
    ├── utils.py                   # Formatter rupiah, tanggal, palet warna, ekspor CSV
    ├── components/
    │   ├── cards.py               # Widget kartu metrik statistik
    │   └── charts.py              # Grafik Donut & Bar chart Matplotlib
    ├── views/
    │   ├── dashboard_view.py      # Tampilan Dashboard
    │   ├── transactions_view.py   # Tampilan Riwayat Transaksi & Filter
    │   ├── budget_view.py         # Tampilan Manajemen Anggaran & Progress Bar
    │   ├── analytics_view.py      # Tampilan Analisis Keuangan & Savings Rate
    │   └── dialogs.py             # Modal dialog Tambah/Edit Transaksi & Anggaran
    └── tests/
        ├── test_database.py       # Unit test database & logika kalkulasi
        └── test_views.py          # UI smoke test instansiasi komponen
```
