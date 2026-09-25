# Trima+ Review Analytics & Business Case Dashboard
Studi Kasus Analisis Ulasan Pengguna Aplikasi Mobile Trima+ (PT Trimegah Sekuritas Indonesia Tbk) untuk Business Case Competition.

🌐 **Akses Live Dashboard:** [https://faradisyulianto20.github.io/bjm/](https://faradisyulianto20.github.io/bjm/)

---

## 📌 Ringkasan Proyek
Proyek ini mengintegrasikan seluruh siklus analitika ulasan aplikasi Google Play Store:
1. **Data Ingestion (Scraping):** Menyerap ulasan publik bertulis terbaru (Sort.NEWEST) untuk aplikasi **Trima+** (`id.trimegah.tplus.android`) dan **Stockbit** (`com.stockbit.android`) per **September 2026**.
2. **Kepatuhan Privasi Data (UU PDP No. 27/2022):** Seluruh nama pengguna, avatar profil, dan identitas nasabah disanitasi secara ketat (*Privacy by Design*).
3. **Data Freshness & Kronologis:** Dataset ulasan diurutkan dari yang **TERBARU ke yang TERLAMA** (*Monotonic Decreasing*), mencakup pembaruan sistem dan rilis fitur paling relevan.
4. **Interactive Dual-App Web Dashboard with Compare Mode:** Antarmuka web modern (Tailwind CSS + Chart.js) dengan fitur tab switching (Trima+, Stockbit, dan Mode Komparasi Head-to-Head), pencarian kata kunci real-time dengan highlight teks, dan multi-filtering.
5. **Benchmark Komparasi Sekuritas:** Membedah keunggulan dan titik friksi kedua aplikasi (Login & Autentikasi, Transaksi, Riset/Chartbit, Customer Service SLA).

---

## 📊 Metrik Kunci (Ulasan Terbaru September 2026)
| Metrik Analitika | Trima+ (Trimegah Sekuritas) | Stockbit (Stockbit Digital) |
| :--- | :--- | :--- |
| **Rating Toko Aplikasi** | **4.61 / 5.0** (2.171 Rating) | **4.74 / 5.0** (74.509 Rating) |
| **Sampel Ulasan Bertulis (N)** | **1.312 ulasan terbaru** | **1.312 ulasan terbaru** |
| **Rata-rata Rating Ulasan Bertulis** | **4.53 / 5.0** | **4.14 / 5.0** |
| **Positive Share (⭐ 4–5)** | **87.1%** (1.143 ulasan) | **77.9%** (1.022 ulasan) |
| **Negative Share (⭐ 1–2)** | **11.0%** (144 ulasan) | **18.6%** (244 ulasan) |
| **Developer Response Rate** | **2.7%** (36 dibalas) | **99.9%** (1.311 dibalas) |
| **Rentang Ulasan** | Sep 2026 s/d Jul 2025 | Sep 2026 s/d Apr 2026 |

---

## 📂 Struktur Berkas
- `index.html` / `dashboard.html`: Live interactive web dashboard (didukung GitHub Pages).
- `analisis_ulasan_trima.ipynb`: Jupyter Notebook 33 sel komprehensif.
- `pipeline.py`: Skrip otomatisasi scraping, cleaning, dan visualisasi TRIMA+.
- `pipeline_stockbit.py`: Skrip benchmarking ulasan terbaru Stockbit (1.312 ulasan terbaru & perbandingan komparatif).
- `update_excel.py`: Skrip penambahan tab ulasan per topik terurut kronologis terbaru.
- `output/trima_reviews_clean.csv` & `output/trima_reviews_analysis.xlsx`: Dataset bersih dan Excel multi-sheet TRIMA+.
- `output/stockbit_reviews_clean.csv` & `output/stockbit_reviews_analysis.xlsx`: Dataset bersih dan Excel multi-sheet ulasan terbaru Stockbit.
- `output/charts/`: Grafik visualisasi 300 DPI (distribusi bintang, sentimen, topik keluhan, dan komparasi TRIMA vs Stockbit).
- `output/LAPORAN_ANALISIS_BISNIS_TRIMA.md`: Naskah laporan eksekutif TRIMA+.
- `output/LAPORAN_ANALISIS_BISNIS_STOCKBIT.md`: Naskah laporan komparasi benchmark TRIMA+ vs Stockbit.

---

## 🚀 Cara Menjalankan Secara Lokal
```bash
# Aktifkan virtual environment
.venv\Scripts\activate

# Jalankan pipeline pembaruan data
python pipeline.py

# Buka dashboard secara lokal
python -m http.server 8000
```
Buka browser di `http://localhost:8000/`
