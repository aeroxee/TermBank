import mysql.connector
import logging
from typing import List
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

    
    def mendapatkan_akun(self, email: str) -> List:
        try:
            sql = "SELECT * FROM akun WHERE email= %s"
            self.cursor.execute(sql, (email,))
            results = self.cursor.fetchone()
            return results
        except mysql.connector.Error as err:
            logging.error("Error: %s" % err)
            return []
    
    
    def update_rekening(self, id_akun: int, nomor_rekening: int, saldo: int) -> bool:
        """Fungsi untuk mengupdate rekening

        Args:
            nomor_rekening (int): nomor rekening
            saldo (int): saldo

        Returns:
            bool: _description_
        """
        try:
            sql = "UPDATE rekening SET nomor_rekening=%s, saldo=%s WHERE id_akun=%s"
            self.cursor.execute(sql, (nomor_rekening, saldo, id_akun))
            self.cnx.commit()
            
            if self.cursor.rowcount > 0:
                logging.info("Update rekening berhasil")
                return True
            else:
                logging.error("Update rekening gagal")
                return False
        except mysql.connector.Error as err:
            logging.error("Update rekening gagal: %s" % err)
            return False
    
    
    def mendapatkan_rekening(self, id_akun: int = None, nomor_rekening: int = None) -> List:
        """Fungsi untuk mendapatkan info rekening.

        Args:
            id_akun (int): id akun pengguna

        Returns:
            List: _description_
        """
        try:
            if id_akun is None:
                sql = "SELECT * FROM rekening WHERE nomor_rekening=%s"
                self.cursor.execute(sql, (nomor_rekening,))
            else:
                sql = "SELECT * FROM rekening WHERE id_akun=%s"
                self.cursor.execute(sql, (id_akun,))
            results = self.cursor.fetchone()
            
            return results
        except mysql.connector.Error as err:
            logging.error("Mysql Error get rekening: %s" % err)
            return []