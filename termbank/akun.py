from .db import DB
import logging, hashlib

class Akun(DB):
    """Kelas ini untuk mengimplementasikan objek-objek yang berkaitan dengan akun.
    """
    
    def __init__(self, db: DB):
        super().__init__(db.cnx._user, db.cnx._password, db.cnx._host, db.cnx._database)
    
    
    def login_akun(self, email: str, pin: int) -> bool:
        """Login akun

        Args:
            email (str): _description_
            pin (int): _description_

        Returns:
            bool: _description_
        """
        
        akun = self.mendapatkan_akun(email)
        if len(akun) > 0:
            enc_pin = akun[4]
            pin = hashlib.sha256(str(pin).encode('utf-8')).hexdigest()
            if (enc_pin != pin):
                return False
            else:
                return True
        else:
            return False