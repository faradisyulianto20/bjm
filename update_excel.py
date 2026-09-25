"""
Add dedicated sheets per topic to output/trima_reviews_analysis.xlsx
Allows user to easily filter, sort, and inspect every review category in Excel.
"""

import os
import pandas as pd

df = pd.read_csv("output/trima_reviews_clean.csv")
excel_path = os.path.join("output", "trima_reviews_analysis.xlsx")

cols_export = [
    "stars", "sentiment", "primary_topic", "review_date", "clean_text", 
    "app_version", "helpful_count", "has_developer_reply", "developer_reply", "review_id"
]

topics_map = {
    "Login_Autentikasi": "Login & Autentikasi",
    "Keluhan_Umum": "Keluhan Umum Aplikasi",
    "UIUX_Performa": "UI/UX & Performa (Loading/Navigasi)",
    "Transaksi_Portofolio": "Transaksi & Portofolio Saham",
    "Stabilitas_Bug": "Stabilitas Sistem & Bug (Crash/Error)",
    "Registrasi_KYC": "Registrasi & Onboarding (KYC)",
    "Customer_Service": "Customer Service & Layanan",
    "Fitur_DataPasar": "Fitur Analisis & Data Pasar"
}

with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    for sheet_name, topic_val in topics_map.items():
        sub_df = df[df['primary_topic'] == topic_val][cols_export].copy()
        sub_df.sort_values(by="stars", ascending=True, inplace=True)
        sub_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"[+] Sheet '{sheet_name}' ({len(sub_df)} baris) berhasil disimpan.")

print(f"[SUCCESS] Seluruh sheet kategori berhasil ditambahkan ke: {excel_path}")
