from bottletext import get, post, run, request, template, redirect, static_file, url, response, template_user

import bottletext
from operator import mod
import bottle 
import model
import Database
from Database import Repo
from uporabnik import AuthService
from functools import wraps

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


r = Database.Repo()
repo = Repo()
auth = AuthService(repo)

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

@bottle.get('/')
def vsi_recepti():
    recepti = r.dobi_vse_gen(model.Recepti)
    return template('views/front-page.tpl', kategorije=kategorije,
                                            kulinarike=kulinarike,
                                            oznake=oznake,
                                            recepti=recepti)


@bottle.get('/prijava')
def prijava_get():
    return template('prijava.tpl', napaka=None)


@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovem id.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = str(request.forms.get('uporabnisko_ime'))
    password = str(request.forms.get('geslo'))

    if not auth.obstaja_uporabnik(username):
        return template("views/registracija.tpl", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        bottle.response.set_cookie("uporabnisko_ime", username)
        bottle.response.set_cookie("id", str(prijava.id))

        redirect(url('/recepti'))
        
    else:
        return template("prijava.tpl", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
    

@post('/registracija')
def registracija():
    username = str(request.forms.get('uporabnisko_ime'))
    password = str(request.forms.get('geslo'))

    if auth.dodaj_uporabnika(username,password):
        prijava = auth.prijavi_uporabnika(username, password)
    else:
        return bottletext.template("registracija.tpl", napaka="Uporabnik s tem že obstaja")
    
    if prijava:
        response.set_cookie("uporabnisko_ime", username)
        response.set_cookie("id", str(prijava.id))

        bottle.redirect('/recepti')

    
@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    bottle.response.delete_cookie("uporabnisko_ime")
    bottle.response.delete_cookie("id")
    
    return template('prijava.tpl', napaka=None)




kategorije = [x.kategorija for x in r.dobi_razlicne_gen(model.Kategorije, 'kategorija', 181, 0)]
kulinarike = [x.kulinarika for x in r.dobi_razlicne_gen(model.Kulinarike, 'kulinarika', 181, 0)]
oznake = [x.oznaka for x in r.dobi_razlicne_gen(model.Oznake, 'oznaka', 181, 0)]
vse_sestavine = r.dobi_vse_gen(model.Sestavine)


@bottle.get('/recepti')
def vsi_recepti_prijava():
    recepti = r.dobi_vse_gen(model.Recepti)
    return template_user('views/front_prijava.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=recepti)

@bottle.get('/moji-recepti')
@cookie_required
def moji_recepti():
    uporabnik = bottle.request.get_cookie('id')
    uporabnikovi_recepti = r.dobi_vse_gen_id(model.Recepti, uporabnik, "id_uporabnika")
    return template_user('views/front_prijava.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=uporabnikovi_recepti)


@bottle.get('/recepti-kategorije/<kategorija>')
def doloceni_recepti(kategorija):
    seznam_idjev = r.dobi_gen_ime(model.Kategorije, kategorija, 'kategorija')
    recepti_izbrane_kategorije = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_kategorije.tpl', kategorija=kategorija,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kategorije)

@bottle.get('/recepti-kulinarike/<kulinarika>')
def doloceni_recepti(kulinarika):
    seznam_idjev = r.dobi_gen_ime(model.Kulinarike, kulinarika, 'kulinarika')
    recepti_izbrane_kulinarike = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_kulinarike.tpl', kulinarika=kulinarika,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kulinarike)

@bottle.get('/recepti-oznake/<oznaka>')
def doloceni_recepti(oznaka):
    seznam_idjev = r.dobi_gen_ime(model.Oznake, oznaka, 'oznaka')
    recepti_izbrane_oznake = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return template_user('views/doloceni_recepti_oznake.tpl', oznaka=oznaka,
                                                                kategorije=kategorije,
                                                                kulinarike=kulinarike,
                                                                oznake=oznake,
                                                                recepti=recepti_izbrane_oznake)

@bottle.post('/<id>/')
def pojdi_na_recept(id):
    return bottle.redirect('/recept/{}'.format(id))

@bottle.get('/recept/<id>')
def recept(id):
    recept = r.dobi_gen_id(model.Recepti, id,'id')
    sestavine = r.dobi_vse_gen_id(model.SestavineReceptov, id,'id_recepta')
    postopek = r.dobi_vse_gen_id(model.Postopki, id,'id_recepta')
    nutrientske_vrednosti = r.dobi_nutrientske_vrednosti(id)
    kategorije_recepta = [x.kategorija for x in r.dobi_vse_gen_id(model.Kategorije, id,'id_recepta')]
    kulinarike_recepta = [x.kulinarika for x in r.dobi_vse_gen_id(model.Kulinarike, id,'id_recepta')]
    oznake_recepta = [x.oznaka for x in r.dobi_vse_gen_id(model.Oznake, id,'id_recepta')]
    return bottle.template('views/urejanje_recepta.tpl', id=recept.id,
                                                         kategorije=kategorije,
                                                         kulinarike=kulinarike,
                                                         oznake=oznake,
                                                         recept=recept,
                                                         sestavine_recepta=sestavine,
                                                         postopek=postopek,
                                                         nutrientske_vrednosti=nutrientske_vrednosti,
                                                         kategorije_recepta=kategorije_recepta,
                                                         kulinarike_recepta=kulinarike_recepta,
                                                         oznake_recepta=oznake_recepta,
                                                         vse_sestavine=vse_sestavine)

@bottle.get('/dodaj-recept')
def dodaj_recept_get():
    return template_user('views/dodaj_recept.tpl', recept = model.ReceptPosSes(), kategorija=kategorije)

@bottle.post('/dodaj-recept')
def dodaj_recept_post():
    ime = str(bottle.request.forms.getunicode('ime'))
    st_porcij = int(bottle.request.forms.getunicode('st_porcij'))
    cas_priprave = int(bottle.request.forms.getunicode('cas_priprave'))
    cas_kuhanja = int(bottle.request.forms.getunicode('cas_kuhanja'))
    kategorija = str(bottle.request.forms.getunicode('ime_kategorije'))
    kulinarika = str(bottle.request.forms.getunicode('kulinarika'))
    oznaka = str(bottle.request.forms.getunicode('oznaka'))

    recept = r.dodaj_recept(model.Recepti(
        ime = ime,
        st_porcij=st_porcij,
        cas_priprave=cas_priprave,
        cas_kuhanja=cas_kuhanja
    ))

    r.dodaj_kategorijo(model.Kategorije(
        id_recepta=recept.id,
        kategorija=kategorija
    ))

    r.dodaj_kulinariko(model.Kulinarike(
        id_recepta=recept.id,
        kulinarika=kulinarika
    ))

    r.dodaj_oznako(model.Oznake(
        id_recepta=recept.id,
        oznaka = oznaka
    ))

    bottle.redirect('/recept/{}'.format(recept.id))


@bottle.post('/izbrisi-recept')
def izbrisi_recept():
    id = bottle.request.forms.getunicode('recept')
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    bottle.redirect('/')

@bottle.post('/izbrisi-recept/<id>')
def izbrisi_recept_id(id):
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    bottle.redirect('/')


@bottle.post('/dodaj-sestavino/<id>')
def dodaj_sestavino(id):
    sestavina = str(bottle.request.forms.getunicode('dodana-sestavina'))
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

    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/izbrisi-sestavino/<id>')
def brisi_sestavino(id):
    ime = bottle.request.forms.getunicode('sestavina')
    r.izbrisi_gen(model.SestavineReceptov, ime, id_col = "sestavina")
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/dodaj-postopek/<id>')
def dodaj_postopek_post(id):
    postopek =  str(bottle.request.forms.getunicode('dodan-postopek'))
    vsi_koraki = r.dobi_vse_gen_id(model.Postopki, id, "id_recepta")
    zadnji_korak = max([x.st_koraka for x in vsi_koraki])

    r.dodaj_postopek(model.Postopki(
        id_recepta=id,
        postopek=postopek,
        st_koraka=zadnji_korak + 1
    ))
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/izbrisi-postopek/<id>')
def brisi_postopek(id):
    korak = bottle.request.forms.getunicode('korak')
    r.izbrisi_gen(model.Postopki, korak, "koraka")
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/uredi-postopek/<id>')
def uredi_postopek(id):
    opis = str(bottle.request.forms.getunicode('spremenjen-postopek'))
    st_koraka = bottle.request.forms.getunicode('nov_korak')
    p = model.Postopki(
        id_recepta=id,
        st_koraka=st_koraka,
        postopek=opis
    )
    print(p)
    r.uredi_postopek(p)
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/dodaj-kategorijo/<id>')
def dodaj_kategorijo(id):
    kategorije = bottle.request.forms.getall('izbrane-kategorije')
    for k in kategorije:
        r.dodaj_kategorijo(model.Kategorije(
            id_recepta=id,
            kategorija=k
        ))
    bottle.redirect('/recept/{}'.format(id))

@bottle.post('/izbrisi-kategorijo/<id>')
def izbrisi_kategorijo(id):
    kategorija = bottle.request.forms.getunicode('kategorija')
    r.izbrisi_dva_pogoja(model.Kategorije, kategorija, "kategorija", id, "id_recepta")
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/dodaj-kulinariko/<id>')
def dodaj_kategorijo(id):
    kulinarike = bottle.request.forms.getall('izbrane-kulinarike')
    for k in kulinarike:
        r.dodaj_kulinariko(model.Kulinarike(
            id_recepta=id,
            kulinarika=k
        ))
    bottle.redirect('/recept/{}'.format(id))

@bottle.post('/izbrisi-kulinariko/<id>')
def izbrisi_kategorijo(id):
    kulinarika = bottle.request.forms.getunicode('kulinarika')
    r.izbrisi_dva_pogoja(model.Kulinarike, kulinarika, "kulinarika", id, "id_recepta")
    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/dodaj-oznako/<id>')
def dodaj_kategorijo(id):
    oznake = bottle.request.forms.getall('izbrane-oznake')
    for o in oznake:
        r.dodaj_oznako(model.Oznake(
            id_recepta=id,
            oznaka=o
        ))
    bottle.redirect('/recept/{}'.format(id))

@bottle.post('/izbrisi-oznako/<id>')
def izbrisi_kategorijo(id):
    oznaka = bottle.request.forms.getunicode('oznaka')
    r.izbrisi_dva_pogoja(model.Oznake, oznaka, "oznaka", id, "id_recepta")
    bottle.redirect('/recept/{}'.format(id))


#bottle.run(reloader=True, debug=True)
# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)