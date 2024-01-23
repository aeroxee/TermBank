import mysql.connector
import logging
import random
import hashlib

class DB:
    """Ini adalah kelas untuk membuat koneksi database.
    """
    
    def __init__(self, user: str, password: str, 
                 host: str = "localhost", database: str = "db_bank"):
        """Inisialisasi untuk kelas koneksi.

        Args:
            user (str): username untuk database
            password (str): password untuk database.
            host (str, optional): hostname untuk server database. Defaults to "localhost".
            database (str, optional): nama dari database. Defaults to "db_bank".
        """
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           host=host, database=database)
        self.cursor = self.cnx.cursor()
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    
    def daftar_akun(self, nama_lengkap: str, email: str, nik: int, pin: int) -> bool:
        """Fungsi ini untuk mendaftarkan akun pengguna ke dalam database.
        Fungsi ini juga akan membuatkan nomor rekening langsung.

        Args:
            nama_lengkap (str): nama lengkap pengguna
            email (str): alaman email pengguna
            nik (int): nomor induk kependudukan pengguna
            pin (int): pin untuk login akun
        """
        try:
            sql = "INSERT INTO akun (nama_lengkap, email, nik, pin) VALUES (%s, %s, %s, %s)"
            pin_encrypt = self.__enkripsi_pin(pin)
            self.cursor.execute(sql, (nama_lengkap, email, nik, pin_encrypt))
            self.cnx.commit()
            if self.cursor.rowcount > 0:
                logging.info("Satu data berhasil di insert kedalam tabel akun.")
                id_akun = self.cursor.lastrowid # ID pengguna yang baru saja di insert.
                # Tambah data rekening
                nomor_rekening = self.__get_angka_random()
                try:
                    sql = "INSERT INTO rekening (id_akun, nomor_rekening) VALUES (%s, %s)"
                    self.cursor.execute(sql, (id_akun, nomor_rekening))
                    self.cnx.commit()
                    if self.cursor.rowcount > 0:
                        logging.info("Tambah rekening sukses.")
                        return True
                    else:
                        logging.error("Tambah rekening gagal")
                        return False
                except mysql.connector.Error as err:
                    logging.error("Tambah rekening error: %s" % err.msg)
                    return False
            else:
                logging.error("Data akun gagal di insert.")
                return False
        except mysql.connector.Error as err:
            logging.error("Insert data akun error: %s" % err.msg)
            return False
    
    def __get_angka_random(self) -> int:
        """Fungsi untuk mengambil 15 digit angka acak untuk pemberian nomor rekening ke
        pelanggan.
        """
        random_number = "".join([str(random.randint(0, 9)) for _ in range(15)])
        return random_number
    
    def __enkripsi_pin(self, pin: int) -> str:
        """Fungsi untuk mengenkripsi pin

        Args:
            pin (int): _description_

        Returns:
            str: pesan enkripsi
        """
        pin_encrypt = hashlib.sha256(str(pin).encode("utf-8")).hexdigest()
        return pin_encrypt