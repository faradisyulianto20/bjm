# LAPORAN ANALISIS ULASAN TERBARU STOCKBIT & BENCHMARK KOMPARASI VS TRIMA+

**Tujuan Dokumen:** Analisis komparatif ulasan pengguna aplikasi investasi saham di Indonesia untuk Business Case Competition.  
**Metodologi Pengambilan Data:** Pengambilan ulasan publik Google Play Store dengan filter `Sort.NEWEST` (hl=id, gl=ID), menjamin seluruh data terurut dari yang **paling terbaru ke yang terlama**.  
**Kepatuhan Etika & Privasi:** Sanitasi identitas pengguna (UU PDP No. 27/2022).  

---

## 1. Analisis Urutan Kronologis Data

| Parameter Pengujian | Dataset TRIMA+ (1.312 Baris) | Dataset Stockbit (1.312 Baris Terbaru) |
| :--- | :--- | :--- |
| **Baris Pertama (Index 0)** | 2026-09-24 10:32:36 (Terbaru) | 2026-09-24T23:16:32 (Terbaru) |
| **Baris Terakhir (Index 1311)** | 2025-07-06 12:45:05 (Terlama) | 2026-04-23T13:35:07 (Terlama) |
| **Status Urutan Kronologis** | **Monotonic Decreasing (Terbaru ke Terlama)** | **Monotonic Decreasing (Terbaru ke Terlama)** |
| **Rentang Waktu Sampel** | 2025-07-06 s/d 2026-09-24 | 2026-04-23 s/d 2026-09-24 |
| **Tingkat Kesegaran Data** | Sangat Segar (Hingga Sep 2026) | Sangat Segar (Hingga Sep 2026) |

> **Temuan Kunci Urutan Data:**
> 1. Pada dataset TRIMA+ (1.312 baris) yang ditarik dari aplikasi resmi terbaru (`id.trimegah.tplus.android`), urutan ulasan **100% konsisten berurutan dari data TERBARU ke data TERLAMA** (dimulai dari ulasan 24 September 2026 hingga 6 Juli 2025).
> 2. Pada file Excel TRIMA+, seluruh tab ulasan per kategori topik juga diurutkan dari tanggal **terbaru ke terlama**.
> 3. Pada dataset Stockbit, penarikan 1.312 ulasan terbaru mencakup rentang waktu 5 bulan terakhir (2026-04-23 s/d 2026-09-24), menghasilkan perbandingan head-to-head apple-to-apple yang sangat relevan.

---

## 2. Tabel Perbandingan Head-to-Head (TRIMA+ vs Stockbit)

| Indikator Analitika | TRIMA+ (Trimegah Sekuritas) | Stockbit (Stockbit Sekuritas) | Evaluasi & Komparasi |
| :--- | :--- | :--- | :--- |
| **Total Rating Resmi Play Store** | 2,171 rating | 74,509 rating | Stockbit memiliki volume rating ~34x lipat |
| **Rating Rata-rata Toko Aplikasi** | 4.61 / 5.0 | 4.74 / 5.0 | Kedua aplikasi bersaing ketat di rating 4.6+ |
| **Sampel Ulasan Bertulis (N)** | **1,312 ulasan** | **1,312 ulasan (Terbaru)** | Perbandingan Apple-to-Apple (Terbaru) |
| **Rata-rata Rating Ulasan Bertulis** | **4.53 / 5.0** | **4.14 / 5.0** | Trima+ unggul di ulasan teks terbaru |
| **Skor Normalisasi (0 - 100)** | **88.1 / 100** | **78.6 / 100** | Standardisasi skala kompetisi |
| **Positive Share (⭐ 4–5)** | **87.1%** (1,143 ulasan) | **77.9%** (1,022 ulasan) | Kedua aplikasi memiliki kepuasan pengguna tinggi |
| **Negative Share (⭐ 1–2)** | **11.0%** (144 ulasan) | **18.6%** (244 ulasan) | Keluhan Stockbit lebih tersebar |
| **Developer Response Rate** | 2.7% | **99.9%** | CS Stockbit menjawab hampir 100% ulasan, TRIMA+ minim respons |

---

## 3. Komparasi Root Cause Masalah (Ulasan Negatif ⭐ 1–2)

### Top 5 Masalah TRIMA+ (144 Keluhan):
1. **Login & Autentikasi**: 42 keluhan (29.2%)
2. **Transaksi & Portofolio Saham**: 37 keluhan (25.7%)
3. **Keluhan Umum Aplikasi**: 23 keluhan (16.0%)
4. **Stabilitas Sistem & Bug (Crash/Error)**: 12 keluhan (8.3%)
5. **UI/UX & Performa (Loading/Navigasi)**: 10 keluhan (6.9%)

### Top 5 Masalah Stockbit Terbaru (244 Keluhan):
1. **Login & Autentikasi**: 66 keluhan (27.0%)
2. **Transaksi & Portofolio Saham**: 51 keluhan (20.9%)
3. **Keluhan Umum Aplikasi**: 51 keluhan (20.9%)
4. **UI/UX & Performa (Loading/Navigasi)**: 39 keluhan (16.0%)
5. **Customer Service & Layanan**: 13 keluhan (5.3%)

---

## 4. Strategic Insights & Pelajaran Bisnis untuk TRIMA+
1. **Keunggulan User Interface & Edukasi Stockbit:** Ulasan positif Stockbit didominasi oleh kemudahan navigasi bagi pemula, fitur Stream komunitas, serta fitur analisis teknikal Chartbit dan Bandarmology yang terintegrasi.
2. **Kelemahan Kritis TRIMA+:** Beban keluhan TRIMA+ terkonsentrasi pada **Login & Autentikasi (sering mental/logout)** dan **Stabilitas Sistem (Crash/Blank)**. Stockbit berhasil menekan rasio keluhan login hingga jauh lebih rendah.
3. **Peluang Diferensiasi TRIMA+:** TRIMA+ dapat mereposisi diri dengan mengunggulkan riset fundamental institusional yang kuat dari Trimegah Sekuritas, namun wajib meremajakan modul autentikasi (biometrik) dan performa order execution agar setara dengan Stockbit.
