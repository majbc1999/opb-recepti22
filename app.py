#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottletext import get, post, run, request, template, redirect, static_file, url, response, template_user


# uvozimo ustrezne podatke za povezavo

from Database import Repo
from model import *
from uporabnik import AuthService
from functools import wraps

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

repo = Repo()
auth = AuthService(repo)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        
           
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        
        return template("prijava.html", napaka="Potrebna je prijava!")

     
        
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')



@get('/')
@cookie_required
def zacetna_stran():
    """
    Domača stran.
    """
    kategorije = repo.kategorije()
        
    return template_user('kategorije.html', skip=0, take=10, kategorije=kategorije)
 
    
@get("/kategorije/<skip:int>/<take:int>/")
@cookie_required
def prikazi_kategorijo(skip,take):    
    
    kategorije = repo.kategorije(skip=skip, take=take )
    return template_user('kategorije.html',skip=skip, take=take, kategorije=kategorije)
    
    
    

@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        
        redirect(url('index'))
        
    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
    
@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', napaka=None)


@get('/prikazi_kategorijo')
def prikazi_kategorijo():
    kategorije = repo.dobi_gen(VseKategorije, 100,0)

    return template_user('prikazi_kategorijo.html', kategorije=kategorije)

@post('/prikazi_kategorijo')
def prikazi_kategorijo_post():
    kategorija = str(request.forms.get('kategorija'))
    #kakoo dobit recepte iz te kategorije?? verjetno ni kul da nimava nikjer v modelu kategorij s svojim id-jem?


#@post('/dodaj_izdelek')
#def dodaj_izdelek_post():
#
#    kategorija_id = int(request.forms.get('kategorija'))
#    ime = str(request.forms.get('ime'))
#    leto = request.forms.get('leto')
#    cena = float(request.forms.get('cena'))
#
#    izdelek = repo.dodaj_izdelek(Izdelek(
#        ime=ime,
#        kategorija=kategorija_id
#    ))
#
#    cena_izdelka = repo.dodaj_ceno_izdelka(CenaIzdelka(
#        izdelek_id=izdelek.id,
#        leto=leto,
#        cena=cena
#    ))
#
#    
#    
#    redirect(url('izdelki', skip=0, take=10))
#@get('/dodaj_kategorijo')
#def dodaj_kategorijo():
#    
#    return template_user('dodaj_kategorijo.html', kategorija = KategorijaIzdelka())
#
#@post('/dodaj_kategorijo')
#def dodaj_kategorijo_post():
#    oznaka = request.forms.get("kategorija")
#
#    repo.dodaj_gen(KategorijaIzdelka(oznaka=oznaka))
#    redirect(url('kategorije', skip=0, take=100))
#




######################################################################
# Glavni program



# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)