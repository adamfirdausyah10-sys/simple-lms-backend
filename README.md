# Simple LMS - Minggu 4 + Minggu 5

Didasarkan pada Modul Praktikum 4 (Django Framework & ORM) dan Modul Praktikum 5 (Database Optimization) Pemrograman Sisi Server. Disusun untuk dijalankan dan diuji di Docker Desktop Windows.

## Persiapan

1. Pastikan Docker Desktop berjalan.
2. Salin `.env.example` menjadi `.env` lalu gunakan password lokal sendiri.
3. Di PowerShell, buka folder project ini.

```powershell
Copy-Item .env.example .env
docker compose build
docker compose up -d
docker compose ps
```

## Django migration dan test

**Custom User harus dibuat sebelum migrate pertama.**

```powershell
docker compose exec app python manage.py makemigrations users catalog
docker compose exec app python manage.py migrate
docker compose exec app python manage.py check
docker compose exec app python manage.py test catalog
```

Jika mau login Django Admin (http://localhost:8000/admin/):

```powershell
docker compose exec app python manage.py createsuperuser
```

Role superuser dapat diubah ke `ADMIN` dari Django shell sebagaimana Modul 4.

## Data dan benchmark Minggu 5

```powershell
docker compose exec app python manage.py seed_demo
docker compose exec app python manage.py generate_performance_data
docker compose exec app python manage.py generate_relationship_data
docker compose exec app python manage.py benchmark_queries
docker compose exec app python manage.py explain_index
```

Generator data dibuat idempotent. Data simulasi menghasilkan minimal 10.000 Course PERF, lalu relasi pada 100 Course PERF (55 user simulasi, 1.000 enrollment, 500 lesson, 200 assignment, 1.000 submission). Ada juga 1 Course PSS01 seed demo.

## Eksperimen index

Ikuti `PANDUAN_INDEX_MINGGU5.txt` dan simpan hasil EXPLAIN BEFORE sebelum mengubah model. Jalankan EXPLAIN AFTER sesudah migration index. Jangan hanya membandingkan query count untuk pengujian index.

## Laporan dan screenshot

Gunakan `LAPORAN_TEMPLATE.md` sebagai kerangka. Isi angka dari eksekusi sendiri dan screenshot terminal yang benar. Jalankan automated test dan screenshot hasilnya. Upload GitHub setelah file `.env` tidak terikut.

## Batas verifikasi

Kode telah diperiksa sintaks statis, tetapi belum dijalankan terhadap Docker dan PostgreSQL di lingkungan ini. Hasil query dan execution time perlu pengukuran pada laptop pengguna.
