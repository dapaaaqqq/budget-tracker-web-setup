import os
import psycopg2
from psycopg2.extras import RealDictCursor

def buat_koneksi():
    # Mengambil URL database dari environment variable Neon di Streamlit Cloud
    DATABASE_URL = os.environ.get("DATABASE_URL")
    
    # Kebutuhan testing lokal jika environment variable belum di-set
    if not DATABASE_URL:
        # Ganti dengan connection string Neon milikmu untuk testing lokal
        DATABASE_URL = "postgresql://user:password@endpoint.neon.tech/neondb?sslmode=require"
        
    koneksi = psycopg2.connect(DATABASE_URL)
    return koneksi

def add_data():
    conn = buat_koneksi()
    kursor = conn.cursor()
    kursor.execute('''
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id SERIAL PRIMARY KEY,
            tanggal TEXT,
            nama TEXT,
            nominal NUMERIC,
            kategori TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Tabel berhasil disiapkan!")

def simpan(tanggal, nama, nominal, kategori):
    conn = buat_koneksi()
    kursor = conn.cursor()
    sql = '''
        INSERT INTO pengeluaran (tanggal, nama, nominal, kategori)
        VALUES (%s, %s, %s, %s)
    '''
    kursor.execute(sql, (tanggal, nama, nominal, kategori))
    conn.commit()
    conn.close()

def hapus_data(id_target):
    conn = buat_koneksi()
    kursor = conn.cursor()
    kursor.execute("DELETE FROM pengeluaran WHERE id = %s", (id_target,))
    conn.commit()
    conn.close()
    print(f"✅ Data dengan ID {id_target} berhasil dihapus!")

def lihat_data():
    conn = buat_koneksi()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM pengeluaran")
    semua_baris = kursor.fetchall()
    conn.close()
    return semua_baris


add_data()