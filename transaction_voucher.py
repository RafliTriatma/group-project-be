from database import connect_db

def insert_transaction_voucher(name, description, price):
    db = connect_db()
    cursor = db.cursor()

    query = """
        INSERT INTO voucher_transactions (name, description, price)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, description, price))
    db.commit()

    print("Data voucher transaksi berhasil disimpan")

    cursor.close()
    db.close()

def get_all_transaction_vouchers():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT voucher_id, name, description, price FROM voucher_transactions"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Daftar semua voucher transaksi:")
    for row in rows:
        print(f"ID Voucher: {row[0]}, Nama: {row[1]}, Deskripsi: {row[2]}, Harga: {row[3]}")
    cursor.close()
    db.close()

def get_transaction_voucher_by_id(voucher_id):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT voucher_id, name, description, price FROM voucher_transactions WHERE voucher_id = %s"
    cursor.execute(query, (voucher_id,))
    row = cursor.fetchone()
    if row:
        print("Data Voucher Transaksi:", row)
    else:
        print("Voucher transaksi tidak ditemukan")
    cursor.close()
    db.close()

def update_transaction_voucher(voucher_id, name=None, description=None, price=None):
    db = connect_db()
    cursor = db.cursor()

    fields = []
    values = []

    if name:
        fields.append("name = %s")
        values.append(name)
    if description:
        fields.append("description = %s")
        values.append(description)
    if price:
        fields.append("price = %s")
        values.append(price)
    if not fields:
        print("Tidak ada data yang diperbarui")
        return

    query = f"UPDATE voucher_transactions SET {', '.join(fields)} WHERE voucher_id = %s"
    values.append(voucher_id)

    cursor.execute(query, values)
    db.commit()
    print("Data berhasil diperbarui")
    cursor.close()
    db.close()

def delete_transaction_voucher(voucher_id):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM voucher_transactions WHERE voucher_id = %s"
    cursor.execute(query, (voucher_id,))
    db.commit()
    print("Data berhasil dihapus")
    cursor.close()
    db.close()

def show_menu():
    print("\n====== Menu Voucher Transaksi ======")
    print("1. Tambah Voucher Transaksi Baru")
    print("2. Tampilkan Semua Voucher Transaksi")
    print("3. Tampilkan Voucher Transaksi Berdasarkan ID")
    print("4. Edit Voucher Transaksi")
    print("5. Hapus Voucher Transaksi")
    print("6. Kembali ke Menu Utama")

def handle_transaction_voucher():
    while True:
        show_menu()
        choice = input("Pilih menu (1-6): ")

        if choice == '1':
            name = input("Masukkan nama voucher: ")
            description = input("Masukkan deskripsi voucher: ")
            price = input("Masukkan harga voucher: ")
            
            insert_transaction_voucher(name, description, price)

        elif choice == '2':
            get_all_transaction_vouchers()

        elif choice == '3':
            voucher_id = int(input("Masukkan ID voucher transaksi: "))
            get_transaction_voucher_by_id(voucher_id)

        elif choice == '4':
            voucher_id = int(input("Masukkan ID voucher yang ingin diedit: "))
            name = input("Masukkan nama voucher terbaru (tekan Enter untuk lewati): ")
            description = input("Masukkan deskripsi terbaru (tekan Enter untuk lewati): ")
            price = input("Masukkan harga terbaru (tekan Enter untuk lewati): ")
            
            update_transaction_voucher(voucher_id, name if name else None, description if description else None, price if price else None)

        elif choice == '5':
            voucher_id = int(input("Masukkan ID voucher yang ingin dihapus: "))
            delete_transaction_voucher(voucher_id)

        elif choice == '6':
            print("Kembali ke Menu Utama")
            return

        else:
            print("Pilihan tidak valid, silakan coba lagi")