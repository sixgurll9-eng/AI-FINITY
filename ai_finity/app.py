import streamlit as st
from groq import Groq
import os
import pandas as pd

st.set_page_config(page_title="Finance Twin AI", page_icon="💸", layout="wide")

# --- Connect to GROQ ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("💸 Finance Twin: Your Digital Financial Twin")
st.write("Masukkan kondisi finansialmu, lalu AI akan membaca, menganalisis, dan memberi rekomendasi.")

# --- Input Bagian Keuangan ---
st.subheader("📊 Input Data Keuangan")

income = st.number_input("Pendapatan bulanan (Rp)", min_value=0, step=100000)
expense = st.number_input("Pengeluaran bulanan (Rp)", min_value=0, step=100000)
savings = st.number_input("Tabungan saat ini (Rp)", min_value=0, step=100000)
debt = st.number_input("Total Utang (Rp)", min_value=0, step=100000)
risk = st.selectbox("Profil Risiko", ["Konservatif", "Moderate", "Agresif"])

# --- Tombol Analisis ---
if st.button("Analisis Keuangan"):
    st.subheader("⏳ Processing...")

    data_summary = f"""
    Data Finansial Pengguna:
    - Pendapatan: Rp {income:,}
    - Pengeluaran: Rp {expense:,}
    - Tabungan: Rp {savings:,}
    - Utang: Rp {debt:,}
    - Profil Risiko: {risk}
    """

    prompt = f"""
    Kamu adalah FINANCE TWIN, AI asisten keuangan pribadi.
    Analisislah data berikut:

    {data_summary}

    Buat output:
    1. Ringkasan kondisi finansial
    2. Tingkat kesehatan finansial (skor 0–100)
    3. Analisis cashflow (baik/tidak stabil)
    4. Saran pengelolaan utang
    5. Saran investasi sesuai profil risiko
    6. Simulasi prediksi tabungan 12 bulan
    7. Aksi cepat yang harus dilakukan

    Buat singkat, jelas, dan actionable.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message["content"]
    st.success("Analisis selesai!")
    st.write(result)

# --- Tabel Output Data Finansial ---
st.subheader("📁 Data Finansial (Ringkas)")
df = pd.DataFrame({
    "Kategori": ["Pendapatan", "Pengeluaran", "Tabungan", "Utang"],
    "Jumlah (Rp)": [income, expense, savings, debt]
})
st.table(df)
