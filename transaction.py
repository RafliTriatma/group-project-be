from database import connect_db

# CREATE
def insert_transaction(user_id, product_detail_id, quantity, status):
    db = connect_db()
    cursor = db.cursor()
    
    try:
        # Step 1: Ambil harga produk dari product_detail_id
        query_price = """
            SELECT p.price
            FROM product_details pd
            JOIN products p ON pd.product_id = p.product_id
            WHERE pd.product_detail_id = %s
        """
        cursor.execute(query_price, (product_detail_id,))
        result = cursor.fetchone()

        price = result[0]
        purchase_price = price * quantity

        # Step 2: Insert ke tabel transactions
        query_transaction = """
            INSERT INTO transactions (user_id, total_amount, status)
            VALUES (%s, %s, %s)
        """
        values_transaction = (user_id, purchase_price, status)
        cursor.execute(query_transaction, values_transaction)

        # Step 3: Ambil transaction_id baru
        transaction_id = cursor.lastrowid

        # Step 4: Insert ke tabel transaction_details
        query_detail = """
            INSERT INTO transaction_details (transaction_id, product_detail_id, quantity, purchase_price)
            VALUES (%s, %s, %s, %s)
        """
        values_detail = (transaction_id, product_detail_id, quantity, purchase_price)
        cursor.execute(query_detail, values_detail)

        # Selesai
        db.commit()
        print(f"Transaksi berhasil ditambahkan (ID Transaksi: {transaction_id}, Total Harga: {purchase_price})")
    
    except Exception as e:
        db.rollback()
        print("Terjadi error:", e)
    
    finally:
        cursor.close()
        db.close()

# READ (Semua transaksi)
def get_all_transactions():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.transaction_id, u.name, td.quantity, p.price, t.total_amount, t.status
        FROM transactions t
        LEFT JOIN users u ON t.user_id = u.user_id
        LEFT JOIN transaction_details td ON t.transaction_id = td.transaction_id
        LEFT JOIN product_details pd ON td.product_detail_id = pd.product_detail_id
        LEFT JOIN products p ON pd.product_id = p.product_id
    """)
    results = cursor.fetchall()
    print("Daftar semua transaksi:")
    for row in results:
        print(f"ID Transaksi: {row[0]}, Pengguna: {row[1]}, Kuantitas: {row[2]}, Harga Satuan: {row[3]}, Total Harga: {row[4]}, Status: {row[5]}")
    cursor.close()
    db.close()

# READ (By ID)
def get_transaction_by_id(transaction_id):
    db = connect_db()
    cursor = db.cursor()
    query = """
        SELECT t.transaction_id, u.name, td.quantity, p.price, t.total_amount, t.status
        FROM transactions t
        LEFT JOIN users u ON t.user_id = u.user_id
        LEFT JOIN transaction_details td ON t.transaction_id = td.transaction_id
        LEFT JOIN product_details pd ON td.product_detail_id = pd.product_detail_id
        LEFT JOIN products p ON pd.product_id = p.product_id
        WHERE t.transaction_id = %s
    """
    cursor.execute(query, (transaction_id,))
    row = cursor.fetchone()
    if row:
        print("\nData Transaksi:")
        print(f"ID Transaksi: {row[0]}, Pengguna: {row[1]}, Kuantitas: {row[2]}, Harga Satuan: {row[3]}, Total Harga: {row[4]}, Status: {row[5]}")
    else:
        print("Data transaksi tidak ditemukan")
    cursor.close()
    db.close()

def update_transaction(transaction_id, quantity, status):
    db = connect_db()
    cursor = db.cursor()

    try:
        # Step 1: Ambil product_detail_id berdasarkan transaction_id
        query_get_detail = """
            SELECT product_detail_id
            FROM transaction_details
            WHERE transaction_id = %s
        """
        cursor.execute(query_get_detail, (transaction_id,))
        result_detail = cursor.fetchone()

        if result_detail is None:
            raise Exception("Data transaksi tidak ditemukan")

        product_detail_id = result_detail[0]

        # Step 2: Ambil harga produk berdasarkan product_detail_id
        query_price = """
            SELECT p.price
            FROM product_details pd
            JOIN products p ON pd.product_id = p.product_id
            WHERE pd.product_detail_id = %s
        """
        cursor.execute(query_price, (product_detail_id,))
        result_price = cursor.fetchone()

        if result_price is None:
            raise Exception("Data produk tidak ditemukan")

        price = result_price[0]
        new_purchase_price = price * quantity

        # Step 3: Update transaction_details (quantity & purchase_price)
        query_update_detail = """
            UPDATE transaction_details
            SET quantity = %s, purchase_price = %s
            WHERE transaction_id = %s
        """
        values_update_detail = (quantity, new_purchase_price, transaction_id)
        cursor.execute(query_update_detail, values_update_detail)

        # Step 4: Update transactions (total_amount & status)
        query_update_transaction = """
            UPDATE transactions
            SET total_amount = %s, status = %s
            WHERE transaction_id = %s
        """
        values_update_transaction = (new_purchase_price, status, transaction_id)
        cursor.execute(query_update_transaction, values_update_transaction)

        # Commit perubahan
        db.commit()
        print(f"Transaksi berhasil diperbarui (ID Transaksi: {transaction_id}, Total Harga: {new_purchase_price})")

    except Exception as e:
        db.rollback()
        print("Terjadi error saat memperbarui:", e)

    finally:
        cursor.close()
        db.close()


# DELETE
def delete_transaction(transaction_id):
    db = connect_db()
    cursor = db.cursor()
    
    delete_detail_query = "DELETE FROM transaction_details WHERE transaction_id = %s"
    cursor.execute(delete_detail_query, (transaction_id,))
    
    delete_transaction_query = "DELETE FROM transactions WHERE transaction_id = %s"
    cursor.execute(delete_transaction_query, (transaction_id,))

    db.commit()
    print("Data transaksi berhasil dihapus")
    cursor.close()
    db.close()

# Fungsi utama untuk menampilkan menu
def show_menu():
    print("\n====== Menu Transaksi ======")
    print("1. Tambah Transaksi")
    print("2. Tampilkan Semua Transaksi")
    print("3. Tampilkan Transaksi Berdasarkan ID")
    print("4. Edit Transaksi")
    print("5. Hapus Transaksi")
    print("6. Keluar")

# Fungsi untuk menangani input pengguna
def handle_transaction():
    while True:
        show_menu()
        choice = input("Pilih opsi (1-6): ")

        if choice == '1':
            user_id = int(input("ID Pengguna: "))
            product_detail_id = int(input("ID Produk: "))
            quantity = int(input("Kuantitas: "))
            status = input("Status (pending/success/failed): ")
    
            insert_transaction(user_id, product_detail_id, quantity, status)

        elif choice == '2':
            get_all_transactions()

        elif choice == '3':
            transaction_id = int(input("Masukkan ID Transaksi: "))
            get_transaction_by_id(transaction_id)

        elif choice == '4':
            transaction_id = int(input("Masukkan ID Transaksi yang mau diperbarui: "))
            quantity_input = input("Masukkan kuantitas baru: ")
            quantity = int(quantity_input) if quantity_input else None
            status = input("Masukkan status baru (pending/success/failed): ")

            update_transaction(transaction_id, quantity, status)

        elif choice == '5':
            transaction_id = int(input("Masukkan ID Transaksi yang ingin dihapus: "))
            delete_transaction(transaction_id)

        elif choice == '6':
            print("Kembali ke Menu Utama")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi")

