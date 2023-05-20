from Database import Repo
from model import *
from typing import Dict
from re import sub
import dataclasses
import bcrypt
from typing import Type
from datetime import date
from typing import Union

class AuthService:

    repo : Repo
    def __init__(self, repo : Repo):
        
        self.repo = repo

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        user = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabnisko_ime")
        if user:
            return True
        else:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> Union[UporabnikDto, bool] :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabnisko_ime")

        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.password_hash.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.last_login = date.today().isoformat()
            self.repo.posodobi_gen(user, id_col="upoabnisko_ime")
            return UporabnikDto(username=user.username, id_uporabnika=user.id_uporabnika)
        
        return False

    def dodaj_uporabnika(self, uporabnik: str, geslo: str) -> UporabnikDto:
        
        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        uporabnik = Uporabnik(
            username=uporabnik,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat()
        )

        self.repo.uporabnik(uporabnik)

        return UporabnikDto(username=uporabnik, id_uporabnika=uporabnik.id_uporabnika)