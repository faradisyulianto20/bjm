# LAPORAN ANALISIS BISNIS & ULASAN PENGGUNA TRIMA+
**Studi Kasus:** Evaluasi Pengalaman Pengguna & Kepuasan Aplikasi Trima+ (PT Trimegah Sekuritas Indonesia Tbk)  
**Tujuan Dokumen:** Bahan Analisis Business Case Competition & Rekomendasi Solusi Strategis  
**Tanggal Pengambilan Data:** 2026-09-26 00:43:31  
**Lingkup Pengambilan Data:** Sampel Publik Google Play Store (hl=id, gl=ID)  

---

## 1. Executive Summary & Metrik Kunci

Tabel berikut memisahkan antara metrik agregat Google Play Store dengan review bertulis yang sebenarnya dianalisis untuk mencegah bias interpretasi:

| Indikator Metrik | Nilai Temuan | Keterangan & Konteks Bisnis |
| :--- | :--- | :--- |
| **Total Rating Google Play** | **2,171 rating** | Angka publik yang ditampilkan toko aplikasi |
| **Total Ulasan Ditampilkan Play Store** | **1,956 ulasan** | Estimasi total ulasan (termasuk tanpa teks) |
| **Sampel Review Bertulis Dianalisis (N)** | **1,312 ulasan** | Seluruh ulasan publik dengan teks yang dapat ditarik |
| **Rata-rata Rating Resmi Play Store** | **4.61 / 5.0** | Rating rata-rata kumulatif aplikasi |
| **Rata-rata Rating Review Bertulis** | **4.53 / 5.0** | Rata-rata dari pengguna yang bersedia menulis feedback |
| **Median Rating** | **5.0 / 5.0** | Nilai tengah distribusi kepuasan |
| **Skor Normalisasi (0.00 – 1.00)** | **0.8813** | Rumus: `(stars - 1) / 4` |
| **Skor Normalisasi (0 – 100)** | **88.1 / 100** | Rumus: `(stars - 1) * 25` |
| **Positive Share (Bintang 4–5)** | **87.1% (1,143 ulasan)** | Basis pengguna loyal & puas |
| **Neutral Share (Bintang 3)** | **1.9% (25 ulasan)** | Pengguna yang menghadapi friksi minor |
| **Negative Share (Bintang 1–2)** | **11.0% (144 ulasan)** | **Area friksi kritis yang membutuhkan intervensi bisnis** |
| **Developer Response Rate** | **2.7%** | Tingkat keterlibatan CS pengembang dalam membalas |

---

## 2. Distribusi Bintang Asli vs Skor Normalisasi

Sesuai metodologi yang tepat: **Distribusi asli bintang 5 tetap dipertahankan sebagai temuan objektif** dan tidak diratakan secara artifisial.

| Bintang Asli | Jumlah Ulasan | Persentase | Skor Normalisasi (0–1) | Skor Normalisasi (0–100) | Kategori Sentimen |
| :---: | :---: | :---: | :---: | :---: | :---: |
| ⭐ 5 | 1,124 | 85.7% | 1.00 | 100.0 | Positif Kuat |
| ⭐ 4 | 19 | 1.4% | 0.75 | 75.0 | Positif |
| ⭐ 3 | 25 | 1.9% | 0.50 | 50.0 | Netral / Friksi Ringan |
| ⭐ 2 | 22 | 1.7% | 0.25 | 25.0 | Negatif Ringan |
| ⭐ 1 | 122 | 9.3% | 0.00 | 0.0 | **Negatif Berat / Churn Risk** |

### Temuan Kritis Distribusi:
- Terdapat **polarisasi berbentuk bimodal** (bintang 5 tinggi, namun bintang 1 juga signifikan mencapai 9.3%).
- Ini menunjukkan bahwa aplikasi Trima+ memiliki basis pengguna setia yang menyukai fitur riset dan kestabilan regulernya, **tetapi pengguna yang mengalami isu teknis langsung mengalami kegagalan fatal** (churn/drop-off), bukan sekadar penurunan kepuasan minor.

---

## 3. Analisis Masalah Utama (Root Cause Ulasan Negatif Bintang 1–2)

Dari total **144 ulasan negatif**, berikut adalah kluster masalah utama yang dihadapi pengguna:

1. **Login & Autentikasi**: 42 keluhan (29.2% dari ulasan negatif)
2. **Transaksi & Portofolio Saham**: 37 keluhan (25.7% dari ulasan negatif)
3. **Keluhan Umum Aplikasi**: 23 keluhan (16.0% dari ulasan negatif)
4. **Stabilitas Sistem & Bug (Crash/Error)**: 12 keluhan (8.3% dari ulasan negatif)
5. **UI/UX & Performa (Loading/Navigasi)**: 10 keluhan (6.9% dari ulasan negatif)

### Analisis Mendalam Per Topik:
1. **Login & Autentikasi**:
   - *Keluhan berulang:* Sering logout otomatis, kegagalan pengiriman OTP via SMS/email, tombol biometrik (sidik jari/Face ID) tidak tersinkronisasi setelah pembaruan versi.
   - *Dampak Bisnis:* Friksi di pintu masuk mengakibatkan penurunan *Daily Active Users (DAU)* dan hilangnya momen transaksi pada jam pembukaan bursa (09:00 WIB).

2. **Stabilitas Sistem (Crash & Blank Screen)**:
   - *Keluhan berulang:* Layar blank putih saat market ramai (jam sibuk/volatilitas tinggi), aplikasi menutup sendiri (*force close*) saat membuka grafik saham.
   - *Dampak Bisnis:* Menimbulkan ketidakpercayaan tinggi (*loss of trust*) karena investor ritel berpotensi mengalami kerugian finansial akibat order yang terlambat.

3. **UI/UX & Kecepatan Loading**:
   - *Keluhan berulang:* Transisi antar tab terasa berat (*lag*), navigasi order book kurang responsif dibandingkan aplikasi sekuritas kompetitor baru.

4. **Customer Support & Service SLA**:
   - *Keluhan berulang:* Lambatnya respon tiket bantuan saat terjadi kendala akun atau verifikasi RDN.

---

## 4. Rekomendasi Strategis untuk Business Case Competition

Berdasarkan temuan data review di atas, rekomendasi bisnis yang dapat diajukan kepada dewan juri meliputi 4 pilar strategi:

### A. Pilar Keandalan Teknis & Infrastruktur (Reliability First)
- **High-Concurrency Order Matching Engine**: Optimasi infrastruktur server cloud autoscale saat jam bursa buka (08:50 – 09:15 WIB) untuk mengeliminasi keluhan *force close* saat volatilitas tinggi.
- **Biometric Token Refreshing**: Perbaiki alur refresh token sesi agar nasabah tidak terlempar keluar (*session expired*) secara tiba-tiba saat sedang memantau order book.

### B. Pilar UX & Modernisasi Antarmuka
- **Fast-Order Entry Feature**: Tambahkan antarmuka transaksi saham kilat (1-click order / swipe to buy) untuk mengatasi keluhan navigasi yang dinilai nasabah ritel terlalu berbelit.
- **Responsive Mobile Charting**: Integrasi library chart ringan (misal TradingView mobile lightweight) agar tidak memberatkan memori RAM ponsel low-to-mid range.

### C. Pilar Customer Experience & Retensi Nasabah
- **In-App Real-time Ticketing**: Buat fitur *live chat in-app* langsung ke tim helpdesk Trimegah dengan SLA penyelesaian maksimal 15 menit untuk kendala trading darurat.
- **Proactive Notification on Downtime**: Notifikasi transparan via push message saat server bursa/aplikasi sedang maintenance berkala, sehingga nasabah tidak mengira akun mereka bermasalah.

---

## 5. Batasan Metodologi (Limitations to Declare in Report)

Untuk menjaga integritas ilmiah dan nilai akademis di hadapan dewan juri lomba, sertakan klausul batasan berikut dalam laporan:

1. **Sumber Data:** Data bersumber dari ulasan publik yang terlihat di Google Play Store (hl=id, gl=ID) pada tanggal pengambilan data.
2. **Representasi Sampel:** Analisis dilakukan terhadap **1,312 ulasan bertulis yang tersedia**, bukan terhadap seluruh 2,171 rating (karena sebagian besar rating diberikan pengguna tanpa menuliskan teks penjelasan).
3. **Data Privacy by Design:** Demi mematuhi etika riset bisnis dan regulasi pelindungan data pribadi (UU PDP No. 27/2022), seluruh identitas pengguna (nama, foto profil, user ID) tidak diekstrak atau diikutsertakan dalam pemrosesan data.
4. **Potensi Seleksi Diri (Self-Selection Bias):** Ulasan publik di Play Store cenderung mencerminkan dua kutub ekstrem (pengguna yang sangat puas atau nasabah yang sangat kecewa ketika terjadi kendala teknis).
