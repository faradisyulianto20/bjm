import os
import sys
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("output/trima_reviews_clean.csv")

topics = [
    "Login & Autentikasi",
    "UI/UX & Performa (Loading/Navigasi)",
    "Transaksi & Portofolio Saham",
    "Stabilitas Sistem & Bug (Crash/Error)",
    "Registrasi & Onboarding (KYC)",
    "Customer Service & Layanan",
    "Fitur Analisis & Data Pasar"
]

print("=== STATISTIK SETIAP TOPIK ===")
for t in topics:
    sub = df[df['primary_topic'] == t]
    stars = sub['stars'].value_counts().sort_index().to_dict()
    reply_rate = (sub['has_developer_reply'] == 'Ya').mean() * 100
    print(f"\n--- {t} ---")
    print(f"Total: {len(sub)} ulasan | Bintang: {stars} | Respon Dev: {reply_rate:.1f}%")
    print("Contoh ulasan bintang 1-2:")
    neg = sub[sub['stars'] <= 2].head(3)
    for _, r in neg.iterrows():
        print(f"  * ⭐{r['stars']} ({r['review_date']}): {r['clean_text']}")
