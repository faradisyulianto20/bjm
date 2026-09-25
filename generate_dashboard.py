"""
Generate standalone interactive dashboard 'dashboard.html'
Uses template replacement so JavaScript syntax is never confused with Python f-strings.
"""

import json
import os
import pandas as pd

df = pd.read_csv("output/trima_reviews_clean.csv")

# Siapkan data ulasan untuk JavaScript
records = []
for _, r in df.iterrows():
    records.append({
        "id": str(r["review_id"]),
        "stars": int(r["stars"]),
        "sentiment": str(r["sentiment"]),
        "topic": str(r["primary_topic"]),
        "date": str(r["review_date"]),
        "year": int(r["review_year"]) if str(r["review_year"]).isdigit() else 0,
        "text": str(r["clean_text"]),
        "version": str(r["app_version"]),
        "helpful": int(r["helpful_count"]) if pd.notna(r["helpful_count"]) else 0,
        "has_reply": str(r["has_developer_reply"]) == "Ya",
        "reply": str(r["developer_reply"]) if pd.notna(r["developer_reply"]) and str(r["developer_reply"]) != "nan" else ""
    })

data_json = json.dumps(records, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Analisis Ulasan Trima+ | PT Trimegah Sekuritas</title>
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
        <div class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow">
          T+
        </div>
        <div>
          <h1 class="text-lg font-bold text-slate-900 leading-tight">Dashboard Interaktif Ulasan Trima+</h1>
          <p class="text-xs text-slate-500">PT Trimegah Sekuritas Indonesia Tbk &bull; Filter & Eksplorasi Data Real-Time</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
          <span class="w-2 h-2 mr-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
          1.312 Ulasan Bertulis
        </span>
        <span class="text-xs text-slate-400">hl=id, gl=ID</span>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- KPI Metric Cards -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Rating Play Store</div>
        <div class="text-2xl font-bold text-slate-900 mt-1">3.747</div>
        <div class="text-xs text-slate-400 mt-1">Skor Resmi: 3.12 / 5.0</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rata-rata Review Teks</div>
        <div class="text-2xl font-bold text-blue-600 mt-1">3.68 <span class="text-sm font-normal text-slate-500">/ 5.0</span></div>
        <div class="text-xs text-slate-400 mt-1">Skor Normal: 67.1 / 100</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="text-xs font-semibold text-emerald-600 uppercase tracking-wider">Positive Share (★4-5)</div>
        <div class="text-2xl font-bold text-emerald-600 mt-1">62.9%</div>
        <div class="text-xs text-slate-400 mt-1">825 ulasan puas</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div class="text-xs font-semibold text-rose-600 uppercase tracking-wider">Negative Share (★1-2)</div>
        <div class="text-2xl font-bold text-rose-600 mt-1">28.4%</div>
        <div class="text-xs text-slate-400 mt-1">372 titik friksi nasabah</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm col-span-2 md:col-span-1">
        <div class="text-xs font-semibold text-purple-600 uppercase tracking-wider">Respon Developer</div>
        <div class="text-2xl font-bold text-purple-600 mt-1">48.0%</div>
        <div class="text-xs text-slate-400 mt-1">630 ulasan dibalas CS</div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Chart 1: Distribusi Bintang -->
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-sm font-bold text-slate-800">Distribusi Rating Bintang Asli (1 - 5)</h2>
          <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">Bimodal Pattern</span>
        </div>
        <div class="h-64">
          <canvas id="chartStars"></canvas>
        </div>
      </div>

      <!-- Chart 2: Root Cause Ulasan Negatif -->
      <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-sm font-bold text-slate-800">Root Cause Keluhan Negatif (Bintang 1 - 2)</h2>
          <span class="text-xs bg-rose-100 text-rose-700 px-2 py-0.5 rounded font-semibold">N = 372</span>
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
            placeholder="Cari kata kunci: misal 'login', 'tarik', 'otp', 'biometrik', 'loading', 'rdn', 'update'..." 
            class="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <!-- Filter Topic Dropdown -->
        <div class="w-full md:w-72">
          <select id="topicFilter" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="ALL">Semua Kategori Topik (Semua)</option>
            <option value="Login & Autentikasi">Login & Autentikasi (143)</option>
            <option value="Keluhan Umum Aplikasi">Keluhan Umum Aplikasi (121)</option>
            <option value="UI/UX & Performa (Loading/Navigasi)">UI/UX & Performa (104)</option>
            <option value="Transaksi & Portofolio Saham">Transaksi & Portofolio Saham (66)</option>
            <option value="Customer Service & Layanan">Customer Service & Layanan (46)</option>
            <option value="Stabilitas Sistem & Bug (Crash/Error)">Stabilitas Sistem & Bug (36)</option>
            <option value="Registrasi & Onboarding (KYC)">Registrasi & Onboarding (29)</option>
            <option value="Fitur Analisis & Data Pasar">Fitur Analisis & Data Pasar (16)</option>
            <option value="Apresiasi Umum & Kepuasan">Apresiasi Umum & Kepuasan (714)</option>
            <option value="Netral / Saran Umum">Netral / Saran Umum (37)</option>
          </select>
        </div>

        <!-- Sorting Dropdown -->
        <div class="w-full md:w-56">
          <select id="sortFilter" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="date_desc">Tanggal: Terbaru &rarr; Terlama</option>
            <option value="date_asc">Tanggal: Terlama &rarr; Terbaru</option>
            <option value="stars_asc">Rating: Terendah &rarr; Tertinggi (★1 dulu)</option>
            <option value="stars_desc">Rating: Tertinggi &rarr; Terendah (★5 dulu)</option>
          </select>
        </div>
      </div>

      <!-- Quick Filter Pills: Stars & CS Reply -->
      <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-100 text-xs">
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-slate-500 font-semibold mr-1">Filter Bintang:</span>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-blue-600 text-white border-blue-600" data-star="ALL">Semua</button>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200" data-star="1">★ 1</button>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200" data-star="2">★ 2</button>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200" data-star="3">★ 3</button>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200" data-star="4">★ 4</button>
          <button class="star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200" data-star="5">★ 5</button>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-slate-500 font-semibold">Respon CS:</span>
          <select id="replyFilter" class="px-2.5 py-1 border border-slate-200 rounded-md bg-white text-xs">
            <option value="ALL">Semua Status</option>
            <option value="YES">Sudah Dibalas CS</option>
            <option value="NO">Belum Dibalas CS</option>
          </select>
          <button id="resetBtn" class="text-blue-600 hover:text-blue-800 font-medium ml-2">Reset Filter</button>
        </div>
      </div>
    </div>

    <!-- Results Status Bar -->
    <div class="flex items-center justify-between text-sm text-slate-600 px-1">
      <div>
        Menampilkan <span id="displayedCount" class="font-bold text-slate-900">0</span> dari 1.312 ulasan
        <span id="activeFilterBadge" class="text-xs text-blue-600 ml-2"></span>
      </div>
      <div class="text-xs text-slate-400">Klik ulasan untuk membaca balasan pengembang</div>
    </div>

    <!-- Reviews List Container -->
    <div id="reviewsContainer" class="space-y-3">
      <!-- Generated via JS -->
    </div>

    <!-- Pagination / Load More -->
    <div id="loadMoreContainer" class="text-center py-4">
      <button id="loadMoreBtn" class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 font-medium text-sm rounded-lg hover:bg-slate-50 shadow-sm transition">
        Tampilkan Lebih Banyak Ulasan
      </button>
    </div>

  </main>

  <footer class="bg-white border-t border-slate-200 mt-12 py-6 text-center text-xs text-slate-500">
    <p>Dashboard Analisis Ulasan Pengguna Trima+ &bull; Dibuat untuk Business Case Competition & Evaluasi CX &bull; UU PDP Compliant</p>
  </footer>

  <!-- Embedded Dataset -->
  <script>
    const rawReviews = /* DATA_PLACEHOLDER */;
  </script>

  <script>
    // State Aplikasi
    let currentStarFilter = "ALL";
    let currentTopicFilter = "ALL";
    let currentReplyFilter = "ALL";
    let currentSort = "date_desc";
    let currentSearchTerm = "";
    let displayLimit = 25;
    let filteredReviews = [];

    // DOM Elements
    const searchInput = document.getElementById("searchInput");
    const topicFilter = document.getElementById("topicFilter");
    const sortFilter = document.getElementById("sortFilter");
    const replyFilter = document.getElementById("replyFilter");
    const resetBtn = document.getElementById("resetBtn");
    const starBtns = document.querySelectorAll(".star-btn");
    const displayedCount = document.getElementById("displayedCount");
    const activeFilterBadge = document.getElementById("activeFilterBadge");
    const reviewsContainer = document.getElementById("reviewsContainer");
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    const loadMoreContainer = document.getElementById("loadMoreContainer");

    // Inisialisasi Chart.js
    function initCharts() {
      // 1. Chart Stars Distribution
      const starCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
      rawReviews.forEach(r => { if (starCounts[r.stars] !== undefined) starCounts[r.stars]++; });
      
      const ctxStars = document.getElementById('chartStars').getContext('2d');
      new Chart(ctxStars, {
        type: 'bar',
        data: {
          labels: ['★ 1', '★ 2', '★ 3', '★ 4', '★ 5'],
          datasets: [{
            label: 'Jumlah Ulasan',
            data: [starCounts[1], starCounts[2], starCounts[3], starCounts[4], starCounts[5]],
            backgroundColor: ['#ef4444', '#f97316', '#eab308', '#84cc16', '#3b82f6'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: ctx => `${ctx.raw} ulasan (${(ctx.raw / rawReviews.length * 100).toFixed(1)}%)`
              }
            }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });

      // 2. Chart Complaints Breakdown
      const complaintCounts = {
        'Keluhan Umum': 121,
        'Login & Auth': 98,
        'UI/UX & Performa': 58,
        'Transaksi Saham': 34,
        'Stabilitas & Bug': 22,
        'Fitur & Analisis': 12,
        'Registrasi KYC': 4,
        'Customer Service': 3
      };

      const ctxComplaints = document.getElementById('chartComplaints').getContext('2d');
      new Chart(ctxComplaints, {
        type: 'bar',
        data: {
          labels: Object.keys(complaintCounts),
          datasets: [{
            label: 'Jumlah Keluhan',
            data: Object.values(complaintCounts),
            backgroundColor: '#e11d48',
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: { beginAtZero: true }
          }
        }
      });
    }

    // Filter Logic
    function applyFilters() {
      const term = currentSearchTerm.toLowerCase().trim();

      filteredReviews = rawReviews.filter(r => {
        // Filter Bintang
        if (currentStarFilter !== "ALL" && r.stars !== parseInt(currentStarFilter)) {
          return false;
        }
        // Filter Topik
        if (currentTopicFilter !== "ALL" && r.topic !== currentTopicFilter) {
          return false;
        }
        // Filter Respon Dev
        if (currentReplyFilter === "YES" && !r.has_reply) return false;
        if (currentReplyFilter === "NO" && r.has_reply) return false;

        // Search text matching
        if (term) {
          const matchText = r.text.toLowerCase().includes(term);
          const matchReply = r.reply.toLowerCase().includes(term);
          const matchTopic = r.topic.toLowerCase().includes(term);
          const matchVer = r.version.toLowerCase().includes(term);
          if (!matchText && !matchReply && !matchTopic && !matchVer) {
            return false;
          }
        }
        return true;
      });

      // Sorting
      filteredReviews.sort((a, b) => {
        if (currentSort === "date_desc") return new Date(b.date) - new Date(a.date);
        if (currentSort === "date_asc") return new Date(a.date) - new Date(b.date);
        if (currentSort === "stars_asc") return a.stars - b.stars;
        if (currentSort === "stars_desc") return b.stars - a.stars;
        return 0;
      });

      renderReviews();
    }

    function highlightText(text, query) {
      if (!query || !text) return text;
      const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
      return text.replace(regex, '<span class="highlight">$1</span>');
    }

    function renderReviews() {
      displayedCount.textContent = filteredReviews.length.toLocaleString('id-ID');
      
      const badgeParts = [];
      if (currentStarFilter !== "ALL") badgeParts.push(`★${currentStarFilter}`);
      if (currentTopicFilter !== "ALL") badgeParts.push(`Topik: ${currentTopicFilter}`);
      if (currentReplyFilter !== "ALL") badgeParts.push(currentReplyFilter === "YES" ? "Dibalas CS" : "Belum Dibalas");
      if (currentSearchTerm) badgeParts.push(`Pencarian: "${currentSearchTerm}"`);
      activeFilterBadge.textContent = badgeParts.length > 0 ? `(${badgeParts.join(' • ')})` : '';

      const slice = filteredReviews.slice(0, displayLimit);

      if (slice.length === 0) {
        reviewsContainer.innerHTML = `
          <div class="bg-white p-12 text-center rounded-xl border border-slate-200">
            <svg class="w-12 h-12 text-slate-300 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-slate-600 font-semibold">Tidak ada ulasan yang cocok dengan kriteria filter.</p>
            <p class="text-slate-400 text-xs mt-1">Coba ubah kata kunci pencarian atau reset filter.</p>
          </div>
        `;
        loadMoreContainer.style.display = 'none';
        return;
      }

      let html = '';
      slice.forEach((r, idx) => {
        const starClass = `badge-star-${r.stars}`;
        const starIcons = '★'.repeat(r.stars) + '☆'.repeat(5 - r.stars);
        const highlightedContent = highlightText(r.text, currentSearchTerm);
        const highlightedReply = highlightText(r.reply, currentSearchTerm);

        html += `
          <div class="bg-white p-4 rounded-xl border border-slate-200 hover:border-slate-300 transition shadow-sm space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full font-bold border ${starClass}">
                  ${starIcons} (${r.stars}/5)
                </span>
                <span class="px-2 py-0.5 bg-slate-100 text-slate-700 rounded font-medium">
                  ${r.topic}
                </span>
              </div>
              <div class="text-slate-400 flex items-center gap-3">
                <span>Versi App: <strong class="text-slate-600">${r.version || '-'}</strong></span>
                <span>&bull;</span>
                <span>${r.date}</span>
              </div>
            </div>

            <p class="text-sm text-slate-800 leading-relaxed font-normal">
              ${highlightedContent}
            </p>

            ${r.has_reply ? `
              <div class="mt-2.5 p-3 rounded-lg bg-blue-50/70 border border-blue-100 text-xs space-y-1">
                <div class="font-bold text-blue-900 flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                  </svg>
                  Tanggapan Pengembang (Trimegah CS):
                </div>
                <div class="text-blue-800 leading-relaxed">${highlightedReply}</div>
              </div>
            ` : ''}
          </div>
        `;
      });

      reviewsContainer.innerHTML = html;

      if (displayLimit >= filteredReviews.length) {
        loadMoreContainer.style.display = 'none';
      } else {
        loadMoreContainer.style.display = 'block';
        loadMoreBtn.textContent = `Tampilkan Lebih Banyak (${slice.length} dari ${filteredReviews.length})`;
      }
    }

    // Event Listeners
    searchInput.addEventListener("input", (e) => {
      currentSearchTerm = e.target.value;
      displayLimit = 25;
      applyFilters();
    });

    topicFilter.addEventListener("change", (e) => {
      currentTopicFilter = e.target.value;
      displayLimit = 25;
      applyFilters();
    });

    sortFilter.addEventListener("change", (e) => {
      currentSort = e.target.value;
      applyFilters();
    });

    replyFilter.addEventListener("change", (e) => {
      currentReplyFilter = e.target.value;
      displayLimit = 25;
      applyFilters();
    });

    starBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        starBtns.forEach(b => {
          b.className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-white text-slate-700 hover:bg-slate-50 border-slate-200";
        });
        btn.className = "star-btn px-2.5 py-1 rounded-md font-medium border bg-blue-600 text-white border-blue-600";
        currentStarFilter = btn.dataset.star;
        displayLimit = 25;
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
      initCharts();
      applyFilters();
    });
  </script>
</body>
</html>
"""

final_html = html_template.replace("/* DATA_PLACEHOLDER */", data_json)

dashboard_path = "dashboard.html"
with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[SUCCESS] Standalone interactive dashboard created at: {dashboard_path} ({len(final_html):,} bytes)")
