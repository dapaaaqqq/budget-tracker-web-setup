import streamlit as st
import pandas as pd
from database_manager import buat_koneksi, simpan, lihat_data, hapus_data
import datetime
from util import filter as filter_data
from util import convert

# 1. Konfigurasi Halaman (Menggunakan Layout Wide agar dashboard lebih luas)
st.set_page_config(page_title="Smart Budget Tracker", layout="wide", page_icon="💰")

# Sembunyikan semua elemen bawaan Streamlit (Header, Footer, Menu, Toolbar)
hide_streamlit_style = """
            <style>
            div[data-testid="stStatusWidget"], .stAppDeployButton, footer, header {
                visibility: hidden !important;
                display: none !important;
            }
            
            
            #MainMenu, [data-testid="stActionButton"] {
                visibility: hidden !important;
                display: none !important;
            }
            
            .stApp {
                margin-top: -40px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# 2. Header Dashboard
st.title("💰 SMART BUDGET TRACKER")
st.caption("Pantau keuanganmu secara cerdas, real-time, dan anti BONCOS!")
st.divider()

# 3. Sidebar (Pengaturan & Filter Terpusat)
st.sidebar.header("⚙️ Kontrol Panel")
limit_harian = st.sidebar.number_input("Set Limit Harian (Rp)", value=500000, step=50000)

# Ambil Data dari Database
conn = buat_koneksi()
df = pd.read_sql_query("SELECT * FROM pengeluaran ORDER BY id DESC", conn)
conn.close()

# Terapkan Filter jika data tidak kosong
if not df.empty:
    df = filter_data(df)

# 4. Logika Perhitungan Nilai Metrik
tgl_hari_ini = str(datetime.date.today())
if not df.empty:
    total_hari_ini = int(df[df['tanggal'] == tgl_hari_ini]['nominal'].sum())
    total_semua = int(df['nominal'].sum())
    sisa_budget = limit_harian - total_hari_ini
else:
    total_hari_ini = 0
    total_semua = 0
    sisa_budget = limit_harian

# 5. Bagian Ringkasan / KPI Cards (Paling Atas)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(
        label="Pengeluaran Hari Ini", 
        value=f"Rp {total_hari_ini:,}",
        delta=f"Limit: Rp {limit_harian:,}",
        delta_color="normal"
    )
with col_m2:
    st.metric(
        label="Total Semua Pengeluaran", 
        value=f"Rp {total_semua:,}"
    )
with col_m3:
    # Warna delta otomatis merah jika minus (overbudget)
    st.metric(
        label="Sisa Budget Hari Ini", 
        value=f"Rp {sisa_budget:,}",
        delta=f"{'Sisa Aman' if sisa_budget >= 0 else 'Overbudget!'}",
        delta_color="normal" if sisa_budget >= 0 else "inverse"
    )

st.divider()

# 6. Status Warning / Informasi Budget
if total_hari_ini > limit_harian:
    st.error(f"⚠️ **Waspada!** Kamu sudah melewati limit harianmu sebesar **Rp {abs(sisa_budget):,}**!")
elif total_hari_ini == limit_harian:
    st.warning("⚠️ **Hati-hati!** Pengeluaranmu pas bersentuhan dengan limit harian.")
elif total_hari_ini >= (limit_harian * 0.8):
    st.warning("⚠️ **Hati-hati!** Kamu sudah mendekati limit harianmu (Sudah >80%).")
elif total_hari_ini > 0:
    st.success("👍 **Bagus!** Pengeluaran hari ini masih berada dalam batas aman limit harianmu.")
else:
    st.info("🎉 Hari ini belum ada pengeluaran. Pertahankan gaya hematmu!")

st.write("") # Spasi tambahan

# 7. Layout Utama (Membagi Dashboard Menjadi 2 Kolom Besar)
kolom_kiri, kolom_kanan = st.columns([3, 2]) # Proporsi 60% kiri, 40% kanan

with kolom_kiri:
    st.subheader("📊 Analisis Visual & Data")
    
    # Menggunakan Tabs agar visualisasi dan tabel data terorganisasi dengan rapi
    tab1, tab2 = st.tabs(["📉 Grafik Kategori", "📋 Tabel Detail"])
    
    with tab1:
        if not df.empty:
            df['kategori'] = df['kategori'].fillna("Lainnya")
            rekap_kategori = df.groupby("kategori")["nominal"].sum().reset_index()
            st.bar_chart(
                rekap_kategori,
                x="kategori",
                y="nominal",
                use_container_width=True,
            )
        else:
            st.info("Belum ada data untuk divisualisasikan.")
            
    with tab2:
        if not df.empty:
            st.dataframe(df[['id', 'tanggal', 'nama', 'nominal', 'kategori']], use_container_width=True)
            
            # Unduh Data ditaruh di dalam tab detail agar tidak merusak pemandangan utama
            st.download_button(
                label="📥 Unduh Data (CSV)",
                data=convert(df),
                file_name=f"laporan_budget_{tgl_hari_ini}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Tabel data kosong.")

with kolom_kanan:
    st.subheader("⚡ Aksi & Manajemen")
    
    # Kotak Tambah Pengeluaran
    with st.expander("➕ Tambah Pengeluaran Baru", expanded=True):
        with st.form("form_input", clear_on_submit=True):
            nama_barang = st.text_input("Nama Barang/Kegiatan")
            nominal = st.number_input("Nominal (Rp)", min_value=0, step=5000, format="%d")
            kategori = st.selectbox("Kategori", ["Makanan", "Transportasi", "Hiburan", "Lainnya"])
            submit_button = st.form_submit_button("Simpan Pengeluaran", use_container_width=True)

        if submit_button:
            if nama_barang and nominal > 0:
                tanggal = datetime.date.today().strftime("%Y-%m-%d")
                simpan(tanggal, nama_barang, nominal, kategori)
                st.success(f"✅ Berhasil mencatat: {nama_barang}")
                st.rerun()
            else:
                st.error("Gagal menyimpan! Pastikan nama barang diisi dan nominal lebih dari 0.")

    # Kotak Hapus Pengeluaran
    with st.expander("🗑️ Hapus Data Pengeluaran"):
        if not df.empty:
            pilihan = df.apply(lambda x: f"{x['id']} - {x['nama']} (Rp {x['nominal']:,})", axis=1).tolist()
            data = st.selectbox("Pilih Data Yang Ingin Dihapus:", pilihan)
            id_target = int(data.split(" - ")[0])

            if st.button("Hapus Data", type="primary", use_container_width=True):
                hapus_data(id_target)
                st.success(f"✅ Data dengan ID {id_target} berhasil dihapus!")
                st.rerun()
        else:
            st.info("Tidak ada data yang bisa dihapus.")