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

## Catatan Teknis
- Data keranjang disimpan di **Flask session** (tidak perlu database) — cukup untuk scope tugas praktikum ini.
- Validasi checkout dilakukan di **dua sisi**: client-side (HTML5 + Bootstrap `was-validated`) dan server-side (regex nomor HP & email, panjang minimal field) di `app.py`.
- Harga produk, level pedas, dan topping didefinisikan sebagai data statis di `app.py` (dictionary `PRODUCT`) — mudah diedit kalau mau ganti brand/produk lain.

## Deploy ke Render (gratis)
1. Push project ini ke GitHub (lihat langkah di bawah).
2. Buka [render.com](https://render.com) → New → Web Service → hubungkan repo GitHub kamu.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Deploy, lalu catat URL yang diberikan Render untuk dilampirkan di laporan.

## Push ke GitHub
```bash
git init
git add .
git commit -m "Cibay Bojot - Flask e-commerce app"
git branch -M main
git remote add origin https://github.com/USERNAME/cibay-bojot.git
git push -u origin main
```
(Ganti `USERNAME` dengan username GitHub kamu, dan buat repo baru bernama `cibay-bojot` dulu di GitHub sebelum push.)

## Yang Masih Perlu Kamu Lengkapi
Sesuai poin-poin tugas, ini yang belum termasuk di source code dan perlu kamu kerjakan sendiri:
- [ ] Ganti mascot/emoji dengan asset grafis asli (boleh dari Freepik) sesuai instruksi tugas poin 6
- [ ] Upload asset ke Google Drive, lampirkan link di laporan
- [ ] Deploy ke Heroku/Render
- [ ] Push source code ke GitHub
- [ ] Buat laporan project (.doc & .pdf) — aku bisa bantu buatkan pakai template yang sudah disediakan
- [ ] Rekam video tutorial, upload ke channel YouTube `praktikumsismul_[nama kamu]`
- [ ] Lampirkan semua link (GitHub, deploy, drive, YouTube) di laporan
