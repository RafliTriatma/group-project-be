# index.py

from user import handle_user as user_menu
from transaction import handle_transaction as transaction_menu
from transaction_voucher import handle_transaction_voucher as transaction_voucher_menu
from product import handle_product as product_menu
from product_voucher import handle_product_voucher as product_voucher_menu
from category import handle_category as category_menu

def main_menu():
    while True:
        print("\n====== Menu ======")
        print("1. Pengguna")
        print("2. Transaksi")
        print("3. Produk")
        print("4. Kategori")
        print("5. Voucher Produk")
        print("6. Voucher Transaksi")
        print("7. Keluar")

        try:
            choice = int(input("Pilih menu (1-7): "))
        except ValueError:
            print("Masukkan angka!")
            continue

        if choice == 1:
            user_menu()
        elif choice == 2:
            transaction_menu()
        elif choice == 3:
            product_menu()
        elif choice == 4:
            category_menu()
        elif choice == 5:
            product_voucher_menu()
        elif choice == 6:
            transaction_voucher_menu()
        elif choice == 7:
            print("Terima kasih")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi")

if __name__ == "__main__":
    main_menu()
