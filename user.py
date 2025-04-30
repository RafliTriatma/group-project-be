from database import connect_db

# CREATE
def insert_user(name, email, password, address, phone_number):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO users (name, email, password, address, phone_number)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, email, password, address, phone_number))
    db.commit()
    print("Data berhasil disimpan")
    cursor.close()
    db.close()

# READ (Semua pengguna)
def get_all_users():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Daftar semua pengguna:")
    for row in rows:
        print(row)
    cursor.close()
    db.close()

# READ (By ID)
def get_user_by_id(user_id):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if row:
        print("Data Pengguna:", row)
    else:
        print("Pengguna tidak ditemukan")
    cursor.close()
    db.close()

# UPDATE
def update_user(user_id, name=None, email=None, address=None, phone_number=None):
    db = connect_db()
    cursor = db.cursor()

    fields = []
    values = []

    if name:
        fields.append("name = %s")
        values.append(name)
    if email:
        fields.append("email = %s")
        values.append(email)
    if address:
        fields.append("address = %s")
        values.append(address)
    if phone_number:
        fields.append("phone_number = %s")
        values.append(phone_number)
    if not fields:
        print("Tidak ada data yang diperbarui")
        return

    query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s"
    values.append(user_id)

    cursor.execute(query, values)
    db.commit()
    print("Data berhasil diperbarui")
    cursor.close()
    db.close()

# DELETE
def delete_user(user_id):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    db.commit()
    print("Data berhasil dihapus")
    cursor.close()
    db.close()

# Fungsi utama untuk menampilkan menu
def show_menu():
    print("\n====== Menu Pengguna ======")
    print("1. Tambah Pengguna Baru")
    print("2. Tampilkan Semua Pengguna")
    print("3. Tampilkan Pengguna Berdasarkan ID")
    print("4. Edit Pengguna")
    print("5. Hapus Pengguna")
    print("6. Kembali ke Menu Utama")

def handle_user():
    while True:
        show_menu()
        choice = input("Pilih menu (1-6): ")

        if choice == '1':
            name = input("Masukkan nama pengguna: ")
            email = input("Masukkan email pengguna: ")
            password = input("Masukkan password pengguna: ")
            address = input("Masukkan alamat pengguna: ")
            phone_number = input("Masukkan nomor telepon pengguna: ")
            insert_user(name, email, password, address, phone_number)

        elif choice == '2':
            get_all_users()

        elif choice == '3':
            user_id = int(input("Masukkan ID pengguna: "))
            get_user_by_id(user_id)

        elif choice == '4':
            user_id = int(input("Masukkan ID pengguna yang ingin diedit: "))
            name = input("Masukkan nama pengguna baru (tekan Enter untuk lewati): ")
            email = input("Masukkan email pengguna baru (tekan Enter untuk lewati): ")
            address = input("Masukkan alamat pengguna baru (tekan Enter untuk lewati): ")
            phone_number = input("Masukkan nomor telepon pengguna baru (tekan Enter untuk skip): ")
            update_user(user_id, name if name else None, email if email else None, address if address else None, phone_number if phone_number else None)

        elif choice == '5':
            user_id = int(input("Masukkan ID pengguna yang ingin dihapus: "))
            delete_user(user_id)

        elif choice == '6':
            print("Kembali ke Menu Utama")
            return

        else:
            print("Pilihan tidak valid, silakan coba lagi")
