# LAPORAN ANALISIS ULASAN TERBARU STOCKBIT & BENCHMARK KOMPARASI VS TRIMA+

**Tujuan Dokumen:** Analisis komparatif ulasan pengguna aplikasi investasi saham di Indonesia untuk Business Case Competition.  
**Metodologi Pengambilan Data:** Pengambilan ulasan publik Google Play Store dengan filter `Sort.NEWEST` (hl=id, gl=ID), menjamin seluruh data terurut dari yang **paling terbaru ke yang terlama**.  
**Kepatuhan Etika & Privasi:** Sanitasi identitas pengguna (UU PDP No. 27/2022).  

---

## 1. Analisis Urutan Kronologis Data

| Parameter Pengujian | Dataset TRIMA+ (1.312 Baris) | Dataset Stockbit (1.312 Baris Terbaru) |
| :--- | :--- | :--- |
| **Baris Pertama (Index 0)** | 2025-07-10 13:03:30 (Terbaru) | 2026-09-24T23:16:32 (Terbaru) |
| **Baris Terakhir (Index 1311)** | 2016-11-25 20:55:32 (Terlama) | 2026-04-23T13:35:07 (Terlama) |
| **Status Urutan Kronologis** | **Monotonic Decreasing (Terbaru ke Terlama)** | **Monotonic Decreasing (Terbaru ke Terlama)** |
| **Rentang Waktu Sampel** | November 2016 – Juli 2025 (~9 tahun) | April 2026 – September 2026 (~5 bulan) |
| **Tingkat Kesegaran Data** | Historis Kumulatif Lengkap | Sangat Segar & Relevan (Update Terkini) |

> **Temuan Kunci Urutan Data:**
> 1. Pada dataset TRIMA+ (1.312 baris), urutan ulasan dari awal **sudah berurutan dari data terbaru ke data terlama** (dimulai dari review terakhir 10 Juli 2025 hingga review tertua 25 November 2016).
> 2. Pada file Excel TRIMA+, seluruh tab ulasan per topik kini telah dipastikan diurutkan dari tanggal **terbaru ke terlama**.
> 3. Pada dataset Stockbit, penarikan 1.312 ulasan terbaru mencakup rentang waktu 5 bulan terakhir (2026-04-23 s/d 2026-09-24), menghasilkan insight yang sangat relevan dengan rilis fitur dan stabilitas aplikasi saat ini.

---

## 2. Tabel Perbandingan Head-to-Head (TRIMA+ vs Stockbit)

| Indikator Analitika | TRIMA+ (Trimegah Sekuritas) | Stockbit (Stockbit Sekuritas) | Selisih / Evaluasi |
| :--- | :--- | :--- | :--- |
| **Total Rating Resmi Play Store** | 3,747 rating | 74,509 rating | Stockbit memiliki volume rating ~20x lipat |
| **Rating Rata-rata Toko Aplikasi** | 3.12 / 5.0 | 4.74 / 5.0 | Stockbit unggul +1.61 poin |
| **Sampel Ulasan Bertulis (N)** | **1,312 ulasan** | **1,312 ulasan (Terbaru)** | Perbandingan Apple-to-Apple |
| **Rata-rata Rating Ulasan Bertulis** | **3.68 / 5.0** | **4.14 / 5.0** | Stockbit lebih disukai pengguna aktif |
| **Skor Normalisasi (0 - 100)** | **67.1 / 100** | **78.6 / 100** | Standardisasi skala kompetisi |
| **Positive Share (⭐ 4–5)** | 62.9% (825 ulasan) | **77.9%** (1,022 ulasan) | Kepuasan pengguna Stockbit lebih dominan |
| **Negative Share (⭐ 1–2)** | **28.4%** (Tinggi / Rentan) | **18.6%** (Rendah) | Friksi teknis TRIMA jauh lebih tinggi (+9.8%) |
| **Developer Response Rate** | 48.0% | 99.9% | Responsivitas CS dalam menanggapi review |

---

## 3. Komparasi Root Cause Masalah (Ulasan Negatif ⭐ 1–2)

### Top 5 Masalah TRIMA+ (372 Keluhan):
1. **Keluhan Umum Aplikasi**: 121 keluhan (32.5%)
2. **Login & Autentikasi**: 98 keluhan (26.3%)
3. **UI/UX & Performa (Loading/Navigasi)**: 58 keluhan (15.6%)
4. **Transaksi & Portofolio Saham**: 34 keluhan (9.1%)
5. **Stabilitas Sistem & Bug (Crash/Error)**: 22 keluhan (5.9%)

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
