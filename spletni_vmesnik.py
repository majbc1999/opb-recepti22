from calendar import month
from sqlite3 import Timestamp
from bottletext import get, post, run, request, template, redirect, static_file, url, response, template_user

import bottletext
from operator import mod
import bottle 
import model
import Database
import operator
from Database import Repo
from uporabnik import AuthService
from functools import wraps
from datetime import datetime

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


r = Database.Repo()
repo = Repo()
auth = AuthService(repo)


kategorije = [x.kategorija for x in r.dobi_razlicne_gen_po_abecedi(model.Kategorije, 'kategorija')]
kulinarike = [x.kulinarika for x in r.dobi_razlicne_gen_po_abecedi(model.Kulinarike, 'kulinarika')]
oznake = [x.oznaka for x in r.dobi_razlicne_gen_po_abecedi(model.Oznake, 'oznaka')]
vse_sestavine = r.dobi_vse_gen(model.Sestavine)


def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnisko_ime")
        if cookie:
            return f(*args, **kwargs)
        return template("views/prijava.tpl", napaka="Potrebna je prijava!")
    return decorated


@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')


####################################### Začetna stran pred prijavo #######################################

@bottle.get('/')
def vsi_recepti():
    """
    Začetna stran vseh receptov, do katere lahko uporabnik dostopa neprijavljen.
    """
    recepti = r.dobi_vse_gen(model.Recepti)
    return template('views/front-page.tpl', kategorije=kategorije,
                                            kulinarike=kulinarike,
                                            oznake=oznake,
                                            recepti=recepti)

@bottle.get('/<param>/uredi')
def uredi(param: str):
    """
    Začetna stran, le da so recepti urejeni po določenem stolpcu.
    """
    recepti = r.gen_urejeno(model.Recepti, param)
    return template('views/front-page.tpl', kategorije=kategorije,
                                            kulinarike=kulinarike,
                                            oznake=oznake,
                                            recepti=recepti)


########################################### PRIJAVA IN ODJAVA ########################################### 

@bottle.get('/prijava')
def prijava_get():
    return template('prijava.tpl', napaka=None)


@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovem id.
    Drugače sporoči, da je prijava neuspešna in te usmeri na registracijo.
    """
    username = str(request.forms.get('uporabnisko_ime'))
    password = str(request.forms.get('geslo'))

    if not auth.obstaja_uporabnik(username):
        return template("views/registracija.tpl", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        bottle.response.set_cookie("uporabnisko_ime", username)
        bottle.response.set_cookie("id", str(prijava.id))

        return redirect(url('vsi_recepti_prijava'))
        
    else:
        return template("prijava.tpl", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
    

@bottle.get('/registracija')
def registracija_get():
    return template('registracija.tpl', napaka=None)


@post('/registracija')
def registracija():
    """
    Če je registracija uspešna, uporabnika prijavi in ustvari piškotke.
    """
    username = str(request.forms.get('uporabnisko_ime'))
    password = str(request.forms.get('geslo'))

    if auth.dodaj_uporabnika(username,password):
        prijava = auth.prijavi_uporabnika(username, password)
    else:
        return bottletext.template("registracija.tpl", napaka="Uporabnik s tem že obstaja")
    
    if prijava:
        response.set_cookie("uporabnisko_ime", username)
        response.set_cookie("id", str(prijava.id))

        return redirect(url('vsi_recepti_prijava'))

    
@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovem id-ju.
    """
    
    bottle.response.delete_cookie("uporabnisko_ime")
    bottle.response.delete_cookie("id")
    
    return template('prijava.tpl', napaka=None)


########################################## VSI RECEPTI ########################################## 

@bottle.get('/recepti')
@cookie_required
def vsi_recepti_prijava():
    """
    Podobno začetni strani, le da uporabnik ob svojih receptih dobi možnost urejanja in brisanja receptov.
    """
    recepti = r.dobi_vse_gen(model.Recepti)
    id_uporabnika = int(bottle.request.get_cookie('id'))
    return template_user('views/front_prijava.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=recepti,
                                                    id_uporabnika=id_uporabnika)

@bottle.get('/<param>/uredi_vsi')
@cookie_required
def uredi_vsi(param: str):
    """
    Urejeni recepti po določenem stolpcu.
    """
    recepti = r.gen_urejeno(model.Recepti, param)
    id_uporabnika = int(bottle.request.get_cookie('id'))
    return template_user('views/front_prijava.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=recepti,
                                                    id_uporabnika=id_uporabnika)


##################################### RECEPTI PRIJAVLJENEGA UPORABNIKA #####################################

@bottle.get('/moji_recepti')
@cookie_required
def moji_recepti():
    """
    Seznam vseh receptov uporabnika. 
    """
    uporabnik = bottle.request.get_cookie('id')
    uporabnikovi_recepti = r.dobi_vse_gen_id(model.Recepti, uporabnik, "id_uporabnika")
    id_uporabnika = int(bottle.request.get_cookie('id'))
    return template_user('views/front_uporabnik.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=uporabnikovi_recepti,
                                                    id_uporabnika=id_uporabnika)

@bottle.get('/<param>/uredi_moji')
@cookie_required
def uredi_moji(param: str):
    """
    Urejeni recepti prijavljenega uporabnika.
    """
    uporabnik = bottle.request.get_cookie('id')
    uporabnikovi_recepti = r.dobi_vse_gen_id_urejeno(model.Recepti, param, uporabnik, "id_uporabnika")
    id_uporabnika = int(bottle.request.get_cookie('id'))
    return template_user('views/front_uporabnik.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=uporabnikovi_recepti,
                                                    id_uporabnika=id_uporabnika)


###################################### RECEPTI GLEDE NA OZNAKO ######################################

@bottle.get('/recepti-kategorije/<kategorija>')
def doloceni_recepti_kat(kategorija):
    """
    Vsi recepti izbrane kategorije.
    """
    seznam_idjev = r.dobi_gen_ime(model.Kategorije, kategorija, 'kategorija')
    recepti_izbrane_kategorije = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_kategorije.tpl', izb_kategorija=kategorija,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kategorije)


@bottle.get('/<param>/uredi_kategorija/<kategorija>')
def uredi_kategorija(param, kategorija):
    """
    Recepti izbrane kategorije, urejeni po določenem stolpcu
    """
    seznam_idjev = r.dobi_gen_ime(model.Kategorije, kategorija, 'kategorija')
    recepti_izbrane_kategorije = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]
    recepti_izbrane_kategorije.sort(key = operator.attrgetter(param))

    return template_user('views/doloceni_recepti_kategorije.tpl', izb_kategorija=kategorija,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kategorije)


@bottle.get('/recepti-kulinarike/<kulinarika>')
def doloceni_recepti_kul(kulinarika):
    """
    Vsi recepti izbrane kulinarike.
    """
    seznam_idjev = r.dobi_gen_ime(model.Kulinarike, kulinarika, 'kulinarika')
    recepti_izbrane_kulinarike = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_kulinarike.tpl', izb_kulinarika=kulinarika,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kulinarike)

@bottle.get('/<param>/recepti-kulinarike/<kulinarika>')
def uredi_kulinarika(param, kulinarika):
    """
    Recepti izbrane kulinarike, urejeni po določenem stolpcu
    """
    seznam_idjev = r.dobi_gen_ime(model.Kulinarike, kulinarika, 'kulinarika')
    recepti_izbrane_kulinarike = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]
    recepti_izbrane_kulinarike.sort(key = operator.attrgetter(param))

    return template_user('views/doloceni_recepti_kulinarike.tpl', izb_kulinarika=kulinarika,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kulinarike)

@bottle.get('/recepti-oznake/<oznaka>')
def doloceni_recepti_oz(oznaka):
    """
    Vsi recepti izbrane oznake.
    """
    seznam_idjev = r.dobi_gen_ime(model.Oznake, oznaka, 'oznaka')
    recepti_izbrane_oznake = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_oznake.tpl', izb_oznaka=oznaka,
                                                                kategorije=kategorije,
                                                                kulinarike=kulinarike,
                                                                oznake=oznake,
                                                                recepti=recepti_izbrane_oznake)

@bottle.get('/<param>/recepti-oznake/<oznaka>')
def uredi_oznaka(param, oznaka):
    """
    Recepti izbrane oznake, urejeni po določenem stolpcu
    """
    seznam_idjev = r.dobi_gen_ime(model.Oznake, oznaka, 'oznaka')
    recepti_izbrane_oznake = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]
    recepti_izbrane_oznake.sort(key = operator.attrgetter(param))

    return template_user('views/doloceni_recepti_oznake.tpl', izb_oznaka=oznaka,
                                                                kategorije=kategorije,
                                                                kulinarike=kulinarike,
                                                                oznake=oznake,
                                                                recepti=recepti_izbrane_oznake)


############################################ STRAN RECEPTA ############################################  

@bottle.post('/<id>/')
def pojdi_na_recept(id):
    return redirect(url('recept', id=id))


@bottle.get('/recept/<id>')
def recept(id):
    """
    Določen recept z vsemi potrebnimi podatki in komentarji.
    """
    recept = r.dobi_gen_id(model.Recepti, id,'id')
    sestavine = r.dobi_vse_gen_id(model.SestavineReceptov, id,'id_recepta')
    postopek = r.dobi_vse_gen_id_urejeno(model.Postopki, 'st_koraka', id,'id_recepta')
    nutrientske_vrednosti = r.dobi_nutrientske_vrednosti(id)
    kategorije_recepta = [x.kategorija for x in r.dobi_vse_gen_id(model.Kategorije, id,'id_recepta')]
    kulinarike_recepta = [x.kulinarika for x in r.dobi_vse_gen_id(model.Kulinarike, id,'id_recepta')]
    oznake_recepta = [x.oznaka for x in r.dobi_vse_gen_id(model.Oznake, id,'id_recepta')]
    komentarji = r.dobi_vse_gen_id(model.Komentarji2, id, 'id_recepta')
    slovarji_komentarjev = [r.slovar_komentarja(x) for x in komentarji]
    return template('views/recept.tpl', id=recept.id,
                                                         kategorije=kategorije,
                                                         kulinarike=kulinarike,
                                                         oznake=oznake,
                                                         recept=recept,
                                                         sestavine_recepta=sestavine,
                                                         postopek=postopek,
                                                         nutrientske_vrednosti=nutrientske_vrednosti,
                                                         kategorije_recepta=kategorije_recepta,
                                                         kulinarike_recepta=kulinarike_recepta,
                                                         slovarji_komentarjev=slovarji_komentarjev,
                                                         oznake_recepta=oznake_recepta,
                                                         vse_sestavine=vse_sestavine)


########################################### BRISANJE RECEPTA ########################################### 

@bottle.post('/izbrisi-recept')
@cookie_required
def izbrisi_recept():
    """ Gumb na strani, kjer je več receptov """
    id = bottle.request.forms.getunicode('recept')
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    return redirect(url('vsi_recepti_prijava'))


@bottle.post('/izbrisi-recept/<id>')
@cookie_required
def izbrisi_recept_id(id):
    """ Gumb na strani izbranega recepta """
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    return redirect(url('vsi_recepti_prijava'))


########################################### UREJANJE RECEPTA ########################################### 

@bottle.get('/urejanje-recepta/<id>')
@cookie_required
def urejanje_recepta(id):
    """
    Pridobimo stran za urejanje recepta, pazimo da lahko recepti še nimajo vseh potrebnih podatkov.
    """
    try:
        nutrientske_vrednosti = r.dobi_nutrientske_vrednosti(id)
    except:
        nutrientske_vrednosti = model.NutrientskeVrednosti(
        id_recepta=id,
        kalorije=0,
        proteini=0,
        ogljikovi_hidrati=0,
        mascobe=0)
    try:
        sestavine = r.dobi_vse_gen_id(model.SestavineReceptov, id,'id_recepta')
    except:
        sestavine = model.SestavineReceptov(
            id_recepta=id,
            kolicina='',
            enota='',
            sestavina=''
        )
    try:
        postopek = r.dobi_vse_gen_id_urejeno(model.Postopki, 'st_koraka', id,'id_recepta')
    except:
        postopek = model.Postopki(
            id_recepta=id,
            st_koraka=-1,
            postopek=""
        )
    try:
        kategorije_recepta = [x.kategorija for x in r.dobi_vse_gen_id(model.Kategorije, id,'id_recepta')]
    except:
        kategorije_recepta = []
    try:
        kulinarike_recepta = [x.kulinarika for x in r.dobi_vse_gen_id(model.Kulinarike, id,'id_recepta')]
    except:
        kulinarike_recepta = []
    try:
        oznake_recepta = [x.oznaka for x in r.dobi_vse_gen_id(model.Oznake, id,'id_recepta')]
    except:
        oznake_recepta = []
    return template_user('views/urejanje_recepta.tpl', recept = r.dobi_gen_id(model.Recepti, id,'id'),
                                                         kategorije=kategorije,
                                                         kulinarike=kulinarike,
                                                         oznake=oznake,
                                                         postopek=postopek,
                                                         sestavine_recepta=sestavine,
                                                         nutrientske_vrednosti=nutrientske_vrednosti,
                                                         vse_sestavine=vse_sestavine,
                                                         kategorije_recepta=kategorije_recepta,
                                                         kulinarike_recepta=kulinarike_recepta,
                                                         oznake_recepta=oznake_recepta)


#Funkcije za dodajanje, brisanje in urejanje sestavin, postopka, oznak, kategorij in kulinarik.

@bottle.post('/dodaj-sestavino/<id>')
def dodaj_sestavino(id):
    sestavina = str(bottle.request.forms.getunicode('dodana-sestavina'))
    sestavine = [x.ime for x in r.dobi_razlicne_gen_po_abecedi(model.Sestavine, 'ime')]
    if sestavina in sestavine:
        enota =  str(bottle.request.forms.getunicode('dodana-enota'))
        kolicina =  str(bottle.request.forms.getunicode('dodana-kolicina'))

        r.dodaj_sestavino(model.SestavineReceptov(
                id_recepta=id,
                sestavina=sestavina,
                kolicina=kolicina,
                enota=enota
            ))

        nutrienti = r.dobi_nutrientske_vrednosti(id)
        s = model.SestavineReceptov(int(id), kolicina, enota, sestavina)
        r.pristej_nutriente(nutrienti, s)

        return redirect(url('urejanje_recepta', id=id)) 
    else:       
        return redirect(url('dodaj_novo_sestavino_get', id=id))


@bottle.post('/izbrisi-sestavino/<id>')
def brisi_sestavino(id):
    ime = bottle.request.forms.getunicode('sestavina')
    s = r.najdi_sestavino(id,ime)
    nutrienti = r.dobi_nutrientske_vrednosti(id)
    r.odstej_nutriente(nutrienti, s)
    r.izbrisi_gen(model.SestavineReceptov, ime, id_col = "sestavina")
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/dodaj-postopek/<id>')
def dodaj_postopek_post(id):
    postopek =  str(bottle.request.forms.getunicode('dodan-postopek'))
    vsi_koraki = r.dobi_vse_gen_id(model.Postopki, id, "id_recepta")
    zadnji_korak = max([x.st_koraka for x in vsi_koraki] + [0])

    r.dodaj_postopek(model.Postopki(
        id_recepta=id,
        postopek=postopek,
        st_koraka=zadnji_korak + 1
    ))
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/izbrisi-postopek/<id>')
def brisi_postopek(id):
    korak = bottle.request.forms.getunicode('korak')
    r.izbrisi_gen(model.Postopki, korak, "postopek")
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/uredi-postopek/<id>')
def uredi_postopek(id):
    opis = str(bottle.request.forms.getunicode('spremenjen-postopek'))
    st_koraka = bottle.request.forms.getunicode('nov_korak')
    p = model.Postopki(
        id_recepta=id,
        st_koraka=st_koraka,
        postopek=opis
    )
    r.uredi_postopek(p)
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/dodaj-kategorijo/<id>')
def dodaj_kategorijo(id):
    kategorije = bottle.request.forms.getall('kategorija')
    for k in kategorije:
        r.dodaj_gen_brez_serial(model.Kategorije(
            id_recepta=id,
            kategorija=k
        ))
    return redirect(url('urejanje_recepta', id=id))

@bottle.post('/izbrisi-kategorijo/<id>')
def izbrisi_kategorijo(id):
    kategorija = bottle.request.forms.getunicode('kategorija')
    r.izbrisi_dva_pogoja(model.Kategorije, kategorija, "kategorija", id, "id_recepta")
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/dodaj-kulinariko/<id>')
def dodaj_kulinariko(id):
    kulinarike = bottle.request.forms.getall('kulinarika')
    for k in kulinarike:
        r.dodaj_gen_brez_serial(model.Kulinarike(
            id_recepta=id,
            kulinarika=k
        ))
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/izbrisi-kulinariko/<id>')
def izbrisi_kulinariko(id):
    kulinarika = bottle.request.forms.getunicode('kulinarika')
    r.izbrisi_dva_pogoja(model.Kulinarike, kulinarika, "kulinarika", id, "id_recepta")
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/dodaj-oznako/<id>')
def dodaj_oznako(id):
    oznake = bottle.request.forms.getall('oznaka')
    for o in oznake:
        r.dodaj_gen_brez_serial(model.Oznake(
            id_recepta=id,
            oznaka=o
        ))
    return redirect(url('urejanje_recepta', id=id))


@bottle.post('/izbrisi-oznako/<id>')
def izbrisi_oznako(id):
    oznaka = bottle.request.forms.getunicode('oznaka')
    r.izbrisi_dva_pogoja(model.Oznake, oznaka, "oznaka", id, "id_recepta")
    return redirect(url('urejanje_recepta', id=id))


########################################### DODAJANJE RECEPTA ########################################### 

@bottle.get('/dodaj-recept')
@cookie_required
def dodaj_recept_get():
    return template_user('views/dodaj_recept.tpl', recept = model.Recepti(),
                                                         kategorije=kategorije,
                                                         kulinarike=kulinarike,
                                                         oznake=oznake)
    

@bottle.post('/dodaj-recept')
def dodaj_recept_post():
    """
    Dodajanje novega recepta. Za začetek potrebuje štiri osnovne informacije kot so ime, štrvilo porcij, čas priprave in 
    čas kuhanja. Nato pa nas stran preusmeri na urejanje recepta, kjer lahko dodajamo postopek, sestavine, oznake, kulinarike in 
    kategorije in jih brišemo. 
    """
    ime = str(bottle.request.forms.getunicode('ime'))
    st_porcij = int(bottle.request.forms.getunicode('st_porcij'))
    cas_priprave = int(bottle.request.forms.getunicode('cas_priprave'))
    cas_kuhanja = int(bottle.request.forms.getunicode('cas_kuhanja'))
    id_uporabnika = int(bottle.request.get_cookie("id"))

    recept = r.dodaj_recept(model.Recepti(
        ime = ime,
        st_porcij=st_porcij,
        cas_priprave=cas_priprave,
        cas_kuhanja=cas_kuhanja,
        id_uporabnika=id_uporabnika
    ))
    r.dodaj_gen_brez_serial(model.NutrientskeVrednosti(
        id_recepta=recept.id
        ))

    return redirect(url('urejanje_recepta', id=recept.id))


########################################### DODAJANJE SESTAVIN ########################################### 

@bottle.get('/dodaj-novo-sestavino/<id>')
@cookie_required
def dodaj_novo_sestavino_get(id):
    recept = r.dobi_gen_id(model.Recepti, id,'id')
    return template('views/dodaj_novo_sestavino.tpl', id=recept.id,
                          oznake=oznake,kategorije=kategorije,kulinarike=kulinarike)

@bottle.post('/dodaj-novo-sestavino/<id>')
def dodaj_novo_sestavino_post(id):
    """
    Ker se ob dodajanju sestavin pri receptu preračunajo njegove nutrientske vrednosti, mora stran vsako sestavino poznati
    in imeti podatke o njenih nutrientskih vrednostih. S to funkcijo čisto novo sestavino dodamo na seznam vseh nato jo bomo
    lahko dodali na recept.
    """
    ime =  str(bottle.request.forms.getunicode('ime'))
    kalorije = float(bottle.request.forms.getunicode('kalorije'))
    proteini = float(bottle.request.forms.getunicode('proteini'))
    ogljikovi_hidrati = float(bottle.request.forms.getunicode('ogljikovi-hidrati'))
    mascobe = float(bottle.request.forms.getunicode('mascobe'))

    r.dodaj_gen(model.Sestavine(
        ime=ime,
        kalorije=kalorije,
        proteini=proteini,
        ogljikovi_hidrati=ogljikovi_hidrati,
        mascobe=mascobe
    ))
    return redirect(url('urejanje_recepta', id=id))


############################################## KOMENTIRANJE ############################################## 

@bottle.post('/dodaj-komentar/<id>')
@cookie_required
def dodaj_komentar(id):
    id_uporabnika = int(bottle.request.get_cookie('id'))
    vsebina = str(bottle.request.forms.getunicode('dodan-komentar'))

    r.dodaj_komentar(model.Komentarji2(
        id_uporabnika = id_uporabnika,
        id_recepta = id,
        vsebina = vsebina
    ))
    redirect(url('recept', id=id))



#bottle.run(reloader=True, debug=True)
# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)



