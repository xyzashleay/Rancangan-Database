
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("alumni_data.xlsx", sheet_name="Data ")
    df["NPM"] = df["NPM"].astype(str)
    df["Angkatan"] = df["Angkatan"].astype(str)
    df["Tahun Lulus"] = df["Tahun Lulus"].astype(str)
    return df

df = load_data()

st.set_page_config(page_title="Database Alumni", layout="wide")

# Welcome Page
st.title("📊 Database Alumni")
st.subheader("Departemen Matematika FMIPA UI")
st.write("Sistem informasi terintegrasi untuk mengelola data alumni Sarjana Matematika, Statistika, dan Ilmu Aktuaria")

st.markdown("---")

# Sidebar Filter
st.sidebar.header("🔍 Filter Pencarian")
nama = st.sidebar.text_input("Nama")
program_studi = st.sidebar.selectbox("Program Studi", ["", "Matematika", "Statistika", "Ilmu Aktuaria"])
npm = st.sidebar.text_input("NPM")
pekerjaan = st.sidebar.text_input("Pekerjaan")
perusahaan = st.sidebar.text_input("Perusahaan")
gaji = st.sidebar.text_input("Gaji (angka atau string)")

# Filter logic
filtered_df = df.copy()
if nama:
    filtered_df = filtered_df[filtered_df["Nama"].str.contains(nama, case=False, na=False)]
if program_studi:
    filtered_df = filtered_df[filtered_df["Program Studi"].str.contains(program_studi, case=False, na=False)]
if npm:
    filtered_df = filtered_df[filtered_df["NPM"].str.contains(npm, na=False)]
if pekerjaan:
    filtered_df = filtered_df[filtered_df["Pekerjaan"].str.contains(pekerjaan, case=False, na=False)]
if perusahaan:
    filtered_df = filtered_df[filtered_df["Nama Perusahaan"].str.contains(perusahaan, case=False, na=False)]
if gaji:
    filtered_df = filtered_df[filtered_df["Rata-rata Gaji"].astype(str).str.contains(gaji, case=False, na=False)]

# Show statistics
col1, col2 = st.columns(2)
col1.metric("Total Alumni", len(df))
col2.metric("Hasil Pencarian", len(filtered_df))

st.markdown("---")

# Display data
st.subheader("📋 Data Alumni")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
