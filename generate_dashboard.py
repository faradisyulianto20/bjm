"""
Generate interactive dual-app web dashboard with comparison mode:
Trima+ vs Stockbit (Sep 2026 Data)
Output: dashboard.html & index.html
"""

import json
import os
import pandas as pd

def build_dashboard():
    # 1. Muat dataset TRIMA+ terbaru
    trima_csv = "output/trima_reviews_clean_latest.csv"
    if not os.path.exists(trima_csv):
        trima_csv = "output/trima_reviews_clean.csv"
    df_tr = pd.read_csv(trima_csv)
    
    # 2. Muat dataset Stockbit terbaru
    sb_csv = "output/stockbit_reviews_clean.csv"
    df_sb = pd.read_csv(sb_csv)
    
    # Helper record extractor
    def extract_records(df):
        records = []
        for _, r in df.iterrows():
            date_val = str(r["review_date"]).replace("T", " ")
            records.append({
                "id": str(r["review_id"]),
                "stars": int(r["stars"]),
                "sentiment": str(r["sentiment"]),
                "topic": str(r["primary_topic"]),
                "date": date_val,
                "year": str(r["review_year"]),
                "text": str(r["clean_text"]) if pd.notna(r["clean_text"]) else "",
                "version": str(r["app_version"]) if pd.notna(r["app_version"]) else "Tidak Tercatat",
                "helpful": int(r["helpful_count"]) if pd.notna(r["helpful_count"]) else 0,
                "has_reply": str(r["has_developer_reply"]) == "Ya",
                "reply": str(r["developer_reply"]) if pd.notna(r["developer_reply"]) and str(r["developer_reply"]) != "nan" else "",
                "replied_at": str(r["replied_at"]).replace("T", " ") if pd.notna(r["replied_at"]) and str(r["replied_at"]) != "nan" else ""
            })
        return records

    trima_data = extract_records(df_tr)
    stockbit_data = extract_records(df_sb)
    
    app_meta_info = {
        "trima": {
            "title": "Trima+",
            "developer": "PT Trimegah Sekuritas Indonesia Tbk",
            "app_id": "id.trimegah.tplus.android",
            "store_score": 4.61,
            "total_ratings": 2171,
            "total_reviews": 1956,
            "sample_count": len(df_tr),
            "date_range": f"{df_tr['review_date'].iloc[-1][:10]} s/d {df_tr['review_date'].iloc[0][:10]}",
            "avg_sample_score": round(df_tr['stars'].mean(), 2),
            "positive_share": round((df_tr['stars'] >= 4).mean() * 100, 1),
            "negative_share": round((df_tr['stars'] <= 2).mean() * 100, 1),
            "reply_rate": round((df_tr['has_developer_reply'] == 'Ya').mean() * 100, 1)
        },
        "stockbit": {
            "title": "Stockbit - Investasi Saham",
            "developer": "PT Stockbit Sekuritas Digital",
            "app_id": "com.stockbit.android",
            "store_score": 4.74,
            "total_ratings": 74509,
            "total_reviews": 27133,
            "sample_count": len(df_sb),
            "date_range": f"{df_sb['review_date'].iloc[-1][:10]} s/d {df_sb['review_date'].iloc[0][:10]}",
            "avg_sample_score": round(df_sb['stars'].mean(), 2),
            "positive_share": round((df_sb['stars'] >= 4).mean() * 100, 1),
            "negative_share": round((df_sb['stars'] <= 2).mean() * 100, 1),
            "reply_rate": round((df_sb['has_developer_reply'] == 'Ya').mean() * 100, 1)
        }
    }
    
    trima_json = json.dumps(trima_data, ensure_ascii=False)
    stockbit_json = json.dumps(stockbit_data, ensure_ascii=False)
    meta_json = json.dumps(app_meta_info, ensure_ascii=False)

    html_template = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Analisis Ulasan: Trima+ vs Stockbit</title>
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js via CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .badge-star-1, .badge-star-2 { background-color: #fee2e2; color: #dc2626; border-color: #fca5a5; }
    .badge-star-3 { background-color: #fef3c7; color: #d97706; border-color: #fcd34d; }
    .badge-star-4, .badge-star-5 { background-color: #dcfce7; color: #16a34a; border-color: #86efac; }
    .highlight { background-color: #fef08a; font-weight: 600; padding: 0 2px; border-radius: 2px; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen">

  <!-- Top Navbar -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <div id="appLogoBadge" class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow transition-colors">
          T+
        </div>
        <div>
          <h1 id="appHeaderTitle" class="text-lg font-bold text-slate-900 leading-tight">Dashboard Analisis Ulasan: Trima+</h1>
          <p id="appHeaderSubtitle" class="text-xs text-slate-500">PT Trimegah Sekuritas Indonesia Tbk &bull; Data Terbaru Play Store</p>
        </div>
      </div>

      <!-- Navigation & Mode Tabs -->
      <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
        <button id="tabTrima" class="px-3.5 py-1.5 rounded-lg transition-all bg-white text-blue-700 shadow-sm font-bold flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-blue-600"></span>
          Trima+ (Sep 2026)
        </button>
        <button id="tabStockbit" class="px-3.5 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          Stockbit (Sep 2026)
        </button>
        <button id="tabCompare" class="px-3.5 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5 ml-1">
          ⚖️ Compare Mode
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- ==================== COMPARE MODE VIEW ==================== -->
    <div id="compareView" class="hidden space-y-6">
      
      <!-- Compare Banner -->
      <div class="bg-gradient-to-r from-blue-700 via-indigo-700 to-emerald-700 rounded-2xl p-6 text-white shadow-md">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-white/20 text-white backdrop-blur mb-2">
              BENCHMARK KOMPARATIF SEKURITAS DIGITAL
            </span>
            <h2 class="text-2xl font-black tracking-tight">Trima+ (Trimegah) vs Stockbit (Stockbit Digital)</h2>
            <p class="text-sm text-blue-100 mt-1">Perbandingan objektif 1.312 ulasan terbaru per September 2026 (Format Apple-to-Apple)</p>
          </div>
          <div class="flex items-center gap-3 text-xs bg-black/20 px-3.5 py-2 rounded-xl backdrop-blur">
            <div>
              <div class="text-slate-300">Data Freshness</div>
              <div class="font-bold text-white">Sep 2026 (Live)</div>
            </div>
            <div class="h-6 w-px bg-white/20"></div>
            <div>
              <div class="text-slate-300">Total Sampel</div>
              <div class="font-bold text-white">2.624 Review</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Head-to-Head KPI Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <!-- Card 1: Official Play Store Score -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rating Toko Resmi</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-slate-900">4.61 / 5.0</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-slate-900">4.74 / 5.0</span>
            </div>
          </div>
        </div>

        <!-- Card 2: Total Play Store Ratings -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Rating Masuk</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-slate-900">2.171</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-slate-900">74.509</span>
            </div>
          </div>
        </div>

        <!-- Card 3: Sample Text Review Rating -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rata-rata Review Teks</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-blue-600">4.53 / 5.0</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-emerald-600">4.14 / 5.0</span>
            </div>
          </div>
        </div>

        <!-- Card 4: Positive Share -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Positive Share (★4-5)</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-emerald-600">87.1%</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-emerald-600">77.9%</span>
            </div>
          </div>
        </div>

        <!-- Card 5: Negative Share -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-rose-600 uppercase tracking-wider">Negative Share (★1-2)</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-rose-600">11.0%</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-rose-600">18.6%</span>
            </div>
          </div>
        </div>

        <!-- Card 6: Dev Response Rate -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-purple-600 uppercase tracking-wider">Tingkat Balas CS</div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-blue-700">Trima+</span>
              <span class="font-bold text-purple-600">2.7%</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="font-medium text-emerald-700">Stockbit</span>
              <span class="font-bold text-purple-600">99.9%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Comparative Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Compare Chart 1: Star Rating Distribution -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-sm font-bold text-slate-800">Komparasi Distribusi Bintang (%)</h3>
              <p class="text-xs text-slate-500">Persentase ulasan per bintang rating (1 s/d 5)</p>
            </div>
            <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">Apple-to-Apple</span>
          </div>
          <div class="h-64">
            <canvas id="chartCompareStars"></canvas>
          </div>
        </div>

        <!-- Compare Chart 2: Sentiment Comparison -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-sm font-bold text-slate-800">Komparasi Proporsi Sentimen (%)</h3>
              <p class="text-xs text-slate-500">Positif (★4-5), Netral (★3), Negatif (★1-2)</p>
            </div>
            <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">N = 1.312 per app</span>
          </div>
          <div class="h-64">
            <canvas id="chartCompareSentiment"></canvas>
          </div>
        </div>
      </div>

      <!-- Compare Chart 3: Top Negative Complaints Comparison -->
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-sm font-bold text-slate-800">Komparasi Kluster Masalah Negatif (Bintang 1-2)</h3>
            <p class="text-xs text-slate-500">Perbandingan jumlah keluhan per topik teknis dan operasional</p>
          </div>
          <span class="text-xs bg-rose-100 text-rose-700 px-2 py-0.5 rounded font-semibold">Area Friksi Nasabah</span>
        </div>
        <div class="h-72">
          <canvas id="chartCompareComplaints"></canvas>
        </div>
      </div>

      <!-- Strategic Takeaways Table -->
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 class="text-base font-bold text-slate-900 mb-4">Matriks Analisis Kesenjangan & Rekomendasi Bisnis Kompetisi</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border border-slate-200 rounded-lg">
            <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th class="p-3">Dimensi Produk</th>
                <th class="p-3 text-blue-700">Trima+ (Temuan Terkini)</th>
                <th class="p-3 text-emerald-700">Stockbit (Temuan Terkini)</th>
                <th class="p-3 text-slate-800">Rekomendasi Solusi Strategis untuk Trimegah</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr class="hover:bg-slate-50">
                <td class="p-3 font-semibold text-slate-900">Login & Autentikasi</td>
                <td class="p-3">Keluhan terbesar (29.2% ulasan negatif), kendala login ulang dan biometrik</td>
                <td class="p-3">Masih ditemukan kendala login (27.0%), namun direspon cepat oleh CS</td>
                <td class="p-3 text-slate-700">Terapkan <em>Biometric Session Refresh Token</em> agar user tidak perlu relogin saat market buka.</td>
              </tr>
              <tr class="hover:bg-slate-50">
                <td class="p-3 font-semibold text-slate-900">Transaksi & Portofolio</td>
                <td class="p-3">25.7% keluhan pada antrian order, penarikan dana RDN, dan sinkronisasi saldo</td>
                <td class="p-3">20.9% keluhan pada jeda penarikan dana RDN dan konfirmasi lot</td>
                <td class="p-3 text-slate-700">Otomasi penarikan dana instan (Instant Withdrawal) dan realtime balance sync.</td>
              </tr>
              <tr class="hover:bg-slate-50">
                <td class="p-3 font-semibold text-slate-900">Layanan Customer Care</td>
                <td class="p-3 text-rose-600 font-medium">Hanya membalas 2.7% ulasan di Play Store (Sangat pasif)</td>
                <td class="p-3 text-emerald-600 font-bold">Membalas 99.9% ulasan secara personal & tanggap</td>
                <td class="p-3 text-slate-700">Bentuk dedicated Play Store Support Desk dengan target SLA respon &lt; 2 jam.</td>
              </tr>
              <tr class="hover:bg-slate-50">
                <td class="p-3 font-semibold text-slate-900">Komunitas & Fitur Analitik</td>
                <td class="p-3">Unggul pada Trima Picks & riset emiten, namun minim aspek interaksi sosial</td>
                <td class="p-3">Sangat kuat pada Stream sosial, Chartbit terintegrasi, dan Bandarmology</td>
                <td class="p-3 text-slate-700">Integrasikan Trima Social Forum untuk diskusi ide trading nasabah ritel.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ==================== SINGLE APP VIEW (TRIMA+ / STOCKBIT) ==================== -->
    <div id="singleAppView" class="space-y-6">

      <!-- KPI Metric Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rating Toko Resmi</div>
          <div id="kpiStoreScore" class="text-2xl font-bold text-slate-900 mt-1">4.61 <span class="text-xs font-normal text-slate-400">/ 5.0</span></div>
          <div id="kpiTotalRatings" class="text-xs text-slate-400 mt-1">2.171 total rating</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rata-rata Review Teks</div>
          <div id="kpiSampleAvg" class="text-2xl font-bold text-blue-600 mt-1">4.53 <span class="text-xs font-normal text-slate-400">/ 5.0</span></div>
          <div id="kpiSampleSize" class="text-xs text-slate-400 mt-1">Sampel 1.312 ulasan</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Positive Share (★4-5)</div>
          <div id="kpiPosShare" class="text-2xl font-bold text-emerald-600 mt-1">87.1%</div>
          <div id="kpiPosCount" class="text-xs text-slate-400 mt-1">1.143 ulasan puas</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-rose-600 uppercase tracking-wider">Negative Share (★1-2)</div>
          <div id="kpiNegShare" class="text-2xl font-bold text-rose-600 mt-1">11.0%</div>
          <div id="kpiNegCount" class="text-xs text-slate-400 mt-1">144 titik friksi</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-purple-600 uppercase tracking-wider">Respon Developer</div>
          <div id="kpiReplyRate" class="text-2xl font-bold text-purple-600 mt-1">2.7%</div>
          <div id="kpiReplyCount" class="text-xs text-slate-400 mt-1">36 ulasan dibalas</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rentang Waktu Ulasan</div>
          <div id="kpiDateRange" class="text-xs font-bold text-slate-800 mt-2">Sep 2026 s/d Jul 2025</div>
          <div class="text-xs text-emerald-600 font-semibold mt-1">Terurut: Terbaru &rarr; Terlama</div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Chart 1: Distribusi Bintang -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 id="chartStarsTitle" class="text-sm font-bold text-slate-800">Distribusi Rating Bintang Asli (1 - 5)</h2>
            <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">Bintang Asli</span>
          </div>
          <div class="h-64">
            <canvas id="chartStars"></canvas>
          </div>
        </div>

        <!-- Chart 2: Root Cause Ulasan Negatif -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 id="chartComplaintsTitle" class="text-sm font-bold text-slate-800">Root Cause Keluhan Negatif (Bintang 1 - 2)</h2>
            <span id="badgeNegCount" class="text-xs bg-rose-100 text-rose-700 px-2 py-0.5 rounded font-semibold">N = 144</span>
          </div>
          <div class="h-64">
            <canvas id="chartComplaints"></canvas>
          </div>
        </div>
      </div>

      <!-- Filter & Search Controls Bar -->
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          
          <!-- Live Search -->
          <div class="relative flex-1">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <input 
              type="text" 
              id="searchInput"
              placeholder="Cari kata kunci: misal 'login', 'tarik', 'otp', 'biometrik', 'loading', 'chart', 'dana'..." 
              class="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <!-- Filter Topic Dropdown -->
          <div class="w-full md:w-72">
            <select id="topicFilter" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="ALL">Semua Topik Analisis</option>
            </select>
          </div>

          <!-- Sort Order Dropdown -->
          <div class="w-full md:w-56">
            <select id="sortFilter" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium">
              <option value="date_desc">📅 Terbaru &rarr; Terlama (Relevan)</option>
              <option value="date_asc">📅 Terlama &rarr; Terbaru</option>
              <option value="stars_desc">⭐ Rating Tertinggi (5 ke 1)</option>
              <option value="stars_asc">⭐ Rating Terendah (1 ke 5)</option>
              <option value="helpful_desc">👍 Paling Membantu</option>
            </select>
          </div>

          <!-- Developer Reply Filter -->
          <div class="w-full md:w-48">
            <select id="replyFilter" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="ALL">Semua Status CS</option>
              <option value="WITH_REPLY">Dibalas Pengembang</option>
              <option value="WITHOUT_REPLY">Tanpa Balasan</option>
            </select>
          </div>

          <!-- Reset Button -->
          <button id="resetBtn" class="px-4 py-2 border border-slate-300 hover:bg-slate-100 rounded-lg text-sm font-medium text-slate-600 transition-colors whitespace-nowrap">
            Reset Filter
          </button>
        </div>

        <!-- Star Quick Filters -->
        <div class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100 text-xs">
          <span class="text-slate-400 font-medium mr-1">Filter Bintang:</span>
          <button data-star="ALL" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-blue-600 text-white border-blue-600">Semua</button>
          <button data-star="5" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200">⭐ 5 Bintang</button>
          <button data-star="4" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200">⭐ 4 Bintang</button>
          <button data-star="3" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200">⭐ 3 Bintang</button>
          <button data-star="2" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200">⭐ 2 Bintang</button>
          <button data-star="1" class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200">⭐ 1 Bintang</button>
        </div>
      </div>

      <!-- Feed Status & Active Filter Summary -->
      <div class="flex items-center justify-between text-xs text-slate-500 px-1">
        <div>
          Menampilkan <span id="filteredCount" class="font-bold text-slate-900">0</span> ulasan dari total <span id="totalCount" class="font-bold text-slate-900">1.312</span>
        </div>
        <div id="activeSortLabel" class="text-blue-600 font-medium">
          Urutan: Terbaru ke Terlama (Paling Relevan)
        </div>
      </div>

      <!-- Review Cards Feed -->
      <div id="reviewsFeed" class="space-y-3">
        <!-- Rendered via JS -->
      </div>

      <!-- Load More Button -->
      <div class="text-center pt-2 pb-6">
        <button id="loadMoreBtn" class="px-6 py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-xl text-sm shadow-sm transition-all hidden">
          Muat 25 Ulasan Berikutnya...
        </button>
      </div>

    </div>

  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-6 mt-12 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 space-y-2">
      <p class="font-semibold text-slate-700">Analisis Ulasan Publik Play Store &bull; Trima+ vs Stockbit</p>
      <p>Data Privacy by Design: Nama pengguna dan avatar disanitasi penuh demi kepatuhan UU PDP No. 27/2022.</p>
    </div>
  </footer>

  <!-- Application Logic -->
  <script>
    // Embedded Datasets
    const trimaData = /* TRIMA_DATA_PLACEHOLDER */;
    const stockbitData = /* STOCKBIT_DATA_PLACEHOLDER */;
    const metaInfo = /* META_PLACEHOLDER */;

    // State
    let currentApp = "trima"; // 'trima', 'stockbit', or 'compare'
    let currentData = trimaData;
    let filteredData = [];
    let displayLimit = 25;

    let currentSearchTerm = "";
    let currentTopicFilter = "ALL";
    let currentStarFilter = "ALL";
    let currentReplyFilter = "ALL";
    let currentSort = "date_desc";

    // Charts instances
    let chartStarsInst = null;
    let chartComplaintsInst = null;
    let chartCompareStarsInst = null;
    let chartCompareSentimentInst = null;
    let chartCompareComplaintsInst = null;

    // DOM Elements
    const tabTrima = document.getElementById("tabTrima");
    const tabStockbit = document.getElementById("tabStockbit");
    const tabCompare = document.getElementById("tabCompare");
    const compareView = document.getElementById("compareView");
    const singleAppView = document.getElementById("singleAppView");

    const appLogoBadge = document.getElementById("appLogoBadge");
    const appHeaderTitle = document.getElementById("appHeaderTitle");
    const appHeaderSubtitle = document.getElementById("appHeaderSubtitle");

    const searchInput = document.getElementById("searchInput");
    const topicFilter = document.getElementById("topicFilter");
    const sortFilter = document.getElementById("sortFilter");
    const replyFilter = document.getElementById("replyFilter");
    const resetBtn = document.getElementById("resetBtn");
    const starBtns = document.querySelectorAll(".star-btn");
    const reviewsFeed = document.getElementById("reviewsFeed");
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    const filteredCount = document.getElementById("filteredCount");
    const totalCount = document.getElementById("totalCount");
    const activeSortLabel = document.getElementById("activeSortLabel");

    // Switch App Function
    function switchMode(mode) {
      currentApp = mode;

      // Update Navigation Tab Styles
      [tabTrima, tabStockbit, tabCompare].forEach(tab => {
        tab.className = "px-3.5 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5";
      });

      if (mode === "trima") {
        tabTrima.className = "px-3.5 py-1.5 rounded-lg transition-all bg-white text-blue-700 shadow-sm font-bold flex items-center gap-1.5";
        appLogoBadge.className = "w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow transition-colors";
        appLogoBadge.innerText = "T+";
        appHeaderTitle.innerText = "Dashboard Analisis Ulasan: Trima+";
        appHeaderSubtitle.innerText = "PT Trimegah Sekuritas Indonesia Tbk • Data Terbaru Play Store";
        compareView.classList.add("hidden");
        singleAppView.classList.remove("hidden");
        currentData = trimaData;
        populateTopicDropdown();
        updateKPIs();
        updateSingleAppCharts();
        applyFilters();
      } else if (mode === "stockbit") {
        tabStockbit.className = "px-3.5 py-1.5 rounded-lg transition-all bg-white text-emerald-700 shadow-sm font-bold flex items-center gap-1.5";
        appLogoBadge.className = "w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold text-xl shadow transition-colors";
        appLogoBadge.innerText = "SB";
        appHeaderTitle.innerText = "Dashboard Analisis Ulasan: Stockbit";
        appHeaderSubtitle.innerText = "PT Stockbit Sekuritas Digital • Data Terbaru Play Store";
        compareView.classList.add("hidden");
        singleAppView.classList.remove("hidden");
        currentData = stockbitData;
        populateTopicDropdown();
        updateKPIs();
        updateSingleAppCharts();
        applyFilters();
      } else if (mode === "compare") {
        tabCompare.className = "px-3.5 py-1.5 rounded-lg transition-all bg-white text-indigo-700 shadow-sm font-bold flex items-center gap-1.5 ml-1";
        appLogoBadge.className = "w-10 h-10 rounded-lg bg-gradient-to-r from-blue-600 to-emerald-600 flex items-center justify-center text-white font-bold text-base shadow transition-colors";
        appLogoBadge.innerText = "VS";
        appHeaderTitle.innerText = "Benchmark Komparasi: Trima+ vs Stockbit";
        appHeaderSubtitle.innerText = "Perbandingan Head-to-Head 1.312 Ulasan Terbaru Sep 2026";
        singleAppView.classList.add("hidden");
        compareView.classList.remove("hidden");
        updateCompareCharts();
      }
    }

    tabTrima.addEventListener("click", () => switchMode("trima"));
    tabStockbit.addEventListener("click", () => switchMode("stockbit"));
    tabCompare.addEventListener("click", () => switchMode("compare"));

    function populateTopicDropdown() {
      const topics = Array.from(new Set(currentData.map(d => d.topic))).filter(Boolean).sort();
      topicFilter.innerHTML = '<option value="ALL">Semua Topik Analisis</option>';
      topics.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.innerText = t;
        topicFilter.appendChild(opt);
      });
      topicFilter.value = "ALL";
      currentTopicFilter = "ALL";
    }

    function updateKPIs() {
      const meta = metaInfo[currentApp];
      if (!meta) return;

      document.getElementById("kpiStoreScore").innerHTML = `${meta.store_score.toFixed(2)} <span class="text-xs font-normal text-slate-400">/ 5.0</span>`;
      document.getElementById("kpiTotalRatings").innerText = `${meta.total_ratings.toLocaleString()} total rating`;

      document.getElementById("kpiSampleAvg").innerHTML = `${meta.avg_sample_score.toFixed(2)} <span class="text-xs font-normal text-slate-400">/ 5.0</span>`;
      document.getElementById("kpiSampleSize").innerText = `Sampel ${meta.sample_count.toLocaleString()} ulasan`;

      const posCnt = currentData.filter(d => d.stars >= 4).length;
      document.getElementById("kpiPosShare").innerText = `${meta.positive_share}%`;
      document.getElementById("kpiPosCount").innerText = `${posCnt.toLocaleString()} ulasan puas`;

      const negCnt = currentData.filter(d => d.stars <= 2).length;
      document.getElementById("kpiNegShare").innerText = `${meta.negative_share}%`;
      document.getElementById("kpiNegCount").innerText = `${negCnt.toLocaleString()} titik friksi`;

      const replyCnt = currentData.filter(d => d.has_reply).length;
      document.getElementById("kpiReplyRate").innerText = `${meta.reply_rate}%`;
      document.getElementById("kpiReplyCount").innerText = `${replyCnt.toLocaleString()} ulasan dibalas`;

      document.getElementById("kpiDateRange").innerText = meta.date_range;
      totalCount.innerText = currentData.length.toLocaleString();
    }

    function updateSingleAppCharts() {
      const isTrima = currentApp === "trima";
      const primaryCol = isTrima ? '#2563eb' : '#059669';

      // 1. Star Distribution
      const starCounts = [0, 0, 0, 0, 0];
      currentData.forEach(d => {
        if (d.stars >= 1 && d.stars <= 5) starCounts[d.stars - 1]++;
      });

      const starCtx = document.getElementById("chartStars").getContext("2d");
      if (chartStarsInst) chartStarsInst.destroy();

      chartStarsInst = new Chart(starCtx, {
        type: 'bar',
        data: {
          labels: ['⭐ 1 Bintang', '⭐ 2 Bintang', '⭐ 3 Bintang', '⭐ 4 Bintang', '⭐ 5 Bintang'],
          datasets: [{
            label: 'Jumlah Ulasan',
            data: starCounts,
            backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#16a34a'],
            borderRadius: 6,
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const val = ctx.raw;
                  const pct = ((val / currentData.length) * 100).toFixed(1);
                  return ` ${val.toLocaleString()} ulasan (${pct}%)`;
                }
              }
            }
          },
          scales: {
            y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
          }
        }
      });

      // 2. Complaints Distribution
      const negReviews = currentData.filter(d => d.stars <= 2);
      document.getElementById("badgeNegCount").innerText = `N = ${negReviews.length.toLocaleString()}`;
      
      const topicCountMap = {};
      negReviews.forEach(d => {
        topicCountMap[d.topic] = (topicCountMap[d.topic] || 0) + 1;
      });

      const sortedTopics = Object.entries(topicCountMap).sort((a, b) => b[1] - a[1]).slice(0, 6);
      const labels = sortedTopics.map(x => x[0]);
      const dataVals = sortedTopics.map(x => x[1]);

      const compCtx = document.getElementById("chartComplaints").getContext("2d");
      if (chartComplaintsInst) chartComplaintsInst.destroy();

      chartComplaintsInst = new Chart(compCtx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            axis: 'y',
            label: 'Jumlah Keluhan',
            data: dataVals,
            backgroundColor: '#ef4444',
            borderRadius: 6
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const val = ctx.raw;
                  const pct = negReviews.length ? ((val / negReviews.length) * 100).toFixed(1) : 0;
                  return ` ${val} keluhan (${pct}% dari isu negatif)`;
                }
              }
            }
          },
          scales: {
            x: { beginAtZero: true, grid: { color: '#f1f5f9' } },
            y: { grid: { display: false }, ticks: { font: { size: 11 } } }
          }
        }
      });
    }

    function updateCompareCharts() {
      // 1. Compare Stars
      const trimaStars = [0, 0, 0, 0, 0];
      const sbStars = [0, 0, 0, 0, 0];
      trimaData.forEach(d => { if (d.stars >= 1 && d.stars <= 5) trimaStars[d.stars - 1]++; });
      stockbitData.forEach(d => { if (d.stars >= 1 && d.stars <= 5) sbStars[d.stars - 1]++; });

      const trimaPct = trimaStars.map(v => ((v / trimaData.length) * 100).toFixed(1));
      const sbPct = sbStars.map(v => ((v / stockbitData.length) * 100).toFixed(1));

      const ctxC1 = document.getElementById("chartCompareStars").getContext("2d");
      if (chartCompareStarsInst) chartCompareStarsInst.destroy();

      chartCompareStarsInst = new Chart(ctxC1, {
        type: 'bar',
        data: {
          labels: ['⭐ 1 Bintang', '⭐ 2 Bintang', '⭐ 3 Bintang', '⭐ 4 Bintang', '⭐ 5 Bintang'],
          datasets: [
            { label: 'Trima+ (%)', data: trimaPct, backgroundColor: '#2563eb', borderRadius: 4 },
            { label: 'Stockbit (%)', data: sbPct, backgroundColor: '#10b981', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: { callbacks: { label: (c) => ` ${c.dataset.label}: ${c.raw}%` } }
          },
          scales: {
            y: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%' }, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
          }
        }
      });

      // 2. Compare Sentiment
      const getSentPct = (arr) => {
        const pos = (arr.filter(d => d.stars >= 4).length / arr.length * 100).toFixed(1);
        const neu = (arr.filter(d => d.stars === 3).length / arr.length * 100).toFixed(1);
        const neg = (arr.filter(d => d.stars <= 2).length / arr.length * 100).toFixed(1);
        return [pos, neu, neg];
      };

      const trimaSent = getSentPct(trimaData);
      const sbSent = getSentPct(stockbitData);

      const ctxC2 = document.getElementById("chartCompareSentiment").getContext("2d");
      if (chartCompareSentimentInst) chartCompareSentimentInst.destroy();

      chartCompareSentimentInst = new Chart(ctxC2, {
        type: 'bar',
        data: {
          labels: ['Positif (★4-5)', 'Netral (★3)', 'Negatif (★1-2)'],
          datasets: [
            { label: 'Trima+ (%)', data: trimaSent, backgroundColor: '#2563eb', borderRadius: 4 },
            { label: 'Stockbit (%)', data: sbSent, backgroundColor: '#10b981', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: { callbacks: { label: (c) => ` ${c.dataset.label}: ${c.raw}%` } }
          },
          scales: {
            y: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%' }, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
          }
        }
      });

      // 3. Compare Negative Complaints
      const countNegTopics = (arr) => {
        const m = {};
        arr.filter(d => d.stars <= 2).forEach(d => { m[d.topic] = (m[d.topic] || 0) + 1; });
        return m;
      };
      const trimaNegMap = countNegTopics(trimaData);
      const sbNegMap = countNegTopics(stockbitData);

      const allTopics = ['Login & Autentikasi', 'Transaksi & Portofolio Saham', 'Keluhan Umum Aplikasi', 'Stabilitas Sistem & Bug (Crash/Error)', 'UI/UX & Performa (Loading/Navigasi)', 'Customer Service & Layanan'];
      const trimaNegVals = allTopics.map(t => trimaNegMap[t] || 0);
      const sbNegVals = allTopics.map(t => sbNegMap[t] || 0);

      const ctxC3 = document.getElementById("chartCompareComplaints").getContext("2d");
      if (chartCompareComplaintsInst) chartCompareComplaintsInst.destroy();

      chartCompareComplaintsInst = new Chart(ctxC3, {
        type: 'bar',
        data: {
          labels: allTopics,
          datasets: [
            { label: 'Trima+ (Keluhan)', data: trimaNegVals, backgroundColor: '#3b82f6', borderRadius: 4 },
            { label: 'Stockbit (Keluhan)', data: sbNegVals, backgroundColor: '#ef4444', borderRadius: 4 }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: { callbacks: { label: (c) => ` ${c.dataset.label}: ${c.raw} keluhan` } }
          },
          scales: {
            x: { beginAtZero: true, grid: { color: '#f1f5f9' } },
            y: { grid: { display: false } }
          }
        }
      });
    }

    // Filter & Search Engine
    function applyFilters() {
      const term = currentSearchTerm.toLowerCase().trim();

      filteredData = currentData.filter(item => {
        if (currentStarFilter !== "ALL" && item.stars !== parseInt(currentStarFilter)) return false;
        if (currentTopicFilter !== "ALL" && item.topic !== currentTopicFilter) return false;
        if (currentReplyFilter === "WITH_REPLY" && !item.has_reply) return false;
        if (currentReplyFilter === "WITHOUT_REPLY" && item.has_reply) return false;

        if (term) {
          const matchText = item.text.toLowerCase().includes(term);
          const matchTopic = item.topic.toLowerCase().includes(term);
          const matchReply = item.reply.toLowerCase().includes(term);
          if (!matchText && !matchTopic && !matchReply) return false;
        }
        return true;
      });

      // Sorting
      if (currentSort === "date_desc") {
        filteredData.sort((a, b) => b.date.localeCompare(a.date));
        activeSortLabel.innerText = "Urutan: Terbaru ke Terlama (Relevan)";
      } else if (currentSort === "date_asc") {
        filteredData.sort((a, b) => a.date.localeCompare(b.date));
        activeSortLabel.innerText = "Urutan: Terlama ke Terbaru";
      } else if (currentSort === "stars_desc") {
        filteredData.sort((a, b) => b.stars - a.stars || b.date.localeCompare(a.date));
        activeSortLabel.innerText = "Urutan: Rating Tertinggi";
      } else if (currentSort === "stars_asc") {
        filteredData.sort((a, b) => a.stars - b.stars || b.date.localeCompare(a.date));
        activeSortLabel.innerText = "Urutan: Rating Terendah";
      } else if (currentSort === "helpful_desc") {
        filteredData.sort((a, b) => b.helpful - a.helpful || b.date.localeCompare(a.date));
        activeSortLabel.innerText = "Urutan: Paling Membantu";
      }

      displayLimit = 25;
      renderReviews();
    }

    function highlightText(text, term) {
      if (!term || !text) return text;
      const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
      return text.replace(regex, '<span class="highlight">$1</span>');
    }

    function renderReviews() {
      filteredCount.innerText = filteredData.length.toLocaleString();
      const visibleItems = filteredData.slice(0, displayLimit);

      if (visibleItems.length === 0) {
        reviewsFeed.innerHTML = `
          <div class="bg-white p-12 text-center rounded-xl border border-slate-200">
            <div class="text-4xl mb-2">🔍</div>
            <h4 class="text-base font-bold text-slate-800">Tidak ada ulasan yang sesuai</h4>
            <p class="text-xs text-slate-500 mt-1">Coba sesuaikan kata kunci pencarian atau reset filter.</p>
          </div>
        `;
        loadMoreBtn.classList.add("hidden");
        return;
      }

      const term = currentSearchTerm.trim();
      const htmlCards = visibleItems.map((item, idx) => {
        const starBadgeClass = `badge-star-${item.stars}`;
        const starIcons = '★'.repeat(item.stars) + '☆'.repeat(5 - item.stars);
        const highlightedContent = highlightText(item.text, term);

        let replyBox = "";
        if (item.has_reply) {
          const highlightedReply = highlightText(item.reply, term);
          replyBox = `
            <div class="mt-3 pl-3 py-2 border-l-2 border-purple-500 bg-purple-50/60 rounded-r-lg text-xs text-slate-700">
              <div class="flex items-center justify-between font-semibold text-purple-900 mb-1">
                <span class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  Respon Tim CS Pengembang
                </span>
                <span class="text-[10px] text-purple-600 font-normal">${item.replied_at || ''}</span>
              </div>
              <p class="leading-relaxed text-slate-600">${highlightedReply}</p>
            </div>
          `;
        }

        return `
          <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold border ${starBadgeClass}">
                  ${starIcons} (${item.stars})
                </span>
                <span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                  ${item.topic}
                </span>
              </div>
              <div class="text-[11px] text-slate-400 font-mono">
                📅 ${item.date}
              </div>
            </div>

            <p class="text-xs text-slate-800 leading-relaxed font-normal">
              ${highlightedContent || '<span class="italic text-slate-400">(Ulasan tanpa teks tambahan)</span>'}
            </p>

            ${replyBox}

            <div class="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
              <div>Versi App: <span class="text-slate-600 font-medium">${item.version}</span></div>
              <div class="flex items-center gap-1">
                <span>👍</span>
                <span>${item.helpful} orang terbantu</span>
              </div>
            </div>
          </div>
        `;
      }).join("");

      reviewsFeed.innerHTML = htmlCards;

      if (filteredData.length > displayLimit) {
        loadMoreBtn.classList.remove("hidden");
      } else {
        loadMoreBtn.classList.add("hidden");
      }
    }

    // Event Listeners
    searchInput.addEventListener("input", (e) => {
      currentSearchTerm = e.target.value;
      applyFilters();
    });

    topicFilter.addEventListener("change", (e) => {
      currentTopicFilter = e.target.value;
      applyFilters();
    });

    sortFilter.addEventListener("change", (e) => {
      currentSort = e.target.value;
      applyFilters();
    });

    replyFilter.addEventListener("change", (e) => {
      currentReplyFilter = e.target.value;
      applyFilters();
    });

    starBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        starBtns.forEach(b => {
          b.className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200";
        });
        btn.className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-blue-600 text-white border-blue-600";
        currentStarFilter = btn.getAttribute("data-star");
        applyFilters();
      });
    });

    resetBtn.addEventListener("click", () => {
      searchInput.value = "";
      topicFilter.value = "ALL";
      sortFilter.value = "date_desc";
      replyFilter.value = "ALL";
      currentSearchTerm = "";
      currentTopicFilter = "ALL";
      currentReplyFilter = "ALL";
      currentSort = "date_desc";
      currentStarFilter = "ALL";
      displayLimit = 25;

      starBtns.forEach(b => {
        b.className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200";
      });
      starBtns[0].className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-blue-600 text-white border-blue-600";

      applyFilters();
    });

    loadMoreBtn.addEventListener("click", () => {
      displayLimit += 25;
      renderReviews();
    });

    // Boot
    window.addEventListener("DOMContentLoaded", () => {
      switchMode("trima");
    });
  </script>
</body>
</html>
"""

    final_html = html_template.replace("/* TRIMA_DATA_PLACEHOLDER */", trima_json)
    final_html = final_html.replace("/* STOCKBIT_DATA_PLACEHOLDER */", stockbit_json)
    final_html = final_html.replace("/* META_PLACEHOLDER */", meta_json)

    # Simpan dashboard.html & index.html
    for dest in ["dashboard.html", "index.html"]:
        with open(dest, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"[SUCCESS] Standalone interactive dashboard created at: {dest} ({len(final_html):,} bytes)")

if __name__ == "__main__":
    build_dashboard()
