import os
import psycopg2
from psycopg2.extras import RealDictCursor

def buat_koneksi(): 
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        DATABASE_URL = "postgresql://neondb_owner:npg_Ih04XmkErBbn@ep-cold-fire-aoio4bhx.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

    koneksi = psycopg2.connect(DATABASE_URL)
    return koneksi
def add_data():
    conn = buat_koneksi()
    kursor = conn.cursor()
    kursor.execute('''
                  CREATE TABLE IF NOT EXISTS pengeluaran (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tanggal TEXT,
                  nama TEXT,
                  nominal TEXT,
                  kategori TEXT
                  )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ Data berhasil disimpan!")


def simpan(tanggal, nama, nominal, kategori):
   conn = buat_koneksi()
   kursor = conn.cursor()

   sql = '''
        INSERT INTO pengeluaran (tanggal, nama, nominal, kategori)
        VALUES (?, ?, ?, ?)
        '''
   
   kursor.execute(sql, (tanggal, nama, nominal, kategori))

   conn.commit()
   conn.close()
   print("✅ Database dan Tabel berhasil disiapkan!")

buat_koneksi()

def lihat_data():
    conn = buat_koneksi()
    kursor = conn.cursor()

    kursor.execute("SELECT * FROM pengeluaran")

    semua_baris = kursor.fetchall()

    print("\n--- LAPORAN PENGELUARAN ---")
    if not semua_baris:
        print("Belum ada data.")
    else:
        for baris in semua_baris:
            print(f"{baris[0]}. {baris[1]} {baris[2]} - Rp{baris[3]} ({baris[4]})")

    conn.close()        

def hapus_data(id_target):
    conn = buat_koneksi()
    kursor = conn.cursor()

    kursor.execute("DELETE FROM pengeluaran WHERE id = ?", (id_target,))

    conn.commit()
    conn.close()
    print(f"✅ Data dengan ID {id_target} berhasil dihapus!")

def menu():
    add_data()
menu()

def layar_bersih():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
        while True:
            print("\n=== SMART BUDGET TRACKER (DB VERSION) ===")
            print("/tambah")
            print("/hapus")
            print("/Lihat Data")
            print("/Keluar")

            pilihan = input("pilih salah satu menu: ")

            if pilihan == "/tambah":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                nama = input("Nama barang: ")
                harga = int(input("Nominal (Angka saja): "))
                kateg = input("Kategori: ")

                simpan(tanggal, nama, harga, kateg)

            elif pilihan == "/hapus":
                lihat_data()
                target = int(input("\nMasukkan data yang mau dihapus: "))
                hapus_data(int(target))

            elif pilihan == "/Lihat Data":
                lihat_data()

            elif pilihan == "/keluar":
                print("Program dimatikan. Data kamu aman di database!")
                break
            else:
                print("Pilihan Salah!")
            
            if pilihan != "/keluar":
                print("\nKembali ke menu utama dalam 2 detik...")
menu()