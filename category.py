from database import connect_db

# CREATE
def insert_category(name, description):
    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
    cursor.execute(query, (name, description))
    db.commit()
    print("Kategori berhasil ditambahkan")
    cursor.close()
    db.close()

# READ (Semua data)
def get_all_categories():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM categories"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Daftar semua Kategori:")
    for row in rows:
        print(row)
    cursor.close()
    db.close()

# READ (By ID)
def get_category_by_id(category_id):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM categories WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    row = cursor.fetchone()
    if row:
        print("Data Kategori:", row)
    else:
        print("Kategori tidak ditemukan")
    cursor.close()
    db.close()

# UPDATE
def update_category(category_id, name = None, description = None):
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

    if not fields:
        print("Tidak ada data yang diperbarui.")
        return

    query = f"UPDATE categories SET {', '.join(fields)} WHERE category_id = %s"
    values.append(category_id)

    cursor.execute(query, values)
    db.commit()
    print("Data berhasil diperbarui")
    cursor.close()
    db.close()

# DELETE
def delete_category(category_id):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM categories WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    db.commit()
    print("Kategori berhasil dihapus")
    cursor.close()
    db.close()

# Fungsi utama untuk menampilkan menu
def show_menu():
    print("\n====== Menu Kategori ======")
    print("1. Tambah Kategori")
    print("2. Tampilkan Semua Kategori")
    print("3. Tampilkan Kategori Berdasarkan ID")
    print("4. Edit Kategori")
    print("5. Hapus Kategori")
    print("6. Keluar")

# Fungsi untuk menangani input pengguna
def handle_category():
    while True:
        show_menu()
        choice = input("Pilih menu (1-6): ")

        if choice == '1':
            name = input("Masukkan nama kategori: ")
            description = input("Masukkan deskripsi kategori: ")
            insert_category(name, description)

        elif choice == '2':
            get_all_categories()

        elif choice == '3':
            category_id = int(input("Masukkan ID kategori: "))
            get_category_by_id(category_id)

        elif choice == '4':
            category_id = int(input("Masukkan ID kategori yang ingin diupdate: "))
            name = input("Masukkan nama kategori baru (tekan Enter untuk skip): ")
            description = input("Masukkan deskripsi kategori baru (tekan Enter untuk skip): ")
            update_category(category_id, name, description)

        elif choice == '5':
            category_id = int(input("Masukkan ID kategori yang ingin dihapus: "))
            delete_category(category_id)

        elif choice == '6':
            print("Terima kasih, keluar dari program.")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi")

