# Cibay Bojot - Web Penjualan (Flask + Bootstrap)

Aplikasi web penjualan sederhana untuk brand **Cibay Bojot**, dibuat sesuai UI/UX yang sudah dirancang (Pesan → Keranjang → Checkout → Selesai).

## Struktur Halaman
- **Home** (`/`) — landing page brand
- **Pesan** (`/produk`) — kustomisasi level pedas, topping, jumlah
- **Keranjang** (`/keranjang`) — daftar item yang sudah ditambahkan
- **Checkout** (`/checkout`) — form data penerima + alamat (dengan validasi)
- **Selesai** (`/selesai`) — konfirmasi pesanan berhasil

## Cara Menjalankan di Windows (Lokal)

Buka **Command Prompt / PowerShell** di folder project ini, lalu jalankan:

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktifkan virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py
```

Setelah berjalan, buka browser ke: **http://127.0.0.1:5000**

> Jika `python` tidak dikenali, coba `py` sebagai gantinya (`py -m venv venv`, dst).
> Jika ada error `pip` tidak ditemukan setelah aktivasi venv, pastikan venv sudah aktif (akan muncul `(venv)` di awal baris terminal).

## Struktur Folder
```
cibay_bojot/
├── app.py                 # Backend Flask (routing, logic keranjang & checkout)
├── requirements.txt        # Dependencies
├── Procfile                 # Untuk deploy ke Heroku/Render
├── templates/
│   ├── base.html            # Layout dengan tab navigasi (Pesan/Keranjang/Checkout/Selesai)
│   ├── home.html            # Landing page
│   ├── product.html         # Halaman Pesan
│   ├── cart.html            # Halaman Keranjang
│   ├── checkout.html        # Halaman Checkout
│   └── complete.html        # Halaman Selesai
└── static/
    ├── css/style.css        # Styling tema merah-emas Cibay Bojot
    └── js/script.js
```
