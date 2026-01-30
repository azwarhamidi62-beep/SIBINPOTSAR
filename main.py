# import streamlit as st
# import pandas as pd
# import sqlite3
# import numpy as np
# import folium
# from streamlit_folium import st_folium
# from fpdf import FPDF
# import base64
# from datetime import date
#
# # --- KONFIGURASI DATABASE ---
# conn = sqlite3.connect('sar_potensi.db', check_same_thread=False)
# c = conn.cursor()
#
# def init_db():
#     c.execute('''CREATE TABLE IF NOT EXISTS personil
#                  (id INTEGER PRIMARY KEY, nama TEXT, organisasi TEXT, lat REAL, lng REAL)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS sertifikasi
#                  (id_personil INTEGER, jenis TEXT, tgl_expired DATE)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS logistik
#                  (id INTEGER PRIMARY KEY, item TEXT, kategori TEXT, jumlah INTEGER, kondisi TEXT)''')
#     conn.commit()
#
# init_db()
#
# # --- FUNGSI HELPER ---
# def haversine(lat1, lon1, lat2, lon2):
#     lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
#     dlat, dlon = lat2 - lat1, lon2 - lon1
#     a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
#     return 6371 * (2 * np.arcsin(np.sqrt(a)))
#
# # --- UI SIDEBAR ---
# st.set_page_config(page_title="Sistem Bina Potensi SAR", layout="wide")
# st.sidebar.title("🚁 Menu Utama")
# menu = ["Dashboard & Peta", "Manajemen Personil", "Logistik SAR", "Respon Cepat (Radius)", "Laporan"]
# choice = st.sidebar.radio("Navigasi", menu)
#
# # --- LOGIKA HALAMAN ---
# if choice == "Dashboard & Peta":
#     st.title("🌍 Peta Sebaran Potensi SAR")
#     df_peta = pd.read_sql_query("SELECT * FROM personil", conn)
#     m = folium.Map(location=[-2.5, 118], zoom_start=5)
#     for _, row in df_peta.iterrows():
#         folium.Marker([row['lat'], row['lng']], popup=row['nama'], icon=folium.Icon(color='blue')).add_to(m)
#     st_folium(m, width="100%", height=500)
#
# elif choice == "Manajemen Personil":
#     st.title("👥 Manajemen Personil & Sertifikasi")
#     with st.form("tambah_p"):
#         c1, c2 = st.columns(2)
#         nama = c1.text_input("Nama Lengkap")
#         org = c2.text_input("Organisasi")
#         lat = c1.number_input("Lat (Desimal)", format="%.6f")
#         lng = c2.number_input("Lng (Desimal)", format="%.6f")
#         if st.form_submit_button("Simpan Personil"):
#             c.execute("INSERT INTO personil (nama, organisasi, lat, lng) VALUES (?,?,?,?)", (nama, org, lat, lng))
#             conn.commit()
#             st.success("Data Tersimpan!")
#
# elif choice == "Respon Cepat (Radius)":
#     st.title("⚡ Analisis Respon Terdekat")
#     col1, col2, col3 = st.columns(3)
#     t_lat = col1.number_input("Lat Musibah", value=-6.175)
#     t_lng = col2.number_input("Lng Musibah", value=106.827)
#     rad = col3.slider("Radius (KM)", 1, 100, 20)
#
#     df_res = pd.read_sql_query("SELECT * FROM personil", conn)
#     if not df_res.empty:
#         df_res['jarak_km'] = df_res.apply(lambda x: haversine(t_lat, t_lng, x['lat'], x['lng']), axis=1)
#         hasil = df_res[df_res['jarak_km'] <= rad].sort_values('jarak_km')
#         st.table(hasil[['nama', 'organisasi', 'jarak_km']])
#
# elif choice == "Laporan":
#     st.title("📄 Export PDF")
#     if st.button("Download Laporan Personil"):
#         df_lap = pd.read_sql_query("SELECT nama, organisasi, lat FROM personil", conn)
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", 'B', 12)
#         pdf.cell(0, 10, "DATA POTENSI SAR", ln=True)
#         for _, r in df_lap.iterrows():
#             pdf.cell(0, 10, f"{r['nama']} - {r['organisasi']}", ln=True)
#
#         pdf_out = pdf.output(dest='S').encode('latin-1')
#         b64 = base64.b64encode(pdf_out).decode()
#         st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="sar_report.pdf">Download PDF</a>', unsafe_allow_html=True)