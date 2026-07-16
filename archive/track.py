semua_pengeluaran = []

def keluar():
    print("\n--- Catatan Pengeluaran Kamu ---")
    try:
        barang = input("Masukkan nama barang atau kegiatan: ")
        nominal = int(input("Masukkan nominal (angka saja): "))
        kategori = input("Masukkan kategori: ")

        data = {
            "nama": barang,
            "nominal": nominal,
            "kategori": kategori
        }

        semua_pengeluaran.append(data)
        print("✅ Data berhasil dicatat!")
    except ValueError:
        print("Error: Nominal harus angka!")

def laporan():
    print("n\--- Laporan Pengeluaran ---")
    total = 0
    for item in semua_pengeluaran:
        print(f"- {item['nama']} ({item['kategori']}): Rp{item['nominal']}")
        total += item['nominal']
    print(f"n\Total Pengeluaran: Rp{total}")

def hapus_data():
    print("n\--- HAPUS DATA PENGELUARAN ---")

    if not semua_pengeluaran:
        print("Belum ada data.")
        return
    for index, item in enumerate(semua_pengeluaran):
        print(f"{index}. {item['nama']} - Rp{item['nominal']}")

    try:
        pilihan = int(input("\Masukkan nomor yang ingin dihapus: "))

        data_terhapus = semua_pengeluaran.pop(pilihan)
        print(f"✅ Berhasil menghapus: {data_terhapus['nama']}")

    except IndexError:
        print("Datanya error woi: Nomor ga diketahui.")
    except ValueError:
        print("Datanya error: Masukin angka, bukan huruf!") 

while True:
    print("\n=== SMART BUDGET TRACKER ===")
    print("1. Tambah Pengeluaran")
    print("2. Hapus Pengeluaran")
    print("3. Lihat Laporan")
    print("4. Keluar")

    pilihan = input("Ketik pilihanmu dengan angka (1/2/3): ")

    if pilihan == "1":
        keluar()
    elif pilihan == "2":
        laporan()
    elif pilihan == "3":
        hapus_data()
    elif pilihan == "4":
        print("Terimakasih sudah memakai, sampai jumpa.")
        break
    else:
        print("Pilihan tidak valid.")