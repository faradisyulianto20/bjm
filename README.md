# Trima+ Review Analytics & Business Case Dashboard
Studi Kasus Analisis Ulasan Pengguna Aplikasi Mobile Trima+ (PT Trimegah Sekuritas Indonesia Tbk) untuk Business Case Competition.

🌐 **Akses Live Dashboard:** [https://faradisyulianto20.github.io/bjm/](https://faradisyulianto20.github.io/bjm/)

---

## 📌 Ringkasan Proyek
Proyek ini mengintegrasikan seluruh siklus analitika ulasan aplikasi Google Play Store:
1. **Data Ingestion (Scraping):** Menyerap 1.312 ulasan bertulis publik (100% dari ulasan bertulis yang tersedia di Google Play Store region Indonesia `hl=id, gl=ID`).
2. **Kepatuhan Privasi Data (UU PDP No. 27/2022):** Seluruh nama pengguna, avatar profil, dan identitas nasabah disanitasi secara ketat.
3. **Normalisasi Skor Objektif:** Mempertahankan tingginya proporsi bintang 5 (55,3%) sebagai temuan empiris otentik serta menstandardisasi skala 0–1 dan 0–100.
4. **Root Cause Analysis Ulasan Negatif:** Membedah 372 keluhan nasabah (bintang 1–2) ke dalam 8 kluster masalah teknis dan operasional.
5. **Interactive Single-File Web Dashboard:** Antarmuka web ringan (Tailwind CSS + Chart.js) dengan pencarian kata kunci real-time dan multi-filtering.
6. **Jupyter Notebook Lengkap:** File analisis terpadu dengan penjelasan narasi, tabel metrik, dan grafik visualisasi.

---

## 📊 Metrik Kunci
- **Total Rating Google Play:** 3.747 rating (Skor rata-rata: 3.12 / 5.0)
- **Total Ulasan Bertulis Dianalisis (N):** 1.312 ulasan (Skor rata-rata: 3.68 / 5.0 | Median: 5.0)
- **Positive Share (⭐ 4–5):** 62,9% (825 ulasan)
- **Neutral Share (⭐ 3):** 8,8% (115 ulasan)
- **Negative Share (⭐ 1–2):** 28,4% (372 ulasan) — *Area Friksi Kritis*
- **Developer Response Rate:** 48,0% (630 ulasan dibalas tim CS Trimegah)

---

## 📂 Struktur Berkas
- `index.html` / `dashboard.html`: Live interactive web dashboard (didukung GitHub Pages).
- `analisis_ulasan_trima.ipynb`: Jupyter Notebook 33 sel komprehensif.
- `pipeline.py`: Skrip otomatisasi scraping, cleaning, dan visualisasi.
- `output/trima_reviews_analysis.xlsx`: Spreadsheet multi-sheet dengan tab per kategori masalah.
- `output/trima_reviews_clean.csv`: Dataset ulasan bersih siap olah.
- `output/charts/`: Grafik visualisasi 300 DPI (`rating_distribution.png`, `negative_topic_breakdown.png`, dll.).
- `output/LAPORAN_ANALISIS_BISNIS_TRIMA.md`: Naskah laporan eksekutif lengkap.

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
