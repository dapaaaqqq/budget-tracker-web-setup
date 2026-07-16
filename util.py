import pandas as pd
import streamlit as st

def filter(df):
    st.sidebar.subheader("Filter Data")
    waktu = st.sidebar.selectbox(
        "Pilih Rentang Waktu",
        ["Semua Waktu", "Hari Ini", "7 Hari Terakhir", "Bulan Ini"]
    )

    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    hari_ini = pd.to_datetime("today").normalize()

    if waktu == "Hari Ini":
        df = df[df['tanggal'] == hari_ini]
    elif waktu == "7 Hari Terakhir":
        df = df[df['tanggal'] >= (hari_ini - pd.Timedelta(days=7))]
    elif waktu == "Bulan Ini":
        df = df[df['tanggal'] >= (hari_ini - pd.Timedelta(days=30))]
    
    return df

def convert(df):
    return df.to_csv(index=False).encode('utf-8')
