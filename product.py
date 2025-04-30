from database import connect_db

# insert product with detail
def insert_product(category_id, name, description, price, color, size, weight, stock):
    db = connect_db()
    cursor = db.cursor()
    
    # Insert ke tabel products
    query = "INSERT INTO products (category_id, name, description, price) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (category_id, name, description, price))
    db.commit()
    
    # Ambil ID produk yang baru saja dibuat
    product_id = cursor.lastrowid

    # Insert ke tabel product_details
    query_detail = """
        INSERT INTO product_details (product_id, color, size, weight, stock)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query_detail, (product_id, color, size, weight, stock))
    db.commit()
    print("Produk baru berhasil ditambahkan")
    
    cursor.close()
    db.close()

# get all products with detail
def get_all_products_with_details():
    db = connect_db()
    cursor = db.cursor()

    query = """
        SELECT p.product_id, c.name AS category, p.name, p.description, p.price,
               d.product_detail_id, d.color, d.size, d.weight, d.stock
        FROM products p
        LEFT JOIN product_details d ON p.product_id = d.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nDaftar semua Produk dan Detailnya:")
    for row in rows:
        print(f"Produk ID: {row[0]}, Kategori: {row[1]} Nama: {row[2]}, Deskripsi: {row[3]}, Harga: {row[4]}")
        if row[5]:  
            print(f"Detail ID: {row[5]}, Warna: {row[6]}, Ukuran: {row[7]}, Berat: {row[8]}kg, Stok: {row[9]}")
        else:
            print("Detail produk tidak ada")
    cursor.close()
    db.close()


# get product by id with detail
def get_product_by_id_with_details(product_id):
    db = connect_db()
    cursor = db.cursor()

    query = """
         SELECT p.product_id, c.name AS category, p.name, p.description, p.price,
               d.product_detail_id, d.color, d.size, d.weight, d.stock
        FROM products p
        LEFT JOIN product_details d ON p.product_id = d.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """
    cursor.execute(query, (product_id,))
    row = cursor.fetchone()

    if row:
        print("\nData Produk:")
        print(f"Produk ID: {row[0]}, Kategori: {row[1]} Nama: {row[2]}, Deskripsi: {row[3]}, Harga: {row[4]}")
        if row[5]:  
            print(f"Detail ID: {row[5]}, Warna: {row[6]}, Ukuran: {row[7]}, Berat: {row[8]}kg, Stok: {row[9]}")
        else:
            print("Detail produk tidak ada")
    else:
        print("Produk tidak ditemukan")

    cursor.close()
    db.close()

# update product with detail
def update_product_with_details(product_id, category_id=None, name=None, description=None, price=None, color=None, size=None, weight=None, stock=None):
    db = connect_db()
    cursor = db.cursor()

    product_fields = []
    product_values = []

    detail_fields = []
    detail_values = []

    # Untuk update tabel products
    if category_id:
        product_fields.append("category_id = %s")
        product_values.append(category_id)
    if name:
        product_fields.append("name = %s")
        product_values.append(name)
    if description:
        product_fields.append("description = %s")
        product_values.append(description)
    if price:
        product_fields.append("price = %s")
        product_values.append(price)

    # Untuk update tabel product_details
    if color:
        detail_fields.append("color = %s")
        detail_values.append(color)
    if size:
        detail_fields.append("size = %s")
        detail_values.append(size)
    if weight:
        detail_fields.append("weight = %s")
        detail_values.append(weight)
    if stock:
        detail_fields.append("stock = %s")
        detail_values.append(stock)

    if not product_fields and not detail_fields:
        print("Tidak ada data yang diperbarui.")
        cursor.close()
        db.close()
        return

    # Update products
    if product_fields:
        product_query = f"UPDATE products SET {', '.join(product_fields)} WHERE product_id = %s"
        product_values.append(product_id)
        cursor.execute(product_query, product_values)

    # Update product_details
    if detail_fields:
        detail_query = f"UPDATE product_details SET {', '.join(detail_fields)} WHERE product_id = %s"
        detail_values.append(product_id)
        cursor.execute(detail_query, detail_values)

    db.commit()

    print("Data produk beserta detailnya berhasil diperbarui")

    cursor.close()
    db.close()

# delete product with detail
def delete_product_with_details(product_id):
    db = connect_db()
    cursor = db.cursor()

    # Hapus dulu product_details (kalau ada)
    delete_details_query = "DELETE FROM product_details WHERE product_id = %s"
    cursor.execute(delete_details_query, (product_id,))

    # Baru hapus product
    delete_product_query = "DELETE FROM products WHERE product_id = %s"
    cursor.execute(delete_product_query, (product_id,))

    db.commit()
    print("Produk beserta detailnya berhasil dihapus")
    cursor.close()
    db.close()


# Fungsi utama untuk menampilkan menu
def show_menu():
    print("\n====== Menu Produk ======")
    print("1. Tambah Produk")
    print("2. Tampilkan Semua Produk")
    print("3. Tampilkan Produk Berdasarkan ID")
    print("4. Edit Produk")
    print("5. Hapus Produk")
    print("6. Keluar")

# Fungsi untuk menangani input pengguna
def handle_product():
    while True:
        show_menu()
        choice = input("Pilih menu (1-6): ")

        if choice == '1':
            category_id = int(input("Masukkan kategori produk: "))
            name = input("Masukkan nama produk: ")
            description = input("Masukkan deskripsi produk: ")
            price = float(input("Masukkan harga produk: "))
            color = input("Masukkan warna produk: ")
            size = input("Masukkan ukuran produk: ")
            weight = float(input("Masukkan berat produk: "))
            stock = int(input("Masukkan stok produk: "))
            insert_product(category_id, name, description, price, color, size, weight, stock)

        elif choice == '2':
            get_all_products_with_details()

        elif choice == '3':
            product_id = int(input("Masukkan ID produk: "))
            get_product_by_id_with_details(product_id)

        elif choice == '4':
            product_id = int(input("Masukkan ID produk yang ingin diupdate: "))
            category_input = input("Masukkan kategori produk baru (tekan Enter untuk skip): ")
            category = int(category_input) if category_input else None
            name = input("Masukkan nama produk baru (tekan Enter untuk skip): ")
            description = input("Masukkan deskripsi produk baru (tekan Enter untuk skip): ")
            price_input = input("Masukkan harga produk baru (tekan Enter untuk skip): ")
            price = float(price_input) if price_input else None
            color = input("Masukkan warna produk baru (tekan Enter untuk skip): ")
            size = input("Masukkan ukuran produk baru (tekan Enter untuk skip): ")
            weight_input = input("Masukkan berat produk baru dalam kg (tekan Enter untuk skip): ")
            weight = float(weight_input) if weight_input else None
            stock_input = input("Masukkan stok produk baru (tekan Enter untuk skip): ")
            stock = int(stock_input) if stock_input else None
            update_product_with_details(product_id, category, name, description, price, color, size, weight, stock)

        elif choice == '5':
            product_id = int(input("Masukkan ID produk yang ingin dihapus: "))
            delete_product_with_details(product_id)

        elif choice == '6':
            print("Kembali ke Menu Utama")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi")

