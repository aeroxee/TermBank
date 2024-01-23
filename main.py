from termbank.db import DB
import logging
from termbank.akun import Akun
import time
from typing import List

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] - %(message)s", filename="termbank.log", filemode="a")

# apakah user ini terautentikasi
IS_AUTHENTICATED = False
USER = None

def menu_utama():
    print("""
Selamat Datang Di TermBank

1. Login
2. Daftar
3. Exit
""")
    
def menu_home(user: List):
    print("""
Halo, %s

1. Tambah Saldo
2. Cek Saldo
3. Transfer
4. Penarikan
5. Logout
""" % user[1])

def main():
    global IS_AUTHENTICATED, USER
    db = DB("root", "root")
    akun = Akun(db)
    
    if not IS_AUTHENTICATED:
        menu_utama()
        pilihan = int(input("Silahkan pilih menu [1/2/3]: "))
        if pilihan == 1:
            email = str(input("Masukkan alamat email: "))
            pin = int(input("Masukkan pin: "))
            time.sleep(0.5) # Simulasi
            login = akun.login_akun(email, pin)
            if login:
                IS_AUTHENTICATED = True
                USER = db.mendapatkan_akun(email)
                main()
            else:
                IS_AUTHENTICATED = False
                main()
        elif pilihan == 2:
            nama_lengkap = str(input("Masukkan nama lengkap: "))
            email = str(input("Masukkan alaman email: "))
            nik = int(input("Masukkan NIK: "))
            pin = int(input("Masukkan pin: "))
            
            daftar = akun.daftar_akun(nama_lengkap, email, nik, pin)
            if (daftar):
                print("Pendaftaran akun berhasil. Silahkan login")
                time.sleep(3)
                main()
            else:
                print("Pendaftaran akun gagal, Alamat email atau NIK sudah terdaftar.")
                time.sleep(3)
                main()
        else:
            print("\n\n Terimakasih\n\n")
            exit(1)
    else:
        menu_home(USER)
        pilihan = int(input("\nMasukkan pilihan [1/2/3/4]: "))
        
        # Tambah saldo
        if pilihan == 1:
            rekening = db.mendapatkan_rekening(id_akun=USER[0])
            print("Saldo Anda: %d" % rekening[3])
            a = int(input("Masukkan jumlah penambahan saldo: "))
            
            #update rekening
            update_rekening = db.update_rekening(USER[0], rekening[2], a)
            if (update_rekening):
                print("Saldo berhasil ditambahkan.")
                time.sleep(3)
                main()
            else:
                print("Ada kesalahan server kami.")
                time.sleep(3)
                main()
        # Cek saldo
        elif pilihan == 2:
            rekening = db.mendapatkan_rekening(id_akun=USER[0])
            print("\nSaldo anda: Rp.%d" % rekening[3])
            _ = input("\nTekan enter untuk kembali.")
            main()
        # Transfer
        elif pilihan == 3:
            rekening = db.mendapatkan_rekening(id_akun=USER[0])
            print("\nSaldo anda: Rp.%d" % rekening[3])
            rek_tujuan = int(input("Masukkan nomor rekening tujuan: "))
            jumlah = int(input("Masukkan nominal transfer: "))
            rekening_target = db.mendapatkan_rekening(nomor_rekening=rek_tujuan)
            # Update rek tujuan
            update_rek_tujuan = db.update_rekening(rekening_target[1], rekening_target[2], rekening_target[3]+jumlah)
            if (update_rek_tujuan):
                # Update rekening pengguna yang login.
                # Karena saldo berkurang karena sudah di transfer.
                update_rekening = db.update_rekening(rekening[1], rekening[2], rekening[3]-jumlah)
                if not update_rekening:
                    print("Berhasil upda.")
                    time.sleep(3)
                    main()
                
                print("Transfer berhasil ke rekening %d dengan nominal Rp.%d." % (rekening_target[2], jumlah))
                _ = input("\nTekan enter untuk kembali.")
                main()
            else:
                print("Ada kesalahan server.")
                _ = input("\nTekan enter untuk kembali.")
                main()
        # Penarikan
        elif pilihan == 4:
            rekening = db.mendapatkan_rekening(id_akun=USER[0])
            print("Saldo anda: Rp.%d" % rekening[3])
            jumlah = int(input("Masukkan nominal penarikan: "))
            update_rekening = db.update_rekening(rekening[1], rekening[2], rekening[3]-jumlah)
            if (update_rekening):
                print("\nPenarikan berhasil.")
                time.sleep(3)
                main()
            else:
                print("\nPenarikan gagal.")
                time.sleep(3)
                main()
        else:
            print("\n\nTerimakasih\n")
            exit(1)

if __name__ == "__main__":
    main()