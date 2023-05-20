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
        try:
            user = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabnisko_ime")
            return True
        except:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> Union[UporabnikDto, bool] :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabnisko_ime")

        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.geslo.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.zadnji_login = date.today().isoformat()
            self.repo.posodobi_gen(user, id_col="upoabnisko_ime")
            return UporabnikDto(uporabnisko_ime=user.uporabnisko_ime, id=user.id)
        
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
            uporabnisko_ime=uporabnik,
            geslo=password_hash.decode(),
            zadnji_login= date.today().isoformat()
        )

        self.repo.uporabnik(uporabnik)

        return UporabnikDto(uporabnisko_ime=uporabnik, id=uporabnik.id)